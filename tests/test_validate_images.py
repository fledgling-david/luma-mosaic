import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_images import parse_ratio, validate_images  # noqa: E402


def make_pattern(path: Path, variant: int, size=(320, 180)) -> None:
    image = Image.new("RGB", size, (20 + variant * 30, 40, 70))
    draw = ImageDraw.Draw(image)
    if variant == 0:
        draw.rectangle((20, 20, 150, 120), fill=(230, 80, 60))
    elif variant == 1:
        draw.ellipse((120, 25, 285, 160), fill=(60, 210, 120))
    else:
        draw.polygon([(20, 160), (170, 15), (300, 160)], fill=(240, 200, 40))
    image.save(path)


class ValidateImagesTests(unittest.TestCase):
    def test_three_valid_distinct_wallpapers_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            paths = [Path(folder) / f"wallpaper-{index}.png" for index in range(3)]
            for index, path in enumerate(paths):
                make_pattern(path, index)
            result = validate_images(
                paths,
                parse_ratio("16:9"),
                min_width=300,
                min_height=160,
                duplicate_distance=0,
            )
            self.assertTrue(result["ok"], result["issues"])

    def test_duplicate_and_wrong_ratio_are_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            first = root / "first.png"
            duplicate = root / "duplicate.png"
            square = root / "square.png"
            make_pattern(first, 0)
            shutil.copyfile(first, duplicate)
            make_pattern(square, 2, size=(200, 200))
            result = validate_images(
                [first, duplicate, square],
                parse_ratio("16:9"),
                min_width=100,
                min_height=100,
                duplicate_distance=0,
            )
            self.assertFalse(result["ok"])
            self.assertTrue(any("near-duplicate" in issue for issue in result["issues"]))
            self.assertTrue(any("expected" in issue for issue in result["issues"]))


if __name__ == "__main__":
    unittest.main()
