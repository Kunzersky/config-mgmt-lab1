from .base import CommandContext, error


def run(context: CommandContext, arguments: list[str]) -> None:
    """Change the current VFS directory."""
    if len(arguments) > 1:
        error(context, "cd: too many arguments")
        return
    try:
        context.vfs.change_dir(arguments[0] if arguments else "/")
    except Exception as exc:
        error(context, str(exc))
