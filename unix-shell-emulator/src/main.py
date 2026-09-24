"""CLI entry point for the UNIX shell emulator."""

from .config import parse_args


def main(argv: list[str] | None = None) -> int:
    config = parse_args(argv)
    print("unix-shell-emulator: project initialized")
    if config.vfs_path:
        print(f"VFS: {config.vfs_path}")
    if config.startup_script:
        print(f"Script: {config.startup_script}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
