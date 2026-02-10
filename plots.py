from __future__ import annotations

import matplotlib.pyplot as plt
from typing import Dict, List, Optional, Tuple

ResultRow = Tuple[str, str, Optional[int], Optional[int], Optional[int], Optional[float]]
# (map_name, algo, path_len, nodes_expanded, frontier_or_iters, runtime_ms)

ALGOS = ["DFS", "A*", "IDA*"]


def _add_bar_labels(bars):
    for b in bars:
        h = b.get_height()
        if h is None:
            continue
        if h == 0:
            continue
        plt.text(
            b.get_x() + b.get_width() / 2,
            h,
            f"{h:.0f}",
            ha="center",
            va="bottom",
            fontsize=9,
        )


def _group_by_map(results: List[ResultRow]):
    maps = sorted(set(r[0] for r in results))
    grouped: Dict[str, Dict[str, ResultRow]] = {m: {} for m in maps}
    for row in results:
        m, algo = row[0], row[1]
        grouped[m][algo] = row
    return maps, grouped


def _bar_chart(maps, grouped, metric_index: int, ylabel: str, title: str, outname: str):
    """
    metric_index:
      2 = path_len
      3 = nodes_expanded
      4 = frontier_or_iters
      5 = runtime_ms
    """
    x = list(range(len(maps)))
    width = 0.25

    plt.figure()
    for i, algo in enumerate(ALGOS):
        ys = []
        for m in maps:
            row = grouped[m].get(algo)
            val = row[metric_index] if row else None
            ys.append(float(val) if isinstance(val, (int, float)) else 0.0)

        bars = plt.bar([xi + (i - 1) * width for xi in x], ys, width=width, label=algo)
        _add_bar_labels(bars)

    plt.xticks(x, maps, rotation=20, ha="right")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(outname, dpi=200)
    print(f"Saved plot: {outname}")


def plot_results(results: List[ResultRow]) -> None:
    # Keep only rows that have at least nodes_expanded computed
    clean = [r for r in results if isinstance(r[3], int)]
    if not clean:
        print("No numeric results yet. Skipping plots.")
        return

    maps, grouped = _group_by_map(clean)

    # Nodes expanded
    _bar_chart(
        maps, grouped,
        metric_index=3,
        ylabel="Nodes Expanded",
        title="Vacuum World Search: Nodes Expanded by Algorithm",
        outname="nodes_expanded.png"
    )

    # Path length
    _bar_chart(
        maps, grouped,
        metric_index=2,
        ylabel="Solution Path Length",
        title="Vacuum World Search: Solution Path Length by Algorithm",
        outname="path_length.png"
    )

    # Frontier size / Iterations (mixed meaning but still useful to show)
    _bar_chart(
        maps, grouped,
        metric_index=4,
        ylabel="Max Frontier (DFS/A*) or Iterations (IDA*)",
        title="Vacuum World Search: Frontier/Iterations by Algorithm",
        outname="frontier_or_iters.png"
    )

    # Runtime (ms)
    # Some very small runs may show ~0ms, that’s fine.
    _bar_chart(
        maps, grouped,
        metric_index=5,
        ylabel="Runtime (ms)",
        title="Vacuum World Search: Runtime by Algorithm",
        outname="runtime_ms.png"
    )
