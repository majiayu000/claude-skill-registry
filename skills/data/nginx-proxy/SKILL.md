---
name: nginx-proxy
description: Nginx reverse proxy configuration and optimization. Set up SSL termination, load balancing, caching, rate limiting, and security headers. Use when configuring Nginx as a reverse proxy, API gateway, or web server for production deployments.
---

# Nginx Reverse Proxy Skill

Configure Nginx as a high-performance reverse proxy with SSL, load balancing, and caching.

## Triggers

Use this skill when you see:
- nginx, nginx proxy, reverse proxy
- ssl termination, load balancer
- proxy pass, upstream, nginx config
- rate limiting, caching, web server

## Instructions

### Basic Reverse Proxy

```nginx
# /etc/nginx/sites-available/app.conf

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### HTTPS with SSL Termination

```nginx
server {
    listen 80;
    server_name app.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name app.example.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;
    ssl_session_timeout 1d;
    ssl_session_cache shared:SSL:50m;
    ssl_session_tickets off;

    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # HSTS
    add_header Strict-Transport-Security "max-age=63072000" always;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Load Balancing with Upstream

```nginx
upstream backend {
    # Load balancing methods: round-robin (default), least_conn, ip_hash
    least_conn;

    server 192.168.1.10:8080 weight=3;
    server 192.168.1.11:8080 weight=2;
    server 192.168.1.12:8080 backup;

    # Health checks (Nginx Plus or OpenResty)
    # health_check interval=10 fails=3 passes=2;

    keepalive 32;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Caching Configuration

```nginx
# Define cache zone in http block
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m use_temp_path=off;

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_cache my_cache;
        proxy_cache_valid 200 302 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        proxy_cache_lock on;

        add_header X-Cache-Status $upstream_cache_status;
    }

    # Bypass cache for specific paths
    location /api {
        proxy_pass http://localhost:3000;
        proxy_cache_bypass 1;
        proxy_no_cache 1;
    }
}
```

### Rate Limiting

```nginx
# Define rate limit zones in http block
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

server {
    listen 80;
    server_name app.example.com;

    # General rate limit
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_conn conn_limit 10;
        proxy_pass http://localhost:3000;
    }

    # Strict rate limit for login
    location /api/login {
        limit_req zone=login_limit burst=5 nodelay;
        proxy_pass http://localhost:3000;
    }
}
```

### Security Headers

```nginx
server {
    listen 443 ssl http2;
    server_name app.example.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Hide Nginx version
    server_tokens off;

    location / {
        proxy_pass http://localhost:3000;
    }
}
```

### WebSocket Support

```nginx
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

server {
    listen 80;
    server_name app.example.com;

    location /ws {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection $connection_upgrade;
        proxy_set_header Host $host;
        proxy_read_timeout 86400;
    }
}
```

### API Gateway Pattern

```nginx
server {
    listen 80;
    server_name api.example.com;

    # API versioning
    location /v1/ {
        proxy_pass http://api_v1_backend/;
    }

    location /v2/ {
        proxy_pass http://api_v2_backend/;
    }

    # Service routing
    location /users/ {
        proxy_pass http://users_service/;
    }

    location /orders/ {
        proxy_pass http://orders_service/;
    }

    location /payments/ {
        proxy_pass http://payments_service/;
    }
}
```

### Static Files with Caching

```nginx
server {
    listen 80;
    server_name app.example.com;

    root /var/www/app;

    # Static files with long cache
    location /static/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }

    # Assets with cache busting
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1M;
        add_header Cache-Control "public";
    }

    # Proxy dynamic requests
    location / {
        try_files $uri @backend;
    }

    location @backend {
        proxy_pass http://localhost:3000;
    }
}
```

### Docker Compose Example

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./conf.d:/etc/nginx/conf.d:ro
      - ./certs:/etc/nginx/certs:ro
      - ./html:/usr/share/nginx/html:ro
    depends_on:
      - app
    restart: unless-stopped

  app:
    build: .
    expose:
      - "3000"
    restart: unless-stopped
```

### Common Commands

```bash
# Test configuration
nginx -t

# Reload configuration
nginx -s reload

# View access logs
tail -f /var/log/nginx/access.log

# View error logs
tail -f /var/log/nginx/error.log

# Check running processes
ps aux | grep nginx
```

## Best Practices

1. **SSL**: Use TLS 1.2+ with strong ciphers, enable HSTS
2. **Security Headers**: Add security headers to all responses
3. **Rate Limiting**: Protect against abuse and DDoS
4. **Caching**: Cache static content and API responses where appropriate
5. **Logging**: Configure detailed access and error logs
6. **Keepalive**: Enable keepalive connections to upstream

## Common Workflows

### Set Up Reverse Proxy
1. Install Nginx: `apt install nginx`
2. Create site configuration in `/etc/nginx/sites-available/`
3. Enable site: `ln -s /etc/nginx/sites-available/app.conf /etc/nginx/sites-enabled/`
4. Test configuration: `nginx -t`
5. Reload: `nginx -s reload`

### Add SSL with Let's Encrypt
1. Install Certbot: `apt install certbot python3-certbot-nginx`
2. Obtain certificate: `certbot --nginx -d app.example.com`
3. Auto-renewal is configured automatically
4. Test renewal: `certbot renew --dry-run`
