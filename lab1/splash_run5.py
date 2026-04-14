import os
from pathlib import Path

import m5
from m5.objects import (
    AddrRange,
    Cache,
    L2XBar,
    Process,
    Root,
    SEWorkload,
    SimpleMemory,
    SrcClockDomain,
    System,
    SystemXBar,
    VoltageDomain,
    X86AtomicSimpleCPU,
    X86O3CPU,
    X86TimingSimpleCPU,
)


# Lab configuration: edit these values directly before each run.
THIS_DIR = Path(__file__).resolve().parent
ROOTDIR = (THIS_DIR.parent / "codes").resolve()
RESULTS_DIR = THIS_DIR / "results"

BENCHMARK = os.environ.get("BENCH", "barnes").strip().lower()
NUM_CPUS = 4
CPU_MODEL = "timing"  # "timing", "atomic", or "o3"
MAX_TICK = None

FREQUENCY = "1GHz"
MEM_SIZE = "2GiB"
CACHELINE_SIZE = 64

USE_L2 = True
L1_SIZE = "64KiB"
L1_LATENCY = 2
L1_IASSOC = 1
L1_DASSOC = 4
L2_SIZE = "256KiB"
L2_LATENCY = 10
L2_ASSOC = 8


def normalized_benchmark():
    aliases = {
        "lu": "lucontig",
        "ocean": "oceancontig",
        "ocean_contig": "oceancontig",
        "ocean_noncontig": "oceannoncontig",
        "ocean_noncontiguous": "oceannoncontig",
        "water_spatial": "waterspatial",
        "water_nsquared": "waternsquared",
        "water-nsquared": "waternsquared",
        "lu_contig": "lucontig",
        "lu_noncontig": "lunoncontig",
        "lu_noncontiguous": "lunoncontig",
    }
    return aliases.get(BENCHMARK, BENCHMARK)


def first_existing_path(*candidates):
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def build_process():
    bench = normalized_benchmark()

    def p(*parts):
        return ROOTDIR.joinpath(*parts)

    if bench == "cholesky":
        proc = Process()
        proc.cwd = str(p("kernels", "cholesky"))
        proc.executable = str(p("kernels", "cholesky", "CHOLESKY"))
        proc.cmd = ["CHOLESKY", f"-p{NUM_CPUS}", "inputs/tk23.O"]
        return proc

    if bench == "fft":
        proc = Process()
        proc.cwd = str(p("kernels", "fft"))
        proc.executable = str(p("kernels", "fft", "FFT"))
        proc.cmd = ["FFT", "-p", str(NUM_CPUS), "-m18"]
        return proc

    if bench == "lucontig":
        proc = Process()
        proc.cwd = str(p("kernels", "lu", "contiguous_blocks"))
        proc.executable = str(p("kernels", "lu", "contiguous_blocks", "LU"))
        proc.cmd = ["LU", "-p", str(NUM_CPUS)]
        return proc

    if bench == "lunoncontig":
        proc = Process()
        proc.cwd = str(p("kernels", "lu", "non_contiguous_blocks"))
        proc.executable = str(p("kernels", "lu", "non_contiguous_blocks", "LU"))
        proc.cmd = ["LU", "-p", str(NUM_CPUS)]
        return proc

    if bench == "radix":
        proc = Process()
        proc.cwd = str(p("kernels", "radix"))
        proc.executable = str(p("kernels", "radix", "RADIX"))
        proc.cmd = ["RADIX", "-n524288", "-p", str(NUM_CPUS)]
        return proc

    if bench == "barnes":
        proc = Process()
        proc.cwd = str(p("apps", "barnes"))
        proc.executable = str(p("apps", "barnes", "BARNES"))
        proc.cmd = ["BARNES"]
        proc.input = str(
            first_existing_path(
                p("apps", "barnes", f"input.p{NUM_CPUS}"),
                p("apps", "barnes", "inputs", f"n8k-p{NUM_CPUS}"),
                p("apps", "barnes", "inputs", f"n16384-p{NUM_CPUS}"),
            )
        )
        return proc

    if bench == "fmm":
        proc = Process()
        proc.cwd = str(p("apps", "fmm"))
        proc.executable = str(p("apps", "fmm", "FMM"))
        proc.cmd = ["FMM"]
        proc.input = str(
            first_existing_path(
                p("apps", "fmm", "inputs", "input.2048"),
                p("apps", "fmm", "inputs", f"input.2048.p{NUM_CPUS}"),
                p("apps", "fmm", "inputs", f"input.{NUM_CPUS}.2048"),
            )
        )
        return proc

    if bench == "oceancontig":
        proc = Process()
        proc.cwd = str(p("apps", "ocean", "contiguous_partitions"))
        proc.executable = str(p("apps", "ocean", "contiguous_partitions", "OCEAN"))
        proc.cmd = ["OCEAN", "-p", str(NUM_CPUS)]
        return proc

    if bench == "oceannoncontig":
        proc = Process()
        proc.cwd = str(p("apps", "ocean", "non_contiguous_partitions"))
        proc.executable = str(
            p("apps", "ocean", "non_contiguous_partitions", "OCEAN")
        )
        proc.cmd = ["OCEAN", "-p", str(NUM_CPUS)]
        return proc

    if bench == "raytrace":
        proc = Process()
        proc.cwd = str(p("apps", "raytrace"))
        proc.executable = str(p("apps", "raytrace", "RAYTRACE"))
        proc.cmd = ["RAYTRACE", f"-p{NUM_CPUS}", "inputs/teapot.env"]
        return proc

    if bench == "waternsquared":
        proc = Process()
        proc.cwd = str(p("apps", "water-nsquared"))
        proc.executable = str(p("apps", "water-nsquared", "WATER-NSQUARED"))
        proc.cmd = ["WATER-NSQUARED"]
        proc.input = str(
            first_existing_path(
                p("apps", "water-nsquared", "input"),
                p("apps", "water-nsquared", f"input.p{NUM_CPUS}"),
                p("apps", "water-nsquared", "inputs", f"n512-p{NUM_CPUS}"),
            )
        )
        return proc

    if bench == "waterspatial":
        proc = Process()
        proc.cwd = str(p("apps", "water-spatial"))
        proc.executable = str(p("apps", "water-spatial", "WATER-SPATIAL"))
        proc.cmd = ["WATER-SPATIAL"]
        proc.input = str(
            first_existing_path(
                p("apps", "water-spatial", "input"),
                p("apps", "water-spatial", f"input.p{NUM_CPUS}"),
                p("apps", "water-spatial", "inputs", f"n512-p{NUM_CPUS}"),
            )
        )
        return proc

    raise ValueError(f"Unsupported benchmark: {BENCHMARK}")


