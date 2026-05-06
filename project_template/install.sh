#!/bin/bash
# project_template/install.sh - SoC/IP 芯片设计项目初始化脚本
# 生成符合 SOC_DESIGN_WORKFLOW.md 标准的项目骨架

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"

# 默认值
PROJECT_NAME="${1:-""}"
CURRENT_PHASE="${2:-"PAD"}"
PROCESS_NODE="${3:-"22nm"}"
ASIL_LEVEL="${4:-"ASIL-B"}"

# 交互式输入
if [ -z "$PROJECT_NAME" ]; then
    read -rp "项目名称 (如 ethernet_controller): " PROJECT_NAME
fi

if [ -z "$CURRENT_PHASE" ]; then
    echo "当前设计阶段:"
    select phase in PAD EDR IDR FDR PostSilicon; do
        CURRENT_PHASE="$phase"
        break
    done
fi

# 创建项目目录
PROJECT_DIR="$PWD/$PROJECT_NAME"
echo "=========================================="
echo "创建项目: $PROJECT_NAME"
echo "路径: $PROJECT_DIR"
echo "阶段: $CURRENT_PHASE"
echo "工艺: $PROCESS_NODE"
echo "ASIL: $ASIL_LEVEL"
echo "=========================================="

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# 创建三级目录结构
echo "[1/6] 创建目录结构..."
mkdir -p ProjectMgmt/{Planning,Tasks/{AI_Yang,Coding_Yang,Design_Agent,Verification_Agent,DFT_Agent,FuSa_Engineer,IP_Architect,System_Architect,PM_Agent},Reviews,Bugs,MeetingMinutes}
mkdir -p Database/{Docs/{Arch,Design,FuSa,Verification},DesignData,Verification,Scripts}
mkdir -p Temp

# 复制模板文件
echo "[2/6] 复制模板文件..."

# AGENTS.md - 项目级行为约束
cp "$TEMPLATES_DIR/AGENTS.md" ./AGENTS.md
sed -i "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" ./AGENTS.md
sed -i "s/{{CURRENT_PHASE}}/$CURRENT_PHASE/g" ./AGENTS.md
sed -i "s/{{PROCESS_NODE}}/$PROCESS_NODE/g" ./AGENTS.md
sed -i "s/{{ASIL_LEVEL}}/$ASIL_LEVEL/g" ./AGENTS.md

# .gitignore
cp "$TEMPLATES_DIR/pm/dot_gitignore_template" ./.gitignore

# README.md
cat > README.md <<EOF
# $PROJECT_NAME

## 项目信息
- **名称**: $PROJECT_NAME
- **当前阶段**: $CURRENT_PHASE
- **工艺节点**: $PROCESS_NODE
- **ASIL等级**: $ASIL_LEVEL
- **创建日期**: $(date -Iseconds)

## 快速开始

### 目录结构
\`\`\`
ProjectMgmt/    # 项目管理（计划、任务、评审、Bug）
Database/       # 设计数据（文档、RTL、验证、脚本）
Temp/           # 临时文件（不提交git）
AGENTS.md       # Coding Yang 行为约束
\`\`\`

### Coding Yang 使用指南
1. 在项目根目录启动 kimi code CLI: \`cd $PROJECT_NAME && kimi\`
2. kimi 会自动加载 \`AGENTS.md\` 中的约束规则
3. 每次任务开始前，确认遵循 AGENTS.md 中的检查清单

## 工作流参考
- [SOC_DESIGN_WORKFLOW.md](../workflow/SOC_DESIGN_WORKFLOW.md)

## 状态
🚧 项目初始化完成，待填充设计内容
EOF

# ProjectMgmt 占位文件
cat > ProjectMgmt/README.md <<EOF
# ProjectMgmt - 项目管理

## 目录
- Planning/ - 项目计划（里程碑、资源、排期）
- Tasks/ - Agent任务清单（按Agent分类）
- Reviews/ - 评审记录（PAD/EDR/IDR/FDR）
- Bugs/ - Bug管理
- MeetingMinutes/ - 会议记录

## 使用方式
各Agent在对应目录下维护任务列表和交付物。
EOF

# Tasks 目录占位
cat > ProjectMgmt/Tasks/Coding_Yang/TASK_LIST.md <<EOF
# Coding Yang - 任务清单

## 待处理

## 进行中

## 已完成

## 规则提醒
每次新任务开始前，回顾 ../AGENTS.md 中的约束规则。
EOF

# Database 占位
cat > Database/README.md <<EOF
# Database - 设计数据

## 目录
- Docs/ - 设计文档
  - Arch/ - 架构文档
  - Design/ - 设计规格
  - FuSa/ - 功能安全文档
  - Verification/ - 验证计划
- DesignData/ - RTL/网表/GDS
- Verification/ - 验证环境
- Scripts/ - EDA脚本

## 文档模板
从 \`sandbox/tools/templates/docs/\` 复制所需模板到对应目录。
EOF

# EDA工具脚本
echo "[3/6] 设置 EDA 工具脚本..."
mkdir -p tools/{cocotb,ghdl,iverilog,verilator}
cp "$TEMPLATES_DIR/scripts/Makefile" tools/Makefile
cp "$TEMPLATES_DIR/scripts/config.mk" tools/config.mk
cp "$TEMPLATES_DIR/scripts/README.md" tools/README.md

# 复制各仿真器脚本
for sim in cocotb ghdl iverilog verilator; do
    if [ -d "$TEMPLATES_DIR/scripts/$sim" ]; then
        cp "$TEMPLATES_DIR/scripts/$sim/"* "tools/$sim/" 2>/dev/null || true
    fi
done

# 设计模板
echo "[4/6] 复制设计模板..."
cp "$TEMPLATES_DIR/design/soc_top.f" design/ 2>/dev/null || true
cp "$TEMPLATES_DIR/design/soc_top_template.sv" design/ 2>/dev/null || true

# PM 模板
echo "[5/6] 复制项目管理模板..."
cp "$TEMPLATES_DIR/pm/Naming_Conventions_Guide.md" ProjectMgmt/ 2>/dev/null || true
cp "$TEMPLATES_DIR/pm/EDA_Tool_Matrix.md" ProjectMgmt/ 2>/dev/null || true

# 完成
echo "[6/6] 项目初始化完成!"
echo ""
echo "=========================================="
echo "项目: $PROJECT_NAME"
echo "=========================================="
echo ""
echo "已生成文件:"
echo "  ✓ AGENTS.md (Coding Yang 行为约束)"
echo "  ✓ README.md"
echo "  ✓ .gitignore"
echo "  ✓ 三级目录结构 (ProjectMgmt/Database/Temp)"
echo "  ✓ EDA工具脚本 (tools/Makefile + 仿真器模板)"
echo ""
echo "下一步:"
echo "  1. cd $PROJECT_NAME"
echo "  2. kimi code cli 启动: kimi"
echo "  3. AGENTS.md 会自动加载到 system prompt"
echo ""
echo "=========================================="
