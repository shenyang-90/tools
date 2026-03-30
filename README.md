# Tools - SoC Design Workflow Tools

车规级芯片设计工作流工具集。

## 工具列表

### 🗂️ project_template

**描述**: SoC/IP 芯片设计项目模板  
**用途**: 初始化符合 SOC_DESIGN_WORKFLOW.md 标准的新项目  
**路径**: [`./project_template/`](./project_template/)

```bash
cd project_template
./install
```

**功能**:
- 6个设计阶段完整目录结构 (PCD→PAD→EDR→IDR→FDR→PostSilicon)
- ProjectMgmt: 计划、评审、Bug、会议、里程碑、风险、变更、报告
- Database: 文档、RTL/网表/GDS、验证、固件、EDA脚本
- Temp: EDA临时文件 (已配置 .gitignore)
- 自动占位符替换 (项目名、工艺节点、ASIL等级等)

**文档**: [project_template/README.md](./project_template/README.md)

---

## 添加新工具

1. 在 `tools/` 目录下创建新文件夹
2. 添加该工具的 `README.md`
3. 更新本文件，添加工具介绍

## 快速链接

- [SOC_DESIGN_WORKFLOW.md](../../workflow/SOC_DESIGN_WORKFLOW.md) - 设计工作流参考
