#!/bin/bash
# GHDL 详细设计脚本

set -e

GHDL="{{GHDL_PATH}}"
TB_TOP="{{TB_TOP}}"
WORK_DIR="work"

# 默认使用系统路径
if [ "$GHDL" = "{{GHDL_PATH}}" ]; then
    GHDL="ghdl"
fi

echo "========================================"
echo "GHDL Elaboration"
echo "========================================"

# 详细设计
$GHDL --workdir=$WORK_DIR -e $TB_TOP

echo "✓ Elaboration successful"
