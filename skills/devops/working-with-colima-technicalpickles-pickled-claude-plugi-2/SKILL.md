---
name: working-with-colima
description: Use when Docker commands fail with "Cannot connect to Docker daemon", when starting/stopping container environments, or when managing multiple Docker contexts on macOS - provides Colima lifecycle management, profile handling, and troubleshooting
---

# Working with Colima

## Overview

Colima provides container runtimes (Docker, Containerd) on macOS with minimal setup. It runs a Linux VM and exposes Docker via contexts.

**Use this skill when:**
- Docker commands fail ("Cannot connect to Docker daemon")
- Starting/stopping container runtime on macOS
- Managing multiple Docker profiles/contexts
- Troubleshooting container environment issues
- Need SSH agent forwarding for Docker builds

**Not for:** Docker Compose, Kubernetes clusters, or Linux environments.

## Quick Reference

| Operation | Command |
|-----------|---------|
| Start | `colima start` or `colima start <profile>` |
| Start with SSH agent | `colima start <profile> -s` |
| Stop | `colima stop` or `colima stop --force` |
| Status | `colima status -p <profile>` |
| List profiles | `colima list` |
| SSH into VM | `colima ssh` or `colima ssh -- <cmd>` |
| Get socket path | `colima status -p <profile> --json \| jq -r .docker_socket` |

## Docker Context Basics

Colima creates Docker contexts per profile:
- Profile `default` → context `colima`
- Profile `work` → context `colima-work`

```bash
# Switch context (global - affects all terminals)
docker context use colima-work

# Override per-session
export DOCKER_CONTEXT=colima-work

# Override per-command
docker --context colima-work ps
```

For details, see `references/docker-contexts.md`.

## Common Issues

**Docker daemon not connecting?**
1. `colima status` - is it running?
2. `docker context list` - right context selected?
3. See `references/troubleshooting.md` for more

**Need more VM resources?**
```bash
colima stop && colima start --cpu 4 --memory 8
```

**"Broken" status after restart?**
```bash
colima stop --force && colima start
```

## References

- `references/docker-contexts.md` - Context switching, DOCKER_HOST, socket paths
- `references/profile-management.md` - Creating, configuring, deleting profiles
- `references/troubleshooting.md` - Common issues and solutions
- `references/common-options.md` - Flags, VM types, resource configuration

## Upstream Documentation

Local copies of official Colima docs (from [github.com/abiosoft/colima](https://github.com/abiosoft/colima)):

- `references/colima-upstream/README.md` - Official README with features and usage
- `references/colima-upstream/FAQ.md` - Official FAQ and troubleshooting
- `references/colima-upstream/INSTALL.md` - Installation options
