---
name: discovery
description: Structured pre-design questioning to surface hidden constraints before any architecture decision is locked in. Forces the architect/auditor/reviewer to enumerate what they DON'T know before proposing.
when_to_use: |
  Apply BEFORE producing architecture docs, audit findings, security plans:
  - architect, before writing ARCH-*.md
  - project-auditor, at the start of /audit
  - security-officer, before threat-modeling
  - l3-support, when triaging a new incident
  - regulated-reviewer, when classifying compliance scope
  - any reviewer who needs domain context the user hasn't given
effort: medium
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(bd:*)
paths:
  - "docs/**"
  - ".great_cto/**"
  - "README*"
---

# Discovery — surface hidden constraints first

The biggest cause of bad agent output is missing context. Before locking
in a decision, enumerate what you don't know and surface it.

## The 7 discovery dimensions

For any non-trivial request, walk through these and record findings in
the report's "Context" section:

### 1. Who depends on this?

- What other services / teams consume the thing you're changing?
- Are there public consumers (open API, OSS users)?
- Is there a deprecation path if you break compatibility?

Grep for: `grep -rE "import.*<your-module>|require.*<your-module>"` in
the repo and any sibling repos you have access to.

### 2. What's the scale today, what's it in 6 months?

- Current traffic: requests/sec, queries/sec, MB/day, daily-active-users
- Storage: rows in main tables, size on disk
- Cost: monthly LLM spend, infra spend
- 6-month projection: linear? exponential? unknown?

If unknown, write: "scale unknown — request from user before proceeding."

### 3. What MUST not change?

- Existing API contracts (backward compatibility window)
- Database schema columns referenced by reporting / BI
- File formats consumed by other tools
- Regulatory commitments (audit log retention, SLA RPO/RTO)

### 4. What's the budget?

- Monthly cost ceiling (LLM + infra)
- Headcount: 1-person task vs cross-team effort
- Calendar: "must ship by X" vs "best by Y"

If unstated, default to "small project_size, 1-engineer-week, <$200/mo
budget." Surface this default in the report so the user can correct.

### 5. What's the failure mode that matters?

Ask: "If this feature breaks at 3am, what gets paged?"
- Data loss → CRITICAL
- Wrong answer to user → HIGH
- Slow response → MEDIUM
- Bad UX (cosmetic) → LOW

The failure mode dictates investment level (e.g., do you need a canary?
A circuit breaker? Just a feature flag?).

### 6. What's already been tried?

- Search Beads: `bd search "<keyword>"` — has this been attempted before?
- Search docs/decisions: any superseded ADR on this topic?
- Search lessons.md: any past learning about this pattern?

If past work exists, build on it. Don't redo it.

### 7. Who decides?

- Is there a CTO sign-off needed (gate:plan, gate:ship)?
- Is there a compliance reviewer required (PCI for fintech, HIPAA for healthcare)?
- Does this need an RFC (multi-team decision)?

## Output

A discovery section at the top of your report:

```markdown
## Context

- **Consumers:** <list, or "unknown — TBD with user">
- **Scale:** <today, 6mo projection>
- **Frozen contracts:** <list, or "none identified">
- **Budget:** <cost + time + people>
- **Failure-mode tier:** Critical | High | Medium | Low
- **Prior work:** <links to ADRs/lessons, or "none found">
- **Decision-makers:** <gate or RFC required>
```

## When to skip

- **nano project_size** — discovery is overhead. Skip and document that
  you skipped: "nano — discovery skipped per skill rules."
- **Pure utility extraction** with no behaviour change — skip.
- **Verbal bug-fix from user** with clear repro — skip.

## Common gotchas

- **Don't assume.** If you write "I assume the user wants X", that
  assumption belongs in Context as a question, not as a fact.
- **Don't outsource to user.** Discovery is YOUR job. Bring back as many
  answers as Glob/Grep/git can produce. Only ask the user for what code
  cannot tell you.
