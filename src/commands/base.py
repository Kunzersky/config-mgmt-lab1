"""Shared command context and command type."""

from dataclasses import dataclass, field
from typing import TextIO

from ..config import Config
from ..vfs.vfs import VFS


@dataclass
class CommandContext:
    """Mutable state shared by built-in commands in one shell session."""

    vfs: VFS
    output: TextIO
    history: list[str] = field(default_factory=list)
    should_exit: bool = False
    config: Config = field(default_factory=Config)
    has_error: bool = False


def error(context: CommandContext, message: str) -> None:
    """Write an error and mark the current command as failed."""
    context.has_error = True
    print(f"shell: {message}", file=context.output)
