---
name: security-check
version: "1.0"
description: Scan Python projects for credential leaks, secrets in code, insecure patterns, LLM API key exposure, PII leakage to external AI services, and .env/.gitignore misconfigurations. Focused on data science pipelines handling API keys, tokens, and LLM integrations.
---

# Security Check Skill

Scan for credential leaks, insecure code patterns, and LLM security issues in Python data science projects.

## When to Activate

- Before committing changes
- After modifying `.env`, `.gitignore`, or config files
- When adding new API integrations or credentials
- When reviewing code that handles tokens, keys, or passwords
- When code sends data to external LLM APIs (Gemini, OpenAI, etc.)
- Periodic security hygiene checks

## Check Process

Read `skills/scan-process.md` for the full 6-step scan process with bash commands.

## Pattern Reference

Read `skills/pattern-tables.md` for API key regex patterns, insecure Python code patterns, and LLM-specific security patterns with severity classifications.

## Behavioral Rules

Read `guidelines.md` for severity classifications, remediation requirements, and escalation rules.
