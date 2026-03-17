---
name: architecture-workshop
description: Framework for designing new architectural mechanisms when existing patterns don't fit
---

# Architecture Workshop

This skill provides a framework for designing options when changes don't fit cleanly into existing codebase architecture.

## When to Use

Load this skill when architecture fit evaluation returns NO_FIT or when you're compensating for architectural gaps with workarounds.

## Core Principle

Your job is NOT to find workarounds that force a fit. If the right answer requires new architectural mechanisms, say so — even if a hacky fit is technically possible.

At the same time, don't over-engineer. If a light-touch structural improvement solves the problem cleanly, that's often better than a full architectural shift.

## Process

### 1. Understand Why It Doesn't Fit

- Why doesn't this fit cleanly?
- Is it a localized mismatch or a systemic gap?
- What's the actual constraint violation vs. what's just unfamiliar?

### 2. Research Deeper (if needed)

Use the `research` skill to understand:
- What patterns exist for the type of problem this change introduces?
- Are there any partial implementations or footholds for the needed mechanism?
- What would be the natural extension points?

### 3. Generate Options

**Light-Touch Options** (consider first):
- Add a new module boundary + interface seam
- Introduce an adapter layer in one location
- Extract a small abstraction that makes the fit clean
- Add migration guardrails for incremental adoption

**Architecture Options** (when light-touch won't work):
- Introduce eventing/pubsub where none exists
- Add state-machine-driven workflow
- Change concurrency model
- Introduce new infrastructure component

### 4. Evaluate Each Option

For each option, assess:
- **Blast radius**: Which domains/components change (not individual files)
- **Incremental path**: Can we keep repo green throughout?
- **Long-term impact**: How this affects future changes, maintainability
- **Reversibility**: How hard to undo if wrong?

## When to Recommend Light-Touch vs Architecture Shift

**Light-Touch** is right when:
- The problem is localized to 1-2 domains
- An interface seam or adapter solves it cleanly
- The repo already has similar patterns elsewhere
- Future changes won't keep hitting this same wall

**Architecture Shift** is right when:
- Multiple modules need to participate in a new coordination model
- The same problem will recur for future features
- The light-touch path creates inconsistent patterns
- The change represents a genuine evolution in what the system does

## Output Format

Document your options:

```markdown
## Architecture Options

### Option A: <Name>

- **Description**: <What this entails — stay high-level>
- **Blast Radius**: <Which domains/components change>
- **Incremental Path**: <Phases to adopt while keeping repo green>
- **Long-Term Impact**: <How this affects future changes>
- **Tradeoffs**: <Honest pros and cons>

### Option B: <Name>

<Same structure>

### Option C: <Name> (if meaningfully different)

<Same structure>

### Recommendation

<Which option and why — optimize for codebase health, not just "easiest fit">
```

## Design Principles

- **Codebase health is the objective**: Don't contort just to fit
- **Light-touch is often best**: A well-placed interface seam can solve many problems
- **Incremental path is mandatory**: "Big bang" is not acceptable
- **Blast radius matters**: Prefer smaller when it solves the problem equally well
- **Keep it high-level**: Architectural guidance, not implementation planning
- **Ground everything in repo reality**: Options must be grounded in what actually exists
