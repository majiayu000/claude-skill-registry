---
name: docker-cleanup
description: Clean up Docker resources including volumes, containers, images, and networks. Use this skill when asked to "clean docker", "prune volumes", "remove unused containers", "free disk space from docker", "docker cleanup", "remove dangling images", or when troubleshooting Docker Desktop issues like unresponsive daemon, hanging commands, or VM problems. Covers volume pruning, identifying dangling/unused resources, container/image removal, Docker Desktop troubleshooting (restart procedures, VM issues), and system-wide cleanup.
---

# Docker Cleanup

## Quick Commands Reference

| Task                      | Command                             |
| ------------------------- | ----------------------------------- |
| List all volumes          | `docker volume ls`                  |
| List dangling volumes     | `docker volume ls -f dangling=true` |
| Prune unused volumes      | `docker volume prune`               |
| List all containers       | `docker ps -a`                      |
| List stopped containers   | `docker ps -a -f status=exited`     |
| Remove stopped containers | `docker container prune`            |
| List dangling images      | `docker images -f dangling=true`    |
| Remove dangling images    | `docker image prune`                |
| Remove all unused images  | `docker image prune -a`             |
| Full system cleanup       | `docker system prune`               |
| Full cleanup + volumes    | `docker system prune --volumes`     |
| Nuclear option            | `docker system prune -a --volumes`  |

## Troubleshooting Docker Desktop (macOS)

### Symptoms of Unresponsive Docker

- Commands hang indefinitely (no output)
- `docker info` or `docker ps` never return
- Docker Desktop icon shows running but CLI unresponsive

### Diagnostic Steps

1. Check if Docker processes are running:

```bash
pgrep -l -f "Docker"
```

2. Check Docker socket:

```bash
ls -la /var/run/docker.sock
```

3. Test basic connectivity:

```bash
docker version 2>&1
```

### Resolution Steps

**Restart Docker Desktop (GUI):**

1. Click Docker icon in menu bar
2. Select "Restart" or "Quit Docker Desktop"
3. Reopen Docker Desktop
4. Wait for icon to stop animating (fully started)

**Restart Docker Desktop (CLI):**

```bash
# Quit Docker Desktop
osascript -e 'quit app "Docker"'

# Wait a moment
sleep 5

# Reopen Docker Desktop
open -a Docker

# Wait for startup (check with loop)
while ! docker info >/dev/null 2>&1; do
  echo "Waiting for Docker to start..."
  sleep 2
done
echo "Docker is ready"
```

**Factory Reset (last resort):**

1. Docker Desktop > Preferences > Reset > Reset to factory defaults
2. Warning: This removes all containers, images, and volumes

### VM Issues

If Docker VM is corrupted:

```bash
# Stop Docker
osascript -e 'quit app "Docker"'

# Remove Docker VM files (careful!)
rm -rf ~/Library/Containers/com.docker.docker
rm -rf ~/Library/Group\ Containers/group.com.docker

# Restart Docker Desktop
open -a Docker
```

## Cleanup Workflows

### Safe Incremental Cleanup

Start conservative, escalate as needed:

```bash
# 1. Remove stopped containers
docker container prune -f

# 2. Remove dangling images (untagged)
docker image prune -f

# 3. Remove unused networks
docker network prune -f

# 4. Remove unused volumes (careful - data loss!)
docker volume prune -f
```

### Aggressive Cleanup

For maximum space recovery (destructive):

```bash
# Remove everything unused: containers, networks, images, volumes
docker system prune -a --volumes -f
```

### Inspect Before Removing

**Check volume usage:**

```bash
# List volumes with size (requires docker system df)
docker system df -v

# Inspect specific volume
docker volume inspect <volume_name>
```

**Find what's using a volume:**

```bash
docker ps -a --filter volume=<volume_name>
```

**Check image layers:**

```bash
docker history <image_name>
```

### Selective Removal

**Remove specific volumes:**

```bash
docker volume rm volume1 volume2
```

**Remove volumes matching pattern:**

```bash
docker volume ls -q | grep "pattern" | xargs docker volume rm
```

**Remove old containers (stopped > 24h ago):**

```bash
docker container prune --filter "until=24h"
```

**Remove images older than 7 days:**

```bash
docker image prune -a --filter "until=168h"
```

## Disk Space Analysis

```bash
# Overview of Docker disk usage
docker system df

# Detailed breakdown
docker system df -v

# Find large images
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}" | sort -k2 -h
```

## Safety Notes

- `docker volume prune` removes **all** volumes not attached to containers - verify important data is backed up
- `-f` flag skips confirmation prompts - use carefully
- `docker system prune -a` removes **all** unused images, not just dangling ones
- Running containers and their resources are never affected by prune commands
