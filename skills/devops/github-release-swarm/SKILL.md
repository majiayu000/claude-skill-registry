---
name: github-release-swarm
description: Orchestrate complex software releases using AI swarms that handle everything from changelog generation to multi-platform deployment. Use for release planning, automated versioning, artifact building, progressive deployment, and multi-repo releases.
---

# GitHub Release Swarm Skill

## Overview

Orchestrate complex software releases using AI swarms. This skill handles release planning, automated versioning, changelog generation, artifact building, progressive deployment, and multi-repo release coordination.

## Quick Start

```bash
# Get last release tag
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')

# Get commits since last release
gh api repos/owner/repo/compare/${LAST_TAG}...HEAD --jq '.commits[].commit.message'

# Get merged PRs since last release
gh pr list --state merged --base main --json number,title,labels,mergedAt

# Create release
gh release create v2.0.0 --title "Release v2.0.0" --notes "..."
```

## When to Use

- Planning and coordinating major releases
- Automated changelog generation
- Multi-platform artifact building
- Progressive deployment strategies
- Multi-repository release coordination
- Hotfix automation

## Release Agents

| Agent | Purpose |
|-------|---------|
| Changelog Agent | Semantic commit analysis, contributor attribution |
| Version Agent | Smart version bumping, breaking change detection |
| Build Agent | Cross-platform compilation, artifact optimization |
| Test Agent | Pre-release testing, environment validation |
| Deploy Agent | Multi-target deployment, staged rollout |

## Usage Examples

### 1. Release Planning

```bash
# Get commit history since last release
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')
COMMITS=$(gh api repos/owner/repo/compare/${LAST_TAG}...HEAD --jq '.commits')

# Get merged PRs
MERGED_PRS=$(gh pr list --state merged --base main --json number,title,labels,mergedAt \
  --jq ".[] | select(.mergedAt > \"$(gh release view $LAST_TAG --json publishedAt -q .publishedAt)\")")

# Plan release with commit analysis
npx ruv-swarm github release-plan \
  --commits "$COMMITS" \
  --merged-prs "$MERGED_PRS" \
  --analyze-commits \
  --suggest-version \
  --identify-breaking \
  --generate-timeline
```

### 2. Generate Changelog

```bash
# Get all merged PRs between versions
PRS=$(gh pr list --state merged --base main --json number,title,labels,author,mergedAt \
  --jq ".[] | select(.mergedAt > \"$(gh release view v1.0.0 --json publishedAt -q .publishedAt)\")")

# Get contributors
CONTRIBUTORS=$(echo "$PRS" | jq -r '[.author.login] | unique | join(", ")')

# Get commit messages
COMMITS=$(gh api repos/owner/repo/compare/v1.0.0...HEAD --jq '.commits[].commit.message')

# Generate categorized changelog
CHANGELOG=$(npx ruv-swarm github changelog \
  --prs "$PRS" \
  --commits "$COMMITS" \
  --contributors "$CONTRIBUTORS" \
  --from v1.0.0 \
  --to HEAD \
  --categorize \
  --add-migration-guide)

echo "$CHANGELOG" > CHANGELOG.md
```

### 3. Create Release with Assets

```bash
# Generate changelog from PRs and commits
CHANGELOG=$(gh api repos/owner/repo/compare/${LAST_TAG}...HEAD \
  --jq '.commits[].commit.message' | \
  npx ruv-swarm github generate-changelog)

# Create release draft
gh release create v2.0.0 \
  --draft \
  --title "Release v2.0.0" \
  --notes "$CHANGELOG" \
  --target main

# Build and upload assets
npm run build
gh release upload v2.0.0 dist/*.tar.gz dist/*.zip

# Publish release
gh release edit v2.0.0 --draft=false

# Create announcement issue
gh issue create \
  --title "Released v2.0.0" \
  --body "$CHANGELOG" \
  --label "announcement,release"
```

### 4. Initialize Release Swarm

```javascript
// Initialize release swarm
mcp__claude-flow__swarm_init({ topology: "hierarchical", maxAgents: 6 })
mcp__claude-flow__agent_spawn({ type: "coordinator", name: "Release Director" })
mcp__claude-flow__agent_spawn({ type: "coder", name: "Changelog Agent" })
mcp__claude-flow__agent_spawn({ type: "analyst", name: "Version Agent" })
mcp__claude-flow__agent_spawn({ type: "coder", name: "Build Agent" })
mcp__claude-flow__agent_spawn({ type: "tester", name: "Test Agent" })
mcp__claude-flow__agent_spawn({ type: "specialist", name: "Deploy Agent" })

// Orchestrate release
mcp__claude-flow__task_orchestrate({
    task: "Complete release v2.0.0 with changelog, build, test, and deploy",
    strategy: "sequential",
    priority: "critical"
})
```

### 5. Multi-Repo Release

