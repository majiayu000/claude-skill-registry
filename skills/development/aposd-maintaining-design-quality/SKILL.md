---
name: aposd-maintaining-design-quality
description: "Enforce strategic programming discipline when modifying existing code. Guide through STOP-ASK-DECIDE-VERIFY workflow with urgency tier assessment (trivial/minor/standard/emergency). Include when NOT to refactor (Chesterton's Fence, performance-critical, no tests) and block tactical shortcuts via anti-rationalization tables. Use when fixing bugs, extending features, or tempted to make quick fixes. Triggers on: modify code, fix bug, extend feature, quick fix, tactical change."
---

# Skill: aposd-maintaining-design-quality

## STOP - The Design Rule

**If you're not making the design better, you're probably making it worse.** Working code is not a high enough standard.

**Zero Tolerance:** There is no acceptable threshold for making design worse. Even "small" compromises accumulate invisibly—dozens of tactical decisions compound into unmaintainable systems.

---

## Urgency Tiers

Not all changes need equal analysis. Match effort to impact:

| Tier | Examples | Required Analysis |
|------|----------|-------------------|
| **Trivial** | Typo fixes, whitespace, comment corrections | None—just do it |
| **Minor** | Bug fix <5 lines, config tweak, dependency bump | Quick check: does this fit cleanly? |
| **Standard** | New feature, refactoring, multi-file change | Full workflow: STOP-ASK-DECIDE-VERIFY |
| **Emergency** | Production down, security breach, data loss | Minimal fix + TODO + 24hr follow-up |

---

## Strategic Modification Workflow

```
BEFORE making any change to existing code:

1. RESIST the temptation to make a quick fix

2. ASK: "Is the current system design still the best one,
   given the change I need to make?"

3. IF NO: Refactor so you end up with the best possible design
   Goal: After this change, the system should have the structure
   it would have had if designed from the start with this in mind

4. IF YES: Make the change within the existing design
   But verify: does your change fit cleanly?

5. BEFORE COMMIT: Scan all changes to verify documentation reflects them
```

---

## The Investment Mindset

| Approach | Short-Term | Long-Term |
|----------|------------|-----------|
| **Tactical** | 10-20% faster | Permanently slower (20%+ productivity loss) |
| **Strategic** | 10-20% slower | Benefits in months; eventually free |

**Recommended investment:** About 10-20% of development time on design improvements.

### Why Strategic Wins

```
Tactical path:
- Each "quick fix" adds small complexity
- Complexities accumulate (dozens/hundreds of small things)
- Eventually: system is hard to understand and modify
- Result: development slows permanently

Strategic path:
- Each change improves or maintains design
- Past investments save time for future investments
- Eventually: strategic investments become FREE
- Result: development accelerates over time
```

---

## Design Evolution Principle

A system's design cannot be conceived correctly at the outset. The design of a mature system is determined **more by changes made during evolution** than by initial conception.

**Implication:** Every modification matters. Your changes ARE the design.

---

## When Refactoring Seems Impractical

Even under tight deadlines, ask:

```
"Is this the best I can possibly do to create a clean system design,
given my current constraints?"
```

| If... | Then... |
|-------|---------|
| Large refactoring is impractical | Look for alternatives that are almost as clean but faster |
| Cannot do proper cleanup now | Create accountability plan (see below) |
| Refactoring creates incompatibilities | Seek middle-ground solutions |

**Never acceptable:** Making the design worse without a plan to fix it.

### Accountability for Deferred Refactoring

If you defer refactoring, it MUST be tracked:

```
1. CREATE a ticket/issue with specific scope
2. TIMEBOX: Must be addressed within 2 sprints (or equivalent)
3. ADD a code comment: // TODO(YYYY-MM-DD): [ticket-id] - [what needs fixing]
4. ESCALATE if 3+ deferrals exist in same area → refactoring becomes MANDATORY
```

**"I'll do it later" without these steps = you won't do it.**

---

## When NOT to Refactor

Refactoring is not always the right choice:

| Scenario | Why Refactoring Hurts | What to Do Instead |
|----------|----------------------|-------------------|
| **Chesterton's Fence code** | Looks bad but handles subtle edge cases | Investigate WHY before changing |
| **Performance-critical paths** | Clean abstractions add overhead | Document why it's intentionally ugly |
| **Regulatory/audited code** | Changes trigger expensive re-certification | Get explicit approval first |
| **Legacy with no tests** | Refactoring without tests is dangerous | Add tests first, or freeze |
| **Code with external quirk dependencies** | Other systems rely on undocumented behavior | Coordinate with dependents |
| **Near end-of-life systems** | Investing in dying code is waste | Document, don't improve |
| **During incident response** | Changing more increases blast radius | Minimal fix only |
| **When you don't understand domain** | "Better design" reflects misunderstanding | Learn first, refactor later |

