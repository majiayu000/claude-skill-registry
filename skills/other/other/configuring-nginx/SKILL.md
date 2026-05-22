---
name: configuring-nginx
description: Configure nginx for static sites, reverse proxying, load balancing, SSL/TLS termination, caching, and performance tuning. When setting up web servers, application proxies, or load balancers, this skill provides production-ready patterns with modern security best practices for TLS 1.3, rate limiting, and security headers.
---

# Configuring nginx

## Purpose

Guide engineers through configuring nginx for common web infrastructure needs: static file serving, reverse proxying backend applications, load balancing across multiple servers, SSL/TLS termination, caching, and performance optimization. Provides production-ready configurations with security best practices.

## When to Use This Skill

Use when working with:
- Setting up web server for static sites or single-page applications
- Configuring reverse proxy for Node.js, Python, Ruby, or Go applications
- Implementing load balancing across multiple backend servers
- Terminating SSL/TLS for HTTPS traffic
- Adding caching layer for performance improvement
- Building API gateway functionality
- Protecting against DDoS with rate limiting
- Proxying WebSocket connections

Trigger phrases: "configure nginx", "nginx reverse proxy", "nginx load balancer", "enable SSL in nginx", "nginx performance tuning", "nginx caching", "nginx rate limiting"

## Installation

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

**RHEL/CentOS/Rocky:**
```bash
sudo dnf install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

**Docker:**
```bash
docker run -d -p 80:80 -v /path/to/config:/etc/nginx/conf.d nginx:alpine
```

## Quick Start Examples

### Static Website

Serve HTML/CSS/JS files from a directory:

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

See `references/static-sites.md` for SPA configurations and advanced patterns.

### Reverse Proxy

Proxy requests to a backend application server:

```nginx
upstream app_backend {
    server 127.0.0.1:3000;
    keepalive 32;
}

server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

See `references/reverse-proxy.md` for WebSocket proxying and API gateway patterns.

### SSL/TLS Configuration

Enable HTTPS with modern TLS configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:50m;
    ssl_session_timeout 1d;

    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    location / {
        try_files $uri $uri/ =404;
    }
}

server {
    listen 80;
    server_name example.com;
    return 301 https://$server_name$request_uri;
}
```

See `references/ssl-tls-config.md` for complete TLS configuration and certificate setup.

## Core Concepts

### Configuration Structure

nginx uses hierarchical configuration contexts:

```
nginx.conf (global settings)
├── events { } (connection processing)
└── http { } (HTTP-level settings)
    └── server { } (virtual host)
        └── location { } (URL routing)
