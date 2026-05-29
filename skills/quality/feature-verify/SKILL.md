---
name: feature-verify
description: System diagnosis skill (READ-ONLY). Verifies feature behavior through code analysis, data validation, and Codex deep confirmation. All operations are strictly read-only - NO data modification allowed.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Task, Skill
context: fork
---

# Feature Verification Skill

## Trigger

- Keywords: verify, investigate, diagnose, check if working, anomaly, validate
- User provides credentials for data sources

## When NOT to Use

- Need to modify data (this skill is read-only only)
- Pure code review (use codex-review)
- Feature development (use feature-dev)

## Core Principle

```
ALL OPERATIONS MUST BE READ-ONLY
```

```
Claude independent analysis -> Form conclusion -> Codex third-perspective confirmation -> Integrated report
```

## Workflow

```
Phase 1: Explore    -> Understand system architecture, data flow, trigger points
Phase 2: Plan       -> Build verification checklist, present to user for confirmation
Phase 3: Execute    -> Execute read-only queries, record expected vs actual
Phase 4: Analyze    -> Claude independently forms diagnostic conclusion
Phase 5: Confirm    -> /codex-brainstorm third-perspective verification
Phase 6: Integrate  -> Synthesize dual perspectives, produce final report
```

## Safety Rules

| Rule              | Description                                      |
| ----------------- | ------------------------------------------------ |
| **READ-ONLY**     | No write/update/delete operations allowed        |
| PLAN-FIRST        | Present verification plan before executing queries |
| CREDENTIAL-SAFETY | Do not expose full credentials in output         |
| INDEPENDENT-FIRST | Claude forms conclusion first, then asks Codex to confirm |

## Verification Checklist

| Category           | Checks                              |
| ------------------ | ----------------------------------- |
| Feature Checks     | API endpoints, jobs, error handling |
| Data Checks        | Collections, aggregations, external |
| Integration Checks | End-to-end flow                     |

## Verification

- Report includes Executive Summary + Status
- Each check has expected/actual/status
- Both Claude + Codex perspectives are documented
- Recommendations split into Immediate / Further / Long-term

## References

- `references/queries.md` - Query templates + safety rules
- `references/output-template.md` - Report format

## Examples

```
Input: /feature-verify User Auth
       MongoDB: mongodb://...
       {ANALYTICS}: project_id={PROJECT_ID}
Action: Explore -> Plan -> Execute queries -> Analyze -> Codex confirm -> Report
```

```
Input: verify user auth is working correctly
Action: Phase 1-6 flow -> Output diagnostic report
```
