from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet, Tuple, Iterable, List, Optional, Dict

Pos = Tuple[int, int]
State = Tuple[Pos, FrozenSet[Pos]]

ACTIONS: Tuple[str, ...] = ("UP", "RIGHT", "DOWN", "LEFT", "CLEAN")


@dataclass(frozen=True)
class VacuumWorld:
    rows: int
    cols: int
    obstacles: FrozenSet[Pos]
    start: Pos
    dirties: FrozenSet[Pos]

    @staticmethod
    def from_grid(grid: List[str]) -> "VacuumWorld":
        """
        Grid legend:
          'S' start
          '#' obstacle
          'D' dirty
          '.' empty
        """
        rows = len(grid)
        cols = len(grid[0]) if rows else 0

        obstacles = set()
        dirties = set()
        start: Optional[Pos] = None

        for r in range(rows):
            if len(grid[r]) != cols:
                raise ValueError("All rows must have same length")
            for c, ch in enumerate(grid[r]):
                if ch == "#":
                    obstacles.add((r, c))
                elif ch == "D":
                    dirties.add((r, c))
                elif ch == "S":
                    start = (r, c)

        if start is None:
            raise ValueError("Grid must contain a start cell 'S'")

        return VacuumWorld(
            rows=rows,
            cols=cols,
            obstacles=frozenset(obstacles),
            start=start,
            dirties=frozenset(dirties),
        )

    def initial_state(self) -> State:
        return (self.start, self.dirties)

    def is_goal(self, state: State) -> bool:
        _, dirty = state
        return len(dirty) == 0

    def successors(self, state: State) -> Iterable[Tuple[str, State, int]]:
        """
        Yields (action, next_state, step_cost).
        We treat invalid actions as illegal and DO NOT yield them.
        """
        (r, c), dirty = state

        moves = {
            "UP": (r - 1, c),
            "RIGHT": (r, c + 1),
            "DOWN": (r + 1, c),
            "LEFT": (r, c - 1),
        }

        # Move actions
        for act in ("UP", "RIGHT", "DOWN", "LEFT"):
            nr, nc = moves[act]
            if 0 <= nr < self.rows and 0 <= nc < self.cols and (nr, nc) not in self.obstacles:
                yield (act, ((nr, nc), dirty), 1)

        # Clean action
        if (r, c) in dirty:
            new_dirty = frozenset(cell for cell in dirty if cell != (r, c))
            yield ("CLEAN", ((r, c), new_dirty), 1)

    def pretty(self, state: State) -> str:
        pos, dirty = state
        lines = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                p = (r, c)
                if p == pos:
                    row.append("R")
                elif p in self.obstacles:
                    row.append("#")
                elif p in dirty:
                    row.append("D")
                elif p == self.start:
                    row.append("S")
                else:
                    row.append(".")
            lines.append("".join(row))
        return "\n".join(lines)
