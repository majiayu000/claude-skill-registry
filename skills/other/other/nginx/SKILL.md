---
name: nginx
description: Nginx web server, reverse proxy, and load balancer. Use for web serving.
---

# Nginx

Nginx is the world's most popular web server. v1.25+ (2025) supports **HTTP/3 (QUIC)** natively.

## When to Use

- **Reverse Proxy**: Termination of SSL, load balancing to backend apps (Node/Python).
- **Static Content**: Serving React/Vue bundles efficiently.
- **Ingress**: Nginx Ingress Controller is the standard K8s ingress.

## Quick Start

```nginx
# nginx.conf
server {
    listen 443 quic reuseport;
    listen 443 ssl;
    http2 on;

    server_name example.com;
    ssl_certificate cert.pem;
    ssl_certificate_key key.pem;

    location / {
        proxy_pass http://localhost:3000;
        add_header Alt-Svc 'h3=":443"; ma=86400';
    }
}
```

## Core Concepts

### Worker Processes

Event-driven architecture. Handles 10k+ connections with low RAM.

### Contexts

`http`, `server`, `location`. Configuration inheritance rules.

### Modules

Extend functionality (e.g., `ngx_http_stub_status_module` for metrics).

## Best Practices (2025)

**Do**:

- **Enable HTTP/3**: Enable QUIC for lower latency over unreliable networks.
- **Tune Buffers**: Optimizing `client_body_buffer_size` prevents disk I/O.
- **Security Headers**: Always set HSTS, X-Frame-Options, etc.

**Don't**:

- **Don't using `if` is evil**: Avoid complex logic in Nginx config. Use `try_files` or `map`.

## References

- [Nginx Documentation](https://nginx.org/en/docs/)
