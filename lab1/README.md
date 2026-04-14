# Lab 1 Splash Runner

This directory contains the Lab 1 runner for Splash benchmarks on gem5 25.1.

`../codes/` stores the shared Splash benchmark binaries and inputs.
`splash_run.py` is the lab-owned script for cache experiments.

Run from anywhere, but keep the benchmark root pointed at `../codes` unless you
intentionally move it.

Example:

```bash
/home/zpxlinux/nu_projects/gem5/build/ALL/gem5.opt \
  --outdir=/home/zpxlinux/nu_projects/ce453_parallel/benchmarks/Splash_3_Gem5/lab1/results/barnes_default \
  /home/zpxlinux/nu_projects/ce453_parallel/benchmarks/Splash_3_Gem5/lab1/splash_run.py \
  -t -b Barnes -n 4
```

Change cache settings through command line options instead of editing the
script:

```bash
/home/zpxlinux/nu_projects/gem5/build/ALL/gem5.opt \
  --outdir=/home/zpxlinux/nu_projects/ce453_parallel/benchmarks/Splash_3_Gem5/lab1/results/fft_large_cache \
  /home/zpxlinux/nu_projects/ce453_parallel/benchmarks/Splash_3_Gem5/lab1/splash_run.py \
  -t -b FFT -n 4 \
  --l1size 64KiB --l1latency 2 --l1iassoc 2 --l1dassoc 8 \
  --l2size 1MiB --l2latency 20 --l2assoc 16
```

Useful options:

- `-t`: timing CPU, recommended for cache experiments
- `-d`: O3 CPU
- `--atomic`: atomic CPU
- `--no-l2`: remove the shared L2 cache
- `--rootdir`: override the benchmark root if `codes/` moves
- `-m`: stop after a fixed number of ticks

Suggested results layout:

```text
lab1/results/<benchmark>/<config_name>/
```
