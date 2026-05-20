---
name: security-scan
description: Main security scanning orchestration. Detects language, runs OWASP Top 10 patterns, identifies vulnerabilities, generates structured reports. Use when scanning for XSS, SQL injection, command injection, secrets, or any security vulnerability.
argument-hint: "[--full] [path]"
user-invocable: true
---

# Security Scan Skill

## Overview

Orchestrates the full security scanning workflow across all supported languages.

## Supported Languages

| Language | Marker Files | Pattern Count |
|----------|-------------|---------------|
| JavaScript/TypeScript | package.json | 25+ |
| PHP | composer.json | 20+ |
| Python | requirements.txt, pyproject.toml | 18+ |
| Swift/iOS | Package.swift, *.xcodeproj | 15+ |
| Go | go.mod | 12+ |
| Rust | Cargo.toml | 10+ |

## Workflow

1. **Detect** language from project markers
2. **Load** patterns from `references/scan-patterns.md`
3. **Run** `scripts/security-scan.sh` for automated scanning
4. **Map** findings to OWASP categories via `references/owasp-top10.md`
5. **Generate** report using `references/templates/scan-report.md`

## Pattern Categories

- XSS (Cross-Site Scripting)
- SQL Injection
- Command Injection
- Code Execution (eval, exec)
- SSRF (Server-Side Request Forgery)
- Weak Cryptography
- Hardcoded Secrets
- Insecure Deserialization
- Path Traversal / LFI / RFI

## Integration

After scanning, delegate fixes to sniper:
```
Task(subagent_type: "fuse-ai-pilot:sniper")
Prompt: "Security fixes: [FILE:LINE] [VULN] [FIX]"
```

## References

- [OWASP Top 10 Mapping](references/owasp-top10.md)
- [Scan Patterns by Language](references/scan-patterns.md)
- [Report Template](references/templates/scan-report.md)
