---
name: caddy-reverse-proxy
description: Caddy reverse proxy configuration, Caddyfile syntax, automatic HTTPS, Docker integration, and common homelab patterns
---

# Caddy Reverse Proxy

Caddy is a modern web server with automatic HTTPS. This skill covers Caddyfile configuration, reverse proxy patterns, and Docker deployment for homelabs.

## Caddyfile basics

```
# Reverse proxy to a backend service
app.example.com {
    reverse_proxy localhost:8080
}

# Multiple domains, same backend
app1.example.com, app2.example.com {
    reverse_proxy backend:3000
}

# Wildcard with on-demand TLS
*.example.com {
    tls {
        on_demand
    }
    reverse_proxy localhost:8080
}
```

## Reverse proxy patterns

### Basic proxy

```
service.example.com {
    reverse_proxy service:8080
}
```

### With path stripping

```
example.com {
    handle /api/* {
        reverse_proxy api-server:3000
    }
    handle {
        reverse_proxy frontend:80
    }
}
```

### WebSocket support (automatic)

Caddy handles WebSocket upgrades automatically. No extra config needed.

### Load balancing

```
app.example.com {
    reverse_proxy node1:8080 node2:8080 node3:8080 {
        lb_policy round_robin
        health_uri /health
        health_interval 10s
    }
}
```

### Headers

```
service.example.com {
    reverse_proxy backend:8080 {
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }
}
```

## TLS / HTTPS

### Automatic (Let's Encrypt)

Caddy gets certificates automatically. Just use a domain name:

```
app.example.com {
    reverse_proxy localhost:8080
}
```

### Cloudflare DNS challenge

For wildcard certs or when port 80/443 isn't publicly reachable. Requires the `caddy-cloudflare` build.

```
*.example.com {
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }
    @app1 host app1.example.com
    handle @app1 {
        reverse_proxy app1:8080
    }
}
```

### Internal / LAN-only (no public TLS)

```
:80 {
    reverse_proxy localhost:8080
}

# Or with self-signed cert
service.lan {
    tls internal
    reverse_proxy localhost:8080
}
```

### Restrict to LAN only

```
service.example.com {
    @denied not remote_ip 192.168.0.0/16 10.0.0.0/8 172.16.0.0/12
    respond @denied 403

    reverse_proxy backend:8080
}
```

## Common homelab patterns

### Catch-all / landing page

```
*.example.com {
    tls {
        dns cloudflare {env.CLOUDFLARE_API_TOKEN}
    }

    # Named matchers for each service
    @grafana host grafana.example.com
    handle @grafana {
        reverse_proxy grafana:3000
    }

    @n8n host n8n.example.com
    handle @n8n {
        reverse_proxy n8n:5678
    }

    # Fallback for unmatched subdomains
    handle {
        respond "Nothing here" 404
    }
}
```

### Basic auth

```
admin.example.com {
    basicauth {
        # Generate hash: caddy hash-password
        admin $2a$14$HASHED_PASSWORD_HERE
    }
    reverse_proxy backend:8080
}
```

### File server

```
files.example.com {
    file_server browse {
        root /srv/files
    }
}
```

### Redirect HTTP to HTTPS (automatic)

Caddy does this by default. To redirect a domain:

```
old.example.com {
    redir https://new.example.com{uri} permanent
}
```

## Docker deployment

### docker-compose.yml

```yaml
services:
  caddy:
    image: caddy:2-alpine
    # Or for Cloudflare DNS: caddybuilds/caddy-cloudflare
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    environment:
      - CLOUDFLARE_API_TOKEN=your-token  # if using DNS challenge
    restart: unless-stopped

volumes:
  caddy_data:
  caddy_config:
```

### Connecting to other Docker services

Services on the same Docker network are reachable by container name:

```
app.example.com {
    reverse_proxy container-name:8080
}
```

For services on different networks, use the host IP or join networks:

```yaml
services:
  caddy:
    networks:
      - frontend
      - backend
```

## Management commands

```bash
# Validate config
caddy validate --config /etc/caddy/Caddyfile

# Reload without downtime (inside container)
docker exec <caddy-container> caddy reload --config /etc/caddy/Caddyfile

# Adapt Caddyfile to JSON (debugging)
caddy adapt --config /etc/caddy/Caddyfile

# View loaded config
caddy config

# Hash a password for basicauth
caddy hash-password
```

## Environment variables

Use `{env.VAR_NAME}` in Caddyfile:

```
service.example.com {
    reverse_proxy {env.BACKEND_HOST}:{env.BACKEND_PORT}
}
```

## Logging

```
service.example.com {
    log {
        output file /var/log/caddy/access.log
        format json
        level INFO
    }
    reverse_proxy backend:8080
}
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Certificate not issuing | Check DNS points to Caddy, ports 80/443 open, or use DNS challenge |
| 502 Bad Gateway | Backend not running or wrong hostname/port. Check `docker network ls` |
| Config not reloading | Use `caddy reload`, not restart (avoids downtime). Check `caddy validate` first |
| Wildcard cert failing | Requires DNS challenge plugin (e.g. `caddy-cloudflare`), not default image |
| WebSocket disconnecting | Usually a proxy timeout. Add `transport http { keepalive 30s }` |
| LAN service reachable externally | Add `remote_ip` matcher to restrict access |

## Caddy vs nginx quick reference

| nginx | Caddy |
|-------|-------|
| `proxy_pass http://backend;` | `reverse_proxy backend:8080` |
| `ssl_certificate /path/cert.pem;` | Automatic (just use domain name) |
| `location /api { ... }` | `handle /api/* { ... }` |
| `nginx -t && nginx -s reload` | `caddy validate && caddy reload` |
| Separate config for HTTPS redirect | Automatic |
