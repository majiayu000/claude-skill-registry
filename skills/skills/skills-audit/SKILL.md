---
name: skills-audit
description: "Audit skill folders for guideline compliance and portability. Use when validating SKILL.md files against skill_development_guidelines.md or checking for non-portable examples, hard-coded paths, or missing references."
---

# Skills Audit

## Overview
Scan skill folders and report guideline violations and portability issues. Produces a JSON report plus a readable summary.

## Quick start
1) Run: `python <REPO_ROOT>/skills/skills-audit/scripts/audit_skills.py --root skills --guidelines skill_development_guidelines.md`
2) Review `audit_results.json` and fix issues in the referenced files.

## Core Guidance
- Audit only; do not modify files automatically.
- Treat portability as a first-class rule: prefer `text` fences and placeholders.
- Report with file paths and line numbers when possible.

## Trust / Permissions
- **Always**: Read skill files and guidelines.
- **Ask**: Writing audit reports outside the repo or running networked checks.
- **Never**: Destructive changes or auto-edits to skill content.

## Resources
- `scripts/audit_skills.py`: Main audit script.
- `references/checklist.md`: Checklist mapped to `skill_development_guidelines.md`.

## Validation
- Run the audit against `skills/` and confirm JSON output is created.
