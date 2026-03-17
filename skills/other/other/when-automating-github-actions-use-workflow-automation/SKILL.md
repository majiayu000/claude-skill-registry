---
name: when-automating-github-actions-use-workflow-automation
description: Advanced GitHub Actions workflow automation with AI swarm coordination, intelligent CI/CD pipelines, and comprehensive repository management. Coordinates cicd-engineer, workflow-automation, tester, and security-auditor agents through mesh topology to create, optimize, and maintain GitHub Actions workflows. Handles workflow generation, performance optimization, security hardening, matrix testing strategies, and workflow debugging. Use when building CI/CD pipelines, optimizing existing workflows, or establishing automation standards.
agents:
  - cicd-engineer
  - workflow-automation
  - tester
  - security-auditor
  - perf-analyzer
topology: mesh
mcp_tools:
  - mcp__claude-flow__swarm_init
  - mcp__claude-flow__agent_spawn
  - mcp__claude-flow__task_orchestrate
---

# GitHub Actions Workflow Automation Skill

## Overview

Design, implement, and optimize GitHub Actions CI/CD workflows using intelligent agent coordination. This skill provides end-to-end workflow automation including pipeline generation, security hardening, performance optimization, test orchestration, and debugging for robust continuous integration and deployment.

## When to Use This Skill

Activate this skill when creating new CI/CD pipelines from scratch, optimizing slow or inefficient workflows, implementing matrix testing strategies, hardening workflow security and secrets management, debugging failing workflows or flaky tests, establishing organizational workflow standards, or migrating from other CI systems (Jenkins, Travis, CircleCI) to GitHub Actions.

Use for both simple single-job workflows and complex multi-stage pipelines, monorepo workflows with selective job triggering, scheduled workflows and cron jobs, or workflow templates for organization-wide reuse.

## Agent Coordination Architecture

### Swarm Topology

Initialize a **mesh topology** enabling parallel workflow development with peer-to-peer coordination between specialized agents. Mesh topology allows security, testing, and performance agents to collaborate directly.

```bash
# Initialize mesh swarm for workflow automation
npx claude-flow@alpha swarm init --topology mesh --max-agents 6 --strategy balanced
```

### Specialized Agent Roles

**CI/CD Engineer** (`cicd-engineer`): Primary workflow architect that designs pipeline structure, selects appropriate actions, configures jobs and steps, and implements deployment strategies. Owns overall workflow design.

**Workflow Automation** (`workflow-automation`): Specializes in GitHub Actions-specific optimizations including caching strategies, artifact management, workflow reuse, and matrix configurations. Expert in GitHub Actions ecosystem.

**Test Engineer** (`tester`): Designs test orchestration strategies including parallel testing, matrix testing, test reporting, and failure analysis. Ensures comprehensive test coverage in CI/CD.

**Security Auditor** (`security-auditor`): Hardens workflows against security vulnerabilities including secrets management, third-party action vetting, permission scoping, and supply chain security.

**Performance Analyzer** (`perf-analyzer`): Optimizes workflow execution time through parallelization, caching, selective job triggering, and resource optimization. Monitors workflow performance metrics.

## Workflow Automation Processes (SOP)

### Workflow 1: Generate CI/CD Pipeline from Scratch

Create comprehensive CI/CD workflow for new or existing project.

**Phase 1: Requirements Analysis**

**Step 1.1: Initialize Mesh Swarm**

```bash
# Set up mesh swarm for collaborative workflow development
mcp__claude-flow__swarm_init topology=mesh maxAgents=6 strategy=balanced

# Spawn specialized agents
mcp__claude-flow__agent_spawn type=coder name=cicd-engineer
mcp__claude-flow__agent_spawn type=coordinator name=workflow-automation
mcp__claude-flow__agent_spawn type=researcher name=tester
mcp__claude-flow__agent_spawn type=analyst name=security-auditor
mcp__claude-flow__agent_spawn type=optimizer name=perf-analyzer
```

**Step 1.2: Analyze Project Structure**

```plaintext
Task("CI/CD Engineer", "
  Analyze project and determine CI/CD requirements:

  1. Detect project type (Node.js, Python, Rust, Go, Java, etc.)
  2. Identify build system (npm, cargo, maven, gradle, make)
  3. Discover test frameworks and test locations
  4. Check for linting and formatting tools
  5. Identify deployment targets (npm registry, Docker Hub, AWS, etc.)
  6. Review existing workflows if migrating from other CI

  Use scripts/project-analyzer.sh for detection
  Store project analysis in memory: github-actions/analysis
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'project analysis'
", "cicd-engineer")
```

**Step 1.3: Define Pipeline Stages**

