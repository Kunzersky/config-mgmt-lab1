from .base import CommandContext, error


def run(context: CommandContext, arguments: list[str]) -> None:
    """Write the contents of the requested text files."""
    if not arguments:
        error(context, "cat: missing operand")
        return
    for path in arguments:
        try:
            content = context.vfs.read_file(path).decode("utf-8")
            print(content, end="", file=context.output)
        except UnicodeDecodeError:
            error(context, f"cat: {path}: binary file")
        except Exception as exc:
            error(context, str(exc))
