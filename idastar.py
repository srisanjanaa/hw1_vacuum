from __future__ import annotations
from typing import Callable, List, Optional, Set, Tuple
from vacuum_world import VacuumWorld, State

Heuristic = Callable[[State], int]
ACTION_ORDER = ("UP", "RIGHT", "DOWN", "LEFT", "CLEAN")
INF = 10**18


def idastar_search(problem: VacuumWorld, h: Heuristic):
    """
    Return: (solution_path, nodes_expanded, iterations)

    IDA* rules:
      - threshold starts at h(start)
      - DFS prunes when f=g+h > threshold
      - if not found, next threshold = minimum f that exceeded threshold
      - no global explored across iterations (linear memory),
        but we DO use path_states to avoid cycles in the current DFS path.
    """
    start = problem.initial_state()
    threshold = h(start)

    total_expanded = 0
    iterations = 0

    while True:
        iterations += 1
        path_actions: List[str] = []
        path_states: Set[State] = {start}

        found_path, min_excess, expanded = _dfs_f_limited(
            problem=problem,
            h=h,
            state=start,
            g=0,
            threshold=threshold,
            path_actions=path_actions,
            path_states=path_states,
        )

        total_expanded += expanded

        if found_path is not None:
            return found_path, total_expanded, iterations

        if min_excess == INF:
            return None, total_expanded, iterations

        threshold = min_excess


def _dfs_f_limited(
    problem: VacuumWorld,
    h: Heuristic,
    state: State,
    g: int,
    threshold: int,
    path_actions: List[str],
    path_states: Set[State],
) -> Tuple[Optional[List[str]], int, int]:
    """
    Returns: (found_path_or_None, min_excess_f, nodes_expanded_in_this_call)

    min_excess_f:
      - the smallest f-value that exceeded current threshold in this subtree
      - used as the next threshold if no solution is found in this iteration
    """
    f = g + h(state)
    if f > threshold:
        return None, f, 0

    if problem.is_goal(state):
        return list(path_actions), INF, 0

    nodes_expanded = 1
    min_excess = INF

    succ = list(problem.successors(state))
    succ.sort(key=lambda x: ACTION_ORDER.index(x[0]))

    for action, nxt, cost in succ:
        if nxt in path_states:
            continue

        path_states.add(nxt)
        path_actions.append(action)

        found, excess, expanded = _dfs_f_limited(
            problem=problem,
            h=h,
            state=nxt,
            g=g + cost,
            threshold=threshold,
            path_actions=path_actions,
            path_states=path_states,
        )

        nodes_expanded += expanded

        if found is not None:
            return found, INF, nodes_expanded

        if excess < min_excess:
            min_excess = excess

        path_actions.pop()
        path_states.remove(nxt)

    return None, min_excess, nodes_expanded
