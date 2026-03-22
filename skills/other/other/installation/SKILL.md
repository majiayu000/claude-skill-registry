---
name: installation
description: OpenClaw 安装与部署
version: 1.0.0
author: terminal-skills
tags: [openclaw, installation, deployment, setup]
---

# OpenClaw 安装与部署

## 概述
OpenClaw 是一个开源的分布式任务调度和工作流编排平台，本文档涵盖各种环境下的安装部署方法。

## 环境要求

### 系统要求
```bash
# 检查系统版本
cat /etc/os-release
uname -a

# 最低要求
# - CPU: 2 核心
# - 内存: 4GB
# - 磁盘: 20GB
# - 操作系统: Linux (CentOS 7+, Ubuntu 18.04+, Debian 10+)

# 检查资源
free -h
df -h
nproc
```

### 依赖检查
```bash
# 检查 Docker
docker --version
docker info

# 检查 Docker Compose
docker-compose --version

# 检查 Java (如需原生安装)
java -version

# 检查 Python
python3 --version
pip3 --version
```

## Docker 方式安装（推荐）

### 单机部署
```bash
# 创建工作目录
mkdir -p /opt/openclaw && cd /opt/openclaw

# 下载 docker-compose.yml
curl -fsSL https://raw.githubusercontent.com/openclaw/openclaw/main/docker-compose.yml -o docker-compose.yml

# 创建必要目录
mkdir -p {data,logs,config}

# 启动服务
docker-compose up -d

# 查看状态
docker-compose ps
docker-compose logs -f
```

### 自定义配置
```yaml
# docker-compose.yml
version: '3.8'

services:
  openclaw-server:
    image: openclaw/openclaw-server:latest
    container_name: openclaw-server
    ports:
      - "8080:8080"
      - "9090:9090"
    environment:
      - OPENCLAW_DB_HOST=openclaw-db
      - OPENCLAW_DB_PORT=3306
      - OPENCLAW_DB_NAME=openclaw
      - OPENCLAW_DB_USER=openclaw
      - OPENCLAW_DB_PASSWORD=${DB_PASSWORD:-openclaw123}
      - OPENCLAW_REDIS_HOST=openclaw-redis
      - OPENCLAW_REDIS_PORT=6379
      - JAVA_OPTS=-Xms1g -Xmx2g
    volumes:
      - ./data:/opt/openclaw/data
      - ./logs:/opt/openclaw/logs
      - ./config:/opt/openclaw/config
    depends_on:
      - openclaw-db
      - openclaw-redis
    restart: unless-stopped

  openclaw-worker:
    image: openclaw/openclaw-worker:latest
    container_name: openclaw-worker
    environment:
      - OPENCLAW_SERVER_HOST=openclaw-server
      - OPENCLAW_SERVER_PORT=9090
      - WORKER_GROUP=default
      - WORKER_THREADS=8
    volumes:
      - ./logs:/opt/openclaw/logs
    depends_on:
      - openclaw-server
    restart: unless-stopped
    deploy:
      replicas: 2

  openclaw-db:
    image: mysql:8.0
    container_name: openclaw-db
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASSWORD:-root123}
      - MYSQL_DATABASE=openclaw
      - MYSQL_USER=openclaw
      - MYSQL_PASSWORD=${DB_PASSWORD:-openclaw123}
    volumes:
      - ./data/mysql:/var/lib/mysql
    restart: unless-stopped

  openclaw-redis:
    image: redis:7-alpine
    container_name: openclaw-redis
    command: redis-server --appendonly yes
    volumes:
      - ./data/redis:/data
    restart: unless-stopped
```

### 环境变量配置
```bash
# 创建 .env 文件
cat > .env << 'EOF'
# 数据库配置
DB_ROOT_PASSWORD=your_root_password
DB_PASSWORD=your_db_password

# 服务配置
OPENCLAW_PORT=8080
OPENCLAW_GRPC_PORT=9090

# 日志级别
LOG_LEVEL=INFO
EOF

# 启动时加载
docker-compose --env-file .env up -d
```

## Kubernetes 部署

### Helm 安装
```bash
# 添加 Helm 仓库
helm repo add openclaw https://charts.openclaw.io
helm repo update

# 查看可用版本
helm search repo openclaw

# 安装（默认配置）
helm install openclaw openclaw/openclaw -n openclaw --create-namespace

# 安装（自定义配置）
helm install openclaw openclaw/openclaw \
  -n openclaw --create-namespace \
  -f values.yaml

# 查看状态
kubectl get pods -n openclaw
kubectl get svc -n openclaw
```

### values.yaml 示例
```yaml
# values.yaml
server:
  replicaCount: 2
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"

worker:
  replicaCount: 3
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "500m"

mysql:
  enabled: true
  auth:
    rootPassword: "your_root_password"
    database: openclaw
    username: openclaw
    password: "your_password"
  primary:
    persistence:
      size: 20Gi

redis:
  enabled: true
  architecture: standalone
  auth:
    enabled: false

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: openclaw.example.com
      paths:
        - path: /
          pathType: Prefix
```

