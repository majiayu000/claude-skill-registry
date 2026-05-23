---
name: postgresql-docker
description: PostgreSQL in containers - Docker, Kubernetes, production configs
version: "3.0.0"
sasmp_version: "1.3.0"
bonded_agent: 08-postgresql-devops
bond_type: SECONDARY_BOND
category: database
difficulty: intermediate
estimated_time: 2h
---

# PostgreSQL Docker Skill

> Atomic skill for containerized PostgreSQL

## Overview

Production-ready patterns for Docker and Kubernetes PostgreSQL deployments.

## Prerequisites

- Docker or Kubernetes
- Understanding of volumes
- Resource planning

## Parameters

```yaml
parameters:
  platform:
    type: string
    required: true
    enum: [docker, kubernetes, compose]
  environment:
    type: string
    enum: [development, staging, production]
```

## Quick Reference

### Docker Compose
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
    deploy:
      resources:
        limits:
          memory: 4G
    command:
      - postgres
      - -c
      - shared_buffers=1GB
      - -c
      - max_connections=200

volumes:
  postgres_data:
```

### Kubernetes StatefulSet
```yaml
apiVersion: apps/v1
kind: StatefulSet
spec:
  template:
    spec:
      containers:
        - name: postgres
          image: postgres:16
          resources:
            limits:
              memory: "4Gi"
          readinessProbe:
            exec:
              command: ["pg_isready"]
          volumeMounts:
            - name: data
              mountPath: /var/lib/postgresql/data
```

### Configuration Tips
```bash
# Pass config via command
postgres -c shared_buffers=1GB -c work_mem=64MB

# Use init scripts
./init.sql -> /docker-entrypoint-initdb.d/
```

## Resource Guidelines

| Workload | Memory | CPU |
|----------|--------|-----|
| Dev | 512MB | 0.5 |
| Staging | 2GB | 1 |
| Production | 4GB+ | 2+ |

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| OOM killed | Low memory limit | Increase limits |
| Slow startup | No init cache | Use pg_prewarm |
| Data loss | No volume | Mount persistent volume |

## Usage

```
Skill("postgresql-docker")
```
