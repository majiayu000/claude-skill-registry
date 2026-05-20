---
name: container-debugging
description: Debug Docker containers and containerized applications. Diagnose deployment issues, container lifecycle problems, and resource constraints.
---

# Container Debugging

## Overview

Container debugging focuses on issues within Docker/Kubernetes environments including resource constraints, networking, and application runtime problems.

## When to Use

- Container won't start
- Application crashes in container
- Resource limits exceeded
- Network connectivity issues
- Performance problems in containers

## Instructions

### 1. **Docker Debugging Basics**

```bash
# Check container status
docker ps -a
docker inspect <container-id>
docker stats <container-id>

# View container logs
docker logs <container-id>
docker logs --follow <container-id>  # Real-time
docker logs --tail 100 <container-id>  # Last 100 lines

# Connect to running container
docker exec -it <container-id> /bin/bash
docker exec -it <container-id> sh

# Inspect container details
docker inspect <container-id> | grep -A 5 "State"
docker inspect <container-id> | grep -E "Memory|Cpu"

# Check container processes
docker top <container-id>

# View resource usage
docker stats <container-id>
# Shows: CPU%, Memory usage, Network I/O

# Copy files from container
docker cp <container-id>:/path/to/file /local/path

# View image layers
docker history <image-name>
docker inspect <image-name>
```

### 2. **Common Container Issues**

```yaml
Issue: Container Won't Start

Diagnosis:
  1. docker logs <container-id>
  2. Check exit code: docker inspect (ExitCode)
  3. Verify image exists: docker images
  4. Check entrypoint: docker inspect --format='{{.Config.Entrypoint}}'

Common Exit Codes:
  0: Normal exit
  1: General application error
  127: Command not found
  128+N: Terminated by signal N
  137: Out of memory (SIGKILL)
  139: Segmentation fault

Solutions:
  - Fix application error
  - Ensure required files exist
  - Check executable permissions
  - Verify working directory

---

Issue: Out of Memory

Symptoms: Exit code 137 (SIGKILL)

Debug:
  docker stats <container-id>
  # Check Memory usage vs limit

Solution:
  docker run -m 512m <image>
  # Increase memory limit
  docker inspect (MemoryLimit)
  # Check current limit

---

Issue: Port Already in Use

Error: "bind: address already in use"

Debug:
  docker ps  # Check running containers
  netstat -tlnp | grep 8080  # Check port usage

Solution:
  docker run -p 8081:8080 <image>
  # Use different host port

---

Issue: Network Issues

Symptom: Cannot reach other containers

Debug:
  docker network ls
  docker inspect <container-id> | grep IPAddress
  docker exec <container-id> ping <other-container>

Solution:
  docker network create app-network
  docker run --network app-network <image>
```

### 3. **Container Optimization**

```yaml
Resource Limits:

Set in docker-compose:
  version: '3'
  services:
    app:
      image: myapp
      environment:
        - NODE_ENV=production
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M

Limits: Maximum resources
Reservations: Guaranteed resources

---

Multi-Stage Builds:

FROM node:16 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm install --production
EXPOSE 3000
CMD ["node", "dist/index.js"]

Result: 1GB → 200MB image size
```

### 4. **Debugging Checklist**

```yaml
Container Issues:

[ ] Container starts without error
[ ] Ports mapped correctly
[ ] Logs show no errors
[ ] Environment variables set
[ ] Volumes mounted correctly
[ ] Network connectivity works
[ ] Resource limits appropriate
[ ] Permissions correct
[ ] Dependencies installed
[ ] Entrypoint working

Kubernetes Issues:

[ ] Pod running (not Pending/CrashLoop)
[ ] All containers started
[ ] Readiness probes passing
[ ] Liveness probes passing
[ ] Resource requests/limits set
[ ] Network policies allow traffic
[ ] Secrets/ConfigMaps available
[ ] Logs show no errors

Tools:

docker:
  - logs
  - stats
  - inspect
  - exec

docker-compose:
  - logs
  - ps
  - config

kubectl (Kubernetes):
  - logs
  - describe pod
  - get events
  - port-forward
```

## Key Points

- Check logs first: `docker logs <container>`
- Understand exit codes (137=OOM, 127=not found)
- Use resource limits appropriately
- Network containers on same network
- Multi-stage builds reduce image size
- Monitor resource usage with stats
- Port mappings: host:container
- Exec into running containers for debugging
- Update base images regularly
- Include health checks in containers
