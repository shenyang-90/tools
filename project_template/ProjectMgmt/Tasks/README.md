# {{PROJECT_NAME}} - 全局任务索引

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
| **Coding Yang** | [TASK_LIST](./Coding_Yang/TASK_LIST.md) | RTL编码、EDA工具执行、验证 |
{{#SOC_TYPE}}
| **System Architect** | [TASK_LIST](./System_Architect/TASK_LIST.md) | 系统架构设计 (SoC专用) |
{{/SOC_TYPE}}
{{#IP_TYPE}}
| **IP Architect** | [TASK_LIST](./IP_Architect/TASK_LIST.md) | IP架构设计 (IP专用) |
{{/IP_TYPE}}
| **Design Agent** | [TASK_LIST](./Design_Agent/TASK_LIST.md) | Design Spec文档 (AI-Yang执行) |
| **Verification Agent** | [TASK_LIST](./Verification_Agent/TASK_LIST.md) | Verification Plan文档 (AI-Yang执行) |
| **DFT Agent** | [TASK_LIST](./DFT_Agent/TASK_LIST.md) | 可测性设计 |
| **FuSa Engineer** | [TASK_LIST](./FuSa_Engineer/TASK_LIST.md) | 功能安全设计 |

## 阶段任务总览

### Phase 1: PCD (Project Concept Definition)
- **目标**: 完成项目概念定义，确认可行性
- **主导**: PM Agent
- **任务**: PM-{{PROJECT_ID}}-001/002/005

### Phase 2: PAD (Product Architecture Definition)
- **目标**: 完成架构设计，冻结架构规格
- **主导**: {{#SOC_TYPE}}System Architect{{/SOC_TYPE}}{{#IP_TYPE}}IP Architect{{/IP_TYPE}}
- **任务**: ARCH-{{PROJECT_ID}}-*/IPARCH-{{PROJECT_ID}}-*

### Phase 3: EDR (Engineering Document Review)
- **目标**: 完成设计/验证文档，冻结文档基线
- **主导**: Design Agent + Verification Agent (AI-Yang执行)
- **任务**: DESIGN-{{PROJECT_ID}}-*/VER-{{PROJECT_ID}}-*

### Phase 4: IDR (Implementation Design Review)
- **目标**: 完成RTL和验证，Code Freeze
- **主导**: Coding Yang
- **任务**: CODE-{{PROJECT_ID}}-001~006

### Phase 5: FDR (Final Design Review) - SoC Only
- **目标**: 完成物理实现，Tapeout
- **主导**: Physical Agent (SoC) / Coding Yang (IP)
- **任务**: CODE-{{PROJECT_ID}}-007~010

---

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
*模板版本: v1.0*
