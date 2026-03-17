---
name: harness-ci
description: Harness CI (Continuous Integration) for container-native builds, test intelligence, caching, parallelization, and build infrastructure management. Activate for build pipelines, CI steps, test automation, artifact publishing, and build optimization.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
  - WebSearch
dependencies:
  - harness-mcp
  - harness-cd
triggers:
  - harness ci
  - harness build
  - build pipeline
  - ci pipeline
  - test intelligence
  - harness test
  - build and push
  - container build
  - ci/cd build
  - harness cache
  - build optimization
  - harness cloud
  - ci infrastructure
---

# Harness CI Skill

Comprehensive Harness CI (Continuous Integration) for container-native builds with test intelligence, caching, and build infrastructure management.

## When to Use This Skill

Activate this skill when:
- Creating or managing Harness CI pipelines
- Configuring build steps (Run, RunTests, BuildAndPush)
- Setting up test intelligence for faster test execution
- Configuring caching strategies (S3, GCS)
- Managing build infrastructure (Kubernetes, Harness Cloud, VMs)
- Parallelizing builds with matrix strategies
- Publishing artifacts and container images
- Integrating with code repositories
- Troubleshooting build failures

## Build Infrastructure Types

### Harness Cloud (Recommended)

Zero-configuration hosted build infrastructure:

```yaml
infrastructure:
  type: Cloud
  spec:
    os: Linux  # Linux, MacOS, or Windows
```

**Benefits:**
- No setup required
- Auto-scaling
- Pre-installed tools
- Managed updates

### Kubernetes Infrastructure

Self-hosted on your K8s cluster:

```yaml
infrastructure:
  type: KubernetesDirect
  spec:
    connectorRef: k8s_connector
    namespace: harness-builds
    automountServiceAccountToken: true
    nodeSelector:
      kubernetes.io/os: linux
    tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "ci"
        effect: "NoSchedule"
    harnessImageConnectorRef: docker_connector
    os: Linux
```

### VM Infrastructure

AWS, Azure, or GCP VMs:

```yaml
infrastructure:
  type: VM
  spec:
    type: Pool
    spec:
      poolName: linux-pool
      os: Linux
```

## CI Pipeline Structure

### Basic Pipeline

```yaml
pipeline:
  name: Build Pipeline
  identifier: build_pipeline
  projectIdentifier: my_project
  orgIdentifier: default
  properties:
    ci:
      codebase:
        connectorRef: harness_code
        repoName: my-service
        build: <+input>
  stages:
    - stage:
        name: Build and Test
        identifier: build_test
        type: CI
        spec:
          cloneCodebase: true
          infrastructure:
            type: Cloud
            spec:
              os: Linux
          execution:
            steps:
              - step:
                  name: Install Dependencies
                  identifier: install
                  type: Run
                  spec:
                    shell: Sh
                    command: npm ci
              - step:
                  name: Run Tests
                  identifier: test
                  type: Run
                  spec:
                    shell: Sh
                    command: npm test -- --coverage
                    reports:
                      type: JUnit
                      spec:
                        paths:
                          - "junit.xml"
              - step:
                  name: Build
                  identifier: build
                  type: Run
                  spec:
                    shell: Sh
                    command: npm run build
```

## Step Types

### Run Step

Execute shell commands:

```yaml
- step:
    name: Run Script
    identifier: run_script
    type: Run
    spec:
      connectorRef: docker_connector  # Optional for Harness Cloud
      image: node:18-alpine           # Optional for Harness Cloud
      shell: Sh  # Sh, Bash, Powershell, Pwsh, Python
      command: |
        echo "Building application"
        npm ci
        npm run build
      envVariables:
        NODE_ENV: production
        API_URL: https://api.company.com
      outputVariables:
        - name: BUILD_VERSION
      reports:
        type: JUnit
        spec:
          paths:
            - "**/test-results/*.xml"
      resources:
        limits:
          memory: 2Gi
          cpu: "1"
```

### Run Tests Step (Test Intelligence)

Run tests with intelligent test selection:

