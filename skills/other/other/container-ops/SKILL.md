---
name: container-ops
description: Docker 容器操作与管理
version: 1.0.0
author: terminal-skills
tags: [docker, container, devops]
---

# Docker 容器操作

## 概述
Docker 容器的日常操作，包括生命周期管理、资源限制、日志查看等。

## 容器生命周期

```bash
# 运行容器
docker run -d --name myapp nginx
docker run -it --rm ubuntu bash

# 常用参数
docker run -d \
  --name myapp \
  -p 8080:80 \
  -v /host/path:/container/path \
  -e ENV_VAR=value \
  --restart unless-stopped \
  nginx

# 启停容器
docker start/stop/restart container_name
docker pause/unpause container_name

# 删除容器
docker rm container_name
docker rm -f container_name              # 强制删除
docker container prune                   # 清理停止的容器
```

## 容器查看

```bash
# 列出容器
docker ps                                # 运行中
docker ps -a                             # 所有
docker ps -q                             # 仅 ID
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# 容器详情
docker inspect container_name
docker inspect -f '{{.NetworkSettings.IPAddress}}' container_name

# 资源使用
docker stats
docker stats container_name
docker top container_name
```

## 容器交互

```bash
# 进入容器
docker exec -it container_name /bin/bash
docker exec -it container_name sh

# 执行命令
docker exec container_name ls -la

# 查看日志
docker logs container_name
docker logs -f container_name            # 实时跟踪
docker logs --tail 100 container_name    # 最后 100 行
docker logs --since 1h container_name    # 最近 1 小时
```

## 资源限制

```bash
# 内存限制
docker run -d --memory=512m nginx

# CPU 限制
docker run -d --cpus=1.5 nginx
docker run -d --cpu-shares=512 nginx

# 更新运行中容器
docker update --memory=1g container_name
docker update --cpus=2 container_name
```

## 文件操作

```bash
# 复制文件
docker cp container_name:/path/file ./local
docker cp ./local container_name:/path/

# 查看文件变更
docker diff container_name

# 导出容器
docker export container_name > container.tar
docker import container.tar myimage:tag
```

## 常见场景

### 场景 1：调试容器
```bash
# 1. 查看容器状态
docker inspect container_name | jq '.[0].State'

# 2. 查看日志
docker logs --tail 50 container_name

# 3. 进入容器排查
docker exec -it container_name sh

# 4. 查看进程
docker top container_name
```

### 场景 2：容器无法启动
```bash
# 查看退出原因
docker inspect container_name | jq '.[0].State.ExitCode'
docker inspect container_name | jq '.[0].State.Error'

# 查看日志
docker logs container_name

# 以交互模式启动排查
docker run -it --entrypoint sh image_name
```

### 场景 3：批量操作
```bash
# 停止所有容器
docker stop $(docker ps -q)

# 删除所有停止的容器
docker container prune -f

# 删除所有容器
docker rm -f $(docker ps -aq)
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 容器退出 | `docker logs`, `docker inspect` |
| 网络不通 | `docker network inspect`, 检查端口映射 |
| 磁盘满 | `docker system df`, `docker system prune` |
| 内存溢出 | `docker stats`, 检查 OOMKilled |
| 启动慢 | 检查健康检查配置, 镜像大小 |
