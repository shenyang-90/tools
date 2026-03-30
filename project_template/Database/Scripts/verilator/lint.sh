#!/bin/bash
# Verilator 静态检查脚本

set -e

VERILATOR="{{VERILATOR_PATH}}"
RTL_DIR="../../DesignData/RTL"
RTL_TOP="{{RTL_TOP}}"

# 默认使用系统路径
if [ "$VERILATOR" = "{{VERILATOR_PATH}}" ]; then
    VERILATOR="verilator"
fi

echo "========================================"
echo "Verilator Lint Check"
echo "========================================"

# Lint 检查
$VERILATOR --lint-only -Wall \
    -y $RTL_DIR \
    $RTL_DIR/$RTL_TOP.v

echo "✓ Lint check passed"
