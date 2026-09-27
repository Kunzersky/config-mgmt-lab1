from pathlib import Path

from src.config import parse_args


def test_parse_args():
    config = parse_args(["--vfs", "sample.zip", "--script", "startup.txt"])
    assert config.vfs_path == Path("sample.zip")
    assert config.startup_script == Path("startup.txt")
