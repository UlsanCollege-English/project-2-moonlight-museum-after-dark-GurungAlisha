[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tfm_-hwX)
# Project 2: Moonlight Museum After Dark

## Team information
- Team name:
- Members:
- Repository name:

---

## Project summary
Write 2-4 sentences explaining what your museum system does.

Example starters:
- Our project builds a system for organizing strange museum artifacts after dark.
- The system uses multiple data structures to manage artifacts, requests, routes, and reports.

---

## Feature checklist
Mark each item when it is working.

### Core structures
- [ ] `Artifact` class/record
- [ ] `ArtifactBST`
- [ ] `RestorationQueue`
- [ ] `ArchiveUndoStack`
- [ ] `ExhibitRoute` singly linked list

### BST features
- [ ] insert artifact
- [ ] search by ID
- [ ] preorder traversal
- [ ] inorder traversal
- [ ] postorder traversal
- [ ] duplicate IDs ignored

### Queue features
- [ ] add request
- [ ] process next request
- [ ] peek next request
- [ ] empty check
- [ ] size

### Stack features
- [ ] push action
- [ ] undo last action
- [ ] peek last action
- [ ] empty check
- [ ] size

### Linked list features
- [ ] add stop to end
- [ ] remove first matching stop
- [ ] list stops in order
- [ ] count stops

### Utility/report features
- [ ] category counts
- [ ] unique rooms
- [ ] sort by age
- [ ] linear search by name

### Integration
- [ ] `demo_museum_night()`
- [ ] at least 8 artifacts in demo
- [ ] demo shows system parts working together

---

## Design note (150-250 words)
Explain your main design choices.

Things to include:
- Why a BST makes sense for artifact IDs
- Why a queue fits restoration requests
- Why a stack fits undo actions
- Why a linked list fits an exhibit route
- How your system is organized across classes and functions

Write your note here:

---

## Complexity reasoning
Write short, specific explanations.

### Example format
- `ArtifactBST.search_by_id`: `O(h)` where `h` is the tree height, because the search follows one path from the root down.
- `RestorationQueue.process_next_request`: `O(1)` because deque removal from the front is constant time.

### Your required entries
- `ArtifactBST.insert`:
- `ArtifactBST.search_by_id`:
- `ArtifactBST.inorder_ids`:
- `RestorationQueue.process_next_request`:
- `ArchiveUndoStack.undo_last_action`:
- `ExhibitRoute.remove_stop`:
- `sort_artifacts_by_age`:
- `linear_search_by_name`:

---

## Edge-case checklist
Explain how your code handles each case.

### BST
- [ ] insert into empty tree
- [ ] search for missing ID
- [ ] empty traversals
- [ ] duplicate ID

### Queue
- [ ] process empty queue
- [ ] peek empty queue

### Stack
- [ ] undo empty stack
- [ ] peek empty stack

### Exhibit route linked list
- [ ] empty route
- [ ] remove missing stop
- [ ] remove first stop
- [ ] remove middle stop
- [ ] remove last stop
- [ ] one-stop route

### Reports
- [ ] empty artifact list
- [ ] repeated categories
- [ ] repeated rooms
- [ ] missing artifact name
- [ ] same-age artifacts

---

## Demo plan / how to run
Explain how someone should run your project.

Example:
```bash
pytest -q
python -c "from src.project import demo_museum_night; demo_museum_night()"
```

Write your steps here:

---

## Assistance & sources
This section is required.

- AI used? (Y/N)
- What it helped with:
- Non-course sources used:
- Links:
