"""Interactive command loop."""

import getpass
import sys
import socket
from pathlib import Path
from typing import TextIO

from .commands import (
    cat,
    cd,
    chown,
    conf_dump,
    exit as exit_command,
    history,
    ls,
    vfs_load,
)
from .commands.base import CommandContext, error
from .config import Config
from .parser import ParseError, parse_line
from .vfs.node import Node
from .vfs.vfs import VFS

COMMANDS = {
    "ls": ls.run,
    "cd": cd.run,
    "exit": exit_command.run,
    "history": history.run,
    "cat": cat.run,
    "chown": chown.run,
    "conf-dump": conf_dump.run,
    "vfs-load": vfs_load.run,
}


def make_prompt(context: CommandContext, template: str) -> str:
    """Render a prompt using the current user, host, and VFS path."""
    return template.format(
        user=getpass.getuser(),
        host=socket.gethostname(),
        cwd=context.vfs.cwd_path,
    )


def execute_line(context: CommandContext, line: str) -> None:
    """Parse and execute one shell command line."""
    parsed = parse_line(line)
    if parsed is None:
        return
    command, arguments = parsed
    context.history.append(line)
    handler = COMMANDS.get(command)
    if handler is None:
        error(context, f"command not found: {command}")
        return
    handler(context, arguments)


def run_repl(
    vfs: VFS | None = None,
    *,
    prompt: str = "{user}@{host}:{cwd}$ ",
    input_stream: TextIO | None = None,
    output_stream: TextIO | None = None,
    startup_script: Path | None = None,
    config: Config | None = None,
) -> None:
    """Run an optional startup script followed by the interactive REPL."""
    input_stream = input_stream or sys.stdin
    output_stream = output_stream or sys.stdout
    context = CommandContext(
        vfs or VFS(Node("", True)),
        output_stream,
        config=config or Config(startup_script=startup_script, prompt=prompt),
    )

    if startup_script and not run_script(context, startup_script, prompt):
        return
    run_interactive(context, prompt, input_stream)


def run_script(
    context: CommandContext,
    startup_script: Path,
    prompt: str,
) -> bool:
    """Echo and execute a script; stop and return false on the first error."""
    for line in startup_script.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        context.output.write(f"{make_prompt(context, prompt)}{line}\n")
        context.has_error = False
        try:
            execute_line(context, line)
        except ParseError as error_value:
            error(context, f"parse error: {error_value}")
        if context.should_exit or context.has_error:
            return False
    return True


def run_interactive(
    context: CommandContext,
    prompt: str,
    input_stream: TextIO,
) -> None:
    """Read and execute commands until the session is asked to exit."""
    while not context.should_exit:
        try:
            context.output.write(make_prompt(context, prompt))
            context.output.flush()
            line = input_stream.readline()
        except KeyboardInterrupt:
            context.output.write("\n")
            continue
        if not line:
            context.output.write("\n")
            break
        try:
            execute_line(context, line.rstrip("\n"))
        except ParseError as error_value:
            error(context, f"parse error: {error_value}")
