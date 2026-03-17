---
name: github-workflow
description: GitHub Actions workflow automation for intelligent CI/CD pipelines with adaptive optimization. Use for workflow creation, pipeline optimization, security scanning, failure analysis, and automated deployment strategies.
---

# GitHub Workflow Automation Skill

## Overview

This skill enables creation and management of intelligent, self-organizing CI/CD pipelines using GitHub Actions with swarm coordination. It provides adaptive workflow generation, performance optimization, and automated pipeline management.

**Key Capabilities:**
- Swarm-powered GitHub Actions workflows
- Dynamic workflow generation based on code analysis
- Intelligent test selection and parallelization
- Self-healing pipeline automation
- Performance monitoring and optimization

## Quick Start

```yaml
# .github/workflows/intelligent-ci.yml
name: Intelligent CI with Swarms
on: [push, pull_request]

jobs:
  analyze-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Analyze Changes
        run: |
          # Determine affected packages
          CHANGED=$(git diff --name-only HEAD~1)
          echo "Changed files: $CHANGED"

      - name: Dynamic Test Selection
        run: |
          # Run only affected tests
          npm test -- --changedSince=HEAD~1
```

## When to Use

- **New Project Setup**: Creating initial CI/CD pipelines
- **Pipeline Optimization**: Improving slow or inefficient workflows
- **Security Integration**: Adding automated security scanning
- **Deployment Automation**: Setting up progressive deployment strategies
- **Failure Recovery**: Implementing self-healing pipelines

## Usage Examples

### 1. Multi-Language Detection Workflow

```yaml
# .github/workflows/polyglot-ci.yml
name: Polyglot Project Handler
on: push

jobs:
  detect-and-build:
    runs-on: ubuntu-latest
    outputs:
      matrix: ${{ steps.detect.outputs.matrix }}
    steps:
      - uses: actions/checkout@v4

      - name: Detect Languages
        id: detect
        run: |
          # Detect project languages
          LANGUAGES=()
          [ -f "package.json" ] && LANGUAGES+=("node")
          [ -f "requirements.txt" ] && LANGUAGES+=("python")
          [ -f "go.mod" ] && LANGUAGES+=("go")
          [ -f "Cargo.toml" ] && LANGUAGES+=("rust")

          # Build matrix JSON
          MATRIX=$(printf '%s\n' "${LANGUAGES[@]}" | jq -R . | jq -s '{language: .}')
          echo "matrix=$MATRIX" >> $GITHUB_OUTPUT

  build:
    needs: detect-and-build
    strategy:
      matrix: ${{ fromJson(needs.detect-and-build.outputs.matrix) }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build ${{ matrix.language }}
        run: |
          case "${{ matrix.language }}" in
            node) npm ci && npm test ;;
            python) pip install -r requirements.txt && pytest ;;
            go) go build ./... && go test ./... ;;
            rust) cargo build && cargo test ;;
          esac
```

### 2. Adaptive Security Scanning

```yaml
# .github/workflows/security-scan.yml
name: Intelligent Security Scan
on:
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  security-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Security Scans
        id: security
        run: |
          # Initialize results
          echo '{"issues": []}' > security-results.json

          # npm audit for Node.js
          if [ -f "package-lock.json" ]; then
            npm audit --json >> security-results.json || true
          fi

          # pip audit for Python
          if [ -f "requirements.txt" ]; then
            pip install pip-audit
            pip-audit --format=json >> security-results.json || true
          fi

      - name: Create Security Issues
        if: failure()
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Parse and create issues for critical findings
          jq -r '.issues[]? | select(.severity == "critical")' security-results.json | \
          while read -r issue; do
            gh issue create \
              --title "Security: $(echo "$issue" | jq -r '.title')" \
              --body "$(echo "$issue" | jq -r '.description')" \
              --label "security,critical"
          done
```

### 3. Self-Healing Pipeline

```yaml
# .github/workflows/self-healing.yml
name: Self-Healing Pipeline
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]

jobs:
  heal-pipeline:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Diagnose Failure
        id: diagnose
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Get failed jobs
          FAILED_JOBS=$(gh run view ${{ github.event.workflow_run.id }} \
            --json jobs --jq '.jobs[] | select(.conclusion == "failure")')

          echo "Failed jobs: $FAILED_JOBS"

          # Common auto-fixes
          LOGS=$(gh run view ${{ github.event.workflow_run.id }} --log)

          if echo "$LOGS" | grep -q "npm ERR! peer dep"; then
            echo "fix=npm-peer-deps" >> $GITHUB_OUTPUT
          elif echo "$LOGS" | grep -q "ENOSPC"; then
            echo "fix=disk-space" >> $GITHUB_OUTPUT
          fi

      - name: Apply Auto-Fix
        if: steps.diagnose.outputs.fix != ''
        run: |
          case "${{ steps.diagnose.outputs.fix }}" in
            npm-peer-deps)
              npm install --legacy-peer-deps
              ;;
            disk-space)
              npm cache clean --force
              ;;
          esac
```

### 4. Progressive Deployment

