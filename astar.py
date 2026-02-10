from __future__ import annotations
import heapq
from typing import Callable, Dict, List, Tuple
from vacuum_world import VacuumWorld, State

Heuristic = Callable[[State], int]
ACTION_ORDER = ("UP", "RIGHT", "DOWN", "LEFT", "CLEAN")


def _reconstruct_path(came_from: Dict[State, Tuple[State, str]], goal: State) -> List[str]:
    actions: List[str] = []
    cur = goal
    while cur in came_from:
        prev, act = came_from[cur]
        actions.append(act)
        cur = prev
    actions.reverse()
    return actions


def astar_search(problem: VacuumWorld, h: Heuristic):
    """
    Return: (solution_path, nodes_expanded, max_frontier_size)

    A* rules:
      - PQ ordered by f = g + h
      - reopen/update a state if a better g is found
      - nodes_expanded increments when we expand a popped state (generate successors)
    """
    start = problem.initial_state()

    # PQ entries: (f, tie, state)
    pq: List[Tuple[int, int, State]] = []
    tie = 0

    g_score: Dict[State, int] = {start: 0}
    came_from: Dict[State, Tuple[State, str]] = {}

    heapq.heappush(pq, (h(start), tie, start))
    tie += 1

    nodes_expanded = 0
    max_frontier = 1

    while pq:
        max_frontier = max(max_frontier, len(pq))

        f, _, state = heapq.heappop(pq)

        # Lazy deletion: skip outdated queue entries
        # (This avoids needing a decrease-key operation.)
        current_f = g_score.get(state, None)
        if current_f is None:
            continue
        if f != current_f + h(state):
            continue

        if problem.is_goal(state):
            return _reconstruct_path(came_from, state), nodes_expanded, max_frontier

        nodes_expanded += 1

        succ = list(problem.successors(state))
        succ.sort(key=lambda x: ACTION_ORDER.index(x[0]))

        for action, nxt, cost in succ:
            tentative_g = g_score[state] + cost
            if (nxt not in g_score) or (tentative_g < g_score[nxt]):
                g_score[nxt] = tentative_g
                came_from[nxt] = (state, action)
                heapq.heappush(pq, (tentative_g + h(nxt), tie, nxt))
                tie += 1

    return None, nodes_expanded, max_frontier
