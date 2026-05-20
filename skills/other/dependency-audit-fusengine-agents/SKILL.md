---
name: dependency-audit
description: Audit project dependencies for known vulnerabilities using ecosystem-specific tools (npm audit, composer audit, pip-audit, cargo audit, etc).
argument-hint: "[--fix] [ecosystem]"
user-invocable: true
---

# Dependency Audit Skill

## Overview

Run dependency vulnerability checks using native package manager audit tools.

## Supported Ecosystems

| Ecosystem | Tool | Auto-fix |
|-----------|------|----------|
| npm/yarn/pnpm/bun | `npm audit` / `yarn audit` | Yes |
| PHP/Composer | `composer audit` | Manual |
| Python/pip | `pip-audit` / `safety check` | Manual |
| Rust/Cargo | `cargo audit` | Yes |
| Go | `govulncheck ./...` | Manual |
| Swift/CocoaPods | `pod audit` | Manual |
| Ruby/Bundler | `bundle audit` | Manual |

## Workflow

1. **Detect** package manager from lock files
2. **Run** appropriate audit command
3. **Parse** output for vulnerabilities
4. **Classify** by severity (CRITICAL/HIGH/MEDIUM/LOW)
5. **Suggest** fix versions or alternatives

## Auto-Fix Support

When `--fix` flag is used:
- `npm audit fix` for safe updates
- `cargo audit fix` for Rust
- Manual guidance for other ecosystems

## References

- [Audit Commands](references/audit-commands.md)
- [Report Template](references/templates/audit-report.md)
