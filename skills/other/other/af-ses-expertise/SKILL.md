---
name: af-ses-expertise
description: Configure SES for email sending in GainInsight Standard projects. Covers domain verification with DKIM, sandbox vs production mode, and integration with Cognito and E2E testing. Use when setting up email infrastructure or debugging email delivery.

# AgentFlow documentation fields
title: SES Expertise (Entry Point)
created: 2026-02-08
updated: 2026-02-08
last_checked: 2026-02-08
tags: [skill, entry-point, ses, email, dkim, aws]
parent: ../README.md
related:
  - ../af-cognito-expertise/SKILL.md
  - ../af-environment-infrastructure/SKILL.md
  - ../../docs/guides/gaininsight-standard/auth-setup.md
---

# SES Expertise

## What to read

**Domain verification workflow (create identity, DKIM records, DNS setup):**
→ [auth-setup.md#ses-domain-verification](../../docs/guides/gaininsight-standard/auth-setup.md#ses-domain-verification)

**Sandbox vs production mode (request process, timelines, verification):**
→ [auth-setup.md#ses-sandbox-vs-production](../../docs/guides/gaininsight-standard/auth-setup.md#ses-sandbox-vs-production)

**SES commands reference (all CLI commands in one place):**
→ [auth-setup.md#ses-commands-reference](../../docs/guides/gaininsight-standard/auth-setup.md#ses-commands-reference)

**Key Doppler secrets (domain admin credentials, Gmail testing):**
→ [auth-setup.md#key-doppler-secrets](../../docs/guides/gaininsight-standard/auth-setup.md#key-doppler-secrets)

**Common pitfalls (sandbox blocks, plus addressing, DKIM, wrong region):**
→ [auth-setup.md#common-pitfalls](../../docs/guides/gaininsight-standard/auth-setup.md#common-pitfalls) — see pitfalls 3, 4, 5, and 7
