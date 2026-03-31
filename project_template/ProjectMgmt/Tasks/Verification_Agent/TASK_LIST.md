# {{PROJECT_NAME}} - Verification Agent 任务清单

> **Verification Agent 负责执行**

## 职责范围
- Verification Plan 编写
- Testbench 架构设计
- 测试策略制定
- 覆盖率计划
- 参考模型设计
- 验证环境搭建指导

## EDR 阶段任务

| 任务ID | 任务名称 | 交付物 | 状态 | 优先级 |
|--------|----------|--------|------|--------|
| VER-{{PROJECT_ID}}-001 | Verification Plan | Verification_Plan.md (7章节) | ⚪ 未开始 | P0 |
| VER-{{PROJECT_ID}}-002 | Testbench架构 | TB_Architecture.md | ⚪ 未开始 | P0 |
| VER-{{PROJECT_ID}}-003 | 测试策略 | Test_Strategy.md | ⚪ 未开始 | P0 |
| VER-{{PROJECT_ID}}-004 | 覆盖率计划 | Coverage_Plan.md | ⚪ 未开始 | P0 |
| VER-{{PROJECT_ID}}-005 | 参考模型设计 | Ref_Model_Design.md | ⚪ 未开始 | P1 |

## 验证文档7章节

| 章节 | 任务ID | 内容 | 状态 |
|------|--------|------|------|
| 1 | VER-{{PROJECT_ID}}-001-1 | Overview | ⚪ 未开始 |
| 2 | VER-{{PROJECT_ID}}-001-2 | Testbench Architecture | ⚪ 未开始 |
| 3 | VER-{{PROJECT_ID}}-001-3 | Test Strategy | ⚪ 未开始 |
| 4 | VER-{{PROJECT_ID}}-001-4 | Test Cases | ⚪ 未开始 |
| 5 | VER-{{PROJECT_ID}}-001-5 | Coverage Plan | ⚪ 未开始 |
| 6 | VER-{{PROJECT_ID}}-001-6 | Regression Plan | ⚪ 未开始 |
| 7 | VER-{{PROJECT_ID}}-001-7 | Safety Verification | ⚪ 未开始 |

## 覆盖率目标

| 类型 | 目标 | 任务ID |
|------|------|--------|
| Code Coverage | >90% | VER-{{PROJECT_ID}}-006 |
| Function Coverage | >85% | VER-{{PROJECT_ID}}-007 |
| Assertion Coverage | >95% | VER-{{PROJECT_ID}}-008 |

## 交付标准

### Verification Plan 质量要求
- 验证策略与 Design Spec 对应
- 测试用例覆盖所有功能点
- 覆盖率目标明确且可测量
- 参考模型算法正确

### 评审流程
```
Verification Agent 完成文档
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

### 与 Design Agent 协作
- 验证计划必须基于 Design Spec 编写
- 接口理解不一致时，与 Design Agent 对齐
- 覆盖率的 Function Point 来自 Design Spec 的功能描述

---
*生成时间: {{DATE}}*
*执行方: Verification Agent*