```yaml
- step:
    name: Run Tests with TI
    identifier: run_tests_ti
    type: RunTests
    spec:
      connectorRef: docker_connector
      image: maven:3.8-openjdk-17
      language: Java  # Java, Kotlin, Scala, CSharp, Python, Ruby
      buildTool: Maven  # Maven, Gradle, Bazel, SBT, Nunit, Pytest, Unittest, Rspec
      args: test
      packages: com.myapp
      runOnlySelectedTests: true  # Enable Test Intelligence
      testAnnotations: org.junit.Test
      preCommand: |
        echo "Setting up test environment"
      postCommand: |
        echo "Test cleanup"
      reports:
        type: JUnit
        spec:
          paths:
            - "**/surefire-reports/*.xml"
      enableTestSplitting: true  # For parallel execution
```

### Build and Push Docker

Build and push container images:

```yaml
- step:
    name: Build and Push
    identifier: build_push
    type: BuildAndPushDockerRegistry
    spec:
      connectorRef: docker_connector
      repo: myorg/myapp
      tags:
        - <+pipeline.sequenceId>
        - <+codebase.shortCommitSha>
        - latest
      dockerfile: Dockerfile
      context: .
      optimize: true  # Harness build optimization
      caching: true   # Layer caching
      buildArgs:
        VERSION: <+pipeline.sequenceId>
        BUILD_DATE: <+pipeline.startTs>
      labels:
        maintainer: team@company.com
        commit: <+codebase.commitSha>
      target: production  # Multi-stage target
      remoteCacheRepo: myorg/myapp-cache  # Remote cache
```

### Build and Push to ECR

```yaml
- step:
    name: Build and Push ECR
    identifier: build_push_ecr
    type: BuildAndPushECR
    spec:
      connectorRef: aws_connector
      region: us-east-1
      account: "123456789012"
      imageName: myapp
      tags:
        - <+pipeline.sequenceId>
      dockerfile: Dockerfile
      caching: true
```

### Build and Push to GCR

```yaml
- step:
    name: Build and Push GCR
    identifier: build_push_gcr
    type: BuildAndPushGCR
    spec:
      connectorRef: gcp_connector
      host: gcr.io
      projectID: my-gcp-project
      imageName: myapp
      tags:
        - <+pipeline.sequenceId>
      dockerfile: Dockerfile
      caching: true
```

### Build and Push to ACR

```yaml
- step:
    name: Build and Push ACR
    identifier: build_push_acr
    type: BuildAndPushACR
    spec:
      connectorRef: azure_connector
      repository: myacr.azurecr.io/myapp
      tags:
        - <+pipeline.sequenceId>
      dockerfile: Dockerfile
      caching: true
```

## Caching Strategies

### S3 Cache

```yaml
# Save cache
- step:
    name: Save Cache
    identifier: save_cache
    type: SaveCacheS3
    spec:
      connectorRef: aws_connector
      region: us-east-1
      bucket: harness-cache
      key: node-modules-{{ checksum "package-lock.json" }}
      sourcePaths:
        - node_modules
      archiveFormat: Tar

# Restore cache
- step:
    name: Restore Cache
    identifier: restore_cache
    type: RestoreCacheS3
    spec:
      connectorRef: aws_connector
      region: us-east-1
      bucket: harness-cache
      key: node-modules-{{ checksum "package-lock.json" }}
      archiveFormat: Tar
      failIfKeyNotFound: false
```

### GCS Cache

```yaml
# Save cache
- step:
    name: Save Cache
    identifier: save_cache
    type: SaveCacheGCS
    spec:
      connectorRef: gcp_connector
      bucket: harness-cache
      key: maven-{{ checksum "pom.xml" }}
      sourcePaths:
        - ~/.m2/repository
      archiveFormat: Tar

# Restore cache
- step:
    name: Restore Cache
    identifier: restore_cache
    type: RestoreCacheGCS
    spec:
      connectorRef: gcp_connector
      bucket: harness-cache
      key: maven-{{ checksum "pom.xml" }}
      archiveFormat: Tar
      failIfKeyNotFound: false
```

### Harness Cache Intelligence

```yaml
# Automatic caching based on build tool detection
- step:
    name: Build with Cache
    identifier: build
    type: Run
    spec:
      shell: Sh
      command: |
        npm ci
        npm run build
      caching:
        enabled: true
        key: npm-<+codebase.branch>
        paths:
          - node_modules
```

## Parallelism and Matrix

### Matrix Strategy

