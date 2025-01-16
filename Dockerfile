# FROM python:3.12-slim-bookworm
# RUN apt-get update && \
#    apt-get install -y curl && \
#    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
#    apt-get install -y nodejs && \
#    apt-get clean && \
#    rm -rf /var/lib/apt/lists/*

# docker build . -t registry.cn-shenzhen.aliyuncs.com/docker-mirror2/python-node:3.12-20

FROM registry.cn-shenzhen.aliyuncs.com/docker-mirror2/python-node:3.12-20

ENV PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple


# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install -r requirements.txt

# 复制应用代码和启动脚本
COPY app/ ./app/
COPY start.sh .

# 创建依赖目录并安装
RUN mkdir -p /dependencies
COPY python-requirements.txt /dependencies
RUN pip install -r /dependencies/python-requirements.txt

# 设置启动脚本权限
RUN chmod +x start.sh

# 暴露端口
EXPOSE 8194

# 使用启动脚本替代直接的 uvicorn 命令
CMD ["./start.sh"]
