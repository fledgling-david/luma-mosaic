import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from analyze_palette import extract_palette  # noqa: E402


class AnalyzePaletteTests(unittest.TestCase):
    def test_extract_palette_reports_sources_and_colors(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            red = root / "red.png"
            blue = root / "blue.png"
            Image.new("RGB", (40, 40), (240, 20, 20)).save(red)
            Image.new("RGB", (40, 40), (20, 40, 230)).save(blue)

            result = extract_palette([red, blue], colors=2)

            self.assertEqual(result["source_count"], 2)
            self.assertEqual(len(result["palette"]), 2)
            self.assertTrue(all(item["hex"].startswith("#") for item in result["palette"]))
            self.assertGreater(result["palette"][0]["weight"], 0)

    def test_extract_palette_rejects_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            extract_palette(["does-not-exist.png"])


if __name__ == "__main__":
    unittest.main()
