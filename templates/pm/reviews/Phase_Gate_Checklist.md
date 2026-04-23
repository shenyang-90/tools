# Phase Gate 检查清单汇总

> 车规级SoC六阶段模型门禁检查清单
> PCD → PAD → EDR → IDR → FDR → Post Silicon

---

## 阶段门禁总览

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  PCD    │ →  │  PAD    │ →  │  EDR    │ →  │  IDR    │ →  │  FDR    │ →  │ Post Si │
│  Gate   │    │  Gate   │    │  Gate   │    │  Gate   │    │  Gate   │    │  Gate   │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
    │               │               │               │               │               │
    ▼               ▼               ▼               ▼               ▼               ▼
 需求确认         架构冻结        文档冻结        Code Freeze     Tapeout        量产
 产品调研         安全概念        设计/验证        • RTL冻结       GDS交付        批准
 项目立项         架构评审        文档评审        • Case完成      功能安全        AEC-Q100
                 批准            批准            • 验证Sign-off   认证通过       认证
                                 ↑                               ↑
                                 │                               │
                           评审会议记录                      评审会议记录
                           PCD/PAD/EDR/                   IDR/FDR/Post Si
                           IDR/FDR/Post Si                会议记录归档
                           会议记录归档
```

---

## PCD Gate - 项目概念门禁

**前置条件**: 项目立项评审完成

### 交付物检查
- [ ] **客户需求文档 (CRD)** - Customer Requirement Document
- [ ] **产品调研报告** - 市场分析、竞品对标
- [ ] **项目立项书** - 目标、范围、资源、预算
- [ ] **风险评估报告** - 技术风险、供应链风险

### 会议记录
- [ ] **PCD评审会议记录归档**: `ProjectMgmt/Reviews/PCD/PCD_Review_Meeting_Minutes_YYYYMMDD.md`

### 决策项
- [ ] **Go/No-Go决策**: 项目立项批准

---

## PAD Gate - 产品架构门禁

**前置条件**: AI Yang 质量检查通过 + ADR Checklist完成

### 交付物检查
- [ ] **Architecture Specification** - 系统架构规格书
- [ ] **Safety Concept** - 功能安全概念文档
- [ ] **FMEDA初版** - 功能安全分析初版
- [ ] **Firmware Architecture Spec** - 固件架构规格
- [ ] **Power Domain Specification** - 功耗域规格
- [ ] **Performance Modeling Report** - 性能建模报告

### Checklist
- [ ] **ADR Checklist完成**: 21项检查，Critical 100% + Major ≥80%

### 质量检查
- [ ] **AI Yang 质量检查通过**
- [ ] **节点状态总结报告**

### 会议记录
- [ ] **PAD评审会议记录归档**: `ProjectMgmt/Reviews/PAD/PAD_Review_Meeting_Minutes_YYYYMMDD.md`
- [ ] **参与人员**: 全体架构师、PM、高级管理层

### 决策项
- [ ] **架构冻结批准**

---

## EDR Gate - 工程文档门禁

**前置条件**: AI Yang 质量检查通过 + 6-Phase EDR Review完成

### 交付物检查
- [ ] **Design Specifications** (各模块) - 详细设计规格
- [ ] **Verification Plan** - 验证计划
- [ ] **Interface Specifications** - 接口规格
- [ ] **CDC/RDC Strategy Doc** - 跨时钟域策略
- [ ] **DFT Specification** - 可测性设计规格
- [ ] **Floorplan Guidelines** - 布局指南

### Checklist
- [ ] **EDR 6-Phase Review完成**:
  - Phase 1-2: 设计文档Review与修改
  - Phase 3: Reference Manual External章节
  - Phase 4: Codebeamer跟踪检查
  - Phase 5: Reference Manual Internal章节
  - Phase 6: 第三方IP文档

### 质量检查
- [ ] **AI Yang 质量检查通过**
- [ ] **EDR Review Checklist已更新**

### 会议记录
- [ ] **EDR评审会议记录归档**: `ProjectMgmt/Reviews/EDR/EDR_Review_Meeting_Minutes_YYYYMMDD.md`

### 决策项
- [ ] **文档冻结批准**，进入实现阶段

---

## IDR Gate - 实现设计门禁

**前置条件**: AI Yang 质量检查通过 + IDR Checklist 42项完成

### 交付物检查
- [ ] **RTL Code** (Lint/CDC Clean)
- [ ] **Testbench & Testcases** - 验证环境
- [ ] **Coverage Reports** - 覆盖率报告
- [ ] **Verification Sign-off** - 验证Sign-off
- [ ] **Fault Injection Report** - 故障注入报告
- [ ] **GLS Report** - 门级仿真报告
- [ ] **FPGA Validation Report** - FPGA验证报告
- [ ] **SDC Constraints** - 时序约束
- [ ] **UPF/CPF** - 低功耗约束

### Checklist
- [ ] **IDR Checklist完成**: 42项检查
  - Common Design: 18项
  - Common Low Power: 2项
  - Common CDC: 9项
  - Common DFT: 13项

### 覆盖率要求
- [ ] **代码覆盖率** > 90%
- [ ] **功能覆盖率** > 85%
- [ ] **断言覆盖率** > 95%

### Bug状态
- [ ] **所有P1/P2 Bug关闭**

### 回归测试
- [ ] **回归测试连续2周100%通过**
- [ ] **GLS仿真通过**
- [ ] **故障注入验证满足FMEDA**

### 质量检查
- [ ] **AI Yang 质量检查通过**
- [ ] **IDR Review Checklist已更新**

### 会议记录
- [ ] **模块级IDR评审会议**: `[ModuleName]_IDR_Review_Meeting_Minutes_YYYYMMDD.md`
- [ ] **系统级IDR评审会议**: `SoC_IDR_Review_Meeting_Minutes_YYYYMMDD.md`

### 决策项
- [ ] **Code Freeze批准**，进入后端阶段

---

## FDR Gate - 最终设计门禁

**前置条件**: AI Yang 质量检查通过 + FDR Checklist完成

### 交付物检查
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

### Checklist
- [ ] **FDR Checklist完成**: 19项检查
  - 逻辑等价性: 2项
  - 时序Sign-off: 4项
  - 物理验证: 3项
  - DFT: 3项
  - 功耗分析: 2项
  - 功能安全: 3项
  - 量产准备: 2项

### 质量检查
- [ ] **AI Yang 质量检查通过**
- [ ] **FDR Review Checklist已更新**

### 会议记录
- [ ] **FDR评审会议记录归档**: `ProjectMgmt/Reviews/FDR/FDR_Review_Meeting_Minutes_YYYYMMDD.md`

### 决策项
- [ ] **Tapeout批准**

---

## Post Silicon Gate - 硅后门禁

**前置条件**: 芯片回片验证完成

### 交付物检查
- [ ] **ATE Test Report** - ATE测试报告
- [ ] **Bring-up Report** - Bring-up报告
- [ ] **Silicon Validation Report** - 硅后验证报告
- [ ] **AEC-Q100 Certificate** - 车规认证

### 关键指标
- [ ] **良率达到目标** (通常 > 90%)
- [ ] **功能验证通过**
- [ ] **AEC-Q100认证通过**
- [ ] **量产测试程序就绪**

### 会议记录
- [ ] **Post Silicon评审会议记录归档**: `ProjectMgmt/Reviews/PostSilicon/PostSilicon_Review_Meeting_Minutes_YYYYMMDD.md`

### 决策项
- [ ] **量产批准**

---

## 文件命名规范

### Review记录
```
[阶段]_Review_Meeting_Minutes_YYYYMMDD.md

