---
name: docker-2025-features
description: Latest Docker 2025 features including AI Assistant, Enhanced Container Isolation, and Moby 25
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Docker 2025 Features

This skill covers the latest Docker features introduced in 2025, ensuring you leverage cutting-edge capabilities for security, performance, and developer experience.

## Docker Engine 28 Features (2025)

### 1. Image Type Mounts

**What it is:**
Mount an image directory structure directly inside a container without extracting to a volume.

**Key capabilities:**
- Mount image layers as read-only filesystems
- Share common data between containers without duplication
- Faster startup for data-heavy containers
- Reduced disk space usage

**How to use:**
```bash
# Mount entire image
docker run --rm \
  --mount type=image,source=mydata:latest,target=/data \
  alpine ls -la /data

# Mount specific path from image
docker run --rm \
  --mount type=image,source=mydata:latest,image-subpath=/config,target=/app/config \
  alpine cat /app/config/settings.json
```

**Use cases:**
- Read-only configuration distribution
- Shared ML model weights across containers
- Static asset serving
- Immutable data sets for testing

### 2. Versioned Debug Endpoints

**What it is:**
Debug endpoints now accessible through standard versioned API paths.

**Previously:** Only available at root paths like `/debug/vars`
**Now:** Also accessible at `/v1.48/debug/vars`, `/v1.48/debug/pprof/*`

**Available endpoints:**
- `/v1.48/debug/vars` - Runtime variables
- `/v1.48/debug/pprof/` - Profiling index
- `/v1.48/debug/pprof/cmdline` - Command line
- `/v1.48/debug/pprof/profile` - CPU profile
- `/v1.48/debug/pprof/trace` - Execution trace
- `/v1.48/debug/pprof/goroutine` - Goroutine stacks

**How to use:**
```bash
# Access debug vars through versioned API
curl --unix-socket /var/run/docker.sock http://localhost/v1.48/debug/vars

# Get CPU profile
curl --unix-socket /var/run/docker.sock http://localhost/v1.48/debug/pprof/profile?seconds=30 > profile.out
```

### 3. Component Updates

**Latest versions in Engine 28.3.3:**
- Buildx v0.26.1 - Enhanced build performance
- Compose v2.40.3 - Latest compose features
- BuildKit v0.25.1 - Security improvements
- Go runtime 1.24.8 - Performance optimizations

### 4. Security Fixes

**CVE-2025-54388:** Fixed firewalld reload issue where published container ports could be accessed from local network even when bound to loopback.

**Impact:** Critical for containers binding to 127.0.0.1 expecting localhost-only access.

### 5. Deprecations

**Raspberry Pi OS 32-bit (armhf):**
- Docker Engine 28 is the last major version supporting armhf
- Starting with Engine 29, no new armhf packages
- Migrate to 64-bit OS or use Engine 28.x LTS

## Docker Desktop 4.47 Features (October 2025)

### 1. MCP Catalog Integration

**What it is:**
Model Context Protocol (MCP) server catalog with 100+ verified, containerized tools.

**Key capabilities:**
- Discover and search MCP servers
- One-click deployment of MCP tools
- Integration with Docker AI and Model Runner
- Centralized management of AI agent tools

**How to access:**
- Docker Hub MCP Catalog
- Docker Desktop MCP Toolkit
- Web: https://www.docker.com/mcp-catalog

**Use cases:**
- AI agent tool discovery
- Workflow automation
- Development environment setup
- CI/CD tool integration

### 2. Model Runner Enhancements

**What's new:**
- Improved UI for model management
- Enhanced inference APIs
- Better inference engine performance
- Model card inspection in Docker Desktop
- `docker model requests` command for monitoring

**How to use:**
```bash
# List running models
docker model ls

# View model details (new: model cards)
docker model inspect llama2-7b

# Monitor requests and responses (NEW)
docker model requests llama2-7b

# Performance metrics
docker stats $(docker model ls -q)
```

### 3. Silent Component Updates

**What it is:**
Docker Desktop automatically updates internal components without requiring full application restart.

**Benefits:**
- Faster security patches
- Less disruption to workflow
- Automatic Compose, BuildKit, Containerd updates
- Background update delivery

