#!/bin/bash
# GTKWave 波形查看脚本

GTKWAVE="{{GTKWAVE_PATH}}"

# 默认使用系统路径
if [ "$GTKWAVE" = "{{GTKWAVE_PATH}}" ]; then
    GTKWAVE="gtkwave"
fi

if [ -f "wave.ghw" ]; then
    echo "Opening wave.ghw..."
    $GTKWAVE wave.ghw &
elif [ -f "dump.vcd" ]; then
    echo "Opening dump.vcd..."
    $GTKWAVE dump.vcd &
else
    echo "Error: No waveform file found. Run simulation first."
    exit 1
fi
