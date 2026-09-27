"""Load a virtual filesystem from ZIP data."""

import base64
import binascii
import io
import zipfile
from pathlib import Path

from .node import Node
from .vfs import VFS


def _read_archive_bytes(source: str | Path | bytes) -> bytes:
    """Read a ZIP or decode a Base64-encoded ZIP source."""
    raw = (
        Path(source).read_bytes()
        if isinstance(source, (str, Path))
        else source
    )
    if raw.startswith(b"PK"):
        return raw
    try:
        decoded = base64.b64decode(b"".join(raw.split()), validate=True)
    except (binascii.Error, ValueError) as error:
        message = "source is neither a ZIP nor valid base64 ZIP"
        raise ValueError(message) from error
    if not decoded.startswith(b"PK"):
        raise ValueError("source is neither a ZIP nor valid base64 ZIP")
    return decoded


def _add_archive_entry(
    root: Node,
    archive: zipfile.ZipFile,
    info: zipfile.ZipInfo,
) -> None:
    """Add one archive member and any missing parent directories to root."""
    parts = [part for part in info.filename.split("/") if part]
    current = root
    for index, part in enumerate(parts):
        is_last = index == len(parts) - 1
        child = current.children.get(part)
        if child is None:
            is_dir = not is_last or info.is_dir()
            content = b"" if is_dir else archive.read(info)
            child = Node(part, is_dir, content)
            current.add_child(child)
        current = child


def load_zip(source: str | Path | bytes) -> VFS:
    """Load a ZIP or Base64-encoded ZIP into a virtual filesystem."""
    raw = _read_archive_bytes(source)
    root = Node("", True)
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            for info in archive.infolist():
                _add_archive_entry(root, archive, info)
    except zipfile.BadZipFile as error:
        raise ValueError("source is not a valid ZIP archive") from error
    return VFS(root)
