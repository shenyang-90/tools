# GHDL VHDL 仿真脚本

GHDL 是一个开源的 VHDL 编译器和仿真器。

## 文件说明

- `compile.sh` - 分析/编译 VHDL 文件
- `elaborate.sh` - 详细设计
- `simulate.sh` - 运行仿真
- `waveform.sh` - 查看波形
- `Makefile` - 统一入口

## 使用方法

```bash
make compile    # 编译
make elaborate  # 详细设计
make simulate   # 仿真
make waveform   # 查看波形
make clean      # 清理
```

## 占位符

- `{{GHDL_PATH}}` - ghdl 可执行文件路径
- `{{GTKWAVE_PATH}}` - gtkwave 可执行文件路径
- `{{RTL_TOP}}` - RTL 顶层实体名
- `{{TB_TOP}}` - Testbench 顶层实体名
