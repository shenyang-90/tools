# {{PROJECT_NAME}}

## 项目概览

| 字段 | 内容 |
|------|------|
| **项目ID** | {{PROJECT_ID}} |
| **项目类型** | {{PROJECT_TYPE}} |
| **工艺节点** | {{PROCESS_NODE}} |
| **ASIL等级** | {{ASIL_LEVEL}} |
| **项目经理** | {{PM_NAME}} |
| **创建日期** | {{DATE}} |

## 项目阶段

```
PCD ──────→ PAD ──────→ EDR ──────→ IDR ──────→ FDR ──────→ Post Silicon
概念阶段    架构阶段    文档阶段    实现阶段    后端阶段      硅后阶段

当前阶段: [████░░░░░░░░░░░░░░░░] PCD (0%)
```

## 快速导航

### 项目管理 (ProjectMgmt/)
- [Planning](./ProjectMgmt/Planning/) - 项目计划、Schedule
- [Reviews](./ProjectMgmt/Reviews/) - 阶段评审记录
- [Bugs](./ProjectMgmt/Bugs/) - Bug跟踪
- [MeetingMinutes](./ProjectMgmt/MeetingMinutes/) - 会议记录
- [Milestones](./ProjectMgmt/Milestones/) - 阶段交付物
- [RiskMgmt](./ProjectMgmt/RiskMgmt/) - 风险管理
- [ChangeMgmt](./ProjectMgmt/ChangeMgmt/) - ECO/CR记录
- [StatusReports](./ProjectMgmt/StatusReports/) - 周报月报

### 设计数据 (Database/)
- [Docs](./Database/Docs/) - 设计文档
- [DesignData](./Database/DesignData/) - RTL/Netlist/GDS
- [Verification](./Database/Verification/) - 验证环境
- [Validation](./Database/Validation/) - FPGA/硅后验证
- [Firmware](./Database/Firmware/) - 固件代码
- [Scripts](./Database/Scripts/) - EDA脚本
- [Reference](./Database/Reference/) - 参考资料
- [ToolConfig](./Database/ToolConfig/) - 工具配置

## 质量门禁

- [ ] **PCD Gate** - 项目概念评审
- [ ] **PAD Gate** - 架构设计评审 (ADR)
- [ ] **EDR Gate** - 工程文档评审
- [ ] **IDR Gate** - 代码冻结评审
- [ ] **FDR Gate** - 最终设计评审 (Tapeout)
- [ ] **Post Silicon Gate** - 量产评审

## 团队角色

| 角色 | Agent | 状态 |
|------|-------|------|
| 质量守门员 | AI Yang | 🟢 待命 |
| 项目经理 | {{PM_NAME}} | 🟢 活跃 |
| 系统架构师 | System Architect | ⚪ 待分配 |
| 设计工程师 | Design Agent | ⚪ 待分配 |
| 验证工程师 | Verification Agent | ⚪ 待分配 |
| DFT工程师 | DFT Agent | ⚪ 待分配 |
| 后端工程师 | Physical Agent | ⚪ 待分配 |

## 项目统计

| 类型 | 数量 |
|------|------|
| **任务** | [查看 ProjectMgmt/Planning/](./ProjectMgmt/Planning/)
| **Bug** | [查看 ProjectMgmt/Bugs/](./ProjectMgmt/Bugs/)
| **Review** | [查看 ProjectMgmt/Reviews/](./ProjectMgmt/Reviews/)

## 最近活动

| 日期 | 活动 | 负责人 |
|------|------|--------|
| {{DATE}} | 项目初始化 | {{PM_NAME}} |

## 重要链接

- [Master Schedule](./ProjectMgmt/Planning/Master_Schedule.md)
- [项目计划模板](./ProjectMgmt/Planning/TEMPLATE_Schedule.md)
- [SOC_DESIGN_WORKFLOW.md](../../../workflow/SOC_DESIGN_WORKFLOW.md)

---

*项目模板版本: v2.0*  
*最后更新: {{DATE}}*
