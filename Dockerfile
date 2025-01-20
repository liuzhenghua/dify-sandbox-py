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
ENV PYTHONPATH=/app

# 安装自身依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装python沙箱执行的代码需要的额外依赖
RUN mkdir -p /dependencies
COPY python-requirements.txt /dependencies
RUN pip install --no-cache-dir -r /dependencies/python-requirements.txt

# 复制文件
COPY start.sh .
COPY api ./api
COPY config ./config
COPY core ./core
COPY main.py .

# 设置启动脚本权限
RUN chmod +x start.sh

# 暴露端口
EXPOSE 8194

# 使用启动脚本替代直接的 uvicorn 命令
CMD ["./start.sh"]
