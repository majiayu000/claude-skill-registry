---
name: using-docker-in-web
description: Set up and use Docker in Claude Code for Web environments. Use when Docker builds fail with bridge/iptables errors, SSL certificate errors through proxy, or when working in containerized web environments.
---

# Docker in Claude Code for Web

Claude Code for Web runs in a restricted container environment that requires special configuration for Docker.

## Detection

You're in Claude Code for Web if:

```bash
# Proxy environment is set
echo $http_proxy  # Shows a proxy URL

# Running inside a container
test -f /.dockerenv && echo "In container"

# iptables is restricted
iptables -L 2>&1 | grep -q "Permission denied"
```

## Quick Setup

```bash
# Install Docker
sudo apt-get update && sudo apt-get install -y docker.io

# Start daemon with restrictions (background)
sudo dockerd --iptables=false --bridge=none &

# Wait for daemon to be ready
sleep 3

# Verify
docker info
```

## Building csb Images

Standard builds fail because Docker tries to create bridge networks. Use these flags:

```bash
# Build with host networking and insecure SSL (for intercepting proxy)
csb build --host-network --insecure
```

What these flags do:

- `--host-network`: Uses host networking instead of bridge (which requires iptables)
- `--insecure`: Adds `-k` to curl commands and disables npm strict-ssl (for SSL-intercepting proxies)

## Creating Sandboxes

Sandbox creation also needs host networking:

```bash
# When creating sandboxes, they'll run in the Docker network
# The proxy container won't work (needs iptables), so use --egress=all
csb create my-sandbox --egress=all
```

## Common Errors and Fixes

### "iptables: Permission denied"

The daemon is trying to manage iptables rules. Restart with:

```bash
sudo pkill dockerd
sudo dockerd --iptables=false --bridge=none &
```

### "network bridge not found"

Same issue - daemon needs `--bridge=none` flag.

### "SSL certificate problem"

The proxy intercepts HTTPS. Use `--insecure` flag with csb build, or for manual curl:

```bash
curl -k https://example.com
```

### "npm ERR! unable to verify certificate"

```bash
npm config set strict-ssl false
npm install
npm config set strict-ssl true  # Reset after
```

## Full Workflow Example

```bash
# 1. Install and start Docker
sudo apt-get update && sudo apt-get install -y docker.io
sudo dockerd --iptables=false --bridge=none &
sleep 3

# 2. Build csb images
csb build --host-network --insecure

# 3. Create a sandbox
csb create dev --egress=all

# 4. Connect
csb ssh dev
```

## Limitations

In Claude Code for Web:

- No bridge networking - containers share host network
- No egress proxy container (requires iptables)
- SSL verification must be disabled for builds
- GPU passthrough not available

## Cleanup

```bash
# Stop all containers
docker stop $(docker ps -q) 2>/dev/null

# Stop daemon
sudo pkill dockerd
```
