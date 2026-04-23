# templates/docker/Dockerfile - Coding Yang Agent 容器模板

FROM ubuntu:22.04

# 基础工具
RUN apt-get update && apt-get install -y \
    git \
    make \
    python3 \
    python3-pip \
    python3-websockets \
    wget \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# 开源EDA工具
RUN apt-get update && apt-get install -y \
    iverilog \
    verilator \
    yosys \
    gtkwave \
    && rm -rf /var/lib/apt/lists/*

# OpenROAD (需手动安装或替换为预编译包)
# RUN wget -q https://github.com/The-OpenROAD-Project/OpenROAD/releases/download/v2.0/openroad_2.0_amd64.deb \
#     && dpkg -i openroad_2.0_amd64.deb \
#     && rm openroad_2.0_amd64.deb

# Agent代码
COPY agent/ /opt/coding-yang/
WORKDIR /opt/coding-yang

# 启动脚本
ENTRYPOINT ["python3", "agent.py"]
