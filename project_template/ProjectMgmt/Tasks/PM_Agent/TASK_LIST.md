# {{PROJECT_NAME}} - PM Agent 任务清单

## 项目信息管理

| 任务ID | 任务名称 | 阶段 | 状态 | 优先级 |
|--------|----------|------|------|--------|
| PM-{{PROJECT_ID}}-001 | 创建项目结构 | Setup | 🟡 待开始 | P0 |
| PM-{{PROJECT_ID}}-002 | 制定Master Schedule | PCD | ⚪ 未开始 | P0 |
| PM-{{PROJECT_ID}}-003 | 资源规划 | PAD | ⚪ 未开始 | P1 |
| PM-{{PROJECT_ID}}-004 | 风险管理计划 | PAD | ⚪ 未开始 | P1 |
| PM-{{PROJECT_ID}}-005 | 组织PCD Review | PCD | ⚪ 未开始 | P0 |
| PM-{{PROJECT_ID}}-006 | 组织PAD Review | PAD | ⚪ 未开始 | P0 |
| PM-{{PROJECT_ID}}-007 | 组织EDR Review | EDR | ⚪ 未开始 | P0 |
| PM-{{PROJECT_ID}}-008 | 组织IDR Review | IDR | ⚪ 未开始 | P0 |
| PM-{{PROJECT_ID}}-009 | 组织FDR Review | FDR | ⚪ 未开始 | P0 |
| PM-{{PROJECT_ID}}-010 | 项目周报 | 全程 | ⚪ 未开始 | P1 |
| PM-{{PROJECT_ID}}-011 | 项目月报 | 全程 | ⚪ 未开始 | P1 |

---

## 📋 各阶段文档状态检查

PM Agent 必须在每个节点检查所有文档状态，确保与当前节点匹配。

### Phase 1: PCD (Project Concept Definition)

**检查任务**: PM-{{PROJECT_ID}}-101

| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| MRD | `ProjectMgmt/Planning/MRD.md` | 已批准 | ❓ | ⬜ |
| 可行性分析 | `ProjectMgmt/Planning/Feasibility_Study.md` | 已完成 | ❓ | ⬜ |
| 项目计划 | `ProjectMgmt/Planning/Master_Schedule.md` | 初版 | ❓ | ⬜ |

**检查结论**: ⬜ 通过 / ⬜ 不通过  
**问题记录**: 

### Phase 2: PAD (Product Architecture Definition)

**检查任务**: PM-{{PROJECT_ID}}-102

| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Architecture Spec | `Database/Docs/Arch/Architecture_Spec.md` | v1.0已冻结 | ❓ | ⬜ |
| Interface Spec | `Database/Docs/Arch/Interface_Specification.md` | v1.0已冻结 | ❓ | ⬜ |
| Safety Concept | `Database/Docs/FuSa/Safety_Concept.md` | v1.0已冻结 | ❓ | ⬜ |
| FMEDA初版 | `Database/Docs/FuSa/FMEDA_Preliminary.xlsx` | 已完成 | ❓ | ⬜ |
| PPA目标 | `Database/Docs/Arch/PPA_Target.md` | 已批准 | ❓ | ⬜ |
| 资源规划 | `ProjectMgmt/Planning/Resource_Plan.md` | 已批准 | ❓ | ⬜ |
| 风险管理计划 | `ProjectMgmt/RiskMgmt/Risk_Management_Plan.md` | 已批准 | ❓ | ⬜ |
| PAD Review Checklist | `ProjectMgmt/Reviews/PAD/PAD_Review_Checklist.md` | **已更新** | ❓ | ⬜ |

**前置条件检查**:
- [ ] AI Yang质量检查通过
- [ ] PAD Review Checklist **已在会议前更新**

**检查结论**: ⬜ 通过 / ⬜ 有条件通过 / ⬜ 不通过  
**遗留问题**: 

### Phase 3: EDR (Engineering Document Review)

**检查任务**: PM-{{PROJECT_ID}}-103

| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Design Spec | `Database/Docs/Design/Design_Specification.md` | v1.0已冻结 | ❓ | ⬜ |
| Verification Plan | `Database/Docs/Verification/Verification_Plan.md` | v1.0已冻结 | ❓ | ⬜ |
| Interface Spec | `Database/Docs/Design/Interface_Spec.md` | v1.0已冻结 | ❓ | ⬜ |
| CDC/RDC Strategy | `Database/Docs/Design/CDC_RDC_Strategy.md` | 已完成 | ❓ | ⬜ |
| Low Power Design | `Database/Docs/Design/Low_Power_Design.md` | 已完成 | ❓ | ⬜ |
| DFT Spec | `Database/Docs/DFT/DFT_Specification.md` | 初版 | ❓ | ⬜ |
| EDR Review Checklist | `ProjectMgmt/Reviews/EDR/EDR_Review_Checklist.md` | **已更新** | ❓ | ⬜ |

**前置条件检查**:
- [ ] Design Spec ↔ Verification Plan 一致性检查通过
- [ ] AI Yang质量检查通过
- [ ] EDR Review Checklist **已在会议前更新** ⭐

**检查结论**: ⬜ 通过 / ⬜ 有条件通过 / ⬜ 不通过  
**遗留问题**: 

### Phase 4: IDR (Implementation Design Review)

**检查任务**: PM-{{PROJECT_ID}}-104

| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| RTL Code | `Database/DesignData/rtl/` | Code Freeze | ❓ | ⬜ |
| Lint Clean报告 | `Database/DesignData/reports/lint_report.md` | 无Critical/Major | ❓ | ⬜ |
| CDC Clean报告 | `Database/DesignData/reports/cdc_report.md` | 已清理 | ❓ | ⬜ |
| UVM环境 | `Database/Verification/uvm/` | 已完成 | ❓ | ⬜ |
| Testcases | `Database/Verification/testcases/` | >95%通过 | ❓ | ⬜ |
| 覆盖率报告 | `Database/Verification/reports/coverage_report.md` | Code>90%, Func>85% | ❓ | ⬜ |
| 回归测试报告 | `Database/Verification/reports/regression_report.md` | 2周100%通过 | ❓ | ⬜ |
| FMEDA报告 | `Database/Docs/FuSa/FMEDA_Report.xlsx` | SPFM>99%, LFM>90% | ❓ | ⬜ |
| 故障注入报告 | `Database/Docs/FuSa/Fault_Injection_Report.md` | 已完成 | ❓ | ⬜ |
| Bug清单 | `ProjectMgmt/Bugs/Bug_Tracking.md` | P1/P2关闭 | ❓ | ⬜ |
| IDR Review Checklist | `ProjectMgmt/Reviews/IDR/IDR_Review_Checklist.md` | **已更新** | ❓ | ⬜ |

**前置条件检查**:
- [ ] 覆盖率达标 (Code>90%, Func>85%, Assert>95%)
- [ ] Bug清理完成 (P1/P2关闭)
- [ ] 回归测试稳定 (连续2周100%通过)
- [ ] AI Yang质量检查通过
- [ ] IDR Review Checklist **已在会议前更新** ⭐

**检查结论**: ⬜ 通过 / ⬜ 有条件通过 / ⬜ 不通过  
**遗留问题**: 

### Phase 5: FDR (Final Design Review) - SoC Only

**检查任务**: PM-{{PROJECT_ID}}-105 ({{PROJECT_TYPE}} = SoC)

| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 综合网表 | `Database/DesignData/netlist/` | 已冻结 | ❓ | ⬜ |
| SDC约束 | `Database/DesignData/constraints/` | 已Sign-off | ❓ | ⬜ |
| LEC报告 | `Database/DesignData/reports/lec_report.md` | 通过 | ❓ | ⬜ |
| STA报告 | `Database/DesignData/reports/sta_report.md` | 时序收敛 | ❓ | ⬜ |
| DFT报告 | `Database/DFT/dft_report.md` | 覆盖率达标 | ❓ | ⬜ |
| ATPG向量 | `Database/DFT/atpg_patterns/` | 已生成 | ❓ | ⬜ |
| GDS | `Database/DesignData/gds/` | 已冻结 | ❓ | ⬜ |
| DRC/LVS报告 | `Database/DesignData/reports/physical_verification.md` | 通过 | ❓ | ⬜ |
| Tapeout检查表 | `ProjectMgmt/Reviews/FDR/Tapeout_Checklist.md` | 已完成 | ❓ | ⬜ |
| FDR Review Checklist | `ProjectMgmt/Reviews/FDR/FDR_Review_Checklist.md` | **已更新** | ❓ | ⬜ |

**前置条件检查**:
- [ ] 物理实现完成
- [ ] 时序收敛
- [ ] AI Yang质量检查通过
- [ ] FDR Review Checklist **已在会议前更新** ⭐

**检查结论**: ⬜ 通过 / ⬜ 不通过  
**遗留问题**: 

---

## 🔍 文档一致性检查流程

### 检查时机
**每个Gate前必须执行**: PM Agent 文档状态检查

### 检查内容
1. **文档存在性**: 所有期望文档是否已创建
2. **版本状态**: 文档版本是否与当前阶段匹配
3. **内容一致性**: 跨文档引用是否一致
4. **Checklist状态**: Review Checklist 是否已更新

### 检查流程
```
PM Agent 准备 Gate Review
        ↓
  执行文档状态检查 (本清单)
        ↓
  ┌─────┴─────┐
  ▼           ▼
全部匹配     发现不匹配
  ↓           ↓
通知AI Yang  记录问题
质量检查     要求责任人修复
  ↓           ↓
组织Review  重新检查
```

### 不匹配处理
| 严重程度 | 处理方式 | 决策权 |
|----------|----------|--------|
| Critical | 阻塞Gate，必须修复 | PM Agent |
| Major | 可遗留，需记录并跟踪 | PM Agent + 实体Yang |
| Minor | 可遗留，限期修复 | PM Agent |

---

## 📊 文档追踪矩阵

| 文档类型 | PCD | PAD | EDR | IDR | FDR |
|----------|-----|-----|-----|-----|-----|
| MRD | ✅ | ✅ | ✅ | ✅ | ✅ |
| Architecture Spec | ⬜ | ✅ | ✅ | ✅ | ✅ |
| Design Spec | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| Verification Plan | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| RTL Code | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| Testbench | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| 覆盖率报告 | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| 综合网表 | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| GDS | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |

---

## 🚨 关键提醒

> **Checklist 必须在 Review 会议前更新完成!**
> 
> 历史教训: EDR阶段Checklist在会议后更新，导致流程偏差。
> 
> 正确流程:
> ```
> 文档完成 → AI Yang检查 → 更新Checklist → Review Meeting → Gate决策
> ```

---

*生成时间: {{DATE}}*
