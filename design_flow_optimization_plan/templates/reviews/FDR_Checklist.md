# FDR (Final Design Review) Checklist

## 基本信息

| 字段 | 值 |
|------|-----|
| **评审阶段** | FDR - Final Design Review (Tapeout) |
| **项目名称** | {{PROJECT_NAME}} |
| **评审日期** | {{DATE}} |
| **版本** | {{VERSION}} |
| **评审人** | {{REVIEWERS}} |
| **评审结果** | ☐ PASS / ☐ CONDITIONAL / ☐ FAIL |

---

## FDR 检查项汇总

| 类别 | 检查项数 | 状态 |
|------|---------|------|
| 逻辑等价性 | 2 | |
| 时序Sign-off | 4 | |
| 物理验证 | 3 | |
| DFT | 3 | |
| 功耗分析 | 2 | |
| 功能安全 | 3 | |
| 量产准备 | 2 | |
| **总计** | **19** | |

**通过标准**: 所有Critical检查项必须通过

---

## 逻辑等价性 (Logical Equivalence)

### 1. 🔴 LEC验证通过 [Critical]
- **描述**: 综合后网表与RTL逻辑等价验证通过
- **参考文档**: `Database/Docs/Physical/LEC_Report.md`
- **验证方法**: Formality/Conformal LEC检查
- **验收标准**: 无逻辑不等价错误
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 2. 🔴 网表版本一致性 [Critical]
- **描述**: 用于PR的网表与用于STA/LEC的网表版本一致
- **参考文档**: `Database/DesignData/Netlist/`
- **验证方法**: 版本号检查、MD5校验
- **验收标准**: 所有流程使用同一版本网表
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## 时序Sign-off (Timing Sign-off)

### 3. 🔴 Setup时序收敛 [Critical]
- **描述**: 所有corner setup时序收敛，无violation
- **参考文档**: `Database/Docs/Physical/STA_Setup_Report.md`
- **验证方法**: PrimeTime/Tempus STA分析
- **验收标准**: Setup Slack > 0 (含margin)
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 4. 🔴 Hold时序收敛 [Critical]
- **描述**: 所有corner hold时序收敛，无violation
- **参考文档**: `Database/Docs/Physical/STA_Hold_Report.md`
- **验证方法**: PrimeTime/Tempus STA分析
- **验收标准**: Hold Slack > 0 (含margin)
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 5. 🟡 MMMC覆盖 [Major]
- **描述**: 多模式多 corner (MMMC) 覆盖完整
- **参考文档**: `Database/Docs/Physical/MMMC_Config.md`
- **验证方法**: 检查scenario定义
- **验收标准**: 覆盖所有工作模式(P0/P1/P2...)
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 6. 🟡 OCV/AOCV/POCV分析 [Major]
- **描述**: 片上变化分析完成
- **参考文档**: `Database/Docs/Physical/OCV_Analysis.md`
- **验证方法**: 检查STA设置
- **验收标准**: OCV/AOCV/POCV正确应用
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## 物理验证 (Physical Verification)

### 7. 🔴 DRC Clean [Critical]
- **描述**: 设计规则检查无错误
- **参考文档**: `Database/Docs/Physical/DRC_Report.md`
- **验证工具**: Calibre/Pegasus/KLayout
- **验收标准**: 无DRC violation
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 8. 🔴 LVS Clean [Critical]
- **描述**: 版图与网表一致性检查通过
- **参考文档**: `Database/Docs/Physical/LVS_Report.md`
- **验证工具**: Calibre/Pegasus
- **验收标准**: 无LVS mismatch
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 9. 🔴 ERC Clean [Critical]
- **描述**: 电气规则检查通过
- **参考文档**: `Database/Docs/Physical/ERC_Report.md`
- **验证工具**: Calibre/Pegasus
- **验收标准**: 无ERC error
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## DFT

### 10. 🔴 ATPG覆盖率达标 [Critical]
- **描述**: ATPG测试向量覆盖率满足目标
- **参考文档**: `Database/Docs/DFT/ATPG_Report.md`
- **验证方法**: TetraMAX/VMAX ATPG分析
- **验收标准**: 覆盖率 > 95%
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 11. 🟡 BIST集成 [Major]
- **描述**: MBIST/LBIST正确集成
- **参考文档**: `Database/Docs/DFT/BIST_Integration.md`
- **验证方法**: BIST仿真验证
- **验收标准**: BIST功能正常，诊断可用
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 12. 🟡 扫描链实现 [Major]
- **描述**: 扫描链插入完成，时序满足
- **参考文档**: `Database/Docs/DFT/Scan_Chain_Report.md`
- **验证方法**: 扫描链连接检查
- **验收标准**: 扫描链可正常工作
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## 功耗分析 (Power Analysis)

