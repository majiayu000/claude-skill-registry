---
name: act-docker-setup
description: Use when configuring Docker environments for act, selecting runner images, managing container resources, or troubleshooting Docker-related issues with local GitHub Actions testing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Act - Docker Configuration and Setup

Use this skill when configuring Docker for act, choosing runner images, managing container resources, and optimizing Docker performance for local GitHub Actions workflow testing.

## Runner Images

### Image Size Categories

Act supports three image size categories:

| Size | Image | Tools | Use Case |
|------|-------|-------|----------|
| Micro | `node:16-buster-slim` | Minimal | Simple Node.js workflows |
| Medium | `catthehacker/ubuntu:act-*` | Common tools | Most workflows |
| Large | `catthehacker/ubuntu:full-*` | Everything | Maximum compatibility |

### Official catthehacker Images

```bash
# Latest Ubuntu (22.04)
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# Specific Ubuntu versions
act -P ubuntu-22.04=catthehacker/ubuntu:act-22.04
act -P ubuntu-20.04=catthehacker/ubuntu:act-20.04

# Full images (larger, more tools)
act -P ubuntu-latest=catthehacker/ubuntu:full-latest
act -P ubuntu-22.04=catthehacker/ubuntu:full-22.04

# Runner images (closest to GitHub)
act -P ubuntu-latest=catthehacker/ubuntu:runner-latest
```

### Language-Specific Images

```bash
# Node.js
act -P ubuntu-latest=node:20
act -P ubuntu-latest=node:20-alpine

# Python
act -P ubuntu-latest=python:3.12
act -P ubuntu-latest=python:3.12-slim

# Go
act -P ubuntu-latest=golang:1.22
act -P ubuntu-latest=golang:1.22-alpine

# Ruby
act -P ubuntu-latest=ruby:3.3
act -P ubuntu-latest=ruby:3.3-alpine
```

## Platform Configuration

### .actrc Configuration

Create `.actrc` in project root for persistent settings:

```
# Default platform images
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-P ubuntu-22.04=catthehacker/ubuntu:act-22.04
-P ubuntu-20.04=catthehacker/ubuntu:act-20.04

# Reuse containers
--reuse

# Container options
--container-architecture linux/amd64
--container-daemon-socket -

# Resource limits
--container-cap-add SYS_PTRACE
--container-cap-add NET_ADMIN
```

### Per-Workflow Configuration

Create `.github/workflows/.actrc` for workflow-specific settings:

```
-P ubuntu-latest=node:20
--env-file .env.ci
```

### Command Line Override

```bash
# Override .actrc settings
act -P ubuntu-latest=python:3.12 --no-reuse
```

## Container Management

### Reusing Containers

```bash
# Reuse containers for faster iteration
act --reuse

# Reuse with specific job
act --reuse -j build

# Force recreate containers
act --rm
```

### Container Lifecycle

```bash
# List running act containers
docker ps --filter "label=act"

# Stop all act containers
docker stop $(docker ps -q --filter "label=act")

# Remove all act containers
docker rm $(docker ps -aq --filter "label=act")

# Clean up act volumes
docker volume prune
```

### Inspect Containers

```bash
# Exec into running container
docker exec -it act-<job-name> /bin/bash

# View container logs
docker logs act-<job-name>

# Inspect container config
docker inspect act-<job-name>
```

## Volume Mounts and Binds

### Default Mounts

Act automatically mounts:

- Current directory → `/github/workspace`
- Act cache → `/root/.cache/act`
- Docker socket (if needed)

### Custom Bind Mounts

```bash
# Mount additional directory
act --bind /host/path:/container/path

# Mount multiple directories
act --bind /data:/data --bind /config:/config

# Read-only mount
act --bind /readonly:/readonly:ro
```

### Persistent Cache

```bash
# Configure cache location
export ACT_CACHE_DIR=$HOME/.cache/act

# Clean cache
rm -rf $HOME/.cache/act
```

## Docker Configuration

### Docker Socket

```bash
# Use default Docker socket
act --container-daemon-socket -

# Use custom socket
act --container-daemon-socket /var/run/docker.sock

# Use Docker Desktop socket (Mac)
act --container-daemon-socket unix:///Users/$USER/.docker/run/docker.sock
```

### Container Architecture

```bash
# Specify architecture
act --container-architecture linux/amd64

# For Apple Silicon Macs
act --container-architecture linux/arm64
```

### Network Configuration

```bash
# Use host network
act --network host

# Use custom network
act --network my-network

# Create isolated network
docker network create act-network
act --network act-network
```

## Resource Management

### Memory Limits

