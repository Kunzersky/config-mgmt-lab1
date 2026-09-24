import io

from src.commands import cat, cd, chown, history, ls
from src.commands.base import CommandContext
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
