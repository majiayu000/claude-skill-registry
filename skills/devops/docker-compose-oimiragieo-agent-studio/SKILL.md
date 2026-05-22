---
name: docker-compose
description: Docker Compose container orchestration and management. Manage multi-container applications, services, networks, and volumes. Use for local development, testing, and orchestration of containerized applications.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read, Glob]
best_practices:
  - Verify docker-compose.yml exists before operations
  - Use project names for isolation
  - Check service status before destructive operations
  - Avoid volume removal without confirmation
  - Review logs before restarting failed services
error_handling: graceful
streaming: supported
safety_level: high
---

# Docker Compose Skill

## Installation

The skill invokes `docker compose`. Easiest: install **Docker Desktop** (includes Docker Engine + Compose):

- **Windows**: [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) (WSL 2 or Hyper-V)
- **Mac**: [Docker Desktop for Mac](https://docs.docker.com/desktop/setup/install/mac-install/) (Apple Silicon or Intel)
- **Linux**: [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/) or Docker Engine + Compose plugin from Docker’s repo

Verify: `docker compose version`

## Cheat Sheet & Best Practices

**Commands:** `docker compose up -d` / `down`; `docker compose ps` / `logs -f <service>`; `docker compose exec <service> sh`; `docker compose build --no-cache`; `docker compose -f compose.prod.yaml config` — validate.

**YAML:** Use named volumes for DBs (`postgres_data:/var/lib/postgresql/data`). Use healthchecks (`healthcheck:` with `test`, `interval`, `timeout`, `retries`). One network default; reference services by name (e.g. `http://api:3000`). Use `env_file` or `environment`; keep secrets in `secrets:`.

**Hacks:** `-f compose.yaml -f override.yaml` merges files (later overrides). Use `--project-name` for isolation. Prefer `build: context: . dockerfile: Dockerfile` for dev; pin image tags in prod. Run `docker compose config` before `up` to catch errors.

## Certifications & Training

**Docker Certified Associate (DCA):** Orchestration 25%, Image/Registry 20%, Install/Config 15%, Networking 15%, Security 15%, Storage 10%. Free: [Official DCA Study Guide](https://www.docker.com/certification/), [Coursera DCA Prep](https://www.coursera.org/specializations/docker-certified-associate-dca-course) (audit). **Skill data:** Compose YAML (services, volumes, networks, healthchecks), CLI (up/down/ps/logs/exec).

## Hooks & Workflows

**Suggested hooks:** Pre-up: `docker compose config` (validate). Post-down: optional cleanup. Use when **devops** or **devops-troubleshooter** is routed.

**Workflows:** Use with **devops** (primary), **devops-troubleshooter** (primary). Flow: validate compose → up/down/exec per task. See `operations/incident-response` for container debugging.

## Overview

This skill provides comprehensive Docker Compose management, enabling AI agents to orchestrate multi-container applications, manage services, inspect logs, and troubleshoot containerized environments with progressive disclosure for optimal context usage.

**Context Savings**: ~92% reduction

- **MCP Mode**: ~25,000 tokens always loaded (multiple tools + schemas)
- **Skill Mode**: ~700 tokens metadata + on-demand loading

## When to Use

- Managing local development environments
- Orchestrating multi-container applications
- Debugging service connectivity and networking
- Monitoring container logs and health
- Building and updating service images
- Testing containerized application stacks
- Troubleshooting service failures
- Managing application lifecycle (start, stop, restart)

## Requirements

- Docker Engine installed and running
- Docker Compose V2 (docker compose) or V1 (docker-compose)
- Valid docker-compose.yml file in project
- Appropriate permissions for Docker socket access

## Quick Reference

```bash
# List running services
docker compose ps

# View service logs
docker compose logs <service>

# Start services
docker compose up -d

# Stop services
docker compose down

# Rebuild services
docker compose build

# Execute command in container
docker compose exec <service> <command>
```

## Tools

The skill provides 15 tools across service management, monitoring, build operations, and troubleshooting categories:

### Service Management (5 tools)

#### up

Start services defined in docker-compose.yml.

| Parameter        | Type    | Description                  | Default        |
| ---------------- | ------- | ---------------------------- | -------------- |
| `detached`       | boolean | Run in detached mode         | true           |
| `build`          | boolean | Build images before starting | false          |
| `force_recreate` | boolean | Recreate containers          | false          |
| `project_name`   | string  | Project name override        | directory name |
| `services`       | array   | Specific services to start   | all services   |

**Example**:

```bash
docker compose up -d
docker compose up --build
docker compose up web api
```

**Safety**: Requires confirmation for production environments.

#### down

Stop and remove containers, networks, volumes.

| Parameter        | Type    | Description                | Default        |
| ---------------- | ------- | -------------------------- | -------------- |
| `volumes`        | boolean | Remove volumes (BLOCKED)   | false          |
| `remove_orphans` | boolean | Remove orphaned containers | false          |
| `project_name`   | string  | Project name override      | directory name |

**Example**:

```bash
docker compose down
docker compose down --remove-orphans
```

**Safety**: Volume removal (`-v` flag) is **BLOCKED** by default. Requires confirmation.

#### start

Start existing containers without recreating them.

| Parameter      | Type   | Description                | Default        |
| -------------- | ------ | -------------------------- | -------------- |
| `services`     | array  | Specific services to start | all services   |
| `project_name` | string | Project name override      | directory name |

**Example**:

```bash
docker compose start
docker compose start web
```

#### stop

Stop running containers without removing them.

| Parameter      | Type   | Description                | Default        |
| -------------- | ------ | -------------------------- | -------------- |
| `timeout`      | number | Shutdown timeout (seconds) | 10             |
| `services`     | array  | Specific services to stop  | all services   |
| `project_name` | string | Project name override      | directory name |

**Example**:

```bash
docker compose stop
docker compose stop --timeout 30 web
```

#### restart

Restart services (stop + start).

| Parameter      | Type   | Description                  | Default        |
| -------------- | ------ | ---------------------------- | -------------- |
| `timeout`      | number | Shutdown timeout (seconds)   | 10             |
| `services`     | array  | Specific services to restart | all services   |
| `project_name` | string | Project name override        | directory name |

**Example**:

```bash
docker compose restart
docker compose restart api
```

### Status & Logs (3 tools)

#### ps

List containers with status information.

| Parameter      | Type    | Description                             | Default        |
| -------------- | ------- | --------------------------------------- | -------------- |
| `all`          | boolean | Show all containers (including stopped) | false          |
| `services`     | array   | Filter by services                      | all services   |
| `project_name` | string  | Project name override                   | directory name |

**Example**:

```bash
docker compose ps
docker compose ps --all
```

**Output Fields**: NAME, IMAGE, STATUS, PORTS

#### logs

View service logs with streaming support.

| Parameter      | Type    | Description                        | Default        |
| -------------- | ------- | ---------------------------------- | -------------- |
| `services`     | array   | Services to view logs for          | all services   |
| `follow`       | boolean | Follow log output (stream)         | false          |
| `tail`         | number  | Number of lines to show            | 100            |
| `timestamps`   | boolean | Show timestamps                    | false          |
| `since`        | string  | Show logs since timestamp/duration | none           |
| `project_name` | string  | Project name override              | directory name |

**Example**:

```bash
docker compose logs web
docker compose logs --tail 50 --follow api
docker compose logs --since "2024-01-01T10:00:00"
```

**Note**: Follow mode automatically terminates after 60 seconds to prevent indefinite streaming.

#### top

Display running processes in containers.

| Parameter      | Type   | Description           | Default        |
| -------------- | ------ | --------------------- | -------------- |
| `services`     | array  | Services to inspect   | all services   |
| `project_name` | string | Project name override | directory name |

**Example**:

```bash
docker compose top
docker compose top web
```

**Output**: Process list with PID, USER, TIME, COMMAND

### Build & Images (3 tools)

#### build

Build or rebuild service images.

| Parameter      | Type    | Description               | Default        |
| -------------- | ------- | ------------------------- | -------------- |
| `no_cache`     | boolean | Build without cache       | false          |
| `pull`         | boolean | Pull newer image versions | false          |
| `parallel`     | boolean | Build in parallel         | true           |
| `services`     | array   | Services to build         | all services   |
| `project_name` | string  | Project name override     | directory name |

**Example**:

```bash
docker compose build
docker compose build --no-cache web
docker compose build --pull
```

**Safety**: Requires confirmation for no-cache builds (resource-intensive).

#### pull

Pull service images from registry.

| Parameter              | Type    | Description            | Default        |
| ---------------------- | ------- | ---------------------- | -------------- |
| `ignore_pull_failures` | boolean | Continue if pull fails | false          |
| `services`             | array   | Services to pull       | all services   |
| `project_name`         | string  | Project name override  | directory name |

**Example**:

```bash
docker compose pull
docker compose pull web api
```

**Safety**: Requires confirmation for production environments.

#### images

List images used by services.

| Parameter      | Type   | Description           | Default        |
| -------------- | ------ | --------------------- | -------------- |
| `project_name` | string | Project name override | directory name |

**Example**:

```bash
docker compose images
```

**Output Fields**: CONTAINER, REPOSITORY, TAG, IMAGE ID, SIZE

### Execution (2 tools)

#### exec

Execute a command in a running container.

| Parameter      | Type   | Description           | Required          |
| -------------- | ------ | --------------------- | ----------------- |
| `service`      | string | Service name          | Yes               |
| `command`      | array  | Command to execute    | Yes               |
| `user`         | string | User to execute as    | container default |
| `workdir`      | string | Working directory     | container default |
| `env`          | object | Environment variables | none              |
| `project_name` | string | Project name override | directory name    |

**Example**:

```bash
docker compose exec web bash
docker compose exec -u root api ls -la /app
docker compose exec db psql -U postgres
```

**Safety**:

- Destructive commands (`rm -rf`, `dd`, `mkfs`) are **BLOCKED**
- Root user execution requires confirmation
- Default timeout: 30 seconds

#### run

Run a one-off command in a new container.

| Parameter      | Type    | Description                 | Default           |
| -------------- | ------- | --------------------------- | ----------------- |
| `service`      | string  | Service to run              | Required          |
| `command`      | array   | Command to execute          | service default   |
| `rm`           | boolean | Remove container after run  | true              |
| `no_deps`      | boolean | Don't start linked services | false             |
| `user`         | string  | User to execute as          | container default |
| `env`          | object  | Environment variables       | none              |
| `project_name` | string  | Project name override       | directory name    |

**Example**:

```bash
docker compose run --rm web npm test
docker compose run --no-deps api python manage.py migrate
```

**Safety**: Requires confirmation for commands that modify data.

### Configuration (2 tools)

#### config

Validate and view the Compose file configuration.

| Parameter               | Type    | Description                | Default        |
| ----------------------- | ------- | -------------------------- | -------------- |
| `resolve_image_digests` | boolean | Pin image tags to digests  | false          |
| `no_interpolate`        | boolean | Don't interpolate env vars | false          |
| `project_name`          | string  | Project name override      | directory name |

**Example**:

```bash
docker compose config
docker compose config --resolve-image-digests
```

**Output**: Parsed and merged Compose configuration

#### port

Print the public port binding for a service port.

| Parameter      | Type   | Description           | Required       |
| -------------- | ------ | --------------------- | -------------- |
| `service`      | string | Service name          | Yes            |
| `private_port` | number | Container port        | Yes            |
| `protocol`     | string | Protocol (tcp/udp)    | tcp            |
| `project_name` | string | Project name override | directory name |

**Example**:

```bash
docker compose port web 80
docker compose port db 5432
```

**Output**: `<host>:<port>` binding

## Common Workflows

### Start a Development Environment

```bash
# 1. Validate configuration
docker compose config

# 2. Pull latest images
docker compose pull

# 3. Build custom images
docker compose build

# 4. Start services in detached mode
docker compose up -d

# 5. Check service status
docker compose ps

# 6. View logs
docker compose logs --tail 100
```

### Troubleshoot a Failing Service

```bash
# 1. Check container status
docker compose ps --all

# 2. View service logs
docker compose logs --tail 200 failing-service

# 3. Inspect running processes
docker compose top failing-service

# 4. Check configuration
docker compose config

# 5. Restart the service
docker compose restart failing-service

# 6. If needed, recreate container
docker compose up -d --force-recreate failing-service
```

### Update Service Images

```bash
# 1. Pull latest images
docker compose pull

# 2. Stop services
docker compose down

# 3. Rebuild if using custom Dockerfiles
docker compose build --pull

# 4. Start with new images
docker compose up -d

# 5. Verify services
docker compose ps
```

### Debug Service Connectivity

```bash
# 1. Check running services
docker compose ps

# 2. Inspect port mappings
docker compose port web 80
docker compose port api 3000

# 3. Exec into container
docker compose exec web sh

# 4. Test connectivity (from inside container)
docker compose exec web curl api:3000/health

# 5. Check logs for errors
docker compose logs web api
```

### Clean Up Environment

```bash
# 1. Stop all services
docker compose down

# 2. Remove orphaned containers
docker compose down --remove-orphans

# 3. View images
docker compose images

# 4. Clean up (manual - volume removal BLOCKED)
# Volumes require manual cleanup with explicit confirmation
```

## Configuration

### Environment Variables

| Variable                 | Description                       | Default                        |
| ------------------------ | --------------------------------- | ------------------------------ |
| `COMPOSE_PROJECT_NAME`   | Default project name              | directory name                 |
| `COMPOSE_FILE`           | Compose file path                 | `docker-compose.yml`           |
| `COMPOSE_PATH_SEPARATOR` | Path separator for multiple files | `:` (Linux/Mac), `;` (Windows) |
| `DOCKER_HOST`            | Docker daemon socket              | `unix:///var/run/docker.sock`  |
| `COMPOSE_HTTP_TIMEOUT`   | HTTP timeout for API calls        | 60                             |
| `COMPOSE_PARALLEL_LIMIT` | Max parallel operations           | unlimited                      |

### Setup

1. **Install Docker Engine**:

   ```bash
   # macOS
   brew install --cask docker

   # Linux (Ubuntu/Debian)
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

   # Windows
   # Download Docker Desktop from docker.com
   ```

2. **Verify Docker Compose**:

   ```bash
   # Check Docker version
   docker --version

   # Check Compose version
   docker compose version
   ```

3. **Create docker-compose.yml**:

   ```yaml
   version: '3.8'
   services:
     web:
       build: .
       ports:
         - '8080:80'
     db:
       image: postgres:14
       environment:
         POSTGRES_PASSWORD: example
   ```

4. **Test the skill**:
   ```bash
   docker compose config
   docker compose ps
   ```

## Safety Features

### Blocked Operations

The following operations are **BLOCKED** by default to prevent accidental data loss:

- **Volume removal**: `docker compose down -v` (BLOCKED - requires manual confirmation)
- **Full cleanup**: `docker compose down -v --rmi all` (BLOCKED - extremely destructive)
- **Destructive exec**: `rm -rf`, `dd`, `mkfs`, `sudo rm` inside containers (BLOCKED)
- **Force removal**: `docker compose rm -f` (BLOCKED - use stop then rm)

### Confirmation Required

These operations require explicit confirmation:

- Building with `--no-cache` (resource-intensive)
- Pulling images in production environments
- Starting services with `--force-recreate`
- Executing commands as root user
- Running commands that modify databases
- Stopping services with very short timeouts

### Auto-Terminating Operations

The following operations auto-terminate to prevent resource issues:

- Log following (`--follow`): 60-second timeout
- Service execution (`exec`): 30-second timeout
- One-off commands (`run`): 60-second timeout

## Error Handling

**Common Errors**:

| Error                             | Cause                 | Fix                                             |
| --------------------------------- | --------------------- | ----------------------------------------------- |
| `docker: command not found`       | Docker not installed  | Install Docker Engine                           |
| `Cannot connect to Docker daemon` | Docker not running    | Start Docker service                            |
| `network ... not found`           | Network cleanup issue | Run `docker compose down` then `up`             |
| `port is already allocated`       | Port conflict         | Change port mapping or stop conflicting service |
| `no configuration file provided`  | Missing compose file  | Create `docker-compose.yml`                     |
| `service ... must be built`       | Image not built       | Run `docker compose build`                      |

**Recovery**:

- Validate configuration: `docker compose config`
- Check Docker status: `docker info`
- View service logs: `docker compose logs`
- Force recreate: `docker compose up -d --force-recreate`
- Clean restart: `docker compose down && docker compose up -d`

## Integration with Agents

This skill integrates with the following agents:

### Primary Agents

- **devops**: Local development, CI/CD integration, container orchestration
- **developer**: Application development, testing, debugging

### Secondary Agents

- **qa**: Integration testing, test environment setup
- **incident-responder**: Debugging production issues, service recovery
- **cloud-integrator**: Cloud deployment, migration to Kubernetes
- **performance-engineer**: Performance testing, resource optimization

## Progressive Disclosure

The skill uses progressive disclosure to minimize context usage:

1. **Initial Load**: Only metadata and tool names (~700 tokens)
2. **Tool Invocation**: Specific tool schema loaded on-demand (~100-150 tokens)
3. **Result Streaming**: Large outputs (logs) streamed incrementally
4. **Context Cleanup**: Old results cleared after use

**Context Optimization**:

- Use `--tail` to limit log output
- Use service filters to target specific containers
- Prefer `ps` over `ps --all` for active services only
- Use `--since` for time-bounded log queries

## Troubleshooting

### Skill Issues

**Docker Compose not found**:

```bash
# Check Docker Compose version
docker compose version

# If using V1, try:
docker-compose version

# Update to V2 (recommended)
# Docker Compose V2 is integrated into Docker CLI
```

**Permission denied**:

```bash
# Add user to docker group (Linux)
sudo usermod -aG docker $USER
newgrp docker

# Verify permissions
docker ps
```

**Compose file issues**:

```bash
# Validate syntax
docker compose config

# Check for errors
docker compose config -q

# View resolved configuration
docker compose config --resolve-image-digests
```

**Network issues**:

```bash
# List networks
docker network ls

# Remove unused networks
docker network prune

# Recreate services
docker compose down
docker compose up -d
```

## Performance Considerations

- **Build caching**: Use layer caching for faster builds; avoid `--no-cache` unless necessary
- **Parallel operations**: Docker Compose V2 parallelizes by default; use `COMPOSE_PARALLEL_LIMIT` to control
- **Resource limits**: Define CPU/memory limits in compose file to prevent resource exhaustion
- **Log rotation**: Use logging drivers to prevent disk space issues
- **Volume cleanup**: Regularly clean unused volumes (requires manual confirmation)

## Related

- **Docker Compose Documentation**: https://docs.docker.com/compose/
- **Compose File Reference**: https://docs.docker.com/compose/compose-file/
- **Docker CLI**: https://docs.docker.com/engine/reference/commandline/cli/
- **Kubernetes Migration**: `.claude/skills/kubernetes-flux/` (Kubernetes orchestration)

## Sources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Compose V2](https://github.com/docker/compose)
- [Compose Specification](https://github.com/compose-spec/compose-spec)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

## Related Skills

- [`cloud-devops-expert`](../cloud-devops-expert/SKILL.md) - Cloud platforms (AWS, GCP, Azure) and Terraform infrastructure

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
