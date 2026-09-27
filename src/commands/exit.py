from .base import CommandContext


def run(context: CommandContext, arguments: list[str]) -> None:
    """Request termination of the current shell session."""
    context.should_exit = True
