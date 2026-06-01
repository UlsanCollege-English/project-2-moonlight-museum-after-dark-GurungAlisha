"""Project 2: Moonlight Museum After Dark.

Complete implementation using stdlib only.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque


@dataclass(frozen=True)
class Artifact:
    """A museum artifact stored in the archive BST."""

    artifact_id: int
    name: str
    category: str
    age: int
    room: str


@dataclass(frozen=True)
class RestorationRequest:
    """A request to inspect or repair an artifact."""

    artifact_id: int
    description: str


# ---------------------------------------------------------------------------
# BST
# ---------------------------------------------------------------------------

class TreeNode:
    """A node for the artifact BST."""

    def __init__(
        self,
        artifact: Artifact,
        left: TreeNode | None = None,
        right: TreeNode | None = None,
    ) -> None:
        self.artifact = artifact
        self.left = left
        self.right = right


class ArtifactBST:
    """Binary search tree keyed by artifact_id.

    HOW A BST WORKS:
    - Every node has a value (artifact_id here).
    - Smaller IDs go to the LEFT child.
    - Larger IDs go to the RIGHT child.
    - This lets us search in O(h) time instead of O(n).

    TRAVERSALS:
    - Inorder  (Left → Root → Right) → gives sorted order
    - Preorder (Root → Left → Right) → useful for copying a tree
    - Postorder(Left → Right → Root) → useful for deleting a tree
    """

    def __init__(self) -> None:
        self.root: TreeNode | None = None

    # -- insert --

    def insert(self, artifact: Artifact) -> bool:
        """Insert an artifact. Returns False if ID already exists."""
        # If tree is empty, this artifact becomes the root
        if self.root is None:
            self.root = TreeNode(artifact)
            return True
        return self._insert(self.root, artifact)

    def _insert(self, node: TreeNode, artifact: Artifact) -> bool:
        """Recursive helper: walk left or right until we find a spot."""
        if artifact.artifact_id == node.artifact.artifact_id:
            return False                        # duplicate → ignore
        if artifact.artifact_id < node.artifact.artifact_id:
            if node.left is None:
                node.left = TreeNode(artifact)  # empty spot on the left → place it
                return True
            return self._insert(node.left, artifact)   # keep going left
        else:
            if node.right is None:
                node.right = TreeNode(artifact) # empty spot on the right → place it
                return True
            return self._insert(node.right, artifact)  # keep going right

    # -- search --

    def search_by_id(self, artifact_id: int) -> Artifact | None:
        """Return the matching artifact, or None."""
        return self._search(self.root, artifact_id)

    def _search(self, node: TreeNode | None, artifact_id: int) -> Artifact | None:
        if node is None:
            return None                                  # fell off the tree → not found
        if artifact_id == node.artifact.artifact_id:
            return node.artifact                         # found it
        if artifact_id < node.artifact.artifact_id:
            return self._search(node.left, artifact_id) # go left
        return self._search(node.right, artifact_id)    # go right

    # -- traversals --

    def inorder_ids(self) -> list[int]:
        """Left → Root → Right  (produces sorted IDs)."""
        result: list[int] = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._inorder(node.left, result)        # go all the way left first
        result.append(node.artifact.artifact_id)
        self._inorder(node.right, result)       # then go right

    def preorder_ids(self) -> list[int]:
        """Root → Left → Right."""
        result: list[int] = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        result.append(node.artifact.artifact_id)  # visit root first
        self._preorder(node.left, result)
        self._preorder(node.right, result)

    def postorder_ids(self) -> list[int]:
        """Left → Right → Root."""
        result: list[int] = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node: TreeNode | None, result: list[int]) -> None:
        if node is None:
            return
        self._postorder(node.left, result)
        self._postorder(node.right, result)
        result.append(node.artifact.artifact_id)  # visit root last


# ---------------------------------------------------------------------------
# Queue  (FIFO — first in, first out)
# ---------------------------------------------------------------------------

class RestorationQueue:
    """Uses collections.deque so popleft() is O(1)."""

    def __init__(self) -> None:
        self._items: Deque[RestorationRequest] = deque()

    def add_request(self, request: RestorationRequest) -> None:
        self._items.append(request)         # add to the back

    def process_next_request(self) -> RestorationRequest | None:
        if self._items:
            return self._items.popleft()    # remove from the front
        return None

    def peek_next_request(self) -> RestorationRequest | None:
        if self._items:
            return self._items[0]           # look at front without removing
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)


# ---------------------------------------------------------------------------
# Stack  (LIFO — last in, first out)
# ---------------------------------------------------------------------------

class ArchiveUndoStack:
    """Uses a plain list. append() pushes, pop() undoes."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push_action(self, action: str) -> None:
        self._items.append(action)          # add to the top

    def undo_last_action(self) -> str | None:
        if self._items:
            return self._items.pop()        # remove from the top
        return None

    def peek_last_action(self) -> str | None:
        if self._items:
            return self._items[-1]          # look at top without removing
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)


# ---------------------------------------------------------------------------
# Singly linked list (exhibit route)
# ---------------------------------------------------------------------------

class ExhibitNode:
    """A node in the singly linked exhibit route."""

    def __init__(self, stop_name: str, next_node: ExhibitNode | None = None) -> None:
        self.stop_name = stop_name
        self.next = next_node


