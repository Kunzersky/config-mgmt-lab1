import base64
import io
import zipfile

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
    vfs = load_zip(base64.b64encode(archive_bytes()))
    assert vfs.read_file("readme.txt") == b"read me"


def test_missing_path_fails():
    vfs = load_zip(archive_bytes())
    try:
        vfs.resolve("missing")
    except VFSError as error:
        assert "no such" in str(error)
    else:
        raise AssertionError("missing path should fail")
