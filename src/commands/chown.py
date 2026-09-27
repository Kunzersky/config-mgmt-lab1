from .base import CommandContext, error

CHOWN_ARGS = 2


def run(context: CommandContext, arguments: list[str]) -> None:
    """Change the owner recorded on a VFS node."""
    if len(arguments) != CHOWN_ARGS:
        error(context, "chown: usage: chown OWNER PATH")
        return
    owner, path = arguments
    try:
        node = context.vfs.resolve(path)
        if node is None:
            raise ValueError(f"no such file or directory: {path}")
        node.owner = owner
    except Exception as exc:
        error(context, str(exc))
