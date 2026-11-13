"""CLI parameters and validation for dependency graph analyzer."""

import argparse
from pathlib import Path
import re
from urllib.parse import urlparse


NPM_NAME = re.compile(r"^(?:@[a-z0-9._-]+/)?[a-z0-9._-]+$")
TEST_NAME = re.compile(r"^[A-Z]+$")


def build_parser():
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(description="Граф зависимостей npm")
    parser.add_argument("--package", required=True, help="Имя пакета")
    parser.add_argument("--repo", required=True, help="URL npm или JSON-файл")
    parser.add_argument("--test-mode", action="store_true")
    parser.add_argument("--ascii-tree", action="store_true")
    parser.add_argument("--show-order", action="store_true")
    parser.add_argument("--compare-npm", action="store_true")
    parser.add_argument("--stage", type=int, choices=range(1, 2), default=1)
    parser.add_argument("--max-nodes", type=int, default=40)
    parser.add_argument("--out", default="output")
    parser.add_argument("--no-open", action="store_true")
    return parser


def validate_config(config):
    """Validate CLI values before fetching package information."""
    if config.max_nodes < 1:
        raise ValueError("--max-nodes должен быть положительным")
    if config.test_mode:
        if not TEST_NAME.fullmatch(config.package):
            raise ValueError("Тестовые пакеты: только большие буквы A-Z")
        if not Path(config.repo).is_file():
            raise ValueError(
                f"Файл тестового репозитория не найден: {config.repo}"
            )
        if config.compare_npm:
            raise ValueError("Сравнение с npm возможно только в сетевом режиме")
    else:
        if not NPM_NAME.fullmatch(config.package):
            raise ValueError(f"Недопустимое имя npm-пакета: {config.package}")
        url = urlparse(config.repo)
        if url.scheme not in ("https", "http") or not url.netloc:
            raise ValueError(
                "--repo должен быть URL вида https://registry.npmjs.org"
            )
    return config


def show_config(config):
    """Display the four parameters required at stage one."""
    print(f"package: {config.package}")
    print(f"repo: {config.repo}")
    print(f"test_mode: {config.test_mode}")
    print(f"ascii_tree: {config.ascii_tree}")
