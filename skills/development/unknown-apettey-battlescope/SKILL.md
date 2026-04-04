# Claude Skill: Docker Registry Management for BattleScope

**Purpose**: Guide all Docker image building, tagging, versioning, and registry management for BattleScope services.

---

## Core Principles

### 1. Image Naming Convention

**Rule**: All BattleScope images MUST follow this naming pattern:

```
<registry>/<organization>/<service>:<version>-<architecture>
```

**Examples**:
```
docker.io/battlescope/ingestion-service:v3.0.0-amd64
docker.io/battlescope/enrichment-service:v3.0.0-arm64
docker.io/battlescope/battle-service:v3.1.2-amd64
```

**Components**:
- **Registry**: `docker.io` (Docker Hub - public registry)
- **Organization**: `battlescope`
- **Service**: Service name in kebab-case
- **Version**: Semantic versioning (v3.x.x for V3 architecture)
- **Architecture**: `amd64` or `arm64` (multi-arch support)

---

## 2. Versioning Strategy

### Semantic Versioning

**Format**: `vMAJOR.MINOR.PATCH`

**V3 Architecture**:
- **Major Version**: `v3` (V3 architecture)
- **Minor Version**: Feature additions, non-breaking changes
- **Patch Version**: Bug fixes, minor updates

**Examples**:
```
v3.0.0 - Initial V3 release
v3.0.1 - Bug fix in ingestion service
v3.1.0 - Added historical ingestion feature
v3.2.0 - Added data retention policy
```

### Image Tags

**Required Tags for Each Image**:
1. **Specific Version**: `v3.0.0-amd64`
2. **Major.Minor**: `v3.0-amd64`
3. **Major**: `v3-amd64`
4. **Latest**: `latest-amd64` (ONLY for latest stable release)

**Multi-Arch Manifest Tags**:
1. **Specific Version**: `v3.0.0` (manifest pointing to all archs)
2. **Major.Minor**: `v3.0`
3. **Major**: `v3`
4. **Latest**: `latest`

**Example Push Sequence**:
```bash
# Build for amd64
docker build --platform linux/amd64 -t battlescope/ingestion-service:v3.0.0-amd64 .
docker tag battlescope/ingestion-service:v3.0.0-amd64 battlescope/ingestion-service:v3.0-amd64
docker tag battlescope/ingestion-service:v3.0.0-amd64 battlescope/ingestion-service:v3-amd64
docker tag battlescope/ingestion-service:v3.0.0-amd64 battlescope/ingestion-service:latest-amd64

# Build for arm64
docker build --platform linux/arm64 -t battlescope/ingestion-service:v3.0.0-arm64 .
docker tag battlescope/ingestion-service:v3.0.0-arm64 battlescope/ingestion-service:v3.0-arm64
docker tag battlescope/ingestion-service:v3.0.0-arm64 battlescope/ingestion-service:v3-arm64
docker tag battlescope/ingestion-service:v3.0.0-arm64 battlescope/ingestion-service:latest-arm64

# Push all tags
docker push battlescope/ingestion-service:v3.0.0-amd64
docker push battlescope/ingestion-service:v3.0-amd64
docker push battlescope/ingestion-service:v3-amd64
docker push battlescope/ingestion-service:latest-amd64
docker push battlescope/ingestion-service:v3.0.0-arm64
docker push battlescope/ingestion-service:v3.0-arm64
docker push battlescope/ingestion-service:v3-arm64
docker push battlescope/ingestion-service:latest-arm64

# Create and push multi-arch manifest
docker manifest create battlescope/ingestion-service:v3.0.0 \
  battlescope/ingestion-service:v3.0.0-amd64 \
  battlescope/ingestion-service:v3.0.0-arm64
docker manifest push battlescope/ingestion-service:v3.0.0

docker manifest create battlescope/ingestion-service:v3.0 \
  battlescope/ingestion-service:v3.0-amd64 \
  battlescope/ingestion-service:v3.0-arm64
docker manifest push battlescope/ingestion-service:v3.0

docker manifest create battlescope/ingestion-service:v3 \
  battlescope/ingestion-service:v3-amd64 \
  battlescope/ingestion-service:v3-arm64
docker manifest push battlescope/ingestion-service:v3

docker manifest create battlescope/ingestion-service:latest \
  battlescope/ingestion-service:latest-amd64 \
  battlescope/ingestion-service:latest-arm64
docker manifest push battlescope/ingestion-service:latest
```

---

## 3. BattleScope V3 Services

### Service Image Names

| Service | Image Name | Description |
|---------|-----------|-------------|
| **Ingestion** | `battlescope/ingestion-service` | Raw killmail acquisition |
| **Enrichment** | `battlescope/enrichment-service` | Killmail augmentation |
| **Battle** | `battlescope/battle-service` | Battle clustering |
| **Search** | `battlescope/search-service` | Full-text search |
| **Notification** | `battlescope/notification-service` | Real-time notifications |
| **Frontend BFF** | `battlescope/frontend-bff` | Backend-for-Frontend |
| **Frontend** | `battlescope/frontend` | Web UI |

### Infrastructure Images (if custom)

