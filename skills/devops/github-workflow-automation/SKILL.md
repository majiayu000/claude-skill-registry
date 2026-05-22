---
name: github-workflow-automation
version: 1.1.0
category: github
description: Advanced GitHub Actions workflow automation with AI swarm coordination
tags:
  - github
  - github-actions
  - ci-cd
  - workflow-automation
  - swarm-coordination
authors:
  - claude-flow
requires:
  - gh (GitHub CLI)
  - git
  - claude-flow@alpha
  - node (v16+)
priority: high
progressive_disclosure: true
---

# GitHub Workflow Automation

## Behavioral Classification

**Type**: Autonomous Execution

This skill executes GitHub Actions workflows and CI/CD pipelines automatically with minimal user intervention. It handles complex multi-step automation tasks independently.

**Autonomous Behaviors**:
- Generates optimized workflows from codebase analysis
- Detects languages and creates appropriate build pipelines
- Analyzes failures and suggests automatic fixes
- Coordinates multi-agent validation on PRs

---

## Quick Start

### Initialize Workflow Automation

```bash
# Generate optimized workflow from codebase analysis
npx ruv-swarm actions generate-workflow \
  --analyze-codebase \
  --detect-languages \
  --create-optimal-pipeline
```

### Common Commands

```bash
# Optimize existing workflow
npx ruv-swarm actions optimize \
  --workflow ".github/workflows/ci.yml" \
  --suggest-parallelization

# Analyze failed runs
gh run view <run-id> --json jobs,conclusion | \
  npx ruv-swarm actions analyze-failure \
    --suggest-fixes
```

---

## Sub-Documentation

| Document | Contents |
|----------|----------|
| [modes.md](./modes.md) | 8 GitHub integration modes (coordinator, pr-manager, etc.) |
| [templates.md](./templates.md) | Production-ready workflow templates |
| [advanced.md](./advanced.md) | Dynamic testing, predictive analysis, custom actions |
| [integration.md](./integration.md) | Claude-Flow swarm coordination patterns |
| [best-practices.md](./best-practices.md) | Security, performance, organization |
| [troubleshooting.md](./troubleshooting.md) | Debugging, examples, command reference |

---

## Core Capabilities

### Swarm-Powered GitHub Modes

8 specialized modes for different GitHub workflows. See [modes.md](./modes.md) for details.

| Mode | Purpose |
|------|---------|
| `gh-coordinator` | Multi-repo workflow orchestration |
| `pr-manager` | Pull request management and review |
| `issue-tracker` | Issue management and project coordination |
| `release-manager` | Release coordination and deployment |
| `repo-architect` | Repository structure optimization |
| `code-reviewer` | Automated code review and QA |
| `ci-orchestrator` | CI/CD pipeline coordination |
| `security-guardian` | Security and compliance management |

### Workflow Templates

Production-ready templates for common scenarios. See [templates.md](./templates.md).

- Intelligent CI with swarms
- Multi-language detection
- Adaptive security scanning
- Self-healing pipeline
- Progressive deployment
- Performance regression detection
- PR validation swarm
- Intelligent release

---

## Integration Checklist

```bash
# Quick setup verification
gh auth status                    # GitHub CLI authenticated
node --version                    # Node.js v16+
npx claude-flow@alpha --version   # claude-flow available
ls .github/workflows/             # Workflows directory exists
```

### Setup Script

```bash
#!/bin/bash
# Install dependencies
npm install -g claude-flow@alpha

# Verify GitHub CLI
gh auth status || gh auth login

# Create workflow directory
mkdir -p .github/workflows

# Generate initial workflow
npx ruv-swarm actions generate-workflow \
  --analyze-codebase \
  --create-optimal-pipeline > .github/workflows/ci.yml

echo "✅ GitHub workflow automation setup complete"
```

---

## Related Skills

- [github-release-management](../github-release-management/SKILL.md) - Release orchestration
- [github-code-review](../github-code-review/SKILL.md) - Code review automation
- [github-project-management](../github-project-management/SKILL.md) - Project coordination

---

## Support & Documentation

- **GitHub CLI Docs**: https://cli.github.com/manual/
- **GitHub Actions**: https://docs.github.com/en/actions
- **Claude-Flow**: https://github.com/ruvnet/claude-flow

---

## Changelog

### v1.1.0 (2026-01-24)
- Decomposed into sub-files for progressive disclosure
- Added behavioral classification (ADR-025)
- Reduced SKILL.md from 1065 to ~150 lines

### v1.0.0 (2025-01-19)
- Initial skill consolidation
- Merged workflow-automation.md and github-modes.md
- Added swarm coordination patterns
