"""Unit tests for graph traversal, cycles, ordering and DOT output."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from config import build_parser, validate_config
from dependency_graph import cycle_example, traverse_bfs
from graph_output import ascii_tree, build_dot
from load_order import dependency_first_order
from npm_registry import latest_dependencies
from test_fixture import load_fixture


FIXTURES = Path(__file__).resolve().parent / "fixtures"


class TestDependencyGraph(unittest.TestCase):
    """Check three graph structures and edge-case validation."""

    def test_bfs(self):
        """BFS visits each reachable vertex once, layer by layer."""
        fixture = load_fixture(FIXTURES / "simple.json")
        graph, traversal = traverse_bfs("A", fixture.__getitem__)
        self.assertEqual(traversal, ["A", "B", "C", "D"])
        self.assertEqual(graph["A"], ["B", "C"])

    def test_cycle(self):
        """A directed cycle does not trap BFS in an infinite loop."""
        fixture = load_fixture(FIXTURES / "cycle.json")
        graph, traversal = traverse_bfs("A", fixture.__getitem__)
        self.assertEqual(len(traversal), 4)
        self.assertEqual(cycle_example(graph), ["A", "B", "C", "A"])
        self.assertIn("[цикл]", ascii_tree(graph, "A"))

    def test_order(self):
        """Shared dependencies appear before packages that depend on them."""
        fixture = load_fixture(FIXTURES / "simple.json")
        order, unresolved = dependency_first_order(fixture)
        self.assertEqual(unresolved, [])
        self.assertLess(order.index("D"), order.index("B"))
        self.assertLess(order.index("D"), order.index("C"))
        self.assertEqual(order[-1], "A")

    def test_cycle_order(self):
        """Cyclic graphs report nodes that cannot be topologically ordered."""
        fixture = load_fixture(FIXTURES / "cycle.json")
        order, unresolved = dependency_first_order(fixture)
        self.assertIn("A", unresolved)
        self.assertEqual(order, ["D"])

    def test_dot(self):
        """DOT output contains directed edges."""
        dot = build_dot({"A": ["B"], "B": []}, "A")
        self.assertIn('"A" -> "B";', dot)
        self.assertIn("digraph", dot)

    def test_npm_metadata(self):
        """The npm adapter selects latest runtime dependencies."""
        data = {
            "dist-tags": {"latest": "2.0.0"},
            "versions": {"2.0.0": {"dependencies": {"b": "^1.0.0"}}},
        }
        self.assertEqual(latest_dependencies(data, "a"), {"b": "^1.0.0"})

    def test_cli_invalid(self):
        """CLI rejects nonexistent files and nonuppercase test package names."""
        parser = build_parser()
        args = parser.parse_args([
            "--package", "A", "--repo", "missing.json", "--test-mode"
        ])
        with self.assertRaises(ValueError):
            validate_config(args)

    def test_node_limit(self):
        """Large graphs fail safely instead of silently truncating."""
        fixture = load_fixture(FIXTURES / "simple.json")
        with self.assertRaises(ValueError):
            traverse_bfs("A", fixture.__getitem__, max_nodes=2)


if __name__ == "__main__":
    unittest.main()