| Component | Image Name | Description |
|-----------|-----------|-------------|
| **Database Migrator** | `battlescope/db-migrator` | Database migrations |
| **Init Container** | `battlescope/init` | Initialization tasks |

---

## 4. Never Overwrite Production Tags

**CRITICAL RULE**: NEVER overwrite existing production image tags.

**Why**:
- Running pods may pull "updated" image causing inconsistency
- Rollbacks become impossible
- Audit trail is lost
- Violates immutability principle

**Correct Approach**:
```bash
# ❌ WRONG - Overwriting existing tag
docker build -t battlescope/ingestion-service:v3.0.0 .
docker push battlescope/ingestion-service:v3.0.0  # Overwrites existing v3.0.0!

# ✅ CORRECT - Create new version
docker build -t battlescope/ingestion-service:v3.0.1 .
docker push battlescope/ingestion-service:v3.0.1  # New tag, doesn't overwrite
```

**Exception**: `latest` tag can be updated (but use with caution in production)

---

## 5. Image Documentation

### Docker Hub Repository Settings

**For Each Service Repository**:

1. **Description** (Short):
   ```
   BattleScope V3 - <Service Name> - <One-line description>
   ```

2. **Full Description** (README.md):
   ```markdown
   # BattleScope <Service Name>

   **Architecture**: V3 Distributed Microservices
   **Version**: v3.x.x

   ## Overview

   <Service description from service specification>

   ## Supported Tags

   - `v3.0.0`, `v3.0`, `v3`, `latest` - Multi-arch manifest
   - `v3.0.0-amd64`, `v3.0-amd64`, `v3-amd64`, `latest-amd64` - AMD64/x86_64
   - `v3.0.0-arm64`, `v3.0-arm64`, `v3-arm64`, `latest-arm64` - ARM64

   ## Quick Start

   ```bash
   docker pull battlescope/<service-name>:v3
   docker run -p <port>:<port> battlescope/<service-name>:v3
   ```

   ## Environment Variables

   | Variable | Description | Default |
   |----------|-------------|---------|
   | `PORT` | Service port | `3000` |
   | `KAFKA_BROKERS` | Kafka connection string | `localhost:9092` |
   | `DATABASE_URL` | PostgreSQL connection string | Required |

   ## Health Check

   ```bash
   curl http://localhost:<port>/health
   ```

   ## Documentation

   - [Architecture](https://github.com/battlescope/battle-monitor/tree/main/docs/architecture-v3)
   - [Service Specification](https://github.com/battlescope/battle-monitor/blob/main/proposal/implementation-v1/services/<service>.md)

   ## License

   MIT
   ```

3. **Enable Auto-Build**: If using GitHub integration
4. **Visibility**: Public (for all BattleScope images)

---

## 6. Build Scripts

### Makefile Integration

```makefile
# Docker build variables
DOCKER_REGISTRY ?= docker.io
DOCKER_ORG ?= battlescope
VERSION ?= v3.0.0
PLATFORMS ?= linux/amd64,linux/arm64

# Service-specific variables
SERVICE_NAME := ingestion-service
IMAGE_NAME := $(DOCKER_REGISTRY)/$(DOCKER_ORG)/$(SERVICE_NAME)

# Build commands
.PHONY: docker-build docker-push docker-build-push docker-manifest

## Build Docker image for current platform
docker-build:
	@echo "Building $(IMAGE_NAME):$(VERSION) for current platform..."
	docker build -t $(IMAGE_NAME):$(VERSION) .

## Build multi-arch Docker images
docker-build-multi:
	@echo "Building $(IMAGE_NAME):$(VERSION) for $(PLATFORMS)..."
	docker buildx build \
		--platform $(PLATFORMS) \
		-t $(IMAGE_NAME):$(VERSION) \
		-t $(IMAGE_NAME):$(shell echo $(VERSION) | cut -d. -f1-2) \
		-t $(IMAGE_NAME):$(shell echo $(VERSION) | cut -d. -f1) \
		-t $(IMAGE_NAME):latest \
		.

## Push Docker image
docker-push:
	@echo "Pushing $(IMAGE_NAME):$(VERSION)..."
	docker push $(IMAGE_NAME):$(VERSION)
	docker push $(IMAGE_NAME):$(shell echo $(VERSION) | cut -d. -f1-2)
	docker push $(IMAGE_NAME):$(shell echo $(VERSION) | cut -d. -f1)
	docker push $(IMAGE_NAME):latest

## Build and push (convenience command)
docker-build-push: docker-build docker-push

## Build multi-arch and push
docker-build-push-multi:
	@echo "Building and pushing $(IMAGE_NAME):$(VERSION) for $(PLATFORMS)..."
	docker buildx build \
		--platform $(PLATFORMS) \
		--push \
		-t $(IMAGE_NAME):$(VERSION) \
		-t $(IMAGE_NAME):$(shell echo $(VERSION) | cut -d. -f1-2) \
		-t $(IMAGE_NAME):$(shell echo $(VERSION) | cut -d. -f1) \
		-t $(IMAGE_NAME):latest \
		.
```

---

## 7. GitHub Actions CI/CD

### Automated Image Building

