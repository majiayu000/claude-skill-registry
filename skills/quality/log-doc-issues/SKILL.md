---
name: log-doc-issues
description: |
  Run /check-docs, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /fix-docs instead if you want to fix issues immediately.
---

# /log-doc-issues

Run documentation audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-docs` to audit documentation
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/fix-docs` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-docs` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/docs" --limit 50
```

### 3. Create Issues

For each finding:

```bash
gh issue create \
  --title "[P1] README missing Installation section" \
  --body "$(cat <<'EOF'
## Problem
README.md exists but lacks Installation section. New developers cannot set up the project.

## Impact
- Contributor onboarding blocked
- Time wasted figuring out setup
- Potential contributors give up

## Location
`README.md`

## Suggested Fix
Run `/fix-docs` or add manually:
- Prerequisites (Node version, etc.)
- Package manager commands
- Environment setup steps

---
Created by `/log-doc-issues`
EOF
)" \
  --label "priority/p1,domain/docs,type/chore"
```

### 4. Issue Format

**Title:** `[P{0-3}] Documentation gap description`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/docs`
- `type/chore`

**Body:**
```markdown
## Problem
What documentation is missing or broken

## Impact
Who is affected (new devs, users, contributors)

## Location
File path or expected file location

## Suggested Fix
Skill to run or manual action

---
Created by `/log-doc-issues`
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| Missing README.md | P0 |
| Missing .env.example (with env vars used) | P0 |
| README missing key sections | P1 |
| Undocumented env vars | P1 |
| Missing architecture docs | P1 |
| Stale documentation (90+ days) | P2 |
| Missing CONTRIBUTING.md | P2 |
| Missing ADR directory | P2 |
| Broken links | P2 |
| Polish improvements | P3 |

## Output

After running:
```
Documentation Issues Created:
- P0: 0
- P1: 3 (README sections, env vars)
- P2: 2 (stale docs, ADRs)
- P3: 1 (link checking)

Total: 6 issues created
View: gh issue list --label domain/docs
```

## Related

- `/check-docs` - The primitive (audit only)
- `/fix-docs` - Fix documentation gaps
- `/documentation` - Full documentation workflow
- `/groom` - Full backlog grooming
