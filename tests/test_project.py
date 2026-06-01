
"""Public tests for Project 2: Moonlight Museum After Dark."""

from __future__ import annotations

from src.project import (
    ArchiveUndoStack,
    Artifact,
    ArtifactBST,
    ExhibitRoute,
    RestorationQueue,
    RestorationRequest,
    count_artifacts_by_category,
    demo_museum_night,
    linear_search_by_name,
    sort_artifacts_by_age,
    unique_rooms,
)


def make_artifacts() -> list[Artifact]:
    return [
        Artifact(40, "Cursed Mirror", "mirror", 220, "North Hall"),
        Artifact(20, "Clockwork Bird", "machine", 80, "Workshop"),
        Artifact(60, "Whispering Map", "paper", 140, "Archive"),
        Artifact(10, "Glowing Key", "metal", 35, "Vault"),
        Artifact(30, "Moon Dial", "device", 120, "North Hall"),
        Artifact(50, "Silver Mask", "costume", 160, "Gallery"),
        Artifact(70, "Lantern Jar", "glass", 60, "Gallery"),
        Artifact(25, "Ink Compass", "device", 120, "Archive"),
    ]


# ---------------------------------------------------------------------------
# Artifact BST tests
# ---------------------------------------------------------------------------


def test_bst_search_empty_tree_returns_none() -> None:
    bst = ArtifactBST()
    assert bst.search_by_id(999) is None



def test_bst_empty_traversals_return_empty_lists() -> None:
    bst = ArtifactBST()
    assert bst.inorder_ids() == []
    assert bst.preorder_ids() == []
    assert bst.postorder_ids() == []



def test_bst_insert_first_artifact_creates_root_and_returns_true() -> None:
    bst = ArtifactBST()
    artifact = Artifact(40, "Cursed Mirror", "mirror", 220, "North Hall")
    assert bst.insert(artifact) is True
    found = bst.search_by_id(40)
    assert found == artifact



def test_bst_search_returns_existing_artifact() -> None:
    bst = ArtifactBST()
    for artifact in make_artifacts():
        bst.insert(artifact)

    found = bst.search_by_id(50)
    assert found is not None
    assert found.name == "Silver Mask"
    assert found.room == "Gallery"



def test_bst_search_missing_id_returns_none() -> None:
    bst = ArtifactBST()
    for artifact in make_artifacts():
        bst.insert(artifact)

    assert bst.search_by_id(999) is None



def test_bst_duplicate_id_is_ignored_and_returns_false() -> None:
    bst = ArtifactBST()
    original = Artifact(40, "Cursed Mirror", "mirror", 220, "North Hall")
    duplicate = Artifact(40, "Fake Mirror", "mirror", 5, "Closet")

    assert bst.insert(original) is True
    assert bst.insert(duplicate) is False

    found = bst.search_by_id(40)
    assert found == original
    assert found != duplicate



def test_bst_inorder_ids_are_sorted() -> None:
    bst = ArtifactBST()
    for artifact in make_artifacts():
        bst.insert(artifact)

    assert bst.inorder_ids() == [10, 20, 25, 30, 40, 50, 60, 70]



def test_bst_preorder_ids_match_expected_shape() -> None:
    bst = ArtifactBST()
    for artifact in make_artifacts():
        bst.insert(artifact)

    assert bst.preorder_ids() == [40, 20, 10, 30, 25, 60, 50, 70]



def test_bst_postorder_ids_match_expected_shape() -> None:
    bst = ArtifactBST()
    for artifact in make_artifacts():
        bst.insert(artifact)

    assert bst.postorder_ids() == [10, 25, 30, 20, 50, 70, 60, 40]


# ---------------------------------------------------------------------------
# Restoration queue tests
# ---------------------------------------------------------------------------


def test_queue_is_empty_at_start() -> None:
    queue = RestorationQueue()
    assert queue.is_empty() is True
    assert queue.size() == 0



def test_queue_peek_empty_returns_none() -> None:
    queue = RestorationQueue()
    assert queue.peek_next_request() is None



def test_queue_process_empty_returns_none() -> None:
    queue = RestorationQueue()
    assert queue.process_next_request() is None



def test_queue_add_and_peek_do_not_remove_item() -> None:
    queue = RestorationQueue()
    request = RestorationRequest(40, "Polish cracked frame")
    queue.add_request(request)

    assert queue.peek_next_request() == request
    assert queue.size() == 1
    assert queue.is_empty() is False



def test_queue_processes_requests_in_fifo_order() -> None:
    queue = RestorationQueue()
    first = RestorationRequest(40, "Polish cracked frame")
    second = RestorationRequest(20, "Oil the wing gears")
    third = RestorationRequest(60, "Flatten folded corner")

    queue.add_request(first)
    queue.add_request(second)
    queue.add_request(third)

    assert queue.process_next_request() == first
    assert queue.process_next_request() == second
    assert queue.process_next_request() == third
    assert queue.process_next_request() is None


# ---------------------------------------------------------------------------
# Undo stack tests
# ---------------------------------------------------------------------------


def test_stack_is_empty_at_start() -> None:
    stack = ArchiveUndoStack()
    assert stack.is_empty() is True
    assert stack.size() == 0



def test_stack_peek_empty_returns_none() -> None:
    stack = ArchiveUndoStack()
    assert stack.peek_last_action() is None



def test_stack_undo_empty_returns_none() -> None:
    stack = ArchiveUndoStack()
    assert stack.undo_last_action() is None



