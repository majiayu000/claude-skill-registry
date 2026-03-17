---
name: nginx
description: Nginx configuration and optimization
version: 1.0.0
author: terminal-skills
tags: [server, nginx, web, proxy, load-balancer]
---

# Nginx Configuration and Optimization

## Overview
Nginx web server configuration, reverse proxy, load balancing, performance optimization and other skills.

## Basic Management

### Service Control
```bash
# Start/Stop services
systemctl start nginx
systemctl stop nginx
systemctl restart nginx
systemctl reload nginx              # Graceful reload config

# Configuration test
nginx -t
nginx -T                            # Test and print config
```

### Configuration Files
```bash
# Main configuration file
/etc/nginx/nginx.conf

# Site configuration
/etc/nginx/conf.d/*.conf
/etc/nginx/sites-available/
/etc/nginx/sites-enabled/

# Log files
/var/log/nginx/access.log
/var/log/nginx/error.log
```

## Basic Configuration

### Static Website
```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/html;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }

    # Static resource caching
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### HTTPS Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # SSL optimization
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    # HSTS
    add_header Strict-Transport-Security "max-age=31536000" always;
}

# HTTP redirect to HTTPS
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## Reverse Proxy

### Basic Proxy
```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### WebSocket Proxy
```nginx
location /ws {
    proxy_pass http://127.0.0.1:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400;
}
```

## Load Balancing

### Basic Configuration
```nginx
upstream backend {
    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080 backup;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout http_500;
    }
}
```

### Load Balancing Strategies
```nginx
# Round Robin (default)
upstream backend {
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

# IP Hash (session persistence)
upstream backend {
    ip_hash;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

# Least Connections
upstream backend {
    least_conn;
    server 192.168.1.10:8080;
    server 192.168.1.11:8080;
}

# Health Check
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
}
```

## Performance Optimization

### Basic Optimization
```nginx
# nginx.conf
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 65535;
    use epoll;
    multi_accept on;
}

http {
    # File transfer optimization
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;

    # Timeout settings
    keepalive_timeout 65;
    client_body_timeout 12;
    client_header_timeout 12;
    send_timeout 10;

    # Buffer settings
    client_body_buffer_size 10K;
    client_header_buffer_size 1k;
    client_max_body_size 8m;
    large_client_header_buffers 4 32k;
}
```

### Gzip Compression
```nginx
gzip on;
gzip_vary on;
gzip_proxied any;
gzip_comp_level 6;
gzip_min_length 1000;
gzip_types text/plain text/css text/xml application/json application/javascript application/xml;
```

## Common Scenarios

### Scenario 1: PHP-FPM Configuration
```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/html;
    index index.php index.html;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### Scenario 2: Rate Limiting
```nginx
# Define rate limit zone
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

server {
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend;
    }
}
```

### Scenario 3: Access Control
```nginx
location /admin {
    allow 192.168.1.0/24;
    deny all;
    
    auth_basic "Admin Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
}
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Configuration error | `nginx -t` to test config |
| 502 Bad Gateway | Check backend service, upstream config |
| 504 Gateway Timeout | Increase proxy_read_timeout |
| Permission issues | Check file permissions, SELinux |
| Performance issues | Check worker_connections, log analysis |
