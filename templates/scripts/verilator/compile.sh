#!/bin/bash
# Verilator 编译脚本

set -e

VERILATOR="{{VERILATOR_PATH}}"
RTL_DIR="../../DesignData/RTL"
TB_DIR="../../Verification/Env"
RTL_TOP="{{RTL_TOP}}"
TB_TOP="{{TB_TOP}}"

# 默认使用系统路径
if [ "$VERILATOR" = "{{VERILATOR_PATH}}" ]; then
    VERILATOR="verilator"
fi

echo "========================================"
echo "Verilator Compilation"
echo "========================================"

# 编译到 C++
$VERILATOR --cc --exe --build --trace \
    -y $RTL_DIR \
    -I $RTL_DIR \
    -Mdir obj_dir \
    --top-module $RTL_TOP \
    $RTL_DIR/$RTL_TOP.v \
    $TB_DIR/$TB_TOP.cpp

echo "✓ Compilation successful"