**Configuration:**
- Enabled by default
- Can be disabled in Settings > General
- Notifications for major updates only

### 4. CVE Fixes

**CVE-2025-10657 (v4.47):** Fixed Enhanced Container Isolation Docker Socket command restrictions not working in 4.46.0.

**CVE-2025-9074 (v4.46):** Fixed malicious container escape allowing Docker Engine access without mounted socket.

## Docker Desktop 4.38-4.45 Features

### 1. Docker AI Assistant (Project Gordon)

**What it is:**
AI-powered assistant integrated into Docker Desktop and CLI for intelligent container development.

**Key capabilities:**
- Natural language command interface
- Context-aware troubleshooting
- Automated Dockerfile optimization
- Real-time best practice recommendations
- Intelligent error diagnosis

**How to use:**
```bash
# Enable in Docker Desktop Settings > Features > Docker AI (Beta)

# Ask questions in natural language
"Optimize my Python Dockerfile"
"Why is my container restarting?"
"Suggest secure nginx configuration"
```

**Local Model Runner:**
- Runs AI models directly on your machine (llama.cpp)
- No cloud API dependencies
- Privacy-preserving (data stays local)
- GPU acceleration for performance
- Works offline

### 2. Enhanced Container Isolation (ECI)

**What it is:**
Additional security layer that restricts Docker socket access and container escape vectors.

**Security benefits:**
- Prevents unauthorized Docker socket access
- Restricts container capabilities by default
- Blocks common escape techniques
- Enforces stricter resource boundaries
- Audits container operations

**How to enable:**
```bash
# Docker Desktop Settings > Security > Enhanced Container Isolation
# Or via CLI:
docker desktop settings set enhancedContainerIsolation=true
```

**Use cases:**
- Multi-tenant environments
- Security-critical applications
- Compliance requirements (PCI-DSS, HIPAA)
- Zero-trust architectures
- Development environments with untrusted code

**Compatibility:**
- May break containers requiring Docker socket access
- Requires Docker Desktop 4.38+
- Supported on Windows (WSL2), macOS, Linux Desktop

### 3. Model Runner

**What it is:**
Built-in AI model execution engine allowing developers to run large language models locally.

**Features:**
- Run AI models without cloud services
- Optimal GPU acceleration
- Privacy-preserving inference
- Multiple model format support
- Integration with Docker AI

**How to use:**
```bash
# Install via Docker Desktop Extensions
# Or use CLI:
docker model run llama2-7b

# View running models:
docker model ls

# Stop model:
docker model stop MODEL_ID
```

**Benefits:**
- No API costs
- Complete data privacy
- Offline availability
- Faster inference (local GPU)
- Integration with development workflow

### 4. Multi-Node Kubernetes Testing

**What it is:**
Test Kubernetes deployments with multi-node clusters directly in Docker Desktop.

**Previously:** Single-node only
**Now:** 2-5 node clusters for realistic testing

**How to enable:**
```bash
# Docker Desktop Settings > Kubernetes > Enable multi-node
# Specify node count (2-5)
```

**Use cases:**
- Test pod scheduling across nodes
- Validate affinity/anti-affinity rules
- Test network policies
- Simulate node failures
- Validate StatefulSets and DaemonSets

### 5. Bake (General Availability)

**What it is:**
High-level build orchestration tool for complex multi-target builds.

**Previously:** Experimental
**Now:** Generally available and production-ready

**Features:**
```hcl
# docker-bake.hcl
target "app" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
  cache-from = ["type=registry,ref=myapp:cache"]
  cache-to = ["type=registry,ref=myapp:cache,mode=max"]
}

target "test" {
  inherits = ["app"]
  target = "test"
  output = ["type=local,dest=./coverage"]
}
```

```bash
# Build all targets
docker buildx bake

# Build specific target
docker buildx bake test
```

## Moby 25 Engine Updates

### Performance Improvements

**1. Faster Container Startup:**
- 20-30% faster cold starts
- Improved layer extraction
- Optimized network initialization

**2. Better Resource Management:**
- More accurate memory accounting
- Improved CPU throttling
- Better cgroup v2 support

**3. Storage Driver Enhancements:**
- overlay2 performance improvements
- Better disk space management
- Faster image pulls

