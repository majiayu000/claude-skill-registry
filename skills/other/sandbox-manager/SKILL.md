---
name: Sandbox Manager
description: Quick sandbox environment provisioning, status checking, teardown, and reset for Ignition gateway development sandboxes. Use when the user wants to create, check, reset, or tear down sandbox environments. Requires Docker and Docker Compose installed.
allowed-tools: Read, Write, Bash, Glob, Grep
license: MIT
---

# Sandbox Manager

Manage Docker-based Ignition gateway sandbox environments for isolated development and testing. Each sandbox is a self-contained environment with its own Ignition gateway instance.

## When to Use

Trigger this skill when the user:
- Asks about sandbox environments or containers
- Wants to create, check, reset, or tear down development environments
- Needs to see sandbox logs or health status
- References "sandbox", "environment", "container", or "gateway instance"

## Operations

All operations use the sandbox manager script:

```bash
python .claude/skills/sandbox-manager/sandbox_manager.py <operation> [name] [options]
```

### Available Operations

| Operation | Command | Description |
|-----------|---------|-------------|
| **list** | `python .claude/skills/sandbox-manager/sandbox_manager.py list` | Show all sandboxes and their status |
| **create** | `python .claude/skills/sandbox-manager/sandbox_manager.py create <name>` | Provision a new sandbox |
| **status** | `python .claude/skills/sandbox-manager/sandbox_manager.py status <name>` | Check container health and gateway status |
| **reset** | `python .claude/skills/sandbox-manager/sandbox_manager.py reset <name>` | Stop, remove, and recreate sandbox |
| **teardown** | `python .claude/skills/sandbox-manager/sandbox_manager.py teardown <name>` | Remove sandbox and cleanup volumes |
| **logs** | `python .claude/skills/sandbox-manager/sandbox_manager.py logs <name>` | Tail sandbox container logs |

### Create Options

| Option | Default | Description |
|--------|---------|-------------|
| `--port` | 8088 | Gateway web port |
| `--version` | 8.1.43 | Ignition version tag |
| `--edition` | standard | Ignition edition (standard/edge) |

## Usage Examples

```bash
# List all sandboxes
python .claude/skills/sandbox-manager/sandbox_manager.py list

# Create a new sandbox for testing
python .claude/skills/sandbox-manager/sandbox_manager.py create my-test --port 9088

# Check if gateway is healthy
python .claude/skills/sandbox-manager/sandbox_manager.py status my-test

# View recent logs
python .claude/skills/sandbox-manager/sandbox_manager.py logs my-test

# Reset a broken sandbox
python .claude/skills/sandbox-manager/sandbox_manager.py reset my-test

# Clean up when done
python .claude/skills/sandbox-manager/sandbox_manager.py teardown my-test
```

## Sandbox Directory Structure

Sandboxes are stored at the project root in `sandboxes/`:

```
sandboxes/
  my-test/
    docker-compose.yml
  another-env/
    docker-compose.yml
```

## Prerequisites

- Docker Desktop or Docker Engine running
- Docker Compose v2+
- Python 3.7+

## Troubleshooting

### Docker Not Running
If operations fail with connection errors, ensure Docker Desktop is running.

### Port Conflicts
If create fails with port binding errors, use `--port` to specify an alternative port.

### Gateway Not Starting
Check logs with the `logs` operation. Common issues:
- EULA not accepted (handled automatically by the template)
- Insufficient memory (Ignition needs at least 1GB)
- Port already in use