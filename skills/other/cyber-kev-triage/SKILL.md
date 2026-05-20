---
name: cyber-kev-triage
description: Prioritize vulnerability remediation using KEV-style exploitation context plus asset criticality. Use for CVE triage, patch order decisions, and remediation reporting.
---

# Cyber KEV Triage

## Overview

Create a patch-priority plan by combining vulnerability severity, exploitation status, and business criticality of affected assets.

## Workflow

1. Collect vulnerabilities with CVE, CVSS, exploitation indicator, and affected asset.
2. Map each vulnerability to asset criticality.
3. Score and rank vulnerabilities into patch priority tiers.
4. Produce concise remediation summary and due-window guidance.

## Use Bundled Resources

- Run `scripts/kev_triage.py` for deterministic triage output.
- Read `references/triage-method.md` for scoring rationale and review checks.

## Guardrails

- Keep output defensive and remediation-focused.
- Do not generate exploit payloads or offensive execution steps.
