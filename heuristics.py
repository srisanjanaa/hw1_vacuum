from typing import FrozenSet, Tuple

Pos = Tuple[int, int]
State = Tuple[Pos, FrozenSet[Pos]]

def h_num_dirty(state: State) -> int:
    """Admissible: each remaining dirty requires at least one CLEAN action."""
    _, dirty = state
    return len(dirty)

def manhattan(a: Pos, b: Pos) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def h_dirty_plus_nearest(state: State) -> int:
    """
    Admissible: must clean each dirty (+|D|) and must reach some dirty (>= nearest Manhattan).
    Manhattan ignores obstacles => optimistic => admissible.
    """
    pos, dirty = state
    if not dirty:
        return 0
    nearest = min(manhattan(pos, d) for d in dirty)
    return len(dirty) + nearest
