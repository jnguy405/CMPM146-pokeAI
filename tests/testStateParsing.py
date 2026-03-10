from external_controller import parse_waiting_state


def test_parse_waiting_state_basic():
    # Construct a minimal WAITING message without STATE payload.
    parts = ["WAITING"]

    # num_moves and 4 (move, pp) pairs
    parts.append("2")  # num_moves
    parts += [
        "1", "10",  # move 0
        "2", "0",   # move 1 (no PP)
        "0", "0",   # move 2 empty
        "0", "0",   # move 3 empty
    ]

    # num_switches and 5 (slot, species) pairs
    parts.append("1")  # num_switches
    parts += [
        "1", "25",  # one valid switch slot
        "0", "0",
        "0", "0",
        "0", "0",
        "0", "0",
    ]

    # num_items and 4 item ids
    parts.append("1")  # num_items
    parts += ["100", "0", "0", "0"]

    # is_double, active_battler_id
    parts += ["0", "1"]

    # field_species[4]
    parts += ["10", "20", "0", "0"]

    # move_targets[4]
    parts += ["0", "0", "0", "0"]

    msg = " ".join(parts)
    info = parse_waiting_state(msg)

    assert info is not None
    assert info["num_moves"] == 2
    assert info["moves"][0] == (1, 10)
    assert info["num_switches"] == 1
    assert info["switch_slots"] == [1]
    assert info["num_items"] == 1
    assert info["trainer_items"][0] == 100
