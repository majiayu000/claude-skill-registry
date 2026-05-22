---
name: config-hardening
description: Harden configuration and defaults for safer deployment. Use when a mid-level developer needs to reduce misconfig risks.
---

# Config Hardening

## Purpose
Harden configuration and defaults for safer deployment.

## Inputs to request
- Current configuration defaults.
- Environment and deployment model.
- Security requirements and threat model.

## Workflow
1. Audit environment variables and defaults.
2. Recommend safer defaults and validation.
3. Identify secrets and rotate if exposed.

## Output
- Config hardening checklist.

## Quality bar
- Avoid breaking changes without migration notes.
- Call out secret handling explicitly.
