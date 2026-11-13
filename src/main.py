"""CLI for five stages of npm dependency graph practical work."""

import sys

from config import build_parser, show_config, validate_config
from dependency_graph import cycle_example, traverse_bfs
from test_fixture import load_fixture
from graph_output import ascii_tree, render_graph
from load_order import show_order
from npm_compare import compare_direct_with_npm
from npm_registry import NpmRegistry


def obtain_lookup(config):
    """Select test JSON repository or live npm Registry data source."""
    if config.test_mode:
        fixture = load_fixture(config.repo)
        if config.package not in fixture:
            raise ValueError(f"Пакета {config.package} нет в тестовом графе")
        return lambda name: fixture[name]
    registry = NpmRegistry(config.repo)
    return registry.dependencies


def display_direct(config, lookup):
    """Display immediate runtime dependencies required at stage two."""
    dependencies = lookup(config.package)
    print(f"Прямые зависимости {config.package}:")
    if isinstance(dependencies, dict):
        for name, version in sorted(dependencies.items()):
            print(f"  {name}: {version}")
    else:
        for name in sorted(dependencies):
            print(f"  {name}")
    if not dependencies:
        print("  (отсутствуют)")
    return dependencies


def display_bfs(config, lookup):
    """Compute reachability with iterative breadth-first search."""
    graph, traversal = traverse_bfs(
        config.package, lookup, max_nodes=config.max_nodes
    )
    print("BFS без рекурсии:", " -> ".join(traversal))
    print("Вершин:", len(graph))
    print("Рёбер:", sum(len(deps) for deps in graph.values()))
    cycle = cycle_example(graph)
    print("Цикл:", " -> ".join(cycle) if cycle else "нет")
    return graph


def run(config):
    """Execute the requested stage with only the relevant output."""
    show_config(config)
    if config.stage == 1:
        return
    lookup = obtain_lookup(config)
    if config.stage == 2:
        display_direct(config, lookup)
        return
    graph = display_bfs(config, lookup)
    if config.stage >= 4 and config.show_order:
        show_order(graph)
    if config.stage >= 4 and config.compare_npm:
        compare_direct_with_npm(
            config.package, config.repo, lookup(config.package)
        )
    if config.stage == 5:
        if config.ascii_tree:
            print("ASCII-дерево:\n" + ascii_tree(graph, config.package))
        render_graph(graph, config.package, config.out, not config.no_open)


def main():
    """Parse arguments and handle expected errors without a traceback."""
    parser = build_parser()
    try:
        config = validate_config(parser.parse_args())
        run(config)
    except (ValueError, KeyError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
