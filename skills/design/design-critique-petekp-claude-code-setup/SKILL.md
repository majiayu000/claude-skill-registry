---
name: design-critique
description: Critique UI/UX designs for clarity, hierarchy, interaction, accessibility, and craft. Use for design reviews, PR feedback on UI changes, evaluating mockups, checking if a component is ship-ready, or when honest feedback is needed on whether something meets a high bar.
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebFetch
  - mcp__claude-in-chrome__*
---

# Design Critique

Honest, specific, actionable feedback on interface design.

## The Critique Stance

- Be direct. No soft language. No vibes-only feedback.
- Point to specifics, not generalities.
- Explain why, not just what.
- Reference principles, not preferences.
- Offer fixes, not just problems.

## Process

1. **Identify what you're critiquing** - Screen, component, flow, or interaction
2. **Gather context** - Platform, users, constraints (if available)
3. **Apply the lens** - Clarity, hierarchy, interaction, accessibility, craft
4. **Prioritize issues** - P0 (blocking) through P3 (polish)
5. **Propose fixes** - Specific, actionable changes

## Quick Check (Use CHECKLIST.md for detailed pass)

**Clarity**
- Can users predict outcomes before acting?
- Is the hierarchy of information obvious?
- Are interactive elements clearly distinguished?

**Interaction**
- Do all states exist? (hover, focus, active, disabled, loading, error)
- Is feedback immediate?
- Can users recover from errors?

**Accessibility**
- Focus visible and logical?
- Contrast sufficient?
- Touch targets adequate (44x44pt)?

## Output Contract

Structure every critique as:

```markdown
## Verdict
[1 sentence: ship/iterate/rethink]

## Issues

### P0: [Issue Name]
- **What's wrong**: [Specific observation]
- **Why it matters**: [User impact]
- **Evidence**: [Element, screen, or behavior]
- **Fix**: [Actionable change]

### P1: [Issue Name]
...

## Accessibility Pass
- Focus visibility: [Pass / Issue + fix]
- Contrast: [Pass / Issue + fix]
- Touch targets: [Pass / Issue + fix]
- Motion: [Respects reduced-motion? / Issue]

## What's Working
[2-3 things done well - critique includes praise]

## Next Steps
- [ ] [Verification action 1]
- [ ] [Verification action 2]
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **P0** | Blocks task, causes confusion, or data loss | Must fix before ship |
| **P1** | Frequent friction, misclicks, unclear recovery | Should fix |
| **P2** | Polish, efficiency, minor annoyance | Fix if time permits |
| **P3** | Nice-to-have refinement | Consider for later |

## The Questions Behind Everything

- "What is the user trying to do here?"
- "What's the most important thing on this screen?"
- "What would happen if we removed this?"
- "Would a new user understand this?"
- "Are we proud of this?"

## Common Critique Notes

**"Too busy"**: Too many things competing for attention. Remove until important things breathe.

**"Not discoverable"**: Hidden functionality, unlabeled icons, gestures without affordance.

**"Inconsistent"**: Different patterns for similar actions. Pick one and commit.

**"Feels off"**: Usually spacing, alignment, or timing. The eye knows before the mind articulates.

**"Overdesigned"**: Every effect turned up. Decoration overwhelming function. Subtract until inevitable.

## Deep Reference

For detailed heuristics, common failures, and platform-specific patterns:
- [CHECKLIST.md](CHECKLIST.md) - Quick pass checklist
- [PRINCIPLES.md](PRINCIPLES.md) - Full critique principles and examples
