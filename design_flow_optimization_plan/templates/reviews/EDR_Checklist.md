# EDR (Engineering Document Review) Checklist

## 基本信息

| 字段 | 值 |
|------|-----|
| **评审阶段** | EDR - Engineering Document Review |
| **项目名称** | {{PROJECT_NAME}} |
| **评审日期** | {{DATE}} |
| **版本** | {{VERSION}} |
| **评审人** | {{REVIEWERS}} |
| **评审结果** | ☐ PASS / ☐ CONDITIONAL / ☐ FAIL |

---

## EDR Review 6-Phase 流程

```
Phase 1: 设计文档初稿 Review
    ↓
Phase 2: 设计文档修改版确认
    ↓
Phase 3: Reference Manual External 章节
    ↓
Phase 4: Codebeamer 跟踪检查
    ↓
Phase 5: Reference Manual Internal 章节
    ↓
Phase 6: 第三方IP文档审查
    ↓
EDR Gate 批准
```

---

## Phase 1-2: 设计文档Review与修改

### Phase 1 检查项
- [ ] 设计文档发送Verification owner review
- [ ] Verification owner提出文档修改意见
- [ ] 修改意见记录在Codebeamer/问题跟踪系统

### Phase 2 检查项
- [ ] IP/Project完成设计文档修改
- [ ] 修改内容确认，关闭review意见
- [ ] 所有修改有对应的问题编号和关闭记录

---

## Phase 3: Reference Manual External章节

### 必需章节检查
- [ ] **Overview** - 模块概述完整
  - 模块功能简介
  - 应用场景
  - 关键特性列表

- [ ] **Function Descriptions** - 功能描述详细
  - 详细功能说明
  - 工作流程描述
  - 算法说明（如适用）

- [ ] **Register Descriptions** - 寄存器定义完整
  - 寄存器列表完整
  - 位域定义准确
  - 读写属性正确（R/W/RW/RC/WC等）
  - 复位值定义

- [ ] **Example** - 使用示例明确
  - 配置流程示例
  - 典型应用场景
  - **每一步是否独立、可以被中断？** ⚠️ 关键检查点

### 复用模块检查
- [ ] **复用模块改动说明** - 重点强调复用模块的改动点
  - 原始模块来源
  - 本次修改内容
  - 修改原因说明

---

## Phase 4: Codebeamer跟踪检查

### HWE2内容检查
- [ ] **HWE2全部内容** - 已在Codebeamer完整记录
  - 所有硬件需求条目化
  - 需求ID分配
  - 需求状态跟踪

### Release标记
- [ ] **Release标记** - v0.5/v0.7/v0.9版本标记清晰
  - v0.5: 初步设计版本
  - v0.7: 设计优化版本
  - v0.9: 冻结前版本
  - v1.0: 冻结版本

### 需求追溯
- [ ] **HWE1追溯检查** - 需求追溯关系正确
  - HWE1 → HWE2追溯
  - HWE2 → Design Spec追溯
  - 双向追溯完整

### 第三方IP
- [ ] **第三方IP重点关注** - 所有第三方IP已识别并跟踪
  - IP供应商信息
  - 版本号
  - License信息
  - 已知问题/Errata

### 参数与配置检查
- [ ] **Parameter与配置选项** - 说明及具体配置明确
  - 所有可配置参数列表
  - 参数取值范围
  - 默认值定义

- [ ] **原始配置工具** - 配置工具、表格、define文件完整
  - 配置工具可用
  - 配置表格最新
  - define文件正确

- [ ] **Timing/Power优化配置** - 优化配置项已定义
  - 时序优化选项
  - 功耗优化选项
  - 面积优化选项

- [ ] **SRAM/ROM大小配置** - 存储器大小配置正确
  - SRAM大小计算
  - ROM大小计算
  - 配置可调整

- [ ] **FIFO大小配置** - FIFO深度配置正确
  - FIFO深度计算依据
  - Burst情况考虑
  - 深度可配置

### 接口与异步检查
- [ ] **Interface** - 接口信号连接正确
  - 信号列表完整
  - 信号方向正确
  - tie固定值或floating处理明确

- [ ] **Async** - 异步信号处理
  - IP顶层异步接口识别
  - IP内部异步处理方案
  - 未处理信号说明及原因

