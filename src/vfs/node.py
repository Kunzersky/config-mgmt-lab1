"""Nodes used by the in-memory filesystem."""

from dataclasses import dataclass, field


@dataclass
class Node:
    name: str
    is_dir: bool
    content: bytes = b""
    owner: str = "root"
    children: dict[str, "Node"] = field(default_factory=dict)
    parent: "Node | None" = field(default=None, repr=False)

    def add_child(self, child: "Node") -> None:
        if not self.is_dir:
            raise ValueError("cannot add a child to a file")
        child.parent = self
        self.children[child.name] = child

    def path(self) -> str:
        parts: list[str] = []
        current: Node | None = self
        while current is not None and current.parent is not None:
            parts.append(current.name)
            current = current.parent
        return "/" + "/".join(reversed(parts))
