---
name: harness-ci
description: Harness CI (Continuous Integration) for container-native builds with test intelligence, caching, parallelization, and build infrastructure management
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, WebSearch]
dependencies: [harness-mcp, harness-cd]
triggers: [harness ci, harness build, build pipeline, ci pipeline, test intelligence, ci infrastructure]
---

# Harness CI Skill

Container-native CI builds with test intelligence, caching, parallelization, and infrastructure management.

## Build Infrastructure

- **Cloud (Recommended):** Zero-config hosted, auto-scaling, pre-installed tools
  ```yaml
  infrastructure:
    type: Cloud
    spec:
      os: Linux  # Linux, MacOS, Windows
  ```

- **Kubernetes:** Self-hosted via k8s clusters
  ```yaml
  infrastructure:
    type: KubernetesDirect
    spec:
      connectorRef: k8s_connector
      namespace: harness-builds
      os: Linux
  ```

- **VMs:** AWS, Azure, GCP pool-based scaling

## Basic Pipeline Structure

```yaml
pipeline:
  name: Build Pipeline
  identifier: build_pipeline
  properties:
    ci:
      codebase:
        connectorRef: harness_code
        repoName: my-service
        build: <+input>
  stages:
    - stage:
        name: Build and Test
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
                  name: Install
                  type: Run
                  spec:
                    shell: Sh
                    command: npm ci
              - step:
                  name: Test
                  type: Run
                  spec:
                    command: npm test -- --coverage
              - step:
                  name: Build
                  type: Run
                  spec:
                    command: npm run build
```

## Step Types

**Run:** Execute shell commands
```yaml
- step:
    name: Build
    type: Run
    spec:
      shell: Sh
      command: npm run build
      envVariables:
        NODE_ENV: production
      resources:
        limits:
          memory: 2Gi
          cpu: "1"
```

**RunTests (Test Intelligence):** Language/framework-aware test execution
```yaml
- step:
    type: RunTests
    spec:
      language: Java  # Java, Kotlin, Scala, C#, Python, Ruby
      buildTool: Maven  # Maven, Gradle, Bazel, etc.
      runOnlySelectedTests: true  # Enable TI
      enableTestSplitting: true   # Parallel execution
      testAnnotations: org.junit.Test
      packages: com.myapp
```

**Docker Registry Build/Push**
```yaml
- step:
    name: Build and Push
    type: BuildAndPushDockerRegistry
    spec:
      connectorRef: docker_connector
      repo: myorg/myapp
      tags: [<+pipeline.sequenceId>, <+codebase.shortCommitSha>, latest]
      dockerfile: Dockerfile
      caching: true
      buildArgs:
        VERSION: <+pipeline.sequenceId>
```

**ECR/GCR/ACR:** Replace `BuildAndPushDockerRegistry` with `BuildAndPushECR`, `BuildAndPushGCR`, or `BuildAndPushACR` with appropriate connector refs.

## Caching

**S3 Cache:**
```yaml
- step:
    name: Save Cache
    type: SaveCacheS3
    spec:
      connectorRef: aws_connector
      bucket: harness-cache
      key: npm-{{ checksum "package-lock.json" }}
      sourcePaths: [node_modules]
- step:
    name: Restore Cache
    type: RestoreCacheS3
    spec:
      connectorRef: aws_connector
      bucket: harness-cache
      key: npm-{{ checksum "package-lock.json" }}
      failIfKeyNotFound: false
```

**GCS Cache:** Replace S3 steps with `SaveCacheGCS`/`RestoreCacheGCS`.

## Parallelism

**Matrix Strategy:** Run steps with multiple configurations
```yaml
- step:
    name: Test Matrix
    type: Run
    spec:
      command: npm test
      envVariables:
        NODE_VERSION: <+matrix.nodeVersion>
        DB_TYPE: <+matrix.database>
    strategy:
      matrix:
        nodeVersion: ["16", "18", "20"]
        database: [postgres, mysql]
      maxConcurrency: 4
```

