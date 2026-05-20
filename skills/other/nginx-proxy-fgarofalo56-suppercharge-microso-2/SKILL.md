---
name: nginx-proxy
description: Configure Nginx and Nginx Proxy Manager for reverse proxying, load balancing, SSL/TLS termination, caching, and web serving. Use when setting up web servers, reverse proxies, SSL certificates, or load balancers. Includes Nginx Proxy Manager GUI, Traefik alternative patterns, and security hardening. (project)
---

# Nginx Proxy Manager

Expert guidance for Nginx web server and reverse proxy configuration.

## When to Use This Skill

- Setting up reverse proxy for web services
- Configuring SSL/TLS certificates (Let's Encrypt)
- Load balancing across multiple backends
- Web server configuration
- Caching and performance optimization
- Security hardening
- Nginx Proxy Manager (NPM) GUI setup

## Nginx Installation

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install nginx

# CentOS/RHEL
sudo yum install nginx

# Docker
docker run -d -p 80:80 -p 443:443 \
  -v /etc/nginx:/etc/nginx:ro \
  -v /var/log/nginx:/var/log/nginx \
  nginx:alpine
```

## Basic Configuration

### Main Config Structure

```nginx
# /etc/nginx/nginx.conf
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
    worker_connections 1024;
    multi_accept on;
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # MIME types
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript;

    # Include virtual hosts
    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### Simple Web Server

```nginx
# /etc/nginx/sites-available/mysite.conf
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    root /var/www/mysite;
    index index.html index.htm;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

## Reverse Proxy Configuration

### Basic Reverse Proxy

```nginx
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### WebSocket Support

```nginx
server {
    listen 80;
    server_name ws.example.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_read_timeout 86400;
    }
}
```

### Multiple Backends (Path-Based)

```nginx
server {
    listen 80;
    server_name api.example.com;

    location /api/v1 {
        proxy_pass http://localhost:3001;
        proxy_set_header Host $host;
    }

    location /api/v2 {
        proxy_pass http://localhost:3002;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
}
```

## SSL/TLS Configuration

### Let's Encrypt with Certbot

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d example.com -d www.example.com

# Auto-renewal (usually set up automatically)
sudo certbot renew --dry-run
```

### SSL Configuration

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

## Load Balancing

```nginx
upstream backend {
    # Round-robin (default)
    server 192.168.1.10:3000;
    server 192.168.1.11:3000;
    server 192.168.1.12:3000;

    # Weighted
    server 192.168.1.10:3000 weight=3;
    server 192.168.1.11:3000 weight=2;
    server 192.168.1.12:3000 weight=1;

    # Least connections
    least_conn;

    # IP hash (session persistence)
    ip_hash;

    # Health checks
    server 192.168.1.10:3000 max_fails=3 fail_timeout=30s;

    # Backup server
    server 192.168.1.99:3000 backup;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
    }
}
```

## Caching

```nginx
# Define cache zone
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m
                 max_size=1g inactive=60m use_temp_path=off;

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_revalidate on;
        proxy_cache_lock on;

        # Cache key
        proxy_cache_key $scheme$proxy_host$uri$is_args$args;

        # Add cache status header
        add_header X-Cache-Status $upstream_cache_status;

        proxy_pass http://localhost:3000;
    }

    # Skip cache for certain paths
    location /api {
        proxy_cache off;
        proxy_pass http://localhost:3000;
    }
}
```

## Nginx Proxy Manager (Docker)

```yaml
# docker-compose.yml
services:
  npm:
    image: 'jc21/nginx-proxy-manager:latest'
    restart: unless-stopped
    ports:
      - '80:80'
      - '443:443'
      - '81:81'  # Admin UI
    volumes:
      - ./data:/data
      - ./letsencrypt:/etc/letsencrypt
    environment:
      DISABLE_IPV6: 'true'
```

```bash
# Start NPM
docker-compose up -d

# Access admin UI: http://localhost:81
# Default login: admin@example.com / changeme
```

### NPM Features

- GUI-based proxy host management
- Automatic Let's Encrypt certificates
- Access lists and authentication
- Custom Nginx configurations
- Redirection rules
- 404 hosts
- Streams (TCP/UDP proxying)

## Security Hardening

```nginx
# Security headers
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self';" always;

# Hide Nginx version
server_tokens off;

# Limit request size
client_max_body_size 10m;

# Rate limiting
limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

server {
    location /api {
        limit_req zone=one burst=20 nodelay;
        proxy_pass http://localhost:3000;
    }
}

# Block bad bots
map $http_user_agent $bad_bot {
    default 0;
    ~*malicious 1;
    ~*scanner 1;
}

server {
    if ($bad_bot) {
        return 403;
    }
}

# IP whitelist/blacklist
allow 192.168.1.0/24;
deny all;
```

## Common Configurations

### PHP-FPM

```nginx
server {
    listen 80;
    server_name php.example.com;
    root /var/www/html;
    index index.php index.html;

    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

### Static File Serving with Cache

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}
```

### Basic Authentication

```bash
# Create password file
sudo apt install apache2-utils
htpasswd -c /etc/nginx/.htpasswd user1
```

```nginx
location /admin {
    auth_basic "Restricted Area";
    auth_basic_user_file /etc/nginx/.htpasswd;
    proxy_pass http://localhost:3000;
}
```

## Troubleshooting

```bash
# Test configuration
sudo nginx -t

# Reload configuration
sudo nginx -s reload
sudo systemctl reload nginx

# View logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log

# Debug upstream
curl -I -H "Host: example.com" http://localhost

# Check listening ports
ss -tlnp | grep nginx

# Real-time monitoring
ngxtop
```

## Performance Tuning

```nginx
# Worker processes (set to CPU cores)
worker_processes auto;

# Worker connections
events {
    worker_connections 4096;
    use epoll;  # Linux
    multi_accept on;
}

# Buffer sizes
proxy_buffer_size 128k;
proxy_buffers 4 256k;
proxy_busy_buffers_size 256k;

# Timeouts
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;

# Keepalive to upstream
upstream backend {
    server localhost:3000;
    keepalive 32;
}
```
