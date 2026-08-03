#!/usr/bin/env python3
"""Build the Faith essay library from immutable Markdown sources."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from src.essaylib import IntegrityError, Essay, parse_markdown, verify_rendered_html
from src.visuals import render_visual


ROOT = Path(__file__).resolve().parent
ESSAYS = ("goodness", "resurrection")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def block_text(block) -> str:
    return block.text


def load_essay(essay_id: str) -> Essay:
    content_dir = ROOT / "content" / essay_id
    manifest = read_json(content_dir / "manifest.json")
    return parse_markdown(
        essay_id,
        content_dir / "essay.md",
        expected_sha256=manifest["expected_sha256"],
    )


def chapter_heading(block, essay_id: str) -> bool:
    text = block.visible
    if essay_id == "goodness":
        return block.kind == "heading" and (text.startswith("I.") or text.startswith("II.") or text.startswith("III.") or text.startswith("IV.") or text.startswith("V.") or text.startswith("VI.") or text.startswith("VII.") or text.startswith("VIII.") or text.startswith("IX.") or text == "Overture")
    return block.kind == "heading" and (
        text == "Overture"
        or text.startswith(tuple(f"{n}." for n in ("I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII")))
        or text.startswith("Appendix ")
    )


def logical_heading_level(block, essay_id: str, seen_chapter: bool) -> int:
    if block.kind != "heading":
        return 0
    if block.level == 1 and not seen_chapter:
        return 1
    if chapter_heading(block, essay_id) or block.visible == "Contents":
        return 2
    return min(4, 2 + max(0, block.level - 1))


def title_and_deck(essay: Essay) -> tuple:
    title = next((b for b in essay.blocks if b.kind == "heading" and b.level == 1), None)
    deck = next((b for b in essay.blocks if b.kind == "paragraph"), None)
    return title, deck


def render_inline(raw: str, glossary: list[dict], seen_terms: set[str], allow_terms: bool = True) -> str:
    import html
    import re

    marked = raw
    placeholders: dict[str, str] = {}
    inline_markup: dict[str, str] = {}
    if allow_terms:
        entries = sorted(glossary, key=lambda item: len(item.get("pattern", item["term"])), reverse=True)
        for entry in entries:
            key = entry["key"]
            if key in seen_terms:
                continue
            pattern = entry.get("pattern", entry["term"])
            match = re.search(r"(?<![\w])(" + re.escape(pattern) + r")(?![\w])", marked, re.IGNORECASE)
            if match:
                token = f"@@FAITHTERM{key.upper()}@@"
                placeholders[token] = match.group(1)
                marked = marked[: match.start()] + token + marked[match.end() :]
                seen_terms.add(key)

    def repl_image(match):
        return match.group(1)

    def repl_link(match):
        token = f"@@FAITHLINK{len(inline_markup)}@@"
        inline_markup[token] = '<a href="%s">%s</a>' % (html.escape(match.group(2), quote=True), match.group(1))
        return token

    def repl_footnote(match):
        token = f"@@FAITHNOTE{len(inline_markup)}@@"
        label = match.group(1)
        inline_markup[token] = '<sup class="note-ref"><a href="#note-%s" id="ref-%s">%s</a></sup>' % (html.escape(label, quote=True), html.escape(label, quote=True), html.escape(label))
        return token

    marked = re.sub(r"!\[([^]]*)\]\([^)]*\)", repl_image, marked)
    marked = re.sub(r"\[([^]]+)\]\(([^)]+)\)", repl_link, marked)
    marked = re.sub(r"\[\^([^]]+)\]", repl_footnote, marked)
    marked = html.escape(marked, quote=False)
    marked = re.sub(r"&lt;(https?://[^&]+)&gt;", r'<a href="\1">\1</a>', marked)
    marked = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", marked)
    marked = re.sub(r"__(.+?)__", r"<strong>\1</strong>", marked)
    marked = re.sub(r"\*([^*]+?)\*", r"<em>\1</em>", marked)
    marked = re.sub(r"_([^_]+?)_", r"<em>\1</em>", marked)
    marked = re.sub(r"`([^`]+?)`", r"<code>\1</code>", marked)
    marked = re.sub(r"~~(.+?)~~", r"<del>\1</del>", marked)
    for token, markup in inline_markup.items():
        marked = marked.replace(token, markup)
    for token, display in placeholders.items():
        marked = marked.replace(
            token,
            '<button class="term" type="button" data-term-key="%s" aria-haspopup="dialog">%s</button>'
            % (token.removeprefix("@@FAITHTERM").removesuffix("@@").lower(), html.escape(display)),
        )
    return marked


def render_block(block, essay_id: str, glossary: list[dict], seen_terms: set[str], heading_level: int = 0) -> str:
    import html

    attrs = f'data-essay-block-id="{html.escape(block.id, quote=True)}"'
    if block.kind == "heading":
        tag = f"h{heading_level or 2}"
        return f"<{tag} {attrs}>{render_inline(block.text, glossary, seen_terms)}</{tag}>"
    if block.kind == "blockquote":
        return f'<blockquote class="source-quote" {attrs}>{render_inline(block.text, glossary, seen_terms)}</blockquote>'
    if block.kind == "list_item":
        return f'<ul class="canonical-list"><li {attrs}>{render_inline(block.text, glossary, seen_terms)}</li></ul>'
    if block.kind == "footnote":
        label = html.escape(block.marker or "note")
        return f'<aside class="canonical-note" id="note-{label}" {attrs}><strong>{label}:</strong> {render_inline(block.text, glossary, seen_terms)}</aside>'
    classes = []
    if essay_id == "goodness":
        leading = block.text.strip()
        if leading.startswith('*"'):
            classes.append("objection")
        elif leading.startswith("**") and any(leading.startswith(prefix) for prefix in ("**Weld", "**Attack", "**Assault", "**Objection", "**Failure", "**Fact", "**Contestant")):
            classes.append("argument-card")
    elif essay_id == "resurrection" and block.kind == "paragraph" and block.text.strip().startswith("**"):
        leading = block.visible.lower()
        pressure = ("for the skeptical", "against, or for caution", "why disbelief", "its costs", "fair verdict", "grave damage", "material weakening")
        classes.extend(("resurrection-card", "pressure-card" if leading.startswith(pressure) else "answer-card"))
    class_attr = f' class="{" ".join(classes)}"' if classes else ""
    return f"<p{class_attr} {attrs}>{render_inline(block.text, glossary, seen_terms)}</p>"


def visual_map(manifest: dict) -> dict[str, list[dict]]:
    result: dict[str, list[dict]] = {}
    specs = list(manifest.get("visuals", []))
    specs.extend({**spec, "kind": "pull"} for spec in manifest.get("pulls", []))
    for spec in specs:
        result.setdefault(spec["after"], []).append(spec)
    return result


def volume_tabs(current: str | None, asset_prefix: str) -> str:
    links = []
    for essay_id, label in (("goodness", "GOODNESS"), ("resurrection", "RESURRECTION")):
        active = " is-active" if essay_id == current else ""
        current_attr = ' aria-current="page"' if essay_id == current else ""
        links.append(
            f'<a class="volume-tab{active}" href="{asset_prefix}{essay_id}/index.html"{current_attr}>{label}</a>'
        )
    return "".join(links)


def reader_excluded_ids(essay: Essay) -> set[str]:
    """Keep source-management material out of the public reading edition."""
    if essay.essay_id != "resurrection":
        return set()
    excluded: set[str] = set()
    in_appendices = False
    in_ledger = False
    ledger_headings = {"SECURE NOW", "STILL CONTESTED", "NOT YET PROVEN", "SOURCE CHECKS"}
    editorial_markers = (
        "research scaffold",
        "drafting charter",
        "verification pass",
        "source-verification",
        "source marker",
        "master list",
    )
    for block in essay.blocks:
        if block.kind == "heading" and block.level == 1:
            in_ledger = False
        if block.kind == "heading" and block.visible.startswith("Appendix A"):
            in_appendices = True
        if in_appendices:
            excluded.add(block.id)
            continue
        if block.kind == "heading" and block.visible in ledger_headings:
            in_ledger = True
        if in_ledger:
            excluded.add(block.id)
            continue
        if block.kind == "blockquote" and block.visible.startswith(("A note on this text.", "PRE-VERDICT AUDIT")):
            excluded.add(block.id)
        elif block.kind == "paragraph" and block.visible.startswith("Grade consistency:"):
            excluded.add(block.id)
        elif block.kind == "list_item" and block.visible.startswith(("Appendix A", "Appendix B")):
            excluded.add(block.id)
        elif any(marker in block.visible.lower() for marker in editorial_markers):
            excluded.add(block.id)
    return excluded


def render_essay_page(essay: Essay, manifest: dict, other_essays: list[Essay], asset_prefix: str) -> str:
    import html
    import re

    title, deck = title_and_deck(essay)
    glossary = manifest.get("glossary", [])
    placement = visual_map(manifest)
    excluded_ids = reader_excluded_ids(essay)
    reader_blocks = [block for block in essay.blocks if block.id not in excluded_ids]
    target_ids = {block.id for block in reader_blocks}
    unresolved = sorted(set(placement) - target_ids)
    if unresolved:
        raise IntegrityError(f"{essay.essay_id}: unresolved visual placement IDs: {', '.join(unresolved)}")

    chapters = []
    for block in reader_blocks:
        if chapter_heading(block, essay.essay_id):
            chapters.append((block.id, block.visible))
    chapter_links = "".join(
        f'<a href="#{html.escape(cid)}" data-chapter-link>{html.escape(label.split(" — ")[0][:44])}</a>'
        for cid, label in chapters
    )
    config = {
        "essayId": essay.essay_id,
        "theme": manifest.get("theme", essay.essay_id),
        "glossary": glossary,
        "route": f'/{essay.essay_id}/',
    }

    seen_terms: set[str] = set()
    body: list[str] = []
    chapter_open = False
    seen_chapter = False
    hero_ids = {title.id if title else None, deck.id if deck else None}
    for block in reader_blocks:
        if block.id in hero_ids:
            continue
        if chapter_heading(block, essay.essay_id):
            if chapter_open:
                body.append("</section>")
            body.append(f'<section class="chapter reveal" id="{html.escape(block.id)}" data-chapter="{html.escape(block.id)}">')
            chapter_open = True
            seen_chapter = True
        level = logical_heading_level(block, essay.essay_id, seen_chapter)
        body.append(render_block(block, essay.essay_id, glossary, seen_terms, level))
        for spec in placement.get(block.id, []):
            body.append(render_visual(spec, essay.essay_id, asset_prefix))
    if chapter_open:
        body.append("</section>")

    hero_title = render_block(title, essay.essay_id, [], set(), 1) if title else ""
    hero_deck = render_block(deck, essay.essay_id, [], set(), 0) if deck else ""
    title_text = title.visible if title else essay.essay_id.title()
    deck_text = deck.visible if deck else ""
    chapter_count = len(chapters)
    reader_word_count = sum(len(re.findall(r"[\w]+(?:['’][\w]+)?", block.visible, flags=re.UNICODE)) for block in reader_blocks)
    minutes = max(1, round(reader_word_count / 190))
    theme = manifest.get("theme", essay.essay_id)
    hero = manifest.get("hero", {})
    if hero.get("asset"):
        hero_media = f'<img class="hero-art" src="{asset_prefix}assets/{html.escape(hero["asset"])}" alt="{html.escape(hero.get("alt", ""))}" fetchpriority="high">'
    else:
        hero_media = '<div class="tomb-threshold" aria-hidden="true"><span></span></div>'

    cards = ""
    for other in other_essays:
        other_title, other_deck = title_and_deck(other)
        cards += (
            f'<a class="volume-link" href="../{other.essay_id}/index.html"><span>{html.escape(other.essay_id.upper())}</span>'
            f'<strong>{html.escape(other_title.visible if other_title else other.essay_id.title())}</strong>'
            f'<em>{html.escape(other_deck.visible if other_deck else "")}</em></a>'
        )
    tabs = volume_tabs(essay.essay_id, asset_prefix)
    return f'''<!doctype html>
<html lang="en" data-theme="dark" data-essay="{html.escape(theme)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title_text)} — Faith Essay Library</title>
<meta name="description" content="{html.escape(deck_text)}">
<link rel="icon" href="{asset_prefix}assets/favicon.svg">
<link rel="stylesheet" href="{asset_prefix}assets/site.css">
</head>
<body>
<div class="progress" id="progress" aria-hidden="true"></div>
<header class="top on has-volume-tabs" id="topbar">
  <a class="brand" href="{("../" if essay.essay_id else "")}index.html">FAITH / ESSAYS</a>
  <nav class="volume-tabs" aria-label="Essay volumes">{tabs}</nav>
  <span class="chap-label" id="chap-label" aria-live="polite"></span>
  <div class="tools">
    <a class="tool-link" href="{("../" if essay.essay_id else "")}index.html">LIBRARY</a>
    <button class="tool-btn" id="menu-btn" type="button" aria-expanded="false" aria-controls="menu-overlay">CHAPTERS</button>
    <button class="tool-btn" id="theme-btn" type="button">LIGHT / DARK</button>
  </div>
</header>
<nav class="rail" aria-label="Chapter navigation">{chapter_links}</nav>
<main>
<article class="essay-content" id="essay-content">
  <section class="hero" id="hero">
    {hero_media}
    <div class="hero-veil" aria-hidden="true"></div>
    <canvas id="dust" aria-hidden="true"></canvas>
    <div class="hero-inner">
      <div class="kicker" data-supporting="true">{html.escape(manifest.get("label", "AN INTERACTIVE READING"))}</div>
      {hero_title}
      <div class="hero-dek">{hero_deck}</div>
      <div class="meta" data-supporting="true">{chapter_count} CHAPTERS &nbsp;·&nbsp; {reader_word_count:,} WORDS &nbsp;·&nbsp; {minutes} MIN READ</div>
    </div>
    <a class="begin" href="#{html.escape(chapters[0][0] if chapters else "essay-content")}" data-supporting="true">BEGIN THE READING <span>↓</span></a>
  </section>
  <div class="reading-key" data-supporting="true">
    <span><i class="key-dot key-gold"></i>essay text</span>
    <span><i class="key-dot key-rose"></i>questions raised</span>
    <span><i class="key-dot key-line"></i>visual guide</span>
  </div>
  <div class="essay-body">{"".join(body)}</div>
</article>
<footer data-supporting="true">
  <div class="finis">END OF VOLUME</div>
  <p>A long-form reading in the Faith essay library.</p>
  <p><a href="{("../" if essay.essay_id else "")}index.html">Return to the essay library</a></p>
</footer>
</main>
<div class="menu-overlay" id="menu-overlay" hidden>
  <div class="menu-panel" role="dialog" aria-modal="true" aria-labelledby="menu-title">
    <button class="menu-close" id="menu-close" type="button" aria-label="Close chapter menu">×</button>
    <div class="menu-title" id="menu-title">{html.escape(title_text)}</div>
    {chapter_links}
    <div class="menu-volumes">{cards}</div>
  </div>
</div>
<aside class="term-card" id="term-card" role="dialog" aria-live="polite" aria-label="Definition" hidden></aside>
<script>window.ESSAY_CONFIG = {json.dumps(config, ensure_ascii=False)};</script>
<script src="{asset_prefix}assets/site.js" defer></script>
</body>
</html>'''


def render_library(essays: list[Essay]) -> str:
    import html

    cards = []
    for essay in essays:
        title, deck = title_and_deck(essay)
        chapter_count = sum(1 for b in essay.blocks if chapter_heading(b, essay.essay_id))
        subject = "Metaphysics, ethics & natural theology" if essay.essay_id == "goodness" else "History, philosophy & Catholic theology"
        route = f"{essay.essay_id}/index.html"
        cards.append(
            f'''<a class="library-card {essay.essay_id}" href="{route}">
              <span class="card-number">VOLUME {1 if essay.essay_id == "goodness" else 2:02d}</span>
              <h2>{html.escape(title.visible if title else essay.essay_id.title())}</h2>
              <p>{html.escape(deck.visible if deck else "")}</p>
              <div class="card-meta"><span>{html.escape(subject)}</span><span>{essay.word_count:,} words · {chapter_count} chapters</span></div>
              <span class="read-link">ENTER THE READING <b>↗</b></span>
            </a>'''
        )
    return f'''<!doctype html>
<html lang="en" data-theme="dark" data-essay="library">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Faith — An Essay Library</title>
<meta name="description" content="A contemplative library of complete Catholic philosophical and theological essays.">
<link rel="icon" href="assets/favicon.svg">
<link rel="stylesheet" href="assets/site.css">
</head>
<body class="library-page">
<header class="library-header"><a class="brand" href="index.html">FAITH / ESSAYS</a><nav class="volume-tabs" aria-label="Essay volumes">{volume_tabs(None, "")}</nav><button class="tool-btn" id="theme-btn" type="button">LIGHT / DARK</button></header>
<main class="library-main">
  <p class="library-kicker">A SMALL LIBRARY OF BIG QUESTIONS</p>
  <h1>Arguments that can<br><em>afford the light.</em></h1>
  <p class="library-intro">Full-length Catholic philosophical and theological essays, read slowly and presented as visual arguments. Each volume keeps its complete source text in view while giving the reader maps, definitions, objections, and room to think.</p>
  <section class="library-grid" aria-label="Essay volumes">{"".join(cards)}</section>
  <div class="library-note"><span>02</span><p>More volumes will join this shelf. The form is meant to expand without flattening the essays into summaries.</p></div>
</main>
<footer class="library-footer"><span>FAITH / ESSAY LIBRARY</span><span>READING IS A FORM OF ATTENTION</span></footer>
<script>window.ESSAY_CONFIG = {json.dumps({"essayId": "library", "theme": "library", "glossary": []})};</script>
<script src="assets/site.js" defer></script>
</body>
</html>'''


def write_report(essays: list[Essay], results: dict[str, dict]) -> None:
    lines = ["# Text integrity report", "", "Generated by `python3 build.py`.", ""]
    for essay in essays:
        r = results[essay.essay_id]
        lines.extend([
            f"## {essay.essay_id.title()}",
            "",
            f"- Source path: `content/{essay.essay_id}/essay.md`",
            f"- SHA-256: `{essay.sha256}`",
            f"- Word count: {r['word_count']:,}",
            f"- Punctuation-aware token count: {r['token_count']:,}",
            f"- Paragraph count: {r['paragraph_count']}",
            f"- Heading count: {r['heading_count']}",
            f"- Quotation count: {r['quotation_count']}",
            f"- Footnote/endnote count: {r['note_count']}",
            f"- Structural-order result: **{r['structural']}**",
            f"- Strict visible-text result: **{r['visible']}**",
            f"- Word-and-punctuation sequence: **{r['tokens']}**",
            f"- Final result: **{r['final']}**",
            "",
        ])
    (ROOT / "reports" / "text-integrity-report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="build and run the integrity/link checks")
    args = parser.parse_args()
    essays = [load_essay(essay_id) for essay_id in ESSAYS]
    manifests = {essay_id: read_json(ROOT / "content" / essay_id / "manifest.json") for essay_id in ESSAYS}
    results: dict[str, dict] = {}

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(exist_ok=True)
    shutil.copy2(ROOT / "style.css", assets_dir / "site.css")
    shutil.copy2(ROOT / "script.js", assets_dir / "site.js")

    for essay in essays:
        manifest = manifests[essay.essay_id]
        page = render_essay_page(essay, manifest, [e for e in essays if e.essay_id != essay.essay_id], "../")
        route_dir = ROOT / essay.essay_id
        route_dir.mkdir(exist_ok=True)
        output = route_dir / "index.html"
        output.write_text(page, encoding="utf-8")
        results[essay.essay_id] = verify_rendered_html(essay, page, reader_excluded_ids(essay))
        print(f"{essay.essay_id}: {results[essay.essay_id]['final']} ({essay.sha256})")

    (ROOT / "index.html").write_text(render_library(essays), encoding="utf-8")
    write_report(essays, results)
    print("wrote index.html, goodness/index.html, resurrection/index.html")
    print("wrote reports/text-integrity-report.md")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except IntegrityError as exc:
        print(f"BUILD FAILED: {exc}")
        raise SystemExit(1)
