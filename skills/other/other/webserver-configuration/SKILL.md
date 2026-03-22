---
name: webserver-configuration
description: Complete web server configuration workflows for Nginx, Apache, Traefik, and Caddy. Use when setting up, configuring, or optimizing web servers, SSL/TLS, load balancers, or reverse proxies.
---

# Web Server Configuration Skill

This skill provides comprehensive configuration guides, best practices, and templates for web servers including Nginx, Apache, Traefik, and Caddy.

## When to Use This Skill

Use this skill when:
- Installing and configuring web servers
- Setting up SSL/TLS certificates
- Configuring reverse proxy
- Implementing load balancing
- Optimizing performance
- Adding security headers
- Setting up virtual hosts
- Configuring caching

## Web Server Selection Guide

```
┌─────────────────────────────────────────────────────────────┐
│ Choose Web Server Based On:                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Nginx:                                                      │
│   ✓ High performance & scalability                          │
│   ✓ Reverse proxy & load balancing                          │
│   ✓ Static file serving                                     │
│   ✓ Low memory footprint                                    │
│                                                             │
│ Apache:                                                     │
│   ✓ .htaccess support                                       │
│   ✓ Module ecosystem                                        │
│   ✓ Legacy application support                              │
│   ✓ Dynamic content                                         │
│                                                             │
│ Traefik:                                                    │
│   ✓ Kubernetes ingress                                      │
│   ✓ Docker integration                                      │
│   ✓ Automatic SSL (Let's Encrypt)                           │
│   ✓ Dynamic configuration                                   │
│                                                             │
│ Caddy:                                                      │
│   ✓ Automatic HTTPS                                         │
│   ✓ Simple configuration                                    │
│   ✓ HTTP/2 push                                             │
│   ✓ Modern defaults                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start Configurations

### Nginx Production Setup

```nginx
# Complete production-ready Nginx configuration
# See resources/nginx-configs.md for full implementation

server {
    listen 443 ssl http2;
    server_name example.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=63072000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
    # Reverse Proxy
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Apache Production Setup

```apache
# Complete production-ready Apache configuration
# See resources/apache-configs.md for full implementation

<VirtualHost *:443>
    ServerName example.com
    DocumentRoot /var/www/html
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=63072000"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    
    # Reverse Proxy
    ProxyPass / http://localhost:8080/
    ProxyPassReverse / http://localhost:8080/
</VirtualHost>
```

### Traefik Docker Setup

```yaml
# docker-compose.yml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=admin@example.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./letsencrypt:/letsencrypt

  webapp:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.webapp.rule=Host(`example.com`)"
      - "traefik.http.routers.webapp.tls=true"
      - "traefik.http.routers.webapp.tls.certresolver=letsencrypt"
```

### Caddy Simple Setup

```caddy
# Caddyfile
example.com {
    reverse_proxy localhost:8080
    
    # Security headers
    header {
        Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
        X-Frame-Options "SAMEORIGIN"
        X-Content-Type-Options "nosniff"
    }
    
    # Compression
    encode zstd gzip
    
    # Logging
    log {
        output file /var/log/caddy/access.log
        format json
    }
}
```

## SSL/TLS Configuration

### Let's Encrypt Setup

```bash
#!/bin/bash
# Automated SSL with Certbot

DOMAIN=$1
EMAIL=$2

# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Obtain certificate
certbot certonly --nginx \
    --agree-tos \
    --redirect \
    --hsts \
    --staple-ocsp \
    --email $EMAIL \
    -d $DOMAIN \
    -d www.$DOMAIN

# Auto-renewal
echo "0 3 * * * certbot renew --quiet --deploy-hook 'systemctl reload nginx'" | crontab -
```

## Security Headers

### Essential Headers

```
# Security Headers (all web servers)
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'
Permissions-Policy: geolocation=(), microphone=(), camera=()
Cache-Control: no-store, no-cache, must-revalidate
```

## Performance Optimization

### Compression

```nginx
# Nginx Gzip
gzip on;
gzip_vary on;
gzip_comp_level 6;
gzip_types text/plain text/css application/json application/javascript;

# Nginx Brotli (better)
brotli on;
brotli_comp_level 6;
brotli_types text/plain text/css application/json application/javascript;
```

### Caching

```nginx
# Static files
location /static/ {
    expires 30d;
    add_header Cache-Control "public, immutable";
}

# API responses
location /api/ {
    add_header Cache-Control "no-store, no-cache, must-revalidate";
}
```

## Load Balancing

### Nginx Load Balancer

```nginx
upstream backend {
    least_conn;
    server 10.0.1.10:8080;
    server 10.0.1.11:8080;
    server 10.0.1.12:8080 backup;
    
    keepalive 32;
}

server {
    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
    }
}
```

## Implementation Resources

Refer to the following resources in this skill for detailed implementations:

- **`resources/nginx-configs.md`**: Complete Nginx configurations for various use cases
- **`resources/apache-configs.md`**: Complete Apache configurations and virtual hosts
- **`resources/ssl-setup.md`**: SSL/TLS certificate setup and configuration
- **`resources/performance-tuning.md`**: Performance optimization techniques

## Anti-Patterns

**Avoid these web server mistakes:**

❌ **Default configurations in production**
❌ **Missing security headers**
❌ **No SSL/TLS**
❌ **Server version exposure**
❌ **Missing rate limiting**
❌ **No compression**
❌ **Improper caching**
❌ **No access logs**
❌ **Running as root**
❌ **No health checks**

## Monitoring

### Essential Metrics

```yaml
# Monitor these metrics:
- Response time (p95, p99)
- Requests per second
- Error rate (4xx, 5xx)
- Active connections
- SSL certificate expiry
- Upstream health
- Cache hit rate
- Bandwidth usage
```

## Troubleshooting

### Common Issues

**502 Bad Gateway:**
- Check upstream service status
- Verify network connectivity
- Check firewall rules

**504 Gateway Timeout:**
- Increase proxy timeouts
- Check upstream performance
- Monitor resource usage

**SSL Errors:**
- Verify certificate paths
- Check certificate expiry
- Verify domain configuration
