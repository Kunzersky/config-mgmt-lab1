from .base import CommandContext, error


def run(context: CommandContext, arguments: list[str]) -> None:
    path = arguments[0] if arguments else "."
    try:
        for node in context.vfs.list_dir(path):
            print(f"{node.name}{'/' if node.is_dir else ''}", file=context.output)
    except Exception as exc:
        error(context, str(exc))
