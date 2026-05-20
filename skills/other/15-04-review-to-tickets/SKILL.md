---
name: 15-04-review-to-tickets
description: Convert findings from any review, audit, or analysis into individual tk tickets with proper priority and tagging.
---

# 15.04 Review-to-Tickets

After any review, audit, or analysis that surfaces issues, create `tk` tickets for **every finding**.

## When This Applies

Any skill or workflow that produces a report of issues:
- Code review (code-review, review-changes)
- Audits (audit, architectural-analysis, axiom-audit, file-name-wizard)
- Plan checks (check-plan)
- Spec/quality reviews (teams-driven-development, 4-step-program)

## Process

1. **Collect all findings** from the review/audit report.
2. **Create one ticket per finding** (or group tightly related findings into one ticket).
3. **Tag tickets** with the source skill and severity.
4. **Reference the report** in each ticket's Links section.

## Ticket Format

```bash
ID=$(tk create "SHORT DESCRIPTION" \
  -t task \
  -p PRIORITY \
  --tags SEVERITY,SOURCE_SKILL \
  -d "## Goal
What needs to be fixed or addressed.

## Source
- Skill: SOURCE_SKILL
- Report: path/to/report.md
- Severity: CRITICAL|HIGH|MEDIUM|LOW

## Details
Exact finding from the report. Include file paths and line numbers.

## Acceptance Criteria
- [ ] Issue is resolved
- [ ] Verification: SPECIFIC CHECK") && tk start $ID
```

## Priority Mapping

| Severity | tk Priority | Action |
|----------|-------------|--------|
| CRITICAL | 0 (urgent) | Fix immediately |
| HIGH | 1 | Fix before merge/release |
| MEDIUM | 2 | Fix soon |
| LOW | 3 | Fix when convenient |

## Grouping Rules

- **One ticket per distinct issue.** Don't lump unrelated findings.
- **Group related findings** if they share the same root cause (e.g., 5 files all missing the same type → one ticket).
- **Split large findings** if they require different fixes in different areas.

## After Creating Tickets

- Close tickets as you fix issues.
- Reference ticket IDs in commits: `t-XXXX: fix description`
- Log changes via `tinychange`.
