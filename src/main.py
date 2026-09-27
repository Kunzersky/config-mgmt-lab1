"""CLI entry point for the UNIX shell emulator."""

import sys

from .commands.conf_dump import format_config
from .config import parse_args
from .repl import run_repl
from .vfs.loader import load_zip
from .vfs.node import Node
from .vfs.vfs import VFS


def main(argv: list[str] | None = None) -> int:
    """Print configuration, initialize VFS, and run the shell."""
    config = parse_args(argv)
    print("Параметры запуска:")
    print(format_config(config))
    try:
        vfs = (
            load_zip(config.vfs_path)
            if config.vfs_path
            else VFS(Node("", True))
        )
        run_repl(
            vfs,
            prompt=config.prompt,
            startup_script=config.startup_script,
            config=config,
        )
    except (OSError, ValueError) as error:
        print(f"shell: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
