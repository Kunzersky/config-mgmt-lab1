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


def test_startup_script_stops_after_first_error(tmp_path):
    root = Node("", True)
    root.add_child(Node("after-error.txt", False, b"should not run\n"))
    script = tmp_path / "startup.txt"
    script.write_text("unknown-command\ncat after-error.txt\n", encoding="utf-8")
    output = io.StringIO()

    run_repl(
        VFS(root),
        input_stream=io.StringIO("exit\n"),
        output_stream=output,
        startup_script=script,
    )

    assert "command not found: unknown-command" in output.getvalue()
    assert "should not run" not in output.getvalue()
