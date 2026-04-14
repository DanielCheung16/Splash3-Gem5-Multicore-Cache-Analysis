import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CSV_PATH = Path(__file__).resolve().parent / "case1_summary.csv"
OUT_PATH = Path(__file__).resolve().parent / "case1_speedup_by_benchmark.png"

BENCH_ORDER = ["barnes", "fft", "lu", "ocean", "radix"]
CORE_ORDER = [1, 2, 4, 8, 16]
COLORS = ["#d7e3f4", "#aac7e8", "#74a9d8", "#3f7fbf", "#1e4f7a"]


def load_speedups():
    speedups = defaultdict(dict)
    with CSV_PATH.open() as f:
        for row in csv.DictReader(f):
            speedups[row["benchmark"]][int(row["cores"])] = float(row["speedup"])
    return speedups


def main():
    speedups = load_speedups()

    # Tuned for a paper with 10pt body text.
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 8,
        }
    )

    fig, ax = plt.subplots(figsize=(6.7, 3.8), dpi=220)

    x = np.arange(len(BENCH_ORDER))
    width = 0.15

    for idx, core in enumerate(CORE_ORDER):
        vals = [speedups[b][core] for b in BENCH_ORDER]
        offset = (idx - (len(CORE_ORDER) - 1) / 2) * width
        ax.bar(
            x + offset,
            vals,
            width=width,
            label=f"{core} cores",
            color=COLORS[idx],
            edgecolor="black",
            linewidth=0.45,
        )

    #ax.set_title("Case 1: Speedup Across Benchmarks and Core Counts", pad=10)
    ax.set_ylabel("Speedup", labelpad=4)
    ax.set_xlabel("Benchmarks", labelpad=3)
    ax.set_xticks(x)
    ax.set_xticklabels([b.capitalize() for b in BENCH_ORDER])
    ax.grid(axis="y", linestyle="--", alpha=0.35, linewidth=0.6)
    ax.set_axisbelow(True)

    # Put legend above the axes, outside plotting area, so it never overlaps.
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.16),
        ncol=5,
        frameon=False,
        handlelength=1.2,
        columnspacing=1.0,
    )

    # Compact margins while keeping title/legend separate.
    fig.subplots_adjust(left=0.1, right=0.985, bottom=0.18, top=0.78)

    fig.savefig(OUT_PATH, bbox_inches="tight")
    print(OUT_PATH)


if __name__ == "__main__":
    main()
