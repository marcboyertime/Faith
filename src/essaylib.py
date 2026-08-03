from __future__ import annotations

import hashlib
import html
import re
import unicodedata
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


class IntegrityError(RuntimeError):
    pass


def slugify(value: str) -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value or "block"


def visible_inline(value: str) -> str:
    value = re.sub(r"!\[([^]]*)\]\([^)]*\)", r"\1", value)
    value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1", value)
    value = re.sub(r"\[\^([^]]+)\]", r"\1", value)
    value = re.sub(r"<https?://([^>]+)>", r"https://\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("**", "").replace("__", "").replace("~~", "").replace("`", "")
    value = re.sub(r"(?<!\w)\*|\*(?!\w)", "", value)
    value = re.sub(r"(?<!\w)_|_(?!\w)", "", value)
    return re.sub(r"\s+", " ", html.unescape(value)).strip()


def token_sequence(value: str) -> list[str]:
    return re.findall(r"[\w]+(?:['’][\w]+)?|[^\w\s]", value, flags=re.UNICODE)


@dataclass(frozen=True)
class Block:
    id: str
    kind: str
    level: int
    text: str
    visible: str
    marker: str = ""


@dataclass
class Essay:
    essay_id: str
    path: Path
    sha256: str
    blocks: list[Block]

    @property
    def visible_text(self) -> str:
        return " ".join(block.visible for block in self.blocks)

    @property
    def word_count(self) -> int:
        return len(re.findall(r"[\w]+(?:['’][\w]+)?", self.visible_text, flags=re.UNICODE))


def _make_id(kind: str, level: int, text: str, counts: dict[str, int]) -> str:
    if kind == "heading":
        base = f"h{level}-{slugify(text)}"
    else:
        base = f"{kind}"
    counts[base] = counts.get(base, 0) + 1
    return base if counts[base] == 1 else f"{base}-{counts[base]}"


def parse_markdown(essay_id: str, path: Path, expected_sha256: str | None = None) -> Essay:
    raw = path.read_bytes()
    sha256 = hashlib.sha256(raw).hexdigest()
    if expected_sha256 and sha256 != expected_sha256:
        raise IntegrityError(
            f"{essay_id}: canonical SHA-256 mismatch; expected {expected_sha256}, got {sha256}"
        )
    lines = raw.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[Block] = []
    counts: dict[str, int] = {}
    i = 0

    def add(kind: str, level: int, text: str, marker: str = "") -> None:
        clean = text.strip()
        if not clean:
            return
        block_id = _make_id(kind, level, clean, counts)
        blocks.append(Block(block_id, kind, level, clean, visible_inline(clean), marker))

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped or stripped == "---":
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", stripped)
        if heading:
            add("heading", len(heading.group(1)), heading.group(2))
            i += 1
            continue
        footnote = re.match(r"^\[\^([^]]+)\]:\s*(.*)$", stripped)
        if footnote:
            add("footnote", 0, f"{footnote.group(1)}: {footnote.group(2)}", footnote.group(1))
            i += 1
            continue
        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]).strip())
                i += 1
            add("blockquote", 0, " ".join(quote_lines))
            continue
        list_match = re.match(r"^\s*([-*+]|\d+[.)])\s+(.+)$", stripped)
        if list_match:
            add("list_item", 0, list_match.group(2), list_match.group(1))
            i += 1
            continue
        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt == "---" or re.match(r"^(#{1,6})\s+", nxt) or nxt.startswith(">") or re.match(r"^\s*([-*+]|\d+[.)])\s+", nxt) or re.match(r"^\[\^([^]]+)\]:", nxt):
                break
            paragraph_lines.append(nxt)
            i += 1
        add("paragraph", 0, " ".join(paragraph_lines))
    return Essay(essay_id, path, sha256, blocks)


class _VisibleHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[tuple[str, str]] = []
        self.current: tuple[str, list[str]] | None = None
        self.supporting_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        attrs_dict = dict(attrs)
        if "data-supporting" in attrs_dict:
            self.supporting_depth += 1
        if self.supporting_depth:
            return
        block_id = attrs_dict.get("data-essay-block-id")
        if block_id:
            self.current = (block_id, [])

    def handle_endtag(self, tag: str) -> None:
        if self.supporting_depth:
            if tag in {"figure", "div", "aside", "section", "span", "nav", "footer", "header"}:
                self.supporting_depth = max(0, self.supporting_depth - 1)
            return
        if self.current and tag in {"h1", "h2", "h3", "h4", "h5", "h6", "p", "blockquote", "li", "aside"}:
            self.blocks.append((self.current[0], "".join(self.current[1])))
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.current and not self.supporting_depth:
            self.current[1].append(data)


def _context(items: list[str], index: int, radius: int = 2) -> str:
    lo = max(0, index - radius)
    hi = min(len(items), index + radius + 1)
    return " | ".join(items[lo:hi])


def verify_rendered_html(essay: Essay, rendered_html: str) -> dict:
    parser = _VisibleHTMLParser()
    parser.feed(rendered_html)
    actual_ids = [item[0] for item in parser.blocks]
    expected_ids = [block.id for block in essay.blocks]
    if actual_ids != expected_ids:
        first = next((i for i, (a, b) in enumerate(zip(actual_ids, expected_ids)) if a != b), min(len(actual_ids), len(expected_ids)))
        raise IntegrityError(
            f"{essay.essay_id}: structural block mismatch at position {first}; "
            f"expected {expected_ids[first:first + 2]}, actual {actual_ids[first:first + 2]}"
        )
    actual_text = [visible_inline(text) for _, text in parser.blocks]
    expected_text = [block.visible for block in essay.blocks]
    for index, (expected, actual) in enumerate(zip(expected_text, actual_text)):
        if expected != actual:
            expected_tokens = token_sequence(expected)
            actual_tokens = token_sequence(actual)
            token_at = next((i for i, (a, b) in enumerate(zip(expected_tokens, actual_tokens)) if a != b), min(len(expected_tokens), len(actual_tokens)))
            raise IntegrityError(
                f"{essay.essay_id} block {essay.blocks[index].id}: visible-text mismatch; "
                f"expected={expected!r}; actual={actual!r}; "
                f"nearby={_context(expected_text, index)}; first token mismatch={token_at}"
            )
    expected_tokens = token_sequence(" ".join(expected_text))
    actual_tokens = token_sequence(" ".join(actual_text))
    if expected_tokens != actual_tokens:
        token_at = next((i for i, (a, b) in enumerate(zip(expected_tokens, actual_tokens)) if a != b), min(len(expected_tokens), len(actual_tokens)))
        raise IntegrityError(
            f"{essay.essay_id}: ordered word-and-punctuation mismatch at token {token_at}; "
            f"expected={expected_tokens[token_at:token_at + 8]}; actual={actual_tokens[token_at:token_at + 8]}"
        )
    return {
        "word_count": essay.word_count,
        "token_count": len(expected_tokens),
        "paragraph_count": sum(block.kind == "paragraph" for block in essay.blocks),
        "heading_count": sum(block.kind == "heading" for block in essay.blocks),
        "quotation_count": sum(block.kind == "blockquote" for block in essay.blocks),
        "note_count": sum(block.kind == "footnote" for block in essay.blocks),
        "structural": "PASS",
        "visible": "PASS",
        "tokens": "PASS",
        "final": "PASS",
    }
