# cocotb 测试框架脚本

cocotb 是一个基于 Python 的 coroutine 协程 Testbench 环境。

## 文件说明

- `test_{{RTL_TOP}}.py` - Python 测试文件
- `Makefile` - cocotb 入口
- `run.sh` - 运行脚本

## 使用方法

```bash
make            # 运行所有测试
make SIM=iverilog  # 使用 Icarus Verilog
make SIM=verilator # 使用 Verilator
make SIM=ghdl      # 使用 GHDL
make clean      # 清理
```

## 占位符

- `{{COCOTB_PATH}}` - cocotb 安装路径
- `{{RTL_TOP}}` - RTL 顶层模块名
- `{{SIM}}` - 默认仿真器 (iverilog/verilator/ghdl)
