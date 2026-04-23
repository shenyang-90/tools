# 项目文件命名规范指南

> 基于 workflow/SOC_DESIGN_WORKFLOW.md 定义
> 适用于车规级SoC设计项目全生命周期

---

## 命名规范总览

```
[类别]_[标识]_[描述]_[版本]_[日期].扩展名
```

---

## 一、Review会议记录

### 命名格式
```
[阶段]_Review_YYYYMMDD.md
```

### 示例
```
PCD_Review_20260327.md
PAD_Review_20260615.md
EDR_Review_20260901.md
IDR_Review_20261220.md
FDR_Review_20270315.md
PostSilicon_Review_20270601.md
```

### 模块级IDR评审
```
[ModuleName]_IDR_Review_YYYYMMDD.md

例如:
- CPU_IDR_Review_20260327.md
- DMA_IDR_Review_20260327.md
- USB_IDR_Review_20260415.md
```

### 存储位置
```
pm/reviews/[阶段]/
```

---

## 二、Checklist文件

### 命名格式
```
[模块/类型]_[阶段]_Checklist_v[版本]_[YYYYMMDD].md
```

### 示例
```
SoC_ADR_Checklist_v1.0_20260615.md
CPU_EDR_Checklist_v1.0_20260901.md
DMA_IDR_Checklist_v1.0_20261220.md
SoC_FDR_Checklist_v1.0_20270315.md
```

### 存储位置
```
pm/reviews/[阶段]/
```

---

## 三、Bug记录

### 命名格式
```
BUG_[ID]_[Brief_Description].md
```

### 示例
```
BUG_001_Clock_Domain_Crossing.md
BUG_002_Memory_Controller_Timeout.md
BUG_003_UART_BaudRate_Error.md
```

### 描述规范
- 使用英文或拼音
- 简洁明了（3-5个词）
- 使用下划线连接
- 首字母大写

### 存储位置
```
pm/bugs/P1_Critical/
pm/bugs/P2_Major/
pm/bugs/P3_Minor/
pm/bugs/P4_Trivial/
```

---

## 四、设计文档

### 命名格式
```
[ModuleName]_[Type]_Spec_v[Version]_[YYYYMMDD].md
```

### 类型说明
| 类型 | 后缀 | 说明 |
|------|------|------|
| 设计规格 | Design_Spec | 模块设计文档 |
| 验证计划 | Verification_Plan | 验证策略文档 |
| 接口规格 | Interface_Spec | 接口定义文档 |
| 架构规格 | Architecture_Spec | 系统架构文档 |
| 安全概念 | Safety_Concept | 功能安全文档 |
| DFT规格 | DFT_Spec | 可测性设计文档 |

### 示例
```
CPU_Subsystem_Design_Spec_v1.0_20260901.md
DMA_Controller_Verification_Plan_v1.0_20260901.md
UART_Interface_Spec_v1.0_20260901.md
SoC_Architecture_Spec_v1.0_20260615.md
Safety_Concept_v1.0_20260615.md
DFT_Spec_v1.0_20260901.md
```

### 存储位置
```
docs/Module_Name/
docs/Arch/
docs/FuSa/
docs/DFT/
```

---

## 五、RTL代码

### 命名格式
```
[module_name].v          # Verilog
[module_name].sv         # SystemVerilog
[module_name]_pkg.sv     # SystemVerilog Package
[module_name]_if.sv      # SystemVerilog Interface
```

### 命名规范
- 小写字母
- 下划线连接
- 模块名与文件名一致
- 后缀表示类型

### 示例
```
cpu_top.v
dma_controller.sv
ahb_arbiter.v
uart_tx_rx.sv
```

### 存储位置
```
design/
├── soc/           # SoC level module, Syste/Safety/Bus/IOMUX/ClockReset/Top
├── ip/            # 独立功能模块，UART/I2C
├── soc_top.f      # Filelist
```

---

## 六、验证环境

### 命名格式
```
[tb/uvm/env]_[module_name]_[component].sv
```

