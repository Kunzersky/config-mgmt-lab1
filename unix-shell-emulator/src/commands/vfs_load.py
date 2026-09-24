from pathlib import Path

from ..vfs.loader import load_zip
from .base import CommandContext, error


def run(context: CommandContext, arguments: list[str]) -> None:
    if len(arguments) != 1:
        error(context, "vfs_load: usage: vfs_load ARCHIVE")
        return
    try:
        loaded = load_zip(Path(arguments[0]))
        context.vfs = loaded
    except Exception as exc:
        error(context, str(exc))
