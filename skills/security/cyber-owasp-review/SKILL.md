---
name: cyber-owasp-review
description: Map application security findings to OWASP Top 10 categories and generate remediation checklists. Use for normalized AppSec review outputs and category-level prioritization.
---

# Cyber OWASP Review

## Overview

Normalize application security findings into OWASP categories and produce remediation actions.

## Workflow

1. Ingest raw findings from scanners, tests, or reviews.
2. Map findings to OWASP categories using keyword and context matching.
3. Aggregate findings by category and severity.
4. Produce category-specific remediation checklist output.

## Use Bundled Resources

- Run `scripts/map_findings_to_owasp.py` for deterministic mapping.
- Read `references/owasp-mapping-guide.md` for category heuristics.

## Guardrails

- Keep guidance remediation-focused.
- Do not provide exploit payloads or offensive attack playbooks.
