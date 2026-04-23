# Scripts/config.mk - 工具链配置模板

#==============================================================================
# 工具路径 (可自定义)
#==============================================================================
# 开源工具 (默认)
IVERILOG        ?= iverilog
VVP             ?= vvp
VERILATOR       ?= verilator
YOSYS           ?= yosys
OPENROAD        ?= openroad
OPENSTA         ?= opensta
MAGIC           ?= magic
NETGEN          ?= netgen
KLAYOUT         ?= klayout

# 商业工具 (需配置)
VCS             ?= vcs
VERDI           ?= verdi
DC_SHELL        ?= dc_shell
GENUS           ?= genus
INNOVUS         ?= innovus
ICC2            ?= icc2
PRIMETIME       ?= pt_shell
TEMPUS          ?= tempus
CONFORMAL       ?= lec
FORMALITY       ?= formality
TESSENT         ?= tessent
MODUS           ?= modus
SPYGLASS        ?= spyglass
ASCENT          ?= ascent
CALIBRE         ?= calibre

#==============================================================================
# 工艺库配置
#==============================================================================
PROCESS_NODE    ?= {{PROCESS_NODE}}
PDK_ROOT        ?= /opt/pdk/$(PROCESS_NODE)
STD_CELL_LIB    ?= $(PDK_ROOT)/lib/stdcells.lib
IO_LIB          ?= $(PDK_ROOT)/lib/iocells.lib
LEF_FILE        ?= $(PDK_ROOT)/lef/stdcells.lef
TECH_LEF        ?= $(PDK_ROOT)/lef/tech.lef
GDS_FILE        ?= $(PDK_ROOT)/gds/stdcells.gds

#==============================================================================
# 设计约束
#==============================================================================
CLK_PERIOD      ?= {{CLK_PERIOD}}
CLK_PORT        ?= {{CLK_PORT}}
RESET_PORT      ?= {{RESET_PORT}}
INPUT_DELAY     ?= 2.0
OUTPUT_DELAY    ?= 2.0

#==============================================================================
# 覆盖率阈值
#==============================================================================
COVERAGE_LINE_THRESHOLD    ?= 90
COVERAGE_TOGGLE_THRESHOLD  ?= 85
COVERAGE_FSM_THRESHOLD     ?= 95
COVERAGE_BRANCH_THRESHOLD  ?= 90

#==============================================================================
# 并行度
#==============================================================================
NPROCS          ?= $(shell nproc 2>/dev/null || echo 4)
