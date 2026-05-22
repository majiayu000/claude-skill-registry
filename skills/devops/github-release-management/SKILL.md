---
name: github-release-management
title: GitHub Release Management
version: 3.0.0
description: Comprehensive GitHub release orchestration with AI swarm coordination for automated versioning, testing, deployment, and rollback management
category: github
tags:
  - release
  - deployment
  - versioning
  - automation
  - ci-cd
  - swarm
author: Claude Flow Team
difficulty: intermediate
prerequisites:
  - gh (GitHub CLI)
  - claude-flow
  - node >= 20.0.0
tools_required:
  - gh
  - npx claude-flow
  - mcp__claude-flow__*
related_skills:
  - github-pr-workflow
  - github-workflow-automation
  - multi-repo-coordination
---

# GitHub Release Management

## Behavioral Classification

**Type**: Guided Decision

This skill guides you through release management decisions and then executes based on your choices.

**Decision Points**:
1. Release type (patch, minor, major, hotfix)?
2. Deployment strategy (direct, staged, canary)?
3. Swarm topology for coordination?
4. Rollback policy?

---

## Overview

Intelligent release automation and orchestration using AI swarms for comprehensive software releases - from changelog generation to multi-platform deployment with rollback capabilities.

**Core Capabilities:**
1. **Release Planning** - Semantic versioning, breaking change detection
2. **Automated Testing** - Multi-stage test orchestration, security scanning
3. **Build & Deploy** - Multi-platform builds, progressive deployment
4. **Documentation** - Automated changelog, release notes, migration guides

---

## Quick Start

### Simple Release Flow

```bash
# Plan and create a release
gh release create v2.0.0 \
  --draft \
  --generate-notes \
  --title "Release v2.0.0"

# Orchestrate with swarm
npx claude-flow github release-create \
  --version "2.0.0" \
  --build-artifacts \
  --deploy-targets "npm,docker,github"
```

### Full Automated Release

```bash
# Initialize release swarm
npx claude-flow swarm init --topology hierarchical

# Execute complete release pipeline
npx claude-flow sparc pipeline "Release v2.0.0 with full validation"
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Basic Usage](./basics.md) | Essential commands, version bumps, simple deployment |
| [Swarm Coordination](./swarm.md) | AI swarm orchestration, specialized agents |
| [Advanced Workflows](./advanced.md) | Multi-package, staged rollout, hotfix procedures |
| [Enterprise Features](./enterprise.md) | Configuration, security, compliance, monitoring |
| [GitHub Actions](./workflows.md) | CI/CD integration, best practices |

---

## Quick Reference

### Essential Commands

```bash
# Get last release tag
LAST_TAG=$(gh release list --limit 1 --json tagName -q '.[0].tagName')

# Create draft release
gh release create v2.0.0 --draft --generate-notes

# Version bump
npm version patch  # or minor, major

# Deploy to npm
npm run build && npm publish
```

### Swarm Initialization

```javascript
mcp__claude-flow__swarm_init {
  topology: "hierarchical",
  maxAgents: 6,
  strategy: "balanced"
}
```

### Release Agent Types

| Agent | Role |
|-------|------|
| Release Director | Coordinate overall release |
| Version Manager | Handle versioning |
| QA Engineer | Run validation tests |
| Release Reviewer | Code review |
| Deployment Analyst | Monitor deployment |
| Compatibility Checker | Verify compatibility |

---

## Release Cadence Guidelines

| Type | Frequency | Contains |
|------|-----------|----------|
| Patch | Weekly | Bug fixes |
| Minor | Bi-weekly | Features |
| Major | Quarterly | Breaking changes |
| Hotfix | On-demand | Critical fixes |

---

## Performance Metrics

- **Release Planning**: < 2 minutes
- **Build Process**: 3-8 minutes
- **Test Execution**: 5-15 minutes
- **Deployment**: 2-5 minutes per target
- **Complete Pipeline**: 15-30 minutes

---

## Success Metrics

- **Release Frequency**: Target weekly minor releases
- **Lead Time**: < 2 hours from commit to production
- **Failure Rate**: < 2% of releases require rollback
- **MTTR**: < 30 minutes for critical hotfixes

---

## Related Resources

- [GitHub CLI Documentation](https://cli.github.com/manual/)
- [Semantic Versioning Spec](https://semver.org/)

---

**Version**: 3.0.0
**Last Updated**: 2025-01-24
