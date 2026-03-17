---
name: ha-addon
description: "Develop Home Assistant add-ons with Docker, Supervisor API, and multi-arch builds. Use when creating add-ons, configuring Dockerfiles, setting up ingress, or publishing to repositories. Activates on keywords: add-on, addon, supervisor, hassio, ingress, bashio, docker."
---

# Home Assistant Add-On Development

> Expert guidance for building, configuring, and publishing Home Assistant add-ons with Docker, Supervisor integration, and multi-architecture support.

## Before You Start

**This skill prevents common Home Assistant add-on development errors:**

| Issue | Symptom | Solution |
|-------|---------|----------|
| Permission errors | `Permission denied` on supervisor API calls | Use correct SUPERVISOR_TOKEN and API endpoints |
| Configuration validation | Add-on won't load | Validate config.yaml schema before publishing |
| Docker base image errors | Missing dependencies in runtime | Use official Home Assistant base images (ghcr.io/home-assistant) |
| Ingress misconfiguration | Web UI not accessible through HA | Configure nginx reverse proxy correctly |
| Multi-arch build failures | Add-on only works on one architecture | Set up build.yaml with architecture matrix |

## Quick Start: Create an Add-On from Scratch

### Step 1: Create the Add-On Directory Structure

```bash
mkdir -p my-addon/{rootfs,rootfs/etc/s6-overlay/s6-rc.d/service-name}
cd my-addon
```

**Why this matters:** Home Assistant expects specific directory layouts. The `rootfs/` contains your actual application files that get packaged into the Docker image.

### Step 2: Create config.yaml

```yaml
---
name: My Custom Add-On
description: My awesome Home Assistant add-on
version: 1.0.0
slug: my-addon
image: ghcr.io/home-assistant/{arch}-addon-my-addon
arch:
  - amd64
  - armv7
  - aarch64
ports:
  8080/tcp: null
options:
  debug: false
schema:
  debug: bool
permissions:
  - homeassistant  # Read/write Home Assistant core data
```

**Why this matters:** This is your add-on's manifest. The slug becomes the internal identifier and determines where configuration is stored.

### Step 3: Create the Dockerfile

```dockerfile
FROM ghcr.io/home-assistant/amd64-base:latest

# Install dependencies
RUN apk add --no-cache python3 py3-pip

# Copy application
COPY rootfs /

# Set working directory
WORKDIR /app

# Install Python packages if needed
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Run using S6 overlay
CMD ["/init"]
```

**Why this matters:** Using Home Assistant base images includes critical runtime components (S6 overlay, bashio helpers, supervisor integration).

### Step 4: Create S6 Service Script

Create `rootfs/etc/s6-overlay/s6-rc.d/service-name/run`:

```bash
#!/command/execlineb -P
foreground { echo "Starting my add-on..." }
/app/my-service
```

Make it executable:
```bash
chmod +x rootfs/etc/s6-overlay/s6-rc.d/service-name/run
```

**Why this matters:** S6 overlay is Home Assistant's init system. It manages service startup, logging, and graceful shutdown.

## Critical Rules

### ✅ Always Do

- ✅ Use official Home Assistant base images (ghcr.io/home-assistant/{arch}-base)
- ✅ Include all supported architectures in config.yaml (amd64, armv7, aarch64)
- ✅ Use bashio helper functions for common operations (bashio::log::info, bashio::addon::option)
- ✅ Validate config.yaml schema before releasing
- ✅ Document configuration options in the schema section
- ✅ Include addon_uuid in logs for debugging

### ❌ Never Do

- ❌ Don't hardcode paths - use bashio to get configuration directory (/data/)
- ❌ Don't run services as root unless absolutely necessary (set USER in Dockerfile)
- ❌ Don't call supervisor API without SUPERVISOR_TOKEN
- ❌ Don't ignore SIGTERM signals - implement graceful shutdown
- ❌ Don't assume one architecture - use {arch} placeholder in image names
- ❌ Don't store data outside /data/ - Home Assistant won't persist it

### Common Mistakes

**❌ Wrong: Hardcoded paths**
```bash
#!/bin/bash
CONFIG_PATH="/config/my-addon"
```

**✅ Correct: Using bashio for configuration**
```bash
#!/command/execlineb -P
CONFIG_PATH=${"$(bashio::addon::config_path)"}
```

**Why:** bashio handles path resolution and ensures your add-on works in any Home Assistant installation.

## Configuration Reference

### config.yaml Structure

