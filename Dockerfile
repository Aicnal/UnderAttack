FROM python:3.13-slim

LABEL authors="liueic"

# 设置工作目录
WORKDIR /app

# 复制当前目录内容到工作目录
COPY . /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行 Python 脚本
CMD ["python", "main.py"]