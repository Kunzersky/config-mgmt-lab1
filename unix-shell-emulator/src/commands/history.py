from .base import CommandContext


def run(context: CommandContext, arguments: list[str]) -> None:
    for index, command in enumerate(context.history, 1):
        print(f"{index}  {command}", file=context.output)