```yaml
---
name: String                          # Display name
description: String                   # Short description
version: String                       # Semantic version (1.0.0)
slug: String                          # URL-safe identifier
image: String                         # Docker image URL with {arch} placeholder
arch:
  - amd64|armv7|aarch64|armhf|i386    # Supported architectures
ports:
  8080/tcp: null                      # TCP port (null=internal only, number=external)
  53/udp: 53                          # UDP with external port mapping
devices:
  - /dev/ttyACM0                      # Device access
services:
  - mysql                             # Depends on other service
options:
  debug: false                        # User configuration options
  log_level: info
schema:
  debug: bool                         # Configuration validation schema
  log_level:
    - debug
    - info
    - warning
    - error
permissions:
  - homeassistant                     # Read/write HA config
  - hassio                            # Full supervisor API access
  - admin                             # Broad system access
  - backup                            # Backup/restore operations
environment:
  NODE_ENV: production
webui: http://[HOST]:[PORT:8080]     # Web UI URL pattern
ingress: true                         # Enable ingress proxy
ingress_port: 8080                    # Internal port for ingress
ingress_entry: /                      # URL path for ingress entry
```

**Key settings:**
- `slug`: Used internally and in supervisor API calls
- `arch`: List all supported architectures or builds fail
- `image`: Must use {arch} placeholder for dynamic builds
- `options`: User-configurable settings
- `permissions`: Controls supervisor API access level
- `ingress`: Enables reverse proxy for web UIs

## Common Patterns

### Using bashio for Logging

```bash
#!/command/execlineb -P
foreground { bashio::log::info "Add-on started" }
foreground { bashio::log::warning "Low disk space" }
foreground { bashio::log::error "Failed to connect" }
```

### Accessing Configuration Options

```bash
#!/command/execlineb -P
define DEBUG "$(bashio::addon::option 'debug')"
define LOG_LEVEL "$(bashio::addon::option 'log_level')"
if { test "${DEBUG}" = "true" }
  bashio::log::debug "Debug mode enabled"
```

### Supervisor API Communication

```bash
#!/bin/bash
# Get addon info
curl -X GET \
  -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
  http://supervisor/addons/self/info | jq .

# Send notification
curl -X POST \
  -H "Authorization: Bearer $SUPERVISOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Warning message"}' \
  http://supervisor/notifications/create
```

### Multi-Arch Docker Build

Create `build.yaml`:

```yaml
build_from:
  amd64: ghcr.io/home-assistant/amd64-base:latest
  armv7: ghcr.io/home-assistant/armv7-base:latest
  aarch64: ghcr.io/home-assistant/aarch64-base:latest
  armhf: ghcr.io/home-assistant/armhf-base:latest
codenotary: your-notary-id  # Optional code signing
```

### Ingress Configuration for Web UIs

```yaml
ingress: true
ingress_port: 8080
ingress_entry: /
# Optional ingress_stream for streaming endpoints
```

Inside your app, use correct reverse proxy headers:
```bash
# nginx configuration in your app
location / {
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  proxy_set_header X-Forwarded-Proto $scheme;
  proxy_set_header Host $host;
  proxy_pass http://localhost:8080;
}
```

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| Add-on fails to start | Missing S6 service files | Create `/etc/s6-overlay/s6-rc.d/service-name/` with `run` executable |
| Supervisor API returns 401 | Invalid SUPERVISOR_TOKEN | Verify token is set by Home Assistant (check logs with `addon_uuid`) |
| Configuration not persisting | Saving outside /data/ | Always use bashio::addon::config_path or /data/ for persistence |
| Port already in use | Multiple services on same port | Check configuration - each service needs unique port |
| Architecture mismatch | {arch} placeholder not used | Use exact placeholder in image field: `ghcr.io/home-assistant/{arch}-base` |
| Build fails with "Unknown architecture" | config.yaml lists unsupported arch | Use only: amd64, armv7, aarch64, armhf, i386 |

## Supervisor API Endpoints

```bash
# Authentication: Pass SUPERVISOR_TOKEN header
# Base URL: http://supervisor

GET /addons/self/info            # Get current add-on details
POST /addons/self/restart        # Restart this add-on
GET /addons/installed            # List installed add-ons
GET /info                        # System information
POST /notifications/create       # Send notification to user
GET /config/homeassistant        # Read Home Assistant config

# Example with bashio
bashio::addon::self_info         # Helper function for self info
```

## Dependencies

### Required

| Package | Version | Purpose |
|---------|---------|---------|
| Home Assistant | 2024.1+ | Add-on platform and supervisor |
| Docker | Latest | Container runtime |
| S6 Overlay | 3.x | Init system (included in base images) |

### Optional

| Package | Version | Purpose |
|---------|---------|---------|
| bashio | Latest | Helper functions (included in base images) |
| python3 | 3.9+ | Python-based add-ons |
| nodejs | 18+ | Node.js-based add-ons |

