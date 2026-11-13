"""Test extraction of direct dependencies from npm metadata."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from npm_registry import latest_dependencies


class TestRegistry(unittest.TestCase):
    """Test npm metadata parsing without making network calls."""

    def test_latest(self):
        """Use latest release and its runtime dependencies."""
        info = {
            "dist-tags": {"latest": "1.5.0"},
            "versions": {"1.5.0": {"dependencies": {"child": "^1.0"}}}
        }
        self.assertEqual(
            latest_dependencies(info, "sample"), {"child": "^1.0"}
        )


if __name__ == "__main__":
    unittest.main()
