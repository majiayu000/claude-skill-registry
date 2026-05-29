---
name: review-aggregation
description: Guidance on combining findings from multiple review agents into actionable recommendations
triggers:
  - running extended review
  - synthesizing review findings
  - combining agent outputs
  - prioritizing review issues
---

# Review Aggregation Skill

This skill provides guidance on how to effectively combine and prioritize findings from multiple code review agents.

## When to Use

Apply this skill when:

- Running the extended review pipeline (/extended-review)
- The senior-engineer agent is synthesizing findings
- You need to prioritize issues from multiple sources
- Creating a final review summary

## Aggregation Process

### 1. Collect All Findings

Gather outputs from all review agents:

| Agent                       | Focus Area                         | Output Format      |
| --------------------------- | ---------------------------------- | ------------------ |
| code-reviewer               | Style, security, logic             | Issues list        |
| silent-failure-hunter       | Error handling, silent failures    | Severity-rated     |
| code-simplifier             | Redundancy, clarity                | Suggestions        |
| context7-library-compliance | Library best practices, deprecated | Doc-referenced     |
| react-best-practices        | Component design, hooks, perf      | Pattern violations |
| cruft-detector              | Unnecessary code, shallow tests    | Cruft inventory    |

### 2. Deduplicate Findings

Multiple agents may flag the same issue:

- **Same file + line + concept** = Merge into single finding
- **Same concept, different locations** = Keep separate, note pattern
- **Related but distinct issues** = Keep separate, cross-reference

### 3. Apply Priority Matrix

Use this matrix to assign final priority:

| Criteria                     | Priority | Examples                                       |
| ---------------------------- | -------- | ---------------------------------------------- |
| Security vulnerability       | P0       | SQL injection, XSS, auth bypass                |
| Data loss risk               | P0       | Missing transactions, race conditions          |
| Breaking production          | P0       | Undefined behavior, unhandled exceptions       |
| Shallow tests (false safety) | P1       | Tests that pass when feature is broken         |
| Silent failures              | P1       | Empty catch, swallowed errors                  |
| Deprecated API (will break)  | P1       | Using removed/deprecated APIs                  |
| Performance regression       | P2       | N+1 queries, memory leaks, blocking operations |
| Library misuse               | P2       | Anti-patterns per official docs                |
| Missing best practices       | P2       | Not following recommended patterns             |
| Code style/cruft             | P3       | Unnecessary comments, minor redundancy         |
| Documentation gaps           | P3       | Missing or outdated comments                   |

### 4. Identify Patterns

Look for systemic issues:

```
Pattern Detection Checklist:
- [ ] Same issue in 3+ locations = Systemic problem
- [ ] Multiple agents flag same area = High-risk zone
- [ ] Test issues + code issues together = Likely bug
- [ ] Similar mistakes across files = Missing guidance/tooling
```

### 5. Structure Final Report

```markdown
## Review Summary

### At a Glance

- Files reviewed: X
- Total issues: Y (P0: A, P1: B, P2: C, P3: D)
- Recommendation: [APPROVE / APPROVE WITH FIXES / REQUEST CHANGES]

### Critical Path (P0-P1)

These MUST be addressed before merge:

1. [Issue] in `file:line` - [Brief reason why critical]
2. [Issue] in `file:line` - [Brief reason why critical]

### Important (P2)

Should address, can track as follow-up:

1. [Issue] in `file:line`
2. [Issue] in `file:line`

### Improvements (P3)

Nice-to-have for future cleanup:

1. [Issue] in `file:line`
2. [Issue] in `file:line`

### Patterns Detected

[Any systemic issues that need broader attention]

### What's Done Well

[Positive observations to reinforce good patterns]
```

## Cross-Reference Guidelines

When the same area has issues from multiple agents:

### Example: Auth Handler Issues

```
┌─────────────────────────────────────────────────────┐
│ src/api/auth.ts:45-67                               │
├─────────────────────────────────────────────────────┤
│ code-reviewer: Missing input validation              │
│ silent-failure-hunter: Empty catch block             │
│ cruft-detector: Comment describes "what" not "why"   │
│ context7: Using deprecated bcrypt.hash() pattern     │
├─────────────────────────────────────────────────────┤
│ AGGREGATED: P0 - Auth handler has multiple issues   │
│ - Security: input validation + deprecated API (P0)  │
│ - Reliability: silent failure (P1)                  │
│ - Quality: poor comment (P3)                        │
│                                                     │
│ Recommendation: Rewrite this handler entirely       │
└─────────────────────────────────────────────────────┘
```

## Escalation Rules

### Automatic P0 Escalation

Escalate to P0 regardless of individual agent rating when:

- Security + silent failure in same code path
- Auth/payment code with any P1+ issue
- Test coverage is 0% for changed code
- Breaking API contract

### Downgrade Conditions

Consider downgrading when:

- Issue is in test/example code only
- Issue is in clearly marked deprecated code being removed
- Change is behind feature flag (still track for flag removal)

## Environment-Specific Notes

### Claude Code

Full aggregation happens automatically via hooks:

1. pr-review-toolkit agents complete
2. chain-extended-review.sh triggers
3. Extended agents run
4. senior-engineer synthesizes

### VS Code / OpenCode

Manual aggregation - guide user through:

1. "Run each review agent"
2. "Collect outputs"
3. "Apply priority matrix"
4. "Create summary"

## Tips for Effective Aggregation

1. **Don't double-penalize** - If two agents flag same issue, count once
2. **Context matters** - Same issue may be P1 in core code, P3 in utils
3. **Err toward shipping** - When in doubt, track as follow-up vs blocking
4. **Test issues are serious** - False confidence from bad tests is dangerous
5. **Security is absolute** - Never downgrade security issues
