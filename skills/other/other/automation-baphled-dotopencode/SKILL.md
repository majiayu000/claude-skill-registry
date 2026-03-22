---
name: automation
description: Eliminate repetitive tasks, build CI/CD pipelines, and create self-maintaining systems
category: DevOps Operations
---

# Skill: automation

## What I do

I eliminate repetitive manual tasks through scripting, CI/CD pipelines, and self-maintaining systems. I focus on identifying automation opportunities, building reliable workflows, and creating systems that reduce toil and human error.

## When to use me

- Performing the same task more than twice.
- Manual processes prone to human error or inconsistency.
- Time-consuming repetitive operations (deployments, backups, reports).
- Implementing code quality checks, security scans, and dependency updates.
- Infrastructure provisioning and environment setup.

## Core principles

1. **Automate the Pain** - Prioritise tasks that cause the most friction or consume the most time.
2. **Idempotency** - Automation must produce the same result regardless of how many times it runs.
3. **Fail Loudly** - Failures must be obvious and actionable; silent failures are dangerous.
4. **Reliability** - Include error handling, retries, and clear failure modes.
5. **Documentation as Code** - Scripts and pipelines are the source of truth for processes.

## Patterns & examples

**Pattern: Pre-commit Hook (Git)**

```bash
#!/bin/bash
set -e
echo "Running pre-commit checks..."
make fmt
make lint
make test-unit
gitleaks detect --no-git --verbose # Secret scanning
echo "All checks passed!"
```

**Pattern: Automated Release (GitHub Actions)**

```yaml
name: Automated Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: make test
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          body: "Release notes generated from commits"
          files: bin/myapp-*
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

**Pattern: Self-Healing Kubernetes Liveness Probe**

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
  failureThreshold: 3
restartPolicy: Always
```

## Anti-patterns

- ❌ **Over-Automation** - Automating simple one-off tasks that take more time to automate than to do.
- ❌ **Fragile Scripts** - Missing error handling (`set -e`) or failing on unexpected but valid inputs.
- ❌ **Hidden Automation** - Scripts that run without team awareness or logging.
- ❌ **No Rollback** - Automation that cannot be undone or reverted safely.
- ❌ **Automation Drift** - Scripts that work locally but fail in CI/CD environments.


## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/DevOps-Operations/Automation.md`

## Related skills

- `devops` - CI/CD and operational excellence.
- `scripter` - Writing robust shell/Python scripts.
- `monitoring` - Automated health checks and alerting.
- `github-expert` - Advanced workflow automation.

