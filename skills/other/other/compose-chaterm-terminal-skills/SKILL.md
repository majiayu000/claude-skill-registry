---
name: compose
description: Docker Compose 编排
version: 1.0.0
author: terminal-skills
tags: [docker, compose, orchestration, multi-container]
---

# Docker Compose 编排

## 概述
多容器编排、环境变量、网络配置等技能。

## 基础命令

```bash
# 启动服务
docker compose up
docker compose up -d                # 后台运行
docker compose up --build           # 重新构建

# 停止服务
docker compose down
docker compose down -v              # 同时删除卷
docker compose down --rmi all       # 同时删除镜像

# 查看状态
docker compose ps
docker compose ps -a

# 查看日志
docker compose logs
docker compose logs -f              # 实时跟踪
docker compose logs service_name

# 执行命令
docker compose exec service_name sh
docker compose run service_name command

# 重启服务
docker compose restart
docker compose restart service_name

# 扩缩容
docker compose up -d --scale web=3
```

## 配置文件

### 基础结构
```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - api

  api:
    build: ./api
    environment:
      - DATABASE_URL=postgres://db:5432/mydb
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret

volumes:
  db_data:

networks:
  default:
    driver: bridge
```

### 服务配置详解

#### build
```yaml
services:
  app:
    # 简单形式
    build: ./app
    
    # 完整形式
    build:
      context: ./app
      dockerfile: Dockerfile.prod
      args:
        - VERSION=1.0
      target: production
      cache_from:
        - myapp:cache
```

#### ports
```yaml
services:
  web:
    ports:
      - "80:80"                     # HOST:CONTAINER
      - "443:443"
      - "8080-8090:8080-8090"       # 端口范围
      - "127.0.0.1:3000:3000"       # 绑定特定 IP
```

#### volumes
```yaml
services:
  app:
    volumes:
      # 命名卷
      - data:/var/lib/data
      # 绑定挂载
      - ./config:/etc/app/config:ro
      # 匿名卷
      - /var/lib/data

volumes:
  data:
    driver: local
```

#### environment
```yaml
services:
  app:
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgres://localhost/db
    # 或使用映射形式
    environment:
      NODE_ENV: production
      DATABASE_URL: postgres://localhost/db
    # 从文件加载
    env_file:
      - .env
      - .env.local
```

#### depends_on
```yaml
services:
  web:
    depends_on:
      - db
      - redis
    # 带条件
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
```

#### healthcheck
```yaml
services:
  web:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

#### deploy（Swarm 模式）
```yaml
services:
  web:
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
```

## 网络配置

### 自定义网络
```yaml
services:
  frontend:
    networks:
      - frontend
  
  backend:
    networks:
      - frontend
      - backend
  
  db:
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true              # 内部网络，无外部访问
```

### 网络别名
```yaml
services:
  db:
    networks:
      backend:
        aliases:
          - database
          - postgres
```

## 环境变量

### .env 文件
```bash
# .env
POSTGRES_VERSION=15
POSTGRES_PASSWORD=secret
APP_PORT=3000
```

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:${POSTGRES_VERSION}
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  
  app:
    ports:
      - "${APP_PORT}:3000"
```

### 多环境配置
```bash
# docker-compose.override.yml（开发环境，自动加载）
# docker-compose.prod.yml（生产环境）

# 使用多个配置文件
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

```yaml
# docker-compose.yml（基础配置）
services:
  app:
    image: myapp:latest

# docker-compose.override.yml（开发覆盖）
services:
  app:
    build: .
    volumes:
      - .:/app
    environment:
      - DEBUG=true

# docker-compose.prod.yml（生产覆盖）
services:
  app:
    restart: always
    environment:
      - DEBUG=false
```

## 常见场景

### 场景 1：Web 应用栈
```yaml
version: "3.9"

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - app

  app:
    build: .
    environment:
      - DATABASE_URL=postgres://postgres:secret@db:5432/mydb
      - REDIS_URL=redis://redis:6379
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: mydb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 场景 2：开发环境热重载
```yaml
version: "3.9"

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules          # 排除 node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
    ports:
      - "3000:3000"
```

### 场景 3：数据库初始化
```yaml
services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    environment:
      POSTGRES_PASSWORD: secret
```

### 场景 4：日志配置
```yaml
services:
  app:
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

## 故障排查

```bash
# 查看配置
docker compose config

# 查看服务日志
docker compose logs service_name --tail=100

# 进入容器
docker compose exec service_name sh

# 查看网络
docker network ls
docker network inspect project_default

# 重建服务
docker compose up -d --force-recreate service_name
```

| 问题 | 排查方法 |
|------|----------|
| 服务无法启动 | `docker compose logs`, 检查依赖 |
| 网络不通 | 检查网络配置、服务名 |
| 卷挂载问题 | 检查路径、权限 |
| 环境变量未生效 | `docker compose config` 验证 |
