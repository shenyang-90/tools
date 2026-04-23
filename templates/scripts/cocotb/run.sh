#!/bin/bash
# cocotb 运行脚本

set -e

echo "========================================"
echo "cocotb Test Framework"
echo "========================================"

# 默认使用 iverilog
SIMULATOR="${1:-iverilog}"

echo "Using simulator: $SIMULATOR"
echo ""

# 运行测试
make SIM=$SIMULATOR

echo ""
echo "✓ Tests completed"