**Parallelism:** Run same step multiple times
```yaml
- step:
    name: Parallel Tests
    type: Run
    spec:
      command: npm test -- --shard=$HARNESS_STAGE_INDEX/$HARNESS_STAGE_TOTAL
    strategy:
      parallelism: 4
```

**Parallel Step Groups:**
```yaml
- stepGroup:
    name: Parallel Build
    steps:
      - parallel:
          - step:
              name: Build Frontend
              type: Run
              spec:
                command: npm run build:frontend
          - step:
              name: Build Backend
              type: Run
              spec:
                command: npm run build:backend
```

## Background Services

Start services (databases, caches) for integration tests:
```yaml
- step:
    name: PostgreSQL
    type: Background
    spec:
      image: postgres:14
      envVariables:
        POSTGRES_USER: test
        POSTGRES_PASSWORD: test
        POSTGRES_DB: testdb
      portBindings:
        "5432": "5432"
      resources:
        limits:
          memory: 1Gi

- step:
    name: Wait for DB
    type: Run
    spec:
      command: until pg_isready -h localhost -p 5432; do sleep 1; done
```

## Plugins & Actions

**Slack Notification:**
```yaml
- step:
    name: Notify Slack
    type: Plugin
    spec:
      image: plugins/slack
      settings:
        webhook: <+secrets.getValue("slack_webhook")>
        channel: builds
        template: "Build {{#success build.status}}succeeded{{else}}failed{{/success}}"
```

**S3 Upload:**
```yaml
- step:
    name: Upload Artifacts
    type: Plugin
    spec:
      image: plugins/s3
      settings:
        bucket: build-artifacts
        source: dist/**/*
        target: builds/<+pipeline.sequenceId>
```

**GitHub Actions:**
```yaml
- step:
    name: Setup Node
    type: Action
    spec:
      uses: actions/setup-node@v3
      with:
        node-version: "18"
        cache: npm
```

## Artifact Management

Upload build outputs to cloud storage:
- **S3:** Type `S3Upload`, spec: `bucket`, `sourcePath`, `target`
- **GCS:** Type `GCSUpload`, spec: `bucket`, `sourcePath`, `target`

## CI Expressions

| Expression | Description |
|------------|-------------|
| `<+codebase.branch>` | Git branch name |
| `<+codebase.commitSha>` | Full commit SHA |
| `<+codebase.shortCommitSha>` | Short SHA (7 chars) |
| `<+codebase.commitMessage>` | Commit message |
| `<+pipeline.sequenceId>` | Build number |
| `<+pipeline.executionId>` | Execution UUID |
| `<+secrets.getValue("key")>` | Secret value |

## Triggers

**Push Trigger:**
```yaml
trigger:
  name: Build on Push
  pipelineIdentifier: build_pipeline
  source:
    type: Webhook
    spec:
      type: Push
      connectorRef: harness_code
      repoName: my-service
      payloadConditions:
        - key: targetBranch
          operator: In
          value: [main, develop]
```

**Pull Request & Tag:** Use `type: PullRequest` or `type: Tag` with `actions` or `tagCondition`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build timeout | Increase timeout, optimize steps |
| Cache miss | Verify checksum file path |
| Image pull failed | Check connector credentials |
| TI not working | Verify language/buildTool config |
| Out of memory | Increase step memory limits |

**Debug:**
```yaml
- step:
    name: Debug
    type: Run
    spec:
      command: |
        echo "Branch: <+codebase.branch>"
        echo "Build: <+pipeline.sequenceId>"
        env | sort
        df -h
```

## Related Documentation

- [Harness CI Docs](https://developer.harness.io/docs/continuous-integration)
- [Test Intelligence](https://developer.harness.io/docs/continuous-integration/use-ci/run-tests/ti-overview)
- [Caching](https://developer.harness.io/docs/continuous-integration/use-ci/caching-ci-data/caching-overview)
- [Build Infrastructure](https://developer.harness.io/docs/continuous-integration/use-ci/set-up-build-infrastructure)