```plaintext
Task("CI/CD Engineer", "
  Design pipeline stages based on project analysis:

  1. Define CI stages: lint → test → build → security-scan
  2. Define CD stages: package → deploy-staging → deploy-production
  3. Determine trigger conditions (push, PR, tag, schedule)
  4. Plan matrix configurations (OS, runtime versions)
  5. Identify dependencies between stages
  6. Create workflow structure diagram

  Reference references/pipeline-patterns.md
  Store pipeline design in memory: github-actions/pipeline-design
", "cicd-engineer")
```

**Phase 2: Parallel Workflow Development**

Execute specialized agents in parallel to build workflow components.

**Step 2.1: Generate Base Workflow Structure**

```plaintext
Task("CI/CD Engineer", "
  Create base workflow YAML structure:

  1. Use references/workflow-templates/${PROJECT_TYPE}.yml as base
  2. Configure workflow triggers (on: push/pull_request/schedule)
  3. Define jobs structure with dependencies
  4. Set up runner environments (ubuntu-latest, macos-latest, windows-latest)
  5. Configure concurrency groups to prevent redundant runs
  6. Add workflow_dispatch for manual triggers

  Use scripts/workflow-generator.sh
  Store base workflow in memory: github-actions/base-workflow
", "cicd-engineer")
```

**Step 2.2: Implement Testing Strategy**

```plaintext
Task("Test Engineer", "
  Design and implement test orchestration:

  1. Configure test matrix (multiple Node versions, Python versions, etc.)
  2. Set up parallel test execution with job matrix
  3. Implement test result reporting (GitHub Actions Summary)
  4. Configure test coverage collection and upload
  5. Add test artifact collection for debugging
  6. Set up flaky test retry logic

  Use references/test-strategies.md
  Store test config in memory: github-actions/testing
", "tester")
```

**Step 2.3: Add Security Hardening**

```plaintext
Task("Security Auditor", "
  Implement workflow security best practices:

  1. Scope GITHUB_TOKEN permissions to minimum required
  2. Pin third-party actions to specific SHA (not @v1 tags)
  3. Configure secrets management properly
  4. Add dependency scanning (Dependabot, Snyk)
  5. Implement SAST scanning (CodeQL, Semgrep)
  6. Add container image scanning if using Docker
  7. Configure branch protection rules

  Use references/workflow-security.md
  Store security config in memory: github-actions/security
", "security-auditor")
```

**Step 2.4: Optimize Performance**

```plaintext
Task("Performance Analyzer", "
  Optimize workflow execution time:

  1. Implement aggressive caching (dependencies, build artifacts)
  2. Configure conditional job execution (path filters)
  3. Parallelize independent jobs where possible
  4. Use faster runners (GitHub-hosted vs self-hosted)
  5. Optimize Docker layer caching for containerized workflows
  6. Add build time monitoring

  Use references/optimization-techniques.md
  Store optimization config in memory: github-actions/optimization
", "perf-analyzer")
```

**Step 2.5: Configure Deployment Automation**

```plaintext
Task("Workflow Automation", "
  Set up deployment automation:

  1. Configure environment-specific deployment jobs
  2. Implement deployment approvals for production
  3. Add rollback capability
  4. Configure deployment status checks
  5. Set up deployment notifications (Slack, Discord)
  6. Implement blue-green or canary deployment if applicable

  Use references/deployment-automation.md
  Store deployment config in memory: github-actions/deployment
", "workflow-automation")
```

**Phase 3: Workflow Integration and Testing**

**Step 3.1: Synthesize Workflow Components**

```plaintext
Task("CI/CD Engineer", "
  Integrate all agent contributions into final workflow:

  1. Retrieve all components from memory (base, testing, security, optimization, deployment)
  2. Merge configurations ensuring no conflicts
  3. Validate YAML syntax using scripts/workflow-validator.sh
  4. Check for logical errors (circular dependencies, missing inputs)
  5. Add comprehensive comments explaining each section
  6. Generate workflow diagram showing job dependencies

  Store final workflow in memory: github-actions/final
", "cicd-engineer")
```

**Step 3.2: Validate Workflow Locally**

```bash
# Validate workflow syntax
bash scripts/workflow-validator.sh \
  --workflow ".github/workflows/ci.yml" \
  --check-actions true \
  --check-secrets true

# Test workflow locally using act
act push --job test --dry-run
```

**Step 3.3: Create Pull Request with Workflow**

```bash
# Create feature branch and commit workflow
git checkout -b "ci/add-github-actions-workflow"
mkdir -p .github/workflows
cp final-workflow.yml .github/workflows/ci.yml
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions CI/CD workflow"
git push origin ci/add-github-actions-workflow

# Create PR
bash scripts/github-api.sh create-pr \
  --repo <owner/repo> \
  --head "ci/add-github-actions-workflow" \
  --base "main" \
  --title "Add GitHub Actions CI/CD Pipeline" \
  --body-file "references/workflow-pr-description.md"
```

