#!/bin/bash
# GHDL 编译脚本

set -e

GHDL="{{GHDL_PATH}}"
RTL_DIR="../../DesignData/RTL"
TB_DIR="../../Verification/Env"
WORK_DIR="work"

# 默认使用系统路径
if [ "$GHDL" = "{{GHDL_PATH}}" ]; then
    GHDL="ghdl"
fi

echo "========================================"
echo "GHDL Compilation"
echo "========================================"

# 创建工作库
mkdir -p $WORK_DIR
$GHDL --workdir=$WORK_DIR --remove

# 分析 RTL 文件
for file in $RTL_DIR/*.vhd; do
    if [ -f "$file" ]; then
        echo "Analyzing: $file"
        $GHDL --workdir=$WORK_DIR -a "$file"
    fi
done

# 分析 Testbench
$GHDL --workdir=$WORK_DIR -a $TB_DIR/{{TB_TOP}}.vhd

echo "✓ Analysis successful"
