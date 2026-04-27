"""Project 2: Moonlight Museum After Dark."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque


@dataclass(frozen=True)
class Artifact:
    artifact_id: int
    name: str
    category: str
    age: int
    room: str


@dataclass(frozen=True)
class RestorationRequest:
    artifact_id: int
    description: str


# ── BST ─────────────────────────────────────────────────────────────────────

class TreeNode:
    def __init__(self, artifact: Artifact, left=None, right=None) -> None:
        self.artifact = artifact
        self.left = left
        self.right = right


class ArtifactBST:
    def __init__(self) -> None:
        self.root: TreeNode | None = None

    def insert(self, artifact: Artifact) -> bool:
        if self.root is None:
            self.root = TreeNode(artifact)
            return True
        return self._insert(self.root, artifact)

    def _insert(self, node: TreeNode, artifact: Artifact) -> bool:
        if artifact.artifact_id == node.artifact.artifact_id:
            return False
        if artifact.artifact_id < node.artifact.artifact_id:
            if node.left is None:
                node.left = TreeNode(artifact)
                return True
            return self._insert(node.left, artifact)
        else:
            if node.right is None:
                node.right = TreeNode(artifact)
                return True
            return self._insert(node.right, artifact)

    def search_by_id(self, artifact_id: int) -> Artifact | None:
        node = self.root
        while node:
            if artifact_id == node.artifact.artifact_id:
                return node.artifact
            node = node.left if artifact_id < node.artifact.artifact_id else node.right
        return None

    def inorder_ids(self) -> list[int]:
        result: list[int] = []
        def walk(node):
            if node:
                walk(node.left)
                result.append(node.artifact.artifact_id)
                walk(node.right)
        walk(self.root)
        return result

    def preorder_ids(self) -> list[int]:
        result: list[int] = []
        def walk(node):
            if node:
                result.append(node.artifact.artifact_id)
                walk(node.left)
                walk(node.right)
        walk(self.root)
        return result

    def postorder_ids(self) -> list[int]:
        result: list[int] = []
        def walk(node):
            if node:
                walk(node.left)
                walk(node.right)
                result.append(node.artifact.artifact_id)
        walk(self.root)
        return result


# ── Queue ────────────────────────────────────────────────────────────────────

class RestorationQueue:
    def __init__(self) -> None:
        self._items: Deque[RestorationRequest] = deque()

    def add_request(self, request: RestorationRequest) -> None:
        self._items.append(request)

    def process_next_request(self) -> RestorationRequest | None:
        return self._items.popleft() if self._items else None

    def peek_next_request(self) -> RestorationRequest | None:
        return self._items[0] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)


# ── Stack ────────────────────────────────────────────────────────────────────

class ArchiveUndoStack:
    def __init__(self) -> None:
        self._items: list[str] = []

    def push_action(self, action: str) -> None:
        self._items.append(action)

    def undo_last_action(self) -> str | None:
        return self._items.pop() if self._items else None

    def peek_last_action(self) -> str | None:
        return self._items[-1] if self._items else None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)


# ── Linked List ──────────────────────────────────────────────────────────────

class ExhibitNode:
    def __init__(self, stop_name: str, next_node=None) -> None:
        self.stop_name = stop_name
        self.next = next_node


class ExhibitRoute:
    def __init__(self) -> None:
        self.head: ExhibitNode | None = None

    def add_stop(self, stop_name: str) -> None:
        new_node = ExhibitNode(stop_name)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def remove_stop(self, stop_name: str) -> bool:
        if self.head is None:
            return False
        if self.head.stop_name == stop_name:
            self.head = self.head.next
            return True
        current = self.head
        while current.next:
            if current.next.stop_name == stop_name:
                current.next = current.next.next
                return True
            current = current.next
        return False

    def list_stops(self) -> list[str]:
        stops, current = [], self.head
        while current:
            stops.append(current.stop_name)
            current = current.next
        return stops

    def count_stops(self) -> int:
        return len(self.list_stops())


# ── Utility Functions ────────────────────────────────────────────────────────

def count_artifacts_by_category(artifacts: list[Artifact]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for a in artifacts:
        counts[a.category] = counts.get(a.category, 0) + 1
    return counts


def unique_rooms(artifacts: list[Artifact]) -> set[str]:
    return {a.room for a in artifacts}


def sort_artifacts_by_age(artifacts: list[Artifact], descending: bool = False) -> list[Artifact]:
    return sorted(artifacts, key=lambda a: a.age, reverse=descending)


def linear_search_by_name(artifacts: list[Artifact], name: str) -> Artifact | None:
    for a in artifacts:
        if a.name == name:
            return a
    return None


# ── Demo ─────────────────────────────────────────────────────────────────────

def demo_museum_night() -> None:
    print("=== Moonlight Museum After Dark ===\n")
    artifacts = [
        Artifact(50, "Golden Mask",     "Jewelry",   3200, "Pharaoh Wing"),
        Artifact(20, "Clay Tablet",     "Relics",    4500, "Mesopotamia Hall"),
        Artifact(70, "Roman Sword",     "Weapons",    900, "Battle Room"),
        Artifact(10, "Obsidian Mirror", "Relics",    2000, "Aztec Gallery"),
        Artifact(30, "Silk Scroll",     "Documents",  600, "East Wing"),
    ]

    # BST
    bst = ArtifactBST()
    for a in artifacts:
        bst.insert(a)
    print("Inorder IDs:", bst.inorder_ids())
    print("Search 20  :", bst.search_by_id(20))
    print("Search 99  :", bst.search_by_id(99))

    # Queue
    queue = RestorationQueue()
    queue.add_request(RestorationRequest(50, "Polish surface"))
    queue.add_request(RestorationRequest(20, "Decipher glyphs"))
    print("Next restoration request:", queue.peek_next_request())
    print("Processed  :", queue.process_next_request())

    # Stack
    stack = ArchiveUndoStack()
    stack.push_action("Inserted artifact 50")
    stack.push_action("Deleted artifact 99")
    print("Undo action:", stack.undo_last_action())

    # Linked list
    route = ExhibitRoute()
    for stop in ["Entrance", "Pharaoh Wing", "Battle Room", "Exit"]:
        route.add_stop(stop)
    route.remove_stop("Battle Room")
    print("Exhibit route:", route.list_stops())

    # Utilities
    print("Category counts:", count_artifacts_by_category(artifacts))
    print("Rooms      :", unique_rooms(artifacts))
    print("By age     :", [a.name for a in sort_artifacts_by_age(artifacts)])
    print("Find name  :", linear_search_by_name(artifacts, "Roman Sword"))


if __name__ == "__main__":
    demo_museum_night()