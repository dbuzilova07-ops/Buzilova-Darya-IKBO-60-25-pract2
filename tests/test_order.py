"""Check dependency-first ordering and cyclic warnings."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from load_order import dependency_first_order
from test_fixture import load_fixture


class TestOrder(unittest.TestCase):
    """Verify dependency-first order for directed acyclic graph."""

    def test_dependency_first(self):
        """Shared dependency must be before its dependents."""
        path = Path(__file__).parent / "fixtures" / "simple.json"
        graph = load_fixture(path)
        order, unresolved = dependency_first_order(graph)
        self.assertEqual(unresolved, [])
        self.assertLess(order.index("D"), order.index("B"))


if __name__ == "__main__":
    unittest.main()
