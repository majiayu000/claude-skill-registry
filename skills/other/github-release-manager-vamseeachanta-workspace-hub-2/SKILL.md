---
name: github-release-manager
description: Automated release coordination and deployment with swarm orchestration for seamless version management, testing, and deployment across multiple packages. Use for release pipelines, version coordination, deployment orchestration, and release documentation.
---

# GitHub Release Manager Skill

## Overview

Automated release coordination with swarm orchestration. This skill handles release pipelines, multi-package version coordination, deployment orchestration with rollback capabilities, release documentation generation, and multi-stage validation.

## Quick Start

```bash
# List releases
gh release list

# Create a release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes..."

# View release
gh release view v1.0.0

# Download release assets
gh release download v1.0.0

# Delete release
gh release delete v1.0.0 --yes
```

## When to Use

- Creating and managing software releases
- Coordinating versions across multiple packages
- Automating deployment with validation
- Generating release documentation
- Multi-stage release validation
- Rollback and recovery procedures

## Core Capabilities

| Capability | Description |
|------------|-------------|
| Automated pipelines | Comprehensive testing and validation |
| Version coordination | Multi-package version sync |
| Deployment orchestration | Staged deployment with rollback |
| Release documentation | Changelog and notes generation |
| Multi-stage validation | Swarm-coordinated testing |

## Usage Examples

### 1. Coordinated Release Preparation

```javascript
// Initialize release management swarm

// Orchestrate release preparation
    task: "Prepare release v1.0.72 with comprehensive testing and validation",
    strategy: "sequential",
    priority: "critical"
})
```

### 2. Create Release with gh CLI

```bash
# Create release branch
git checkout -b release/v1.0.72 main

# Get commits since last release
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')
COMMITS=$(gh api repos/owner/repo/compare/${LAST_TAG}...HEAD --jq '.commits[].commit.message')

# Generate changelog
echo "$COMMITS" > CHANGELOG_DRAFT.md

# Create draft release
gh release create v1.0.72 \
  --draft \
  --title "Release v1.0.72" \
  --notes-file CHANGELOG_DRAFT.md \
  --target release/v1.0.72

# Upload assets
gh release upload v1.0.72 dist/*.tar.gz dist/*.zip

# Publish release
gh release edit v1.0.72 --draft=false
```

### 3. Multi-Package Version Coordination

```bash
# Update package versions
cd ../ruv-swarm && npm version 1.0.12 --no-git-tag-version

# Run tests for all packages
npm test --workspaces

# Create coordinated release PR
gh pr create \
  --title "Release v1.0.72: GitHub Integration and Swarm Enhancements" \
  --head release/v1.0.72 \
  --base main \
  --body "## Release v1.0.72

### Package Updates
- **ruv-swarm**: v1.0.11 -> v1.0.12

### Changes
- GitHub workflow integration
- Enhanced swarm coordination
- Advanced MCP tools integration

### Validation
- [x] Unit tests passing
- [x] Integration tests: 89% success
- [x] Build verification successful"
```

### 4. Automated Release Validation

```bash
# Run comprehensive validation
npm install && npm test && npm run lint && npm run build

# Security audit
npm audit

# Create validation report
gh issue create \
  --title "Release Validation: v1.0.72" \
  --body "## Validation Results
- Unit tests: PASS
- Integration tests: 89% success
- Lint: PASS
- Build: PASS
- Security: No vulnerabilities" \
  --label "release,validation"
```

### 5. Batch Release Workflow

```javascript
[Single Message - Complete Release Management]:
    // Initialize comprehensive release swarm

    // Create release branch
    Bash("git checkout -b release/v1.0.72 main")

    // Run comprehensive validation
    Bash("npm install && npm test && npm run lint && npm run build")

    // Create release PR
    Bash(`gh pr create \
      --title "Release v1.0.72" \
      --head "release/v1.0.72" \
      --base "main" \
      --body "[release description]"`)

    // Track release progress
    TodoWrite({ todos: [
      { id: "rel-prep", content: "Prepare release branch", status: "completed" },
      { id: "rel-test", content: "Run comprehensive tests", status: "completed" },
      { id: "rel-pr", content: "Create release PR", status: "completed" },
      { id: "rel-review", content: "Code review and approval", status: "pending" },
      { id: "rel-merge", content: "Merge and deploy", status: "pending" }
    ]})

    // Store release state
        action: "store",
        key: "release/v1.0.72/status",
        value: JSON.stringify({
            version: "1.0.72",
            stage: "validation_complete",
            validation_passed: true
        })
    })
```

## Release Strategies

### Semantic Versioning

```javascript
const versionStrategy = {
    major: "Breaking changes or architecture overhauls",
    minor: "New features, GitHub integration, swarm enhancements",
    patch: "Bug fixes, documentation updates, dependency updates",
    coordination: "Cross-package version alignment"
}
```

### Multi-Stage Validation

```javascript
const validationStages = [
    "unit_tests",           // Individual package testing
    "integration_tests",    // Cross-package integration
    "performance_tests",    // Performance regression detection
    "compatibility_tests",  // Version compatibility validation
    "documentation_tests",  // Documentation accuracy verification
    "deployment_tests"      // Deployment simulation
]
```

### Rollback Strategy

```javascript
const rollbackPlan = {
    triggers: ["test_failures", "deployment_issues", "critical_bugs"],
    automatic: ["failed_tests", "build_failures"],
    manual: ["user_reported_issues", "performance_degradation"],
    recovery: "Previous stable version restoration"
}
```

## MCP Tool Integration

### Swarm Coordination

```javascript
    topology: "hierarchical",
    maxAgents: 6,
    strategy: "sequential"  // Release stages run in order
})
```

### Memory for Release State

```javascript
// Store release state
    action: "store",
    key: "release/v1.0.72/state",
    namespace: "releases",
    value: JSON.stringify({
        version: "1.0.72",
        stage: "testing",
        timestamp: Date.now()
    })
})
```

## GitHub Actions Integration

```yaml
name: Release Management
on:
  pull_request:
    branches: [main]
    paths: ['**/package.json', 'CHANGELOG.md']

jobs:
  release-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install and Test
        run: |
          npm install
          npm test
          npm run lint
          npm run build
      - name: Validate Release
```

## Best Practices

### 1. Comprehensive Testing
- Multi-package test coordination
- Integration test validation
- Performance regression detection
- Security vulnerability scanning

### 2. Documentation Management
- Automated changelog generation
- Release notes with detailed changes
- Migration guides for breaking changes
- API documentation updates

### 3. Deployment Coordination
- Staged deployment with validation
- Rollback mechanisms and procedures
- Performance monitoring during deployment
- User communication and notifications

### 4. Version Management
- Semantic versioning compliance
- Cross-package version coordination
- Dependency compatibility validation
- Breaking change documentation

## Monitoring and Metrics

### Release Quality Metrics
- Test coverage percentage
- Integration success rate
- Deployment time metrics
- Rollback frequency

### Automated Monitoring
- Performance regression detection
- Error rate monitoring
- User adoption metrics
- Feedback collection and analysis

---

## Version History

- **1.0.0** (2025-01-02): Initial release - converted from release-manager agent
