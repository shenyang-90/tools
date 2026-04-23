#!/bin/bash
# Verilator 仿真脚本

set -e

RTL_TOP="{{RTL_TOP}}"

echo "========================================"
echo "Verilator Simulation"
echo "========================================"

# 运行仿真
./obj_dir/V$RTL_TOP

echo "✓ Simulation completed"
echo "  Waveform: trace.vcd"
