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

#### 1.1 项目基础文档
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| README | `README.md` | 已创建 | ❓ | ⬜ |
| MRD | `ProjectMgmt/Planning/MRD.md` | 已批准 | ❓ | ⬜ |
| 可行性分析 | `ProjectMgmt/Planning/Feasibility_Study.md` | 已完成 | ❓ | ⬜ |
| Master Schedule | `ProjectMgmt/Planning/Master_Schedule.md` | 初版 | ❓ | ⬜ |

#### 1.2 Review & Checklist
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| PCD Review Checklist | `ProjectMgmt/Reviews/PCD/PCD_Review_Checklist.md` | **已更新** | ❓ | ⬜ |
| PCD Review Minutes | `ProjectMgmt/Reviews/PCD/PCD_Review_Meeting_YYYYMMDD.md` | 待创建 | ❓ | ⬜ |

#### 1.3 风险与状态
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 风险登记册 | `ProjectMgmt/RiskMgmt/Risk_Register.md` | 初版 | ❓ | ⬜ |
| 项目周报 | `ProjectMgmt/StatusReports/Weekly_Report_Week1.md` | 已发布 | ❓ | ⬜ |

**前置条件检查**:
- [ ] 所有基础文档已创建且非空
- [ ] PCD Review Checklist **已在会议前更新**

**检查结论**: ⬜ 通过 / ⬜ 有条件通过 / ⬜ 不通过  
**问题记录**: 

---

### Phase 2: PAD (Product Architecture Definition)

**检查任务**: PM-{{PROJECT_ID}}-102

#### 2.1 架构文档
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Architecture Spec | `Database/Docs/Arch/Architecture_Spec.md` | v1.0已冻结 | ❓ | ⬜ |
| Interface Spec | `Database/Docs/Arch/Interface_Specification.md` | v1.0已冻结 | ❓ | ⬜ |
| PPA目标 | `Database/Docs/Arch/PPA_Target.md` | 已批准 | ❓ | ⬜ |
| Micro Arch | `Database/Docs/Arch/Micro_Architecture.md` | 已完成 | ❓ | ⬜ |

#### 2.2 功能安全文档
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Safety Concept | `Database/Docs/FuSa/Safety_Concept.md` | v1.0已冻结 | ❓ | ⬜ |
| FMEDA初版 | `Database/Docs/FuSa/FMEDA_Preliminary.xlsx` | 已完成 | ❓ | ⬜ |

#### 2.3 项目管理文档
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 资源规划 | `ProjectMgmt/Planning/Resource_Plan.md` | 已批准 | ❓ | ⬜ |
| 风险管理计划 | `ProjectMgmt/RiskMgmt/Risk_Management_Plan.md` | 已批准 | ❓ | ⬜ |
| Milestone Plan | `ProjectMgmt/Planning/Milestone_Plan.md` | 已批准 | ❓ | ⬜ |
| Task Assignment | `ProjectMgmt/Planning/Task_Assignment.md` | 已创建 | ❓ | ⬜ |

#### 2.4 Agent 任务清单
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| System/IP Architect Tasks | `ProjectMgmt/Tasks/System_Architect/TASK_LIST.md` | 已更新 | ❓ | ⬜ |
| Design Agent Tasks | `ProjectMgmt/Tasks/Design_Agent/TASK_LIST.md` | 已创建 | ❓ | ⬜ |
| Verification Agent Tasks | `ProjectMgmt/Tasks/Verification_Agent/TASK_LIST.md` | 已创建 | ❓ | ⬜ |

#### 2.5 Review & Checklist
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| PAD Review Checklist | `ProjectMgmt/Reviews/PAD/PAD_Review_Checklist.md` | **已更新** | ❓ | ⬜ |
| PAD Review Minutes | `ProjectMgmt/Reviews/PAD/PAD_Review_Meeting_YYYYMMDD.md` | 待创建 | ❓ | ⬜ |
| Architecture Review记录 | `ProjectMgmt/Reviews/PAD/Architecture_Review_YYYYMMDD.md` | 已完成 | ❓ | ⬜ |

