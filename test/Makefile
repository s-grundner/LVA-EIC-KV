# ============================================================================== 
# Makefile
# See https://docs.cocotb.org/en/stable/quickstart.html for more info
# ============================================================================== 

# ------------------------------------------------------------------------------ 
# defaults
# ------------------------------------------------------------------------------ 

SIM ?= icarus
# SIM ?= verilator
TOPLEVEL_LANG ?= verilog
RELATIVE_SRC_DIR ?= ../src
SRC_DIR = $(PWD)/$(RELATIVE_SRC_DIR)

# ------------------------------------------------------------------------------ 
# Project source files:
# ------------------------------------------------------------------------------ 

PROJECT_SOURCES = \
	tt_um_s_grundner.v \
	global.v \
	counter.v \
	pwm.v \
	rx.v \
	midi.v \
	note2cnt.v \
	osc.v \
	synth.v

# ------------------------------------------------------------------------------ 
# Simulation settings: RTL / Gate Level
# ------------------------------------------------------------------------------

ifneq ($(GATES),yes)

# RTL simulation:
SIM_BUILD = sim_build/rtl
VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

else

# Gate level simulation:
SIM_BUILD = sim_build/gl
COMPILE_ARGS += -DGL_TEST
COMPILE_ARGS += -DFUNCTIONAL
COMPILE_ARGS += -DUSE_POWER_PINS
COMPILE_ARGS += -DSIM
COMPILE_ARGS += -DUNIT_DELAY=\#1
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# this gets copied in by the GDS action workflow
VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

endif

# Common Compiler arguments:
# Set include path for project source files
COMPILE_ARGS += -I$(SRC_DIR)

# ------------------------------------------------------------------------------
# Define each test and its Verilog testbench
# Format: TEST_NAME:TOPLEVEL:TESTBENCH_FILE
# ------------------------------------------------------------------------------

# Mandatory testbench test for GHA pass
TEST_CONFIGS = test:tb:tb.v 

# Custom module tests
ifneq ($(GATES),yes)
TEST_CONFIGS += \
	test_counter:tb_counter:tb_counter.v \
	test_note2cnt:tb_note2cnt:tb_note2cnt.v
endif

# Default rule to run all tests
.DEFAULT_GOAL := all

# Generate Test Names
TEST_NAMES = $(foreach config,$(TEST_CONFIGS),$(firstword $(subst :, ,$(config))))

# Run all tests
all: $(TEST_NAMES)
	
# Rule to run each test
$(TEST_NAMES):
	$(eval CFG := $(filter $@:%, $(TEST_CONFIGS)))
	$(eval TEST_MODULE := $(word 1,$(subst :, ,$(CFG))))
	$(eval TOPLEVEL := $(word 2,$(subst :, ,$(CFG))))
	$(eval TB_FILE := $(word 3,$(subst :, ,$(CFG))))

	@echo "=============================================="
	@echo " Running Cocotb test: $(TEST_MODULE)"
	@echo " Top-level: $(TOPLEVEL)"
	@echo " File: $(TB_FILE)"
	@echo "=============================================="

	@mkdir -p results
	@mkdir -p waves

	$(MAKE) -f $(shell cocotb-config --makefiles)/Makefile.sim \
		SIM=$(SIM) \
		TOPLEVEL_LANG=$(TOPLEVEL_LANG) \
		TOPLEVEL=$(TOPLEVEL) \
		COCOTB_TEST_MODULES=$(TEST_MODULE) \
		COCOTB_RESULTS_FILE=$(PWD)/results/$(TEST_MODULE)_results.xml \
		COMPILE_ARGS="$(COMPILE_ARGS)" \
		VERILOG_SOURCES="$(VERILOG_SOURCES) $(PWD)/benches/$(TB_FILE)" \
		SIM_BUILD="$(PWD)/$(SIM_BUILD)/$(TEST_MODULE)" \
		WAVES=1 \

# ------------------------------
# Cleanup
# ------------------------------

clean:
	rm -rf results sim_build waves

.PHONY: all clean-builds $(TEST_NAMES)

