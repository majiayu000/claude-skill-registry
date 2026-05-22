---
name: agent-ops-debugging
description: "Systematic debugging approaches for isolating and fixing software defects. Use when something isn't working and the cause is unclear."
category: utility
invokes: [agent-ops-state, agent-ops-tasks]
invoked_by: [agent-ops-recovery, agent-ops-implementation, agent-ops-testing]
state_files:
  read: [constitution.md, baseline.md, focus.md, issues/*.md]
  write: [focus.md, issues/*.md]
---

# Skill: agent-ops-debugging

> Systematic debugging approaches for isolating and fixing software defects

---

## Purpose

Systematic problem isolation, root cause analysis, and defect resolution. Use when something isn't working and the cause is unclear.

---

## Core Principles

### 1. Understand Before Acting

- **Reproduce the issue**: Can you consistently trigger the problem?
- **Define expected vs actual**: What should happen vs what is happening?
- **Gather context**: When does this occur? Under what conditions?
- **Recent changes**: What changed before this appeared?

### 2. Isolate the Problem

- **Binary search**: Comment out half the code, test, repeat
- **Minimize reproduction**: Create minimal test case
- **Control variables**: Change one thing at a time
- **Eliminate noise**: Remove unrelated factors

### 3. Form Hypotheses

- **State your assumption**: "I believe X is causing Y because..."
- **Make predictions**: "If my hypothesis is true, then Z should happen"
- **Test predictions**: Verify or refute each hypothesis
- **Iterate**: Refine hypothesis based on evidence

### 4. Fix and Verify

- **Address root cause**: Not just symptoms
- **Minimize changes**: Smallest fix that resolves the issue
- **Add tests**: Prevent regression
- **Verify fix**: Test the specific scenario and related scenarios

---

## Systematic Debugging Process

### Phase 1: Problem Definition

1. **Describe the bug** in one sentence
2. **List reproduction steps** (minimal set)
3. **Specify expected behavior**
4. **Capture actual behavior** (screenshots, logs, error messages)
5. **Identify scope**: How widespread is this?

### Phase 2: Information Gathering

1. **Check logs**: Application logs, system logs, crash reports
2. **Inspect state**: Database records, cache contents, file system
3. **Review code**: Recent changes, related code paths
4. **Compare environments**: Dev vs staging vs production differences
5. **Monitor resources**: CPU, memory, disk, network during issue

### Phase 3: Hypothesis Formation

Common failure patterns:

| Pattern | Symptoms | Where to Look |
|---------|----------|---------------|
| **Timing issues** | Intermittent, "works sometimes" | Race conditions, deadlocks, timeouts |
| **State corruption** | Wrong data, unexpected mutations | Shared state, caches, global variables |
| **Resource exhaustion** | Slows down, eventually fails | Memory leaks, connection pools |
| **Configuration** | Works elsewhere, fails here | Environment variables, settings files |
| **Dependencies** | Broke after update | Library versions, API changes |
| **Assumption violations** | Edge case failures | Code assumes something that isn't true |

### Phase 4: Hypothesis Testing

1. **Add logging**: Instrument code to verify assumptions
2. **Use debugger**: Set breakpoints, inspect variables, step through
3. **Write tests**: Create failing test that reproduces bug
4. **Simplify**: Remove complexity while preserving failure
5. **Verify**: Confirm hypothesis explains all symptoms

### Phase 5: Resolution

1. **Implement fix**: Address root cause, not symptoms
2. **Add regression test**: Ensure bug doesn't return
3. **Review similar code**: Check for same issue elsewhere
4. **Document**: Add comments, update docs if behavior changed
5. **Verify**: Test fix works and doesn't break other things

---

## Debugging by Symptom

### "It Works on My Machine"

| Check | Action |
|-------|--------|
| Environment differences | Python versions, OS, dependencies |
| Uncommitted config | Local settings, .env files |
| Race conditions | Timing-dependent issues |
| Data differences | Test with production data subset |
| Resource constraints | Production may have different limits |

### Intermittent Failures

| Check | Action |
|-------|--------|
| Shared state | Global variables, singletons, caches |
| Timing | Race conditions, timeouts, async issues |
| Randomness | Random seeds, shuffling, sampling |
| Resource cleanup | Are resources properly released? |
| External dependencies | Network calls, third-party services |

### Performance Degradation

| Check | Action |
|-------|--------|
| Profile first | Measure before optimizing |
| O(n²) | Nested loops, repeated work |
| I/O | Database queries, file reads, network |
| Memory | Leaks, large objects, excessive allocations |
| Caching | Repeated expensive operations |

### Memory Leaks

| Check | Action |
|-------|--------|
| Profile memory | Track allocations over time |
| Circular references | GC can't collect cycles |
| Event listeners | Detached handlers keeping objects alive |
| Caches | Growing without bounds |
| Static collections | Accumulating entries |

### Deadlocks

| Check | Action |
|-------|--------|
| Lock order | Identify held locks, acquisition order |
| Cycles | A waits for B, B waits for A |
| Timeouts | Are operations waiting indefinitely? |
| Hold-and-wait | Holding one lock while waiting for another |

---

## Tool-Specific Guidance

### Print/Log Statements

```python
# Strategic placement with unique markers
print(f"[DEBUG-001] user_id={user_id}, state={state}")

# Include enough context
logger.debug(f"Processing item {i}/{total}: {item.id}")

# Remove after debugging!
```

### Debugger

- Set breakpoints at suspicious locations, not everywhere
- Watch expressions for specific variables
- Check call stack to understand how you got here
- Step carefully through suspicious code

### Tests for Debugging

- Write failing test that captures bug reproduction
- Use `git bisect` to find when bug was introduced
- Mock external dependencies to isolate
- Property-based testing finds edge cases

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| **Shotgun debugging** | Random changes hoping something works | Form hypothesis, test, refine |
| **Symptom treatment** | Adding error handling to hide failures | Fix underlying cause |
| **Assuming** | "This variable can't be null" | Add assertion to verify |
| **Overcomplicating** | Complex debugging infrastructure | Start simple, add tools as needed |
| **Ignoring evidence** | Dismissing data that doesn't fit | Revise hypothesis to explain all |

---

## Debugging Checklist

Before declaring "debugged":

- [ ] Root cause identified, not just symptom treated
- [ ] Fix is minimal and targeted
- [ ] Regression test added
- [ ] Related code checked for same issue
- [ ] Documentation updated if needed
- [ ] Fix verified in realistic scenario
- [ ] No new issues introduced

---

## When to Escalate

Consider asking for help if:

- After 2 hours without progress
- Issue is in unfamiliar technology stack
- Problem involves complex distributed systems
- Security implications
- Production outage
- Going in circles (revisiting same hypotheses)

---

## Recording Debug Sessions

Track in `.agent/focus.md`:

```markdown
## Debugging: [Issue Description]

**Symptom**: [What's happening]
**Expected**: [What should happen]
**Reproduction**: [Steps to trigger]

### Hypotheses
1. [Hypothesis] → [TESTED: result]
2. [Hypothesis] → [PENDING]

### Evidence Gathered
- Log at X showed Y
- Variable Z had value W

### Resolution
[Root cause and fix applied]
```
