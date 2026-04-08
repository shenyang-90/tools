# Bug Record - {{BUG_ID}}

## 基本信息

| 字段 | 值 |
|------|-----|
| **Bug ID** | {{BUG_ID}} |
| **标题** | {{BRIEF_DESCRIPTION}} |
| **所属模块** | {{MODULE_NAME}} |
| **发现阶段** | ☐ PCD / ☐ PAD / ☐ EDR / ☐ IDR / ☐ FDR / ☐ Post Silicon |
| **发现日期** | {{DATE}} |
| **报告人** | {{REPORTER}} |
| **优先级** | ☐ P1-Critical / ☐ P2-Major / ☐ P3-Minor / ☐ P4-Trivial |
| **状态** | ☐ Open / ☐ Fixed / ☐ Verified / ☐ Waived / ☐ Duplicate |

---

## 问题描述

### 现象描述
{{DESCRIPTION}}

### 复现步骤
1. 
2. 
3. 

### 期望行为
{{EXPECTED_BEHAVIOR}}

### 实际行为
{{ACTUAL_BEHAVIOR}}

### 影响范围
- [ ] 功能影响：
- [ ] 性能影响：
- [ ] 面积影响：
- [ ] 功耗影响：
- [ ] 时序影响：
- [ ] 其他：

---

## 环境信息

| 项目 | 信息 |
|------|------|
| 工艺节点 | {{PROCESS}} |
| 工具版本 | {{TOOL_VERSION}} |
| RTL版本 | {{RTL_REVISION}} |
| 测试用例 | {{TESTCASE}} |
| 仿真环境 | {{SIM_ENV}} |

---

## 根本原因分析 (RCA)

### 根因描述
{{ROOT_CAUSE}}

### 引入原因
- [ ] 设计错误
- [ ] 规格理解错误
- [ ] 工具问题
- [ ] 配置错误
- [ ] 流程遗漏
- [ ] 其他：

---

## 修复方案

### 修复描述
{{FIX_DESCRIPTION}}

### 修改文件
| 文件路径 | 修改类型 | 说明 |
|----------|----------|------|
| | ☐ 新增 / ☐ 修改 / ☐ 删除 | |

### 修复责任人
{{FIX_OWNER}}

### 修复日期
{{FIX_DATE}}

---

## 验证结果

### 验证方法
{{VERIFICATION_METHOD}}

### 验证用例
{{VERIFICATION_TESTCASE}}

### 验证结果
- [ ] 问题已修复
- [ ] 回归测试通过
- [ ] 覆盖率无下降
- [ ] 时序无恶化
- [ ] 其他影响已评估

### 验证人
{{VERIFIER}}

### 验证日期
{{VERIFICATION_DATE}}

---

## 审批流程

### P3/P4 Waive 审批 (如适用)

| 角色 | 审批意见 | 签字 | 日期 |
|------|---------|------|------|
| PM / 架构师 (P3) | ☐ 批准 / ☐ 拒绝 | | |
| Verification Lead (P4) | ☐ 批准 / ☐ 拒绝 | | |

**Waive 理由**:

---

## 经验教训

### 预防措施
{{PREVENTION_MEASURES}}

### 流程改进建议
{{PROCESS_IMPROVEMENT}}

### 是否更新Checklist
- [ ] 是，已更新相关Checklist
- [ ] 否

---

## 历史记录

| 版本 | 日期 | 变更说明 | 作者 |
|------|------|---------|------|
| v1.0 | | Bug创建 | {{REPORTER}} |
| v1.1 | | 根因分析完成 | {{ANALYZER}} |
| v1.2 | | 修复完成 | {{FIX_OWNER}} |
| v1.3 | | 验证通过 | {{VERIFIER}} |

---

## 附件

- [ ] 仿真波形/截图
- [ ] 分析报告
- [ ] 修复前后对比
- [ ] 其他支持材料

---

*Bug记录命名规范: BUG_[ID]_[Brief_Description].md*
*存储位置: ProjectMgmt/Bugs/P[N]_[Priority]/*
