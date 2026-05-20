---
name: documentation-audit
description: Full audit and update of BioETL project documentation for v5.22+. Use when asked to review docs for staleness, reconcile docs with code, sync RULES.md and REQUIREMENTS.md, update architecture/provider/contract docs, reflect ADR-010/ADR-014/ADR-017, or identify dead documentation.
---

# Documentation Audit

## Objective
Perform a full documentation audit of BioETL and bring docs in sync with code and ADRs (v5.22+). Produce a clear audit report, a prioritized plan, and updated documentation changes.

## Required inputs (before starting)
- Load `.claude/skills/documentation-audit.audit-checklist.md` — checklist for each audit area.
- Load `.claude/skills/documentation-audit.report-template.md` — template for the audit report.

## Workflow

### 1. Intake and scope
- Confirm repo root and target version (v5.22+).
- Identify doc entry points: README.md, mkdocs.yml.
- List files under `docs/`: `rg --files docs`.

### 2. Audit (follow audit-checklist.md)
- Compare documentation to current code and configs.
- Focus: RULES.md, REQUIREMENTS.md, architecture, provider, contract docs.
- Check ADR alignment: ADR-010 (Local-Only), ADR-014 (Determinism), ADR-017 (Observability).
- Record findings with severity: Critical, High, Medium, Low.

### 3. Plan
- Turn findings into a concrete change list.
- Prioritize by impact (Critical > High > Medium > Low).
- Call out unknowns that need user confirmation.

### 4. Update (if user requests)
- Edit docs to match current code and ADRs.
- Keep versions and dates explicit in text.
- For obsolete docs: propose delete/archive, do not remove unless user asks.

### 5. Verify
- Check links and nav entries (mkdocs.yml).
- Confirm RULES.md and REQUIREMENTS.md are synchronized.
- Ensure ADRs are reflected in top-level docs.

## Practical commands
```bash
# ADR references
rg -n "ADR-010|ADR-014|ADR-017" docs README.md mkdocs.yml

# Version mentions
rg -n "v5\.14|5\.14" docs README.md

# Doc refs in nav
rg -n "docs/|\.md" mkdocs.yml README.md

# Orphan scan: list docs/ then search each filename in mkdocs.yml and other docs
rg --files docs
```

## Output format
- Use `.claude/skills/documentation-audit.report-template.md` structure for the audit report.
- Provide a short prioritized change list and required user decisions.
- Do not change code unless explicitly requested; focus on documentation.

## Constraints

### MUST
- Use `.claude/skills/documentation-audit.report-template.md` for the audit report.
- Verify findings against actual code and configs.
- Record severity for each finding.

### MUST NOT
- Change code unless user explicitly asks.
- Remove docs without explicit user approval.
- Document desired behavior instead of reality when code and docs diverge — flag and propose options.

### SHOULD
- Prefer documenting reality; when code and docs diverge, flag and propose options.
