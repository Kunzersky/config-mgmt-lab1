import base64
import io
import zipfile
from pathlib import Path

from src.vfs.loader import load_zip
from src.vfs.vfs import VFSError


def archive_bytes() -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w") as archive:
        archive.writestr("etc/motd", "hello")
        archive.writestr("readme.txt", "read me")
    return output.getvalue()


def test_load_zip_and_navigate():
    vfs = load_zip(archive_bytes())
    assert [node.name for node in vfs.list_dir()] == ["etc", "readme.txt"]
    vfs.change_dir("etc")
    assert vfs.read_file("motd") == b"hello"
    vfs.change_dir("..")
    assert vfs.cwd_path == "/"


def test_load_base64_zip():
    vfs = load_zip(base64.encodebytes(archive_bytes()))
    assert vfs.read_file("readme.txt") == b"read me"


def test_invalid_archive_has_clear_error():
    try:
        load_zip(b"not an archive")
    except ValueError as error:
        assert "valid base64 ZIP" in str(error)
    else:
        raise AssertionError("invalid archive should fail")


def test_deep_tree_sample_has_three_levels():
    samples = Path(__file__).parents[1] / "vfs_samples"
    vfs = load_zip(samples / "deep_tree.b64")

    assert vfs.read_file("a/b/c/deep.txt") == b"deep file\n"


def test_missing_path_fails():
    vfs = load_zip(archive_bytes())
    try:
        vfs.resolve("missing")
    except VFSError as error:
        assert "no such" in str(error)
    else:
        raise AssertionError("missing path should fail")
