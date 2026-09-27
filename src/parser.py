"""Parse one shell input line."""

import shlex


class ParseError(ValueError):
    """Raised when a command line cannot be tokenized."""

    pass


def parse_line(line: str) -> tuple[str, list[str]] | None:
    """Split a command line into its name and arguments."""
    try:
        parts = shlex.split(line)
    except ValueError as error:
        raise ParseError(str(error)) from error
    return (parts[0], parts[1:]) if parts else None
