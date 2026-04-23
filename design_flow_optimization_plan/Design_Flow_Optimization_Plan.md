# 车规级芯片设计全流程优化方案

## 版本信息
- **版本**: v2.0
- **日期**: 2025-05-13
- **作者**: AI Yang
- **适用范围**: SoC / IP 数字设计项目

---

## 目录

1. [概述](#概述)
2. [总体架构](#总体架构)
3. [目录结构定义](#目录结构定义)
4. [EDA工具流程脚本](#eda工具流程脚本)
5. [模板库](#模板库)
6. [多Agent协作机制](#多agent协作机制)
7. [项目Dashboard](#项目dashboard)
8. [Review节点体系](#review节点体系)
9. [本地Agent部署](#本地agent部署)
10. [实施路线图](#实施路线图)

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

### 项目实例化模板

项目骨架通过手动从 `templates/` 复制所需模板组装生成，实例化后目录结构如下：

```
project/
├── ProjectMgmt/              # 项目管理
│   ├── Planning/             # 项目计划
│   │   ├── Master_Schedule.md
│   │   ├── Milestone_Plan.md
│   │   ├── Resource_Plan.md
│   │   └── README.md
│   ├── Tasks/                # Agent任务清单
│   │   ├── AI_Yang/
│   │   │   └── TASK_LIST.md
│   │   ├── Coding_Yang/
│   │   │   ├── TASK_LIST.md
│   │   │   └── task_template.json
│   │   ├── Design_Agent/
│   │   ├── DFT_Agent/
│   │   ├── FuSa_Engineer/
│   │   ├── IP_Architect/
│   │   ├── PM_Agent/
│   │   ├── System_Architect/
│   │   └── Verification_Agent/
│   ├── Reviews/              # 评审记录
│   ├── Bugs/                 # Bug管理
│   ├── MeetingMinutes/       # 会议记录
│   └── README.md
│
├── design/                   # 设计数据
│   └── DesignData/
│       └── README.md
│
├── docs/                     # 文档
│   ├── Arch/                 # 架构文档
│   ├── Design/               # 设计规格
│   ├── FuSa/                 # 功能安全
│   ├── Verification/         # 验证计划
│   │   └── Verification_Plan.md
│   └── README.md
│
├── tools/                    # EDA工具脚本
│   ├── Makefile              # 统一入口
│   ├── README.md
│   ├── cocotb/               # Cocotb仿真
│   ├── ghdl/                 # GHDL仿真
│   ├── iverilog/             # Icarus Verilog仿真
│   └── verilator/            # Verilator仿真
│
├── Verification/             # 验证环境
│   └── README.md
│
├── Temp/                     # 临时文件（不提交git）
│   └── README.md
│
├── .gitignore
└── README.md
```

### 三级目录映射

| 层级 | 目录 | 用途 |
|------|------|------|
| L1 | `ProjectMgmt/` | 项目级管理文档 |
| L2 | `ProjectMgmt/Planning/` | 计划、任务、评审、Bug |
| L3 | `ProjectMgmt/Tasks/Coding_Yang/` | Agent级任务清单 |

---

## EDA工具流程脚本

### 统一Makefile入口

项目实例化后，`tools/Makefile` 由模板 `templates/scripts/Makefile` 提供。

**模板路径**: `sandbox/tools/templates/scripts/Makefile`

**实例化路径**: `project/tools/Makefile`

Makefile 提供以下目标分类：

| 类别 | 目标 | 说明 |
|------|------|------|
| RTL | `rtl`, `sim`, `regression`, `coverage`, `view` | 编译、仿真、回归、覆盖率、波形 |
| Verification | `lint`, `cdc`, `sva`, `formal` | 静态检查、CDC、断言、形式验证 |
| Implementation | `synth`, `synth_opt`, `dft`, `pr`, `sta` | 综合、优化、DFT、物理设计、STA |
| Signoff | `lec`, `drc`, `lvs`, `signoff` | 等价性、DRC、LVS、完整签核 |
| Utility | `info`, `dashboard`, `metrics`, `docs`, `clean` | 信息、仪表板、指标、文档、清理 |
| CI/CD | `ci-lint`, `ci-sim`, `ci-coverage`, `ci-full` | 持续集成目标 |

### 工具链配置

**模板路径**: `sandbox/tools/templates/scripts/config.mk`

配置项包括：
- 开源工具路径（iverilog、verilator、yosys、openroad 等）
- 商业工具路径（VCS、DC、Innovus、PrimeTime 等，需许可证）
- 工艺库配置（PDK_ROOT、STD_CELL_LIB、LEF_FILE 等）
- 设计约束（CLK_PERIOD、CLK_PORT、RESET_PORT、INPUT_DELAY、OUTPUT_DELAY）
- 覆盖率阈值（COVERAGE_LINE_THRESHOLD、COVERAGE_TOGGLE_THRESHOLD 等）

### 各工具链脚本

| 工具 | 模板路径 | 说明 |
|------|---------|------|
| Icarus Verilog | `templates/scripts/iverilog/` | compile.sh、simulate.sh、waveform.sh、Makefile |
| Verilator | `templates/scripts/verilator/` | compile.sh、simulate.sh、lint.sh、Makefile |
| GHDL | `templates/scripts/ghdl/` | compile.sh、elaborate.sh、simulate.sh、waveform.sh、Makefile |
| Cocotb | `templates/scripts/cocotb/` | run.sh、test_{{RTL_TOP}}.py、Makefile |
| Yosys | `templates/scripts/yosys/yosys.mk` | 综合脚本模板 |
| OpenROAD | `templates/scripts/openroad/openroad.mk` | 物理设计脚本模板 |

---

## 模板库

### 模板库结构

所有可复用模板存放于 `sandbox/tools/templates/`：

```
templates/
├── design/                   # 设计模板
│   ├── ip/Module_Name/
│   │   ├── power_intent.upf
│   │   ├── synthesis.sdc
│   │   ├── uart.f
│   │   └── uart_top_template.sv
│   ├── soc/
│   │   ├── system/
│   │   │   └── system_top.sv
│   │   ├── soc_top.f
│   │   └── soc_top_template.sv
│   └── netlist/
│       └── xxx_syn_netlist.v
│
├── docs/                     # 文档模板
│   ├── Arch/
│   │   └── Architecture_Specification_Template.md
│   ├── Module/Module_Name/
│   │   ├── Coverage_Requirements.md
│   │   ├── ModuleName_Design_Specification_Template.md
│   │   └── ModuleName_Verification_Plan_Template.md
│   ├── DFT/
│   │   └── DFT_Spec.md
│   ├── FuSa/
│   │   └── README.md
│   └── Physical/
│       └── README.md
│
├── pm/                       # 项目管理模板
│   ├── bugs/
│   │   ├── Bug_Record_Template.md
│   │   ├── P1_Critical/README.md
│   │   ├── P2_Major/README.md
│   │   ├── P3_Minor/README.md
│   │   ├── P4_Trivial/README.md
│   │   └── README.md
│   ├── changes/README.md
│   ├── dashboard/README.md
│   ├── EDA_Tool_Matrix.md
│   ├── Naming_Conventions_Guide.md
│   ├── dot_gitignore_template
│   ├── reviews/
│   │   ├── ADR_Checklist_PAD.md
│   │   ├── FDR_Checklist.md
│   │   ├── Meeting_Minutes_Template.md
│   │   ├── ModuleName_EDR_Checklist.md
│   │   ├── ModuleName_IDR_Checklist.md
│   │   ├── Phase_Gate_Checklist.md
│   │   ├── Review_Checklist_Template.md
│   │   ├── ADR/README.md
│   │   ├── EDR/Module_Name/README.md
│   │   ├── FDR/Module_Name/README.md
│   │   ├── IDR/Module_Name/README.md
│   │   └── PCD/README.md
│   └── tasks/
│       ├── TASK_IDR_001_RTL_Implementation_Template.md
│       ├── ADR/README.md
│       ├── EDR/README.md
│       ├── FDR/README.md
│       ├── IDR/README.md
│       └── PCD/README.md
│
├── scripts/                  # 脚本模板
│   ├── cocotb/
│   ├── ghdl/
│   ├── iverilog/
│   ├── verilator/
│   ├── yosys/
│   ├── openroad/
│   ├── flow/
│   │   ├── task_workflow.py      # 任务状态自动流转引擎
│   │   └── update_dashboard.py  # Dashboard生成脚本
│   ├── review_bot/
│   │   └── review_bot.py         # 自动化Review检查引擎
│   ├── Makefile
│   ├── README.md
│   ├── config.mk
│   └── install_coding_yang.sh  # Coding Yang Agent安装脚本
│
├── docker/                   # 容器化模板
│   ├── Dockerfile
│   └── docker-compose.yml
│
└── agent/                    # 本地Agent模板
    └── agent.py              # Coding Yang Agent核心代码
```

### 模板使用方式

1. **项目初始化**：从 `templates/` 复制所需模板到项目目录，手动填充 `{{PROJECT_NAME}}`、`{{RTL_TOP}}` 等占位符
2. **文档创建**：从 `templates/docs/` 复制模板到项目 `docs/` 目录，替换 `Module_Name`
3. **脚本复用**：`templates/scripts/` 提供标准化 Makefile 和工具链脚本
4. **Review Checklist**：从 `templates/pm/reviews/` 复制对应阶段的 Checklist

---

## 多Agent协作机制

### Agent角色定义

| Agent | 角色 | 位置 | 核心能力 | 触发关键词 |
|-------|------|------|----------|-----------|
| PM Agent | 项目经理 | 云端 | 计划、排期、报告 | "项目计划"、"里程碑"、"进度" |
| AI Yang | 质量守门员 | 云端 | Review、Checklist、质检 | "review"、"检查"、"质量" |
| Design Agent | 文档编写 | 云端 | Spec、架构、约束 | "design spec"、"sdc"、"upf" |
| Verification Agent | 验证规划 | 云端 | Testplan、Coverage | "验证计划"、"testplan" |
| FuSa Agent | 功能安全 | 云端 | FMEDA、安全分析 | "FMEDA"、"ASIL" |
| Architect | 架构师 | 云端 | 系统/SoC/FuSa/安全架构 | "架构设计"、"SoC架构" |
| **Coding Yang** | RTL实现 | **本地** | RTL开发、Lint、综合 | "Coding Yang 任务:" |
| **Verification Coding Agent** | 验证实现 | **本地** | Case开发、覆盖率、回归 | "Verification Coding Agent 任务:" |
| **Flow Agent** | 物理实现 | **本地** | DFT、STA、PR、Signoff | "Flow Agent 任务:" |

### 任务状态机

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

### 任务JSON协议

任务描述采用标准化 JSON 格式，包含以下字段：

| 字段分组 | 关键字段 | 说明 |
|---------|---------|------|
| 基础信息 | `task_id`, `project_id`, `task_type`, `priority`, `status` | 任务标识与状态 |
| 分配信息 | `assigned_to`, `assigned_by`, `deadline` | 指派与期限 |
| 需求描述 | `title`, `requirements`, `acceptance_criteria` | 任务内容与验收标准 |
| 交付物 | `rtl_files`, `testcases`, `reports` | 预期产出文件路径 |
| 依赖关系 | `pre_tasks`, `post_tasks`, `blocks` | 上下游依赖 |
| 执行信息 | `working_directory`, `commands`, `expected_duration` | 执行环境与命令 |

**模板路径**: `sandbox/tools/templates/pm/tasks/task_template.json`

### 任务自动流转

**模板路径**: `sandbox/tools/templates/scripts/flow/task_workflow.py`

流转规则：
- `pending` → `on_assign` → `assigned`
- `assigned` → `on_start` → `running`（超时未开始则退回 `pending`）
- `running` → `on_submit` → `reviewing`
- `reviewing` → `on_pass` → `completed`（触发下游任务）
- `reviewing` → `on_fail` → `rejected` → `on_rework` → `running`

---

## 项目Dashboard

### Dashboard架构

Dashboard 由 `update_dashboard.py` 自动生成，输出为 Markdown 格式存放于 `ProjectMgmt/Dashboard.md`。

**生成脚本模板路径**: `sandbox/tools/templates/scripts/flow/update_dashboard.py`

**实例化输出路径**: `project/ProjectMgmt/Dashboard.md`

### Dashboard面板

| 面板 | 类型 | 数据来源 |
|------|------|---------|
| Phase Status | 进度条 | `ProjectMgmt/Planning/` 阶段状态 |
| Task Queue | 表格 | `ProjectMgmt/Tasks/` 各Agent任务清单 |
| Agent Status | 网格 | 各Agent当前负载 |
| Quality Metrics | 图表 | `Verification/Coverage/` 覆盖率数据 |
| Alerts | 列表 | 任务逾期、覆盖率不达标等告警 |

### Makefile集成

```bash
# 更新Dashboard
make dashboard
# 收集指标
make metrics
```

---

## Review节点体系

### Review阶段定义

| 阶段 | 全称 | 目的 | 关键交付物 | 模板路径 |
|------|------|------|-----------|---------|
| PCD | Project Concept Definition | 确认项目可行性和商业价值 | MRD、可行性分析 | `templates/pm/reviews/PCD/` |
| PAD | Product Architecture Definition | 冻结架构规格 | Architecture Spec、Safety Concept | `templates/pm/reviews/ADR_Checklist_PAD.md` |
| EDR | Engineering Document Review | 冻结设计文档基线 | Design Spec、Verification Plan、SDC、UPF | `templates/pm/reviews/ModuleName_EDR_Checklist.md` |
| IDR | Implementation Design Review | 确认RTL和验证完成 | RTL、Coverage Report、Lint Report | `templates/pm/reviews/ModuleName_IDR_Checklist.md` |
| FDR | Final Design Review | 确认物理实现完成 | GDS、STA Report、DRC/LVS Report | `templates/pm/reviews/FDR_Checklist.md` |
| PostSilicon | 硅后验证 | 确认芯片功能正确 | ATE程序、验证报告 | `templates/pm/reviews/Review_Checklist_Template.md` |

### Review Checklist模板

各阶段 Checklist 模板位于 `templates/pm/reviews/`，命名规范：
- `ModuleName_EDR_Checklist.md`
- `ModuleName_IDR_Checklist.md`
- `FDR_Checklist.md`
- `ADR_Checklist_PAD.md`
- `Phase_Gate_Checklist.md`
- `Review_Checklist_Template.md`

通用 Checklist 结构包含：
- 基本信息（阶段、项目、日期、结果）
- 参与人员与签名
- 交付物检查清单
- 质量检查（完整性、一致性、可追溯性、质量底线、规范性）
- 问题清单（ID、描述、严重程度、负责人、状态）
- 决策记录与签名

### Review Bot

**模板路径**: `sandbox/tools/templates/scripts/review_bot/review_bot.py`

Review Bot 是自动化检查引擎，作为任务进入 REVIEWING 状态时的第一道质量关卡。

#### 架构定位

```
输入: Task状态变更 → REVIEWING
输出: Review Report (PASS / CONDITIONAL / FAIL)
触发: 自动执行 + AI Yang复核 + 人工确认
```

#### 各阶段检查项

| 阶段 | 检查项 | 类型 |
|------|--------|------|
| PCD | 文件存在性、Markdown格式、必要章节 | 客观检查 |
| PAD | 架构文档存在性、可追溯性 | 客观检查 |
| EDR | Design Spec章节、SDC/UPF存在性 | 客观+结构检查 |
| IDR | RTL存在性、覆盖率阈值、Lint错误、Bug状态 | 客观+数据检查 |
| FDR | GDS存在性、时序收敛、DRC/LVS Clean | 客观+报告解析 |

#### CLI接口

```bash
# 执行指定阶段检查
python3 review_bot.py --stage IDR --project . --task TASK-ID

# 执行所有阶段
python3 review_bot.py --all --project .

# 仅执行特定检查
python3 review_bot.py --stage IDR --checks "LintCheck,CoverageCheck"

# 仅生成报告，不保存
python3 review_bot.py --stage EDR --dry-run
```

#### 集成到 Makefile

```bash
# 提交Review（自动运行Review Bot）
make submit-review STAGE=IDR TASK=TASK-ID

# 各阶段快捷命令
make review-pcd / review-pad / review-edr / review-idr / review-fdr

# Git pre-commit检查
make pre-commit-check
```

#### 报告输出位置

```
ProjectMgmt/Reviews/
├── PCD/
│   ├── REVIEW_PCD_Report.md       # Review Bot生成
│   ├── REVIEW_PCD_Report.json     # 机器可读格式
│   ├── Meeting_Minutes_PCD.md     # 人工会议记录
│   └── CHECKLIST_PCD.md           # 人工复核清单
├── PAD/
├── EDR/
├── IDR/
├── FDR/
└── PostSilicon/
```

#### Review Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                      Review Pipeline                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Review Bot (自动化)                                       │
│     ├── 文件存在性检查                                        │
│     ├── 文档格式/章节检查                                     │
│     ├── 代码覆盖率检查                                        │
│     ├── Lint/CDC检查                                         │
│     ├── 时序/物理验证检查                                     │
│     └── 输出: PASS / CONDITIONAL / FAIL                     │
│                      ↓                                       │
│  2. AI Yang (抽样复核)                                        │
│     ├── 复杂逻辑检查                                          │
│     ├── 架构一致性评估                                        │
│     ├── 风险识别                                              │
│     └── 输出: 批准 / 有条件批准 / 驳回                        │
│                      ↓                                       │
│  3. 实体Yang (最终决策)                                       │
│     ├── 关键决策确认                                          │
│     ├── 资源/schedule权衡                                    │
│     └── 输出: Gate通过 / 延期 / 驳回                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| Agent | 职责 | 处理时间 | 通过率 |
|-------|------|---------|--------|
| **Review Bot** | 自动化客观检查 | < 5分钟 | ~60%基础问题过滤 |
| **AI Yang** | 智能质量评估 | 1-4小时 | 抽样检查关键项 |
| **实体Yang** | 最终批准决策 | 按需 | 战略决策 |

---

## 本地Agent部署

### 部署架构

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

### Docker部署

**Dockerfile模板路径**: `sandbox/tools/templates/docker/Dockerfile`

**docker-compose.yml模板路径**: `sandbox/tools/templates/docker/docker-compose.yml`

容器包含：
- Ubuntu 22.04 基础环境
- Git、Python3、websockets 等基础工具
- 开源EDA工具（iverilog、verilator、yosys、gtkwave）
- Agent核心代码挂载

### 本地Agent代码

**模板路径**: `sandbox/tools/templates/agent/agent.py`

核心功能：
- WebSocket 连接 OpenClaw Gateway
- 自动注册并上报 EDA 工具可用性
- 接收任务分配、执行、回传结果
- 支持 RTL 开发、仿真、Lint、综合等任务类型

### 安装脚本

**模板路径**: `sandbox/tools/templates/scripts/install_coding_yang.sh`

安装步骤：
1. 检查 Docker / Docker Compose 依赖
2. 创建工作目录（默认 `$HOME/workspace`）
3. 生成 `.env` 配置（含随机 Agent Token）
4. 构建 Agent 容器镜像
5. 启动容器

安装后常用命令：
```bash
docker-compose logs -f    # 查看日志
docker-compose stop       # 停止Agent
docker-compose start      # 启动Agent
```

---

## 实施路线图

### 阶段划分

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

### 优先级矩阵

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

### 成功指标

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

### B. 模板路径速查表

| 模板内容 | 路径 |
|---------|------|
| 统一Makefile | `templates/scripts/Makefile` |
| 工具链配置 | `templates/scripts/config.mk` |
| Iverilog仿真 | `templates/scripts/iverilog/` |
| Verilator仿真 | `templates/scripts/verilator/` |
| GHDL仿真 | `templates/scripts/ghdl/` |
| Cocotb仿真 | `templates/scripts/cocotb/` |
| Yosys综合 | `templates/scripts/yosys/yosys.mk` |
| OpenROAD物理设计 | `templates/scripts/openroad/openroad.mk` |
| 任务状态机 | `templates/scripts/flow/task_workflow.py` |
| Dashboard生成 | `templates/scripts/flow/update_dashboard.py` |
| Review Bot | `templates/scripts/review_bot/review_bot.py` |
| Dockerfile | `templates/docker/Dockerfile` |
| Docker Compose | `templates/docker/docker-compose.yml` |
| Agent核心代码 | `templates/agent/agent.py` |
| 安装脚本 | `templates/scripts/install_coding_yang.sh` |
| 架构Spec模板 | `templates/docs/Arch/Architecture_Specification_Template.md` |
| Design Spec模板 | `templates/docs/Module/Module_Name/ModuleName_Design_Specification_Template.md` |
| Verification Plan模板 | `templates/docs/Module/Module_Name/ModuleName_Verification_Plan_Template.md` |
| EDR Checklist | `templates/pm/reviews/ModuleName_EDR_Checklist.md` |
| IDR Checklist | `templates/pm/reviews/ModuleName_IDR_Checklist.md` |
| FDR Checklist | `templates/pm/reviews/FDR_Checklist.md` |
| Bug记录模板 | `templates/pm/bugs/Bug_Record_Template.md` |
| 会议记录模板 | `templates/pm/reviews/Meeting_Minutes_Template.md` |

### C. 参考资源

1. [OpenLANE Documentation](https://openlane.readthedocs.io/)
2. [OpenROAD Flow](https://openroad.readthedocs.io/)
3. [SiliconCompiler Schema](https://docs.siliconcompiler.com/)
4. [ASIC Design Flow (VLSI)](https://yogish.com/blog/vlsi-blog/)

---

*文档版本: v2.0*  
*最后更新: 2025-05-13*  
*作者: AI Yang (Quality Gatekeeper)*