### 13. 🟡 IR Drop分析 [Major]
- **描述**: 电源压降分析在规格内
- **参考文档**: `Database/Docs/Physical/IR_Drop_Report.md`
- **验证工具**: RedHawk/Voltus
- **验收标准**: IR Drop < 5%
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 14. 🟡 EM分析 [Major]
- **描述**: 电迁移分析通过
- **参考文档**: `Database/Docs/Physical/EM_Report.md`
- **验证工具**: RedHawk/Voltus
- **验收标准**: 无EM violation
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## 功能安全 (Functional Safety)

### 15. 🔴 Safety Case完整 [Critical]
- **描述**: 功能安全论证文档完整
- **参考文档**: `Database/Docs/FuSa/Safety_Case.md`
- **验证方法**: 文档完整性检查
- **验收标准**: 满足ISO 26262要求
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 16. 🔴 FMEDA最终版 [Critical]
- **描述**: FMEDA最终版本完成并审核
- **参考文档**: `Database/Docs/FuSa/FMEDA_Final.xlsx`
- **验证方法**: FMEDA计算检查
- **验收标准**: 满足ASIL等级要求
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 17. 🔴 DFA完成 [Critical]
- **描述**: 相关故障分析完成
- **参考文档**: `Database/Docs/FuSa/DFA_Report.md`
- **验证方法**: DFA分析检查
- **验收标准**: 所有相关故障已分析
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## 量产准备 (Production Readiness)

### 18. 🟡 GDSII通过Foundry检查 [Major]
- **描述**: GDSII数据通过代工厂检查
- **参考文档**: `Database/DesignData/GDS/`
- **验证方法**: Foundry DRC检查
- **验收标准**: Foundry确认可接收
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

### 19. 🟡 ATE测试程序准备 [Major]
- **描述**: ATE量产测试程序就绪
- **参考文档**: `Database/Validation/ATE/`
- **验证方法**: ATE程序验证
- **验收标准**: ATE程序通过验证
- **状态**: ☐ 符合 / ☐ 不符合 / ☐ 不适用
- **责任人**: ___________
- **备注**: ___________

---

## FDR 评审结论

### 关键交付物检查
- [ ] **Scan Insertion** - 扫描链实现
- [ ] **BIST Controllers** - BIST控制器
- [ ] **Netlist (LEC Verified)** - 综合后网表
- [ ] **GDSII Layout** - 物理版图
- [ ] **STA Sign-off Report** - 时序Sign-off
- [ ] **DRC/LVS/ERC Clean Report** - 物理验证
- [ ] **Power Analysis Report** - 功耗分析
- [ ] **ATPG Patterns** - 测试向量
- [ ] **Safety Case** - 安全论证
- [ ] **FMEDA (最终版)** - 最终安全分析
- [ ] **DFA Report** - 相关故障分析

### 检查项统计
| 类别 | Critical | Major | 总计 | 通过 | 不通过 |
|------|----------|-------|------|------|--------|
| 检查项 | 10 | 9 | 19 | | |

**通过标准检查**:
- [ ] 🔴 Critical (10项): 全部符合 ___ / 10

**评审结论**: ☐ 通过 / ☐ 有条件通过 / ☐ 不通过

**Tapeout决策**: ☐ 批准 / ☐ 延迟 / ☐ 拒绝

---

## 签字确认

| 角色 | 签名 | 日期 |
|------|------|------|
| 物理设计负责人 | ___________ | ___________ |
| DFT负责人 | ___________ | ___________ |
| 功能安全架构师 | ___________ | ___________ |
| 时序负责人 | ___________ | ___________ |
| 项目经理 | ___________ | ___________ |
| AI Yang (Quality Gatekeeper) | ☐ | ___________ |
| 实体Yang (最终批准) | ☐ | ___________ |

---

## 历史版本记录

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| v1.0 | | 首次创建 FDR Checklist | |

---

*此Checklist基于 workflow/SOC_DESIGN_WORKFLOW.md 定义*
