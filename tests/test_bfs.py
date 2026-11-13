"""Check the iterative breadth-first traversal and simple cycle."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from dependency_graph import cycle_example, traverse_bfs
from test_fixture import load_fixture


class TestBfs(unittest.TestCase):
    """Exercise breadth-first traversal of a cyclic test graph."""

    def test_cycle(self):
        """BFS visits each node exactly once despite a cycle."""
        path = Path(__file__).parent / "fixtures" / "cycle.json"
        data = load_fixture(path)
        graph, order = traverse_bfs("A", data.__getitem__)
        self.assertEqual(order, ["A", "B", "C", "D"])
        self.assertEqual(cycle_example(graph), ["A", "B", "C", "A"])


if __name__ == "__main__":
    unittest.main()
