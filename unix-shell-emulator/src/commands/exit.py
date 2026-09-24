from .base import CommandContext


def run(context: CommandContext, arguments: list[str]) -> None:
    context.should_exit = True
