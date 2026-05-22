---
name: react-patterns
description: React best practices and anti-patterns reference. Use when writing React components, reviewing code for anti-patterns, debugging useEffect issues, optimizing performance, or deciding between state vs derived values. Covers Effects, state design, component patterns, performance, and event handling.
---

# React Patterns

## Overview

Decision-driven guidance for writing idiomatic React. Focus on avoiding common anti-patterns and choosing the right tool for each job.

## Quick Decision Trees

### Should This Be a useEffect?

```
Is this synchronizing with an EXTERNAL system?
├─ YES (DOM, network, third-party widget) → useEffect
└─ NO
   ├─ Caused by USER ACTION? → Event handler
   ├─ Can be CALCULATED from state/props? → Render-time calculation
   └─ Runs because component DISPLAYED? → useEffect
```

### Should This Be State?

```
Can it be computed from existing props/state?
├─ YES → Derive it (const x = ...)
└─ NO
   ├─ Does it change over time? → useState
   └─ NO → Regular variable or prop
```

### Should I Memoize This?

```
Is the calculation expensive (>1ms)?
├─ NO → Don't memoize
└─ YES
   ├─ Used in render? → useMemo
   └─ Passed to child as prop? → Consider useMemo
```

## Anti-Pattern Quick Reference

| BAD                                | GOOD                          | Reference                   |
| ---------------------------------- | ----------------------------- | --------------------------- |
| Derived state in useEffect         | Calculate during render       | `references/effects.md`     |
| useEffect for event logic          | Put in event handler          | `references/effects.md`     |
| useEffect to reset state on prop   | Use React `key` prop          | `references/effects.md`     |
| Effect chains (A→B→C)              | Calculate in single handler   | `references/effects.md`     |
| Notify parent via useEffect        | Call in same event handler    | `references/effects.md`     |
| Store full object when ID suffices | Store ID, derive object       | `references/state.md`       |
| Prop drilling 5+ levels            | Composition or context        | `references/components.md`  |
| useMemo/useCallback everywhere     | Only when measurably needed   | `references/performance.md` |
| Inline handlers causing re-renders | useCallback IF measured issue | `references/performance.md` |
| Logic in onClick directly          | Extract to named handler      | `references/events.md`      |

## When to Load References

Load the specific reference file when working on that area:

- **Effects issues**: `Read(.claude/skills/react-patterns/references/effects.md)`
- **State structure**: `Read(.claude/skills/react-patterns/references/state.md)`
- **Component design**: `Read(.claude/skills/react-patterns/references/components.md)`
- **Performance**: `Read(.claude/skills/react-patterns/references/performance.md)`
- **Event handling**: `Read(.claude/skills/react-patterns/references/events.md)`

## Core Principles

1. **Effects are escape hatches** - Only for external system sync
2. **Derive, don't sync** - If computable, compute it
3. **State should be minimal** - Store IDs not objects, derive the rest
4. **Measure before optimizing** - No premature useMemo/useCallback
5. **Colocate related logic** - Keep cause and effect together
6. **Data flows down** - Avoid passing data up via Effects
