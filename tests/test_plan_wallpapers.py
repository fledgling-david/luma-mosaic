import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from plan_wallpapers import build_plan, choose_bold_direction  # noqa: E402


class PlanWallpaperTests(unittest.TestCase):
    def test_build_plan_has_three_distinct_modes(self):
        plan = build_plan("tabby cat", "quiet", ["#AA9977", "445566"])
        ids = [direction["id"] for direction in plan["directions"]]
        self.assertEqual(
            ids,
            [
                "01-source-match",
                "02-intelligent-extension",
                "03-bold-reimagination",
            ],
        )
        self.assertEqual(plan["directions"][0]["palette"], ["#AA9977", "#445566"])

    def test_bold_direction_is_deterministic_but_not_fixed(self):
        self.assertEqual(
            choose_bold_direction("cat", "quiet"),
            choose_bold_direction("cat", "quiet"),
        )
        directions = {
            choose_bold_direction(f"subject-{index}", "natural")
            for index in range(20)
        }
        self.assertGreater(len(directions), 1)

    def test_invalid_hex_color_is_rejected(self):
        with self.assertRaises(ValueError):
            build_plan("product", "clean", ["not-a-color"])


if __name__ == "__main__":
    unittest.main()
