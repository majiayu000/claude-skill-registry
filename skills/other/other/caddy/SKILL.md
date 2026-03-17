---
name: caddy
description: Caddy automatic HTTPS web server. Use for simple web serving.
---

# Caddy

Caddy 2 is a powerful, enterprise-ready web server with **automatic HTTPS** by default. v2.8 (2025) improves **HTTP/3** performance and certificate management.

## When to Use

- **HTTPS Default**: You want zero-config SSL. Caddy obtains and renews certificates automatically.
- **Simplicity**: `Caddyfile` is the most human-readable config format.
- **Go Apps**: Can act as a process manager or library for Go applications.

## Quick Start

```caddyfile
# Caddyfile
example.com {
    reverse_proxy localhost:3000
    encode zstd gzip
    file_server
}
```

## Core Concepts

### Caddyfile

Simple configuration format.
`directive argument { block }`

### JSON Config

The native config format. Caddyfile is adapted to JSON. API allows real-time config updates via REST.

### Modules

Caddy is extensible. Plugins (like `caddy-dns-cloudflare`) are compiled in via `xcaddy`.

## Best Practices (2025)

**Do**:

- **Use Caddyfile**: For 99% of cases, it's enough.
- **Persist /data**: Caddy stores certificates in the `/data` directory. Mount this volume in Docker.
- **Use `caddy fmt`**: Auto-format your config.

**Don't**:

- **Don't sit behind another proxy**: If you hide Caddy behind Cloudflare/Nginx, you break its ACME challenges unless you configure it specifically.

## References

- [Caddy Documentation](https://caddyserver.com/docs/)
