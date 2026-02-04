---
name: load-balancer
description: 负载均衡配置
version: 1.0.0
author: terminal-skills
tags: [networking, load-balancer, haproxy, nginx, lb]
---

# 负载均衡配置

## 概述
HAProxy、Nginx LB、健康检查配置等技能。

## HAProxy

### 安装与管理
```bash
# 安装
apt install haproxy                   # Debian/Ubuntu
yum install haproxy                   # CentOS/RHEL

# 服务管理
systemctl start haproxy
systemctl enable haproxy
systemctl reload haproxy

# 检查配置
haproxy -c -f /etc/haproxy/haproxy.cfg
```

### 基础配置
```bash
# /etc/haproxy/haproxy.cfg
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon
    maxconn 4096

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000
    errorfile 400 /etc/haproxy/errors/400.http
    errorfile 403 /etc/haproxy/errors/403.http
    errorfile 408 /etc/haproxy/errors/408.http
    errorfile 500 /etc/haproxy/errors/500.http
    errorfile 502 /etc/haproxy/errors/502.http
    errorfile 503 /etc/haproxy/errors/503.http
    errorfile 504 /etc/haproxy/errors/504.http
```

### HTTP 负载均衡
```bash
frontend http_front
    bind *:80
    default_backend http_back
    
    # ACL 规则
    acl is_api path_beg /api
    use_backend api_back if is_api

backend http_back
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    
    server web1 192.168.1.10:8080 check weight 3
    server web2 192.168.1.11:8080 check weight 2
    server web3 192.168.1.12:8080 check backup

backend api_back
    balance leastconn
    option httpchk GET /api/health
    
    server api1 192.168.1.20:8080 check
    server api2 192.168.1.21:8080 check
```

### TCP 负载均衡
```bash
frontend mysql_front
    bind *:3306
    mode tcp
    default_backend mysql_back

backend mysql_back
    mode tcp
    balance roundrobin
    option mysql-check user haproxy
    
    server mysql1 192.168.1.30:3306 check
    server mysql2 192.168.1.31:3306 check backup
```

### HTTPS 终止
```bash
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/example.pem
    mode http
    
    # 重定向 HTTP 到 HTTPS
    http-request redirect scheme https unless { ssl_fc }
    
    default_backend http_back

frontend http_front
    bind *:80
    mode http
    redirect scheme https code 301
```

### 统计页面
```bash
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats auth admin:password
    stats admin if TRUE
```

### 负载均衡算法
```bash
# 轮询（默认）
balance roundrobin

# 最少连接
balance leastconn

# 源 IP 哈希
balance source

# URI 哈希
balance uri

# 首个可用
balance first
```

## Nginx 负载均衡

### 基础配置
```nginx
# /etc/nginx/nginx.conf
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080 backup;
}

server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 负载均衡方法
```nginx
# 轮询（默认）
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

# 权重
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=1;
}

# IP 哈希
upstream backend {
    ip_hash;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

# 最少连接
upstream backend {
    least_conn;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

# 哈希
upstream backend {
    hash $request_uri consistent;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}
```

### 健康检查
```nginx
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
}

# Nginx Plus 主动健康检查
upstream backend {
    zone backend 64k;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

server {
    location / {
        proxy_pass http://backend;
        health_check interval=5s fails=3 passes=2;
    }
}
```

### 会话保持
```nginx
# IP 哈希
upstream backend {
    ip_hash;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

# Cookie（Nginx Plus）
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
    sticky cookie srv_id expires=1h;
}
```

## 常见场景

### 场景 1：蓝绿部署
```bash
# HAProxy
backend blue
    server blue1 192.168.1.10:8080 check
    server blue2 192.168.1.11:8080 check

backend green
    server green1 192.168.1.20:8080 check
    server green2 192.168.1.21:8080 check

frontend http_front
    bind *:80
    # 切换后端
    use_backend green
```

### 场景 2：金丝雀发布
```bash
# HAProxy - 10% 流量到新版本
frontend http_front
    bind *:80
    acl canary rand(100) lt 10
    use_backend canary_back if canary
    default_backend stable_back

backend stable_back
    server stable1 192.168.1.10:8080 check

backend canary_back
    server canary1 192.168.1.20:8080 check
```

### 场景 3：基于路径的路由
```nginx
upstream api {
    server 192.168.1.10:8080;
}

upstream web {
    server 192.168.1.20:8080;
}

server {
    listen 80;
    
    location /api {
        proxy_pass http://api;
    }
    
    location / {
        proxy_pass http://web;
    }
}
```

### 场景 4：限流
```bash
# HAProxy
frontend http_front
    bind *:80
    stick-table type ip size 100k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 后端不可用 | 检查健康检查、后端服务 |
| 连接超时 | 检查超时配置、网络 |
| 会话丢失 | 检查会话保持配置 |
| 负载不均 | 检查权重、算法配置 |

```bash
# HAProxy 统计
echo "show stat" | socat stdio /run/haproxy/admin.sock
echo "show servers state" | socat stdio /run/haproxy/admin.sock

# 查看后端状态
curl http://localhost:8404/stats

# Nginx 状态
curl http://localhost/nginx_status
```
