# cocotb Makefile

# 顶层模块
TOPLEVEL = {{RTL_TOP}}
MODULE = test_{{RTL_TOP}}

# 默认使用 iverilog
SIM ?= iverilog

# 源码路径
RTL_DIR = ../../DesignData/RTL
TB_DIR = ../../Verification/Env

# Verilog 源文件
VERILOG_SOURCES = $(RTL_DIR)/{{RTL_TOP}}.v

# cocotb 配置
export COCOTB_REDUCED_LOG_FMT = 1

# 包含 cocotb 配置
include $(shell cocotb-config --makefiles)/Makefile.sim

.PHONY: help

help:
	@echo "cocotb Test Framework"
	@echo ""
	@echo "Usage: make [SIM=simulator]"
	@echo ""
	@echo "Simulators:"
	@echo "  make SIM=iverilog   # Icarus Verilog (default)"
	@echo "  make SIM=verilator  # Verilator"
	@echo "  make SIM=ghdl       # GHDL"
	@echo ""
	@echo "Other targets:"
	@echo "  make clean          # Clean build files"