```yaml
# .github/workflows/progressive-deploy.yml
name: Progressive Deployment
on:
  push:
    branches: [main]

jobs:
  analyze-risk:
    runs-on: ubuntu-latest
    outputs:
      risk: ${{ steps.risk.outputs.level }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Analyze Risk
        id: risk
        run: |
          # Count changed files
          CHANGED=$(git diff --name-only HEAD~1 | wc -l)

          # Determine risk level
          if [ "$CHANGED" -gt 50 ]; then
            echo "level=high" >> $GITHUB_OUTPUT
          elif [ "$CHANGED" -gt 10 ]; then
            echo "level=medium" >> $GITHUB_OUTPUT
          else
            echo "level=low" >> $GITHUB_OUTPUT
          fi

  deploy:
    needs: analyze-risk
    runs-on: ubuntu-latest
    steps:
      - name: Deploy Strategy
        run: |
          case "${{ needs.analyze-risk.outputs.risk }}" in
            low)
              echo "Direct deployment"
              # Deploy immediately
              ;;
            medium)
              echo "Canary deployment - 10%"
              # Deploy to 10% of traffic
              ;;
            high)
              echo "Blue-green deployment with rollback"
              # Full blue-green with auto-rollback
              ;;
          esac
```

## MCP Tool Integration

### Multi-Agent Pipeline Orchestration

```javascript
// Initialize workflow automation swarm

// Create automation rules
  rules: [
    {
      trigger: "pull_request",
      conditions: ["files_changed > 10", "complexity_high"],
      actions: ["spawn_review_swarm", "parallel_testing", "security_scan"]
    },
    {
      trigger: "push_to_main",
      conditions: ["all_tests_pass", "security_cleared"],
      actions: ["deploy_staging", "performance_test", "notify_stakeholders"]
    }
  ]
}

// Orchestrate workflow management
  task: "Manage intelligent CI/CD pipeline with continuous optimization",
  strategy: "adaptive",
  priority: "high"
}
```

### Performance Monitoring

```javascript
// Generate workflow performance reports
  format: "detailed",
  timeframe: "30d"
}

// Analyze bottlenecks
  component: "github_actions_workflow",
  metrics: ["build_time", "test_duration", "deployment_latency"]
}

// Store insights
  action: "store",
  key: "workflow/performance/analysis",
  value: {
    bottlenecks_identified: ["slow_test_suite", "inefficient_caching"],
    optimization_opportunities: ["parallel_matrix", "smart_caching"],
    cost_optimization_potential: "23%"
  }
}
```

## Workflow Optimization Commands

### Pipeline Optimization

```bash
# Analyze workflow performance
gh run list --workflow=ci.yml --limit=20 --json databaseId,conclusion,startedAt,updatedAt | \
  jq 'map({id: .databaseId, status: .conclusion, duration: ((.updatedAt | fromdateiso8601) - (.startedAt | fromdateiso8601))})'

# Identify slow steps
gh run view $RUN_ID --json jobs --jq '.jobs[] | {name: .name, duration: .steps | map(.completedAt | fromdateiso8601) | max - (.steps | map(.startedAt | fromdateiso8601) | min)}'
```

### Failure Analysis

```bash
# Analyze failed runs
gh run list --status=failure --limit=10 --json databaseId,name,headBranch | \
  jq -r '.[] | "\(.databaseId): \(.name) on \(.headBranch)"'

# Get failure details
gh run view $RUN_ID --log-failed
```

## Best Practices

### 1. Workflow Organization
- Use reusable workflows for common operations
- Implement proper caching strategies
- Set appropriate timeouts for each job
- Use workflow dependencies wisely

### 2. Security
- Store secrets in GitHub Secrets
- Use OIDC for cloud authentication
- Implement least-privilege principles
- Audit workflow permissions regularly

### 3. Performance
- Cache dependencies between runs
- Use appropriate runner sizes
- Implement early termination for failures
- Optimize parallel execution

### 4. Cost Management
- Use self-hosted runners for heavy workloads
- Implement concurrency controls
- Cache Docker layers
- Skip redundant workflow runs

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| max-parallel | number | 4 | Maximum parallel jobs |
| timeout-minutes | number | 30 | Job timeout |
| retry-on-failure | boolean | false | Auto-retry failed jobs |
| cache-strategy | string | "npm" | Dependency caching |

## Error Handling

### Common Errors

**Error: ENOSPC (No space left)**
- Cause: Disk space exhausted
- Solution: Clear caches, use smaller runners

**Error: Rate limit exceeded**
- Cause: Too many API calls
- Solution: Add delays, use caching

**Error: Timeout exceeded**
- Cause: Long-running job
- Solution: Increase timeout or optimize job

## Related Skills

- [github-sync](../github-sync/SKILL.md) - Repository synchronization
- [github-swarm-pr](../github-swarm-pr/SKILL.md) - PR management
- [github-swarm-issue](../github-swarm-issue/SKILL.md) - Issue coordination

---

## Version History

- **1.0.0** (2026-01-02): Initial skill conversion from workflow-automation agent
