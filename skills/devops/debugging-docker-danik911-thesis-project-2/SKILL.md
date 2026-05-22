---
name: debugging-docker
description: Debugs Docker build failures, container runtime errors, platform architecture issues (ARM64/AMD64/WSL2), AWS ECR/ECS pull failures, and optimizes Docker workflows. Use when encountering Docker build errors, container crashes, ECR authentication issues, ECS deployment problems, performance issues, networking failures, volume permission errors, or when working with multi-platform Docker images.
---

# Debugging Docker Operations

## Overview

Systematic troubleshooting workflows for Docker build failures, runtime errors, AWS container services, platform-specific issues, and performance optimization. Designed for multi-platform environments (ARM64/AMD64/WSL2) with pharmaceutical compliance contexts requiring GAMP-5 validation.

## When to Use

- **Build Failures**: Package installation errors, COPY failures, layer caching issues
- **Runtime Errors**: Container crashes, exit codes, DNS resolution, port conflicts
- **AWS Container Services**: ECR authentication, ECS pull failures, rate limiting
- **Platform Issues**: ARM64 vs AMD64 emulation, WSL2 integration, cross-platform builds
- **Performance Problems**: Slow builds, large images, QEMU emulation overhead
- **Volumes/Networking**: Permission errors, mount failures, port binding

---

## Available Tools

### Standard Tools
| Tool | Purpose |
|------|---------|
| Bash | Execute Docker commands, view logs |
| Read | Examine Dockerfiles, compose files |
| Grep | Search for patterns in logs |
| Glob | Find Docker-related files |

### AWS MCP Tools
| Tool | Purpose |
|------|---------|
| `mcp__aws-api-mcp__call_aws` | Execute AWS CLI for ECR/ECS operations |
| `mcp__aws-knowledge-mcp__aws___search_documentation` | Search AWS docs for container guidance |
| `mcp__aws-ccapi-mcp__list_resources` | List ECS tasks, ECR repositories |

---

## Core Workflow

### Phase 1: Symptom Diagnosis

**Objective**: Identify problem category and gather diagnostic information

1. **Identify Problem Type**
   ```bash
   # For build failures
   docker build 2>&1 | tee build.log

   # For runtime errors
   docker logs <container-name>
   docker inspect <container-name>

   # For AWS issues
   aws ecr describe-repositories
   aws ecs describe-tasks --cluster <cluster> --tasks <task-arn>
   ```

2. **Categorize the Issue**
   - Build Failure (exit during `docker build`)
   - Runtime Error (container exits or crashes)
   - AWS ECR/ECS Issue (authentication, pull failures)
   - Platform/Architecture Issue (ARM64/AMD64 mismatch)
   - Performance Problem (slow or inefficient)
   - Networking/Volume Issue

3. **Collect Context**
   ```bash
   docker version && docker info | head -30
   uname -m  # Platform: x86_64 or aarch64
   ```

**Quality Gate**: Problem type identified, initial logs collected

---

### Phase 2: Root Cause Analysis

#### Build Failures

**Common Patterns:**
```bash
# Check build log for specific failures
grep -E "ERROR|failed|error:" build.log

# Common patterns:
# "COPY failed" → File not in build context
# "returned a non-zero code" → Command failed
# "no matching manifest" → Platform mismatch
```

**Key Checks:**
- Build context: `ls -la <path-to-file>`
- .dockerignore: `cat .dockerignore`
- Layer caching: `docker build --no-cache`

See `reference/common-errors.md` for complete error matrix.

#### Runtime Errors

**Exit Code Quick Reference:**

| Code | Meaning | Common Cause |
|------|---------|--------------|
| 0 | Normal exit | Application completed |
| 1 | Application error | Check application logs |
| 126 | Cannot execute | Permission issue |
| 127 | Command not found | Wrong CMD/ENTRYPOINT |
| 137 | OOM killed | Memory limit exceeded |
| 139 | Segfault | Application crash |
| 143 | SIGTERM | Graceful shutdown |

**Diagnosis:**
```bash
docker inspect <container> | jq '.[0].State'
docker logs --tail 100 <container>
```

#### AWS ECR/ECS Issues

**ECR Authentication:**
```
Error: "no basic auth credentials"
```
- **Cause**: ECR login token expired (12-hour validity)
- **Fix**:
  ```bash
  aws ecr get-login-password --region eu-west-2 | \
    docker login --username AWS --password-stdin \
    <account-id>.dkr.ecr.eu-west-2.amazonaws.com
  ```

**ECS Pull Failures:**
```
Error: "CannotPullContainerError"
```
- **Checklist**:
  1. Task execution role has ECR permissions
  2. VPC has NAT Gateway (for private subnets)
  3. Image tag exists in ECR

**Using AWS MCP:**
```
# Check ECR images
mcp__aws-api-mcp__call_aws: aws ecr describe-images --repository-name <repo>

# Check ECS task failures
mcp__aws-api-mcp__call_aws: aws ecs describe-tasks --cluster <cluster> --tasks <task-arn>
```

See `reference/aws-ecr-ecs.md` for complete AWS troubleshooting guide.

#### Platform/Architecture Issues

**Slow Build Detection:**
```bash
# Check if emulation is active (ARM64 host building AMD64)
docker run --rm --platform=linux/amd64 alpine uname -m
# If output shows x86_64 on ARM64 host → emulation active (slow)
```

**Solutions:**
1. Use native platform for development
2. Build target platform only for deployment
3. Use multi-stage with `${BUILDPLATFORM}`

See `reference/platform-guide.md` for complete platform guidance.

