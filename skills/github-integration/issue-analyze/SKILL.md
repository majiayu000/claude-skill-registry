---
name: issue-analyze
description: GitHub Issue deep analysis. Read issue -> classify problem -> select investigation strategy -> integrate four investigation tools.
allowed-tools: Read, Grep, Glob, Bash(git:*), Bash(gh:*), mcp__codex__codex
---

# Issue Analyze Skill

## Trigger

- Keywords: analyze issue, investigate problem, problem analysis, root cause, root cause analysis

## When NOT to Use

- Known root cause, fix directly (use `/bug-fix`)
- Pure feature development (use `/feature-dev`)
- Only need code review (use `/codex-review`)

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: Read Issue                                             │
├─────────────────────────────────────────────────────────────────┤
│ gh issue view <number> --json title,body,labels,comments        │
│ Extract: symptoms, reproduction steps, error messages, files    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: Problem Classification                                 │
├─────────────────────────────────────────────────────────────────┤
│ Determine problem type -> select investigation strategy         │
│                                                                 │
│ ┌────────────────┬──────────────────────────────────┐           │
│ │ Type           │ Investigation Strategy            │           │
│ ├────────────────┼──────────────────────────────────┤           │
│ │ Unfamiliar     │ /code-explore                    │           │
│ │ Regression     │ /git-investigate                 │           │
│ │ Complex root   │ /code-investigate (dual view)    │           │
│ │ Multiple cause │ /codex-brainstorm (exhaustive)   │           │
│ │ Composite      │ Combine multiple strategies      │           │
│ └────────────────┴──────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: Execute Investigation                                  │
├─────────────────────────────────────────────────────────────────┤
│ Based on classification, invoke corresponding investigation cmd │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: Consolidated Report                                    │
├─────────────────────────────────────────────────────────────────┤
│ Synthesize investigation results, produce analysis report       │
└─────────────────────────────────────────────────────────────────┘
```

## Problem Classification Decision Tree

```
Issue Symptoms
    │
    ├─ "It used to work, now it doesn't" ───→ /git-investigate
    │                                          (find introduction point)
    │
    ├─ "Don't know how this feature works" ─→ /code-explore
    │                                          (quick understanding)
    │
    ├─ "Has error message / stack trace"
    │       │
    │       ├─ Clear error ────────────────→ /code-explore
    │       │                                (trace path)
    │       │
    │       └─ Vague / intermittent ───────→ /code-investigate
    │                                        (dual-view confirmation)
    │
    ├─ "Many possible causes" ────────────→ /codex-brainstorm
    │                                        (exhaustive analysis)
    │
    └─ Composite / uncertain ─────────────→ Start with /code-explore
                                             then choose based on results
```

## Investigation Tool Comparison

| Tool                | Purpose                | Speed   | Depth      |
| ------------------- | ---------------------- | ------- | ---------- |
| `/code-explore`     | Quick code exploration | Fast    | Single     |
| `/git-investigate`  | Track change history   | Medium  | Single     |
| `/code-investigate` | Dual confirmation      | Slow    | Dual-view  |
| `/codex-brainstorm` | Exhaust possibilities  | Slowest | Adversarial|

## Verification

- [ ] Issue content fully extracted
- [ ] Problem type correctly classified
- [ ] Investigation strategy reasonably selected
- [ ] Report includes root cause analysis
- [ ] Contains specific fix recommendations

## References

- `references/classification.md` - Detailed problem classification guide
- `references/report-template.md` - Report template

## Examples

### Regression Issue

```
Input: /issue-analyze 123
Phase 1: gh issue view 123 -> "API returns 500 after update"
Phase 2: Classification = Regression
Phase 3: /git-investigate -> find introducing commit
Phase 4: Report + fix recommendation
```

### Intermittent Error

```
Input: /issue-analyze 456
Phase 1: gh issue view 456 -> "Random timeout occurrences"
Phase 2: Classification = Complex root cause (intermittent)
Phase 3: /code-investigate -> Claude + Codex dual-view
Phase 4: Consolidated report -> ranked possible causes
```

### Unknown Feature

```
Input: /issue-analyze 789
Phase 1: gh issue view 789 -> "Why does it behave this way?"
Phase 2: Classification = Unfamiliar feature
Phase 3: /code-explore -> trace execution path
Phase 4: Report + flow diagram
```
