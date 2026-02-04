---
name: ssl-tls
description: SSL/TLS 证书
version: 1.0.0
author: terminal-skills
tags: [security, ssl, tls, certificate, openssl, letsencrypt]
---

# SSL/TLS 证书

## 概述
证书申请、配置、自动续期技能。

## OpenSSL 基础

### 生成私钥
```bash
# RSA 私钥
openssl genrsa -out private.key 2048
openssl genrsa -out private.key 4096

# 带密码保护
openssl genrsa -aes256 -out private.key 2048

# ECDSA 私钥
openssl ecparam -genkey -name prime256v1 -out private.key
```

### 生成 CSR
```bash
# 交互式
openssl req -new -key private.key -out request.csr

# 非交互式
openssl req -new -key private.key -out request.csr \
    -subj "/C=CN/ST=Beijing/L=Beijing/O=Company/CN=example.com"

# 带 SAN
openssl req -new -key private.key -out request.csr \
    -config <(cat <<EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req

[req_distinguished_name]
CN = example.com

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = example.com
DNS.2 = www.example.com
DNS.3 = api.example.com
EOF
)
```

### 自签名证书
```bash
# 一步生成
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout private.key -out certificate.crt \
    -subj "/CN=example.com"

# 从已有私钥
openssl req -x509 -key private.key -days 365 -out certificate.crt
```

### 查看证书
```bash
# 查看证书信息
openssl x509 -in certificate.crt -text -noout

# 查看 CSR
openssl req -in request.csr -text -noout

# 查看私钥
openssl rsa -in private.key -text -noout

# 验证证书链
openssl verify -CAfile ca.crt certificate.crt

# 检查远程证书
openssl s_client -connect example.com:443 -servername example.com
```

### 格式转换
```bash
# PEM 转 DER
openssl x509 -in cert.pem -outform DER -out cert.der

# DER 转 PEM
openssl x509 -in cert.der -inform DER -out cert.pem

# PEM 转 PKCS12
openssl pkcs12 -export -out cert.p12 -inkey private.key -in cert.pem

# PKCS12 转 PEM
openssl pkcs12 -in cert.p12 -out cert.pem -nodes
```

## Let's Encrypt

### Certbot 安装
```bash
# Debian/Ubuntu
apt install certbot python3-certbot-nginx

# CentOS/RHEL
yum install certbot python3-certbot-nginx
```

### 申请证书
```bash
# Nginx 插件
certbot --nginx -d example.com -d www.example.com

# Apache 插件
certbot --apache -d example.com

# Standalone
certbot certonly --standalone -d example.com

# Webroot
certbot certonly --webroot -w /var/www/html -d example.com

# DNS 验证（通配符）
certbot certonly --manual --preferred-challenges dns -d "*.example.com"
```

### 管理证书
```bash
# 查看证书
certbot certificates

# 续期测试
certbot renew --dry-run

# 手动续期
certbot renew

# 删除证书
certbot delete --cert-name example.com
```

### 自动续期
```bash
# Cron
0 0 * * * certbot renew --quiet

# Systemd timer
systemctl enable certbot.timer
systemctl start certbot.timer
```

## Nginx 配置

### 基础 HTTPS
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;
    
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
}
```

### HTTP 重定向
```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

### 安全加固
```nginx
ssl_session_timeout 1d;
ssl_session_cache shared:SSL:50m;
ssl_session_tickets off;

ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;

add_header Strict-Transport-Security "max-age=63072000" always;
```

## 常见场景

### 场景 1：创建 CA
```bash
# 生成 CA 私钥
openssl genrsa -out ca.key 4096

# 生成 CA 证书
openssl req -x509 -new -nodes -key ca.key -sha256 -days 3650 \
    -out ca.crt -subj "/CN=My CA"

# 签发证书
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key \
    -CAcreateserial -out server.crt -days 365 -sha256
```

### 场景 2：检查证书过期
```bash
#!/bin/bash
DOMAIN=$1
DAYS=30

EXPIRY=$(echo | openssl s_client -connect ${DOMAIN}:443 -servername ${DOMAIN} 2>/dev/null | \
    openssl x509 -noout -enddate | cut -d= -f2)

EXPIRY_EPOCH=$(date -d "$EXPIRY" +%s)
NOW_EPOCH=$(date +%s)
DIFF=$(( (EXPIRY_EPOCH - NOW_EPOCH) / 86400 ))

if [ $DIFF -lt $DAYS ]; then
    echo "WARNING: ${DOMAIN} 证书将在 ${DIFF} 天后过期"
fi
```

### 场景 3：批量续期
```bash
#!/bin/bash
certbot renew --deploy-hook "systemctl reload nginx"
```

## 故障排查

| 问题 | 排查方法 |
|------|----------|
| 证书不信任 | 检查证书链、CA |
| 域名不匹配 | 检查 CN、SAN |
| 证书过期 | 检查有效期、续期 |
| 握手失败 | 检查协议、密码套件 |

```bash
# 测试 SSL
openssl s_client -connect example.com:443

# 检查证书链
openssl s_client -connect example.com:443 -showcerts

# SSL Labs 测试
curl https://api.ssllabs.com/api/v3/analyze?host=example.com
```