### 手动 YAML 部署
```bash
# 创建命名空间
kubectl create namespace openclaw

# 应用配置
kubectl apply -f https://raw.githubusercontent.com/openclaw/openclaw/main/deploy/kubernetes/ -n openclaw

# 或本地文件
kubectl apply -f openclaw-deployment.yaml -n openclaw

# 查看部署状态
kubectl get all -n openclaw
kubectl describe deployment openclaw-server -n openclaw
```

## 原生安装

### 下载安装包
```bash
# 下载最新版本
OPENCLAW_VERSION=$(curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest | grep tag_name | cut -d '"' -f 4)
wget https://github.com/openclaw/openclaw/releases/download/${OPENCLAW_VERSION}/openclaw-${OPENCLAW_VERSION}.tar.gz

# 解压
tar -xzf openclaw-${OPENCLAW_VERSION}.tar.gz -C /opt/
mv /opt/openclaw-${OPENCLAW_VERSION} /opt/openclaw
cd /opt/openclaw
```

### 初始化数据库
```bash
# 创建数据库
mysql -u root -p << 'EOF'
CREATE DATABASE IF NOT EXISTS openclaw DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'openclaw'@'%' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON openclaw.* TO 'openclaw'@'%';
FLUSH PRIVILEGES;
EOF

# 导入初始数据
mysql -u openclaw -p openclaw < /opt/openclaw/sql/init.sql
```

### 配置并启动
```bash
# 编辑配置
vim /opt/openclaw/conf/application.yml

# 启动服务
/opt/openclaw/bin/openclaw-server.sh start
/opt/openclaw/bin/openclaw-worker.sh start

# 查看状态
/opt/openclaw/bin/openclaw-server.sh status
/opt/openclaw/bin/openclaw-worker.sh status

# 查看日志
tail -f /opt/openclaw/logs/openclaw-server.log
```

### Systemd 服务
```bash
# 创建 Server 服务
cat > /etc/systemd/system/openclaw-server.service << 'EOF'
[Unit]
Description=OpenClaw Server
After=network.target mysql.service redis.service

[Service]
Type=forking
User=openclaw
Group=openclaw
Environment=JAVA_HOME=/usr/lib/jvm/java-11
ExecStart=/opt/openclaw/bin/openclaw-server.sh start
ExecStop=/opt/openclaw/bin/openclaw-server.sh stop
ExecReload=/opt/openclaw/bin/openclaw-server.sh restart
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 创建 Worker 服务
cat > /etc/systemd/system/openclaw-worker.service << 'EOF'
[Unit]
Description=OpenClaw Worker
After=network.target openclaw-server.service

[Service]
Type=forking
User=openclaw
Group=openclaw
Environment=JAVA_HOME=/usr/lib/jvm/java-11
ExecStart=/opt/openclaw/bin/openclaw-worker.sh start
ExecStop=/opt/openclaw/bin/openclaw-worker.sh stop
ExecReload=/opt/openclaw/bin/openclaw-worker.sh restart
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 启用并启动
systemctl daemon-reload
systemctl enable openclaw-server openclaw-worker
systemctl start openclaw-server openclaw-worker
systemctl status openclaw-server openclaw-worker
```

## 安装验证

### 健康检查
```bash
# API 健康检查
curl -s http://localhost:8080/api/health | jq .

# 组件状态
curl -s http://localhost:8080/api/status | jq .

# 集群信息
curl -s http://localhost:8080/api/cluster/info | jq .
```

### 访问 Web UI
```bash
# 默认访问地址
# http://localhost:8080

# 默认管理员账号
# 用户名: admin
# 密码: admin123 (首次登录后请修改)

# 测试登录
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## 升级指南

### Docker 升级
```bash
# 备份数据
docker-compose exec openclaw-db mysqldump -u openclaw -p openclaw > backup.sql

# 拉取新版本
docker-compose pull

# 重启服务
docker-compose down
docker-compose up -d

# 验证
docker-compose ps
curl -s http://localhost:8080/api/health
```

### Kubernetes 升级
```bash
# Helm 升级
helm upgrade openclaw openclaw/openclaw -n openclaw

# 查看升级状态
kubectl rollout status deployment/openclaw-server -n openclaw

# 回滚（如需要）
helm rollback openclaw -n openclaw
```

## 卸载

### Docker 卸载
```bash
# 停止并删除容器
docker-compose down

# 删除数据（谨慎）
docker-compose down -v
rm -rf /opt/openclaw

# 删除镜像
docker rmi $(docker images openclaw/* -q)
```

### Kubernetes 卸载
```bash
# Helm 卸载
helm uninstall openclaw -n openclaw

# 删除命名空间
kubectl delete namespace openclaw

# 清理 PVC（谨慎）
kubectl delete pvc --all -n openclaw
```

## 安装问题排查

| 问题 | 可能原因 | 解决方法 |
|------|----------|----------|
| 端口被占用 | 其他服务占用 | `netstat -tlnp \| grep 8080` |
| 数据库连接失败 | 配置错误/网络问题 | 检查连接配置和网络 |
| 内存不足 | JVM 配置过大 | 调整 JAVA_OPTS |
| 权限问题 | 目录权限不足 | `chown -R openclaw:openclaw /opt/openclaw` |
| Worker 无法注册 | Server 未启动/网络问题 | 检查 Server 状态和网络连通性 |
