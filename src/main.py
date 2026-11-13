"""Stage 2: fetch immediate dependencies from npm Registry."""

import sys

from config import build_parser, show_config, validate_config
from npm_registry import NpmRegistry
from test_fixture import load_fixture


def obtain_dependencies(config):
    """Select dependency source based on test mode."""
    if config.test_mode:
        fixture = load_fixture(config.repo)
        if config.package not in fixture:
            raise ValueError(f"Пакет {config.package} отсутствует")
        return fixture[config.package]
    return NpmRegistry(config.repo).dependencies(config.package)


def main():
    """Display direct dependencies for the chosen package."""
    parser = build_parser()
    try:
        config = validate_config(parser.parse_args())
        show_config(config)
        if config.stage == 1:
            return 0
        deps = obtain_dependencies(config)
        print(f"Прямые зависимости {config.package}:")
        if isinstance(deps, dict):
            for name, version in sorted(deps.items()):
                print(f"  {name}: {version}")
        else:
            for name in sorted(deps):
                print(f"  {name}")
        if not deps:
            print("  (отсутствуют)")
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
