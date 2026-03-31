# {{PROJECT_NAME}} - AI Yang 任务清单

> **质量守门员** - 所有 Gate 前的质量检查 (不直接执行文档编写)

## 质量检查任务

| 任务ID | 任务名称 | 检查内容 | 阶段 | 状态 |
|--------|----------|----------|------|------|
| AI-{{PROJECT_ID}}-001 | PCD Gate质量检查 | 完整性/可行性 | PCD | ⚪ 未开始 |
| AI-{{PROJECT_ID}}-002 | PAD Gate质量检查 | 架构/安全概念 | PAD | ⚪ 未开始 |
| AI-{{PROJECT_ID}}-003 | EDR Gate质量检查 | 设计文档/验证计划 | EDR | ⚪ 未开始 |
| AI-{{PROJECT_ID}}-004 | IDR Gate质量检查 | RTL/覆盖率/安全 | IDR | ⚪ 未开始 |
| AI-{{PROJECT_ID}}-005 | FDR Gate质量检查 | 物理实现/时序 | FDR | ⚪ 未开始 |

## 检查清单 (Checklist)

### 通用检查项

| 检查维度 | 检查内容 | 任务ID |
|----------|----------|--------|
| 完整性 | 所有交付物存在且非空 | AI-{{PROJECT_ID}}-006 |
| 一致性 | 交付物间无矛盾 | AI-{{PROJECT_ID}}-007 |
| 可追溯性 | 需求→设计→验证链路完整 | AI-{{PROJECT_ID}}-008 |
| 质量底线 | 无明显缺陷/错误 | AI-{{PROJECT_ID}}-009 |
| 规范性 | 符合 workflow 定义 | AI-{{PROJECT_ID}}-010 |

## 检查对象

### EDR 阶段检查
| 交付物 | 编写者 | AI Yang 检查项 |
|--------|--------|----------------|
| Design Spec | **Design Agent** | 8章节完整性、寄存器定义、一致性 |
| Verification Plan | **Verification Agent** | 7章节完整性、覆盖率计划、与Spec对应 |
| Interface Spec | Design Agent | 接口定义准确性 |
| CDC/RDC Strategy | Design Agent | 策略合理性 |

### IDR 阶段检查
| 交付物 | 编写者 | AI Yang 检查项 |
|--------|--------|----------------|
| RTL Code | **Coding Yang** | 代码质量、Lint清理、CDC合规 |
| UVM环境 | Coding Yang | 环境完整性、可运行性 |
| 覆盖率报告 | Coding Yang | Code>90%, Func>85%, Assert>95% |
| 测试用例 | Coding Yang | 与 Verification Plan 对应 |

## 输出模板

### 节点状态总结
```markdown
## 节点状态总结: [阶段名]

### 检查结果
- **交付物完整性**: ✅ / ❌
- **内部一致性**: ✅ / ❌
- **质量评估**: 高 / 中 / 低

### 发现的问题
| 问题 | 严重程度 | 状态 | 备注 |
|------|---------|------|------|
| ... | Critical/Major/Minor | 已修复/待修复 | |

### 建议
- **推荐决策**: 通过 / 有条件通过 / 不通过
- **实体 Yang 需重点检查**: [列出关键交付物]
```

## 工作流程

```
Design/Verification Agent 完成文档
              ↓
      PM Agent 通知 AI Yang
              ↓
        AI Yang 质量检查
              ↓
        ┌─────┴─────┐
        ▼           ▼
      通过        不通过
        ↓           ↓
    生成总结    反馈修改意见
        ↓           ↓
    提交实体Yang  返回Agent修改
```

---
*生成时间: {{DATE}}*
*角色: 质量守门员 (不直接编写文档)*
