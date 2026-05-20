---
name: vibe-wave-based-remediation
description: Systematically fixes large backlogs of issues using prioritized waves. Use when facing 10+ issues, bugs, or gaps to address.
user-invocable: true
---

# vibe-wave-based-remediation

When you have 50 issues, don't fix them randomly. Attack in waves.

## When to Use This Skill

- 10+ bugs, issues, or gaps to fix
- After an audit or review that produced many findings
- After `vibe-spec-vs-code-audit` reveals many gaps
- Technical debt cleanup with many items

## When NOT to Use This Skill

- Fewer than 5 issues (just fix them sequentially)
- All issues are the same priority (no need to wave)
- Issues are all in one file (batch-fix is simpler)

## Steps

1. **Triage all issues** into priority:
   - **P0 — Blocker**: Breaks core functionality, security vulnerability, data loss risk
   - **P1 — High**: Wrong behavior, significant UX issue, missing critical feature
   - **P2 — Medium**: Incomplete implementation, minor bugs, documentation gaps
   - **P3 — Low**: Polish, optimization, nice-to-have improvements

2. **Group into waves**:
   - **Wave 0**: All P0 issues (fix immediately, before anything else)
   - **Wave 1**: All P1 issues, grouped by affected module/file for efficiency
   - **Wave 2**: P2 issues, parallelizable groups
   - **Wave 3**: P3 issues (may defer to backlog)

3. **Execute each wave**:
   - Fix all issues in the wave
   - Run tests after the wave
   - Verify fixes don't introduce regressions
   - Commit the wave as a logical unit
   - **Do NOT start Wave N+1 until Wave N passes tests**

4. **Track progress**:

## Output Format

### Wave-Based Remediation

**Total Issues**: X
**Waves**: Y

| Wave | Priority | Issues | Status |
|------|----------|--------|--------|
| 0 | P0 (Blocker) | 3 | Complete |
| 1 | P1 (High) | 12 | In Progress (8/12) |
| 2 | P2 (Medium) | 25 | Pending |
| 3 | P3 (Low) | 10 | Deferred |

### Wave 1 Detail
| Issue | File | Status | Fix |
|-------|------|--------|-----|
| GAP-001 | auth.go | Done | Added token expiry |

### Remaining
- Wave 2: 25 issues (ready to start)
- Wave 3: 10 issues (deferred to backlog)
