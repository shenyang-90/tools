# Verilator 仿真脚本

Verilator 是一个快速的 Verilog/SystemVerilog 到 C++ 的转换器和仿真器。

## 文件说明

- `compile.sh` - 编译 Verilog 到 C++
- `build.sh` - 构建仿真可执行文件
- `simulate.sh` - 运行仿真
- `lint.sh` - 静态检查
- `Makefile` - 统一入口

## 使用方法

```bash
make lint       # 静态检查
make compile    # 编译
make build      # 构建
make simulate   # 仿真
make clean      # 清理
```

## 占位符

- `{{VERILATOR_PATH}}` - verilator 可执行文件路径
- `{{RTL_TOP}}` - RTL 顶层模块名
- `{{TB_TOP}}` - Testbench 顶层模块名
