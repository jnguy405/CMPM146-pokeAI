from ai_agent import (
    choose_action,
    EXT_CTRL_ACTION_MOVE,
    EXT_CTRL_ACTION_ITEM,
    EXT_CTRL_ACTION_SWITCH,
)


def test_choose_action_prefers_move_over_switch_and_item():
    info = {
        "moves": [(1, 10), (0, 0), (0, 0), (0, 0)],
        "num_switches": 1,
        "switch_slots": [2],
        "trainer_items": [100, 0, 0, 0],
        "is_double": 0,
        "move_targets": [0, 0, 0, 0],
        "field_species": [0, 0, 0, 0],
        "active_battler_id": 1,
    }

    action, index, target = choose_action(info)

    assert action == EXT_CTRL_ACTION_MOVE
    assert index == 0
    assert target == 0


def test_choose_action_switches_when_no_moves_available():
    info = {
        "moves": [(0, 0), (0, 0), (0, 0), (0, 0)],
        "num_switches": 1,
        "switch_slots": [3],
        "trainer_items": [0, 0, 0, 0],
        "is_double": 0,
        "move_targets": [0, 0, 0, 0],
        "field_species": [0, 0, 0, 0],
        "active_battler_id": 1,
    }

    action, index, target = choose_action(info)

    assert action == EXT_CTRL_ACTION_SWITCH
    assert index == 3
    assert target == 0


def test_choose_action_uses_item_when_only_items_available():
    info = {
        "moves": [(0, 0), (0, 0), (0, 0), (0, 0)],
        "num_switches": 0,
        "switch_slots": [],
        "trainer_items": [0, 200, 0, 0],
        "is_double": 0,
        "move_targets": [0, 0, 0, 0],
        "field_species": [0, 0, 0, 0],
        "active_battler_id": 1,
    }

    action, index, target = choose_action(info)

    assert action == EXT_CTRL_ACTION_ITEM
    assert index == 1
    assert target == 0
