# {{PROJECT_NAME}} - Design Agent 任务清单

> **Design Agent 负责执行**

## 职责范围
- Design Specification 编写
- 接口规格定义
- CDC/RDC 策略制定
- 低功耗设计策略
- DFT Specification
- Floorplan 指南

## EDR 阶段任务

| 任务ID | 任务名称 | 交付物 | 状态 | 优先级 |
|--------|----------|--------|------|--------|
| DESIGN-{{PROJECT_ID}}-001 | Design Specification | Design_Spec.md (8章节) | ⚪ 未开始 | P0 |
| DESIGN-{{PROJECT_ID}}-002 | 接口规格书 | Interface_Spec.md | ⚪ 未开始 | P0 |
| DESIGN-{{PROJECT_ID}}-003 | CDC/RDC策略 | CDC_RDC_Strategy.md | ⚪ 未开始 | P1 |
| DESIGN-{{PROJECT_ID}}-004 | 低功耗设计策略 | Low_Power_Design.md | ⚪ 未开始 | P1 |
| DESIGN-{{PROJECT_ID}}-005 | DFT Specification | DFT_Spec.md | ⚪ 未开始 | P2 |
| DESIGN-{{PROJECT_ID}}-006 | Floorplan指南 | Floorplan_Guide.md | ⚪ 未开始 | P2 |

## 设计文档8章节

| 章节 | 任务ID | 内容 | 状态 |
|------|--------|------|------|
| 1 | DESIGN-{{PROJECT_ID}}-001-1 | Overview | ⚪ 未开始 |
| 2 | DESIGN-{{PROJECT_ID}}-001-2 | Function Descriptions | ⚪ 未开始 |
| 3 | DESIGN-{{PROJECT_ID}}-001-3 | Register Descriptions | ⚪ 未开始 |
| 4 | DESIGN-{{PROJECT_ID}}-001-4 | Example | ⚪ 未开始 |
| 5 | DESIGN-{{PROJECT_ID}}-001-5 | Block Design | ⚪ 未开始 |
| 6 | DESIGN-{{PROJECT_ID}}-001-6 | FSM | ⚪ 未开始 |
| 7 | DESIGN-{{PROJECT_ID}}-001-7 | Low Power | ⚪ 未开始 |
| 8 | DESIGN-{{PROJECT_ID}}-001-8 | Patent | ⚪ 未开始 |

## 交付标准

### Design Spec 质量要求
- 所有章节完整，无占位符
- 寄存器定义精确到 bit 级别
- 接口时序图清晰
- 与其他文档交叉引用一致

### 评审流程
```
Design Agent 完成文档
        ↓
PM Agent 通知 AI Yang
        ↓
AI Yang 质量检查
        ↓
  ┌─────┴─────┐
  ▼           ▼
通过        不通过
  ↓           ↓
冻结版本    返回修改
```

---
*生成时间: {{DATE}}*
*执行方: Design Agent*
