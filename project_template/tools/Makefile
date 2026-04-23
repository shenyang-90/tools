# Database/Scripts/Makefile - 统一EDA入口模板

#==============================================================================
# 项目配置 (由install脚本自动填充)
#==============================================================================
PROJECT_NAME    ?= {{PROJECT_NAME}}
PROJECT_ID      ?= {{PROJECT_ID}}
RTL_TOP         ?= {{RTL_TOP}}
TB_TOP          ?= {{TB_TOP}}
PROCESS_NODE    ?= {{PROCESS_NODE}}
ASIL_LEVEL      ?= {{ASIL_LEVEL}}

# 目录配置
RTL_DIR         ?= ../DesignData/RTL
TB_DIR          ?= ../Verification
ENV_DIR         ?= ../Verification/Env
TC_DIR          ?= ../Verification/Testcases
OUT_DIR         ?= ../../Temp

# 工具选择
SIMULATOR       ?= iverilog    # iverilog/verilator/vcs/xrun/ghdl
LINT_TOOL       ?= verilator   # verilator/spyglass/ascent
SYNTH_TOOL      ?= yosys       # yosys/dc_shell/genus
PR_TOOL         ?= openroad    # openroad/innovus/icc2
STA_TOOL        ?= opensta     # opensta/pt_shell/tempus
DFT_TOOL        ?= dftadvisor  # dftadvisor/tessent/modus
PV_TOOL         ?= klayout     # klayout/calibre/pegasus

# 包含工具链配置
include config.mk

#==============================================================================
# 默认目标
#==============================================================================
.PHONY: help info lint rtl sim synth dft pr sta signoff clean dashboard

.DEFAULT_GOAL := help

help:
	@echo "================================================================"
	@echo "$(PROJECT_NAME) - EDA Tool Flow"
	@echo "Project ID: $(PROJECT_ID) | Process: $(PROCESS_NODE) | ASIL: $(ASIL_LEVEL)"
	@echo "================================================================"
	@echo ""
	@echo "=== RTL Development ==="
	@echo "  make rtl               - Compile RTL (with lint check)"
	@echo "  make sim TEST=<name>   - Run simulation (default: tc_smoke)"
	@echo "  make regression        - Run full regression suite"
	@echo "  make coverage          - Collect coverage data"
	@echo "  make view              - Open waveform viewer"
	@echo ""
	@echo "=== Verification ==="
	@echo "  make lint              - Run static lint checks"
	@echo "  make cdc               - Run CDC checks"
	@echo "  make sva               - Run assertion checks"
	@echo "  make formal            - Run formal verification"
	@echo ""
	@echo "=== Implementation ==="
	@echo "  make synth             - Logic synthesis"
	@echo "  make synth_opt         - Synthesis with optimization"
	@echo "  make dft               - DFT insertion"
	@echo "  make pr                - Place \u0026 Route (full flow)"
	@echo "  make sta               - Static timing analysis"
	@echo ""
	@echo "=== Signoff ==="
	@echo "  make lec               - Logic equivalence check"
	@echo "  make drc               - Design rule check"
	@echo "  make lvs               - Layout vs schematic"
	@echo "  make signoff           - Full signoff flow"
	@echo ""
	@echo "=== Utilities ==="
	@echo "  make info              - Show project configuration"
	@echo "  make dashboard         - Update project dashboard"
	@echo "  make metrics           - Collect and display metrics"
	@echo "  make docs              - Generate documentation"
	@echo "  make clean             - Clean all temporary files"
	@echo "  make clean_all         - Clean everything (including outputs)"
	@echo ""
	@echo "Variables:"
	@echo "  SIMULATOR=<tool>       - Select simulator (iverilog/verilator/vcs)"
	@echo "  SYNTH_TOOL=<tool>      - Select synthesis tool (yosys/dc_shell)"
	@echo "  TEST=<name>            - Select test case"
	@echo "  GUI=1                  - Enable GUI mode"
	@echo ""
	@echo "Examples:"
	@echo "  make sim TEST=tc_nist SIMULATOR=vcs"
	@echo "  make synth SYNTH_TOOL=dc_shell"
	@echo "  make pr PR_TOOL=innovus"
	@echo "================================================================"

