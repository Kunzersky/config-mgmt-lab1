import io

from src.repl import run_repl
from src.vfs.node import Node
from src.vfs.vfs import VFS


def test_repl_runs_script_and_input():
    root = Node("", True)
    root.add_child(Node("hello.txt", False, b"hello\n"))
    output = io.StringIO()
    run_repl(VFS(root), input_stream=io.StringIO("cat hello.txt\nexit\n"), output_stream=output)
    assert "hello" in output.getvalue()