def test_stack_push_and_peek_do_not_remove_item() -> None:
    stack = ArchiveUndoStack()
    stack.push_action("Added Cursed Mirror to archive")

    assert stack.peek_last_action() == "Added Cursed Mirror to archive"
    assert stack.size() == 1
    assert stack.is_empty() is False



def test_stack_undo_follows_lifo_order() -> None:
    stack = ArchiveUndoStack()
    first = "Added Cursed Mirror to archive"
    second = "Queued Clockwork Bird repair"
    third = "Removed Secret Vault stop"

    stack.push_action(first)
    stack.push_action(second)
    stack.push_action(third)

    assert stack.undo_last_action() == third
    assert stack.undo_last_action() == second
    assert stack.undo_last_action() == first
    assert stack.undo_last_action() is None


# ---------------------------------------------------------------------------
# Exhibit route linked list tests
# ---------------------------------------------------------------------------


def test_route_starts_empty() -> None:
    route = ExhibitRoute()
    assert route.list_stops() == []
    assert route.count_stops() == 0



def test_route_add_stop_appends_to_end() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    route.add_stop("Mirror Room")
    route.add_stop("Clockwork Gallery")

    assert route.list_stops() == [
        "Entrance",
        "Mirror Room",
        "Clockwork Gallery",
    ]
    assert route.count_stops() == 3



def test_route_remove_missing_stop_returns_false() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    route.add_stop("Mirror Room")

    assert route.remove_stop("Lantern Vault") is False
    assert route.list_stops() == ["Entrance", "Mirror Room"]



def test_route_remove_from_empty_route_returns_false() -> None:
    route = ExhibitRoute()
    assert route.remove_stop("Entrance") is False



def test_route_remove_first_stop() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    route.add_stop("Mirror Room")
    route.add_stop("Clockwork Gallery")

    assert route.remove_stop("Entrance") is True
    assert route.list_stops() == ["Mirror Room", "Clockwork Gallery"]



def test_route_remove_middle_stop() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    route.add_stop("Mirror Room")
    route.add_stop("Clockwork Gallery")

    assert route.remove_stop("Mirror Room") is True
    assert route.list_stops() == ["Entrance", "Clockwork Gallery"]



def test_route_remove_last_stop() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")
    route.add_stop("Mirror Room")
    route.add_stop("Clockwork Gallery")

    assert route.remove_stop("Clockwork Gallery") is True
    assert route.list_stops() == ["Entrance", "Mirror Room"]



def test_route_remove_only_stop_leaves_empty_route() -> None:
    route = ExhibitRoute()
    route.add_stop("Entrance")

    assert route.remove_stop("Entrance") is True
    assert route.list_stops() == []
    assert route.count_stops() == 0


# ---------------------------------------------------------------------------
# Utility/report tests
# ---------------------------------------------------------------------------


def test_category_counts_empty_list_returns_empty_dict() -> None:
    assert count_artifacts_by_category([]) == {}



def test_category_counts_repeated_categories_correctly() -> None:
    artifacts = make_artifacts()
    counts = count_artifacts_by_category(artifacts)

    assert counts["device"] == 2
    assert counts["mirror"] == 1
    assert counts["glass"] == 1



def test_unique_rooms_empty_list_returns_empty_set() -> None:
    assert unique_rooms([]) == set()



def test_unique_rooms_removes_duplicates() -> None:
    rooms = unique_rooms(make_artifacts())
    assert rooms == {"North Hall", "Workshop", "Archive", "Vault", "Gallery"}



def test_sort_artifacts_by_age_ascending() -> None:
    artifacts = make_artifacts()
    sorted_artifacts = sort_artifacts_by_age(artifacts)
    sorted_ids = [artifact.artifact_id for artifact in sorted_artifacts]

    assert sorted_ids == [10, 70, 20, 30, 25, 60, 50, 40]



def test_sort_artifacts_by_age_descending() -> None:
    artifacts = make_artifacts()
    sorted_artifacts = sort_artifacts_by_age(artifacts, descending=True)
    sorted_ids = [artifact.artifact_id for artifact in sorted_artifacts]

    assert sorted_ids == [40, 50, 60, 30, 25, 20, 70, 10]



def test_sort_artifacts_by_age_empty_list_returns_empty_list() -> None:
    assert sort_artifacts_by_age([]) == []



def test_linear_search_by_name_returns_matching_artifact() -> None:
    artifacts = make_artifacts()
    found = linear_search_by_name(artifacts, "Whispering Map")

    assert found is not None
    assert found.artifact_id == 60
    assert found.room == "Archive"



def test_linear_search_by_name_missing_returns_none() -> None:
    artifacts = make_artifacts()
    assert linear_search_by_name(artifacts, "Phantom Teapot") is None



def test_linear_search_by_name_empty_list_returns_none() -> None:
    assert linear_search_by_name([], "Anything") is None


# ---------------------------------------------------------------------------
# Demo smoke test
# ---------------------------------------------------------------------------


def test_demo_museum_night_runs_and_prints_key_sections(capsys) -> None:
    demo_museum_night()
    captured = capsys.readouterr()
    output = captured.out

    assert "Moonlight Museum After Dark" in output
    assert "Inorder IDs:" in output
    assert "Next restoration request:" in output
    assert "Undo action:" in output
    assert "Exhibit route:" in output
    assert "Category counts:" in output