#### 2.6 Bug & Risk
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Bug Tracking | `ProjectMgmt/Bugs/Bug_Tracking.md` | 已创建 | ❓ | ⬜ |
| 风险登记册 | `ProjectMgmt/RiskMgmt/Risk_Register.md` | 已更新 | ❓ | ⬜ |
| 风险缓解计划 | `ProjectMgmt/RiskMgmt/Risk_Mitigation_Plan.md` | 已完成 | ❓ | ⬜ |

#### 2.7 状态报告
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 项目周报 | `ProjectMgmt/StatusReports/Weekly_Report_Week*.md` | 持续更新 | ❓ | ⬜ |
| PAD阶段总结 | `ProjectMgmt/StatusReports/PAD_Phase_Summary.md` | 待创建 | ❓ | ⬜ |

**前置条件检查**:
- [ ] AI Yang质量检查通过
- [ ] PAD Review Checklist **已在会议前更新**
- [ ] 所有架构文档已冻结

**检查结论**: ⬜ 通过 / ⬜ 有条件通过 / ⬜ 不通过  
**遗留问题**: 

---

### Phase 3: EDR (Engineering Document Review)

**检查任务**: PM-{{PROJECT_ID}}-103

#### 3.1 设计文档
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Design Spec | `Database/Docs/Design/Design_Specification.md` | v1.0已冻结 | ❓ | ⬜ |
| Interface Spec | `Database/Docs/Design/Interface_Spec.md` | v1.0已冻结 | ❓ | ⬜ |
| CDC/RDC Strategy | `Database/Docs/Design/CDC_RDC_Strategy.md` | 已完成 | ❓ | ⬜ |
| Low Power Design | `Database/Docs/Design/Low_Power_Design.md` | 已完成 | ❓ | ⬜ |

#### 3.2 验证文档
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Verification Plan | `Database/Docs/Verification/Verification_Plan.md` | v1.0已冻结 | ❓ | ⬜ |
| Testbench Arch | `Database/Docs/Verification/TB_Architecture.md` | 已完成 | ❓ | ⬜ |
| Coverage Plan | `Database/Docs/Verification/Coverage_Plan.md` | 已完成 | ❓ | ⬜ |
| Test Strategy | `Database/Docs/Verification/Test_Strategy.md` | 已完成 | ❓ | ⬜ |

#### 3.3 DFT文档
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| DFT Spec | `Database/Docs/DFT/DFT_Specification.md` | 初版 | ❓ | ⬜ |

#### 3.4 Agent 任务清单
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Design Agent Tasks | `ProjectMgmt/Tasks/Design_Agent/TASK_LIST.md` | 已完成 | ❓ | ⬜ |
| Verification Agent Tasks | `ProjectMgmt/Tasks/Verification_Agent/TASK_LIST.md` | 已完成 | ❓ | ⬜ |
| DFT Agent Tasks | `ProjectMgmt/Tasks/DFT_Agent/TASK_LIST.md` | 已更新 | ❓ | ⬜ |

#### 3.5 Review & Checklist
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| EDR Review Checklist | `ProjectMgmt/Reviews/EDR/EDR_Review_Checklist.md` | **已更新** | ❓ | ⬜ |
| EDR Review Minutes | `ProjectMgmt/Reviews/EDR/EDR_Review_Meeting_YYYYMMDD.md` | 待创建 | ❓ | ⬜ |
| Design Review记录 | `ProjectMgmt/Reviews/EDR/Design_Review_YYYYMMDD.md` | 已完成 | ❓ | ⬜ |
| Verification Review记录 | `ProjectMgmt/Reviews/EDR/Verification_Review_YYYYMMDD.md` | 已完成 | ❓ | ⬜ |

