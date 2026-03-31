# {{PROJECT_NAME}} - Coding Yang 任务清单

> **代码/EDA工具类任务** - 通过 `sandbox/task_queue` 仓库交互

## IDR 阶段任务

| 任务ID | 任务名称 | 交付物 | 状态 | 优先级 |
|--------|----------|--------|------|--------|
| CODE-{{PROJECT_ID}}-001 | RTL模块编码 | `rtl/*.v` | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-002 | Lint/CDC检查 | Lint_Clean_Report | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-003 | UVM环境搭建 | `tb/*.sv` | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-004 | Testcase开发 | `testcases/*.sv` | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-005 | 验证运行 | 仿真日志/波形 | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-006 | 覆盖率收敛 | 覆盖率报告 | ⚪ 未开始 | P0 |

## FDR 阶段任务

| 任务ID | 任务名称 | 交付物 | 状态 | 优先级 |
|--------|----------|--------|------|--------|
| CODE-{{PROJECT_ID}}-007 | 逻辑综合 | 网表/SDC | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-008 | LEC验证 | LEC报告 | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-009 | STA分析 | 时序报告 | ⚪ 未开始 | P0 |
| CODE-{{PROJECT_ID}}-010 | ATPG生成 | 测试向量 | ⚪ 未开始 | P0 |

## 覆盖率目标

| 类型 | 目标 | 任务ID |
|------|------|--------|
| Code Coverage | >90% | CODE-{{PROJECT_ID}}-011 |
| Function Coverage | >85% | CODE-{{PROJECT_ID}}-012 |
| Assertion Coverage | >95% | CODE-{{PROJECT_ID}}-013 |

## 任务交互方式

```
PM Agent 创建 task → 推送到 sandbox/task_queue 仓库
                           ↓
              Coding Yang git pull 获取任务
                           ↓
                    执行编码/EDA任务
                           ↓
              git commit -m "[TASK-XXX] description"
                           ↓
                    git push origin main
                           ↓
              更新 task_queue 状态为 COMPLETED
                           ↓
                    AI Yang 质量检查
```

---
*生成时间: {{DATE}}*
