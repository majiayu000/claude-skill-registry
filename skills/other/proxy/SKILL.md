---
name: proxy
description: 代理服务器配置
version: 1.0.0
author: terminal-skills
tags: [networking, proxy, squid, nginx, forward-proxy, reverse-proxy]
---

# 代理服务器配置

## 概述
Squid、Nginx 代理、正向/反向代理配置技能。

## Squid 正向代理

### 安装与管理
```bash
# 安装
apt install squid                     # Debian/Ubuntu
yum install squid                     # CentOS/RHEL

# 服务管理
systemctl start squid
systemctl enable squid
systemctl reload squid

# 检查配置
squid -k parse
squid -k check
```

### 基础配置
```bash
# /etc/squid/squid.conf
# 端口配置
http_port 3128

# ACL 定义
acl localnet src 10.0.0.0/8
acl localnet src 172.16.0.0/12
acl localnet src 192.168.0.0/16

acl SSL_ports port 443
acl Safe_ports port 80 21 443 70 210 280 488 591 777 1025-65535

# 访问控制
http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow localnet
http_access deny all

# 缓存配置
cache_dir ufs /var/spool/squid 100 16 256
maximum_object_size 100 MB
cache_mem 256 MB

# 日志
access_log /var/log/squid/access.log squid
cache_log /var/log/squid/cache.log
```

### 认证配置
```bash
# 基础认证
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwd
auth_param basic children 5
auth_param basic realm Squid Proxy
auth_param basic credentialsttl 2 hours

acl authenticated proxy_auth REQUIRED
http_access allow authenticated

# 创建用户
htpasswd -c /etc/squid/passwd user1
htpasswd /etc/squid/passwd user2
```

### 透明代理
```bash
# Squid 配置
http_port 3128 transparent

# iptables 重定向
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128
iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 443 -j REDIRECT --to-port 3128
```

### 访问控制
```bash
# 时间控制
acl work_hours time MTWHF 09:00-18:00
http_access allow localnet work_hours

# 域名黑名单
acl blocked_sites dstdomain .facebook.com .youtube.com
http_access deny blocked_sites

# URL 正则
acl blocked_urls url_regex -i porn adult gambling
http_access deny blocked_urls

# 带宽限制
delay_pools 1
delay_class 1 2
delay_parameters 1 1000000/1000000 100000/100000
delay_access 1 allow localnet
```

## Nginx 反向代理

### 基础反向代理
```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### HTTPS 反向代理
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    
    location / {
        proxy_pass http://backend:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### WebSocket 代理
```nginx
location /ws {
    proxy_pass http://websocket_backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400;
}
```

### 缓存配置
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

server {
    location / {
        proxy_pass http://backend;
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

## Nginx 正向代理

### HTTP 正向代理
```nginx
server {
    listen 8080;
    resolver 8.8.8.8;
    
    location / {
        proxy_pass http://$http_host$request_uri;
        proxy_set_header Host $http_host;
        proxy_buffers 256 4k;
        proxy_max_temp_file_size 0;
        proxy_connect_timeout 30;
    }
}
```

### HTTPS 正向代理（ngx_http_proxy_connect_module）
```nginx
server {
    listen 8080;
    resolver 8.8.8.8;
    
    proxy_connect;
    proxy_connect_allow 443 563;
    proxy_connect_connect_timeout 10s;
    proxy_connect_read_timeout 10s;
    proxy_connect_send_timeout 10s;
    
    location / {
        proxy_pass http://$host;
        proxy_set_header Host $host;
    }
}
```

## HAProxy 代理

### TCP 代理
```bash
frontend tcp_front
    bind *:3306
    mode tcp
    default_backend mysql_back

backend mysql_back
    mode tcp
    balance roundrobin
    server mysql1 192.168.1.10:3306 check
    server mysql2 192.168.1.11:3306 check
```

### HTTP 代理
```bash
frontend http_front
    bind *:80
    mode http
    default_backend web_back

backend web_back
    mode http
    balance roundrobin
    option httpchk GET /health
    server web1 192.168.1.10:8080 check
    server web2 192.168.1.11:8080 check
```

## SOCKS 代理

### SSH SOCKS 代理
```bash
# 创建 SOCKS5 代理
ssh -D 1080 -f -C -q -N user@remote_server

# 后台运行
ssh -D 1080 -fNq user@remote_server

# 指定绑定地址
ssh -D 0.0.0.0:1080 -fNq user@remote_server
```

### Dante SOCKS 服务器
```bash
# 安装
apt install dante-server

# /etc/danted.conf
logoutput: syslog
internal: eth0 port = 1080
external: eth0

socksmethod: username
user.privileged: root
user.unprivileged: nobody

client pass {
    from: 192.168.0.0/16 to: 0.0.0.0/0
    log: connect disconnect error
}

socks pass {
    from: 192.168.0.0/16 to: 0.0.0.0/0
    log: connect disconnect error
}
```

## 常见场景

### 场景 1：企业上网代理
```bash
# Squid 配置
http_port 3128
acl company_network src 10.0.0.0/8
acl blocked dstdomain "/etc/squid/blocked_sites.txt"
acl work_hours time MTWHF 09:00-18:00

http_access deny blocked
http_access allow company_network work_hours
http_access deny all

# 日志分析
cat /var/log/squid/access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -20
```

### 场景 2：API 网关
```nginx
upstream api_v1 {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

upstream api_v2 {
    server 192.168.1.20:8080;
    server 192.168.1.21:8080;
}

server {
    listen 80;
    
    location /api/v1 {
        proxy_pass http://api_v1;
        proxy_set_header X-API-Version "v1";
    }
    
    location /api/v2 {
        proxy_pass http://api_v2;
        proxy_set_header X-API-Version "v2";
    }
}
```

### 场景 3：跨域代理
```nginx
server {
    listen 80;
    
    location /api/ {
        proxy_pass http://api.external.com/;
        
        # CORS 头
        add_header Access-Control-Allow-Origin *;
        add_header Access-Control-Allow-Methods "GET, POST, OPTIONS";
        add_header Access-Control-Allow-Headers "Authorization, Content-Type";
        
        if ($request_method = OPTIONS) {
            return 204;
        }
    }
}
```

### 场景 4：代理链
```bash
# 使用 proxychains
# /etc/proxychains.conf
strict_chain
proxy_dns
[ProxyList]
socks5 127.0.0.1 1080
http 192.168.1.100 8080

# 使用
proxychains curl http://example.com
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 连接超时 | 检查后端服务、超时配置 |
| 502 错误 | 检查后端健康、代理配置 |
| 缓存不生效 | 检查缓存头、缓存配置 |
| 认证失败 | 检查认证配置、用户密码 |

```bash
# Squid 调试
squid -k parse
tail -f /var/log/squid/access.log
tail -f /var/log/squid/cache.log

# Nginx 调试
nginx -t
tail -f /var/log/nginx/error.log

# 测试代理
curl -x http://proxy:3128 http://example.com
curl -x socks5://127.0.0.1:1080 http://example.com

# 查看代理连接
ss -tnp | grep squid
netstat -tnp | grep nginx
```
