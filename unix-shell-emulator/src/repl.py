"""Interactive command loop."""

import getpass
import io
import socket
from pathlib import Path

from .commands import cat, cd, chown, exit as exit_command, history, ls, vfs_load
from .commands.base import CommandContext, error
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
    "vfs_load": vfs_load.run,
}


def make_prompt(context: CommandContext, template: str) -> str:
    return template.format(
        user=getpass.getuser(),
        host=socket.gethostname(),
        cwd=context.vfs.cwd_path,
    )


def execute_line(context: CommandContext, line: str) -> None:
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
    input_stream: io.TextIOBase | None = None,
    output_stream: io.TextIOBase | None = None,
    startup_script: Path | None = None,
) -> None:
    input_stream = input_stream or io.TextIOWrapper(__import__("sys").stdin.buffer)
    output_stream = output_stream or __import__("sys").stdout
    context = CommandContext(vfs or VFS(Node("", True)), output_stream)

    if startup_script:
        for line in startup_script.read_text(encoding="utf-8").splitlines():
            if line.strip() and not line.lstrip().startswith("#"):
                try:
                    execute_line(context, line)
                except ParseError as error_value:
                    error(context, f"parse error: {error_value}")
                if context.should_exit:
                    return

    while not context.should_exit:
        try:
            output_stream.write(make_prompt(context, prompt))
            output_stream.flush()
            line = input_stream.readline()
        except KeyboardInterrupt:
            output_stream.write("\n")
            continue
        if not line:
            output_stream.write("\n")
            break
        try:
            execute_line(context, line.rstrip("\n"))
        except ParseError as error_value:
            error(context, f"parse error: {error_value}")
