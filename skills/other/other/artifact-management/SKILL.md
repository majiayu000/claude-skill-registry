---
name: artifact-management
description: Manage build artifacts, Docker images, and package registries. Configure artifact repositories, versioning, and distribution strategies.
---

# Artifact Management

## Overview

Implement comprehensive artifact management strategies for storing, versioning, and distributing built binaries, Docker images, and packages across environments.

## When to Use

- Docker image registry management
- Package publication and versioning
- Build artifact storage and retrieval
- Container image optimization
- Artifact retention policies
- Multi-registry distribution
- Dependency caching

## Implementation Examples

### 1. **Docker Registry Configuration**

```dockerfile
# Dockerfile with multi-stage build for optimization
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY package*.json ./

EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node healthcheck.js

CMD ["node", "dist/server.js"]

LABEL org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.description="Production application" \
      org.opencontainers.image.authors="DevOps Team"
```

### 2. **GitHub Container Registry (GHCR) Push**

```yaml
# .github/workflows/publish-image.yml
name: Publish to GHCR

on:
  push:
    tags: ['v*']
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Log in to registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.prod
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache
          cache-to: type=registry,ref=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:buildcache,mode=max
```

### 3. **npm Package Publishing**

```json
{
  "name": "@myorg/awesome-library",
  "version": "1.2.3",
  "description": "Awesome library for developers",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ],
  "publishConfig": {
    "registry": "https://npm.pkg.github.com",
    "access": "public"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/myorg/awesome-library.git"
  },
  "scripts": {
    "prepublishOnly": "npm run build && npm run test",
    "prepack": "npm run build"
  }
}
```

### 4. **Artifact Retention Policy**

```yaml
# .github/workflows/cleanup-artifacts.yml
name: Cleanup Old Artifacts

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Delete artifacts older than 30 days
        uses: geekyeggo/delete-artifact@v2
        with:
          name: '*'
          minCreatedTime: 30d
          failOnError: false
```

### 5. **Artifact Versioning**

```bash
#!/bin/bash
# artifact-version.sh

BUILD_DATE=$(date -u +'%Y%m%d')
GIT_HASH=$(git rev-parse --short HEAD)
VERSION=$(grep '"version"' package.json | sed 's/.*"version": "\([^"]*\)".*/\1/')

# Full version tag
FULL_VERSION="${VERSION}-${BUILD_DATE}.${GIT_HASH}"

# Create artifact with version
docker build -t myapp:${FULL_VERSION} .
docker tag myapp:${FULL_VERSION} myapp:latest

echo "Built artifact version: ${FULL_VERSION}"
```

### 10. **GitLab Package Registry**

```yaml
# .gitlab-ci.yml
publish-package:
  stage: publish
  script:
    - npm config set @myorg:registry https://gitlab.example.com/api/v4/packages/npm/
    - npm config set '//gitlab.example.com/api/v4/packages/npm/:_authToken' "${CI_JOB_TOKEN}"
    - npm publish
  only:
    - tags
```

## Best Practices

### ✅ DO
- Use semantic versioning for artifacts
- Implement image scanning before deployment
- Set retention policies for old artifacts
- Use multi-stage builds for Docker images
- Sign and verify artifacts
- Implement artifact immutability
- Document artifact metadata
- Use specific base image versions
- Implement vulnerability scanning
- Cache layers aggressively
- Tag images with commit SHA
- Compress artifacts for storage

### ❌ DON'T
- Use `latest` tag as sole identifier
- Store secrets in artifacts
- Push artifacts without scanning
- Use untrusted base images
- Skip artifact verification
- Overwrite published artifacts
- Mix binary and source artifacts
- Ignore image layer optimization
- Store build logs with sensitive data

## Artifact Storage Standards

```bash
# Naming convention
{registry}/{org}/{repo}/{service}:{version}-{build}-{commit}

# Examples
docker.io/myorg/web-app:1.2.3-123-abc1234
ghcr.io/myorg/api-service:2.0.0-456-def5678
artifactory.example.com/releases/core:3.1.0-789-ghi9012
```

## Resources

- [Docker Registry API](https://docs.docker.com/registry/spec/api/)
- [npm Registry](https://docs.npmjs.com/cli/v8/using-npm/registry)
- [GitHub Artifact Management](https://docs.github.com/en/actions/managing-workflow-runs/removing-workflow-artifacts)
- [Artifactory Documentation](https://jfrog.com/help/artifactory/)
