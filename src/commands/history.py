from .base import CommandContext


def run(context: CommandContext, arguments: list[str]) -> None:
    """Print commands entered during the current session."""
    for index, command in enumerate(context.history, 1):
        print(f"{index}  {command}", file=context.output)
