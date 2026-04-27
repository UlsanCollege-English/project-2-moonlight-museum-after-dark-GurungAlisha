[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tfm_-hwX)
# Project 2: Moonlight Museum After Dark


## Project summary

Our project builds a management system for a museum's after-dark archive operations. It uses a Binary Search Tree to store and retrieve artifacts by ID, a queue to handle restoration requests in order, a stack to track and undo archive actions, and a singly linked list to manage the exhibit tour route. Together these structures power a full demo that simulates a night shift at the museum.

---

## Feature checklist

### Core structures
- [x] `Artifact` class/record
- [x] `ArtifactBST`
- [x] `RestorationQueue`
- [x] `ArchiveUndoStack`
- [x] `ExhibitRoute` singly linked list

### BST features
- [x] insert artifact
- [x] search by ID
- [x] preorder traversal
- [x] inorder traversal
- [x] postorder traversal
- [x] duplicate IDs ignored

### Queue features
- [x] add request
- [x] process next request
- [x] peek next request
- [x] empty check
- [x] size

### Stack features
- [x] push action
- [x] undo last action
- [x] peek last action
- [x] empty check
- [x] size

### Linked list features
- [x] add stop to end
- [x] remove first matching stop
- [x] list stops in order
- [x] count stops

### Utility/report features
- [x] category counts
- [x] unique rooms
- [x] sort by age
- [x] linear search by name

### Integration
- [x] `demo_museum_night()`
- [x] at least 8 artifacts in demo
- [x] demo shows system parts working together

---

## Design note (150-250 words)

A Binary Search Tree is the natural fit for artifact IDs because each ID is a unique integer, which means every insert and search follows a clear left/right path. Inorder traversal of the BST automatically returns IDs in sorted order, which is useful for generating reports without an extra sort step.

A queue fits restoration requests because conservators must handle them in the order they were submitted — first in, first out. Using `collections.deque` gives O(1) appends at the back and O(1) pops from the front, making both `add_request` and `process_next_request` efficient.

A stack fits undo actions because the most recent archive operation is always the one that needs to be undone first — last in, first out. A plain Python list with `append` and `pop` from the end gives O(1) performance for both push and undo.

A singly linked list fits the exhibit route because stops are visited in sequence and the route changes frequently (stops added or removed at any point). Linked lists handle insertions and deletions without shifting elements, which keeps the route flexible.

The system is split into four self-contained classes (BST, Queue, Stack, ExhibitRoute) plus four standalone utility functions for reporting. This separation keeps each data structure focused on one responsibility and makes the code easy to test independently.

---

## Complexity reasoning

- `ArtifactBST.insert`: `O(h)` where `h` is the tree height, because each step moves either left or right down one level until an empty spot is found.
- `ArtifactBST.search_by_id`: `O(h)` where `h` is the tree height, because the search follows one path from root to the target node (or a leaf).
- `ArtifactBST.inorder_ids`: `O(n)` where `n` is the number of nodes, because every node is visited exactly once.
- `RestorationQueue.process_next_request`: `O(1)` because `deque.popleft()` removes from the front in constant time.
- `ArchiveUndoStack.undo_last_action`: `O(1)` because `list.pop()` removes from the end in constant time.
- `ExhibitRoute.remove_stop`: `O(n)` where `n` is the number of stops, because the list may need to be traversed to find the target node.
- `sort_artifacts_by_age`: `O(n log n)` because Python's built-in `sorted()` uses Timsort.
- `linear_search_by_name`: `O(n)` where `n` is the number of artifacts, because in the worst case every artifact is checked before finding a match (or returning None).

---

## Edge-case checklist

### BST
- [x] insert into empty tree — `self.root` is `None`, so a new root node is created directly.
- [x] search for missing ID — the iterative search reaches `None` and returns `None`.
- [x] empty traversals — the recursive `walk` helper returns immediately when `node` is `None`, producing an empty list.
- [x] duplicate ID — `_insert` checks `artifact_id == node.artifact.artifact_id` and returns `False` without inserting.

### Queue
- [x] process empty queue — `process_next_request` checks `if self._items` and returns `None` when the deque is empty.
- [x] peek empty queue — `peek_next_request` returns `None` the same way.

### Stack
- [x] undo empty stack — `undo_last_action` checks `if self._items` and returns `None`.
- [x] peek empty stack — `peek_last_action` returns `None` the same way.

### Exhibit route linked list
- [x] empty route — `remove_stop` returns `False` immediately; `list_stops` returns `[]`.
- [x] remove missing stop — the loop exhausts without a match and returns `False`.
- [x] remove first stop — detected by checking `self.head.stop_name` and reassigning `self.head`.
- [x] remove middle stop — the loop finds the predecessor node and relinks `current.next`.
- [x] remove last stop — handled by the same predecessor-relinking logic; the tail's `next` becomes `None`.
- [x] one-stop route — removing the only stop hits the head check and sets `self.head = None`.

### Reports
- [x] empty artifact list — all four utility functions return empty containers (`{}`, `set()`, `[]`, `None`).
- [x] repeated categories — `count_artifacts_by_category` accumulates counts correctly with `dict.get`.
- [x] repeated rooms — `unique_rooms` uses a set, so duplicates are automatically ignored.
- [x] missing artifact name — `linear_search_by_name` returns `None` after checking every artifact.
- [x] same-age artifacts — `sort_artifacts_by_age` uses a stable sort, so ties preserve original order.

---

## Demo plan / how to run

Run the demo directly:

```bash
python moonlight_museum.py
```

This executes `demo_museum_night()` which exercises all four data structures and all four utility functions and prints results to the terminal.

---

## Assistance & sources
- AI used? Y
- What it helped with: code structure, implementation of BST traversals, queue/stack/linked-list methods, and utility functions.
- Non-course sources used: Python standard library documentation (`collections.deque`, `dataclasses`).
- Links: https://docs.python.org/3/library/collections.html#collections.deque