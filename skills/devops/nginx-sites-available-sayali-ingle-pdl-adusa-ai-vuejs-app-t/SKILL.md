---
name: nginx-sites-available
description: Generates nginx-sites-available-default in project root for Debian/Ubuntu-based nginx installations.
---

# Nginx Sites Available Default Skill

## Purpose
Generate nginx sites-available default configuration file in the project root directory.

## Output
Create the file: `nginx-sites-available-default` (in project root)

## Template
See: `examples.md` for the exact configuration template.

## Critical Configuration Elements
- **SPA routing**: `try_files $uri $uri/ /index.html;` (required for Vue Router)
- **IPv4/IPv6**: Dual-stack support on port 8080
- **Error pages**: Custom 50x.html error page handling
- **SSL template**: Commented configuration for HTTPS setup
- **PHP template**: Commented configuration for PHP applications
- **Virtual hosts**: Example for additional domains

## Docker Integration
This file is referenced in Dockerfile:
```dockerfile
RUN cp -a nginx-sites-available-default /etc/nginx/sites-available/default
```

## Notes
- Debian/Ubuntu standard location for nginx site configurations
- File serves static files from `/usr/share/nginx/html` (Vite build output location)
- Includes comprehensive comments and templates for common patterns
- All configuration values are production-ready defaults
- No customization needed based on user parameters
