# 车规级芯片设计全流程优化方案

## 版本信息
- **版本**: v1.0
- **日期**: 2026-04-02
- **作者**: AI Yang
- **适用范围**: SoC / IP 数字设计项目

---

## 目录

1. [概述](#概述)
2. [总体架构](#总体架构)
3. [目录结构定义](#目录结构定义)
4. [EDA工具流程脚本](#eda工具流程脚本)
5. [多Agent协作机制](#多agent协作机制)
6. [项目Dashboard](#项目dashboard)
7. [Review节点体系](#review节点体系)
8. [本地Agent部署](#本地agent部署)
9. [实施路线图](#实施路线图)

---

## 概述

### 当前痛点分析

| 痛点 | 影响 | 优化目标 |
|------|------|----------|
| EDA工具脚本分散 | 重复劳动，版本不一致 | 统一Makefile入口，工具链可插拔 |
| Agent协作无标准 | 任务交接混乱 | 标准化任务JSON协议 |
| Review节点手动 | 容易遗漏检查项 | 自动化Checklist验证 |
| 状态追踪困难 | 项目进度不透明 | 实时Dashboard + Git集成 |
| 本地EDA环境缺失 | Coding Yang无法直接运行工具 | 容器化本地Agent部署 |

### 参考开源项目

| 项目 | 特点 | 借鉴点 |
|------|------|--------|
| [OpenLANE](https://github.com/The-OpenROAD-Project/OpenLane) | RTL-to-GDS全自动流程 | 统一配置、阶段化执行 |
| [OpenROAD](https://github.com/The-OpenROAD-Project/OpenROAD) | 开源物理设计 | Floorplan/CTS/Routing脚本结构 |
| [siliconcompiler](https://github.com/siliconcompiler/siliconcompiler) | Python-based设计流程 | 任务依赖图、并行执行 |
| [chipyard](https://github.com/ucb-bar/chipyard) | SoC生成框架 | 生成器模式、配置驱动 |

---

## 总体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Project Dashboard                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │  Phase   │ │  Tasks   │ │  Agents  │ │  Metrics │ │  Alerts  │      │
│  │  Status  │ │  Queue   │ │  Status  │ │  Trends  │ │  & Logs  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
        ┌─────────────────┐ ┌──────────────┐ ┌─────────────┐
        │   AI Yang       │ │  PM Agent    │ │  Review Bot │
        │ (Quality Gate)  │ │(Orchestrator)│ │(Auto Check) │
        └────────┬────────┘ └──────┬───────┘ └──────┬──────┘
                 │                 │                │
                 └─────────────────┼────────────────┘
                                   ▼
        ┌─────────────────────────────────────────────────────────┐
        │              Task Queue & State Machine                 │
        │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
        │  │ PENDING │→│ ASSIGNED│→│ RUNNING │→│REVIEWING│    │
        │  └─────────┘  └─────────┘  └─────────┘  └─────────┘    │
        │                                          ↓           │
        │                                    ┌─────────┐        │
        │                                    │COMPLETED│        │
        │                                    └─────────┘        │
        └─────────────────────────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Coding Agent   │    │  Design Agent   │    │  Verify Agent   │
│  (本地部署)      │    │  (云端/本地)     │    │  (云端/本地)     │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ RTL Coding  │ │    │ │ Doc Writing │ │    │ │ Test Writing│ │
│ │ Simulation  │ │    │ │ Review      │ │    │ │ Coverage    │ │
│ │ Lint/CDC    │ │    │ │ Analysis    │ │    │ │ Regression  │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 目录结构定义

### 三级目录结构（保留现有）

```
project/
├── ProjectMgmt/              # 项目管理 (所有与项目管理相关的文档)
│   ├── Planning/             # 项目计划
│   │   ├── Master_Schedule.md
│   │   ├── Milestone_Plan.md
│   │   ├── Resource_Plan.md
│   │   └── Task_Assignment.md
│   │
│   ├── Tasks/                # Agent任务清单（按项目节点分类）
│   │   ├── PCD/              # Project Concept Definition
│   │   │   ├── TASK_PCD_001_MRD.md
│   │   │   ├── TASK_PCD_002_Feasibility.md
│   │   │   └── CHECKLIST_PCD.md
│   │   ├── PAD/              # Product Architecture Definition
│   │   │   ├── TASK_PAD_001_Arch_Spec.md
│   │   │   ├── TASK_PAD_002_Safety_Concept.md
│   │   │   ├── TASK_PAD_003_Security_Concept.md
│   │   │   ├── REVIEW_PAD_Report.md
│   │   │   └── CHECKLIST_PAD.md
│   │   ├── EDR/              # Engineering Document Review
│   │   │   ├── TASK_EDR_001_Design_Spec.md
│   │   │   ├── TASK_EDR_002_Verification_Plan.md
│   │   │   ├── TASK_EDR_003_DFT_Spec.md
│   │   │   ├── TASK_EDR_004_CDC_Strategy.md
│   │   │   ├── TASK_EDR_005_SDC.md
│   │   │   ├── TASK_EDR_006_UPF.md
│   │   │   ├── REVIEW_EDR_Report.md
│   │   │   └── CHECKLIST_EDR.md
│   │   ├── IDR/              # Implementation Design Review
│   │   │   ├── TASK_IDR_001_RTL_Implementation.md
│   │   │   ├── TASK_IDR_002_UVM_Environment.md
│   │   │   ├── TASK_IDR_003_Testcase_Development.md
│   │   │   ├── TASK_IDR_004_Coverage_Collection.md
│   │   │   ├── REVIEW_IDR_Report.md
│   │   │   └── CHECKLIST_IDR.md
│   │   ├── FDR/              # Final Design Review
│   │   │   ├── TASK_FDR_001_Physical_Design.md
│   │   │   ├── TASK_FDR_002_STA_Signoff.md
│   │   │   ├── TASK_FDR_003_DFT_Implementation.md
│   │   │   ├── TASK_FDR_004_PV_Signoff.md
│   │   │   ├── REVIEW_FDR_Report.md
│   │   │   └── CHECKLIST_FDR.md
│   │   ├── PostSilicon/      # 硅后验证
│   │   │   ├── TASK_PS_001_ATE_Program.md
│   │   │   ├── TASK_PS_002_Validation_Report.md
│   │   │   └── CHECKLIST_PostSilicon.md
│   │   └── README.md         # 全局任务索引
│   │
│   ├── Reviews/              # 评审记录
│   │   ├── PCD/
│   │   ├── PAD/
│   │   ├── EDR/
│   │   ├── IDR/
│   │   ├── FDR/
│   │   └── PostSilicon/
│   │
│   ├── Bugs/                 # Bug管理
│   │   ├── P1_Critical/
│   │   ├── P2_Major/
│   │   ├── P3_Minor/
│   │   └── P4_Trivial/
│   │
│   ├── MeetingMinutes/       # 会议记录
│   ├── Milestones/           # 阶段交付物汇总
│   ├── RiskMgmt/             # 风险管理
│   ├── ChangeMgmt/           # 变更管理
│   └── StatusReports/        # 状态报告
│
├── Docs/                     # 文档
│   ├── Arch/                 # 架构文档
│   │   ├── Architecture_Specification.md     # [TEMPLATE: 含History章节记录版本变更]
│   │   ├── System_Architecture.md            # [TEMPLATE: 含History章节]
│   │   ├── SoC_Architecture.md               # [TEMPLATE: 含History章节]
│   │   ├── Safety_Concept.md                 # [TEMPLATE: 含History章节]
│   │   └── Security_Architecture.md          # [TEMPLATE: 含History章节]
│   │
│   ├── Design/               # 设计规格
│   │   ├── Design_Specification.md           # [TEMPLATE: 含History章节]
│   │   ├── Interface_Specs/
│   │   │   ├── AXI4_Interface_Spec.md        # [TEMPLATE: 含History章节]
│   │   │   └── APB_Interface_Spec.md         # [TEMPLATE: 含History章节]
│   │   ├── Module_Specs/
│   │   │   └── Module_Template.md            # [TEMPLATE: 含History章节]
│   │   ├── SDC/              # 时序约束 (原ToolConfig内容)
│   │   │   ├── synthesis.sdc                 # [TEMPLATE]
│   │   │   └── pt_analysis.sdc
│   │   ├── UPF/              # 低功耗意图
│   │   │   └── power_intent.upf              # [TEMPLATE]
│   │   └── SGDC/             # SpyGlass配置
│   │       ├── lint.sgdc
│   │       └── cdc.sgdc
│   │
│   ├── Verification/         # 验证计划与报告
│   │   ├── Verification_Plan.md              # [TEMPLATE: 含History章节]
│   │   ├── Testplan_Coverage.md              # [TEMPLATE: 含History章节]
│   │   └── Coverage_Report.md                # [TEMPLATE: 含History章节]
│   │
│   ├── FuSa/                 # 功能安全文档
│   │   ├── FMEDA_Report.md                   # [TEMPLATE: 含History章节]
│   │   ├── Safety_Concept.md                 # [TEMPLATE: 含History章节]
│   │   └── Safety_Mechanism_Signals.md       # [TEMPLATE: 含History章节]
│   │
│   ├── DFT/                  # DFT规格
│   │   ├── DFT_Specification.md              # [TEMPLATE: 含History章节]
│   │   └── Scan_Plan.md                      # [TEMPLATE: 含History章节]
│   │
│   ├── Physical/             # 物理设计文档
│   │   ├── Floorplan_Guideline.md            # [TEMPLATE: 含History章节]
│   │   └── Power_Plan.md                     # [TEMPLATE: 含History章节]
│   │
│   └── Firmware/             # 固件文档
│       └── Firmware_Spec.md                  # [TEMPLATE: 含History章节]
│
├── Design/                   # 设计数据 (原DesignData)
│   ├── RTL/                  # RTL源码
│   │   ├── soc/              # SoC层级模块
│   │   │   ├── top/
│   │   │   │   ├── soc_top.sv              # [TEMPLATE_WITH_HEADER: 版本记录在header中]
│   │   │   │   └── soc_top.f
│   │   │   ├── bus/
│   │   │   │   ├── bus_matrix.sv
│   │   │   │   └── bus_matrix.f
│   │   │   ├── system/
│   │   │   │   ├── system_ctrl.sv
│   │   │   │   └── system_ctrl.f
│   │   │   ├── safety/
│   │   │   │   ├── safety_monitor.sv
│   │   │   │   └── safety_monitor.f
│   │   │   ├── memory/
│   │   │   │   ├── mem_ctrl.sv
│   │   │   │   └── mem_ctrl.f
│   │   │   ├── otp/
│   │   │   │   ├── otp_ctrl.sv
│   │   │   │   └── otp_ctrl.f
│   │   │   ├── clkrst/
│   │   │   │   ├── clk_rst_ctrl.sv
│   │   │   │   └── clk_rst_ctrl.f
│   │   │   └── iomux/
│   │   │       ├── io_mux.sv
│   │   │       └── io_mux.f
│   │   │
│   │   └── ip/               # IP层级模块
│   │       ├── uart/
│   │       │   ├── uart_top.sv             # [TEMPLATE_WITH_HEADER: 版本记录在header中]
│   │       │   ├── uart_tx.sv
│   │       │   ├── uart_rx.sv
│   │       │   ├── uart_regs.sv
│   │       │   └── uart.f
│   │       ├── spi/
│   │       │   ├── spi_top.sv
│   │       │   ├── spi_master.sv
│   │       │   ├── spi_slave.sv
│   │       │   └── spi.f
│   │       └── i2c/          # 其他IP实例
│   │           ├── i2c_top.sv
│   │           └── i2c.f
│   │
│   ├── Netlist/              # 综合后网表
│   │   ├── synth/
│   │   ├── dft/
│   │   └── pr/
│   │
│   ├── GDS/                  # 版图数据
│   └── Constraints/          # 其他约束文件
│
├── Verification/             # 验证环境
│   ├── Env/                  # 验证环境
│   │   ├── uvm/              # UVM基础环境
│   │   │   ├── base/
│   │   │   │   ├── base_test.sv            # [TEMPLATE] v0.1.0
│   │   │   │   ├── base_sequence.sv
│   │   │   │   └── base_scoreboard.sv
│   │   │   ├── agents/
│   │   │   │   ├── axi4_agent.sv
│   │   │   │   ├── apb_agent.sv
│   │   │   │   └── uart_agent.sv
│   │   │   └── env_top.sv
│   │   │
│   │   ├── tb/               # Testbench
│   │   │   ├── tb_top.sv                   # [TEMPLATE] v0.1.0
│   │   │   ├── tb_top.f
│   │   │   ├── clock_gen.sv
│   │   │   └── reset_gen.sv
│   │   │
│   │   ├── sva/              # 断言
│   │   │   ├── protocol_checkers.sv
│   │   │   ├── safety_assertions.sv
│   │   │   └── coverage_assertions.sv
│   │   │
│   │   └── tvla/             # 侧信道测试
│   │       └── tvla_testbench.sv
│   │
│   ├── Testcases/            # 测试用例
│   │   ├── directed/         # 定向测试
│   │   │   ├── tc_smoke.sv                 # [TEMPLATE] v0.1.0
│   │   │   ├── tc_rst_reg.sv
│   │   │   ├── tc_basic_rw.sv
│   │   │   └── tc_interrupt.sv
│   │   │
│   │   ├── random/           # 随机测试
│   │   │   ├── tc_random_tx.sv
│   │   │   └── tc_stress.sv
│   │   │
│   │   └── vectors/          # 测试向量
│   │       ├── nist_vectors/
│   │       ├── directed_patterns/
│   │       └── golden_ref/
│   │
│   ├── Regression/           # 回归测试配置
│   │   ├── regression_full.cfg
│   │   ├── regression_smoke.cfg
│   │   └── regression_nightly.cfg
│   │
│   └── Coverage/             # 覆盖率数据
│       ├── coverage_plan.md
│       └── coverage_report.md
│
├── Validation/               # 硅前/硅后验证
│   ├── FPGA/
│   ├── ATE/
│   └── PostSilicon/
│
├── Firmware/                 # 固件
│   ├── BootROM/
│   ├── Drivers/
│   ├── HAL_BSP/
│   └── TestPrograms/
│
├── Scripts/                  # EDA工具脚本
│   ├── Makefile
│   ├── flow.py
│   ├── config.mk
│   ├── common/
│   ├── rtl/
│   ├── lint/
│   ├── synth/
│   ├── dft/
│   ├── pr/
│   ├── sta/
│   ├── lec/
│   └── signoff/
│
├── Reference/                # 参考资料
│   ├── NIST_Standards/
│   ├── Datasheets/
│   └── AppNotes/
│
└── Temp/                     # EDA工具临时文件（不提交git）
    ├── VCS/
    ├── Verilator/
    ├── Spyglass/
    ├── DesignCompiler/
    ├── ICC2/
    ├── Innovus/
    ├── PrimeTime/
    ├── Tessent/
    ├── Calibre/
    └── Others/
```
│   │   ├── Coding_Yang/      # RTL/验证实现任务
│   │   ├── Design_Agent/     # 设计文档任务
│   │   ├── Verification_Agent/ # 验证文档任务
│   │   ├── DFT_Agent/        # DFT任务
│   │   ├── FuSa_Engineer/    # 功能安全任务
│   │   ├── IP_Architect/     # IP架构任务（IP项目）
│   │   ├── System_Architect/ # 系统架构任务（SoC项目）
│   │   ├── PM_Agent/         # 项目管理任务
│   │   └── README.md         # 全局任务索引
│   ├── Reviews/              # 评审记录
│   │   ├── PCD/              # Project Concept Definition
│   │   ├── PAD/              # Product Architecture Definition
│   │   ├── EDR/              # Engineering Document Review
│   │   ├── IDR/              # Implementation Design Review
│   │   ├── FDR/              # Final Design Review
│   │   └── PostSilicon/      # 硅后验证
│   ├── Bugs/                 # Bug管理
│   │   ├── P1_Critical/      # 致命
│   │   ├── P2_Major/         # 严重
│   │   ├── P3_Minor/         # 轻微
│   │   └── P4_Trivial/       # 可忽略
│   ├── MeetingMinutes/       # 会议记录
│   ├── Milestones/           # 阶段交付物汇总
│   ├── RiskMgmt/             # 风险管理
│   ├── ChangeMgmt/           # 变更管理
│   └── StatusReports/        # 状态报告
│
├── Docs/                     # 文档
│   ├── Arch/                 # 架构文档
│   ├── Design/               # 设计规格
│   │   ├── Interface_Specs/       # 接口规格
│   │   └── Module_Specs/          # 模块规格
│   ├── Verification/         # 验证计划与报告
│   ├── FuSa/                 # 功能安全文档
│   │   ├── FMEDA_Report.md
│   │   ├── Safety_Concept.md
│   │   └── Safety_Mechanism_Signals.md
│   ├── DFT/                  # DFT规格
│   ├── Physical/             # 物理设计文档
│   └── Firmware/             # 固件文档
│
├── Design/                   # 设计数据
│   ├── RTL/                  # RTL源码 (.v/.sv)
│   │   ├── top/              # 顶层模块
│   │   ├── core/             # 核心模块
│   │   ├── interface/        # 接口模块
│   │   └── safety/           # 安全机制模块
│   ├── Netlist/              # 综合后网表
│   │   ├── synth/            # 综合网表
│   │   ├── dft/              # DFT插入后网表
│   │   └── pr/               # PR后网表
│   ├── GDS/                  # 版图数据
│   ├── SDC/                  # 时序约束
│   ├── UPF/                  # 低功耗意图
│   └── Constraints/          # 其他约束文件
│
├── Verification/             # 验证环境
│   ├── Env/                  # 验证环境
│   │   ├── uvm/              # UVM环境
│   │   ├── tb/               # Testbench
│   │   ├── sva/              # 断言
│   │   └── tvla/             # 侧信道测试
│   ├── Testcases/            # 测试用例
│   │   ├── directed/         # 定向测试
│   │   ├── random/           # 随机测试
│   │   └── vectors/          # 测试向量
│   ├── Regression/           # 回归测试配置
│   └── Coverage/             # 覆盖率数据
│
├── Validation/               # 硅前/硅后验证
│   ├── FPGA/                 # FPGA验证
│   ├── ATE/                  # ATE测试程序
│   └── PostSilicon/          # 硅后验证
│
├── Firmware/                 # 固件
│   ├── BootROM/              # BootROM代码
│   ├── Drivers/              # 驱动程序
│   ├── HAL_BSP/              # HAL/BSP
│   └── TestPrograms/         # 测试程序
│
├── Scripts/                  # EDA工具脚本 [优化重点]
│   ├── Makefile              # 统一入口
│   ├── flow.py               # 流程控制脚本
│   ├── config.mk             # 工具链配置
│   ├── common/               # 公共脚本库
│   │   ├── utils.tcl
│   │   ├── report_parser.py
│   │   └── metrics_collect.sh
│   ├── rtl/                  # RTL仿真脚本
│   │   ├── iverilog.mk
│   │   ├── verilator.mk
│   │   ├── vcs.mk
│   │   └── xrun.mk
│   ├── lint/                 # Lint检查脚本
│   │   ├── spyglass.mk
│   │   ├── verilator_lint.mk
│   │   └── ascent.mk
│   ├── synth/                # 逻辑综合脚本
│   │   ├── dc_shell.mk
│   │   ├── genus.mk
│   │   └── yosys.mk
│   ├── dft/                  # DFT脚本
│   │   ├── tessent.mk
│   │   ├── modus.mk
│   │   └── dftadvisor.mk
│   ├── pr/                   # 物理设计脚本
│   │   ├── innovus.mk
│   │   ├── icc2.mk
│   │   └── openroad.mk
│   ├── sta/                  # 时序分析脚本
│   │   ├── pt_shell.mk
│   │   ├── tempus.mk
│   │   └── opensta.mk
│   ├── lec/                  # 形式验证脚本
│   │   ├── conformal.mk
│   │   └── formality.mk
│   └── signoff/              # Signoff脚本
│       ├── calibre.mk
│       ├── pegasus.mk
│       └── klayout.mk
│
├── Reference/                # 参考资料
│   ├── NIST_Standards/
│   ├── Datasheets/
│   └── AppNotes/
│
└── Temp/                     # EDA工具临时文件（不提交git）
    ├── VCS/                  # VCS仿真中间文件
    ├── Verilator/            # Verilator编译目录
    ├── Spyglass/             # Spyglass报告
    ├── DesignCompiler/       # DC工作目录
    ├── ICC2/                 # ICC2工作目录
    ├── Innovus/              # Innovus工作目录
    ├── PrimeTime/            # PT工作目录
    ├── Tessent/              # DFT工作目录
    ├── Calibre/              # PV工作目录
    └── Others/               # 其他临时文件
```

---

## EDA工具流程脚本

### 4.1 统一Makefile入口

```makefile
# Scripts/Makefile - 统一EDA入口

#==============================================================================
# 项目配置
#==============================================================================
PROJECT_NAME    ?= aes_crypto
RTL_TOP         ?= aes_top
TB_TOP          ?= tb_aes_top
RTL_DIR         ?= ../Design/RTL
TB_DIR          ?= ../Verification
SIMULATOR       ?= iverilog  # iverilog/verilator/vcs/xrun
SYNTH_TOOL      ?= yosys     # yosys/dc/genus
PR_TOOL         ?= openroad  # openroad/innovus/icc2

#==============================================================================
# 默认目标
#==============================================================================
.PHONY: help lint rtl sim synth dft pr sta signoff clean

help:
	@echo "================================================================"
	@echo "$(PROJECT_NAME) - EDA Tool Flow"
	@echo "================================================================"
	@echo ""
	@echo "=== RTL Development ==="
	@echo "  make rtl               - Compile RTL (lint check)"
	@echo "  make sim TEST=tc_smoke - Run simulation"
	@echo "  make regression        - Run regression suite"
	@echo "  make coverage          - Collect coverage"
	@echo ""
	@echo "=== Verification ==="
	@echo "  make lint              - Run static checks"
	@echo "  make cdc               - Run CDC checks"
	@echo "  make sva               - Run assertion checks"
	@echo ""
	@echo "=== Implementation ==="
	@echo "  make synth             - Logic synthesis"
	@echo "  make dft               - DFT insertion"
	@echo "  make pr                - Place & Route"
	@echo "  make sta               - Static timing analysis"
	@echo ""
	@echo "=== Signoff ==="
	@echo "  make lec               - Logic equivalence check"
	@echo "  make drc               - Design rule check"
	@echo "  make lvs               - Layout vs schematic"
	@echo "  make signoff           - Full signoff flow"
	@echo ""
	@echo "=== Utilities ==="
	@echo "  make dashboard         - Update project dashboard"
	@echo "  make metrics           - Collect metrics"
	@echo "  make clean             - Clean temporary files"
	@echo ""
	@echo "Examples:"
	@echo "  make sim TEST=tc_nist SIMULATOR=vcs"
	@echo "  make synth SYNTH_TOOL=dc"
	@echo "================================================================"

#==============================================================================
# RTL Development
#==============================================================================
rtl: lint
	@echo "[RTL] Compilation successful"

sim:
	$(MAKE) -f rtl/$(SIMULATOR).mk TEST=$(TEST)

regression:
	@./common/run_regression.py --suite full

coverage:
	@./common/collect_coverage.py --tool $(SIMULATOR)

#==============================================================================
# Verification
#==============================================================================
lint:
	$(MAKE) -f lint/lint.mk TOOL=$(LINT_TOOL)

cdc:
	$(MAKE) -f lint/cdc.mk

sva:
	$(MAKE) -f rtl/$(SIMULATOR).mk TARGET=sva

#==============================================================================
# Implementation
#==============================================================================
synth:
	$(MAKE) -f synth/$(SYNTH_TOOL).mk

dft:
	$(MAKE) -f dft/$(DFT_TOOL).mk

pr:
	$(MAKE) -f pr/$(PR_TOOL).mk

sta:
	$(MAKE) -f sta/sta.mk

#==============================================================================
# Signoff
#==============================================================================
lec:
	$(MAKE) -f lec/lec.mk

drc:
	$(MAKE) -f signoff/pv.mk TARGET=drc

lvs:
	$(MAKE) -f signoff/pv.mk TARGET=lvs

signoff: lec sta drc lvs
	@echo "[Signoff] All checks passed"

#==============================================================================
# Utilities
#==============================================================================
dashboard:
	@./common/update_dashboard.py

metrics:
	@./common/metrics_collect.sh

clean:
	@rm -rf ../../Temp/*
	@echo "[Clean] Temporary files removed"
```

### 4.2 工具链配置 (config.mk)

```makefile
# Scripts/config.mk - 工具链配置

#==============================================================================
# 工具路径 (可自定义)
#==============================================================================
# 开源工具 (默认)
IVERILOG        ?= iverilog
VVP             ?= vvp
VERILATOR       ?= verilator
YOSYS           ?= yosys
OPENROAD        ?= openroad
OPENSTA         ?= opensta
MAGIC           ?= magic
NETGEN          ?= netgen
KLAYOUT         ?= klayout

# 商业工具 (需配置)
VCS             ?= vcs
VERDI           ?= verdi
DC_SHELL        ?= dc_shell
GENUS           ?= genus
INNOVUS         ?= innovus
ICC2            ?= icc2
PRIMETIME       ?= pt_shell
TEMPUS          ?= tempus
CONFORMAL       ?= lec
FORMALITY       ?= formality
TESSENT         ?= tessent
MODUS           ?= modus
SPYGLASS        ?= spyglass
ASCENT          ?= ascent
CALIBRE         ?= calibre

#==============================================================================
# 工艺库配置
#==============================================================================
PROCESS_NODE    ?= tsmc7nm
PDK_ROOT        ?= /opt/pdk/$(PROCESS_NODE)
STD_CELL_LIB    ?= $(PDK_ROOT)/lib/stdcells.lib
IO_LIB          ?= $(PDK_ROOT)/lib/iocells.lib
LEF_FILE        ?= $(PDK_ROOT)/lef/stdcells.lef
TECH_LEF        ?= $(PDK_ROOT)/lef/tech.lef
GDS_FILE        ?= $(PDK_ROOT)/gds/stdcells.gds

#==============================================================================
# 设计约束
#==============================================================================
CLK_PERIOD      ?= 10.0
CLK_PORT        ?= clk
RESET_PORT      ?= rst_n
INPUT_DELAY     ?= 2.0
OUTPUT_DELAY    ?= 2.0
```

### 4.3 仿真脚本模板 (iverilog.mk)

```makefile
# Database/Scripts/rtl/iverilog.mk - Icarus Verilog仿真

TEST            ?= tc_smoke
OUT_DIR         ?= ../../Temp/VCS
RTL_DIR         ?= ../Design/RTL
TC_DIR          ?= ../Verification/Testcases/directed
TB_DIR          ?= ../Verification/Env/tb

COMP_FLAGS      = -g2012 -Wall \
                  -y $(RTL_DIR) \
                  -I $(RTL_DIR) \
                  -I $(TB_DIR) \
                  -D SIMULATION \
                  -D DUMP_VCD

.PHONY: compile sim view clean

compile:
	@mkdir -p $(OUT_DIR)
	@echo "[Iverilog] Compiling $(TEST)..."
	$(IVERILOG) $(COMP_FLAGS) -o $(OUT_DIR)/$(TEST).out \
		$(TC_DIR)/$(TEST).sv 2>&1 | tee $(OUT_DIR)/$(TEST)_compile.log

sim: compile
	@echo "[Iverilog] Running $(TEST)..."
	cd $(OUT_DIR) && $(VVP) $(TEST).out 2>&1 | tee $(TEST)_sim.log
	@echo "[Iverilog] Simulation complete"
	@./common/parse_sim_log.py $(OUT_DIR)/$(TEST)_sim.log

view:
	gtkwave $(OUT_DIR)/$(TEST).vcd &

clean:
	@rm -f $(OUT_DIR)/$(TEST).out $(OUT_DIR)/$(TEST)_*.log $(OUT_DIR)/$(TEST).vcd
```

### 4.4 综合脚本模板 (yosys.mk)

```makefile
# Database/Scripts/synth/yosys.mk - Yosys综合

OUT_DIR         ?= ../../Temp/Yosys
RTL_DIR         ?= ../Design/RTL
TOP             ?= $(RTL_TOP)

.PHONY: synth synth_opt clean

synth:
	@mkdir -p $(OUT_DIR)
	@echo "[Yosys] Synthesizing $(TOP)..."
	$(YOSYS) -p "
		read_verilog $(RTL_DIR)/*.v;
		synth -top $(TOP);
		dfflibmap -liberty $(STD_CELL_LIB);
		abc -liberty $(STD_CELL_LIB);
		clean;
		write_verilog $(OUT_DIR)/$(TOP)_synth.v;
		write_sdc $(OUT_DIR)/$(TOP).sdc;
	" 2>&1 | tee $(OUT_DIR)/yosys.log
	@echo "[Yosys] Synthesis complete"

synth_opt: synth
	@echo "[Yosys] Optimizing..."
	$(YOSYS) -p "
		read_verilog $(OUT_DIR)/$(TOP)_synth.v;
		read_liberty $(STD_CELL_LIB);
		opt;
		techmap;
		opt;
		write_verilog $(OUT_DIR)/$(TOP)_opt.v;
	" 2>&1 | tee $(OUT_DIR)/yosys_opt.log
```

### 4.5 物理设计脚本模板 (openroad.mk)

```makefile
# Database/Scripts/pr/openroad.mk - OpenROAD物理设计

OUT_DIR         ?= ../../Temp/OpenROAD
RTL_TOP         ?= aes_top

.PHONY: floorplan place cts route final

floorplan:
	@mkdir -p $(OUT_DIR)
	@echo "[OpenROAD] Floorplan..."
	openroad -exit $(SCRIPTS_DIR)/pr/floorplan.tcl \
		-log $(OUT_DIR)/floorplan.log

place: floorplan
	@echo "[OpenROAD] Placement..."
	openroad -exit $(SCRIPTS_DIR)/pr/place.tcl \
		-log $(OUT_DIR)/place.log

cts: place
	@echo "[OpenROAD] CTS..."
	openroad -exit $(SCRIPTS_DIR)/pr/cts.tcl \
		-log $(OUT_DIR)/cts.log

route: cts
	@echo "[OpenROAD] Routing..."
	openroad -exit $(SCRIPTS_DIR)/pr/route.tcl \
		-log $(OUT_DIR)/route.log

final: route
	@echo "[OpenROAD] Final..."
	openroad -exit $(SCRIPTS_DIR)/pr/final.tcl \
		-log $(OUT_DIR)/final.log

pr: final
	@echo "[OpenROAD] Physical design complete"
```

---

### 5.1 Agent角色定义

```yaml
# Agent角色配置
agents:
  # 云端Agent (OpenClaw托管)
  pm_agent:
    name: "PM Agent"
    role: project_manager
    capabilities: [planning, scheduling, reporting]
    location: cloud
    trigger_keywords: ["项目计划", "里程碑", "进度"]

  ai_yang:
    name: "AI Yang"
    role: quality_gatekeeper
    capabilities: [review, checklist, quality_check]
    location: cloud
    trigger_keywords: ["review", "检查", "质量"]

  design_agent:
    name: "Design Agent"
    role: documentation_writer
    capabilities: [spec_writing, architecture_doc, dft_spec, sdc, upf, sgdc]
    location: cloud
    trigger_keywords: ["design spec", "架构文档", "dft spec", "sdc", "upf"]
    responsibilities:
      - Design Spec编写
      - DFT Spec编写
      - SDC约束定义
      - UPF低功耗意图
      - SpyGlass配置文件(sgdc)

  verification_agent:
    name: "Verification Agent"
    role: verification_planning
    capabilities: [testplan, coverage_plan]
    location: cloud
    trigger_keywords: ["验证计划", "testplan"]

  fusa_agent:
    name: "FuSa Agent"
    role: functional_safety
    capabilities: [fmeda, safety_analysis]
    location: cloud
    trigger_keywords: ["FMEDA", "安全", "ASIL"]

  architect:
    name: "Architect"
    role: chief_architect
    capabilities: [system_architecture, soc_architecture, fusa_architecture, cybersecurity_architecture, architecture_review]
    location: cloud
    trigger_keywords: ["架构设计", "系统设计", "SoC架构", "FuSa架构", "安全架构"]
    responsibilities:
      - 系统架构设计
      - SoC架构设计
      - FuSa架构设计
      - CyberSecurity架构设计
      - 输出架构文档
      - Review所有开发流程交付物

  # 本地Agent (部署在用户主机)
  design_coding_agent:
    name: "Design Coding Agent"
    role: rtl_implementation
    capabilities: [rtl_coding, lint_check, synth_env_setup, netlist_generation]
    location: local
    host: user_workstation
    responsibilities:
      - RTL开发 (Verilog/SystemVerilog)
      - LINT检查与清理
      - 综合环境搭建
      - 生成综合后网表
    eda_tools: [iverilog, verilator, vcs, spyglass, dc_shell, genus, yosys]
    trigger_keywords: ["Design Coding Agent 任务:", "RTL开发", "LINT", "综合"]

  verification_coding_agent:
    name: "Verification Coding Agent"
    role: verification_implementation
    capabilities: [testcase_development, env_debug, coverage_collection, regression]
    location: local
    host: user_workstation
    responsibilities:
      - 验证case开发 (UVM/Directed/Random)
      - 验证环境调试
      - 覆盖率收集与报告
      - 回归测试执行
    eda_tools: [vcs, xcelium, verilator, imc, verdi]
    trigger_keywords: ["Verification Coding Agent 任务:", "验证case", "覆盖率", "回归"]

  flow_agent:
    name: "Flow Agent"
    role: physical_implementation
    capabilities: [dft_insertion, sta_analysis, physical_design, signoff]
    location: local
    host: user_workstation
    responsibilities:
      - DFT插入 (Scan/MBIST)
      - STA时序分析
      - 物理设计 (Floorplan/CTS/PR)
      - Signoff检查 (DRC/LVS)
    eda_tools: [tessent, modus, pt_shell, tempus, innovus, icc2, openroad, calibre]
    trigger_keywords: ["Flow Agent 任务:", "DFT", "STA", "PR", "Signoff"]
```

### 5.2 任务管理与自动流转

#### 5.2.1 任务状态机

```
┌─────────┐    assign    ┌─────────┐    start     ┌─────────┐
│ PENDING │ ───────────→ │ ASSIGNED│ ───────────→ │ RUNNING │
└─────────┘              └─────────┘              └────┬────┘
      ▲                                                │
      │              complete                         │ submit
      │         ┌──────────────┐                      ▼
      └─────────┤  COMPLETED   │←──────────────── ┌─────────┐
                  └──────────────┘                 │REVIEWING│
      ▲                                            └────┬────┘
      │              pass                               │
      │         ┌──────────────┐                      ▼
      └─────────┤   APPROVED   │←──────────────── ┌─────────┐
                  └──────────────┘                 │  REVIEW │
      ▲                                            └────┬────┘
      │              fail                               │
      │         ┌──────────────┐                      ▼
      └─────────┤    REJECTED  │←──────────────── ┌─────────┐
                  └──────────────┘                 │ REWORK  │
                                                   └─────────┘
```

#### 5.2.2 任务JSON格式

```json
{
  "task_id": "TASK-AES-RTL-001",
  "project_id": "IP_20260331_001",
  "project_name": "AES_Crypto",
  "task_type": "rtl_implementation",
  "priority": "P0",
  "status": "assigned",
  
  "assignment": {
    "assigned_to": "Coding_Yang",
    "assigned_by": "PM_Agent",
    "assigned_date": "2026-04-02T10:00:00+08:00",
    "deadline": "2026-04-14T18:00:00+08:00"
  },
  
  "description": {
    "title": "AES Core RTL Implementation",
    "summary": "Implement AES core with 128/192/256-bit key support",
    "requirements": [
      "Support ECB, CBC, CTR, GCM, XTS modes",
      "Implement 3-share TI S-Box",
      "Pass all NIST test vectors"
    ],
    "acceptance_criteria": [
      "Code coverage >95%",
      "Lint clean",
      "All directed tests pass"
    ]
  },
  
  "deliverables": {
    "rtl_files": [
      "Design/RTL/aes_core.v",
      "Design/RTL/sbox_masked.v",
      "Design/RTL/key_schedule.v"
    ],
    "testcases": [
      "Verification/Testcases/directed/tc_aes_core_direct.sv"
    ],
    "reports": [
      "ProjectMgmt/Tasks/Coding_Yang/TASK-AES-RTL-001_report.md"
    ]
  },
  
  "dependencies": {
    "pre_tasks": ["TASK-AES-SPEC-001"],
    "post_tasks": ["TASK-AES-LINT-001", "TASK-AES-TC-001"],
    "blocks": []
  },
  
  "execution": {
    "working_directory": "sandbox/aes",
    "commands": [
      "make rtl",
      "make sim TEST=tc_aes_core_direct",
      "make coverage"
    ],
    "expected_duration": "8h",
    "retry_policy": {
      "max_attempts": 3,
      "on_failure": "notify_pm"
    }
  },
  
  "metadata": {
    "created_by": "PM_Agent",
    "created_date": "2026-04-02T09:00:00+08:00",
    "phase": "IDR",
    "tags": ["rtl", "aes", "core"]
  }
}
```

#### 5.2.3 自动流转规则

```python
# task_workflow.py - 任务自动流转

class TaskWorkflow:
    """任务状态自动流转引擎"""
    
    RULES = {
        # 规则: 当前状态 → 触发条件 → 下一状态
        "pending": {
            "on_assign": "assigned",
            "auto_assign": "assigned"  # 根据负载均衡自动分配
        },
        "assigned": {
            "on_start": "running",
            "on_timeout": "pending"  # 超时未开始，重新分配
        },
        "running": {
            "on_submit": "reviewing",
            "on_block": "blocked",
            "progress_check": "running"  # 进度检查点
        },
        "reviewing": {
            "on_pass": "completed",
            "on_fail": "rejected",
            "auto_review": "completed"  # 自动检查通过
        },
        "rejected": {
            "on_rework": "running",
            "on_reassign": "assigned"
        },
        "completed": {
            "trigger_next": True  # 触发下游任务
        }
    }
    
    def transition(self, task, event):
        """执行状态流转"""
        current = task.status
        if event in self.RULES[current]:
            new_status = self.RULES[current][event]
            self._update_status(task, new_status)
            self._notify_agents(task, current, new_status)
            self._execute_hooks(task, new_status)
            return new_status
        return None
    
    def _execute_hooks(self, task, new_status):
        """执行状态钩子"""
        if new_status == "reviewing":
            # 自动触发质量检查
            self.trigger_quality_check(task)
        elif new_status == "completed":
            # 触发下游任务
            self.trigger_downstream_tasks(task)
            # 更新dashboard
            self.update_dashboard(task)
```

#### 5.2.4 Agent通信协议

```json
{
  "protocol_version": "1.0",
  "message_types": {
    "task_assignment": {
      "description": "任务分配",
      "fields": ["task_id", "assignee", "description", "deliverables", "deadline"]
    },
    "task_status": {
      "description": "任务状态更新",
      "fields": ["task_id", "status", "progress", "blockers", "output_files"]
    },
    "review_request": {
      "description": "评审请求",
      "fields": ["review_type", "deliverables", "reviewer", "criteria"]
    },
    "review_feedback": {
      "description": "评审反馈",
      "fields": ["review_id", "issues", "severity", "recommendations"]
    },
    "milestone_achieved": {
      "description": "里程碑达成",
      "fields": ["milestone", "deliverables", "metrics"]
    }
  }
}
```

---

## 6. 项目Dashboard

### 6.1 Dashboard架构

```yaml
# dashboard.yaml - Dashboard配置

dashboard:
  refresh_interval: 300  # 5分钟
  
  panels:
    # 阶段进度面板
    phase_status:
      type: progress_bar
      phases: [PCD, PAD, EDR, IDR, FDR, PostSilicon]
      current: IDR
      
    # 任务队列面板
    task_queue:
      type: table
      columns: [ID, Type, Assignee, Status, Deadline, Progress]
      filters: [status, priority, assignee]
      
    # Agent状态面板
    agent_status:
      type: grid
      agents: [PM_Agent, AI_Yang, Coding_Yang, Design_Agent, Verification_Agent]
      metrics: [active_tasks, completed_today, load]
      
    # 质量指标面板
    quality_metrics:
      type: charts
      metrics:
        - code_coverage: [line, branch, toggle, fsm]
        - bug_trend: [open, fixed, critical]
        - review_pass_rate: [pass, fail, pending]
        
    # 警报面板
    alerts:
      type: list
      severity: [critical, warning, info]
      auto_refresh: true
```

### 7.2 Dashboard页面 (Markdown格式)

```markdown
# AES_Crypto - Project Dashboard

*Last Updated: 2026-04-02 14:30:00*

---

## 📊 Phase Status

| Phase | Status | Progress | Gate Date |
|-------|--------|----------|-----------|
| PCD | ✅ COMPLETE | 100% | 2026-03-31 |
| PAD | ✅ COMPLETE | 100% | 2026-03-31 |
| EDR | ✅ COMPLETE | 100% | 2026-03-31 |
| IDR | 🚀 IN PROGRESS | 65% | 2026-04-28 |
| FDR | ⚪ NOT STARTED | 0% | - |
| Post Silicon | ⚪ NOT STARTED | 0% | - |

---

## 📝 Active Tasks

| Task ID | Type | Assignee | Status | Deadline | Progress |
|---------|------|----------|--------|----------|----------|
| TASK-AES-RTL-001 | RTL | Coding_Yang | 🟢 Running | 04/14 | 70% |
| TASK-AES-UVM-001 | UVM | Coding_Yang | 🟢 Running | 04/07 | 85% |
| TASK-AES-LINT-001 | LINT | Coding_Yang | ⏳ Waiting | 04/11 | - |
| TASK-AES-FMEDA-001 | FuSa | FuSa_Engineer | ⏳ Incoming | 04/18 | - |

---

## 👥 Agent Status

| Agent | Active Tasks | Completed Today | Load |
|-------|-------------|-----------------|------|
| PM_Agent | 5 | 3 | 🟢 Normal |
| AI_Yang | 1 | 2 | 🟢 Normal |
| Coding_Yang | 2 | 0 | 🟡 High |
| Design_Agent | 0 | 1 | 🟢 Idle |
| Verification_Agent | 0 | 1 | 🟢 Idle |

---

## 📈 Quality Metrics

### Code Coverage
```
Line:        ████████████████████░░ 92.5% (target: 90%)
Condition:   ████████████████████░░ 91.2% (target: 90%)
Toggle:      █████████████████░░░░░ 87.3% (target: 85%)
FSM:         █████████████████████░ 97.8% (target: 95%)
```

### Bug Trend
| Severity | Open | Fixed Today | Trend |
|----------|------|-------------|-------|
| P1 Critical | 0 | 0 | → |
| P2 Major | 0 | 0 | → |
| P3 Minor | 2 | 1 | ↓ |
| P4 Trivial | 1 | 0 | → |

---

## 🚨 Alerts

| Time | Severity | Message | Agent |
|------|----------|---------|-------|
| 14:25 | ⚠️ Warning | TASK-AES-RTL-001 approaching deadline (3 days) | PM_Agent |
| 14:20 | ℹ️ Info | Code coverage line metric exceeded target | AI_Yang |
| 13:45 | ✅ Success | EDR Minor Issues remediation completed | Design_Agent |

---

## 📅 Upcoming Milestones

| Date | Milestone | Owner | Status |
|------|-----------|-------|--------|
| 04/07 | UVM Environment Complete | Coding_Yang | 🟡 On Track |
| 04/14 | RTL Development Complete | Coding_Yang | 🟡 On Track |
| 04/18 | FMEDA Analysis Complete | FuSa_Engineer | ⏳ Planned |
| 04/28 | IDR Gate | PM_Agent | ⏳ Planned |

---

*Dashboard auto-generated from ProjectMgmt data*
```

### 7.3 Dashboard生成脚本

```python
#!/usr/bin/env python3
# common/update_dashboard.py - Dashboard更新脚本

import json
import os
from datetime import datetime
from pathlib import Path

class DashboardGenerator:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.dashboard_path = self.project_path / "ProjectMgmt" / "Dashboard.md"
        
    def generate(self):
        """生成Dashboard"""
        content = []
        content.append(self._header())
        content.append(self._phase_status())
        content.append(self._active_tasks())
        content.append(self._agent_status())
        content.append(self._quality_metrics())
        content.append(self._alerts())
        content.append(self._milestones())
        content.append(self._footer())
        
        with open(self.dashboard_path, 'w') as f:
            f.write('\n'.join(content))
    
    def _phase_status(self):
        """阶段状态"""
        phases = self._load_phase_data()
        # 生成表格...
        return "## Phase Status\n\n..."
    
    def _active_tasks(self):
        """活跃任务"""
        tasks = self._load_task_data()
        # 生成表格...
        return "## Active Tasks\n\n..."
    
    def _quality_metrics(self):
        """质量指标"""
        metrics = self._collect_metrics()
        # 生成图表...
        return "## Quality Metrics\n\n..."
```

---

## 7. Review节点体系

### 7.1 Review阶段定义

```yaml
# review_stages.yaml

review_stages:
  PCD:  # Project Concept Definition
    name: "项目概念定义"
    purpose: "确认项目可行性和商业价值"
    
    participants:
      required: [PM_Agent, AI_Yang, 实体Yang]
      optional: [System_Architect, IP_Architect]
    
    deliverables:
      - MRD (市场需求文档)
      - 可行性分析报告
      - 资源估算
      - 风险评估
    
    checklist:
      - 市场机会明确
      - 技术可行性确认
      - 资源可获得
      - 风险可控
    
    criteria:
      must_have: [MRD, 可行性分析]
      exit_condition: "所有检查项通过"

  PAD:  # Product Architecture Definition
    name: "产品架构定义"
    purpose: "冻结架构规格，确定实现方案"
    
    participants:
      required: [IP_Architect, System_Architect, AI_Yang, 实体Yang]
      optional: [FuSa_Engineer, Security_Expert]
    
    deliverables:
      - Architecture Specification
      - Safety Concept (FuSa)
      - Security Concept
      - Interface Specification
    
    checklist:
      - 架构满足功能需求
      - 安全机制设计完整
      - 功耗/面积目标可达
      - 接口定义明确
    
    criteria:
      must_have: [Architecture_Spec, Safety_Concept]
      exit_condition: "AI Yang有条件通过或实体Yang批准"

  EDR:  # Engineering Document Review
    name: "工程设计文档评审"
    purpose: "冻结设计文档基线"
    
    participants:
      required: [Design_Agent, Verification_Agent, AI_Yang, 实体Yang]
      optional: [DFT_Agent, Physical_Designer]
    
    deliverables:
      - Design Specification
      - Verification Plan
      - DFT Strategy
      - CDC/RDC Strategy
      - Power Intent
    
    checklist:
      - 8章节Design Spec完整
      - Verification Plan覆盖所有功能点
      - CDC策略定义
      - 低功耗意图定义
      - DFT可测性规划
    
    criteria:
      must_have: [Design_Spec, Verification_Plan]
      exit_condition: "实体Yang批准"

  IDR:  # Implementation Design Review
    name: "实现设计评审"
    purpose: "确认RTL和验证完成，代码冻结"
    
    participants:
      required: [Coding_Yang, AI_Yang, 实体Yang]
      optional: [Design_Agent, Verification_Agent]
    
    deliverables:
      - RTL Code (所有模块)
      - Testbench Environment
      - Coverage Report (>90%)
      - Lint/CDC Clean Report
      - FMEDA Analysis
    
    checklist:
      - 所有RTL模块完成
      - 代码覆盖率>90%
      - Lint/CDC无错误
      - 所有Critical/Major Bug修复
      - FMEDA分析完成
    
    criteria:
      must_have: [RTL, Coverage_Report, Lint_Report]
      exit_condition: "所有检查项通过"

  FDR:  # Final Design Review
    name: "最终设计评审"
    purpose: "确认物理实现完成，可Tapeout"
    
    participants:
      required: [Physical_Designer, DFT_Agent, AI_Yang, 实体Yang]
      optional: [PM_Agent]
    
    deliverables:
      - GDSII
      - STA Sign-off Report
      - DRC/LVS Clean Report
      - ATPG Patterns
      - Power Analysis
    
    checklist:
      - 时序收敛
      - DRC/LVS无错误
      - 功耗满足规格
      - DFT覆盖率达标
    
    criteria:
      must_have: [GDS, STA_Report, DRC_LVS_Report]
      exit_condition: "所有Signoff检查通过"

  PostSilicon:  # 硅后验证
    name: "硅后验证"
    purpose: "确认芯片功能正确，可量产"
    
    participants:
      required: [Validation_Engineer, PM_Agent, 实体Yang]
    
    deliverables:
      - ATE测试程序
      - 硅后验证报告
      - 量产测试规范
    
    checklist:
      - 所有功能测试通过
      - 良率达标
      - 可靠性测试通过
    
    criteria:
      must_have: [Validation_Report]
      exit_condition: "量产批准"
```

### 8.2 Review Checklist模板

```markdown
# {{STAGE}} Review Checklist

## 基本信息

| 字段 | 值 |
|------|-----|
| **评审阶段** | {{STAGE}} |
| **项目名称** | {{PROJECT_NAME}} |
| **评审日期** | {{DATE}} |
| **评审结果** | ☐ PASS / ☐ CONDITIONAL / ☐ FAIL |

## 参与人员

| 角色 | 姓名 | 签名 | 日期 |
|------|------|------|------|
| {{ROLE_1}} | | ☐ | |
| {{ROLE_2}} | | ☐ | |
| {{ROLE_3}} | | ☐ | |

## 交付物检查清单

| # | 交付物 | 必需 | 状态 | 位置 | 检查人 |
|---|--------|------|------|------|--------|
| 1 | {{DELIVERABLE_1}} | ✅ | ☐ | {{PATH_1}} | |
| 2 | {{DELIVERABLE_2}} | ✅ | ☐ | {{PATH_2}} | |
| 3 | {{DELIVERABLE_3}} | ⚠️ | ☐ | {{PATH_3}} | |

## 质量检查

| 检查项 | 标准 | 结果 | 备注 |
|--------|------|------|------|
| 完整性 | 所有必需交付物存在 | ☐ PASS / ☐ FAIL | |
| 一致性 | 交付物间无矛盾 | ☐ PASS / ☐ FAIL | |
| 可追溯性 | 需求→设计→验证链路完整 | ☐ PASS / ☐ FAIL | |
| 质量底线 | 无明显缺陷 | ☐ PASS / ☐ FAIL | |
| 规范性 | 符合模板要求 | ☐ PASS / ☐ FAIL | |

## 问题清单

| ID | 问题描述 | 严重程度 | 负责人 | 截止日期 | 状态 |
|----|----------|----------|--------|----------|------|
| 1 | | Critical/Major/Minor | | | Open/Fixed |

## 决策记录

| 决策项 | 决策 | 批准人 | 日期 |
|--------|------|--------|------|
| {{STAGE}} Gate | ☐ PASS / ☐ CONDITIONAL / ☐ FAIL | | |
| 条件通过项 | | | |
| 下一步行动 | | | |

## 签名

| 角色 | 签名 | 日期 |
|------|------|------|
| Quality Gatekeeper | ☐ | |
| Project Manager | ☐ | |
| 最终批准人 | ☐ | |
```

### 8.3 自动化Review检查

```python
#!/usr/bin/env python3
# common/auto_review.py - 自动化Review检查

class AutoReviewer:
    """自动化Review检查引擎"""
    
    CHECKS = {
        "PCD": [
            FileExistsCheck("ProjectMgmt/Planning/MRD.md"),
            FileExistsCheck("ProjectMgmt/RiskMgmt/Risk_Assessment.md"),
            MarkdownLintCheck(),
        ],
        "PAD": [
            FileExistsCheck("Docs/Arch/Architecture_Spec.md"),
            FileExistsCheck("Docs/FuSa/Safety_Concept.md"),
            StructureCheck(min_sections=8),
            TraceabilityCheck(),
        ],
        "EDR": [
            FileExistsCheck("Docs/Design/Design_Specification.md"),
            FileExistsCheck("Docs/Verification/Verification_Plan.md"),
            SectionCheck(required=["Overview", "Functions", "Registers", "Block Design"]),
        ],
        "IDR": [
            FileExistsCheck("Design/RTL/"),
            CoverageCheck(min_line=90, min_toggle=85),
            LintCheck(warnings_max=0),
            BugCheck(no_critical_major=True),
        ],
        "FDR": [
            FileExistsCheck("Design/GDS/"),
            TimingCheck(setup_slack_min=0, hold_slack_min=0),
            PVCheck(drc_clean=True, lvs_clean=True),
        ]
    }
    
    def review(self, stage, project_path):
        """执行自动化Review"""
        results = []
        for check in self.CHECKS[stage]:
            result = check.run(project_path)
            results.append(result)
        
        report = self._generate_report(stage, results)
        return report
    
    def _generate_report(self, stage, results):
        """生成Review报告"""
        passed = sum(1 for r in results if r.passed)
        total = len(results)
        
        return {
            "stage": stage,
            "summary": f"{passed}/{total} checks passed",
            "passed": passed == total,
            "details": [r.to_dict() for r in results]
        }
```

---

## 8. 本地Agent部署

### 8.1 部署架构

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户主机 (Linux/Mac)                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Coding Yang Agent Container               │   │
│  │                                                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │  Task Queue │  │  EDA Tools  │  │  Git Sync   │     │   │
│  │  │  Listener   │  │  Executor   │  │   Client    │     │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │   │
│  │         │                │                │             │   │
│  │         └────────────────┼────────────────┘             │   │
│  │                          ▼                              │   │
│  │                   ┌─────────────┐                        │   │
│  │                   │  Workflow   │                        │   │
│  │                   │   Engine    │                        │   │
│  │                   └─────────────┘                        │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   EDA Tools Volume                       │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │ Iverilog │ │ Verilator│ │  Yosys   │ │ OpenROAD │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │   │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │   │
│  │  │   VCS    │ │ DC Shell │ │  Innovus │ │  Calibre │   │   │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   Workspace Volume                       │   │
│  │              /home/user/workspace/                       │   │
│  │                    (bind mount)                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ SSH/Git
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OpenClaw Cloud Gateway                        │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │  AI Yang    │  │  PM Agent   │  │   GitHub    │             │
│  │  (云端)      │  │  (云端)      │  │   Mirror    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Docker部署配置

```dockerfile
# Dockerfile.coding-yang
FROM ubuntu:22.04

# 基础工具
RUN apt-get update && apt-get install -y \
    git \
    make \
    python3 \
    python3-pip \
    wget \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 开源EDA工具
RUN apt-get update && apt-get install -y \
    iverilog \
    verilator \
    yosys \
    gtkwave \
    && rm -rf /var/lib/apt/lists/*

# OpenROAD (预编译二进制)
RUN wget -q https://github.com/The-OpenROAD-Project/OpenROAD/releases/download/v2.0/openroad_2.0_amd64.deb \
    && dpkg -i openroad_2.0_amd64.deb \
    && rm openroad_2.0_amd64.deb

# Python依赖
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Agent代码
COPY agent/ /opt/coding-yang/
WORKDIR /opt/coding-yang

# 启动脚本
ENTRYPOINT ["python3", "agent.py"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  coding-yang:
    build:
      context: ./agent
      dockerfile: Dockerfile.coding-yang
    container_name: coding-yang-agent
    volumes:
      # 工作目录挂载
      - ${WORKSPACE}:/workspace:rw
      # EDA工具许可证
      - ${LM_LICENSE_FILE}:/opt/licenses:ro
      # 工具配置
      - ./config:/opt/config:ro
    environment:
      - OPENCLAW_GATEWAY=${OPENCLAW_GATEWAY}
      - AGENT_ID=coding_yang
      - AGENT_TOKEN=${AGENT_TOKEN}
      - WORKSPACE=/workspace
    networks:
      - eda_network
    restart: unless-stopped

networks:
  eda_network:
    driver: bridge
```

### 8.3 本地Agent代码

```python
#!/usr/bin/env python3
# agent/agent.py - Coding Yang本地Agent

import os
import json
import asyncio
import websockets
from pathlib import Path
from datetime import datetime

class CodingYangAgent:
    """Coding Yang本地Agent"""
    
    def __init__(self):
        self.agent_id = "coding_yang"
        self.gateway_url = os.getenv("OPENCLAW_GATEWAY")
        self.workspace = Path(os.getenv("WORKSPACE", "/workspace"))
        self.active_tasks = {}
        
    async def run(self):
        """主循环"""
        async with websockets.connect(self.gateway_url) as ws:
            # 注册Agent
            await self._register(ws)
            
            # 监听任务
            while True:
                message = await ws.recv()
                await self._handle_message(ws, json.loads(message))
    
    async def _register(self, ws):
        """向Gateway注册"""
        await ws.send(json.dumps({
            "type": "register",
            "agent_id": self.agent_id,
            "capabilities": [
                "rtl_coding",
                "simulation",
                "lint",
                "synthesis",
                "debug"
            ],
            "eda_tools": self._detect_eda_tools()
        }))
    
    def _detect_eda_tools(self):
        """检测可用的EDA工具"""
        tools = []
        
        # 开源工具
        if self._cmd_exists("iverilog"):
            tools.append({"name": "iverilog", "type": "simulation", "version": self._get_version("iverilog -V")})
        if self._cmd_exists("verilator"):
            tools.append({"name": "verilator", "type": "simulation", "version": self._get_version("verilator --version")})
        if self._cmd_exists("yosys"):
            tools.append({"name": "yosys", "type": "synthesis", "version": self._get_version("yosys -V")})
        if self._cmd_exists("openroad"):
            tools.append({"name": "openroad", "type": "physical", "version": self._get_version("openroad -version")})
            
        # 商业工具 (需许可证)
        if self._cmd_exists("vcs"):
            tools.append({"name": "vcs", "type": "simulation", "license": "checked"})
        if self._cmd_exists("dc_shell"):
            tools.append({"name": "dc_shell", "type": "synthesis", "license": "checked"})
            
        return tools
    
    async def _handle_message(self, ws, message):
        """处理消息"""
        msg_type = message.get("type")
        
        if msg_type == "task_assign":
            await self._handle_task_assign(ws, message)
        elif msg_type == "task_cancel":
            await self._handle_task_cancel(ws, message)
        elif msg_type == "status_query":
            await self._handle_status_query(ws, message)
    
    async def _handle_task_assign(self, ws, message):
        """处理任务分配"""
        task = message["task"]
        task_id = task["task_id"]
        
        # 接受任务
        self.active_tasks[task_id] = {
            "task": task,
            "status": "accepted",
            "start_time": datetime.now().isoformat()
        }
        
        await ws.send(json.dumps({
            "type": "task_accepted",
            "task_id": task_id,
            "agent_id": self.agent_id
        }))
        
        # 执行任务
        asyncio.create_task(self._execute_task(ws, task))
    
    async def _execute_task(self, ws, task):
        """执行任务"""
        task_id = task["task_id"]
        task_type = task["task_type"]
        
        try:
            self.active_tasks[task_id]["status"] = "running"
            
            # 根据任务类型执行
            if task_type == "rtl_implementation":
                result = await self._run_rtl_task(task)
            elif task_type == "simulation":
                result = await self._run_simulation_task(task)
            elif task_type == "lint":
                result = await self._run_lint_task(task)
            else:
                result = {"status": "error", "message": "Unknown task type"}
            
            # 发送完成消息
            await ws.send(json.dumps({
                "type": "task_completed",
                "task_id": task_id,
                "result": result
            }))
            
        except Exception as e:
            await ws.send(json.dumps({
                "type": "task_failed",
                "task_id": task_id,
                "error": str(e)
            }))
        finally:
            del self.active_tasks[task_id]
    
    async def _run_rtl_task(self, task):
        """执行RTL任务"""
        import subprocess
        
        working_dir = self.workspace / task["execution"]["working_directory"]
        commands = task["execution"]["commands"]
        
        results = []
        for cmd in commands:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=working_dir,
                capture_output=True,
                text=True
            )
            results.append({
                "command": cmd,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            })
        
        # 解析结果
        success = all(r["returncode"] == 0 for r in results)
        
        return {
            "status": "success" if success else "failure",
            "commands": results,
            "output_files": self._collect_outputs(task)
        }
    
    def _collect_outputs(self, task):
        """收集输出文件"""
        outputs = []
        for f in task["deliverables"].get("rtl_files", []):
            path = self.workspace / f
            if path.exists():
                outputs.append({
                    "file": f,
                    "size": path.stat().st_size,
                    "mtime": path.stat().st_mtime
                })
        return outputs
    
    def _cmd_exists(self, cmd):
        """检查命令是否存在"""
        return os.system(f"which {cmd} > /dev/null 2>&1") == 0
    
    def _get_version(self, cmd):
        """获取工具版本"""
        try:
            import subprocess
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip().split('\n')[0]
        except:
            return "unknown"

if __name__ == "__main__":
    agent = CodingYangAgent()
    asyncio.run(agent.run())
```

### 8.4 部署脚本

```bash
#!/bin/bash
# install_coding_yang.sh - 安装Coding Yang本地Agent

set -e

echo "=========================================="
echo "Coding Yang Agent 安装脚本"
echo "=========================================="

# 检查依赖
echo "[1/5] 检查依赖..."
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装"
    exit 1
fi

# 配置
WORKSPACE=${1:-"$HOME/workspace"}
OPENCLAW_GATEWAY=${2:-"ws://localhost:8080/agent"}

echo "[2/5] 创建工作目录..."
mkdir -p "$WORKSPACE"
mkdir -p "$WORKSPACE/sandbox"
mkdir -p "$WORKSPACE/eda_tools"

# 生成配置
echo "[3/5] 生成配置..."
cat > .env <<EOF
WORKSPACE=$WORKSPACE
OPENCLAW_GATEWAY=$OPENCLAW_GATEWAY
AGENT_TOKEN=$(openssl rand -hex 32)
LM_LICENSE_FILE=${LM_LICENSE_FILE:-""}
EOF

# 拉取/构建镜像
echo "[4/5] 构建Agent镜像..."
docker-compose build

# 启动
echo "[5/5] 启动Agent..."
docker-compose up -d

echo ""
echo "=========================================="
echo "安装完成!"
echo "=========================================="
echo ""
echo "配置信息:"
echo "  Workspace: $WORKSPACE"
echo "  Gateway:   $OPENCLAW_GATEWAY"
echo ""
echo "常用命令:"
echo "  docker-compose logs -f    # 查看日志"
echo "  docker-compose stop       # 停止Agent"
echo "  docker-compose start      # 启动Agent"
echo ""
echo "Coding Yang已就绪，等待任务分配..."
```

---

## 9. 实施路线图

### 9.1 阶段划分

```
Phase 1: 基础设施 (Week 1-2)
├── 统一Makefile入口框架
├── 开源工具链集成 (iverilog, verilator, yosys)
├── Dashboard基础框架
└── 任务JSON协议定义

Phase 2: Agent协作 (Week 3-4)
├── 任务状态机实现
├── Agent通信协议
├── 自动流转规则
└── Review Checklist模板

Phase 3: 本地部署 (Week 5-6)
├── Coding Yang容器化
├── EDA工具自动检测
├── 任务执行引擎
└── 结果回传机制

Phase 4: 高级功能 (Week 7-8)
├── Dashboard可视化
├── 自动化Review检查
├── 质量趋势分析
└── 多项目支持

Phase 5: 优化迭代 (Week 9+)
├── 性能优化
├── 用户体验改进
├── 商业工具集成
└── CI/CD集成
```

### 10.2 优先级矩阵

| 功能 | 影响 | 复杂度 | 优先级 | 计划 |
|------|------|--------|--------|------|
| 统一Makefile | 高 | 低 | P0 | Week 1 |
| Dashboard基础 | 高 | 中 | P0 | Week 1-2 |
| 任务JSON协议 | 高 | 中 | P0 | Week 2 |
| 开源工具集成 | 高 | 低 | P1 | Week 2 |
| Agent容器化 | 高 | 中 | P1 | Week 3-4 |
| 自动Review | 中 | 高 | P2 | Week 5-6 |
| 商业工具集成 | 中 | 高 | P2 | Week 7-8 |
| CI/CD集成 | 低 | 高 | P3 | Week 9+ |

### 10.3 成功指标

| 指标 | 基线 | 目标 | 测量方式 |
|------|------|------|----------|
| EDA工具启动时间 | 5分钟 | 30秒 | make命令执行时间 |
| 任务交接时间 | 手动1小时 | 自动5分钟 | 任务状态流转时间 |
| Review检查时间 | 2小时 | 15分钟 | AutoReview执行时间 |
| 覆盖率追踪 | 手动 | 自动实时 | Dashboard更新频率 |
| Agent可用性 | N/A | 99% | 在线监控 |

---

## 附录

### A. 工具链对比

| 工具类型 | 开源方案 | 商业方案 | 推荐 |
|----------|----------|----------|------|
| 仿真 | iverilog, verilator | VCS, Xcelium | 开源+商业 |
| 综合 | yosys | DC, Genus | 开源起步 |
| 物理设计 | OpenROAD | Innovus, ICC2 | 商业为主 |
| STA | OpenSTA | PrimeTime | 商业为主 |
| DFT | - | Tessent, Modus | 商业 |
| PV | Magic, KLayout | Calibre | 开源+商业 |

### B. 参考资源

1. [OpenLANE Documentation](https://openlane.readthedocs.io/)
2. [OpenROAD Flow](https://openroad.readthedocs.io/)
3. [SiliconCompiler Schema](https://docs.siliconcompiler.com/)
4. [ASIC Design Flow (VLSI)](https://yogish.com/blog/vlsi-blog/)

---

*文档版本: v1.0*  
*最后更新: 2026-04-02*  
*作者: AI Yang (Quality Gatekeeper)*
