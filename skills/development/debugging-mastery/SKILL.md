---
name: debugging-mastery
description: Systematic debugging methodologies for finding and resolving complex bugs. Use PROACTIVELY when encountering difficult bugs, mysterious failures, or issues that resist simple fixes. MUST BE USED when debugging spans multiple files, involves race conditions, or has eluded initial investigation attempts.
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Task"]
---

# Debugging Mastery Skill

## Overview

**Key Principle:** Root cause over symptom treatment. Never be satisfied with making symptoms disappear. Understand WHY the bug occurred.

### When to Use

**MUST USE when:**
- Bug spans multiple files or components
- Involves race conditions or timing issues
- Has eluded initial investigation (>30 minutes)
- Symptoms are intermittent or hard to reproduce
- Previous fix attempts have failed

**SHOULD USE when:**
- Bug is in unfamiliar code
- Error messages are unclear or misleading
- Multiple hypotheses are possible

---

## The DEBUG Framework

```
D → E → B → U → G
│   │   │   │   │
│   │   │   │   └─ GUARD: Fix and prevent regression
│   │   │   └───── UNCOVER: Find root cause (5 Whys)
│   │   └───────── BISECT: Narrow down location
│   └───────────── EXPLORE: Gather evidence
└───────────────── DEFINE: Expected vs Actual
```

| Phase | Purpose | Key Action | Output |
|-------|---------|------------|--------|
| **D** | Define | State expected vs actual | Problem statement |
| **E** | Explore | Gather evidence, logs, recent changes | Evidence list |
| **B** | Bisect | Narrow down with binary search | Suspect location |
| **U** | Uncover | Apply 5 Whys to find root cause | Root cause |
| **G** | Guard | Fix + regression test | Verified fix |

### D - Define the Problem
State clearly: **Expected** vs **Actual** behavior, reproduction steps, environment.

### E - Explore Evidence
Collect: Full stack traces, surrounding logs, recent changes (`git log`), affected scope.

### B - Bisect and Narrow
Use binary search: Comment out code halves, use `git bisect`, create minimal reproduction.

### U - Uncover Root Cause
Apply 5 Whys: Ask "why" until you reach an actionable fix point. Verify: "If we fix this, would the bug have been prevented?"

### G - Guard Against Recurrence
Fix the root cause (not symptom), add regression test, check for similar patterns elsewhere.

**Full framework details:** [reference/debugging-techniques.md](reference/debugging-techniques.md)

---

## Bug Classification Quick Reference

### By Reproducibility

| Type | Debugging Approach |
|------|-------------------|
| **100% Reproducible** | Standard: breakpoints, logging |
| **Intermittent** | Logging, state capture, timing analysis |
| **Rare** | Defensive logging, assertions, monitoring |

### By Bug Type

| Type | Symptoms | Primary Technique |
|------|----------|-------------------|
| **Logic** | Wrong output | Code review, test cases |
| **State** | Corruption, unexpected values | State logging |
| **Timing** | Race conditions, deadlocks | Thread analysis |
| **Resource** | Leaks, exhaustion | Profiling |
| **Integration** | API mismatches | Interface comparison |
| **Environment** | "Works on my machine" | Config diff |

**Full classification:** [reference/bug-classification.md](reference/bug-classification.md)

---

## Core Techniques

| Technique | When to Use | Key Command |
|-----------|-------------|-------------|
| **5 Whys** | Unclear cause | Ask "why" 5 times |
| **Git Bisect** | Regression | `git bisect start/good/bad` |
| **Binary Search** | Large codebase | Comment out halves |
| **Isolation** | Complex bug | Create minimal repro |
| **Rubber Duck** | Stuck | Explain code line-by-line |
| **Printf Debug** | No debugger | Strategic print statements |

### Git Bisect Quick Reference
```bash
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>
# Test and mark: git bisect good OR git bisect bad
# Repeat until culprit found
git bisect reset
```

**Full techniques:** [reference/debugging-techniques.md](reference/debugging-techniques.md)

---

## Root Cause Analysis

### The 5 Whys Process

```
Problem: API returns 500 error
  ↓ Why?
Database query failed
  ↓ Why?
Connection pool exhausted
  ↓ Why?
Connections not released
  ↓ Why?
Exception handler missing close()
  ↓ Why?
Template code lacked finally block
  ↓
ROOT CAUSE: Missing resource cleanup pattern
```

**Stop when:** You reach an actionable fix within your control.

**Verify:** "If we fix this, would the problem have been prevented?"

**Full RCA guide:** [reference/root-cause-analysis.md](reference/root-cause-analysis.md)

---

## Subagent Integration

### When to Escalate to `debugger` Subagent
- Standard techniques haven't worked after 3 attempts
- Bug requires multi-codebase analysis
- Need advanced reasoning (Ultrathink methodology)
- Complex distributed system issues

### Handoff Protocol
Provide: Bug summary, DEBUG progress so far, files involved, hypotheses tested, specific request.

### Iteration Tracking
The debugger subagent has a **5-iteration limit**. Track attempts and escalate if needed.

---

## Quality Checklist

### Must Pass
- [ ] Root cause identified (not just symptom)
- [ ] Fix tested (reproduction steps no longer work)
- [ ] Regression test added
- [ ] No new bugs introduced

### Should Pass
- [ ] Similar patterns checked elsewhere
- [ ] Documentation updated if process gap found
- [ ] Code review complete

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Better Approach |
|--------------|--------------|-----------------|
| **Shotgun debugging** | Random changes | Use DEBUG framework |
| **Fixing symptoms** | Bug will return | Find root cause |
| **Skipping reproduction** | Can't verify fix | Always reproduce first |
| **Ignoring intermittent** | Gets worse | Add logging, capture state |
| **Debug in production** | High risk | Reproduce locally |
| **Assuming the obvious** | Wastes time | Verify with tests |
| **Not adding tests** | Bug will recur | Always add regression test |

**Full examples:** [reference/anti-patterns.md](reference/anti-patterns.md)

---

## Templates

| Template | Purpose |
|----------|---------|
| [templates/debugging-session.md](templates/debugging-session.md) | Track entire session |
| [templates/root-cause-report.md](templates/root-cause-report.md) | Document RCA |
| [templates/hypothesis-log.md](templates/hypothesis-log.md) | Track hypotheses |

---

## Quick DEBUG Template

```markdown
## Quick DEBUG

**D - Define:**
Expected: [what should happen]
Actual: [what happens]
Steps: [to reproduce]

**E - Explore:**
Error: [full message]
Changed: [recent changes]
Scope: [who's affected]

**B - Bisect:**
Last working: [commit/date]
First broken: [commit/date]
Narrowed to: [component/file]

**U - Uncover:**
Why 1: [symptom reason]
Why 2: [deeper reason]
Why 3: [root cause]

**G - Guard:**
Fix: [what to change]
Test: [regression test]
```

---

## Reference Documentation

- [reference/root-cause-analysis.md](reference/root-cause-analysis.md) - 5 Whys, Fishbone, Fault Trees
- [reference/debugging-techniques.md](reference/debugging-techniques.md) - Binary search, git bisect, isolation
- [reference/bug-classification.md](reference/bug-classification.md) - Bug types and approaches
- [reference/anti-patterns.md](reference/anti-patterns.md) - Common mistakes

---

**Remember:** A bug isn't fixed until you understand WHY it occurred and have prevented it from recurring.
