---
name: security-scan
description: >
  Orchestrates SAST, dependency audit, and secrets detection using self-hosted tools
  (Semgrep, Bandit, pip-audit, Trivy, gitleaks). Integrates with task-monitor and memory.
allowed-tools:
  - run_command
  - read_file
triggers:
  - security scan
  - security-scan
  - sast
  - vulnerability scan
  - secrets detection
  - dependency audit
metadata:
  short-description: Security scanning orchestrator (SAST, deps, secrets)

provides:
  - security-scan
composes: [, task-monitor]
---

# Security-Scan: Self-Hosted Security Scanning

Orchestrate comprehensive security scanning using self-hosted tools.

## Features

1. **SAST (Static Application Security Testing)**
   - Semgrep: Multi-language pattern matching
   - Bandit: Python-specific security linting

2. **Dependency Audit**
   - pip-audit: Python package vulnerabilities
   - npm audit: Node.js package vulnerabilities (auto-detected)
   - Trivy: Container and filesystem scanning

3. **Secrets Detection**
   - gitleaks: Find hardcoded credentials, API keys, tokens

4. **Integrations**
   - Task-monitor: Real-time progress tracking
   - Memory: Store and recall scan results across sessions

## Commands

| Command | Description |
|---------|-------------|
| `./run.sh scan --path .` | Run all security scans |
| `./run.sh sast --path . --language python` | Run SAST only |
| `./run.sh deps --path .` | Run dependency audit only |
| `./run.sh secrets --path .` | Run secrets detection only |
| `./run.sh report --format json` | Generate scan report |

## Usage

```bash
# Full security scan
./run.sh scan --path /path/to/project

# SAST scan for Python
./run.sh sast --path . --language python

# Dependency audit
./run.sh deps --path .

# Secrets detection
./run.sh secrets --path .

# Store results in memory
./run.sh scan --path . --store-results
```

## Output Format

All commands output structured JSON with:
- `findings`: List of security issues
- `severity`: critical/high/medium/low/info
- `location`: File path and line number
- `rule_id`: Scanner rule that triggered
- `description`: Human-readable description
- `remediation`: Suggested fix

## Required Tools

| Tool | Purpose | Install |
|------|---------|---------|
| semgrep | SAST | `pip install semgrep` |
| bandit | Python SAST | `pip install bandit` |
| pip-audit | Python deps | `pip install pip-audit` |
| gitleaks | Secrets | Binary from GitHub releases |
| trivy | Container scan | Binary from GitHub releases |

## Integration with Task-Monitor

Scans automatically register with task-monitor for progress tracking:

```bash
# View scan progress
.pi/skills/task-monitor/run.sh tui --filter security-scan
```

## Integration with Memory

Store scan results for trend analysis:

```bash
# Store results
./run.sh scan --path . --store-results

# Recall previous scans
.pi/skills/memory/run.sh recall "security scan results"
```
