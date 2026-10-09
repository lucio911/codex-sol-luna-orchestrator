"""Documentation smoke tests for quickstart discovery and local links."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = (
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "docs/QUICKSTART.md",
    ROOT / "docs/QUICKSTART.zh-CN.md",
    ROOT / "examples/prompts.md",
    ROOT / "examples/AGENTS.example.md",
)
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


class DocumentationTests(unittest.TestCase):
    def test_quick_start_and_examples_present(self):
        for path in DOCS:
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertTrue(path.is_file())
                self.assertTrue(path.read_text(encoding="utf-8").strip())

    def test_local_links_resolve(self):
        for path in DOCS:
            body = path.read_text(encoding="utf-8")
            for raw_url in MARKDOWN_LINK.findall(body):
                url = raw_url.split("#", 1)[0]
                if not url or url.startswith(("https://", "http://", "mailto:")):
                    continue
                with self.subTest(from_file=path.name, link=url):
                    target = (path.parent / url).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()), "Link escapes repository")
                    self.assertTrue(target.is_file(), f"Missing local link target: {url}")

    def test_examples_cover_all_modes(self):
        guide = (ROOT / "docs/QUICKSTART.zh-CN.md").read_text(encoding="utf-8")
        for mode in ("auto", "economy", "quality", "research"):
            with self.subTest(mode=mode):
                self.assertIn(f"$sol-luna-orchestrator mode={mode}", guide)
        self.assertIn("luna_executor", guide)
        self.assertIn("不能证明", guide)


if __name__ == "__main__":
    unittest.main()