```bash
# Set memory limit
act --memory 4g

# Set memory and swap
act --memory 4g --memory-swap 8g
```

### CPU Limits

```bash
# Limit CPU cores
act --cpus 2

# Set CPU shares
act --cpu-shares 512
```

### Disk Space

```bash
# Check Docker disk usage
docker system df

# Clean up unused resources
docker system prune -a

# Remove old act cache
find ~/.cache/act -type d -mtime +30 -exec rm -rf {} +
```

## Security

### Capabilities

```bash
# Add Linux capabilities
act --container-cap-add SYS_PTRACE

# Drop capabilities
act --container-cap-drop ALL

# Security profile
act --security-opt seccomp=unconfined
```

### Privileged Mode

```bash
# Run in privileged mode (use sparingly)
act --privileged

# Safer: add specific capabilities instead
act --container-cap-add SYS_ADMIN
```

## Multi-Platform Builds

### Docker Buildx

```yaml
# Workflow using buildx
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v5
        with:
          platforms: linux/amd64,linux/arm64
```

Test with act:

```bash
# Enable buildx in act
act --use-gitignore=false \
    -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

## Troubleshooting

### Image Pull Failures

```bash
# Pull image manually
docker pull catthehacker/ubuntu:act-latest

# Use cached image
act --pull=false

# Force pull latest
act --pull=true
```

### Permission Issues

```bash
# Fix workspace permissions
act --container-options "--user $(id -u):$(id -g)"

# Run as root (not recommended)
act --container-options "--user root"
```

### DNS Issues

```bash
# Use custom DNS
act --container-options "--dns 8.8.8.8"

# Use host DNS
act --container-options "--dns-search ."
```

### Container Exit Codes

```bash
# Continue on error
act --continue-on-error

# Capture exit code
act; echo $?
```

## Performance Optimization

### Image Selection

Choose the smallest image that meets your needs:

```bash
# Fast but limited
act -P ubuntu-latest=node:20-alpine

# Balanced
act -P ubuntu-latest=catthehacker/ubuntu:act-latest

# Comprehensive but slow
act -P ubuntu-latest=catthehacker/ubuntu:full-latest
```

### Layer Caching

```yaml
# Optimize Dockerfile for caching
FROM node:20

# Install system deps first (changes rarely)
RUN apt-get update && apt-get install -y git

# Copy package files (changes sometimes)
COPY package*.json ./

# Install deps (changes sometimes)
RUN npm ci

# Copy source (changes often)
COPY . .
```

### Parallel Jobs

```bash
# Run jobs in parallel
act --parallel

# Limit parallelism
act --parallel --jobs 2
```

## Custom Images

### Building Custom Image

Create `Dockerfile`:

```dockerfile
FROM catthehacker/ubuntu:act-latest

# Add custom tools
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Install specific Node version
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Install global npm packages
RUN npm install -g pnpm yarn
```

Build and use:

```bash
docker build -t my-act-runner .
act -P ubuntu-latest=my-act-runner
```

### Publishing Custom Image

```bash
# Tag image
docker tag my-act-runner username/act-runner:latest

# Push to Docker Hub
docker push username/act-runner:latest

# Use in team
act -P ubuntu-latest=username/act-runner:latest
```

## Best Practices

### DO

✅ Use `.actrc` for consistent configuration across team
✅ Choose appropriate image size for your needs
✅ Use `--reuse` during development
✅ Clean up Docker resources regularly
✅ Pin image versions in production workflows
✅ Use layer caching for faster builds
✅ Document image requirements in README

### DON'T

❌ Use `:latest` tags in production
❌ Run containers in privileged mode unnecessarily
❌ Ignore Docker disk space usage
❌ Use oversized images for simple workflows
❌ Commit large images to version control
❌ Skip Docker resource cleanup
❌ Expose sensitive data in container logs

## Common Patterns

### Development Setup

```bash
# Fast iteration setup
cat > .actrc << 'EOF'
-P ubuntu-latest=catthehacker/ubuntu:act-latest
--reuse
--rm=false
--container-architecture linux/amd64
EOF
```

### CI Validation

```bash
# Strict validation setup
act --dryrun \
    --pull=true \
    --no-reuse \
    -P ubuntu-latest=catthehacker/ubuntu:full-latest
```

### Monorepo Setup

```bash
# Different images per job
act -j backend -P ubuntu-latest=node:20 \
    -j frontend -P ubuntu-latest=node:20-alpine \
    -j database -P ubuntu-latest=postgres:16
```

## Related Skills

- **act-workflow-syntax**: Creating workflow files
- **act-local-testing**: Testing workflows with act CLI
- **act-advanced-features**: Advanced act usage patterns
