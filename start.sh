#!/bin/bash

# 检查并安装依赖
if [ -f "/dependencies/python-requirements.txt" ]; then
    echo "Dependency file found, starting to install additional dependencies..."
    uv pip install --system -r /dependencies/python-requirements.txt
fi

# 启动 FastAPI 应用
exec python main.py