### 组件类型
| 后缀 | 说明 |
|------|------|
| _tb | Testbench顶层 |
| _env | UVM Environment |
| _agent | UVM Agent |
| _driver | UVM Driver |
| _monitor | UVM Monitor |
| _sequencer | UVM Sequencer |
| _seq | UVM Sequence |
| _test | UVM Test |
| _scoreboard | Scoreboard |
| _ref | Reference Model |

### 示例
```
tb_cpu_top.sv
uvm_cpu_env.sv
uvm_cpu_agent.sv
uvm_cpu_driver.sv
uvm_cpu_monitor.sv
cpu_base_seq.sv
cpu_smoke_test.sv
cpu_scoreboard.sv
cpu_ref_model.sv
```

### 存储位置
```
verification
├── st           # ST
├── ut           # UT
```

---

## 七、测试用例

### 命名格式
```
[test_type]_[module]_[scenario]_[number].sv
```

### 测试类型
| 前缀 | 说明 |
|------|------|
| smoke_ | 冒烟测试 |
| sanity_ | 健全性测试 |
| reg_ | 寄存器测试 |
| func_ | 功能测试 |
| perf_ | 性能测试 |
| stress_ | 压力测试 |
| err_ | 错误注入测试 |

### 示例
```
smoke_cpu_basic_001.sv
reg_dma_registers_001.sv
func_uart_tx_rx_001.sv
perf_ddr_bandwidth_001.sv
stress_interrupt_handling_001.sv
err_memory_parity_001.sv
```

### 存储位置
```
verification/st/tests/
├── directed/      # 定向测试
├── random/        # 随机测试
└── vectors/       # 测试向量
```

---

## 八、EDA脚本

### 命名格式
```
run_[flow]_[target]_[version].tcl/py/sh
[tool]_[action].mk
```

### 流程类型
| 前缀 | 说明 |
|------|------|
| run_synth_ | 逻辑综合 |
| run_sta_ | 时序分析 |
| run_pr_ | 物理实现 |
| run_dft_ | DFT流程 |
| run_lec_ | 形式验证 |
| run_pv_ | 物理验证 |

### 示例
```
run_synth_cpu_v1.0.tcl
run_sta_setup_v1.0.tcl
run_pr_innovus_v1.0.tcl
run_dft_insertion_v1.0.tcl
run_lec_formality_v1.0.tcl
run_pv_calibre_v1.0.tcl

# Makefile
spyglass.mk
vcs.mk
verilator.mk
```

### 存储位置
```
Database/Scripts/
├── rtl/           # RTL仿真脚本
├── lint/          # Lint检查脚本
├── synth/         # 逻辑综合脚本
├── dft/           # DFT脚本
├── pr/            # 物理设计脚本
├── sta/           # 时序分析脚本
├── lec/           # 形式验证脚本
└── signoff/       # Signoff脚本
```

---

## 九、报告文件

### 命名格式
```
[Type]_Report_[Module]_[Date].[ext]
```

### 报告类型
| 类型 | 示例 |
|------|------|
| 覆盖率报告 | Coverage_Report_CPU_20260327.md |
| 时序报告 | Timing_Report_CPU_20260327.pdf |
| 功耗报告 | Power_Report_CPU_20260327.pdf |
| Lint报告 | Lint_Report_CPU_20260327.rpt |
| CDC报告 | CDC_Report_CPU_20260327.rpt |
| 物理验证报告 | PV_Report_CPU_20260327.pdf |
| ATPG报告 | ATPG_Report_CPU_20260327.pdf |

### 存储位置
```
ProjectMgmt/Milestones/
Database/Verification/Coverage/
Database/Docs/Physical/
```

---

## 十、约束文件

### 命名格式
```
[project]_[type].[sdc|upf|cpf]
```

### 示例
```
soc_top.sdc
soc_power.upf
soc_lowpower.cpf
```

### 存储位置
```
Database/DesignData/SDC/
Database/DesignData/UPF/
```

---

## 十一、任务文件

### 命名格式
```
TASK_[阶段]_[编号]_[描述].md
```

