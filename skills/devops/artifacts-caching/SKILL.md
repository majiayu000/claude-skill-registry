---
name: gitlab-ci-artifacts-caching
description: Use when configuring artifacts for inter-job data passing or caching for faster builds. Covers cache strategies and artifact management.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# GitLab CI - Artifacts & Caching

Configure artifacts and caching for efficient pipeline execution.

## Artifacts

### Basic Artifact Configuration

```yaml
build:
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week
```

### Artifact Reports

```yaml
test:
  script:
    - npm test -- --coverage
  artifacts:
    reports:
      junit: junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
```

### Conditional Artifacts

```yaml
build:
  artifacts:
    paths:
      - dist/
    when: on_success  # on_success, on_failure, always
    exclude:
      - dist/**/*.map
```

### Artifact Dependencies

```yaml
build:
  artifacts:
    paths:
      - dist/

test:
  dependencies:
    - build  # Downloads build artifacts
  script:
    - npm test

deploy:
  dependencies: []  # Skip all artifact downloads
  script:
    - ./deploy.sh
```

## Caching

### Basic Cache Configuration

```yaml
default:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
      - .npm/
```

### Cache Key Strategies

```yaml
# Per-branch cache
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - node_modules/

# Lock file based cache
cache:
  key:
    files:
      - package-lock.json
  paths:
    - node_modules/

# Combined key
cache:
  key:
    prefix: ${CI_JOB_NAME}
    files:
      - package-lock.json
  paths:
    - node_modules/
```

### Cache Policy

```yaml
install:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: push  # Only upload cache
  script:
    - npm ci

test:
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/
    policy: pull  # Only download cache
  script:
    - npm test
```

### Fallback Keys

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  fallback_keys:
    - ${CI_DEFAULT_BRANCH}
    - main
  paths:
    - node_modules/
```

## Distributed Cache (S3)

Configure in GitLab Runner:

```toml
[runners.cache]
  Type = "s3"
  Shared = true
  [runners.cache.s3]
    ServerAddress = "s3.amazonaws.com"
    BucketName = "gitlab-runner-cache"
    BucketLocation = "us-east-1"
```

## Artifacts vs Cache

| Feature | Artifacts | Cache |
|---------|-----------|-------|
| Purpose | Pass data between jobs | Speed up job execution |
| Storage | GitLab server | Runner local or S3 |
| Reliability | Guaranteed | Best effort |
| Expiration | Configurable | Configurable |
| Cross-pipeline | Yes (with dependencies) | Yes (with keys) |

## Best Practices

1. Use cache for dependencies (node_modules, vendor)
2. Use artifacts for build outputs
3. Set appropriate expiration times
4. Use lock file-based cache keys
5. Exclude source maps and unnecessary files
6. Use `policy: pull` for jobs that only read cache