**Step 3.4: Monitor First Workflow Run**

```plaintext
Task("CI/CD Engineer", "
  Monitor and validate first workflow execution:

  1. Watch workflow run in GitHub Actions UI
  2. Check for job failures or warnings
  3. Validate caching is working correctly
  4. Verify test results are reported properly
  5. Confirm security scans complete successfully
  6. Measure total workflow execution time

  Store first-run metrics in memory: github-actions/first-run
", "cicd-engineer")
```

### Workflow 2: Optimize Existing Workflow Performance

Improve slow or inefficient workflows.

**Phase 1: Performance Analysis**

**Step 1.1: Collect Workflow Metrics**

```bash
# Analyze workflow execution history
bash scripts/workflow-analytics.sh analyze \
  --repo <owner/repo> \
  --workflow "ci.yml" \
  --runs 50 \
  --output "references/workflow-metrics.json"
```

**Step 1.2: Identify Bottlenecks**

```plaintext
Task("Performance Analyzer", "
  Analyze workflow performance and identify bottlenecks:

  1. Review workflow metrics from references/workflow-metrics.json
  2. Identify slowest jobs and steps
  3. Check cache hit rates (low = opportunity)
  4. Analyze dependency installation time
  5. Check for serialized jobs that could be parallelized
  6. Identify redundant operations across jobs

  Use scripts/bottleneck-analyzer.sh
  Store bottleneck analysis in memory: github-actions/bottlenecks
", "perf-analyzer")
```

**Phase 2: Optimization Implementation**

**Step 2.1: Implement Caching Strategy**

```yaml
# Add aggressive caching
- name: Cache dependencies
  uses: actions/cache@v4
  with:
    path: |
      ~/.npm
      ~/.cargo/registry
      ~/.cargo/git
      target/
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json', '**/Cargo.lock') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

**Step 2.2: Parallelize Independent Jobs**

```yaml
# Convert serial jobs to parallel
jobs:
  lint:
    runs-on: ubuntu-latest
    # Remove "needs: build" to run in parallel with build

  test:
    runs-on: ubuntu-latest
    # Remove "needs: build" if tests don't need build artifacts

  security-scan:
    runs-on: ubuntu-latest
    # Run in parallel with other jobs
```

**Step 2.3: Add Path Filtering**

```yaml
# Only run workflows when relevant files change
on:
  push:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'package.json'
      - '.github/workflows/ci.yml'
  pull_request:
    paths:
      - 'src/**'
      - 'tests/**'
```

**Step 2.4: Optimize Docker Builds**

```yaml
# Use Docker layer caching and buildx
- name: Set up Docker Buildx
  uses: docker/setup-buildx-action@v3

- name: Build and push
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: ${{ env.IMAGE_TAG }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

**Phase 3: Validation**

**Step 3.1: Measure Improvement**

```bash
# Compare workflow execution time before/after
bash scripts/workflow-analytics.sh compare \
  --before "references/metrics-before.json" \
  --after "references/metrics-after.json" \
  --output "references/improvement-report.md"
```

### Workflow 3: Debug Failing Workflow

Systematically debug and fix failing workflows.

**Phase 1: Failure Analysis**

**Step 1.1: Collect Failure Context**

```bash
# Fetch failed workflow run details
bash scripts/github-api.sh get-workflow-run \
  --repo <owner/repo> \
  --run-id <run-id> \
  --include-logs true \
  --output "references/failed-run.json"
```

**Step 1.2: Analyze Failure Patterns**

```plaintext
Task("CI/CD Engineer", "
  Analyze workflow failure:

  1. Review failure logs from references/failed-run.json
  2. Classify failure type (test failure, build error, timeout, rate limit)
  3. Check if failure is intermittent (flaky) or consistent
  4. Identify changed files that might have triggered failure
  5. Check for environment-specific issues (OS, runtime version)
  6. Review recent workflow file changes

  Store failure analysis in memory: github-actions/failure-analysis
", "cicd-engineer")
```

**Phase 2: Root Cause Investigation**

**Step 2.1: Reproduce Locally**

```bash
# Reproduce workflow locally using act
act push \
  --job <failed-job-name> \
  --secret-file .secrets \
  --verbose
```

**Step 2.2: Add Debug Logging**

```yaml
# Temporarily add debug steps
- name: Debug Environment
  run: |
    echo "Runner OS: ${{ runner.os }}"
    echo "Node Version: $(node --version)"
    echo "Working Directory: $(pwd)"
    ls -la
    env | sort

- name: Debug Dependencies
  run: |
    npm list --depth=0 || true
    cargo tree --depth=0 || true
```

**Phase 3: Fix Implementation**

**Step 3.1: Apply Fix**

Based on root cause, apply appropriate fix:

**Flaky Test Fix:**
```yaml
# Add test retry logic
- name: Run Tests with Retry
  uses: nick-fields/retry@v2
  with:
    timeout_minutes: 10
    max_attempts: 3
    command: npm test
```

**Timeout Fix:**
```yaml
# Increase timeout for slow jobs
jobs:
  build:
    timeout-minutes: 30  # Increased from default 6 hours
```

**Dependency Issue Fix:**
```yaml
# Lock dependency versions
- name: Install Dependencies
  run: npm ci  # Use ci instead of install for reproducible builds
```

**Step 3.2: Validate Fix**

```bash
# Push fix and monitor workflow
git add .github/workflows/ci.yml
git commit -m "fix(ci): resolve workflow failure in build job"
git push origin main

# Monitor workflow run
bash scripts/workflow-monitor.sh \
  --repo <owner/repo> \
  --branch "main" \
  --wait-for-completion true
```

## Advanced Workflow Patterns

### Matrix Testing Strategy

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        node-version: [16, 18, 20]
        include:
          # Add specific configuration combinations
          - os: ubuntu-latest
            node-version: 20
            coverage: true
        exclude:
          # Exclude problematic combinations
          - os: windows-latest
            node-version: 16
      fail-fast: false  # Continue even if one combination fails
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-build.yml
name: Reusable Build Workflow
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      deploy_key:
        required: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: npm run build
```

Call reusable workflow:
```yaml
jobs:
  prod-build:
    uses: ./.github/workflows/reusable-build.yml
    with:
      environment: production
    secrets:
      deploy_key: ${{ secrets.PROD_DEPLOY_KEY }}
```

### Composite Actions

Create reusable action compositions:

```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Set up Node.js and install dependencies with caching'
inputs:
  node-version:
    description: 'Node.js version'
    required: true
runs:
  using: 'composite'
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ inputs.node-version }}
        cache: 'npm'
    - run: npm ci
      shell: bash
