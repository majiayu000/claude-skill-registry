---
name: log-observability-issues
description: |
  Run /check-observability, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /fix-observability instead if you want to fix issues immediately.
---

# /log-observability-issues

Run observability audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-observability` to audit monitoring infrastructure
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/fix-observability` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-observability` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/observability" --limit 50
```

### 3. Create Issues

For each finding:

```bash
gh issue create \
  --title "[P0] No error tracking configured" \
  --body "$(cat <<'EOF'
## Problem
No error tracking (Sentry) configured. Production errors are invisible.

## Impact
- Errors happen silently
- Users affected without our knowledge
- No alert when things break
- Debugging requires log diving

## Suggested Fix
Run `/fix-observability` or manually:
```bash
pnpm add @sentry/nextjs
npx @sentry/wizard@latest -i nextjs
```

Configure DSN in environment variables.

---
Created by `/log-observability-issues`
EOF
)" \
  --label "priority/p0,domain/observability,type/chore"
```

### 4. Issue Format

**Title:** `[P{0-3}] Observability gap description`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/observability`
- `type/chore`

**Body:**
```markdown
## Problem
What monitoring/logging is missing

## Impact
What goes unseen, risk of blind spots

## Suggested Fix
Commands or skill to run

---
Created by `/log-observability-issues`
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No error tracking | P0 |
| No health endpoint | P0 |
| Error tracking misconfigured | P1 |
| No structured logging | P1 |
| Shallow health checks | P1 |
| No alerting | P1 |
| No analytics | P2 |
| Console.log overuse | P2 |
| No uptime monitoring | P2 |
| Performance monitoring | P3 |

## Output

After running:
```
Observability Issues Created:
- P0: 2 (no error tracking, no health endpoint)
- P1: 3 (logging, alerting, deep health)
- P2: 2 (analytics, console cleanup)
- P3: 1 (perf monitoring)

Total: 8 issues created
View: gh issue list --label domain/observability
```

## Related

- `/check-observability` - The primitive (audit only)
- `/fix-observability` - Fix observability gaps
- `/observability` - Full observability setup
- `/groom` - Full backlog grooming
