---
name: github-code-review
version: 1.0.0
description: Comprehensive GitHub code review with AI-powered swarm coordination
category: github
tags: [code-review, github, swarm, pr-management, automation]
author: Claude Code Flow
requires:
  - github-cli
  - ruv-swarm
  - claude-flow
capabilities:
  - Multi-agent code review
  - Automated PR management
  - Security and performance analysis
  - Swarm-based review orchestration
  - Intelligent comment generation
  - Quality gate enforcement
---

# GitHub Code Review Skill

> **AI-Powered Code Review**: Deploy specialized review agents to perform comprehensive, intelligent code reviews that go beyond traditional static analysis.

## Behavioral Classification

**Type**: Autonomous Execution

This skill executes code reviews automatically when invoked. When triggered:
1. Swarm initializes with appropriate agents
2. Reviews execute in parallel
3. Results are posted to PR
4. Quality gates are enforced

---

## Quick Start

### Simple Review
```bash
# Initialize review swarm for PR
gh pr view 123 --json files,diff | npx ruv-swarm github review-init --pr 123

# Post review status
gh pr comment 123 --body "🔍 Multi-agent code review initiated"
```

### Complete Review Workflow
```bash
# Get PR context with gh CLI
PR_DATA=$(gh pr view 123 --json files,additions,deletions,title,body)
PR_DIFF=$(gh pr diff 123)

# Initialize comprehensive review
npx ruv-swarm github review-init \
  --pr 123 \
  --pr-data "$PR_DATA" \
  --diff "$PR_DIFF" \
  --agents "security,performance,style,architecture,accessibility" \
  --depth comprehensive
```

---

## Sub-Documentation

For detailed information, see the following files:

| Document | Contents |
|----------|----------|
| [Agents](./agents.md) | Security, performance, architecture, style review agents |
| [Workflows](./workflows.md) | PR-based swarm management, CI/CD integration, automation |
| [Quality Gates](./quality-gates.md) | Status checks, thresholds, metrics tracking |
| [Troubleshooting](./troubleshooting.md) | Common issues and solutions |

---

## Quick Reference

### Specialized Review Agents

| Agent | Focus | Command Flag |
|-------|-------|--------------|
| **Security** | Vulnerabilities, secrets, auth | `--agents security` |
| **Performance** | Complexity, queries, memory | `--agents performance` |
| **Architecture** | Patterns, coupling, SOLID | `--agents architecture` |
| **Style** | Formatting, naming, docs | `--agents style` |
| **Accessibility** | WCAG, screen readers, contrast | `--agents accessibility` |

### PR Comment Commands

Execute from PR comments:
```markdown
/swarm init mesh 6
/swarm spawn coder "Implement authentication"
/swarm spawn tester "Write unit tests"
/swarm status
/swarm review --agents security,performance
```

### Label-Based Agent Assignment

```json
{
  "label-mapping": {
    "bug": ["debugger", "tester"],
    "feature": ["architect", "coder", "tester"],
    "refactor": ["analyst", "coder"],
    "security": ["security", "authentication", "audit"]
  }
}
```

### Topology by PR Size

| PR Size | Lines Changed | Topology |
|---------|---------------|----------|
| Small | < 100 | ring |
| Medium | 100-500 | mesh |
| Large | > 500 | hierarchical |

### Quality Gate Thresholds

```bash
npx ruv-swarm github quality-gates \
  --define '{
    "security": {"threshold": "no-critical"},
    "performance": {"regression": "<5%"},
    "coverage": {"minimum": "80%"},
    "architecture": {"complexity": "<10"},
    "duplication": {"maximum": "5%"}
  }'
```

---

## Configuration

### Review Configuration File

```yaml
# .github/review-swarm.yml
version: 1
review:
  auto-trigger: true
  required-agents:
    - security
    - performance
    - style
  optional-agents:
    - architecture
    - accessibility

  thresholds:
    security: block      # Block merge on security issues
    performance: warn    # Warn on performance issues
    style: suggest       # Suggest style improvements
```

---

## Example Workflows

### Security-Critical PR
```bash
npx ruv-swarm github review-init \
  --pr 456 \
  --agents "security,authentication,audit" \
  --depth "maximum" \
  --require-security-approval
```

### Performance-Sensitive PR
```bash
npx ruv-swarm github review-init \
  --pr 789 \
  --agents "performance,database,caching" \
  --benchmark \
  --profile
```

### Feature Development PR
```bash
gh pr view 456 --json body,labels,files | \
  npx ruv-swarm github pr-init 456 \
    --topology hierarchical \
    --agents "architect,coder,tester,security" \
    --auto-assign-tasks
```

---

## Best Practices

### Review Configuration
- Define clear review criteria upfront
- Set appropriate severity thresholds
- Configure agent specializations for your stack

### Comment Quality
- Provide actionable, specific feedback
- Include code examples with suggestions
- Reference documentation and best practices

### Performance Optimization
- Cache analysis results to avoid redundant work
- Use incremental reviews for large PRs
- Enable parallel agent execution

---

## Security Checklist

- [ ] GitHub token scoped to repository only
- [ ] Webhook signatures verified
- [ ] Command injection protection enabled
- [ ] Rate limiting configured
- [ ] Audit logging enabled
- [ ] Secrets scanning active
- [ ] Branch protection rules enforced

---

## Related Skills

- `github-pr-manager` - Comprehensive PR lifecycle management
- `github-workflow-automation` - Automate GitHub workflows
- `swarm-coordination` - Advanced swarm orchestration

---

**Last Updated:** 2025-10-19
**Version:** 1.0.0
**Maintainer:** Claude Code Flow Team
