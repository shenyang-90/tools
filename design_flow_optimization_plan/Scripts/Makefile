#==============================================================================
# Scripts/Makefile - 统一EDA入口
#==============================================================================

#==============================================================================
# 项目配置
#==============================================================================
PROJECT_NAME    ?= aes_crypto
RTL_TOP         ?= aes_top
TB_TOP          ?= tb_aes_top
RTL_DIR         ?= ../Design/RTL
TB_DIR          ?= ../Verification
SIMULATOR       ?= iverilog  # iverilog/verilator/vcs/xrun
SYNTH_TOOL      ?= yosys     # yosys/dc/genus
PR_TOOL         ?= openroad  # openroad/innovus/icc2
LINT_TOOL       ?= spyglass  # spyglass/verilator/ascent

#==============================================================================
# 默认目标
#==============================================================================
.PHONY: help lint rtl sim synth dft pr sta signoff clean review

help:
	@echo "================================================================"
	@echo "$(PROJECT_NAME) - EDA Tool Flow"
	@echo "================================================================"
	@echo ""
	@echo "=== RTL Development ==="
	@echo "  make rtl               - Compile RTL (lint check)"
	@echo "  make sim TEST=tc_smoke - Run simulation"
	@echo "  make regression        - Run regression suite"
	@echo "  make coverage          - Collect coverage"
	@echo ""
	@echo "=== Verification ==="
	@echo "  make lint              - Run static checks"
	@echo "  make cdc               - Run CDC checks"
	@echo "  make sva               - Run assertion checks"
	@echo ""
	@echo "=== Implementation ==="
	@echo "  make synth             - Logic synthesis"
	@echo "  make dft               - DFT insertion"
	@echo "  make pr                - Place & Route"
	@echo "  make sta               - Static timing analysis"
	@echo ""
	@echo "=== Signoff ==="
	@echo "  make lec               - Logic equivalence check"
	@echo "  make drc               - Design rule check"
	@echo "  make lvs               - Layout vs schematic"
	@echo "  make signoff           - Full signoff flow"
	@echo ""
	@echo "=== Review ==="
	@echo "  make submit-review STAGE=IDR   - Submit for review"
	@echo "  make review-idr                - IDR stage review"
	@echo "  make review-edr                - EDR stage review"
	@echo "  make review-fdr                - FDR stage review"
	@echo ""
	@echo "=== Utilities ==="
	@echo "  make dashboard         - Update project dashboard"
	@echo "  make metrics           - Collect metrics"
	@echo "  make clean             - Clean temporary files"
	@echo ""
	@echo "Examples:"
	@echo "  make sim TEST=tc_nist SIMULATOR=vcs"
	@echo "  make synth SYNTH_TOOL=dc"
	@echo "  make submit-review STAGE=IDR TASK=TASK-AES-001"
	@echo "================================================================"

#==============================================================================
# RTL Development
#==============================================================================
rtl: lint
	@echo "[RTL] Compilation successful"

sim:
	$(MAKE) -f rtl/$(SIMULATOR).mk TEST=$(TEST)

regression:
	@./common/run_regression.py --suite full

coverage:
	@./common/collect_coverage.py --tool $(SIMULATOR)

#==============================================================================
# Verification
#==============================================================================
lint:
	$(MAKE) -f lint/lint.mk TOOL=$(LINT_TOOL)

cdc:
	$(MAKE) -f lint/cdc.mk

sva:
	$(MAKE) -f rtl/$(SIMULATOR).mk TARGET=sva

#==============================================================================
# Implementation
#==============================================================================
synth:
	$(MAKE) -f synth/$(SYNTH_TOOL).mk

dft:
	$(MAKE) -f dft/tessent.mk

pr:
	$(MAKE) -f pr/$(PR_TOOL).mk

sta:
	$(MAKE) -f sta/pt_shell.mk

#==============================================================================
# Signoff
#==============================================================================
lec:
	$(MAKE) -f lec/conformal.mk

drc:
	$(MAKE) -f signoff/calibre.mk TARGET=drc

lvs:
	$(MAKE) -f signoff/calibre.mk TARGET=lvs

signoff: sta lec drc lvs
	@echo "[Signoff] All checks completed"

#==============================================================================
# Review Bot Integration
#==============================================================================
submit-review:
	@echo "Running Review Bot for stage $(STAGE)..."
	@python3 common/review_bot.py --stage $(STAGE) --project .. --task $(TASK)
	@if [ $$? -eq 0 ]; then \
		echo "Review passed. Waiting for AI Yang/人工确认..."; \
	else \
		echo "Review failed. Please fix issues and retry."; \
		exit 1; \
	fi

review-pcd:
	$(MAKE) submit-review STAGE=PCD TASK=$(TASK)

review-pad:
	$(MAKE) submit-review STAGE=PAD TASK=$(TASK)

review-edr:
	$(MAKE) submit-review STAGE=EDR TASK=$(TASK)

review-idr:
	$(MAKE) submit-review STAGE=IDR TASK=$(TASK)

review-fdr:
	$(MAKE) submit-review STAGE=FDR TASK=$(TASK)

# 预提交检查 (Git hook调用)
pre-commit-check:
	@echo "Running pre-commit checks..."
	@python3 common/review_bot.py --stage IDR --checks "LintCheck,FilelistCheck" --dry-run

#==============================================================================
# Utilities
#==============================================================================
dashboard:
	@python3 common/update_dashboard.py

metrics:
	@python3 common/collect_metrics.py

clean:
	@echo "Cleaning temporary files..."
	@rm -rf ../Temp/VCS/*
	@rm -rf ../Temp/Verilator/*
	@rm -rf ../Temp/Spyglass/*
	@rm -rf ../Temp/DesignCompiler/*
	@echo "Clean complete"

#==============================================================================
# Project Setup
#==============================================================================
init:
	@echo "Initializing project structure..."
	@mkdir -p ../ProjectMgmt/{Planning,Tasks,Reviews,Bugs,MeetingMinutes,Milestones}
	@mkdir -p ../Docs/{Arch,Design,Verification,FuSa,DFT,Physical}
	@mkdir -p ../Design/{RTL/{soc,ip},Netlist/{synth,dft,pr},GDS}
	@mkdir -p ../Verification/{Env,Testcases/{directed,random,vectors},Regression,Coverage}
	@mkdir -p ../Temp/{VCS,Verilator,Spyglass,DesignCompiler}
	@echo "Project structure initialized"
