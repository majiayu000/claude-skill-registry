---
name: gitlab-ci-best-practices
description: Use when optimizing GitLab CI/CD pipelines for performance, reliability, or maintainability. Covers pipeline optimization and organizational patterns.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# GitLab CI - Best Practices

Optimize GitLab CI/CD pipelines for performance, reliability, and maintainability.

## Pipeline Optimization

### Use DAG with Needs

```yaml
stages:
  - build
  - test
  - deploy

build:frontend:
  stage: build
  script: npm run build:frontend

build:backend:
  stage: build
  script: npm run build:backend

test:frontend:
  stage: test
  needs: ["build:frontend"]
  script: npm run test:frontend

test:backend:
  stage: test
  needs: ["build:backend"]
  script: npm run test:backend

deploy:
  stage: deploy
  needs: ["test:frontend", "test:backend"]
  script: ./deploy.sh
```

### Parallel Execution

```yaml
test:
  parallel:
    matrix:
      - SUITE: [unit, integration, e2e]
  script:
    - npm run test:$SUITE
```

### Interruptible Jobs

```yaml
test:
  interruptible: true
  script:
    - npm test

deploy:production:
  interruptible: false  # Never cancel
  script:
    - ./deploy.sh
```

## Configuration Organization

### Split Configuration Files

```yaml
# .gitlab-ci.yml
include:
  - local: .gitlab/ci/build.yml
  - local: .gitlab/ci/test.yml
  - local: .gitlab/ci/deploy.yml

stages:
  - build
  - test
  - deploy
```

### Reusable Templates

```yaml
.node_template: &node_template
  image: node:20-alpine
  before_script:
    - npm ci
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

test:unit:
  <<: *node_template
  script:
    - npm run test:unit

test:lint:
  <<: *node_template
  script:
    - npm run lint
```

### Extends Keyword

```yaml
.base_job:
  image: node:20-alpine
  before_script:
    - npm ci

test:
  extends: .base_job
  script:
    - npm test

build:
  extends: .base_job
  script:
    - npm run build
```

## Resource Management

### Resource Groups

```yaml
deploy:staging:
  resource_group: staging
  script:
    - ./deploy.sh staging

deploy:production:
  resource_group: production
  script:
    - ./deploy.sh production
```

### Runner Tags

```yaml
heavy_build:
  tags:
    - high-memory
    - docker
  script:
    - ./build.sh
```

## Error Handling

### Retry Configuration

```yaml
test:flaky:
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
      - script_failure
```

### Allow Failure

```yaml
test:experimental:
  allow_failure: true
  script:
    - npm run test:experimental

test:experimental:soft:
  allow_failure:
    exit_codes: [42]  # Only allow specific exit code
```

## Security Best Practices

### Protected Pipelines

```yaml
deploy:production:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
  environment:
    name: production
```

### Secure Variables

```yaml
# Use protected and masked variables
deploy:
  script:
    - echo "$API_KEY"  # Masked in logs
  rules:
    - if: $CI_COMMIT_REF_PROTECTED == "true"
```

## Monitoring & Debugging

### Job Logging

```yaml
test:
  script:
    - set -x  # Enable debug output
    - npm test
  after_script:
    - echo "Job status: $CI_JOB_STATUS"
```

### Pipeline Badges

```markdown
[![Pipeline](https://gitlab.com/group/project/badges/main/pipeline.svg)](https://gitlab.com/group/project/-/pipelines)
[![Coverage](https://gitlab.com/group/project/badges/main/coverage.svg)](https://gitlab.com/group/project/-/pipelines)
```

## Common Anti-Patterns

1. **Avoid**: Running all jobs in sequence
   **Do**: Use `needs` for parallel execution

2. **Avoid**: Downloading all artifacts
   **Do**: Use `dependencies` to limit downloads

3. **Avoid**: Rebuilding node_modules every job
   **Do**: Use cache with lock file keys

4. **Avoid**: Hardcoded secrets
   **Do**: Use CI/CD variables with protection

5. **Avoid**: Single monolithic `.gitlab-ci.yml`
   **Do**: Split into multiple included files
