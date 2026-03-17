---
name: sast-runner
description: Runs Static Application Security Testing (SAST) using Semgrep. Scans source code for vulnerabilities, security anti-patterns, and OWASP Top 10 issues. Use when user asks to "run SAST", "scan for vulnerabilities", "static analysis", "code security scan", "静的解析", "脆弱性スキャン".
---

# SAST Runner

Wrapper for Semgrep to perform Static Application Security Testing.

## Prerequisites

Semgrep must be installed:
```bash
# pip
pip install semgrep

# macOS
brew install semgrep

# Docker
docker pull semgrep/semgrep
```

## Usage

```bash
# Scan current directory with auto config
npx sast-runner .

# Scan with specific ruleset
npx sast-runner . --config security-audit

# Scan with JSON output
npx sast-runner . --json

# Available rulesets
npx sast-runner --list-configs

# Check if semgrep is installed
npx sast-runner --check
```

## Rulesets

| Config | Description |
|--------|-------------|
| auto | Auto-detect languages and apply relevant rules |
| security-audit | Comprehensive security audit |
| owasp-top-ten | OWASP Top 10 focused |
| cwe-top-25 | CWE/SANS Top 25 |
| default | Default ruleset |

## Output Format

```json
{
  "tool": "semgrep",
  "scanPath": ".",
  "findings": [
    {
      "id": "javascript.express.security.audit.xss.mustache-escape",
      "severity": "high",
      "message": "Potential XSS vulnerability",
      "file": "src/app.js",
      "line": 42,
      "code": "res.send(userInput)",
      "cwes": ["CWE-79"],
      "owasp": ["A03:2021"],
      "fix": "Use proper output encoding"
    }
  ],
  "summary": {
    "total": 1,
    "critical": 0,
    "high": 1,
    "medium": 0,
    "low": 0
  }
}
```

## Exit Codes

- `0`: No issues found
- `1`: Issues detected
- `2`: Tool not installed or error

## CWE Coverage

Common vulnerabilities detected:
- CWE-89: SQL Injection
- CWE-79: Cross-site Scripting (XSS)
- CWE-78: OS Command Injection
- CWE-94: Code Injection
- CWE-22: Path Traversal
- CWE-502: Deserialization of Untrusted Data
- CWE-200: Exposure of Sensitive Information

## Supported Languages

JavaScript, TypeScript, Python, Go, Java, Ruby, PHP, C, C++, Rust, Kotlin, Swift, and more.