```bash
# Coordinate releases across repos
REPOS=("frontend:v2.0.0" "backend:v2.1.0" "cli:v1.5.0")

for entry in "${REPOS[@]}"; do
  IFS=':' read -r repo version <<< "$entry"

  # Create release in each repo
  gh release create "$version" \
    --repo "org/$repo" \
    --title "Release $version" \
    --generate-notes

  echo "Released $repo $version"
done

# Link releases
npx ruv-swarm github multi-release-link \
  --releases "${REPOS[@]}" \
  --create-summary
```

## Release Configuration

```yaml
# .github/release-swarm.yml
version: 1
release:
  versioning:
    strategy: semantic
    breaking-keywords: ["BREAKING", "!"]

  changelog:
    sections:
      - title: "Features"
        labels: ["feature", "enhancement"]
      - title: "Bug Fixes"
        labels: ["bug", "fix"]
      - title: "Documentation"
        labels: ["docs", "documentation"]

  artifacts:
    - name: npm-package
      build: npm run build
      publish: npm publish

    - name: docker-image
      build: docker build -t app:$VERSION .
      publish: docker push app:$VERSION

    - name: binaries
      build: ./scripts/build-binaries.sh
      upload: github-release

  deployment:
    environments:
      - name: staging
        auto-deploy: true
        validation: npm run test:e2e

      - name: production
        approval-required: true
        rollback-enabled: true

  notifications:
    - slack: releases-channel
    - email: stakeholders@company.com
```

## Progressive Deployment

```yaml
# Staged rollout configuration
deployment:
  strategy: progressive
  stages:
    - name: canary
      percentage: 5
      duration: 1h
      metrics:
        - error-rate < 0.1%
        - latency-p99 < 200ms

    - name: partial
      percentage: 25
      duration: 4h
      validation: automated-tests

    - name: full
      percentage: 100
      approval: required
```

## MCP Tool Integration

### Swarm Coordination

```javascript
mcp__claude-flow__swarm_init({
    topology: "hierarchical",
    maxAgents: 6,
    strategy: "sequential"
})

mcp__claude-flow__parallel_execute({
    tasks: [
        { task: "generate-changelog", agent: "changelog-agent" },
        { task: "build-artifacts", agent: "build-agent" },
        { task: "run-tests", agent: "test-agent" }
    ]
})

mcp__claude-flow__load_balance({
    swarmId: "release-swarm",
    tasks: ["build-linux", "build-macos", "build-windows"]
})
```

### Memory for Release State

```javascript
mcp__claude-flow__memory_usage({
    action: "store",
    key: "release/v2.0.0/state",
    value: JSON.stringify({
        stage: "testing",
        changelog: "generated",
        artifacts: ["npm", "docker"],
        tests: "running"
    })
})
```

## GitHub Actions Workflow

```yaml
name: Release Workflow
on:
  push:
    tags: ['v*']

jobs:
  release-swarm:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Setup GitHub CLI
        run: echo "${{ secrets.GITHUB_TOKEN }}" | gh auth login --with-token

      - name: Initialize Release Swarm
        run: |
          RELEASE_TAG=${{ github.ref_name }}
          PREV_TAG=$(gh release list --limit 2 --json tagName -q '.[1].tagName')

          PRS=$(gh pr list --state merged --base main --json number,title,labels,author \
            --search "merged:>=$(gh release view $PREV_TAG --json publishedAt -q .publishedAt)")

          npx ruv-swarm github release-init \
            --tag $RELEASE_TAG \
            --previous-tag $PREV_TAG \
            --prs "$PRS" \
            --spawn-agents "changelog,version,build,test,deploy"

      - name: Generate Release Assets
        run: |
          CHANGELOG=$(npx ruv-swarm github release-changelog --format markdown)
          gh release edit ${{ github.ref_name }} --notes "$CHANGELOG"

          npm run build
          for file in dist/*; do
            gh release upload ${{ github.ref_name }} "$file"
          done

      - name: Publish Release
        run: |
          npm publish
          gh issue create \
            --title "Released ${{ github.ref_name }}" \
            --body "Release notes at releases page" \
            --label "announcement"
```

## Emergency Procedures

### Hotfix Process

```bash
# Emergency hotfix
npx ruv-swarm github emergency-release \
  --severity critical \
  --bypass-checks security-only \
  --fast-track \
  --notify-all
```

### Rollback Procedure

```bash
# Immediate rollback
npx ruv-swarm github rollback \
  --to-version v1.9.9 \
  --reason "Critical bug in v2.0.0" \
  --preserve-data \
  --notify-users
```

## Best Practices

### 1. Release Planning
- Regular release cycles
- Feature freeze periods
- Beta testing phases
- Clear communication

### 2. Automation
- Comprehensive CI/CD
- Automated testing
- Progressive rollouts
- Monitoring and alerts

### 3. Documentation
- Up-to-date changelogs
- Migration guides
- API documentation
- Example updates

---

## Version History

- **1.0.0** (2025-01-02): Initial release - converted from release-swarm agent
