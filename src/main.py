"""Stage 4: show dependency-first order and compare with native npm."""

import sys

from config import build_parser, show_config, validate_config
from dependency_graph import cycle_example, traverse_bfs
from load_order import show_order
from npm_compare import compare_direct_with_npm
from npm_registry import NpmRegistry
from test_fixture import load_fixture


def select_lookup(config):
    """Create direct dependency provider for test or live mode."""
    if config.test_mode:
        fixture = load_fixture(config.repo)
        if config.package not in fixture:
            raise ValueError(f"Пакет {config.package} отсутствует")
        return lambda name: fixture[name]
    return NpmRegistry(config.repo).dependencies


def main():
    """Perform BFS and print optional topological order."""
    parser = build_parser()
    try:
        config = validate_config(parser.parse_args())
        show_config(config)
        if config.stage == 1:
            return 0
        lookup = select_lookup(config)
        if config.stage == 2:
            print("Прямые зависимости:", sorted(lookup(config.package)))
            return 0
        graph, order = traverse_bfs(
            config.package, lookup, config.max_nodes
        )
        print("BFS:", " -> ".join(order))
        print("Цикл:", cycle_example(graph) or "нет")
        if config.stage == 4 and config.show_order:
            show_order(graph)
        if config.stage == 4 and config.compare_npm:
            compare_direct_with_npm(
                config.package, config.repo, lookup(config.package)
            )
    except (ValueError, KeyError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