```yaml
# .github/workflows/docker-build.yml
name: Build and Push Docker Images

on:
  push:
    branches:
      - main
    tags:
      - 'v*.*.*'

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
          - ingestion-service
          - enrichment-service
          - battle-service
          - search-service
          - notification-service
          - frontend-bff
          - frontend

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract version from tag
        id: version
        run: |
          if [[ "${{ github.ref }}" =~ ^refs/tags/v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "VERSION=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
          else
            echo "VERSION=v3.0.0-dev-$(git rev-parse --short HEAD)" >> $GITHUB_OUTPUT
          fi

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: ./services/${{ matrix.service }}
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            battlescope/${{ matrix.service }}:${{ steps.version.outputs.VERSION }}
            battlescope/${{ matrix.service }}:latest
          cache-from: type=registry,ref=battlescope/${{ matrix.service }}:buildcache
          cache-to: type=registry,ref=battlescope/${{ matrix.service }}:buildcache,mode=max
```

---

## 8. Image Security and Scanning

### Best Practices

1. **Base Images**:
   ```dockerfile
   # Use official Node.js LTS with Alpine for smaller size
   FROM node:20-alpine AS base
   ```

2. **Non-Root User**:
   ```dockerfile
   # Create non-root user
   RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
   USER nodejs
   ```

3. **Multi-Stage Builds**:
   ```dockerfile
   FROM node:20-alpine AS builder
   # Build stage

   FROM node:20-alpine AS runner
   # Runtime stage (smaller final image)
   ```

4. **Security Scanning**:
   ```bash
   # Scan images before pushing
   docker scan battlescope/ingestion-service:v3.0.0
   ```

---

## 9. Registry Cleanup Policy

### Retention Rules

**Keep**:
- All major versions (v3.x.x, v4.x.x, etc.)
- Last 10 minor versions of current major
- Last 5 patch versions of current minor
- `latest` tag

**Delete**:
- Dev/test tags older than 30 days
- Untagged images (dangling)
- Superseded patch versions (keep last 5 only)

### Cleanup Script

```bash
#!/bin/bash
# cleanup-old-images.sh

REGISTRY="docker.io"
ORG="battlescope"
SERVICE="$1"

# List all tags
TAGS=$(curl -s "https://hub.docker.com/v2/repositories/${ORG}/${SERVICE}/tags/?page_size=100" | jq -r '.results[].name')

# Delete dev tags older than 30 days
for TAG in $TAGS; do
  if [[ "$TAG" =~ -dev- ]]; then
    # Check age and delete if > 30 days
    echo "Considering $TAG for deletion..."
  fi
done
```

---

## 10. Kubernetes Image References

### Pod Spec Image Reference

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ingestion-service
spec:
  template:
    spec:
      containers:
        - name: ingestion-service
          # ✅ CORRECT - Use specific version tag
          image: battlescope/ingestion-service:v3.0.0
          imagePullPolicy: IfNotPresent

          # ❌ WRONG - Using 'latest' in production
          # image: battlescope/ingestion-service:latest
          # imagePullPolicy: Always
```

**Image Pull Policy**:
- `IfNotPresent` - Pull only if not cached (recommended for versioned tags)
- `Always` - Always pull (use for `latest` tag only, not recommended for production)
- `Never` - Never pull (use for local development only)

---

## 11. Image Registry Credentials

### Docker Hub Authentication

**Local Development**:
```bash
docker login docker.io
# Enter username and password
```

**Kubernetes Secret**:
```bash
kubectl create secret docker-registry docker-hub-creds \
  --docker-server=docker.io \
  --docker-username=<username> \
  --docker-password=<password> \
  --docker-email=<email> \
  --namespace=battlescope
```

**Pod Spec**:
```yaml
spec:
  imagePullSecrets:
    - name: docker-hub-creds
```

---

## 12. Troubleshooting

### Common Issues

**Issue**: Image not found
```bash
Error: Failed to pull image "battlescope/ingestion-service:v3.0.0": rpc error: code = NotFound
```

**Solution**:
```bash
# Verify image exists
docker pull battlescope/ingestion-service:v3.0.0

# Check tag exists on Docker Hub
curl https://hub.docker.com/v2/repositories/battlescope/ingestion-service/tags | jq '.results[].name'
```

**Issue**: Architecture mismatch
```bash
WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)
```

**Solution**:
```bash
# Pull multi-arch manifest (not architecture-specific tag)
docker pull battlescope/ingestion-service:v3.0.0  # Multi-arch manifest
# NOT: battlescope/ingestion-service:v3.0.0-amd64
```

---

## Summary Checklist

Before pushing any image:

- [ ] Image follows naming convention: `battlescope/<service>:v3.x.x`
- [ ] Version tag is unique (not overwriting existing tag)
- [ ] Multi-arch build (amd64 + arm64)
- [ ] All required tags created (version, major.minor, major, latest)
- [ ] Docker Hub repository has proper description
- [ ] Image scanned for vulnerabilities
- [ ] Kubernetes manifests updated with new version
- [ ] CHANGELOG updated with new version

---

**Remember**: Images are immutable. Never overwrite an existing production tag!
