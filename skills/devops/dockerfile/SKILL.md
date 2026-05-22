---
name: dockerfile
description: Dockerfile 编写最佳实践
version: 1.0.0
author: terminal-skills
tags: [docker, dockerfile, build, best-practices]
---

# Dockerfile 编写

## 概述
Dockerfile 最佳实践、安全扫描等技能。

## 指令详解

### FROM
```dockerfile
# 基础镜像
FROM ubuntu:22.04
FROM node:18-alpine
FROM python:3.11-slim

# 多阶段构建
FROM node:18 AS builder
FROM nginx:alpine AS production

# 使用 ARG 动态指定
ARG BASE_IMAGE=node:18-alpine
FROM ${BASE_IMAGE}
```

### WORKDIR
```dockerfile
# 设置工作目录（推荐使用绝对路径）
WORKDIR /app
WORKDIR /home/node/app

# 多次使用会切换目录
WORKDIR /app
WORKDIR src
# 当前目录: /app/src
```

### COPY 与 ADD
```dockerfile
# COPY（推荐）
COPY package.json ./
COPY src/ ./src/
COPY --chown=node:node . .

# 多文件复制
COPY package.json package-lock.json ./

# ADD（支持 URL 和解压）
ADD https://example.com/file.tar.gz /app/
ADD archive.tar.gz /app/           # 自动解压

# 推荐：优先使用 COPY，除非需要 ADD 的特殊功能
```

### RUN
```dockerfile
# Shell 形式
RUN apt-get update && apt-get install -y curl

# Exec 形式
RUN ["apt-get", "update"]

# 最佳实践：合并命令减少层数
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        wget \
        git && \
    rm -rf /var/lib/apt/lists/*
```

### CMD 与 ENTRYPOINT
```dockerfile
# CMD - 默认命令（可被覆盖）
CMD ["node", "app.js"]
CMD ["npm", "start"]

# ENTRYPOINT - 入口点（不易被覆盖）
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["postgres"]

# 组合使用
ENTRYPOINT ["python"]
CMD ["app.py"]
# 运行: python app.py
# docker run myimage other.py -> python other.py
```

### ENV 与 ARG
```dockerfile
# ENV - 运行时环境变量
ENV NODE_ENV=production
ENV PORT=3000 HOST=0.0.0.0

# ARG - 构建时参数
ARG VERSION=1.0
ARG BUILD_DATE

# ARG 转 ENV
ARG APP_VERSION
ENV APP_VERSION=${APP_VERSION}

# 使用构建参数
# docker build --build-arg VERSION=2.0 .
```

### EXPOSE
```dockerfile
# 声明端口（文档作用）
EXPOSE 80
EXPOSE 443
EXPOSE 3000/tcp
EXPOSE 5000/udp
```

### VOLUME
```dockerfile
# 声明挂载点
VOLUME /data
VOLUME ["/data", "/logs"]
```

### USER
```dockerfile
# 切换用户
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# 或使用 UID
USER 1000:1000
```

### HEALTHCHECK
```dockerfile
# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost/ || exit 1

# 禁用健康检查
HEALTHCHECK NONE
```

## 最佳实践模板

### Node.js 应用
```dockerfile
FROM node:18-alpine

# 创建非 root 用户
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# 先复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm ci --only=production && npm cache clean --force

# 复制源代码
COPY --chown=appuser:appgroup . .

# 切换用户
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "app.js"]
```

### Python 应用
```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 创建非 root 用户
RUN useradd -m -r appuser && chown appuser:appuser /app
USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Go 应用
```dockerfile
# 构建阶段
FROM golang:1.21-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o main .

# 生产阶段
FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/main /main

EXPOSE 8080

ENTRYPOINT ["/main"]
```

### Java 应用
```dockerfile
# 构建阶段
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline

COPY src ./src
RUN mvn package -DskipTests

# 生产阶段
FROM eclipse-temurin:17-jre-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

## .dockerignore

```dockerignore
# Git
.git
.gitignore

# Node
node_modules
npm-debug.log

# Python
__pycache__
*.pyc
.venv
venv

# IDE
.idea
.vscode
*.swp

# Docker
Dockerfile*
docker-compose*
.dockerignore

# 文档
*.md
LICENSE

# 测试
test
tests
coverage

# 其他
.env
.env.*
*.log
tmp
```

## 安全检查

### 镜像扫描
```bash
# Docker Scout
docker scout cves myimage:tag
docker scout recommendations myimage:tag

# Trivy
trivy image myimage:tag

# Snyk
snyk container test myimage:tag
```

### Dockerfile 检查
```bash
# Hadolint
docker run --rm -i hadolint/hadolint < Dockerfile

# Dockle
dockle myimage:tag
```

## 常见场景

### 场景 1：入口脚本
```dockerfile
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["app"]
```

```bash
#!/bin/bash
set -e

# 初始化逻辑
if [ "$1" = 'app' ]; then
    # 等待依赖服务
    until nc -z db 5432; do
        echo "Waiting for database..."
        sleep 1
    done
fi

exec "$@"
```

### 场景 2：多架构构建
```bash
# 创建 builder
docker buildx create --name mybuilder --use

# 多架构构建并推送
docker buildx build --platform linux/amd64,linux/arm64 \
    -t myrepo/myimage:tag --push .
```

### 场景 3：构建缓存
```bash
# 使用 BuildKit 缓存
docker build --build-arg BUILDKIT_INLINE_CACHE=1 -t myimage:tag .

# 使用缓存
docker build --cache-from myimage:tag -t myimage:new .
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 构建慢 | 优化 COPY 顺序、使用缓存 |
| 镜像大 | 多阶段构建、精简基础镜像 |
| 权限问题 | 检查 USER、文件权限 |
| 依赖问题 | 检查网络、使用国内镜像源 |
