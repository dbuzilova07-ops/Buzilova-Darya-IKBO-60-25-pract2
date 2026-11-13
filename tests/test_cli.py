"""Validate the initial CLI arguments."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import build_parser, validate_config


class TestConfig(unittest.TestCase):
    """Minimal CLI tests for the first development milestone."""

    def test_valid(self):
        """Accept a valid test fixture and uppercase name."""
        filename = Path(__file__).parent / "fixtures" / "simple.json"
        args = build_parser().parse_args([
            "--package", "A", "--repo", str(filename), "--test-mode"
        ])
        self.assertEqual(validate_config(args).package, "A")

    def test_invalid_name(self):
        """Reject lowercase package name in test mode."""
        filename = Path(__file__).parent / "fixtures" / "simple.json"
        args = build_parser().parse_args([
            "--package", "a", "--repo", str(filename), "--test-mode"
        ])
        with self.assertRaises(ValueError):
            validate_config(args)


if __name__ == "__main__":
    unittest.main()