```

**File locations:**
- `/etc/nginx/nginx.conf` - Main configuration
- `/etc/nginx/sites-available/` - Available site configs
- `/etc/nginx/sites-enabled/` - Enabled sites (symlinks)
- `/etc/nginx/conf.d/*.conf` - Additional configs
- `/etc/nginx/snippets/` - Reusable config snippets

See `references/configuration-structure.md` for detailed anatomy.

### Location Matching Priority

nginx evaluates location blocks in this order:

1. `location = /exact` - Exact match (highest priority)
2. `location ^~ /prefix` - Prefix match, stop searching
3. `location ~ \.php$` - Regex, case-sensitive
4. `location ~* \.(jpg|png)$` - Regex, case-insensitive
5. `location /` - Prefix match (lowest priority)

Example:
```nginx
location = /api/status {
    return 200 "OK\n";
}

location ^~ /static/ {
    root /var/www;
}

location ~ \.php$ {
    fastcgi_pass unix:/var/run/php/php-fpm.sock;
}

location / {
    proxy_pass http://backend;
}
```

### Essential Proxy Headers

When proxying to backends, preserve client information:

```nginx
proxy_set_header Host $host;
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
```

Create reusable snippet at `/etc/nginx/snippets/proxy-params.conf` and include with:
```nginx
include snippets/proxy-params.conf;
```

## Common Patterns

### Load Balancing

Distribute traffic across multiple backend servers:

**Round Robin (default):**
```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8080;
    server backend3.example.com:8080;
    keepalive 32;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        include snippets/proxy-params.conf;
    }
}
```

**Least Connections:**
```nginx
upstream backend {
    least_conn;
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

**IP Hash (sticky sessions):**
```nginx
upstream backend {
    ip_hash;
    server backend1.example.com:8080;
    server backend2.example.com:8080;
}
```

**Health Checks:**
```nginx
upstream backend {
    server backend1.example.com:8080 max_fails=3 fail_timeout=30s;
    server backend2.example.com:8080 max_fails=3 fail_timeout=30s;
    server backup.example.com:8080 backup;
}
```

See `references/load-balancing.md` for weighted load balancing and advanced patterns.

### WebSocket Proxying

Enable WebSocket connections by upgrading HTTP protocol:

```nginx
upstream websocket_backend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name ws.example.com;

    location / {
        proxy_pass http://websocket_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;

        # Long timeouts for persistent connections
        proxy_connect_timeout 7d;
        proxy_send_timeout 7d;
        proxy_read_timeout 7d;
    }
}
```

### Rate Limiting

Protect against abuse and DDoS attacks:

```nginx
# In http context
http {
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=5r/s;
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;
}

# In server context
server {
    listen 80;

    limit_req zone=api_limit burst=10 nodelay;
    limit_conn conn_limit 10;

    location /api/ {
        proxy_pass http://backend;
    }
}
```

See `references/security-hardening.md` for complete security configuration.

### Performance Optimization

**Worker Configuration:**
```nginx
# In main context
user www-data;
worker_processes auto;  # 1 per CPU core
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
    multi_accept on;
}
```

**Gzip Compression:**
```nginx
# In http context
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

**Proxy Caching:**
```nginx
# Define cache zone
proxy_cache_path /var/cache/nginx/proxy
                 levels=1:2
                 keys_zone=app_cache:100m
                 max_size=1g
                 inactive=60m;

# Use in location
location / {
    proxy_cache app_cache;
    proxy_cache_valid 200 60m;
    proxy_cache_use_stale error timeout updating;
    add_header X-Cache-Status $upstream_cache_status;
    proxy_pass http://backend;
}
```

See `references/performance-tuning.md` for detailed optimization strategies.

### Security Headers

Add essential security headers to protect against common vulnerabilities:

```nginx
# Create /etc/nginx/snippets/security-headers.conf
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

Include in server blocks:
```nginx
server {
    include snippets/security-headers.conf;
    # ... rest of config
}
```

### Access Control

Restrict access by IP address:

```nginx
server {
    listen 80;
    server_name admin.example.com;

    # Allow specific IPs
    allow 10.0.0.0/8;
    allow 203.0.113.0/24;

    # Deny all others
    deny all;

    location / {
        proxy_pass http://admin_backend;
    }
}
```

## Decision Framework

**Choose nginx for:** Performance-critical workloads (10K+ connections), reverse proxy, load balancing, static file serving, modern application stacks.

**Choose alternatives for:** Apache (`.htaccess`, mod_php, legacy apps), Caddy (auto-HTTPS, simpler config), Traefik (dynamic containers), Envoy (service mesh).

## Safety Checklist

Before deploying nginx configurations:

- [ ] Test configuration syntax: `sudo nginx -t`
- [ ] Use reload, not restart: `sudo systemctl reload nginx` (zero downtime)
- [ ] Check error logs: `sudo tail -f /var/log/nginx/error.log`
- [ ] Verify SSL/TLS: `openssl s_client -connect domain:443 -servername domain`
- [ ] Test externally: `curl -I https://domain.com`
- [ ] Monitor worker processes: `ps aux | grep nginx`
- [ ] Check open connections: `netstat -an | grep :80 | wc -l`
- [ ] Verify backend health: `curl -I http://localhost:8080`

## Troubleshooting

**Quick fixes:** Test config (`sudo nginx -t`), check logs (`/var/log/nginx/error.log`), verify backend (`curl http://127.0.0.1:3000`).

**Common errors:** 502 (backend down), 504 (timeout - increase `proxy_read_timeout`), 413 (upload size - set `client_max_body_size`).

See `references/troubleshooting.md` for complete debugging guide.

## Integration Points

**Related Skills:**

- **implementing-tls** - Certificate generation and automation (Let's Encrypt, cert-manager)
- **load-balancing-patterns** - Advanced load balancing architecture and decision frameworks
- **deploying-applications** - Application deployment strategies with nginx integration
- **security-hardening** - Complete server security beyond nginx-specific configuration
- **configuring-firewalls** - Firewall rules for HTTP/HTTPS access
- **dns-management** - DNS configuration for nginx virtual hosts
- **kubernetes-operations** - nginx Ingress Controller for Kubernetes

## Additional Resources

**Progressive Disclosure:**
- `references/installation-guide.md` - Detailed installation for all platforms
- `references/configuration-structure.md` - Complete nginx.conf anatomy
- `references/static-sites.md` - Static hosting patterns (basic, SPA, PHP)
- `references/reverse-proxy.md` - Advanced proxy scenarios and API gateway patterns
- `references/load-balancing.md` - All algorithms, health checks, sticky sessions
- `references/ssl-tls-config.md` - Complete TLS configuration and certificate setup
- `references/performance-tuning.md` - Workers, caching, compression, buffers
- `references/security-hardening.md` - Rate limiting, headers, access control
- `references/troubleshooting.md` - Common errors and debugging techniques

**Working Examples:**
- `examples/static-site/` - Static website and SPA configurations
- `examples/reverse-proxy/` - Node.js, WebSocket, API gateway examples
- `examples/load-balancing/` - All load balancing algorithms
- `examples/ssl-tls/` - Modern TLS and mTLS configurations
- `examples/performance/` - High-traffic optimization and caching
- `examples/security/` - Rate limiting and security hardening

**Reusable Snippets:**
- `snippets/ssl-modern.conf` - Modern TLS configuration
- `snippets/proxy-params.conf` - Standard proxy headers
- `snippets/security-headers.conf` - OWASP security headers
- `snippets/cache-static.conf` - Static asset caching
