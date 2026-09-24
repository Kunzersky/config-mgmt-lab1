"""Shared command context and command type."""

from dataclasses import dataclass, field
from typing import TextIO

from ..vfs.vfs import VFS


@dataclass
class CommandContext:
    vfs: VFS
    output: TextIO
    history: list[str] = field(default_factory=list)
    should_exit: bool = False


def error(context: CommandContext, message: str) -> None:
    print(f"shell: {message}", file=context.output)
