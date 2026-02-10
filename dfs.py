from __future__ import annotations
from typing import List, Set, Tuple
from vacuum_world import VacuumWorld, State

# Keep action order stable for reproducible results
ACTION_ORDER = ("UP", "RIGHT", "DOWN", "LEFT", "CLEAN")


def dfs_search(problem: VacuumWorld):
    """
    Return: (solution_path, nodes_expanded, max_frontier_size)
      - solution_path: List[str] or None if no solution
      - nodes_expanded: number of states expanded (i.e., successors generated from that state)
      - max_frontier_size: max size of stack at any time

    DFS rules:
      - iterative (stack), no recursion
      - explored set to avoid cycles
      - returns first found solution (not necessarily optimal)
    """
    start = problem.initial_state()

    stack: List[Tuple[State, List[str]]] = [(start, [])]
    explored: Set[State] = set()

    nodes_expanded = 0
    max_frontier = 1

    while stack:
        max_frontier = max(max_frontier, len(stack))

        state, path = stack.pop()

        if problem.is_goal(state):
            return path, nodes_expanded, max_frontier

        if state in explored:
            continue

        explored.add(state)
        nodes_expanded += 1

        # Sort successors by action order, then push reversed so ACTION_ORDER is explored first (LIFO)
        succ = list(problem.successors(state))
        succ.sort(key=lambda x: ACTION_ORDER.index(x[0]))

        for action, next_state, _ in reversed(succ):
            if next_state not in explored:
                stack.append((next_state, path + [action]))

    return None, nodes_expanded, max_frontier