### Security Updates

**1. Enhanced Seccomp Profiles:**
```json
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_AARCH64"],
  "syscalls": [
    {
      "names": ["read", "write", "exit"],
      "action": "SCMP_ACT_ALLOW"
    }
  ]
}
```

**2. Improved AppArmor Integration:**
- Better Docker profile generation
- Reduced false positives
- Enhanced logging

**3. User Namespace Improvements:**
- Easier configuration
- Better compatibility
- Performance optimizations

## Docker Compose v2.40.3+ Features (2025)

### Compose Bridge (Convert to Kubernetes)

**What it is:**
Convert local compose.yaml files to Kubernetes manifests in a single command.

**Key capabilities:**
- Automatic conversion of Compose services to Kubernetes Deployments
- Service-to-Service mapping
- Volume conversion to PersistentVolumeClaims
- ConfigMap and Secret generation
- Ingress configuration

**How to use:**
```bash
# Convert compose file to Kubernetes manifests
docker compose convert --format kubernetes > k8s-manifests.yaml

# Or use compose-bridge directly
docker compose-bridge convert docker-compose.yml

# Apply to Kubernetes cluster
kubectl apply -f k8s-manifests.yaml
```

**Example conversion:**
```yaml
# docker-compose.yml
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - data:/usr/share/nginx/html

volumes:
  data:

# Converts to Kubernetes:
# - Deployment for 'web' service
# - Service exposing port 80
# - PersistentVolumeClaim for 'data'
```

**Use cases:**
- Local development to Kubernetes migration
- Testing Kubernetes deployments locally
- CI/CD pipeline conversion
- Multi-environment deployment strategies

### Breaking Changes

**1. Version Field Obsolete:**
```yaml
# OLD (deprecated):
version: '3.8'
services:
  app:
    image: nginx

# NEW (2025):
services:
  app:
    image: nginx
```

The `version` field is now ignored and can be omitted.

### New Features

**1. Develop Watch with initial_sync:**
```yaml
services:
  app:
    build: .
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
          initial_sync: full  # NEW: Sync all files on start
```

**2. Volume Type: Image:**
```yaml
services:
  app:
    volumes:
      - type: image
        source: mydata:latest
        target: /data
        read_only: true
```

**3. Build Print:**
```bash
# Debug complex build configurations
docker compose build --print > build-config.json
```

**4. Config No-Env-Resolution:**
```bash
# View raw config without environment variable substitution
docker compose config --no-env-resolution
```

**5. Watch with Prune:**
```bash
# Automatically prune unused resources during watch
docker compose watch --prune
```

**6. Run with Quiet:**
```bash
# Reduce output noise
docker compose run --quiet app npm test
```

## BuildKit Updates (2025)

### New Features

**1. Git SHA-256 Support:**
```dockerfile
# Use SHA-256 based repositories
ADD https://github.com/user/repo#sha256:abc123... /src
```

**2. Enhanced COPY/ADD --exclude:**
```dockerfile
# Now generally available (was labs-only)
COPY --exclude=*.test.js --exclude=*.md . /app
```

**3. ADD --unpack with --chown:**
```dockerfile
# Extract and set ownership in one step
ADD --unpack=true --chown=appuser:appgroup archive.tar.gz /app
```

**4. Git Query Parameters:**
```dockerfile
# Fine-grained Git clone control
ADD https://github.com/user/repo.git?depth=1&branch=main /src
```

**5. Image Checksum Verification:**
```dockerfile
# Verify image integrity
FROM alpine:3.19@sha256:abc123...
# BuildKit verifies checksum automatically
```

### Security Enhancements

**1. Improved Frontend Verification:**
```dockerfile
# Always use official Docker frontends
# syntax=docker/dockerfile:1

# Pin with digest for maximum security
# syntax=docker/dockerfile:1@sha256:ac85f380a63b13dfcefa89046420e1781752bab202122f8f50032edf31be0021
```

**2. Remote Cache Improvements:**
- Fixed concurrency issues
- Better loop handling
- Enhanced security

## Best Practices for 2025 Features

### Using Docker AI Effectively

**DO:**
- Provide specific context in queries
- Verify AI-generated configurations
- Combine with traditional security tools
- Use for learning and exploration

