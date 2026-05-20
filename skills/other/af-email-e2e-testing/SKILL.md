---
name: af-email-e2e-testing
description: Test email flows in E2E tests including signup verification, password reset, and invitation emails. Uses Gmail API with service account for test email verification. Use when testing any feature that sends or verifies emails.

# AgentFlow documentation fields
title: Email E2E Testing (Entry Point)
created: 2026-02-06
updated: 2026-02-06
last_checked: 2026-02-06
tags: [skill, entry-point, testing, email, gmail, e2e, verification]
parent: ../README.md
related:
  - ../af-testing-expertise/SKILL.md
  - ../../docs/guides/testing-guide.md
---

# Email E2E Testing

## What to read

**Gmail API verification workflow, credentials, and helper patterns:**
→ [af-testing-expertise/SKILL.md](../af-testing-expertise/SKILL.md) — see "Workflow: Email Verification in E2E Tests"

**E2E infrastructure requirements (SES, Cognito email config):**
→ [testing-guide.md#e2e-infrastructure-requirements](../../docs/guides/testing-guide.md#e2e-infrastructure-requirements)

**E2E-ready authentication checklist:**
→ [testing-guide.md#e2e-ready-authentication-checklist](../../docs/guides/testing-guide.md#e2e-ready-authentication-checklist)

**Common pitfalls (Gmail search queries, email URL extraction):**
→ [af-testing-expertise/SKILL.md](../af-testing-expertise/SKILL.md) — see "Gmail Search Query Mismatch" and "Email Links Contain Production URLs"
