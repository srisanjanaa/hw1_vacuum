from __future__ import annotations

import csv
import time
from typing import Any, Dict, List, Tuple, Optional

from vacuum_world import VacuumWorld
from heuristics import h_dirty_plus_nearest

from dfs import dfs_search
from astar import astar_search
from idastar import idastar_search

from plots import plot_results


ResultRow = Tuple[str, str, Optional[int], Optional[int], Optional[int], Optional[float]]
# (map_name, algo, path_len, nodes_expanded, frontier_or_iters, runtime_ms)


def timed_call(fn, *args, **kwargs):
    t0 = time.perf_counter()
    out = fn(*args, **kwargs)
    t1 = time.perf_counter()
    runtime_ms = (t1 - t0) * 1000.0
    return out, runtime_ms


def save_csv(results: List[ResultRow], filename: str = "results.csv") -> None:
    headers = ["map", "algorithm", "path_len", "nodes_expanded", "frontier_or_iters", "runtime_ms"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for row in results:
            w.writerow(row)
    print(f"Saved results: {filename}")


def main():
    maps: Dict[str, List[str]] = {
        "map1_easy": [
            "S..",
            ".D.",
            "...",
        ],
        "map2_obstacles": [
            "S#..",
            ".#D.",
            "..#.",
            "....",
        ],
        "map3_more_dirt": [
            "S.D..",
            ".#.#.",
            ".D.D.",
            ".#.#.",
            ".....",
        ],
    }

    results: List[ResultRow] = []

    for name, grid in maps.items():
        problem = VacuumWorld.from_grid(grid)
        print("\n===", name, "===")
        print(problem.pretty(problem.initial_state()))

        # DFS
        try:
            (path, expanded, frontier), rt = timed_call(dfs_search, problem)
            results.append((name, "DFS",
                            len(path) if path else None,
                            expanded,
                            frontier,
                            rt))
        except Exception as e:
            print(f"[DFS] failed on {name}: {e}")
            results.append((name, "DFS", None, None, None, None))

        # A*
        try:
            (path, expanded, frontier), rt = timed_call(astar_search, problem, h_dirty_plus_nearest)
            results.append((name, "A*",
                            len(path) if path else None,
                            expanded,
                            frontier,
                            rt))
        except Exception as e:
            print(f"[A*] failed on {name}: {e}")
            results.append((name, "A*", None, None, None, None))

        # IDA*
        try:
            (path, expanded, iters), rt = timed_call(idastar_search, problem, h_dirty_plus_nearest)
            results.append((name, "IDA*",
                            len(path) if path else None,
                            expanded,
                            iters,
                            rt))
        except Exception as e:
            print(f"[IDA*] failed on {name}: {e}")
            results.append((name, "IDA*", None, None, None, None))

    print("\nRESULTS (map, algo, path_len, expanded, frontier/iters, runtime_ms)")
    for row in results:
        print(row)

    save_csv(results, "results.csv")
    plot_results(results)


if __name__ == "__main__":
    main()
