import io
from pathlib import Path

import pytest

from src.main import main
from src.repl import run_repl
from src.vfs.node import Node
from src.vfs.vfs import VFS


def test_repl_runs_script_and_input(tmp_path):
    root = Node("", True)
    root.add_child(Node("hello.txt", False, b"hello\n"))
    output = io.StringIO()
    script = tmp_path / "startup.txt"
    script.write_text("cat hello.txt\nexit\n", encoding="utf-8")
    run_repl(
        VFS(root),
        input_stream=io.StringIO(""),
        output_stream=output,
        startup_script=script,
    )
    assert "cat hello.txt" in output.getvalue()
    assert "hello" in output.getvalue()


def test_startup_script_stops_after_first_error(tmp_path):
    root = Node("", True)
    root.add_child(Node("after-error.txt", False, b"should not run\n"))
    script = tmp_path / "startup.txt"
    script.write_text(
        "unknown-command\ncat after-error.txt\n",
        encoding="utf-8",
    )
    output = io.StringIO()

    run_repl(
        VFS(root),
        input_stream=io.StringIO("exit\n"),
        output_stream=output,
        startup_script=script,
    )

    assert "command not found: unknown-command" in output.getvalue()
    assert "should not run" not in output.getvalue()
    assert "cat after-error.txt" not in output.getvalue()


@pytest.mark.parametrize(
    ("failing_command", "expected_error"),
    [
        ("missing-command", "command not found"),
        ("cd missing", "no such file or directory"),
        ("cat missing.txt", "no such file or directory"),
        ("chown", "usage: chown OWNER PATH"),
    ],
)
def test_script_stops_after_each_error(
    tmp_path, failing_command, expected_error
):
    root = Node("", True)
    root.add_child(Node("after-error.txt", False, b"should not run\n"))
    script = tmp_path / "error.txt"
    script.write_text(
        f"{failing_command}\ncat after-error.txt\n", encoding="utf-8"
    )
    output = io.StringIO()

    run_repl(
        VFS(root),
        input_stream=io.StringIO(""),
        output_stream=output,
        startup_script=script,
    )

    assert expected_error in output.getvalue()
    assert "should not run" not in output.getvalue()


def test_main_prints_config_and_handles_missing_script(tmp_path, capsys):
    script = tmp_path / "startup.txt"
    script.write_text("exit\n", encoding="utf-8")
    result = main(["--script", str(script), "--prompt", "tester:{cwd}$ "])

    output = capsys.readouterr()
    assert result == 0
    assert "Параметры запуска:" in output.out
    assert "vfs_path: не задан" in output.out
    assert f"startup_script: {script}" in output.out
    assert "prompt: tester:{cwd}$ " in output.out
    assert "tester:/$ exit" in output.out

    result = main(["--script", str(tmp_path / "missing.txt")])
    output = capsys.readouterr()
    assert result == 1
    assert "shell:" in output.err
    assert "Traceback" not in output.err


def test_main_handles_missing_vfs(tmp_path, capsys):
    result = main(["--vfs", str(tmp_path / "missing.b64")])

    output = capsys.readouterr()
    assert result == 1
    assert "shell:" in output.err
    assert "Traceback" not in output.err
