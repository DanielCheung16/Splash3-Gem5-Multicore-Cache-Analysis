BASEDIR := $(dir $(realpath $(lastword $(MAKEFILE_LIST))))
NAME ?= 5out
OUTDIR := $(BASEDIR)/results/$(NAME)
CASE ?= case1
BENCH ?= barnes

NUM ?= 1
GEM5 := ~/nu_projects/gem5/build/ALL/gem5.opt
PY_RUN := $(BASEDIR)/splash_run$(NUM).py

CORE1_RUN := $(BASEDIR)/splash_run1.py
CORE2_RUN := $(BASEDIR)/splash_run2.py
CORE4_RUN := $(BASEDIR)/splash_run3.py
CORE8_RUN := $(BASEDIR)/splash_run4.py
CORE16_RUN := $(BASEDIR)/splash_run5.py

run:
	mkdir -p $(OUTDIR)
	BENCH=$(BENCH) $(GEM5) \
		--listener-mode=off \
		--remote-gdb-port=0 \
		--outdir=$(OUTDIR) \
		$(PY_RUN)

burst_run_case1:
	mkdir -p $(BASEDIR)/results
	mkdir -p $(BASEDIR)/results/$(CASE)_$(BENCH)_core1
	mkdir -p $(BASEDIR)/results/$(CASE)_$(BENCH)_core2
	mkdir -p $(BASEDIR)/results/$(CASE)_$(BENCH)_core4
	mkdir -p $(BASEDIR)/results/$(CASE)_$(BENCH)_core8
	mkdir -p $(BASEDIR)/results/$(CASE)_$(BENCH)_core16
	BENCH=$(BENCH) $(GEM5) --listener-mode=off --remote-gdb-port=0 --outdir=$(BASEDIR)/results/$(CASE)_$(BENCH)_core1 $(CORE1_RUN) > $(BASEDIR)/results/$(CASE)_$(BENCH)_core1/sim.log 2>&1 &
	BENCH=$(BENCH) $(GEM5) --listener-mode=off --remote-gdb-port=0 --outdir=$(BASEDIR)/results/$(CASE)_$(BENCH)_core2 $(CORE2_RUN) > $(BASEDIR)/results/$(CASE)_$(BENCH)_core2/sim.log 2>&1 &
	BENCH=$(BENCH) $(GEM5) --listener-mode=off --remote-gdb-port=0 --outdir=$(BASEDIR)/results/$(CASE)_$(BENCH)_core4 $(CORE4_RUN) > $(BASEDIR)/results/$(CASE)_$(BENCH)_core4/sim.log 2>&1 &
	BENCH=$(BENCH) $(GEM5) --listener-mode=off --remote-gdb-port=0 --outdir=$(BASEDIR)/results/$(CASE)_$(BENCH)_core8 $(CORE8_RUN) > $(BASEDIR)/results/$(CASE)_$(BENCH)_core8/sim.log 2>&1 &
	BENCH=$(BENCH) $(GEM5) --listener-mode=off --remote-gdb-port=0 --outdir=$(BASEDIR)/results/$(CASE)_$(BENCH)_core16 $(CORE16_RUN) > $(BASEDIR)/results/$(CASE)_$(BENCH)_core16/sim.log 2>&1 &
	@echo "Started 5 runs in background:"
	@echo "  $(CASE)_$(BENCH)_core1"
	@echo "  $(CASE)_$(BENCH)_core2"
	@echo "  $(CASE)_$(BENCH)_core4"
	@echo "  $(CASE)_$(BENCH)_core8"
	@echo "  $(CASE)_$(BENCH)_core16"
	@echo "Use 'ps -ef | grep [g]em5' to check progress."

run_one:
	mkdir -p $(BASEDIR)/results/$(CASE)_$(BENCH)_core1
	BENCH=$(BENCH) $(GEM5) --listener-mode=off --remote-gdb-port=0 --outdir=$(BASEDIR)/results/$(CASE)_$(BENCH)_core1 $(CORE1_RUN) > $(BASEDIR)/results/$(CASE)_$(BENCH)_core1/sim.log 2>&1 &