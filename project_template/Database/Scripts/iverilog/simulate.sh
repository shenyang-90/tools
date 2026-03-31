#!/bin/bash
# Icarus Verilog 仿真脚本

set -e

VVP="{{VVP_PATH}}"

# 默认使用系统路径
if [ "$VVP" = "{{VVP_PATH}}" ]; then
    VVP="vvp"
fi

echo "========================================"
echo "Icarus Verilog Simulation"
echo "========================================"

# 运行仿真
$VVP -n sim.out -lxt2

echo "✓ Simulation completed"
echo "  Waveform: dump.vcd"
