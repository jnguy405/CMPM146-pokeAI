from dotenv import load_dotenv
import os
from typing import Any, Dict, Tuple


# Action constants mirror external_controller.py / ROM contract
EXT_CTRL_ACTION_MOVE = 0
EXT_CTRL_ACTION_ITEM = 1
EXT_CTRL_ACTION_SWITCH = 2


load_dotenv()  # loads .env into environment

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def choose_action(info: Dict[str, Any]) -> Tuple[int, int, int]:
    """Basic rule-based policy: prefer moves, then switches, then items."""
    moves = info.get("moves", [])
    trainer_items = info.get("trainer_items", [])
    num_switches = info.get("num_switches", 0)
    switch_slots = info.get("switch_slots", [])

    valid_move_slots = [
        i for i, (mid, pp) in enumerate(moves)
        if mid != 0 and pp > 0
    ]
    valid_item_slots = [
        i for i, item_id in enumerate(trainer_items)
        if item_id != 0
    ]

    has_moves = bool(valid_move_slots)
    has_switches = num_switches > 0 and bool(switch_slots)
    has_items = bool(valid_item_slots)

    if has_moves:
        index = valid_move_slots[0]
        # For now, always target 0 (the game will resolve for non-selected moves).
        return EXT_CTRL_ACTION_MOVE, index, 0

    if has_switches:
        return EXT_CTRL_ACTION_SWITCH, switch_slots[0], 0

    if has_items:
        return EXT_CTRL_ACTION_ITEM, valid_item_slots[0], 0

    # Fallback: force move slot 0 (typically Struggle if nothing else is legal).
    return EXT_CTRL_ACTION_MOVE, 0, 0