class L1(Cache):
    mshrs = 12
    tgts_per_mshr = 8


class L2(Cache):
    mshrs = 92
    tgts_per_mshr = 16
    write_buffers = 8


def build_cpus():
    cpu_map = {
        "atomic": (X86AtomicSimpleCPU, "atomic"),
        "timing": (X86TimingSimpleCPU, "timing"),
        "o3": (X86O3CPU, "timing"),
    }
    cpu_cls, mem_mode = cpu_map[CPU_MODEL]
    return [cpu_cls(cpu_id=i) for i in range(NUM_CPUS)], mem_mode


if not ROOTDIR.exists():
    raise FileNotFoundError(f"ROOTDIR does not exist: {ROOTDIR}")

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

cpus, mem_mode = build_cpus()

system = System(
    cpu=cpus,
    physmem=SimpleMemory(),
    membus=SystemXBar(),
    mem_mode=mem_mode,
    mem_ranges=[AddrRange(MEM_SIZE)],
    cache_line_size=CACHELINE_SIZE,
)
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = FREQUENCY
system.clk_domain.voltage_domain = VoltageDomain()

system.physmem.range = system.mem_ranges[0]
system.physmem.port = system.membus.mem_side_ports
system.system_port = system.membus.cpu_side_ports

if USE_L2:
    system.toL2bus = L2XBar()
    system.l2 = L2(
        size=L2_SIZE,
        assoc=L2_ASSOC,
        tag_latency=L2_LATENCY,
        data_latency=L2_LATENCY,
        response_latency=L2_LATENCY,
    )
    system.l2.cpu_side = system.toL2bus.mem_side_ports
    system.l2.mem_side = system.membus.cpu_side_ports

for cpu in cpus:
    cpu.createInterruptController()
    cpu.addPrivateSplitL1Caches(
        L1(
            size=L1_SIZE,
            assoc=L1_IASSOC,
            tag_latency=L1_LATENCY,
            data_latency=L1_LATENCY,
            response_latency=L1_LATENCY,
        ),
        L1(
            size=L1_SIZE,
            assoc=L1_DASSOC,
            tag_latency=L1_LATENCY,
            data_latency=L1_LATENCY,
            response_latency=L1_LATENCY,
        ),
    )
    if USE_L2:
        cpu.connectAllPorts(
            system.toL2bus.cpu_side_ports,
            system.membus.cpu_side_ports,
            system.membus.mem_side_ports,
        )
    else:
        cpu.connectAllPorts(
            system.membus.cpu_side_ports,
            system.membus.cpu_side_ports,
            system.membus.mem_side_ports,
        )

process = build_process()
system.workload = SEWorkload.init_compatible(process.executable)
for cpu in cpus:
    cpu.workload = process
    cpu.createThreads()

root = Root(full_system=False, system=system)
m5.instantiate()

if MAX_TICK is not None:
    exit_event = m5.simulate(MAX_TICK)
else:
    exit_event = m5.simulate(m5.MaxTick)

print("Exiting @ tick", m5.curTick(), "because", exit_event.getCause())
