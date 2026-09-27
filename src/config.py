"""Command-line configuration for the emulator."""

from dataclasses import dataclass
from pathlib import Path
import argparse


@dataclass(frozen=True)
class Config:
    """Command-line values used to start the emulator."""

    vfs_path: Path | None = None
    startup_script: Path | None = None
    prompt: str = "{user}@{host}:{cwd}$ "


def parse_args(argv: list[str] | None = None) -> Config:
    """Parse command-line arguments into a Config instance."""
    parser = argparse.ArgumentParser(description="Run the UNIX shell emulator.")
    parser.add_argument(
        "--vfs",
        type=Path,
        help="ZIP archive or Base64-encoded ZIP",
    )
    parser.add_argument(
        "--script",
        type=Path,
        help="commands to execute before the REPL",
    )
    parser.add_argument(
        "--prompt",
        default="{user}@{host}:{cwd}$ ",
        help="prompt template with {user}, {host}, and {cwd} fields",
    )
    args = parser.parse_args(argv)
    return Config(
        vfs_path=args.vfs,
        startup_script=args.script,
        prompt=args.prompt,
    )