Run steps with multiple configurations:

```yaml
- step:
    name: Test Matrix
    identifier: test_matrix
    type: Run
    spec:
      shell: Sh
      command: |
        echo "Testing on Node $NODE_VERSION with $DB_TYPE"
        npm test
      envVariables:
        NODE_VERSION: <+matrix.nodeVersion>
        DB_TYPE: <+matrix.database>
    strategy:
      matrix:
        nodeVersion:
          - "16"
          - "18"
          - "20"
        database:
          - postgres
          - mysql
        exclude:
          - nodeVersion: "16"
            database: mysql
      maxConcurrency: 4
```

### Parallelism

Run same step multiple times in parallel:

```yaml
- step:
    name: Parallel Tests
    identifier: parallel_tests
    type: Run
    spec:
      shell: Sh
      command: |
        npm test -- --shard=$HARNESS_STAGE_INDEX/$HARNESS_STAGE_TOTAL
    strategy:
      parallelism: 4
```

### Step Groups for Parallelism

```yaml
- stepGroup:
    name: Parallel Build
    identifier: parallel_build
    steps:
      - parallel:
          - step:
              name: Build Frontend
              identifier: build_frontend
              type: Run
              spec:
                command: npm run build:frontend
          - step:
              name: Build Backend
              identifier: build_backend
              type: Run
              spec:
                command: npm run build:backend
          - step:
              name: Build Docs
              identifier: build_docs
              type: Run
              spec:
                command: npm run build:docs
```

## Background Services

Start services for integration tests:

```yaml
# Database service
- step:
    name: Start PostgreSQL
    identifier: postgres
    type: Background
    spec:
      connectorRef: docker_connector
      image: postgres:14
      shell: Sh
      envVariables:
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
        POSTGRES_DB: testdb
      portBindings:
        "5432": "5432"
      resources:
        limits:
          memory: 1Gi

# Redis service
- step:
    name: Start Redis
    identifier: redis
    type: Background
    spec:
      connectorRef: docker_connector
      image: redis:7-alpine
      portBindings:
        "6379": "6379"

# Wait for services
- step:
    name: Wait for Services
    identifier: wait
    type: Run
    spec:
      shell: Sh
      command: |
        # Wait for PostgreSQL
        until pg_isready -h localhost -p 5432; do
          sleep 1
        done

        # Wait for Redis
        until redis-cli -h localhost ping; do
          sleep 1
        done
```

## Test Intelligence

### Configuration

```yaml
- step:
    name: Run Tests with TI
    identifier: test_ti
    type: RunTests
    spec:
      language: Java
      buildTool: Maven
      runOnlySelectedTests: true  # Enable TI
      testGlobs: "**/test/**/*.java"
      testAnnotations: org.junit.Test, org.junit.jupiter.api.Test
      packages: com.mycompany
      args: test -Dmaven.test.failure.ignore=true
      reports:
        type: JUnit
        spec:
          paths:
            - "**/surefire-reports/*.xml"
```

### Supported Languages

| Language | Build Tools |
|----------|-------------|
| **Java** | Maven, Gradle, Bazel |
| **Kotlin** | Maven, Gradle, Bazel |
| **Scala** | Maven, Gradle, Bazel, SBT |
| **C#** | NUnit, dotnet |
| **Python** | Pytest, Unittest |
| **Ruby** | RSpec |

### Test Splitting

```yaml
- step:
    name: Parallel Tests
    identifier: parallel_tests
    type: RunTests
    spec:
      language: Python
      buildTool: Pytest
      runOnlySelectedTests: true
      enableTestSplitting: true  # Split across parallel instances
      testSplitStrategy: ClassTiming  # or TestCount
      args: --junitxml=report.xml
    strategy:
      parallelism: 4  # Run 4 parallel test containers
```

## Plugins

### Harness Plugins

