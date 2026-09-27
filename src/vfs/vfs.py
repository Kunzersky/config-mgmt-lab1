"""Navigation and lookup for the in-memory filesystem."""

from pathlib import PurePosixPath

from .node import Node


class VFSError(Exception):
    """Base error for virtual filesystem operations."""


class VFS:
    """Provide path resolution and file operations over a Node tree."""

    def __init__(self, root: Node | None = None):
        """Create a VFS rooted at the given node or an empty directory."""
        self.root = root or Node("", True)
        self.cwd = self.root

    @property
    def cwd_path(self) -> str:
        """Return the absolute path of the current directory."""
        return self.cwd.path() or "/"

    def resolve(self, path: str, *, must_exist: bool = True) -> Node | None:
        """Resolve an absolute or relative path within the VFS."""
        if not path:
            path = "."
        current = self.root if path.startswith("/") else self.cwd
        for part in PurePosixPath(path).parts:
            if part in ("", ".", "/"):
                continue
            if part == "..":
                current = current.parent or self.root
                continue
            if not current.is_dir:
                raise VFSError(f"not a directory: {current.name}")
            current = current.children.get(part)  # type: ignore[assignment]
            if current is None:
                if must_exist:
                    raise VFSError(f"no such file or directory: {path}")
                return None
        return current

    def change_dir(self, path: str) -> None:
        """Set the current directory to an existing directory path."""
        node = self.resolve(path)
        if node is None or not node.is_dir:
            raise VFSError(f"not a directory: {path}")
        self.cwd = node

    def list_dir(self, path: str = ".") -> list[Node]:
        """Return a directory's children in name order."""
        node = self.resolve(path)
        if node is None or not node.is_dir:
            raise VFSError(f"not a directory: {path}")
        return [node.children[name] for name in sorted(node.children)]

    def read_file(self, path: str) -> bytes:
        """Return the bytes stored at a file path."""
        node = self.resolve(path)
        if node is None or node.is_dir:
            raise VFSError(f"not a file: {path}")
        return node.content
