from .base import CommandContext, error


def run(context: CommandContext, arguments: list[str]) -> None:
    if len(arguments) != 2:
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
