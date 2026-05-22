---
name: security-bluebook-builder
description: Create or refine a concise, normative security policy ("Blue Book") for sensitive applications. Use when users need a threat model, data classification rules, auth/session policy, logging and audit requirements, retention/deletion expectations, incident response, or security gates for apps handling PII/PHI/financial data.
---

# Security Bluebook Builder

## When to use this skill
Build a minimal but real security policy for sensitive apps. The output is a single, coherent Blue Book document using MUST/SHOULD/CAN language, with explicit assumptions, scope, and security gates.

## Workflow

### 1) Gather inputs (ask only if missing)
Collect just enough context to fill the template. If the user has not provided details, ask up to 6 short questions:
- What data classes are handled (PII, PHI, financial, tokens, content)?
- What are the trust boundaries (client/server/third parties)?
- How do users authenticate (OAuth, email/password, SSO, device sessions)?
- What storage is used (DB, object storage, logs, analytics)?
- What connectors or third parties are used?
- Retention and deletion expectations (default + user-initiated)?

If the user cannot answer, proceed with safe defaults and mark TODOs.

### 2) Draft the Blue Book
Load `references/bluebook_template.md` and fill it with the provided details. Keep it concise, deterministic, and enforceable.

### 3) Enforce guardrails
- Do not include secrets, tokens, or internal credentials.
- If something is unknown, write "TODO" plus a clear assumption.
- Fail closed: if a capability is required but unavailable, call it out explicitly.
- Keep scope minimal; do not add features or tools beyond what the user asked for.

### 4) Quality checks
Confirm the Blue Book includes:
- Threat model (assumptions + out-of-scope)
- Data classification + handling rules
- Trust boundaries + controls
- Auth/session policy
- Token handling policy
- Logging/audit policy
- Retention/deletion
- Incident response mini-runbook
- Security gates + go/no-go checklist

## Resources
- `references/bluebook_template.md`

## How to use this skill

Refer to the instructions above or standard agent usage for this skill type.
