---
name: nginx-default-conf
description: Generates nginx.default.conf in project root for nginx conf.d directory configuration. Serves static files from /usr/share/nginx/html.
---

# Nginx Default Conf Skill

## Purpose
Generate nginx.default.conf file in the project root directory for nginx conf.d directory configuration.

## Output
Create the file: `nginx.default.conf` (in project root)

## Template
See: `examples.md` for the exact configuration template.

## Critical Configuration Elements
- **SPA routing**: `try_files $uri $uri/ /index.html;` (required for Vue Router)
- **CORS**: `add_header Access-Control-Allow-Origin *;` (required for micro-frontends)
- **Caching**: `expires max;` and `Cache-Control "public"` headers
- **Error pages**: Custom 50x.html error page handling
- **Port**: Listen on 8080 (container standard)

## Docker Integration
This file is referenced in Dockerfile:
```dockerfile
RUN cp -a nginx.default.conf /etc/nginx/conf.d/default.conf
```

## Notes
- File serves static files from `/usr/share/nginx/html` (Vite build output location)
- All configuration values are production-ready defaults
- No customization needed based on user parameters
