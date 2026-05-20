---
name: networking
description: Docker 容器网络
version: 1.0.0
author: terminal-skills
tags: [docker, networking, bridge, overlay]
---

# Docker 容器网络

## 概述
容器网络模式、跨主机通信等技能。

## 网络驱动

### 网络类型
```bash
# bridge（默认）- 单主机容器通信
# host - 共享主机网络
# none - 无网络
# overlay - 跨主机通信（Swarm）
# macvlan - 分配 MAC 地址
```

### 查看网络
```bash
# 列出网络
docker network ls

# 网络详情
docker network inspect bridge
docker network inspect network_name

# 查看容器网络
docker inspect container_name --format '{{json .NetworkSettings.Networks}}'
```

## Bridge 网络

### 默认 bridge
```bash
# 容器使用默认 bridge
docker run -d --name web nginx

# 查看 IP
docker inspect web --format '{{.NetworkSettings.IPAddress}}'

# 默认 bridge 容器间通过 IP 通信
# 不支持容器名解析
```

### 自定义 bridge
```bash
# 创建网络
docker network create mynet
docker network create --driver bridge --subnet 172.20.0.0/16 mynet

# 使用自定义网络
docker run -d --name web --network mynet nginx
docker run -d --name api --network mynet myapi

# 自定义网络支持容器名解析
docker exec api ping web
```

### 连接多个网络
```bash
# 创建网络
docker network create frontend
docker network create backend

# 容器连接多个网络
docker run -d --name app --network frontend myapp
docker network connect backend app

# 断开网络
docker network disconnect frontend app
```

## Host 网络

```bash
# 使用主机网络
docker run -d --network host nginx

# 容器直接使用主机端口
# 无需端口映射
# 性能最好，但端口可能冲突
```

## None 网络

```bash
# 无网络
docker run -d --network none myapp

# 完全隔离，无网络访问
# 适用于安全敏感场景
```

## 端口映射

```bash
# 映射端口
docker run -d -p 8080:80 nginx              # HOST:CONTAINER
docker run -d -p 80:80 -p 443:443 nginx     # 多端口
docker run -d -p 127.0.0.1:8080:80 nginx    # 绑定特定 IP
docker run -d -P nginx                       # 随机端口

# 查看端口映射
docker port container_name
```

## DNS 配置

```bash
# 自定义 DNS
docker run -d --dns 8.8.8.8 nginx
docker run -d --dns 8.8.8.8 --dns 8.8.4.4 nginx

# 自定义主机名
docker run -d --hostname myhost nginx

# 添加 hosts 记录
docker run -d --add-host db:192.168.1.100 nginx
```

## 网络别名

```bash
# 创建网络
docker network create mynet

# 使用别名
docker run -d --name web --network mynet --network-alias webserver nginx

# 其他容器可通过别名访问
docker run --rm --network mynet busybox ping webserver
```

## Overlay 网络（Swarm）

```bash
# 初始化 Swarm
docker swarm init

# 创建 overlay 网络
docker network create -d overlay myoverlay

# 创建可附加的 overlay（非 Swarm 服务也可使用）
docker network create -d overlay --attachable myoverlay

# 在服务中使用
docker service create --name web --network myoverlay nginx
```

## Macvlan 网络

```bash
# 创建 macvlan 网络
docker network create -d macvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o parent=eth0 \
    mymacvlan

# 使用 macvlan
docker run -d --network mymacvlan --ip 192.168.1.100 nginx

# 容器获得独立 MAC 地址，可直接在物理网络通信
```

## 网络诊断

### 容器内诊断
```bash
# 进入容器
docker exec -it container_name sh

# 网络工具
apt-get update && apt-get install -y iputils-ping curl netcat-openbsd

# 或使用 netshoot
docker run -it --network container:target_container nicolaka/netshoot
```

### 常用诊断命令
```bash
# 查看容器 IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name

# 查看网络中的容器
docker network inspect mynet -f '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{"\n"}}{{end}}'

# 测试连通性
docker exec container1 ping container2
docker exec container1 curl http://container2:80
```

## 常见场景

### 场景 1：容器间通信
```bash
# 创建网络
docker network create app-network

# 启动数据库
docker run -d --name db --network app-network postgres

# 启动应用（通过容器名访问数据库）
docker run -d --name app --network app-network \
    -e DATABASE_URL=postgres://db:5432/mydb \
    myapp
```

### 场景 2：隔离前后端
```bash
# 创建网络
docker network create frontend
docker network create backend

# 前端只在 frontend
docker run -d --name nginx --network frontend -p 80:80 nginx

# 后端连接两个网络
docker run -d --name api --network frontend myapi
docker network connect backend api

# 数据库只在 backend
docker run -d --name db --network backend postgres
```

### 场景 3：调试网络问题
```bash
# 使用 netshoot 调试
docker run -it --rm --network container:target nicolaka/netshoot

# 常用命令
ip addr
ss -tlnp
curl -v http://service:port
tcpdump -i eth0
nslookup service_name
```

### 场景 4：限制网络带宽
```bash
# 使用 tc 限制带宽（需要 NET_ADMIN 权限）
docker run -d --cap-add NET_ADMIN myapp

# 在容器内
tc qdisc add dev eth0 root tbf rate 1mbit burst 32kbit latency 400ms
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 容器间无法通信 | 检查是否在同一网络 |
| DNS 解析失败 | 检查是否使用自定义网络 |
| 端口无法访问 | 检查端口映射、防火墙 |
| 网络性能差 | 考虑使用 host 网络 |

```bash
# 检查网络配置
docker network inspect network_name

# 检查容器网络
docker inspect container_name | jq '.[0].NetworkSettings'

# 检查 iptables 规则
iptables -L -n -t nat
```
