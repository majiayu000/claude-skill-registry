---
name: gitlab-ci-job-configuration
description: Use when defining GitLab CI jobs, configuring scripts, setting up environments, or managing job dependencies. Covers job structure and execution options.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# GitLab CI - Job Configuration

Configure GitLab CI jobs with proper scripts, environments, and execution settings.

## Basic Job Structure

```yaml
job_name:
  stage: test
  image: node:20-alpine
  before_script:
    - npm ci
  script:
    - npm test
  after_script:
    - echo "Cleanup tasks"
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

## Script Configuration

### Multi-Line Scripts

```yaml
build:
  script:
    - echo "Building application..."
    - npm run build
    - echo "Build complete"
```

### Script with Exit Codes

```yaml
test:
  script:
    - npm test || exit 1
    - npm run lint
  allow_failure: false
```

## Environment Configuration

```yaml
deploy:production:
  stage: deploy
  script:
    - ./deploy.sh
  environment:
    name: production
    url: https://example.com
    on_stop: stop:production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual

stop:production:
  stage: deploy
  script:
    - ./teardown.sh
  environment:
    name: production
    action: stop
  when: manual
```

## Job Rules

### Conditional Execution

```yaml
job:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: always
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: on_success
    - when: never
```

### Changes-Based Rules

```yaml
test:frontend:
  rules:
    - changes:
        - "src/frontend/**/*"
        - "package.json"
```

### Exists-Based Rules

```yaml
docker:build:
  rules:
    - exists:
        - Dockerfile
```

## Job Dependencies

### Using Dependencies

```yaml
build:
  stage: build
  script: npm run build
  artifacts:
    paths:
      - dist/

test:
  stage: test
  dependencies:
    - build
  script: npm test
```

### Using Needs (DAG)

```yaml
test:unit:
  needs:
    - job: build
      artifacts: true
  script: npm run test:unit
```

## Parallel Jobs

### Matrix Jobs

```yaml
test:
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "22"]
        OS: ["alpine", "bullseye"]
  image: node:${NODE_VERSION}-${OS}
  script: npm test
```

### Simple Parallel

```yaml
test:
  parallel: 5
  script: npm run test:shard
```

## Resource Configuration

```yaml
heavy_job:
  tags:
    - high-memory
  resource_group: deploy
  timeout: 2h
  retry:
    max: 2
    when:
      - runner_system_failure
      - stuck_or_timeout_failure
```
