---
name: dependency-analysis
description: Analyze project dependencies for security vulnerabilities, outdated
  packages, and upgrade paths. Use when auditing dependencies or planning upgrades.
---

# Dependency Analysis Skill

## Purpose
Systematic analysis of project dependencies for security and maintenance.

## When to Use
- Security audits
- Before adding new dependencies
- Planning version upgrades
- Regular maintenance checks

## Analysis Process

### Step 1: Identify Package Manager
Detect from files:
- `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` → Node.js
- `requirements.txt` / `Pipfile.lock` / `poetry.lock` → Python
- `go.sum` → Go

### Step 2: Run Security Audit
Execute appropriate command:
```bash
# Node.js
npm audit --json || yarn audit --json

# Python (if pip-audit installed)
pip-audit --format json

# Go
govulncheck ./...
```

### Step 3: Check Outdated
```bash
# Node.js
npm outdated --json

# Python
pip list --outdated --format json

# Go
go list -u -m all
```

### Step 4: Analyze Results
Categorize findings:
- **Critical**: Security vulnerabilities with known exploits
- **High**: Security issues or major version behind
- **Medium**: Minor version behind or deprecated
- **Low**: Patch version behind

## Output Format
Use [templates/dep-report.md](templates/dep-report.md)

## Storage Location
Save to: `docs/research/dependency-audit-{date}.md`
