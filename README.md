# SoC Project Template

车规级芯片设计项目模板，符合 SOC_DESIGN_WORKFLOW.md 标准目录结构。

## 快速开始

```bash
# 克隆仓库
git clone git@github.com:shenyang-90/tools.git
cd tools/project_template

# 初始化新项目
./install
```

## 目录结构

```
project_template/
├── ProjectMgmt/          # 项目管理
│   ├── Planning/         # 项目计划
│   ├── Reviews/          # 评审记录
│   ├── Bugs/             # Bug管理
│   └── ...
├── Database/             # 设计数据
│   ├── Docs/             # 设计文档
│   ├── DesignData/       # RTL/Netlist/GDS
│   ├── Verification/     # 验证环境
│   └── ...
└── Temp/                 # EDA临时文件
```

## 使用方法

运行 `./install` 后按提示输入：
- 项目类型 (SoC/IP)
- 项目名称
- 工艺节点
- ASIL等级
- 项目经理

将自动生成完整的项目结构，并自动替换模板中的占位符。

## 文档

- [SOC_DESIGN_WORKFLOW.md](../../workflow/SOC_DESIGN_WORKFLOW.md) - 设计工作流参考
