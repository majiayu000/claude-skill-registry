---
name: agent-shield
description: Run ecc-agentshield security scan against Claude Code configuration
disable-model-invocation: true
---

# AgentShield Security Scan

Scans `.claude/` configuration for security vulnerabilities using [ecc-agentshield](https://github.com/affaan-m/everything-claude-code).

## When to Run

- After modifying hooks, skills, or CLAUDE.md
- After adding MCP servers or updating mcp.json
- Before merging infrastructure PRs
- Periodically as part of security hygiene

## Quick Scan (Static Analysis)

Run 102 static rules against hooks, skills, CLAUDE.md, settings.json:

```bash
npx ecc-agentshield scan --path .claude/ --format markdown
```

Save results:
```bash
npx ecc-agentshield scan --path .claude/ --format markdown > .claude/phases/output/security-scan-$(date +%Y-%m-%d).md
```

## Deep Scan (3-Agent Opus Pipeline)

Requires `ANTHROPIC_API_KEY` env var. Runs red-team, blue-team, and auditor agents:

```bash
npx ecc-agentshield scan --path .claude/ --opus --stream
```

## What It Checks

| Category | Examples |
|----------|---------|
| Secrets | Hardcoded API keys in CLAUDE.md, env vars in hooks |
| Permissions | Overly broad Bash(*) allows, missing deny lists |
| Injection | Shell variable interpolation in Python heredocs, unquoted vars |
| MCP | Risky servers, npx -y auto-install, hardcoded secrets |
| Hooks | Data exfiltration, silent error suppression, command injection |

## Interpreting Results

Grades: A (90-100) through F (0-39). Focus on HIGH and CRITICAL findings first. MEDIUM findings are good improvement opportunities. LOW can be addressed opportunistically.

## After Scanning

1. Fix all CRITICAL/HIGH findings immediately
2. Create tasks for MEDIUM findings
3. Document any accepted risks in CLAUDE.md