#### 3.6 Bug & Risk
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Bug Tracking | `ProjectMgmt/Bugs/Bug_Tracking.md` | PAD遗留Bug已跟踪 | ❓ | ⬜ |
| 风险登记册 | `ProjectMgmt/RiskMgmt/Risk_Register.md` | 已更新 | ❓ | ⬜ |

#### 3.7 状态报告
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 项目周报 | `ProjectMgmt/StatusReports/Weekly_Report_Week*.md` | 持续更新 | ❓ | ⬜ |
| EDR阶段总结 | `ProjectMgmt/StatusReports/EDR_Phase_Summary.md` | 待创建 | ❓ | ⬜ |

**前置条件检查**:
- [ ] Design Spec ↔ Verification Plan 一致性检查通过
- [ ] AI Yang质量检查通过
- [ ] EDR Review Checklist **已在会议前更新** ⭐

**检查结论**: ⬜ 通过 / ⬜ 有条件通过 / ⬜ 不通过  
**遗留问题**: 

---

### Phase 4: IDR (Implementation Design Review)

**检查任务**: PM-{{PROJECT_ID}}-104

#### 4.1 RTL代码
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| RTL Source | `Database/DesignData/rtl/` | Code Freeze | ❓ | ⬜ |
| RTL顶层 | `Database/DesignData/rtl/{{PROJECT_NAME}}_top.v` | 已冻结 | ❓ | ⬜ |
| Lint Clean报告 | `Database/DesignData/reports/lint_report.md` | 无Critical/Major | ❓ | ⬜ |
| CDC Clean报告 | `Database/DesignData/reports/cdc_report.md` | 已清理 | ❓ | ⬜ |
| 综合报告 | `Database/DesignData/reports/synthesis_report.md` | 已完成 | ❓ | ⬜ |

#### 4.2 验证环境
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| UVM环境 | `Database/Verification/uvm/` | 已完成 | ❓ | ⬜ |
| Testcases | `Database/Verification/testcases/` | >95%通过 | ❓ | ⬜ |
| 覆盖率报告 | `Database/Verification/reports/coverage_report.md` | Code>90%, Func>85% | ❓ | ⬜ |
| 回归测试报告 | `Database/Verification/reports/regression_report.md` | 2周100%通过 | ❓ | ⬜ |
| 验证状态报告 | `Database/Verification/reports/verification_status.md` | 已完成 | ❓ | ⬜ |

#### 4.3 功能安全
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| FMEDA报告 | `Database/Docs/FuSa/FMEDA_Report.xlsx` | SPFM>99%, LFM>90% | ❓ | ⬜ |
| 故障注入报告 | `Database/Docs/FuSa/Fault_Injection_Report.md` | 已完成 | ❓ | ⬜ |
| Safety Case | `Database/Docs/FuSa/Safety_Case.md` | 已完成 | ❓ | ⬜ |

#### 4.4 Agent 任务清单
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Coding Yang Tasks | `ProjectMgmt/Tasks/Coding_Yang/TASK_LIST.md` | 已完成 | ❓ | ⬜ |
| FuSa Engineer Tasks | `ProjectMgmt/Tasks/FuSa_Engineer/TASK_LIST.md` | 已完成 | ❓ | ⬜ |

#### 4.5 Review & Checklist
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| IDR Review Checklist | `ProjectMgmt/Reviews/IDR/IDR_Review_Checklist.md` | **已更新** | ❓ | ⬜ |
| IDR Review Minutes | `ProjectMgmt/Reviews/IDR/IDR_Review_Meeting_YYYYMMDD.md` | 待创建 | ❓ | ⬜ |
| Code Review记录 | `ProjectMgmt/Reviews/IDR/Code_Review_YYYYMMDD.md` | 已完成 | ❓ | ⬜ |
| Verification Review记录 | `ProjectMgmt/Reviews/IDR/Verification_Review_YYYYMMDD.md` | 已完成 | ❓ | ⬜ |

