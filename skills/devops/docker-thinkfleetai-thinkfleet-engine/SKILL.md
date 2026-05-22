---
name: docker
description: "Manage Docker containers, images, networks, and volumes using the Docker CLI."
metadata: {"thinkfleetbot":{"emoji":"🐳","requires":{"bins":["docker"]}}}
---

# Docker

Manage Docker containers, images, networks, and volumes.

## List containers

```bash
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
```

```bash
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | head -20
```

## Container logs

```bash
docker logs my-container --tail 50
```

```bash
docker logs my-container --since 1h --follow &
```

## Start / stop / restart

```bash
docker start my-container
```

```bash
docker stop my-container
```

```bash
docker restart my-container
```

## Run a container

```bash
docker run -d --name my-app -p 8080:80 nginx:latest
```

## Execute command in container

```bash
docker exec my-container ls -la /app
```

```bash
docker exec -it my-container sh
```

## Inspect container

```bash
docker inspect my-container | jq '.[0] | {State, NetworkSettings: .NetworkSettings.Networks}'
```

## List images

```bash
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}" | head -20
```

## Build image

```bash
docker build -t my-app:latest .
```

## Remove container / image

```bash
docker rm my-container
```

```bash
docker rmi my-app:latest
```

## Docker Compose

```bash
docker compose ps
```

```bash
docker compose up -d
```

```bash
docker compose logs --tail 50
```

## System info

```bash
docker system df
```

```bash
docker system prune --dry-run
```

## Networks

```bash
docker network ls
```

## Volumes

```bash
docker volume ls
```

## Notes

- Docker socket must be mounted for the agent to access the host Docker daemon.
- Use `--format` with Go templates for structured output.
- Always confirm before removing containers, images, or running `prune`.
- Use `docker compose` (v2) instead of `docker-compose` (v1).
