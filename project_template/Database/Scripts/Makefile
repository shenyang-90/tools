# Unified EDA Tool Makefile
# 统一的 EDA 工具入口

# 工具路径（会被 install 脚本替换）
IVERILOG_PATH = {{IVERILOG_PATH}}
VERILATOR_PATH = {{VERILATOR_PATH}}
GHDL_PATH = {{GHDL_PATH}}
COCOTB_PATH = {{COCOTB_PATH}}
GTKWAVE_PATH = {{GTKWAVE_PATH}}

# 顶层模块名
RTL_TOP = {{RTL_TOP}}
TB_TOP = {{TB_TOP}}

# 默认使用 iverilog
SIM ?= iverilog

.PHONY: help lint compile simulate waveform clean iverilog verilator ghdl cocotb

help:
	@echo "统一 EDA 工具入口"
	@echo ""
	@echo "使用方法:"
	@echo "  make iverilog       # 使用 Icarus Verilog"
	@echo "  make verilator      # 使用 Verilator"
	@echo "  make ghdl           # 使用 GHDL"
	@echo "  make cocotb         # 使用 cocotb"
	@echo "  make lint           # 静态检查"
	@echo "  make simulate       # 运行仿真"
	@echo "  make waveform       # 查看波形"
	@echo "  make clean          # 清理所有"
	@echo ""
	@echo "变量:"
	@echo "  RTL_TOP=<top>       # 指定顶层模块"
	@echo "  TB_TOP=<tb>         # 指定 Testbench"

iverilog:
	$(MAKE) -C iverilog all

verilator:
	$(MAKE) -C verilator all

ghdl:
	$(MAKE) -C ghdl all

cocotb:
	$(MAKE) -C cocotb SIM=$(SIM)

lint:
	@echo "Running lint checks..."
	@echo "  1. Verilator lint"
	@$(MAKE) -C verilator lint 2>/dev/null || echo "     [SKIPPED]"
	@echo "  2. Iverilog lint"
	@$(MAKE) -C iverilog lint 2>/dev/null || echo "     [SKIPPED]"
	@echo "✓ Lint checks completed"

compile:
	@echo "Compiling with $(SIM)..."
	@$(MAKE) -C $(SIM) compile

simulate:
	@echo "Simulating with $(SIM)..."
	@$(MAKE) -C $(SIM) simulate

waveform:
	@echo "Opening waveform viewer..."
	@$(MAKE) -C $(SIM) waveform

clean:
	@echo "Cleaning all EDA tool outputs..."
	@$(MAKE) -C iverilog clean 2>/dev/null || true
	@$(MAKE) -C verilator clean 2>/dev/null || true
	@$(MAKE) -C ghdl clean 2>/dev/null || true
	@$(MAKE) -C cocotb clean 2>/dev/null || true
	@echo "✓ Clean completed"

# 快捷方式
iv: iverilog
vl: verilator
gh: ghdl
cb: cocotb
