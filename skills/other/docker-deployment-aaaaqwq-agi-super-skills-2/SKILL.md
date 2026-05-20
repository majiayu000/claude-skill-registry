---
name: docker-deployment
description: Docker container deployment with Nginx HTTPS configuration and Cloudflare Tunnel integration. Use when deploying web applications with Docker, configuring SSL/TLS certificates, setting up Nginx reverse proxy, or integrating with Cloudflare Tunnel for secure external access.
license: MIT
---

# Docker Deployment with Nginx HTTPS

## Quick Start

For Docker web application deployment with HTTPS support:

1. **Configure Nginx** with SSL certificates (see [nginx-https.md](references/nginx-https.md))
2. **Set up docker-compose.yml** with certificate volume mounting
3. **Configure Cloudflare Tunnel** to connect external domain to local container

## Common Tasks

| Task | Reference |
|------|-----------|
| Nginx HTTPS configuration | [nginx-https.md](references/nginx-https.md) |
| Cloudflare Origin Certificate | [cf-origin-cert.md](references/cf-origin-cert.md) |
| Docker data persistence | [data-persistence.md](references/data-persistence.md) |
| Cloudflare Tunnel setup | [cf-tunnel.md](references/cf-tunnel.md) |

## Architecture Overview

```
Internet → Cloudflare Edge (HTTPS) → Cloudflare Tunnel → Ubuntu/Docker (Nginx)
```

## Key Principles

- **Always use named Docker volumes** for persistent data
- **Nginx should redirect HTTP (80) to HTTPS (443)** in production
- **Cloudflare Origin Certificates** are for CF-to-origin encryption only
- **Tunnel connects to HTTP or HTTPS** - configure based on nginx setup

## Troubleshooting

**HTTPS not working after enabling Cloudflare force HTTPS?**
- Check if nginx listens on port 443
- Verify SSL certificates are mounted correctly
- Ensure Cloudflare Tunnel service URL matches (http:// or https://)

**Data lost after container restart?**
- Check docker-compose.yml uses named volumes, not bind mounts for critical data
- Verify database path points to mounted volume directory

See individual reference files for detailed solutions.
