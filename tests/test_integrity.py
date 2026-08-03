import tempfile
import unittest
from pathlib import Path

from build import reader_excluded_ids
from src.essaylib import IntegrityError, parse_markdown, verify_rendered_html


class IntegrityTests(unittest.TestCase):
    def test_canonical_hashes_and_rendered_pages_pass(self):
        root = Path(__file__).resolve().parents[1]
        for essay_id, expected in (("goodness", "fc6a5f905aa9bc591a49799c6b7e4fda3671a504655e8de5e7355183acfb2e60"), ("resurrection", "e5da22a010731a448785fbef36c238902a215e849697df8cce0f8e9fa7ed6f0f")):
            essay = parse_markdown(essay_id, root / "content" / essay_id / "essay.md", expected)
            page = (root / essay_id / "index.html").read_text(encoding="utf-8")
            self.assertEqual("PASS", verify_rendered_html(essay, page, reader_excluded_ids(essay))["final"])

    def test_deliberate_source_deletion_fails_hash_verification(self):
        root = Path(__file__).resolve().parents[1]
        source = root / "content" / "goodness" / "essay.md"
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / "essay.md"
            copy.write_bytes(source.read_bytes().replace(b"Goodness Itself", b"Goodness", 1))
            with self.assertRaises(IntegrityError):
                parse_markdown("goodness-test-copy", copy, "fc6a5f905aa9bc591a49799c6b7e4fda3671a504655e8de5e7355183acfb2e60")


if __name__ == "__main__":
    unittest.main()
