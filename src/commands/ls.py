from ..vfs.node import Node
from .base import CommandContext, error


def _format_node(node: Node, long_format: bool) -> str:
    """Format one VFS entry for the selected listing style."""
    name = f"{node.name}/" if node.is_dir else node.name
    return f"{node.owner} {name}" if long_format else name


def run(context: CommandContext, arguments: list[str]) -> None:
    """List VFS files and directories, optionally including owners."""
    long_format = "-l" in arguments
    paths = [argument for argument in arguments if argument != "-l"] or ["."]
    for path in paths:
        try:
            node = context.vfs.resolve(path)
            if node is None:
                continue
            entries = context.vfs.list_dir(path) if node.is_dir else [node]
            for entry in entries:
                print(_format_node(entry, long_format), file=context.output)
        except Exception as exc:
            error(context, str(exc))