**DON'T:**
- Trust AI blindly for security-critical apps
- Skip manual code review
- Ignore security scan results
- Use in air-gapped environments without Model Runner

### Enhanced Container Isolation

**DO:**
- Enable for security-sensitive workloads
- Test containers for compatibility first
- Document socket access requirements
- Use with least privilege principles

**DON'T:**
- Enable without testing existing containers
- Disable without understanding risks
- Grant socket access unnecessarily
- Ignore audit logs

### Modern Compose Files

**DO:**
- Remove version field from new compose files
- Use new features (volume type: image, watch improvements)
- Leverage --print for debugging
- Adopt --quiet for cleaner CI/CD output

**DON'T:**
- Keep version field (it's ignored anyway)
- Rely on deprecated syntax
- Skip testing with Compose v2.40+
- Use outdated documentation

## Migration Guide

### Updating to Docker Desktop 4.38+

**1. Backup existing configurations:**
```bash
# Export current settings
docker context export desktop-linux > backup.tar
```

**2. Update Docker Desktop:**
- Download latest from docker.com
- Run installer
- Restart machine if required

**3. Enable new features:**
```bash
# Enable AI Assistant (beta)
docker desktop settings set enableAI=true

# Enable Enhanced Container Isolation
docker desktop settings set enhancedContainerIsolation=true
```

**4. Test existing containers:**
```bash
# Verify containers work with ECI
docker compose up -d
docker compose ps
docker compose logs
```

### Updating Compose Files

**Before:**
```yaml
version: '3.8'

services:
  app:
    image: nginx:latest
    volumes:
      - data:/data

volumes:
  data:
```

**After:**
```yaml
services:
  app:
    image: nginx:1.26.0  # Specific version
    volumes:
      - data:/data
    develop:
      watch:
        - action: sync
          path: ./config
          target: /etc/nginx/conf.d
          initial_sync: full

volumes:
  data:
    driver: local
```

## Troubleshooting 2025 Features

### Docker AI Issues

**Problem:** AI Assistant not responding
**Solution:**
```bash
# Check Docker Desktop version
docker version

# Ensure beta features enabled
docker desktop settings get enableAI

# Restart Docker Desktop
```

**Problem:** Model Runner slow
**Solution:**
- Update GPU drivers
- Increase Docker Desktop memory (Settings > Resources)
- Close other GPU-intensive applications
- Use smaller models for faster inference

### Enhanced Container Isolation Issues

**Problem:** Container fails with socket permission error
**Solution:**
```bash
# Identify socket dependencies
docker inspect CONTAINER | grep -i socket

# If truly needed, add socket access explicitly
# (Document why in docker-compose.yml comments)
docker run -v /var/run/docker.sock:/var/run/docker.sock ...
```

**Problem:** ECI breaks CI/CD pipeline
**Solution:**
- Disable ECI temporarily: `docker desktop settings set enhancedContainerIsolation=false`
- Review which containers need socket access
- Refactor to eliminate socket dependencies
- Re-enable ECI with exceptions documented

### Compose v2.40 Issues

**Problem:** "version field is obsolete" warning
**Solution:**
```yaml
# Simply remove the version field
# OLD:
version: '3.8'
services: ...

# NEW:
services: ...
```

**Problem:** watch with initial_sync fails
**Solution:**
```bash
# Check file permissions
ls -la ./src

# Ensure paths are correct
docker compose config | grep -A 5 watch

# Verify sync target exists in container
docker compose exec app ls -la /app/src
```

## Recommended Feature Adoption Timeline

**Immediate (Production-Ready):**
- Bake for complex builds
- Compose v2.40 features (remove version field)
- Moby 25 engine (via regular Docker updates)
- BuildKit improvements (automatic)

**Testing (Beta but Stable):**
- Docker AI for development workflows
- Model Runner for local AI testing
- Multi-node Kubernetes for pre-production

**Evaluation (Security-Critical):**
- Enhanced Container Isolation (test thoroughly)
- ECI with existing production containers
- Socket access elimination strategies

This skill ensures you stay current with Docker's 2025 evolution while maintaining stability, security, and production-readiness.
