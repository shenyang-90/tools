# Icarus Verilog 仿真脚本

Icarus Verilog 是一个开源的 Verilog 仿真工具。

## 文件说明

- `compile.sh` - 编译 Verilog 源文件
- `simulate.sh` - 运行仿真
- `waveform.sh` - 查看波形 (使用 GTKWave)
- `Makefile` - 统一入口

## 使用方法

```bash
make compile    # 编译
make simulate   # 仿真
make waveform   # 查看波形
make clean      # 清理
```

## 占位符

- `{{IVERILOG_PATH}}` - iverilog 可执行文件路径
- `{{VVP_PATH}}` - vvp 可执行文件路径
- `{{GTKWAVE_PATH}}` - gtkwave 可执行文件路径
- `{{RTL_TOP}}` - RTL 顶层模块名
- `{{TB_TOP}}` - Testbench 顶层模块名
