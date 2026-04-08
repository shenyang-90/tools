# Design Flow Optimization Plan

## 目录

1. [总体架构](./Design_Flow_Optimization_Plan.md#1-总体架构)
2. [Agent角色定义](./Design_Flow_optimization_Plan.md#2-agent角色定义)
3. [目录结构规范](./Design_Flow_optimization_Plan.md#3-目录结构规范)
4. [模板规范](./Design_Flow_optimization_Plan.md#4-模板规范)
5. [Agent通信协议与任务管理](./Design_Flow_optimization_Plan.md#5-agent通信协议与任务管理)
6. [项目Dashboard](./Design_Flow_optimization_Plan.md#6-项目dashboard)
7. [Review节点体系](./Design_Flow_optimization_Plan.md#7-review节点体系)
8. [实施路线图](./Design_Flow_optimization_Plan.md#8-实施路线图)
9. [工具集成](./Design_Flow_optimization_Plan.md#9-工具集成)

## 文件清单

### 文档
- `Design_Flow_Optimization_Plan.md` - 主文档
- `README.md` - 本文件

### 脚本
- `Scripts/common/review_bot.py` - Review Bot 自动化检查引擎
- `Scripts/Makefile` - 统一 EDA 工具入口

### 模板

#### RTL 模板
- `templates/rtl/soc_top_template.sv` - SoC Top 模板（含版本历史 header）
- `templates/rtl/uart_top_template.sv` - IP (UART) 模板（含版本历史 header）
- `templates/rtl/soc_top.f` - SoC 顶层 filelist 模板
- `templates/rtl/uart.f` - IP filelist 模板

#### 文档模板
- `templates/docs/Architecture_Specification_Template.md` - 架构规格说明书模板（含 History 章节）
- `templates/docs/Design_Specification_Template.md` - 设计规格说明书模板（含 History 章节）
- `templates/docs/Verification_Plan_Template.md` - 验证计划模板（含 History 章节）
- `templates/docs/synthesis.sdc` - SDC 约束模板
- `templates/docs/power_intent.upf` - UPF 功耗意图模板

#### 任务模板
- `templates/tasks/TASK_IDR_001_RTL_Implementation_Template.md` - 任务模板示例

#### Review 模板
- `templates/reviews/Review_Checklist_Template.md` - Review 检查清单模板
- `templates/reviews/Meeting_Minutes_Template.md` - 评审会议记录模板
- `templates/reviews/ADR_Checklist_PAD.md` - PAD阶段架构设计评审Checklist
- `templates/reviews/ModuleName_EDR_Checklist.md` - EDR阶段文档评审Checklist
- `templates/reviews/ModuleName_IDR_Checklist.md` - IDR阶段模块级评审Checklist (42项)
- `templates/reviews/FDR_Checklist.md` - FDR阶段Tapeout前评审Checklist
- `templates/reviews/Phase_Gate_Checklist.md` - 六阶段模型门禁汇总

#### 项目管理模板
- `templates/project_mgmt/Bug_Record_Template.md` - Bug记录模板
- `templates/project_mgmt/dot_gitignore_template` - 项目.gitignore模板
- `templates/project_mgmt/Naming_Conventions_Guide.md` - 文件命名规范指南
- `templates/project_mgmt/EDA_Tool_Matrix.md` - EDA工具矩阵参考

#### 验证规范模板
- `templates/verification/Coverage_Requirements.md` - 覆盖率要求规范

## 快速开始

### 1. 创建新项目
```bash
cd Scripts
make init
```

### 2. 提交 Review
```bash
cd Scripts
make submit-review STAGE=IDR TASK=TASK-XXX-001
```

### 3. 运行 Review Bot
```bash
python3 Scripts/common/review_bot.py --stage IDR --project .
```

### 4. 更新 Dashboard
```bash
cd Scripts
make dashboard
```

## Agent 角色速查

| Agent | 主要职责 | 工作目录 |
|-------|----------|----------|
| PM Agent | 项目管理、任务分配 | ProjectMgmt/ |
| Architect | 架构设计、技术决策 | Docs/Arch/ |
| Design Agent | 模块设计、规格定义 | Docs/Design/ |
| Design_Coding_Agent | RTL 开发、LINT | Design/RTL/ |
| Verification_Coding_Agent | 验证环境、用例 | Verification/ |
| Flow_Agent | DFT、STA、PR | Design/DFT/, Design/STA/ |
| FuSa Agent | 安全分析、FMEDA | Docs/FuSa/ |

## 版本记录

| 版本 | 日期 | 作者 | 变更 |
|------|------|------|------|
| v0.1.0 | 2026-04-03 | AI Yang | 初始版本 |
