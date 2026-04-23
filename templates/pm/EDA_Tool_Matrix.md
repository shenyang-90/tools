# EDA工具矩阵参考

> 基于 workflow/SOC_DESIGN_WORKFLOW.md 定义
> 车规级SoC设计各阶段工具推荐

---

## 工具矩阵总览

| 流程阶段 | 核心工具 | 用途 | 开源替代 |
|---------|---------|------|---------|
| PCD | Excel/PPT/Markdown | 需求分析、调研报告 | Markdown |
| PAD | SystemC/Gem5 | 性能建模 | Gem5 |
| EDR | Word/Markdown | 文档编写 | Markdown |
| IDR | VCS/Xcelium/UVM | RTL开发与验证 | Verilator/Icarus |
| FDR | ICC2/Innovus/PT | 物理实现与Sign-off | OpenROAD |
| Post Si | ATE/示波器 | 硅后测试 | - |

---

## 一、仿真验证工具

### 商业工具

| 工具 | 厂商 | 用途 | 特点 |
|------|------|------|------|
| **VCS** | Synopsys | RTL仿真 | 高性能，业界标准 |
| **Xcelium** | Cadence | RTL仿真 | 多核并行，UVM支持好 |
| **QuestaSim** | Siemens | RTL仿真 | 调试功能强 |

### 开源工具

| 工具 | 用途 | 特点 | 适用场景 |
|------|------|------|---------|
| **Verilator** | RTL仿真 | 速度快，支持SVA | 大规模设计，CI/CD |
| **Icarus Verilog** | RTL仿真 | 轻量，易用 | 小规模设计，教育 |
| **GHDL** | VHDL仿真 | VHDL支持好 | VHDL设计 |

### Makefile集成
```makefile
# 仿真目标
.PHONY: sim_vcs sim_xcelium sim_verilator

sim_vcs:
	vcs -sverilog -debug_access+all -f filelist.f -o simv
	./simv

sim_xcelium:
	xrun -sv -access +rwc -f filelist.f

sim_verilator:
	verilator --cc --exe --build --trace -f filelist.f top.sv sim_main.cpp
```

---

## 二、Lint/CDC检查工具

### 商业工具

| 工具 | 厂商 | 用途 |
|------|------|------|
| **SpyGlass** | Synopsys | Lint/CDC/RDC/DFT检查 |
| **Ascent** | Real Intent | CDC/RDC检查 |
| **Conformal** | Cadence | 等效性检查 |

### 开源工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **Verilator --lint-only** | Lint检查 | 快速，基础检查 |
| **Yosys** | 综合+检查 | 可扩展，脚本化 |

### Makefile集成
```makefile
.PHONY: lint_spyglass lint_verilator

lint_spyglass:
	spyglass -project sg_project.prj -batch

lint_verilator:
	verilator --lint-only -Wall -f filelist.f top.sv
```

---

## 三、逻辑综合工具

### 商业工具

| 工具 | 厂商 | 用途 | 特点 |
|------|------|------|------|
| **Design Compiler** | Synopsys | 逻辑综合 | 业界标准，QoR好 |
| **Fusion Compiler** | Synopsys | 综合+布局 | 统一流程，PPA优化 |
| **Genus** | Cadence | 逻辑综合 | 多线程，快速 |

### 开源工具

| 工具 | 用途 | 特点 | 限制 |
|------|------|------|------|
| **Yosys** | 逻辑综合 | 开源，可扩展 | 先进工艺支持有限 |
| **ABC** | 逻辑优化 | 优化算法强 | 需配合Yosys |

### Makefile集成
```makefile
.PHONY: synth_dc synth_yosys

synth_dc:
	dc_shell -f scripts/synth.tcl | tee logs/synth.log

synth_yosys:
	yosys -s scripts/synth.ys | tee logs/synth.log
```

---

## 四、物理实现工具

### 商业工具

| 工具 | 厂商 | 用途 | 特点 |
|------|------|------|------|
| **Innovus** | Cadence | 物理设计 | 先进工艺支持好 |
| **ICC2** | Synopsys | 物理设计 | 与DC流程集成好 |

### 开源工具

| 工具 | 用途 | 特点 | 状态 |
|------|------|------|------|
| **OpenROAD** | RTL-to-GDS | 全流程开源 | 活跃开发 |
| **Magic** | 版图编辑 | 经典工具 | 成熟稳定 |
| **KLayout** | 版图查看/编辑 | 现代UI | 推荐 |

### OpenROAD流程
```bash
# OpenROAD流程
openroad -exit -no_splash -log logs/openroad.log scripts/floorplan.tcl
```

---

## 五、时序分析工具

### 商业工具

| 工具 | 厂商 | 用途 | 特点 |
|------|------|------|------|
| **PrimeTime** | Synopsys | STA Sign-off | 业界标准 |
| **Tempus** | Cadence | STA分析 | 与Innovus集成 |