**Quality Gate**: Root cause identified, specific error patterns documented

---

### Phase 3: Solution & Validation

#### Build Failure Fixes

```dockerfile
# Fix missing file in context
# Verify path exists: ls -la <path>
COPY main.py /app/

# Fix package installation with retry
RUN pip install --no-cache-dir -r requirements.txt || \
    (pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt)

# Fix platform issues
# docker build --platform=linux/amd64 -t image:prod .
```

#### Runtime Error Fixes

```bash
# Fix permission issues
docker run --user $(id -u):$(id -g) image:tag

# Fix OOM (Exit 137)
docker run -m 2g --memory-swap 2g image:tag

# Fix port conflicts
docker run -p 8081:8080 image:tag  # Change host port
```

#### AWS Fixes

```bash
# Refresh ECR credentials
aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin <account>.dkr.ecr.eu-west-2.amazonaws.com

# Fix Docker Hub rate limiting - use ECR Public
# FROM public.ecr.aws/docker/library/python:3.12-slim
```

#### Validation

```bash
# Rebuild with verbose output
docker build --progress=plain -f Dockerfile -t image:test .

# Test container startup
docker run --rm image:test

# Verify functionality
docker run -it image:test /bin/sh -c "command-to-test"
```

**Quality Gate**: Fix applied, container builds and runs without errors

---

## Quick Reference Table

| Problem | Quick Check | Common Fix |
|---------|-------------|------------|
| ECR "no basic auth" | Token age (12hr) | `aws ecr get-login-password \| docker login` |
| ECS CannotPull | Task role, NAT | Check IAM + VPC config |
| Docker Hub rate limit | Error message | Use ECR Public or authenticate |
| Build fails at COPY | `ls -la <file>` | Fix path or add to build context |
| Package install fails | Check network | Update pip, verify package name |
| Exit 137 (OOM) | `docker inspect` OOMKilled | Increase memory limit (-m flag) |
| Exit 127 | Command not found | Fix CMD/ENTRYPOINT path |
| Slow ARM64 build | `--platform` flag | Use native ARM64 for dev |
| WSL2 vmmem bloat | Task Manager | `.wslconfig` memory limits |
| Volume mount not working | Check compose mounts | `docker-compose down && up -d` |
| Port already in use | `docker ps` | Change host port or stop conflict |
| Permission denied | Check USER in Dockerfile | Add USER directive, fix volume perms |

---

## Best Practices

### Build Optimization
- **Layer ordering**: Dependencies before code (cache efficiency)
- **Multi-stage builds**: Separate build and runtime environments
- **Use .dockerignore**: Exclude `node_modules`, `.git`, `__pycache__`

### Security
```dockerfile
# Non-root user
RUN adduser -D appuser
USER appuser

# Never COPY secrets - use --secret flag
```

### Platform Handling
```bash
# Development (native platform - fast)
docker build -t image:dev .

# Production (target platform)
docker build --platform=linux/amd64 -t image:prod .

# Multi-platform with cache
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --cache-from type=registry,ref=<repo>:cache \
  --cache-to type=registry,ref=<repo>:cache \
  -t image:multi --push .
```

### WSL2 Performance
- Store projects in WSL2 filesystem (`~/`), NOT Windows mount (`/mnt/c/`)
- Configure `.wslconfig` with memory limits
- Use `wsl --shutdown` to reclaim memory

See `reference/wsl2-optimization.md` for complete WSL2 guide.

---

## Common Pitfalls

### Don't: Use relative paths without verification
```dockerfile
# WRONG - may fail if context is incorrect
COPY ../app/file.py /app/

# RIGHT - relative to build context root
COPY app/file.py /app/
```

### Do: Use explicit platform for production
```bash
# WRONG - platform inferred (may differ from prod)
docker build -t api:latest .

# RIGHT - explicit platform
docker build --platform=linux/amd64 -t api:latest .
```

### Do: Verify volume mounts work
```bash
# Check if container sees host files
docker exec <container> ls -la /app/

# Recreate containers after mount changes
docker-compose down && docker-compose up -d
```

---

## Quality Checklist

- [ ] Problem type identified (build/runtime/AWS/platform/network/volume)
- [ ] Diagnostic logs collected and analyzed
- [ ] Root cause determined with specific error patterns
- [ ] Solution applied with appropriate fix
- [ ] Build succeeds without errors
- [ ] Container starts and runs successfully
- [ ] Functionality validated
- [ ] Platform architecture verified (matches deployment target)
- [ ] Security checked (non-root user, no exposed secrets)

---

## Detailed References

- **Docker Commands**: `reference/docker-commands.md`
- **Common Error Matrix**: `reference/common-errors.md` (20+ error patterns)
- **AWS ECR/ECS Guide**: `reference/aws-ecr-ecs.md`
- **Platform Guide**: `reference/platform-guide.md` (ARM64/AMD64/WSL2, buildx caching)
- **WSL2 Optimization**: `reference/wsl2-optimization.md`
- **Build Optimization**: `reference/build-optimization.md`
- **Security Hardening**: `reference/security-hardening.md`

## Diagnostic Scripts

- **Build Failure Analysis**: `scripts/analyze-build-failure.sh <log-file>`
- **Container Inspection**: `scripts/inspect-container.sh <container-name>`
- **Platform Check**: `scripts/check-platform.sh`

---

**Remember**: Docker issues are systematic and diagnosable. Follow the three-phase workflow (Symptom → Root Cause → Solution), use AWS MCP tools for ECR/ECS issues, and reference the detailed guides for complex scenarios. Always validate fixes before considering the issue resolved.