class ExhibitRoute:
    """Singly linked list of exhibit stops.

    HOW REMOVAL WORKS:
    - Keep a 'prev' pointer one step behind 'current'.
    - When you find the node to remove, set prev.next = current.next
      which skips over the node we want to delete.
    - Special case: if the head itself is the target, just move head forward.
    """

    def __init__(self) -> None:
        self.head: ExhibitNode | None = None

    def add_stop(self, stop_name: str) -> None:
        """Walk to the end, then attach a new node."""
        new_node = ExhibitNode(stop_name)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def remove_stop(self, stop_name: str) -> bool:
        """Remove the first matching stop. Returns True if removed."""
        if self.head is None:
            return False

        # Special case: head is the target
        if self.head.stop_name == stop_name:
            self.head = self.head.next
            return True

        # General case: walk with prev and current
        prev = self.head
        current = self.head.next
        while current is not None:
            if current.stop_name == stop_name:
                prev.next = current.next    # skip over current
                return True
            prev = current
            current = current.next

        return False  # not found

    def list_stops(self) -> list[str]:
        stops = []
        current = self.head
        while current is not None:
            stops.append(current.stop_name)
            current = current.next
        return stops

    def count_stops(self) -> int:
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count


# ---------------------------------------------------------------------------
# Utility / report functions
# ---------------------------------------------------------------------------

def count_artifacts_by_category(artifacts: list[Artifact]) -> dict[str, int]:
    """Count how many artifacts belong to each category."""
    counts: dict[str, int] = {}
    for artifact in artifacts:
        counts[artifact.category] = counts.get(artifact.category, 0) + 1
    return counts


def unique_rooms(artifacts: list[Artifact]) -> set[str]:
    """Return the set of all rooms that appear in the artifact list."""
    return {artifact.room for artifact in artifacts}


def sort_artifacts_by_age(
    artifacts: list[Artifact],
    descending: bool = False,
) -> list[Artifact]:
    """Return a new list sorted by age (youngest first by default)."""
    return sorted(artifacts, key=lambda a: a.age, reverse=descending)


def linear_search_by_name(
    artifacts: list[Artifact],
    name: str,
) -> Artifact | None:
    """Walk through the list and return the first exact name match."""
    for artifact in artifacts:
        if artifact.name == name:
            return artifact
    return None


# ---------------------------------------------------------------------------
# Integration demo
# ---------------------------------------------------------------------------

def demo_museum_night() -> None:
    """Show the full system working together."""

    print("=" * 50)
    print("   Moonlight Museum After Dark — Night Demo")
    print("=" * 50)

    # -- 8 artifacts --
    artifacts = [
        Artifact(40, "Cursed Mirror",   "mirror",  220, "North Hall"),
        Artifact(20, "Clockwork Bird",  "machine",  80, "Workshop"),
        Artifact(60, "Whispering Map",  "paper",   140, "Archive"),
        Artifact(10, "Glowing Key",     "metal",    35, "Vault"),
        Artifact(30, "Moon Dial",       "device",  120, "North Hall"),
        Artifact(50, "Silver Mask",     "costume", 160, "Gallery"),
        Artifact(70, "Lantern Jar",     "glass",    60, "Gallery"),
        Artifact(25, "Ink Compass",     "device",  120, "Archive"),
    ]

    # -- BST --
    print("\n--- BST ---")
    bst = ArtifactBST()
    for a in artifacts:
        bst.insert(a)

    print("Inorder IDs:", bst.inorder_ids())
    print("Preorder IDs:", bst.preorder_ids())
    print("Postorder IDs:", bst.postorder_ids())

    found = bst.search_by_id(50)
    print(f"Search ID 50 → {found.name if found else 'Not found'}")
    print(f"Search ID 99 → {bst.search_by_id(99) or 'Not found'}")

    # -- Queue --
    print("\n--- Restoration Queue ---")
    queue = RestorationQueue()
    queue.add_request(RestorationRequest(40, "Polish cracked frame"))
    queue.add_request(RestorationRequest(20, "Oil the wing gears"))
    queue.add_request(RestorationRequest(60, "Flatten folded corner"))
    print(f"Next restoration request: {queue.peek_next_request().description}")
    print(f"Processing: {queue.process_next_request().description}")
    print(f"Queue size after processing: {queue.size()}")

    # -- Stack --
    print("\n--- Undo Stack ---")
    stack = ArchiveUndoStack()
    stack.push_action("Added Cursed Mirror to archive")
    stack.push_action("Queued Clockwork Bird repair")
    stack.push_action("Removed Secret Vault stop")
    print(f"Undo action: {stack.undo_last_action()}")
    print(f"Undo action: {stack.undo_last_action()}")
    print(f"Stack size after undos: {stack.size()}")

    # -- Linked list --
    print("\n--- Exhibit Route ---")
    route = ExhibitRoute()
    for stop in ["Entrance", "Mirror Room", "Clockwork Gallery", "Vault", "Exit"]:
        route.add_stop(stop)
    print("Exhibit route:", route.list_stops())
    route.remove_stop("Clockwork Gallery")
    print("After removing 'Clockwork Gallery':", route.list_stops())

    # -- Reports --
    print("\n--- Reports ---")
    print("Category counts:", count_artifacts_by_category(artifacts))
    print("Unique rooms:", unique_rooms(artifacts))
    print("Sorted by age (asc):", [a.name for a in sort_artifacts_by_age(artifacts)])
    found_name = linear_search_by_name(artifacts, "Moon Dial")
    print(f"Search by name 'Moon Dial' → {found_name.name if found_name else 'Not found'}")