### 示例
```
TASK_IDR_001_RTL_Implementation.md
TASK_EDR_002_Design_Spec.md
TASK_FDR_003_STA_Signoff.md
```

### 存储位置
```
ProjectMgmt/Tasks/[Agent]/
```

---

## 十二、网表文件

### 命名格式
```
[design]_[stage]_[version].v
```

### 阶段标识
| 后缀 | 说明 |
|------|------|
| _rtl | RTL源码 |
| _syn | 综合后网表 |
| _dft | DFT插入后网表 |
| _pr | PR后网表 |

### 示例
```
cpu_top_rtl_v1.0.v
cpu_top_syn_v1.0.v
cpu_top_dft_v1.0.v
cpu_top_pr_v1.0.v
```

### 存储位置
```
Database/DesignData/Netlist/
├── synth/
├── dft/
└── pr/
```

---

## 十三、版本号规范

### 格式
```
v[主版本].[次版本]

例如:
v0.5   # 初步版本
v0.7   # 优化版本
v0.9   # 冻结前版本
v1.0   # 正式发布版本
v1.1   # 小修改版本
v2.0   # 重大更新版本
```

### 版本含义
| 版本 | 阶段 | 说明 |
|------|------|------|
| v0.1-v0.4 | 草稿 | 初步编写 |
| v0.5 | 初稿 | 可Review版本 |
| v0.6-v0.8 | 修改 | 根据Review修改 |
| v0.9 | 预冻结 | 接近冻结 |
| v1.0 | 冻结 | 正式发布 |
| v1.x+ | 维护 | ECO/更新 |
| v2.0 | 重构 | 重大变更 |

---

## 十四、快速参考表

| 文件类型 | 命名示例 | 存储位置 |
|---------|---------|---------|
| Review记录 | IDR_Review_Meeting_Minutes_20261220.md | ProjectMgmt/Reviews/IDR/ |
| Checklist | IDR_Checklist_CPU_v1.0_20261220.md | ProjectMgmt/Reviews/IDR/ |
| Bug记录 | BUG_001_Clock_Domain_Crossing.md | ProjectMgmt/Bugs/P2_Major/ |
| 设计文档 | CPU_Design_Spec_v1.0_20260901.md | Database/Docs/Design/ |
| RTL代码 | cpu_top.v | Database/DesignData/RTL/ |
| 测试用例 | smoke_cpu_basic_001.sv | Database/Verification/Testcases/ |
| EDA脚本 | run_synth_v1.0.tcl | Database/Scripts/synth/ |
| 报告 | Coverage_Report_CPU_20260327.md | ProjectMgmt/Milestones/ |
| 约束文件 | soc_top.sdc | Database/DesignData/SDC/ |
| 任务文件 | TASK_IDR_001_RTL_Implementation.md | ProjectMgmt/Tasks/ |

---

## 十五、禁止事项

❌ **不要使用的命名方式**:
- 使用空格: `My Design Spec.md`
- 使用特殊字符: `design@spec#1.md`
- 版本号不明确: `design_spec_old.md`, `design_spec_new.md`
- 混合大小写混乱: `Cpu_Top.V`, `cpu_Top.SV`
- 无意义数字: `file1.md`, `file2.md`

✅ **推荐的命名方式**:
- 使用下划线连接: `CPU_Design_Spec_v1.0.md`
- 明确的版本号: `v1.0`, `v1.1`
- 一致的格式: 全部小写或首字母大写
- 有意义的描述: `Clock_Domain_Crossing` 而非 `CDC`

---

## 十六、自动化检查

### 命名检查脚本
```bash
#!/bin/bash
# naming_check.sh - 检查文件名规范

# 检查空格
find . -name "* *" -type f

# 检查特殊字符
find . -name "*[@#\$%]*" -type f

# 检查大小写混乱
find . -name "*.V" -o -name "*.SV"
```

---

*此规范基于 workflow/SOC_DESIGN_WORKFLOW.md 定义*
*版本: v1.0*
