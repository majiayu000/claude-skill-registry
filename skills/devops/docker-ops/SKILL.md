---
name: docker-ops
description: >
  Safe Docker cleanup and compose stack management.
  Prune unused containers/images/volumes, redeploy stacks.
triggers:
  - clean up docker
  - prune docker
  - docker cleanup
  - redeploy stack
  - restart containers
  - docker compose redeploy
  - free docker disk space
allowed-tools: Bash
metadata:
  short-description: Safe Docker cleanup and stack management
---

# Docker Ops

Safe Docker management with dry-run defaults.

## Commands

```bash
# Prune unused resources (dry-run by default)
./scripts/prune.sh

# Actually prune
./scripts/prune.sh --execute

# Prune images older than 24h
./scripts/prune.sh --until 24h --execute

# Redeploy compose stack (dry-run)
./scripts/redeploy.sh --stack docker-compose.yml

# Actually redeploy
./scripts/redeploy.sh --stack docker-compose.yml --execute

# Redeploy specific service
./scripts/redeploy.sh --stack docker-compose.yml --service web --execute
```

## Environment Variables

| Variable             | Default            | Description                   |
| -------------------- | ------------------ | ----------------------------- |
| `DOCKER_PRUNE_UNTIL` | -                  | Default age filter for prune  |
| `STACK_FILE`         | docker-compose.yml | Default compose file          |
| `HEALTH_CMD`         | -                  | Command to run after redeploy |
