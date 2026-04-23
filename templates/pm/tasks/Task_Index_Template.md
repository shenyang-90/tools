# {{PROJECT_NAME}} - Agent 任务索引模板

## 项目信息

| 字段 | 值 |
|------|-----|
| **项目ID** | {{PROJECT_ID}} |
| **项目类型** | {{PROJECT_TYPE}} |
| **创建日期** | {{DATE}} |

## 团队任务分配

| Agent | 任务清单 | 主要职责 |
|-------|----------|----------|
| **PM Agent** | [TASK_LIST](./PM_Agent/TASK_LIST.md) | 项目进度管控、Gate评审组织 |
| **AI Yang** | [TASK_LIST](./AI_Yang/TASK_LIST.md) | Gate前质量检查、节点状态总结 |
| **Coding Yang** | [TASK_LIST](./Coding_Yang/TASK_LIST.md) | RTL编码、EDA工具执行、验证执行 |
| **System Architect** | [TASK_LIST](./System_Architect/TASK_LIST.md) | 系统架构设计 (SoC专用) |
| **IP Architect** | [TASK_LIST](./IP_Architect/TASK_LIST.md) | IP架构设计 (IP专用) |
| **Design Agent** | [TASK_LIST](./Design_Agent/TASK_LIST.md) | Design Spec、接口规格、设计策略 |
| **Verification Agent** | [TASK_LIST](./Verification_Agent/TASK_LIST.md) | Verification Plan、测试策略、覆盖率 |
| **DFT Agent** | [TASK_LIST](./DFT_Agent/TASK_LIST.md) | 可测性设计 |
| **FuSa Engineer** | [TASK_LIST](./FuSa_Engineer/TASK_LIST.md) | 功能安全设计 |

## 阶段任务总览

| 阶段 | 主导Agent | 核心交付物 |
|------|----------|-----------|
| PCD | PM Agent | MRD、可行性分析、Master Schedule |
| PAD | System/IP Architect | Architecture Spec、Safety Concept |
| EDR | Design + Verification Agent | Design Spec、Verification Plan、SDC、UPF |
| IDR | Coding Yang | RTL、Coverage Report、Lint Report |
| FDR | Physical Agent / Coding Yang | GDS、STA Report、DRC/LVS Report |

## 任务状态速查

| 状态图标 | 含义 |
|----------|------|
| 🟡 | 待开始/准备中 |
| 🟢 | 进行中 |
| ✅ | 已完成 |
| ⚪ | 未开始 |
| ❌ | 阻塞/问题 |

---
*生成时间: {{DATE}}*
