from .base import CommandContext, error


def run(context: CommandContext, arguments: list[str]) -> None:
    if arguments:
        error(context, "conf-dump: does not accept arguments")
        return

    config = context.config
    print(f"vfs_path: {config.vfs_path or 'не задан'}", file=context.output)
    print(f"startup_script: {config.startup_script or 'не задан'}", file=context.output)
    print(f"prompt: {config.prompt}", file=context.output)