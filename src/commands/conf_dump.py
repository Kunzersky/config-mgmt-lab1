from ..config import Config
from .base import CommandContext, error


def format_config(config: Config) -> str:
    """Return a readable representation of command-line settings."""
    return "\n".join(
        (
            f"vfs_path: {config.vfs_path or 'не задан'}",
            f"startup_script: {config.startup_script or 'не задан'}",
            f"prompt: {config.prompt}",
        )
    )


def run(context: CommandContext, arguments: list[str]) -> None:
    """Print the current configuration."""
    if arguments:
        error(context, "conf-dump: does not accept arguments")
        return

    print(format_config(context.config), file=context.output)