示例:
- PCD_Review_Meeting_Minutes_20260327.md
- PAD_Review_Meeting_Minutes_20260615.md
- EDR_Review_Meeting_Minutes_20260901.md
- IDR_Review_Meeting_Minutes_20261220.md
- FDR_Review_Meeting_Minutes_20270315.md
- PostSilicon_Review_Meeting_Minutes_20270601.md
```

### IDR模块级记录
```
[ModuleName]_IDR_Review_Meeting_Minutes_YYYYMMDD.md

示例:
- CPU_IDR_Review_Meeting_Minutes_20260327.md
- DMA_IDR_Review_Meeting_Minutes_20260327.md
- USB_IDR_Review_Meeting_Minutes_20260415.md
```

### Checklist文件
```
[阶段]_Checklist_[ModuleName]_v[X.X]_[YYYYMMDD].md

示例:
- ADR_Checklist_PAD_v1.0_20260615.md
- EDR_Checklist_CPU_v1.0_20260901.md
- IDR_Checklist_DMA_v1.0_20261220.md
- FDR_Checklist_SoC_v1.0_20270315.md
```

---

## AI Yang 质量检查节点

每个Gate前的标准流程：

```
PM Agent 确认交付物完成
        ↓
通知 AI Yang（Quality Gatekeeper）
        ↓
批判性检查（完整性、一致性、可追溯性、质量底线、规范性）
        ↓
发现问题 → 反馈 PM Agent → 修改 → 重新检查
        ↓
无问题 → 生成节点状态总结 → 提交实体 Yang
        ↓
实体 Yang 审阅并决策（通过/不通过）
        ↓
举行评审会议 → 更新Checklist → 签字确认
```

---

## 历史版本记录

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| v1.0 | | 首次创建 Phase Gate 汇总 | |

---

*此Checklist基于 workflow/SOC_DESIGN_WORKFLOW.md 定义*
