"""CLI entry point for the UNIX shell emulator."""

from .config import parse_args
from .repl import run_repl
from .vfs.loader import load_zip
from .vfs.node import Node
from .vfs.vfs import VFS


def main(argv: list[str] | None = None) -> int:
    config = parse_args(argv)
    vfs = load_zip(config.vfs_path) if config.vfs_path else VFS(Node("", True))
    run_repl(
        vfs,
        prompt=config.prompt,
        startup_script=config.startup_script,
        config=config,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
