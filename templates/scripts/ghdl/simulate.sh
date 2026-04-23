#!/bin/bash
# GHDL 仿真脚本

set -e

GHDL="{{GHDL_PATH}}"
TB_TOP="{{TB_TOP}}"
WORK_DIR="work"

# 默认使用系统路径
if [ "$GHDL" = "{{GHDL_PATH}}" ]; then
    GHDL="ghdl"
fi

echo "========================================"
echo "GHDL Simulation"
echo "========================================"

# 运行仿真
$GHDL --workdir=$WORK_DIR -r $TB_TOP --wave=wave.ghw --vcd=dump.vcd

echo "✓ Simulation completed"
echo "  Waveform: wave.ghw / dump.vcd"
