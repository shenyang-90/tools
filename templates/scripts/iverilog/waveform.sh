#!/bin/bash
# GTKWave 波形查看脚本

GTKWAVE="{{GTKWAVE_PATH}}"

# 默认使用系统路径
if [ "$GTKWAVE" = "{{GTKWAVE_PATH}}" ]; then
    GTKWAVE="gtkwave"
fi

if [ ! -f "dump.vcd" ]; then
    echo "Error: dump.vcd not found. Run simulation first."
    exit 1
fi

echo "Opening waveform viewer..."
$GTKWAVE dump.vcd &
