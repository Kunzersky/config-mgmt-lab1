"""Load a virtual filesystem from ZIP data."""

import base64
import io
import zipfile
from pathlib import Path

from .node import Node
from .vfs import VFS


def load_zip(source: str | Path | bytes) -> VFS:
    raw = Path(source).read_bytes() if isinstance(source, (str, Path)) else source
    if not raw.startswith(b"PK"):
        try:
            raw = base64.b64decode(raw, validate=True)
        except Exception as error:
            raise ValueError("source is neither a ZIP nor valid base64 ZIP") from error

    root = Node("", True)
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        for info in archive.infolist():
            parts = [part for part in info.filename.split("/") if part]
            current = root
            for index, part in enumerate(parts):
                is_last = index == len(parts) - 1
                child = current.children.get(part)
                is_dir = info.is_dir() if is_last else True
                if child is None:
                    child = Node(part, is_dir, b"" if is_dir else archive.read(info))
                    current.add_child(child)
                current = child
    return VFS(root)
