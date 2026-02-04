---
name: image-management
description: Docker 镜像管理
version: 1.0.0
author: terminal-skills
tags: [docker, image, registry, build]
---

# Docker 镜像管理

## 概述
镜像构建、多阶段构建、镜像优化等技能。

## 镜像操作

### 查看镜像
```bash
# 列出镜像
docker images
docker images -a                    # 包含中间层
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"

# 镜像详情
docker inspect image_name
docker history image_name           # 构建历史

# 搜索镜像
docker search nginx
```

### 拉取与推送
```bash
# 拉取镜像
docker pull nginx
docker pull nginx:1.20
docker pull registry.example.com/myapp:latest

# 推送镜像
docker push myrepo/myimage:tag

# 登录仓库
docker login
docker login registry.example.com
docker logout
```

### 镜像标签
```bash
# 添加标签
docker tag source_image:tag target_image:tag
docker tag myapp:latest myrepo/myapp:v1.0

# 删除镜像
docker rmi image_name
docker rmi -f image_name            # 强制删除
docker image prune                  # 删除悬空镜像
docker image prune -a               # 删除未使用镜像
```

### 导入导出
```bash
# 导出镜像
docker save -o myimage.tar myimage:tag
docker save myimage:tag | gzip > myimage.tar.gz

# 导入镜像
docker load -i myimage.tar
docker load < myimage.tar.gz
```

## 镜像构建

### 基础构建
```bash
# 构建镜像
docker build -t myimage:tag .
docker build -t myimage:tag -f Dockerfile.prod .

# 指定构建参数
docker build --build-arg VERSION=1.0 -t myimage:tag .

# 不使用缓存
docker build --no-cache -t myimage:tag .

# 指定目标阶段
docker build --target builder -t myimage:builder .
```

### Dockerfile 基础
```dockerfile
# 基础镜像
FROM node:18-alpine

# 元数据
LABEL maintainer="your@email.com"
LABEL version="1.0"

# 设置工作目录
WORKDIR /app

# 复制文件
COPY package*.json ./
COPY . .

# 运行命令
RUN npm install

# 环境变量
ENV NODE_ENV=production
ENV PORT=3000

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["node", "app.js"]
```

### 多阶段构建
```dockerfile
# 构建阶段
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 生产阶段
FROM node:18-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

### Go 应用多阶段构建
```dockerfile
# 构建阶段
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# 生产阶段
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
```

## 镜像优化

### 减小镜像体积
```dockerfile
# 1. 使用精简基础镜像
FROM alpine:latest
FROM node:18-alpine
FROM python:3.11-slim

# 2. 合并 RUN 命令
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        package1 \
        package2 && \
    rm -rf /var/lib/apt/lists/*

# 3. 使用 .dockerignore
# .dockerignore 文件
node_modules
.git
*.md
Dockerfile
.dockerignore

# 4. 多阶段构建只复制必要文件
COPY --from=builder /app/dist ./dist
```

### 构建缓存优化
```dockerfile
# 先复制依赖文件，利用缓存
COPY package*.json ./
RUN npm ci

# 再复制源代码
COPY . .
RUN npm run build
```

### 安全最佳实践
```dockerfile
# 1. 使用非 root 用户
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# 2. 固定版本
FROM node:18.17.0-alpine3.18

# 3. 扫描漏洞
# docker scan myimage:tag

# 4. 最小权限
RUN chmod 500 /app/main
```

## 私有仓库

### 搭建私有仓库
```bash
# 运行 Registry
docker run -d -p 5000:5000 --name registry registry:2

# 推送到私有仓库
docker tag myimage:tag localhost:5000/myimage:tag
docker push localhost:5000/myimage:tag

# 拉取
docker pull localhost:5000/myimage:tag
```

### 配置认证
```bash
# 创建密码文件
htpasswd -Bc /auth/htpasswd admin

# 运行带认证的 Registry
docker run -d -p 5000:5000 \
  -v /auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  registry:2
```

## 常见场景

### 场景 1：分析镜像层
```bash
# 查看镜像层
docker history myimage:tag --no-trunc

# 使用 dive 分析
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  wagoodman/dive:latest myimage:tag
```

### 场景 2：清理磁盘空间
```bash
# 查看磁盘使用
docker system df
docker system df -v

# 清理未使用资源
docker system prune              # 清理悬空资源
docker system prune -a           # 清理所有未使用资源
docker system prune --volumes    # 包括卷
```

### 场景 3：镜像漏洞扫描
```bash
# Docker Scout
docker scout cves myimage:tag

# Trivy
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image myimage:tag
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 构建失败 | 检查 Dockerfile 语法、网络 |
| 镜像过大 | 使用多阶段构建、精简基础镜像 |
| 拉取失败 | 检查网络、认证、镜像名 |
| 缓存失效 | 检查 COPY 顺序、文件变更 |
