import io
import zipfile
from pathlib import Path

from src.commands import cat, cd, chown, history, ls
from src.commands.base import CommandContext
from src.config import Config
from src.repl import COMMANDS, execute_line
from src.vfs.node import Node
from src.vfs.vfs import VFS


def make_context():
    root = Node("", True)
    root.add_child(Node("notes.txt", False, b"hello\n"))
    root.add_child(Node("docs", True))
    return CommandContext(VFS(root), io.StringIO(), ["ls"])


def test_ls_and_cat():
    context = make_context()
    ls.run(context, [])
    cat.run(context, ["notes.txt"])
    assert context.output.getvalue() == "docs/\nnotes.txt\nhello\n"


def test_cd_chown_and_history():
    context = make_context()
    cd.run(context, ["docs"])
    assert context.vfs.cwd_path == "/docs"
    cd.run(context, [".."])
    chown.run(context, ["alice", "notes.txt"])
    assert context.vfs.resolve("notes.txt").owner == "alice"
    history.run(context, [])
    assert "1  ls" in context.output.getvalue()


def test_conf_dump_command():
    context = make_context()
    context.config = Config(Path("sample.zip"), Path("startup.txt"), "{cwd}> ")

    execute_line(context, "conf-dump")

    assert context.output.getvalue() == (
        "vfs_path: sample.zip\n"
        "startup_script: startup.txt\n"
        "prompt: {cwd}> \n"
    )


def test_vfs_load_command(tmp_path):
    archive_path = tmp_path / "sample.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("loaded.txt", "loaded")
    context = make_context()

    execute_line(context, f"vfs-load {archive_path}")

    assert [node.name for node in context.vfs.list_dir()] == ["loaded.txt"]
    assert "vfs-load" in COMMANDS
    assert "vfs_load" not in COMMANDS
