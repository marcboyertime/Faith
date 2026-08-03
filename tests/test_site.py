import re
import unittest
from pathlib import Path


class SiteChecks(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]

    def test_expected_routes_and_assets_exist(self):
        for route in (self.root / "index.html", self.root / "goodness" / "index.html", self.root / "resurrection" / "index.html"):
            self.assertTrue(route.exists(), route)
        self.assertTrue((self.root / "assets" / "site.css").exists())
        self.assertTrue((self.root / "assets" / "site.js").exists())

    def test_generated_pages_have_no_duplicate_ids_or_missing_local_assets(self):
        for page in (self.root / "index.html", self.root / "goodness" / "index.html", self.root / "resurrection" / "index.html"):
            source = page.read_text(encoding="utf-8")
            ids = re.findall(r'(?<![\w-])id="([^"]+)"', source)
            self.assertEqual(len(ids), len(set(ids)), page)
            for href in re.findall(r'(?:href|src)="([^"#]+)"', source):
                if href.startswith(("http:", "https:", "data:", "mailto:")):
                    continue
                target = (page.parent / href).resolve()
                self.assertTrue(target.exists(), f"{page}: {href}")

    def test_chapter_links_target_generated_sections(self):
        for page in (self.root / "goodness" / "index.html", self.root / "resurrection" / "index.html"):
            source = page.read_text(encoding="utf-8")
            ids = set(re.findall(r'(?<![\w-])id="([^"]+)"', source))
            for target in re.findall(r'href="#([^"]+)"', source):
                self.assertIn(target, ids, f"{page}: #{target}")

    def test_volume_tabs_are_real_local_links(self):
        library = (self.root / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="goodness/index.html"', library)
        self.assertIn('href="resurrection/index.html"', library)
        for essay_id in ("goodness", "resurrection"):
            source = (self.root / essay_id / "index.html").read_text(encoding="utf-8")
            self.assertIn('href="../goodness/index.html"', source)
            self.assertIn('href="../resurrection/index.html"', source)
            self.assertIn('class="volume-tab is-active"', source)


if __name__ == "__main__":
    unittest.main()
