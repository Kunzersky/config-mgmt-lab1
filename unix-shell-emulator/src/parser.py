"""Parse one shell input line."""

import shlex


class ParseError(ValueError):
    pass


def parse_line(line: str) -> tuple[str, list[str]] | None:
    try:
        parts = shlex.split(line)
    except ValueError as error:
        raise ParseError(str(error)) from error
    return (parts[0], parts[1:]) if parts else None