#### 4.6 Bug & Risk
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Bug Tracking | `ProjectMgmt/Bugs/Bug_Tracking.md` | P1/P2关闭 | ❓ | ⬜ |
| Bug分析报告 | `ProjectMgmt/Bugs/Bug_Analysis_Report.md` | 已完成 | ❓ | ⬜ |
| 风险登记册 | `ProjectMgmt/RiskMgmt/Risk_Register.md` | 已更新 | ❓ | ⬜ |

#### 4.7 状态报告
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 项目周报 | `ProjectMgmt/StatusReports/Weekly_Report_Week*.md` | 持续更新 | ❓ | ⬜ |
| IDR阶段总结 | `ProjectMgmt/StatusReports/IDR_Phase_Summary.md` | 待创建 | ❓ | ⬜ |
| 项目月报 | `ProjectMgmt/StatusReports/Monthly_Report_M*.md` | 已发布 | ❓ | ⬜ |

**前置条件检查**:
- [ ] 覆盖率达标 (Code>90%, Func>85%, Assert>95%)
- [ ] Bug清理完成 (P1/P2关闭)
- [ ] 回归测试稳定 (连续2周100%通过)
- [ ] AI Yang质量检查通过
- [ ] IDR Review Checklist **已在会议前更新** ⭐

**检查结论**: ⬜ 通过 / ⬜ 有条件通过 / ⬜ 不通过  
**遗留问题**: 

---

### Phase 5: FDR (Final Design Review) - SoC Only

**检查任务**: PM-{{PROJECT_ID}}-105 ({{PROJECT_TYPE}} = SoC)

#### 5.1 物理实现
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 综合网表 | `Database/DesignData/netlist/` | 已冻结 | ❓ | ⬜ |
| SDC约束 | `Database/DesignData/constraints/` | 已Sign-off | ❓ | ⬜ |
| LEC报告 | `Database/DesignData/reports/lec_report.md` | 通过 | ❓ | ⬜ |
| STA报告 | `Database/DesignData/reports/sta_report.md` | 时序收敛 | ❓ | ⬜ |
| GDS | `Database/DesignData/gds/` | 已冻结 | ❓ | ⬜ |
| DRC/LVS报告 | `Database/DesignData/reports/physical_verification.md` | 通过 | ❓ | ⬜ |

#### 5.2 DFT
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| DFT报告 | `Database/DFT/dft_report.md` | 覆盖率达标 | ❓ | ⬜ |
| ATPG向量 | `Database/DFT/atpg_patterns/` | 已生成 | ❓ | ⬜ |
| 扫描链报告 | `Database/DFT/scan_chain_report.md` | 已完成 | ❓ | ⬜ |

#### 5.3 Tapeout
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Tapeout检查表 | `ProjectMgmt/Reviews/FDR/Tapeout_Checklist.md` | 已完成 | ❓ | ⬜ |
| Tapeout数据包 | `Database/DesignData/tapeout/` | 已准备 | ❓ | ⬜ |
| 交付物清单 | `ProjectMgmt/Reviews/FDR/Deliverables_Checklist.md` | 已签署 | ❓ | ⬜ |

#### 5.4 Review & Checklist
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| FDR Review Checklist | `ProjectMgmt/Reviews/FDR/FDR_Review_Checklist.md` | **已更新** | ❓ | ⬜ |
| FDR Review Minutes | `ProjectMgmt/Reviews/FDR/FDR_Review_Meeting_YYYYMMDD.md` | 待创建 | ❓ | ⬜ |

#### 5.5 Bug & Risk
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| Bug Tracking | `ProjectMgmt/Bugs/Bug_Tracking.md` | 所有Bug关闭或遗留 | ❓ | ⬜ |
| 风险登记册 | `ProjectMgmt/RiskMgmt/Risk_Register.md` | 已关闭或接受 | ❓ | ⬜ |