#==============================================================================
# 信息显示
#==============================================================================
info:
	@echo "================================================================"
	@echo "Project Information"
	@echo "================================================================"
	@echo "Name:        $(PROJECT_NAME)"
	@echo "ID:          $(PROJECT_ID)"
	@echo "RTL Top:     $(RTL_TOP)"
	@echo "TB Top:      $(TB_TOP)"
	@echo "Process:     $(PROCESS_NODE)"
	@echo "ASIL Level:  $(ASIL_LEVEL)"
	@echo ""
	@echo "Tools:"
	@echo "  Simulator: $(SIMULATOR)"
	@echo "  Lint:      $(LINT_TOOL)"
	@echo "  Synthesis: $(SYNTH_TOOL)"
	@echo "  PR:        $(PR_TOOL)"
	@echo "  STA:       $(STA_TOOL)"
	@echo "================================================================"

#==============================================================================
# RTL Development
#==============================================================================
rtl: lint
	@echo "[RTL] Compilation successful for $(RTL_TOP)"

# 仿真目标 - 动态分派到具体工具
sim:
	@if [ -f "rtl/$(SIMULATOR).mk" ]; then \
		$(MAKE) -f rtl/$(SIMULATOR).mk TEST=$(TEST) SIMULATOR=$(SIMULATOR); \
	else \
		echo "Error: Simulator '$(SIMULATOR)' not supported"; \
		exit 1; \
	fi

# 回归测试
regression:
	@./common/run_regression.py \
		--simulator $(SIMULATOR) \
		--suite full \
		--jobs $(NPROCS)

# 覆盖率收集
coverage:
	@./common/collect_coverage.py \
		--tool $(SIMULATOR) \
		--output $(OUT_DIR)/Coverage

# 波形查看
view:
	@if [ -f "$(OUT_DIR)/$(SIMULATOR)/$(TEST).vcd" ]; then \
		gtkwave $(OUT_DIR)/$(SIMULATOR)/$(TEST).vcd & \
	elif [ -f "$(OUT_DIR)/$(SIMULATOR)/$(TEST).fst" ]; then \
		gtkwave $(OUT_DIR)/$(SIMULATOR)/$(TEST).fst & \
	else \
		echo "No waveform found for $(TEST)"; \
	fi

#==============================================================================
# Verification
#==============================================================================
lint:
	@echo "[Lint] Running $(LINT_TOOL) checks..."
	@if [ -f "lint/$(LINT_TOOL).mk" ]; then \
		$(MAKE) -f lint/$(LINT_TOOL).mk RTL_DIR=$(RTL_DIR) TOP=$(RTL_TOP); \
	else \
		echo "Warning: Lint tool '$(LINT_TOOL)' not configured"; \
	fi

cdc:
	@echo "[CDC] Running CDC checks..."
	@if [ -f "lint/cdc.mk" ]; then \
		$(MAKE) -f lint/cdc.mk; \
	else \
		echo "Warning: CDC checks not configured"; \
	fi

sva:
	@echo "[SVA] Running assertion checks..."
	@if [ -f "rtl/$(SIMULATOR).mk" ]; then \
		$(MAKE) -f rtl/$(SIMULATOR).mk TARGET=sva; \
	fi

formal:
	@echo "[Formal] Running formal verification..."
	@if [ -f "formal/formal.mk" ]; then \
		$(MAKE) -f formal/formal.mk; \
	else \
		echo "Warning: Formal verification not configured"; \
	fi

#==============================================================================
# Implementation
#==============================================================================
synth:
	@echo "[Synthesis] Running $(SYNTH_TOOL) synthesis..."
	@if [ -f "synth/$(SYNTH_TOOL).mk" ]; then \
		$(MAKE) -f synth/$(SYNTH_TOOL).mk TOP=$(RTL_TOP); \
	else \
		echo "Error: Synthesis tool '$(SYNTH_TOOL)' not supported"; \
		exit 1; \
	fi

synth_opt: synth
	@echo "[Synthesis] Running optimization..."
	@if [ -f "synth/$(SYNTH_TOOL).mk" ]; then \
		$(MAKE) -f synth/$(SYNTH_TOOL).mk opt; \
	fi

dft:
	@echo "[DFT] Running $(DFT_TOOL) DFT insertion..."
	@if [ -f "dft/$(DFT_TOOL).mk" ]; then \
		$(MAKE) -f dft/$(DFT_TOOL).mk; \
	else \
		echo "Warning: DFT tool '$(DFT_TOOL)' not configured"; \
	fi

