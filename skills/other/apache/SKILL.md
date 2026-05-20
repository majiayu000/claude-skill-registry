---
name: apache
description: Apache HTTP Server web server. Use for traditional web hosting.
---

# Apache HTTP Server (httpd)

Apache is a robust, modular web server. While Nginx leads in raw performance, Apache leads in **flexibility** via `.htaccess`. v2.4 remains the stable standard in 2025.

## When to Use

- **Shared Hosting**: `.htaccess` allows per-directory config without restarting the server.
- **Dynamic Modules**: Loading modules without recompiling.
- **Legacy Apps**: Many PHP/Perl apps are pre-tuned for Apache.

## Core Concepts

### MPM (Multi-Processing Modules)

- `prefork`: Compatible with non-thread-safe libraries (old PHP).
- `event`: Modern, async I/O. Best for high concurrency.

### VirtualHosts

Serving multiple domains from one IP.

### .htaccess

Files in the web root that override config. Convenient but slows performance.

## Best Practices (2025)

**Do**:

- **Use `event` MPM**: It rivals Nginx in connection handling.
- **Disable `.htaccess`**: If you have root access, put config in `httpd.conf` `Directory` blocks for performance.
- **Use HTTP/2**: Enable `mod_http2`.

**Don't**:

- **Don't enable unnecessary modules**: Reduce attack surface.

## References

- [Apache HTTP Server Documentation](https://httpd.apache.org/docs/2.4/)
