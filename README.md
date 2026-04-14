# Splash3-Gem5 Multicore Cache Analysis

This repository contains a gem5-based CE453 Lab 1 project using Splash-3
benchmarks to study two questions:

1. Whether multicore execution improves performance.
2. How private L1 cache size affects performance and cache behavior.

The project uses Splash-3 as the workload suite and gem5 in SE mode as the
simulation platform.

## What This Project Does

The experiment is split into two cases.

- `case1`: Vary the core count and measure multicore speedup.
- `case2`: Fix the system at 4 cores and vary the L1 cache size.

The selected benchmarks are:

- `barnes`
- `fft`
- `lu`
- `ocean`
- `radix`

## Repository Structure

- `codes/`
  Compiled Splash-3 benchmarks and input files.

- `lab1/`
  Main experiment workspace.

- `lab1/splash_run*.py`
  gem5 configuration scripts used to run different experiment settings.

- `lab1/Makefile`
  Helper targets for running single cases or batched cases.

- `lab1/report_data/`
  Processed CSV data and plotting scripts for the report.

- `lab1/CE453_lab1/`
  LaTeX source and figures for the final report.

## Main Results

- `case1_summary.csv`
  Summarizes speedup, CPI, and cache miss rates when the core count changes.

- `case2_summary.csv`
  Summarizes performance and miss-rate changes when the L1 size changes.

- `case1_speedup_by_benchmark.png`
  Grouped bar chart showing multicore speedup across benchmarks.

- `case2_speedup_by_l1size.png`
  Grouped bar chart showing speedup under different L1 cache sizes.

## How To Run

Run a single benchmark case:

```bash
cd lab1
make BENCH=barnes run
```

Run a batched case:

```bash
cd lab1
make CASE=case1 BENCH=barnes burst_run_case1
```

## Notes

- `lab1/results/` is ignored by Git because it contains large raw simulation
  outputs.
- `lab1/report_data/` stores the processed data used in the report.
- The report figures are regenerated from the CSV files using the plotting
  scripts in `lab1/report_data/`.

## Reference

C. Sakalis, C. Leonardsson, S. Kaxiras, and A. Ros, “Splash-3: A properly
synchronized benchmark suite for contemporary research,” in \textit{IEEE
International Symposium on Performance Analysis of Systems and Software
(ISPASS)}, 2016.
