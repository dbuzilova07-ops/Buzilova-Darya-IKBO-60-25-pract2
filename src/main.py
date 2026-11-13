"""Stage 1: CLI configuration and error handling."""

import sys

from config import build_parser, show_config, validate_config


def main():
    """Read and display CLI options for the minimal prototype."""
    parser = build_parser()
    try:
        config = validate_config(parser.parse_args())
        show_config(config)
    except ValueError as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
