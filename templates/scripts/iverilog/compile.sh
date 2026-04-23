#!/bin/bash
# Icarus Verilog 编译脚本

set -e

IVERILOG="{{IVERILOG_PATH}}"
RTL_DIR="../../DesignData/RTL"
TB_DIR="../../Verification/Env"
OUTPUT="sim.out"

# 默认使用系统路径
if [ "$IVERILOG" = "{{IVERILOG_PATH}}" ]; then
    IVERILOG="iverilog"
fi

echo "========================================"
echo "Icarus Verilog Compilation"
echo "========================================"

# 编译命令
$IVERILOG -g2012 -o $OUTPUT \
    -y $RTL_DIR \
    -I $RTL_DIR \
    $TB_DIR/{{TB_TOP}}.sv \
    $RTL_DIR/{{RTL_TOP}}.v

echo "✓ Compilation successful: $OUTPUT"
