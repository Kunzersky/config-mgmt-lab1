from .base import CommandContext, error


def run(context: CommandContext, arguments: list[str]) -> None:
    if not arguments:
        error(context, "cat: missing operand")
        return
    for path in arguments:
        try:
            print(context.vfs.read_file(path).decode("utf-8"), end="", file=context.output)
        except UnicodeDecodeError:
            error(context, f"cat: {path}: binary file")
        except Exception as exc:
            error(context, str(exc))