## Official Documentation

- [Home Assistant Add-On Development](https://developers.home-assistant.io/docs/add-ons)
- [Add-On Configuration Reference](https://developers.home-assistant.io/docs/add-ons/configuration)
- [Supervisor Development](https://developers.home-assistant.io/docs/supervisor/developing)
- [bashio Helper Functions](https://github.com/hassio-addons/bashio)
- [S6 Overlay Documentation](https://skarnet.org/software/s6-overlay/)

## Troubleshooting

### Add-on Won't Start

**Symptoms:** Add-on shows as "Not running" or "Unknown"

**Solution:**
```bash
# Check logs
docker logs addon_name_latest  # Or use HA UI: Settings > System > Logs

# Common causes:
# 1. Invalid config.yaml syntax
# 2. Missing S6 service files
# 3. Dockerfile can't find base image
# 4. Permission denied on rootfs files
```

### Supervisor API Returns 401

**Symptoms:** API calls fail with "Unauthorized"

**Solution:**
```bash
# Verify SUPERVISOR_TOKEN is set
echo $SUPERVISOR_TOKEN

# Check add-on logs for token errors
# Token is automatically injected by Home Assistant

# Verify permissions in config.yaml
# If calling hassio endpoints, add: permissions: [hassio]
```

### Configuration Not Saving

**Symptoms:** Options are lost after restart

**Solution:**
```bash
# Always save to /data/ or use bashio
CONFIG_PATH="$(bashio::addon::config_path)"  # Returns /data/
echo "my_value=123" > "${CONFIG_PATH}/settings.json"

# Verify /data/ exists and is writable
ls -la /data/
```

### Ingress Web UI Not Accessible

**Symptoms:** Ingress URL returns 502 or blank page

**Solution:**
```bash
# 1. Verify service is listening on correct port
netstat -tlnp | grep 8080

# 2. Check reverse proxy headers in app config
# X-Forwarded-For, X-Forwarded-Proto must be set

# 3. Verify ingress settings in config.yaml
ingress: true
ingress_port: 8080
ingress_entry: /
```

### Build Fails with Architecture Error

**Symptoms:** "Unknown architecture" or "Image not found"

**Solution:**
```yaml
# Check config.yaml has valid arch values
arch:
  - amd64      # x86 64-bit
  - armv7      # 32-bit ARM (Pi 2/3)
  - aarch64    # 64-bit ARM (Pi 4+)
  - armhf      # 32-bit ARM (older devices)
  - i386       # 32-bit x86 (rare)

# Dockerfile must use {arch} placeholder
FROM ghcr.io/home-assistant/{arch}-base:latest
```

## Setup Checklist

Before publishing your add-on, verify:

- [ ] config.yaml has valid YAML syntax (use online YAML validator)
- [ ] All listed architectures are supported (amd64, armv7, aarch64, armhf, i386)
- [ ] Dockerfile uses official Home Assistant base image
- [ ] S6 service files exist and are executable (chmod +x)
- [ ] All configuration options are documented in schema
- [ ] No hardcoded paths (use bashio helpers)
- [ ] Permissions field lists required supervisor API access
- [ ] Tested on at least amd64 and ARM architecture
- [ ] Logs use bashio::log functions
- [ ] Graceful shutdown on SIGTERM implemented
- [ ] /data/ used for all persistent data
- [ ] Ingress working if web UI is provided
- [ ] README includes installation and usage instructions

## Creating a Repository

To publish multiple add-ons:

### 1. Create Repository Structure

```bash
mkdir my-addon-repo
cd my-addon-repo
```

### 2. Create repository.yaml

```yaml
---
name: My Add-On Repository
url: https://github.com/username/my-addon-repo
maintainer: Your Name <email@example.com>
```

### 3. Add Add-Ons

```
my-addon-repo/
├── repository.yaml
├── my-addon-1/
│   ├── config.yaml
│   ├── Dockerfile
│   └── rootfs/
└── my-addon-2/
    ├── config.yaml
    ├── Dockerfile
    └── rootfs/
```

### 4. Push to GitHub

Add the repository URL to Home Assistant to make add-ons discoverable.

## Advanced: Publishing to GitHub Container Registry

For private repositories or multi-architecture builds:

```bash
# Build and push for all architectures
docker buildx build \
  --platform linux/amd64,linux/arm/v7,linux/arm64/v8 \
  -t ghcr.io/username/my-addon:1.0.0 \
  --push .
```

## Related Skills

- `docker-configs` - Docker fundamentals and best practices
- `esphome-config-helper` - Related IoT device integration patterns
- `home-assistant-automation` - Home Assistant automation and scripting
