---
name: "security-best-practices"
description: "Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests security best practices guidance, a security review/report, or secure-by-default coding help. Trigger only for supported languages (python, javascript/typescript, go). Do not trigger for general code review, debugging, or non-security tasks."
---

# Security Best Practices

## Overview

Identify in-scope languages/frameworks, load matching guidance from `references/`, and apply it to:
- write secure-by-default code,
- flag critical issues during normal work,
- produce a prioritized security report when requested.

## Workflow

1. Identify all in-scope languages/frameworks (frontend and backend where applicable).
2. Load all matching `references/` files:
   - `<language>-<framework>-<stack>-security.md`
   - `<language>-general-<stack>-security.md` when present.
3. For full-stack web work, cover both frontend and backend.
4. If frontend framework is unspecified, also load `javascript-general-web-frontend-security.md`.
5. If no matching references exist, use established best practices; if uncertain, research recent authoritative sources.

### Modes

1. **Default mode**: apply guidance while implementing code.
2. **Passive mode**: flag high-impact vulnerabilities/security regressions while working.
3. **Report mode**: when asked for review/report/security hardening, produce a full prioritized report, then offer fixes.

## Workflow Decision Tree

- Language/framework unclear: inspect repo, list evidence.
- Matching references exist: load only relevant files and follow them.
- No references: use established best practices; if user requested a report, state that concrete local guidance was unavailable.

# Overrides

Project constraints can require exceptions. Follow project docs/prompts when they explicitly override a best practice. You may report the deviation, but do not block progress. Recommend documenting the rationale for future consistency.

# Report Format

When asked for a report:
- Write Markdown to `security_best_practices_report.md` unless user specifies another path.
- Include a short executive summary.
- Group findings by severity/urgency.
- Assign numeric IDs to all findings.
- For critical findings, include a one-sentence impact statement.
- Include precise code references with line numbers.
- After writing, summarize findings in chat and state the report path.

# Fixes

- After report delivery, ask user whether to proceed with fixes.
- If passive mode finds a critical issue, notify user and ask whether to fix it.
- Fix one finding at a time.
- Keep comments concise and rationale-focused.
- Preserve functionality; evaluate regression risk and second-order effects.
- Follow project commit/change flow; if committing, use clear security-focused messages.
- Follow project test flow before finalizing fixes.

# General Security Advice

### Public IDs

Do not expose small auto-incrementing IDs for internet-facing resources. Prefer UUIDv4 or long random IDs.

### TLS

Do not report missing TLS as a blanket issue in local/dev contexts. Secure cookies require TLS and can break non-TLS local deployments. Prefer environment-gated secure-cookie behavior for production TLS. Avoid recommending HSTS unless the team fully understands operational lock-in and outage risk.