### 开源工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **OpenSTA** | STA分析 | OpenROAD配套 |
| **Yosys sta** | 基础STA | 快速评估 |

### Makefile集成
```makefile
.PHONY: sta_pt sta_opensta

sta_pt:
	pt_shell -f scripts/sta.tcl | tee logs/sta.log

sta_opensta:
	opensta scripts/sta.tcl | tee logs/sta.log
```

---

## 六、DFT工具

### 商业工具

| 工具 | 厂商 | 用途 |
|------|------|------|
| **Tessent** | Siemens | 完整DFT方案 |
| **Modus** | Cadence | ATPG/BIST |
| **DFTAdvisor** | Synopsys | 扫描链插入 |

### 开源工具

| 工具 | 用途 | 状态 |
|------|------|------|
| **OpenROAD** | 基础DFT | 有限支持 |
| **Fault** | 故障仿真 | 教育用途 |

**注意**: DFT流程建议以商业工具为主

---

## 七、形式验证工具

### 商业工具

| 工具 | 厂商 | 用途 |
|------|------|------|
| **Conformal** | Cadence | LEC |
| **Formality** | Synopsys | LEC |

### 开源工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **Yosys equiv** | 简单LEC | 基础检查 |

---

## 八、物理验证工具

### 商业工具

| 工具 | 厂商 | 用途 |
|------|------|------|
| **Calibre** | Siemens | DRC/LVS/ERC |
| **Pegasus** | Cadence | DRC/LVS |

### 开源工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **KLayout** | DRC/LVS | 现代，脚本化 |
| **Magic** | DRC/提取 | 经典工具 |

---

## 九、波形调试工具

### 商业工具

| 工具 | 厂商 | 用途 |
|------|------|------|
| **Verdi** | Synopsys | 波形调试 |
| **SimVision** | Cadence | 波形调试 |

### 开源工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **GTKWave** | 波形查看 | 轻量，免费 |
| **Surfer** | 波形查看 | 现代UI |

---

## 十、覆盖率分析工具

### 商业工具

| 工具 | 厂商 | 用途 |
|------|------|------|
| **Verdi** | Synopsys | 覆盖率分析 |
| **IMC** | Cadence | 覆盖率合并 |
| **Verification Planner** | Synopsys | Vplan管理 |

### 开源工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **Verilator coverage** | 覆盖率 | 配合仿真 |
| **Yosys cover** | 覆盖率 | 基础检查 |

---

## 十一、版本控制工具

| 工具 | 用途 | 推荐 |
|------|------|------|
| **Git** | 版本控制 | ✅ 必须使用 |
| **Git LFS** | 大文件管理 | ✅ 推荐 |
| **Perforce** | 大规模版本控制 | 企业可选 |

---

## 十二、项目管理工具

| 工具 | 用途 | 推荐 |
|------|------|------|
| **Markdown** | 文档编写 | ✅ 推荐 |
| **Codebeamer** | 需求管理 | 车规项目 |
| **Jira** | 任务跟踪 | 通用项目 |
| **GitHub/GitLab** | Issue跟踪 | 开源项目 |

---

## 十三、工具链选择建议

### 初创/教育项目 (全开源)
```
仿真: Verilator/Icarus
综合: Yosys
物理: OpenROAD
验证: GTKWave
```

### 中小型商业项目 (混合)
```
仿真: VCS/Verilator
Lint: SpyGlass + Verilator
综合: Design Compiler
物理: Innovus
DFT: Tessent
STA: PrimeTime
```

### 大型车规项目 (商业为主)
```
全流程: Synopsys/Cadence 完整流程
DFT: Tessent
验证: VCS + Verdi
项目管理: Codebeamer
```

---

## 十四、工具配置模板

### config.mk 示例
```makefile
# EDA工具配置

# 仿真工具: vcs | xcelium | verilator | iverilog
SIM_TOOL ?= vcs

# 综合工具: dc | genus | yosys
SYNTH_TOOL ?= dc

# 物理工具: innovus | icc2 | openroad
PR_TOOL ?= innovus

# STA工具: pt | tempus | opensta
STA_TOOL ?= pt

# DFT工具: tessent | modus | dftadvisor
DFT_TOOL ?= tessent

# 根据配置设置命令
ifeq ($(SIM_TOOL),vcs)
  SIM_CMD = vcs -sverilog
else ifeq ($(SIM_TOOL),verilator)
  SIM_CMD = verilator --cc --exe
endif
```

---

## 十五、许可证管理

### 商业工具许可证
- 浮动许可证 (FlexLM)
- 许可证服务器配置
- 使用监控

### 开源工具
- 无需许可证
- 社区支持

---

## 十六、相关文档

- `Database/Scripts/config.mk`
- `Database/ToolConfig/`

---

*此文档基于 workflow/SOC_DESIGN_WORKFLOW.md 定义*
*版本: v1.0*
