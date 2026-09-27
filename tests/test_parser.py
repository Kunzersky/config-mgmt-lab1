import pytest

from src.parser import ParseError, parse_line


def test_parser_handles_quotes():
    assert parse_line('cat "hello world.txt"') == ("cat", ["hello world.txt"])


def test_parser_ignores_empty_line():
    assert parse_line("  ") is None


def test_parser_reports_unclosed_quote():
    with pytest.raises(ParseError):
        parse_line('cat "broken')