```yaml
# Slack notification
- step:
    name: Notify Slack
    identifier: slack
    type: Plugin
    spec:
      connectorRef: docker_connector
      image: plugins/slack
      settings:
        webhook: <+secrets.getValue("slack_webhook")>
        channel: builds
        template: |
          Build {{#success build.status}}succeeded{{else}}failed{{/success}}
          Repository: {{repo.name}}
          Branch: {{build.branch}}
          Commit: {{build.commit}}

# Upload to S3
- step:
    name: Upload Artifacts
    identifier: upload_s3
    type: Plugin
    spec:
      connectorRef: docker_connector
      image: plugins/s3
      settings:
        bucket: build-artifacts
        region: us-east-1
        access_key: <+secrets.getValue("aws_access_key")>
        secret_key: <+secrets.getValue("aws_secret_key")>
        source: dist/**/*
        target: builds/<+pipeline.sequenceId>
```

### GitHub Actions

```yaml
- step:
    name: GitHub Action
    identifier: github_action
    type: Action
    spec:
      uses: actions/setup-node@v3
      with:
        node-version: "18"
        cache: npm
```

### Bitrise Steps

```yaml
- step:
    name: Bitrise Step
    identifier: bitrise
    type: Bitrise
    spec:
      uses: script@1
      with:
        content: |
          echo "Running Bitrise step"
```

## Artifact Management

### Upload Artifacts

```yaml
- step:
    name: Upload Artifact
    identifier: upload_artifact
    type: Run
    spec:
      shell: Sh
      command: |
        tar -czf dist.tar.gz dist/
      outputVariables:
        - name: ARTIFACT_PATH
          type: String
          value: dist.tar.gz
```

### GCS Artifacts

```yaml
- step:
    name: Upload to GCS
    identifier: upload_gcs
    type: GCSUpload
    spec:
      connectorRef: gcp_connector
      bucket: build-artifacts
      sourcePath: dist/
      target: builds/<+pipeline.sequenceId>/
```

### S3 Artifacts

```yaml
- step:
    name: Upload to S3
    identifier: upload_s3
    type: S3Upload
    spec:
      connectorRef: aws_connector
      region: us-east-1
      bucket: build-artifacts
      sourcePath: dist/
      target: builds/<+pipeline.sequenceId>/
```

## CI Expressions

| Expression | Description |
|------------|-------------|
| `<+codebase.branch>` | Git branch name |
| `<+codebase.tag>` | Git tag (if tagged) |
| `<+codebase.commitSha>` | Full commit SHA |
| `<+codebase.shortCommitSha>` | Short commit SHA (7 chars) |
| `<+codebase.commitMessage>` | Commit message |
| `<+codebase.commitRef>` | Commit reference |
| `<+codebase.repoUrl>` | Repository URL |
| `<+codebase.gitUserId>` | Git user ID |
| `<+codebase.gitUserEmail>` | Git user email |
| `<+codebase.sourceBranch>` | PR source branch |
| `<+codebase.targetBranch>` | PR target branch |
| `<+codebase.prNumber>` | Pull request number |
| `<+codebase.prTitle>` | Pull request title |
| `<+codebase.prBody>` | Pull request body |
| `<+pipeline.sequenceId>` | Build number |
| `<+pipeline.executionId>` | Execution UUID |
| `<+pipeline.startTs>` | Start timestamp |

## Triggers

### Push Trigger

```yaml
trigger:
  name: Build on Push
  identifier: build_on_push
  enabled: true
  pipelineIdentifier: build_pipeline
  source:
    type: Webhook
    spec:
      type: Harness
      spec:
        type: Push
        spec:
          connectorRef: harness_code
          repoName: my-service
          autoAbortPreviousExecutions: true
          payloadConditions:
            - key: targetBranch
              operator: In
              value:
                - main
                - develop
```

### Pull Request Trigger

```yaml
trigger:
  name: Build on PR
  identifier: build_on_pr
  enabled: true
  pipelineIdentifier: build_pipeline
  source:
    type: Webhook
    spec:
      type: Harness
      spec:
        type: PullRequest
        spec:
          connectorRef: harness_code
          repoName: my-service
          autoAbortPreviousExecutions: true
          actions:
            - Open
            - Reopen
            - Synchronize
          payloadConditions:
            - key: targetBranch
              operator: Equals
              value: main
```

### Tag Trigger

```yaml
trigger:
  name: Build on Tag
  identifier: build_on_tag
  enabled: true
  pipelineIdentifier: release_pipeline
  source:
    type: Webhook
    spec:
      type: Harness
      spec:
        type: Tag
        spec:
          connectorRef: harness_code
          repoName: my-service
          tagCondition:
            operator: Regex
            value: "^v[0-9]+\\.[0-9]+\\.[0-9]+$"
```