### DFT检查
- [ ] **DFT特殊处理** - IP内部特殊的时钟、复位及对应的DFT处理
  - 特殊时钟处理
  - 特殊复位处理
  - DFT可控性保证

---

## Phase 5: Reference Manual Internal章节

### 状态机
- [ ] **状态机定义完整**
  - 状态机框图
  - 状态编码定义
  - 状态转换条件
  - 复位状态定义

### 关键接口时序
- [ ] **关键接口时序图准确**
  - 输入/输出时序
  -  Setup/Hold要求
  - 时钟域说明

### 专利点说明
- [ ] **专利申请点、创新点说明**
  - 创新技术点
  - 专利申请建议
  - 与竞品差异

---

## Phase 6: 第三方IP文档

### Standard Cell
- [ ] **需要替换的standard cell列表**
  - 目标工艺库适配
  - 替换方案
  - 替换风险

### Release Notes
- [ ] **第三方IP release notes已获取**
  - 版本变更历史
  - 新功能说明
  - 已知限制

### Errata
- [ ] **第三方IP errata已获取并评估影响**
  - 已知问题列表
  - 影响分析
  - 规避方案

---

## EDR Review 会议记录模板

### 基本信息
| 字段 | 值 |
|------|-----|
| **会议名称** | EDR评审会 - {{MODULE_NAME}} |
| **会议日期** | {{DATE}} |
| **会议地点** | {{LOCATION}} |
| **记录人** | {{RECORDER}} |

### 参会人员
| 角色 | 姓名 | 部门 | 出席状态 |
|------|------|------|---------|
| 主持人 | | | |
| IP设计工程师 | | | |
| Verification工程师 | | | |
| System Architect | | | |
| DFT工程师 | | | |
| PM | | | |

### 各Phase评审记录

| Phase | 检查项 | 状态 | 问题/备注 |
|-------|--------|------|----------|
| Phase 1 | 设计文档初稿Review | ☐ | |
| Phase 2 | 修改版确认 | ☐ | |
| Phase 3 | External章节 | ☐ | |
| Phase 4 | Codebeamer跟踪 | ☐ | |
| Phase 5 | Internal章节 | ☐ | |
| Phase 6 | 第三方IP文档 | ☐ | |

### 问题清单
| ID | 问题描述 | 严重程度 | 责任人 | 截止日期 | 状态 |
|----|----------|----------|--------|----------|------|
| 1 | | Critical/Major/Minor | | | Open/Fixed |

### 决策事项
| 决策项 | 决策结果 | 决策依据 |
|--------|---------|---------|
| EDR Gate | ☐ PASS / ☐ CONDITIONAL / ☐ FAIL | |

### Action Items
| # | 行动项 | 责任人 | 截止日期 | 状态 |
|---|--------|--------|----------|------|
| 1 | | | | |

---

## EDR Gate 检查清单

### 交付物检查
- [ ] **Design Specifications** (各模块) - 详细设计规格
- [ ] **Verification Plan** - 验证计划
- [ ] **Interface Specifications** - 接口规格
- [ ] **CDC/RDC Strategy Doc** - 跨时钟域策略
- [ ] **DFT Specification** - 可测性设计规格
- [ ] **Floorplan Guidelines** - 布局指南

### 质量检查
- [ ] **AI Yang 质量检查通过** (Gate前)
- [ ] **EDR Review Checklist已更新**
- [ ] **所有6个Phase检查通过**
- [ ] **无Critical遗留问题**
- [ ] **Major问题有明确解决方案**

### 评审会议
- [ ] **EDR评审会议召开**
- [ ] **会议记录归档**: `ProjectMgmt/Reviews/EDR/EDR_Review_Meeting_Minutes_YYYYMMDD.md`
- [ ] **参会人员签字确认**

---

## 签字确认

| 角色 | 签名 | 日期 |
|------|------|------|
| IP设计负责人 | ___________ | ___________ |
| Verification负责人 | ___________ | ___________ |
| System Architect | ___________ | ___________ |
| DFT负责人 | ___________ | ___________ |
| 项目经理 | ___________ | ___________ |
| AI Yang (Quality Gatekeeper) | ☐ | ___________ |
| 实体Yang (最终批准) | ☐ | ___________ |

---

## 历史版本记录

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| v1.0 | | 首次创建 EDR Checklist | |

---

*此Checklist基于 workflow/SOC_DESIGN_WORKFLOW.md 定义*
*6-Phase EDR Review流程*
