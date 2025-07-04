# 使用官方 Python 基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如 gcc 用于编译依赖库）
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     && rm -rf /var/lib/apt/lists/*

# 复制项目文件到容器中
COPY . /app

# 设置国内源并安装 Python 依赖
RUN pip config set global.index-url https://mirrors.ustc.edu.cn/pypi/web/simple && \
    pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 默认端口
EXPOSE 5000

# 设定启动命令（默认 app.py）
CMD ["python", "app.py"]