# 物理设计分步执行
floorplan:
	@echo "[PR] Floorplan..."
	$(MAKE) -f pr/$(PR_TOOL).mk floorplan

place: floorplan
	@echo "[PR] Placement..."
	$(MAKE) -f pr/$(PR_TOOL).mk place

cts: place
	@echo "[PR] Clock Tree Synthesis..."
	$(MAKE) -f pr/$(PR_TOOL).mk cts

route: cts
	@echo "[PR] Routing..."
	$(MAKE) -f pr/$(PR_TOOL).mk route

final: route
	@echo "[PR] Final..."
	$(MAKE) -f pr/$(PR_TOOL).mk final

# 完整物理设计流程
pr: final
	@echo "[PR] Physical design complete"

sta:
	@echo "[STA] Running $(STA_TOOL) timing analysis..."
	@if [ -f "sta/$(STA_TOOL).mk" ]; then \
		$(MAKE) -f sta/$(STA_TOOL).mk; \
	else \
		echo "Warning: STA tool '$(STA_TOOL)' not configured"; \
	fi

#==============================================================================
# Signoff
#==============================================================================
lec:
	@echo "[LEC] Running logic equivalence check..."
	@if [ -f "lec/lec.mk" ]; then \
		$(MAKE) -f lec/lec.mk; \
	else \
		echo "Warning: LEC not configured"; \
	fi

drc:
	@echo "[PV] Running DRC..."
	@if [ -f "signoff/$(PV_TOOL).mk" ]; then \
		$(MAKE) -f signoff/$(PV_TOOL).mk TARGET=drc; \
	else \
		echo "Warning: PV tool '$(PV_TOOL)' not configured"; \
	fi

lvs:
	@echo "[PV] Running LVS..."
	@if [ -f "signoff/$(PV_TOOL).mk" ]; then \
		$(MAKE) -f signoff/$(PV_TOOL).mk TARGET=lvs; \
	else \
		echo "Warning: PV tool '$(PV_TOOL)' not configured"; \
	fi

signoff: lec sta drc lvs
	@echo "[Signoff] ================================================"
	@echo "[Signoff] All signoff checks completed"
	@echo "[Signoff] Review reports in $(OUT_DIR)/Signoff/"
	@echo "[Signoff] ================================================"

#==============================================================================
# Utilities
#==============================================================================
dashboard:
	@echo "[Dashboard] Updating project dashboard..."
	@./common/update_dashboard.py --project $(PROJECT_ID)

metrics:
	@echo "[Metrics] Collecting project metrics..."
	@./common/metrics_collect.sh --output $(OUT_DIR)/Metrics

docs:
	@echo "[Docs] Generating documentation..."
	@./common/generate_docs.py --output ../../Database/Docs/Generated

clean:
	@echo "[Clean] Cleaning temporary files..."
	@rm -rf $(OUT_DIR)/VCS/*
	@rm -rf $(OUT_DIR)/Verilator/*
	@rm -rf $(OUT_DIR)/Coverage/temp/*
	@echo "[Clean] Temporary files removed"

clean_all: clean
	@echo "[Clean] Cleaning all generated files..."
	@rm -rf $(OUT_DIR)/*
	@rm -rf ../DesignData/Netlist/*
	@echo "[Clean] All generated files removed"

#==============================================================================
# Debug targets
#==============================================================================
debug-rtl:
	@echo "[Debug] RTL files:"
	@find $(RTL_DIR) -name "*.v" -o -name "*.sv" | head -20

debug-env:
	@echo "[Debug] Environment variables:"
	@echo "WORKSPACE: $(WORKSPACE)"
	@echo "RTL_DIR: $(RTL_DIR)"
	@echo "OUT_DIR: $(OUT_DIR)"

#==============================================================================
# CI/CD targets
#==============================================================================
ci-lint: lint
	@./common/check_lint_results.py --fail-on-error

ci-sim: regression
	@./common/check_regression_results.py --fail-on-failures

ci-coverage: coverage
	@./common/check_coverage_thresholds.py \
		--line $(COVERAGE_LINE_THRESHOLD) \
		--toggle $(COVERAGE_TOGGLE_THRESHOLD)

ci-full: ci-lint ci-sim ci-coverage
	@echo "[CI] Full CI flow passed"
