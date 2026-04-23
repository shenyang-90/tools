#!/bin/bash
# templates/scripts/install_coding_yang.sh - Coding Yang Agent 安装脚本模板

set -e

echo "=========================================="
echo "Coding Yang Agent 安装脚本"
echo "=========================================="

# 检查依赖
echo "[1/5] 检查依赖..."
if ! command -v docker &> /dev/null; then
    echo "错误: Docker未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "错误: Docker Compose未安装"
    exit 1
fi

# 配置
WORKSPACE=${1:-"$HOME/workspace"}
OPENCLAW_GATEWAY=${2:-"ws://localhost:8080/agent"}

echo "[2/5] 创建工作目录..."
mkdir -p "$WORKSPACE"
mkdir -p "$WORKSPACE/sandbox"
mkdir -p "$WORKSPACE/eda_tools"

# 生成配置
echo "[3/5] 生成配置..."
cat > .env <<EOF
WORKSPACE=$WORKSPACE
OPENCLAW_GATEWAY=$OPENCLAW_GATEWAY
AGENT_TOKEN=$(openssl rand -hex 32)
LM_LICENSE_FILE=${LM_LICENSE_FILE:-""}
EOF

# 拉取/构建镜像
echo "[4/5] 构建Agent镜像..."
docker-compose build

# 启动
echo "[5/5] 启动Agent..."
docker-compose up -d

echo ""
echo "=========================================="
echo "安装完成!"
echo "=========================================="
echo ""
echo "配置信息:"
echo "  Workspace: $WORKSPACE"
echo "  Gateway:   $OPENCLAW_GATEWAY"
echo ""
echo "常用命令:"
echo "  docker-compose logs -f    # 查看日志"
echo "  docker-compose stop       # 停止Agent"
echo "  docker-compose start      # 启动Agent"
echo ""