**Key question:** Do I understand WHY the code is the way it is?

---

## Emergency Bypass Criteria

Skip the normal workflow ONLY when ALL of these conditions are true:

1. Production is down RIGHT NOW (not "might break soon")
2. Users are actively impacted, security breach in progress, OR data loss occurring
3. The fix is minimal (rollback or single-line change)
4. You commit to returning for proper implementation within 24 hours

**Emergency does NOT mean:**
- "Demo in 30 minutes" — That's planning failure
- "CEO is asking" — Authority pressure ≠ emergency
- "Team is blocked" — They can wait for you to think
- "We need this fast" — Speed pressure is when discipline matters MOST

---

## Red Flags

| Red Flag | Symptom | What It Signals |
|----------|---------|-----------------|
| **Quick Fix Mentality** | "Just make it work for now" | Tactical programming—design will degrade |
| **Complexity Creep** | Adding special cases, conditionals, dependencies | Design is getting worse, not better |
| **Patch Stacking** | Workarounds on top of workarounds | Technical debt accumulating |
| **Tactical Tornado** | Very fast developer leaving messes | Others will pay for their speed |
| **Stale Comments** | Comments no longer match code | Trust erosion; documentation debt |
| **Deferred Cleanup** | "We'll refactor later" | Later never comes; delay becomes permanent |

---

## Anti-Rationalization Table

### Classic Rationalizations

| Tempting Shortcut | Why It Feels Right | Why It's Wrong |
|-------------------|-------------------|----------------|
| "Just make it work" | Faster now | Creates technical debt forever; 20%+ productivity loss |
| "Don't touch working code" | Risk averse | Prevents improvement; design decays anyway |
| "We'll refactor later" | Deferred pain | Later never comes; there's always another crunch |
| "This is just a quick fix" | Scope limiting | Quick fixes accumulate; complexity is incremental |
| "I don't have time" | Deadline pressure | 10-20% investment now saves more later |
| "It's not that bad" | Normalizing decay | Each small compromise adds up to major complexity |

### Responsibility-Avoidance Rationalizations

| Tempting Shortcut | Why It Feels Right | Why It's Wrong |
|-------------------|-------------------|----------------|
| "I'm not the owner of this module" | Not my responsibility | If you're touching it, you're responsible for it |
| "The original author did it this way" | Appeal to authority | Original author might have been wrong, or context changed |
| "This matches the existing pattern" | Consistency | Consistently following a bad pattern spreads the problem |

### "It Doesn't Count" Rationalizations

| Tempting Shortcut | Why It Feels Right | Why It's Wrong |
|-------------------|-------------------|----------------|
| "This is temporary/experimental code" | It's throwaway | Nothing is as permanent as temporary code |
| "The tests pass" | Correctness verified | Passing tests ≠ good design |
| "I'll document the tech debt" | I'm being responsible | Documentation is not remediation |

---

## Comment Maintenance

When modifying code, keep comments synchronized:

| Rule | Why |
|------|-----|
| Position comments close to code they describe | Developers see them when modifying |
| Avoid duplicating documentation | One source of truth |
| Document each decision exactly once | Find the single most obvious place |
| Scan all changes before commit | Catch stale comments early |

---

## Technical Debt Reality

| Myth | Reality |
|------|---------|
| "We'll pay it back" | Most technical debt is never fully repaid |
| "It's a fair trade" | Amount paid back exceeds amount borrowed |
| "Just this once" | Once you start, it's difficult to change |
| "Everyone does it" | Complexity accumulates rapidly if everyone programs tactically |

---

## Quick Reference

```
EVERY TIME you modify existing code:

1. STOP - Resist the quick fix temptation
2. ASK - "Is this design still optimal for what I need?"
3. DECIDE:
   - Design is optimal? Make change cleanly
   - Design needs work? Refactor first
   - Can't refactor now? Plan when you will
4. VERIFY - Comments updated? Design improved or maintained?
5. COMMIT - Only when design is better or at least not worse

THE RULE:
"If you're not making the design better, you're probably making it worse."

INVESTMENT MATH:
- 10-20% slower now → faster forever
- "Quick fix" now → 20%+ slower forever
```


---

## Chain

| After | Next |
|-------|------|
| Design assessment done | Back to task checklist |