## Complete CI/CD Pipeline Example

```yaml
pipeline:
  name: Full CI/CD Pipeline
  identifier: full_cicd
  projectIdentifier: my_project
  orgIdentifier: default
  properties:
    ci:
      codebase:
        connectorRef: harness_code
        repoName: my-service
        build: <+input>
  stages:
    # CI Stage
    - stage:
        name: Build and Test
        identifier: build_test
        type: CI
        spec:
          cloneCodebase: true
          infrastructure:
            type: Cloud
            spec:
              os: Linux
          caching:
            enabled: true
            key: npm-<+codebase.branch>
            paths:
              - node_modules
          execution:
            steps:
              - step:
                  name: Install
                  identifier: install
                  type: Run
                  spec:
                    shell: Sh
                    command: npm ci
              - parallel:
                  - step:
                      name: Lint
                      identifier: lint
                      type: Run
                      spec:
                        shell: Sh
                        command: npm run lint
                  - step:
                      name: Type Check
                      identifier: typecheck
                      type: Run
                      spec:
                        shell: Sh
                        command: npm run typecheck
              - step:
                  name: Test
                  identifier: test
                  type: Run
                  spec:
                    shell: Sh
                    command: npm test -- --coverage
                    reports:
                      type: JUnit
                      spec:
                        paths:
                          - junit.xml
              - step:
                  name: Build
                  identifier: build
                  type: Run
                  spec:
                    shell: Sh
                    command: npm run build
              - step:
                  name: Build and Push
                  identifier: build_push
                  type: BuildAndPushDockerRegistry
                  spec:
                    connectorRef: docker_connector
                    repo: myorg/myapp
                    tags:
                      - <+pipeline.sequenceId>
                      - <+codebase.shortCommitSha>
                    caching: true
                    optimize: true

    # CD Stage
    - stage:
        name: Deploy to Dev
        identifier: deploy_dev
        type: Deployment
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: my_service
            serviceInputs:
              serviceDefinition:
                type: Kubernetes
                spec:
                  artifacts:
                    primary:
                      primaryArtifactRef: docker_image
                      sources:
                        - identifier: docker_image
                          type: DockerRegistry
                          spec:
                            tag: <+pipeline.sequenceId>
          environment:
            environmentRef: development
            infrastructureDefinitions:
              - identifier: dev_k8s
          execution:
            steps:
              - step:
                  name: Rolling Deployment
                  identifier: rollingDeployment
                  type: K8sRollingDeploy
                  timeout: 10m
                  spec:
                    skipDryRun: false
            rollbackSteps:
              - step:
                  name: Rollback
                  identifier: rollback
                  type: K8sRollingRollback
                  timeout: 10m
                  spec: {}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Build timeout | Long-running step | Increase timeout, optimize build |
| Cache miss | Key mismatch | Check checksum file path |
| Image pull failed | Auth issue | Verify connector credentials |
| Test Intelligence not working | Missing config | Check language/buildTool settings |
| Out of memory | Resource limits | Increase memory in step spec |

### Debug Logging

```yaml
- step:
    name: Debug Info
    identifier: debug
    type: Run
    spec:
      shell: Sh
      command: |
        echo "=== Build Debug Info ==="
        echo "Branch: <+codebase.branch>"
        echo "Commit: <+codebase.commitSha>"
        echo "PR: <+codebase.prNumber>"
        echo "Build: <+pipeline.sequenceId>"
        echo "=== Environment ==="
        env | sort
        echo "=== Disk Usage ==="
        df -h
        echo "=== Memory ==="
        free -m
```

## Related Documentation

- [Harness CI Docs](https://developer.harness.io/docs/continuous-integration)
- [Test Intelligence](https://developer.harness.io/docs/continuous-integration/use-ci/run-tests/ti-overview)
- [Caching](https://developer.harness.io/docs/continuous-integration/use-ci/caching-ci-data/caching-overview)
- [Build Infrastructure](https://developer.harness.io/docs/continuous-integration/use-ci/set-up-build-infrastructure)
- [Harness Knowledge Base](../docs/HARNESS-KNOWLEDGE-BASE.md)