#### 5.6 状态报告
| 文档 | 路径 | 期望状态 | 实际状态 | 匹配 |
|------|------|----------|----------|------|
| 项目总结报告 | `ProjectMgmt/StatusReports/Project_Summary.md` | 待创建 | ❓ | ⬜ |
| Tapeout公告 | `ProjectMgmt/StatusReports/Tapeout_Announcement.md` | 待创建 | ❓ | ⬜ |

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

### 检查范围
PM Agent 必须检查项目文件夹下的**所有文件**，包括：
1. **基础文档**: README、MRD、可行性分析
2. **技术文档**: Architecture/Design/Verification/DFT/FuSa
3. **Review记录**: Review Checklist、Review Minutes、设计评审记录
4. **任务管理**: 各Agent Task List、Task Assignment
5. **Bug管理**: Bug Tracking、Bug分析报告
6. **风险管理**: Risk Register、Risk Mitigation Plan、Risk Management Plan
7. **状态报告**: 周报、月报、阶段总结、项目总结
8. **交付物清单**: Tapeout检查表、交付物清单

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
质量检查     按严重程度升级
  ↓           ↓
组织Review  等待决策
```

---

## ⚠️ 不匹配处理规则

| 严重程度 | 定义 | 处理方式 | 决策权 |
|----------|------|----------|--------|
| **Critical** | 阻塞Gate，影响项目继续推进 | 必须修复，Gate推迟 | **实体 Yang** |
| **Major** | 影响交付质量，但不阻塞Gate | 可遗留，需限期修复 | **AI Yang** |
| **Minor** | 轻微问题，不影响主要功能 | 可遗留，后续迭代修复 | **PM Agent** |

### 升级流程
```
发现不匹配
    ↓
评估严重程度
    ↓
  ┌─────┬─────────┴────────┐
  ▼     ▼                  ▼
Minor  Major             Critical
  ↓     ↓                  ↓
PM    AI Yang         实体 Yang
决策   决策              决策
  ↓     ↓                  ↓
记录   限期修复          阻塞Gate
```

### 决策标准

#### Critical (实体 Yang 决策)
- 核心文档缺失或严重不完整
- 跨文档关键信息严重不一致
- 安全/合规要求未满足
- 版本冻结文档存在重大缺陷

#### Major (AI Yang 决策)
- 文档章节不完整但非核心内容
- 跨文档引用存在轻微不一致
- 覆盖率/质量指标轻微不达标
- Bug遗留但已评估风险

#### Minor (PM Agent 决策)
- 格式/排版问题
- 非关键描述不准确
- 缺少次要章节
- 历史遗留的轻微问题

---

## 📊 文档追踪矩阵

| 文档类型 | PCD | PAD | EDR | IDR | FDR |
|----------|-----|-----|-----|-----|-----|
| README | ✅ | ✅ | ✅ | ✅ | ✅ |
| MRD | ✅ | ✅ | ✅ | ✅ | ✅ |
| Master Schedule | ✅ | ✅ | ✅ | ✅ | ✅ |
| Architecture Spec | ⬜ | ✅ | ✅ | ✅ | ✅ |
| Design Spec | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| Verification Plan | ⬜ | ⬜ | ✅ | ✅ | ✅ |
| RTL Code | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| Testbench | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| 覆盖率报告 | ⬜ | ⬜ | ⬜ | ✅ | ✅ |
| 综合网表 | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| GDS | ⬜ | ⬜ | ⬜ | ⬜ | ✅ |
| Review Checklist | ✅ | ✅ | ✅ | ✅ | ✅ |
| Review Minutes | ✅ | ✅ | ✅ | ✅ | ✅ |
| Bug Tracking | ⬜ | ✅ | ✅ | ✅ | ✅ |
| Risk Register | ✅ | ✅ | ✅ | ✅ | ✅ |
| 状态报告 | ✅ | ✅ | ✅ | ✅ | ✅ |

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

> **不匹配处理必须遵循升级规则:**
> - Critical → 实体 Yang 决策
> - Major → AI Yang 决策  
> - Minor → PM Agent 决策

---

*生成时间: {{DATE}}*