```

### Conditional Execution

```yaml
jobs:
  deploy:
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Production
        run: ./deploy.sh
```

## MCP Tool Integration

### Task Orchestration

```bash
# Orchestrate workflow optimization
mcp__claude-flow__task_orchestrate \
  task="Optimize CI/CD workflow performance" \
  strategy=parallel \
  maxAgents=5 \
  priority=high
```

### Swarm Monitoring

```bash
# Monitor workflow automation agents
mcp__claude-flow__swarm_status verbose=true

# Get agent metrics
mcp__claude-flow__agent_metrics metric=all
```

## Best Practices

**Pin Action Versions**: Always pin actions to specific commit SHA for security and reproducibility. Never use `@main` or `@latest`.

**Minimal Permissions**: Set `permissions` at job level with least privilege required. Don't grant unnecessary permissions.

**Secrets Management**: Never log secrets or echo environment variables that might contain secrets. Use GitHub Secrets for sensitive data.

**Fail Fast Configuration**: Use `fail-fast: false` in matrix to see all failures, not just first one.

**Caching Strategy**: Cache dependencies aggressively but use specific cache keys to avoid stale caches.

**Workflow Documentation**: Add comments explaining non-obvious workflow logic. Future maintainers will thank you.

**Monitoring and Alerts**: Set up Slack/Discord notifications for workflow failures. Don't rely on checking GitHub manually.

**Testing Before Merge**: Test workflow changes in feature branches before merging to main.

## Error Handling

**API Rate Limiting**: Implement exponential backoff for GitHub API calls. Use `GITHUB_TOKEN` for authenticated requests.

**Flaky Tests**: Implement retry logic for intermittently failing tests. Track flaky tests and fix root causes.

**Timeout Management**: Set reasonable timeouts for each job. Don't let workflows run indefinitely.

**Artifact Storage**: Clean up old artifacts to avoid storage quota issues. Use artifact retention policies.

**Workflow Syntax Errors**: Always validate YAML syntax locally before pushing. Use `actionlint` for linting.

## References

- `references/workflow-templates/` - Language-specific workflow templates
- `references/pipeline-patterns.md` - Common CI/CD pipeline patterns
- `references/test-strategies.md` - Test orchestration strategies
- `references/workflow-security.md` - Security best practices
- `references/optimization-techniques.md` - Performance optimization guide
- `references/deployment-automation.md` - Deployment workflow patterns
- `scripts/project-analyzer.sh` - Project type and build system detection
- `scripts/workflow-generator.sh` - Workflow YAML generation
- `scripts/workflow-validator.sh` - Workflow syntax validation
- `scripts/workflow-analytics.sh` - Workflow performance analysis
- `scripts/bottleneck-analyzer.sh` - Performance bottleneck identification
- `scripts/workflow-monitor.sh` - Real-time workflow monitoring
