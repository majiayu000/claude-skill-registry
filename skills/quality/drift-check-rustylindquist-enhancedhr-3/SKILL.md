---
name: drift-check
description: Detect documentation drift (docs out of sync with code). Use after changes, periodically, or when something feels wrong. Returns severity-rated findings with specific fixes.
allowed-tools: Read, Glob, Grep, Bash
---

# Drift Check

Detect documentation rot by comparing code reality against documented expectations.

## When to Use

- After completing a feature or bug fix
- Before starting work on unfamiliar area
- When behavior doesn't match expectations
- Periodically (weekly recommended)

## Severity Levels

| Severity | Areas | Action Required |
|----------|-------|-----------------|
| 🔴 Critical | Auth/RLS wrong, billing docs incorrect, schema mismatch | Fix immediately |
| 🟠 High | Server action undocumented, invariant violated | Fix this session |
| 🟡 Medium | Route missing from surfaces, stale checklist | Fix soon |
| 🟢 Low | Minor description inaccuracy | Track |

## Check Categories

1. **Server Actions vs Docs** — Actions exist in code but not documented (or vice versa)
2. **Routes vs User Surfaces** — Routes exist but not in feature doc tables
3. **Schema vs Data Model** — Tables/columns don't match docs
4. **RLS vs Permissions Docs** — Policies undocumented or incorrect
5. **Invariants vs Reality** — Can't find code enforcing documented invariants
6. **Workflow Steps vs UI** — Documented steps don't match actual UI

## Quick Check Commands

```bash
# Count server actions
find app/actions -name "*.ts" | wc -l

# Count routes
find app -name "page.tsx" | wc -l

# Recent migrations (verify reflected in docs)
ls -lt supabase/migrations/ | head -5
```

## Output

```markdown
## Drift Check Report — [date]

**Scope**: [full / feature-name]

| Severity | Count |
|----------|-------|
| 🔴 Critical | [n] |
| 🟠 High | [n] |
| 🟡 Medium | [n] |
| 🟢 Low | [n] |

### Issues Found
[For each issue: category, location, finding, remediation]

### No Drift Found
[Areas checked with no issues]
```

## Related

- Detailed check procedures: See [reference/check-procedures.md](reference/check-procedures.md)
- Remediation templates: See [reference/remediation-templates.md](reference/remediation-templates.md)
- Severity scoring matrix: See [reference/severity-matrix.md](reference/severity-matrix.md)
- After finding drift: Run `/doc-update` to fix
