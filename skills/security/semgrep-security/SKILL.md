---
name: semgrep-security
description: Semgrep code security scanning and SAST analysis
allowed-tools: [Bash, Read, Glob]
---

# Semgrep Security Skill

## Overview

Static Application Security Testing (SAST) with Semgrep. 90%+ context savings.

## Requirements

- Semgrep CLI installed
- Optional: SEMGREP_APP_TOKEN for cloud features

## Tools (Progressive Disclosure)

### Scanning

| Tool      | Description             |
| --------- | ----------------------- |
| scan      | Run security scan       |
| scan-ci   | CI-optimized scan       |
| scan-diff | Scan only changed files |

### Rules

| Tool       | Description          |
| ---------- | -------------------- |
| list-rules | List available rules |
| rule-info  | Get rule details     |
| test-rule  | Test custom rule     |

### Results

| Tool         | Description         |
| ------------ | ------------------- |
| findings     | List scan findings  |
| sarif-export | Export SARIF format |
| json-export  | Export JSON format  |

### Severity Categories

- **ERROR**: Critical security issues
- **WARNING**: Medium severity
- **INFO**: Low severity/best practices

## Agent Integration

- **security-architect** (primary): Security review
- **qa** (primary): Quality gates
- **code-reviewer** (secondary): PR scanning

## Common Rulesets

- p/default (general security)
- p/owasp-top-ten
- p/javascript
- p/typescript
- p/python
- p/secrets (credential detection)
