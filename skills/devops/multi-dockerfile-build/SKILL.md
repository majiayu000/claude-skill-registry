---
name: multi-dockerfile-build
description: This skill should be used when the user asks to "build multiple Dockerfiles",
  "compile varios dockerfiles", "multi-container build", "multiple Docker images in GitLab",
  "parallel Docker builds", "monorepo Docker builds", "build frontend backend worker containers",
  or needs to build multiple Docker images from different Dockerfiles in a single GitLab project
  using To-Be-Continuous Docker template.
version: 1.0.0
---

# Multi-Dockerfile Build with To-Be-Continuous

Knowledge base for building multiple Docker images from different Dockerfiles in a single GitLab project using the To-Be-Continuous Docker template.

## Overview

When a project contains multiple Dockerfiles (e.g., frontend, backend, worker), the TBC Docker template supports multi-instantiation to build all images in parallel using Kaniko, Buildah, or Docker-in-Docker.

## Solution: Multi-Instantiation with parallel:matrix

The recommended approach is to use GitLab CI's `parallel:matrix` feature to instantiate the Docker template multiple times with different configurations.

### Basic Structure

```yaml
include:
  - component: $CI_SERVER_FQDN/to-be-continuous/docker/gitlab-ci-docker@6
    inputs:
      build-tool: kaniko

# Multi-instantiate the Docker template
.docker-base:
  parallel:
    matrix:
      # Configuration for each Dockerfile
      - DOCKER_FILE: path/to/Dockerfile1
        DOCKER_CONTEXT_PATH: path/to/context1
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/service1:$CI_COMMIT_REF_SLUG
        DOCKER_RELEASE_IMAGE: $CI_REGISTRY_IMAGE/service1:$CI_COMMIT_REF_NAME

      - DOCKER_FILE: path/to/Dockerfile2
        DOCKER_CONTEXT_PATH: path/to/context2
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/service2:$CI_COMMIT_REF_SLUG
        DOCKER_RELEASE_IMAGE: $CI_REGISTRY_IMAGE/service2:$CI_COMMIT_REF_NAME
```

## Required Variables per Dockerfile

For each matrix entry, configure:

| Variable | Description | Example |
|----------|-------------|---------|
| `DOCKER_FILE` | Path to Dockerfile | `frontend/Dockerfile` |
| `DOCKER_CONTEXT_PATH` | Build context directory | `frontend` |
| `DOCKER_SNAPSHOT_IMAGE` | Snapshot image name/tag | `$CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_SLUG` |
| `DOCKER_RELEASE_IMAGE` | Release image name/tag | `$CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_NAME` |

## Optional Variables per Dockerfile

| Variable | Description | Example |
|----------|-------------|---------|
| `DOCKER_BUILD_ARGS` | Build arguments | `--build-arg NODE_ENV=production` |
| `DOCKER_METADATA` | Custom labels | `--label version=1.0` |
| `DOCKER_BUILD_CACHE_DISABLED` | Disable cache | `true` |

## Complete Example: 3-Service Architecture

```yaml
include:
  - component: $CI_SERVER_FQDN/to-be-continuous/docker/gitlab-ci-docker@6
    inputs:
      build-tool: kaniko
      trivy-disabled: false
      hadolint-disabled: false
      sbom-disabled: false

.docker-base:
  parallel:
    matrix:
      # Frontend service
      - DOCKER_FILE: frontend/Dockerfile
        DOCKER_CONTEXT_PATH: frontend
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_SLUG
        DOCKER_RELEASE_IMAGE: $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_NAME
        DOCKER_BUILD_ARGS: "--build-arg NODE_ENV=production --build-arg API_URL=$API_URL"

      # Backend API service
      - DOCKER_FILE: backend/Dockerfile
        DOCKER_CONTEXT_PATH: backend
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_REF_SLUG
        DOCKER_RELEASE_IMAGE: $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_REF_NAME
        DOCKER_BUILD_ARGS: "--build-arg DATABASE_URL=$DATABASE_URL"

      # Worker service
      - DOCKER_FILE: worker/Dockerfile
        DOCKER_CONTEXT_PATH: worker
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/worker:$CI_COMMIT_REF_SLUG
        DOCKER_RELEASE_IMAGE: $CI_REGISTRY_IMAGE/worker:$CI_COMMIT_REF_NAME
        DOCKER_BUILD_ARGS: "--build-arg QUEUE_URL=$QUEUE_URL"
```

## Project Structure

```
project/
├── .gitlab-ci.yml          # Configuration with parallel:matrix
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
└── worker/
    ├── Dockerfile
    └── tasks/
```

## How It Works

### 1. Job Multiplication

When using `parallel:matrix`, **all TBC Docker jobs are multiplied** for each matrix entry:

- `docker-hadolint` (Dockerfile linting)
- `docker-kaniko-build` (or buildah/dind)
- `docker-trivy` (security scanning)
- `docker-sbom` (bill of materials)
- `docker-healthcheck` (health verification)
- `docker-publish` (release publishing)

### 2. Parallel Execution

All builds run **in parallel** if GitLab runners are available, significantly reducing total pipeline time.

### 3. Cache Strategy

Each image has its own cache location:
- Kaniko: `${DOCKER_SNAPSHOT_IMAGE%:*}/cache`
- Stored in: `$CI_PROJECT_DIR/.cache`

### 4. Artifact Outputs

Each build generates separate dotenv artifacts:
- `docker.env` with variables:
  - `docker_image`
  - `docker_image_digest`
  - `docker_repository`
  - `docker_tag`
  - `docker_digest`

## Alternative: Individual Job Definitions

For cases requiring more control, define separate jobs:

```yaml
include:
  - component: $CI_SERVER_FQDN/to-be-continuous/docker/gitlab-ci-docker@6

# Disable default jobs
docker-kaniko-build:
  rules:
    - when: never

# Frontend build
docker-kaniko-build:frontend:
  extends: .docker-kaniko-base
  stage: package-build
  variables:
    DOCKER_FILE: frontend/Dockerfile
    DOCKER_CONTEXT_PATH: frontend
    DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_SLUG
  script:
    - run_build_kaniko "$DOCKER_SNAPSHOT_IMAGE" --digest-file .img-digest-frontend.txt

# Backend build
docker-kaniko-build:backend:
  extends: .docker-kaniko-base
  stage: package-build
  variables:
    DOCKER_FILE: backend/Dockerfile
    DOCKER_CONTEXT_PATH: backend
    DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_REF_SLUG
  script:
    - run_build_kaniko "$DOCKER_SNAPSHOT_IMAGE" --digest-file .img-digest-backend.txt
```

## Build Tool Compatibility

All three build tools support multi-instantiation:

| Tool | Performance | Use Case |
|------|-------------|----------|
| **kaniko** | Fast, optimized cache | Recommended default |
| **buildah** | Rootless, secure | Security-focused |
| **dind** | Full Docker API | Complex requirements |

## Security Scanning per Image

With `parallel:matrix`, each image gets:
- **Hadolint** scan (Dockerfile best practices)
- **Trivy** scan (vulnerability detection)
- **SBOM** generation (dependency tracking)

Disable per-build if needed:

```yaml
.docker-base:
  parallel:
    matrix:
      - DOCKER_FILE: frontend/Dockerfile
        DOCKER_TRIVY_DISABLED: "true"  # Skip Trivy for this image
      - DOCKER_FILE: backend/Dockerfile
        DOCKER_HADOLINT_DISABLED: "true"  # Skip Hadolint for this image
```

## Advanced: Shared Dependencies

For images sharing base layers or dependencies:

```yaml
.docker-base:
  parallel:
    matrix:
      # Base image (built first)
      - DOCKER_FILE: base/Dockerfile
        DOCKER_CONTEXT_PATH: base
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/base:$CI_COMMIT_REF_SLUG
        DOCKER_BUILD_ARGS: "--cache-from $CI_REGISTRY_IMAGE/base:latest"

      # Derived images (use base as cache)
      - DOCKER_FILE: frontend/Dockerfile
        DOCKER_CONTEXT_PATH: frontend
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_SLUG
        DOCKER_BUILD_ARGS: "--cache-from $CI_REGISTRY_IMAGE/base:$CI_COMMIT_REF_SLUG"
```

## Publishing Strategy

Configure per-image publishing:

```yaml
.docker-base:
  parallel:
    matrix:
      # Auto-publish frontend
      - DOCKER_FILE: frontend/Dockerfile
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_REF_SLUG
        DOCKER_PROD_PUBLISH_STRATEGY: auto

      # Manual publish backend
      - DOCKER_FILE: backend/Dockerfile
        DOCKER_SNAPSHOT_IMAGE: $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_REF_SLUG
        DOCKER_PROD_PUBLISH_STRATEGY: manual
```

## Key Benefits

1. **Parallelization**: All builds execute concurrently
2. **Code Reuse**: Single template, multiple configurations
3. **Consistency**: Same build process for all images
4. **Security**: Automated scanning per image
5. **Maintainability**: Centralized configuration

## Limitations

### Variables Only

The `parallel:matrix` syntax **requires variables**, not component inputs:

```yaml
# WRONG - component inputs don't work with matrix
.docker-base:
  parallel:
    matrix:
      - inputs:
          file: frontend/Dockerfile  # NOT SUPPORTED

# CORRECT - use variables
.docker-base:
  parallel:
    matrix:
      - DOCKER_FILE: frontend/Dockerfile  # SUPPORTED
```

### No Dynamic Context Path

If `DOCKER_CONTEXT_PATH` is not set, it defaults to the Dockerfile directory:

```yaml
# These are equivalent:
- DOCKER_FILE: frontend/Dockerfile
  DOCKER_CONTEXT_PATH: frontend

- DOCKER_FILE: frontend/Dockerfile
  # DOCKER_CONTEXT_PATH auto-detected as "frontend"
```

## Troubleshooting

### Build Order Dependencies

Matrix jobs run in parallel. For build dependencies:

```yaml
# Option 1: Use needs with artifacts
docker-kaniko-build:
  parallel:
    matrix:
      - DOCKER_FILE: base/Dockerfile
        JOB_ORDER: "1"
      - DOCKER_FILE: app/Dockerfile
        JOB_ORDER: "2"

docker-kaniko-build:app:
  needs:
    - docker-kaniko-build: [base]
```

### Cache Conflicts

Each image should have unique cache locations:

```yaml
.docker-base:
  parallel:
    matrix:
      - DOCKER_FILE: service1/Dockerfile
        KANIKO_SNAPSHOT_IMAGE_CACHE: $CI_REGISTRY_IMAGE/service1/cache
      - DOCKER_FILE: service2/Dockerfile
        KANIKO_SNAPSHOT_IMAGE_CACHE: $CI_REGISTRY_IMAGE/service2/cache
```

## Reference Documentation

- TBC Docker Template: `docs/to-be-continuous-knowledge/templates/docker/`
- Multi-instantiation: TBC usage.md section "Multiple template instantiation"
- Parallel matrix: GitLab CI parallel:matrix documentation

## Related Skills

- **component-research**: Evaluate if Docker template fits the use case
- **building-with-tbc**: General TBC pipeline generation
- **template-discovery**: Find available TBC templates