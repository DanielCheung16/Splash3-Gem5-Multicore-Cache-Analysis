import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


CSV_PATH = Path(__file__).resolve().parent / "case2_summary.csv"
OUT_PATH = Path(__file__).resolve().parent / "case2_speedup_by_l1size.png"

BENCH_ORDER = ["lu", "ocean", "radix"]
L1_ORDER = ["4KiB", "8KiB", "16KiB", "32KiB", "64KiB"]
COLORS = ["#ead6c4", "#d9b99b", "#c88f6a", "#ab6540", "#7c4324"]


def load_rows():
    rows = []
    with CSV_PATH.open() as f:
        for row in csv.DictReader(f):
            row["simTicks"] = int(row["simTicks"])
            rows.append(row)
    return rows


def main():
    rows = load_rows()
    ticks = defaultdict(dict)
    for row in rows:
        ticks[row["benchmark"]][row["l1Size"]] = row["simTicks"]

    speedup = defaultdict(dict)
    for bench in BENCH_ORDER:
        baseline = ticks[bench]["4KiB"]
        for l1 in L1_ORDER:
            speedup[bench][l1] = baseline / ticks[bench][l1]

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

    fig, ax = plt.subplots(figsize=(6.4, 3.8), dpi=220)
    x = np.arange(len(BENCH_ORDER))
    width = 0.1

    for idx, l1 in enumerate(L1_ORDER):
        vals = [speedup[b][l1] for b in BENCH_ORDER]
        offset = (idx - (len(L1_ORDER) - 1) / 2) * width
        ax.bar(
            x + offset,
            vals,
            width=width,
            label=l1,
            color=COLORS[idx],
            edgecolor="black",
            linewidth=0.45,
        )

    #ax.set_title("Case 2: Speedup Across Benchmarks and L1 Cache Sizes", pad=10)
    ax.set_ylabel("Speedup", labelpad=4)
    ax.set_xlabel("Benchmarks", labelpad=3)
    ax.set_ylim(0.9, 1.18)
    ax.set_xticks(x)
    ax.set_xticklabels([b.capitalize() for b in BENCH_ORDER])
    ax.grid(axis="y", linestyle="--", alpha=0.35, linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_yticks(np.arange(0.9, 1.181, 0.05))
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.62, 1.16),
        ncol=5,
        frameon=False,
        handlelength=1.2,
        columnspacing=1.0,
    )
    fig.text(0.4, 0.837, "L1 size:", fontsize=8, ha="right", va="center")
    fig.subplots_adjust(left=0.1, right=0.985, bottom=0.18, top=0.78)
    fig.savefig(OUT_PATH, bbox_inches="tight")
    print(OUT_PATH)


if __name__ == "__main__":
    main()
