---
name: define-x-strategy
description: 'Creates personalized X/Twitter growth strategy through guided interview. Based on algorithm-derived principles (exposure equation, phase model). Use when asked about X growth, Twitter strategy, building audience, or social media presence.'
---

**User request**: $ARGUMENTS

Create personalized X_STRATEGY.md through discovery interview. Strategy is grounded in algorithm-derived optimal growth principles.

**Before starting**: Read the reference documents in `skills/define-x-strategy/references/`:
- `OPTIMAL_STRATEGY.md` — The growth model and optimization principles
- `ALGORITHM_ANALYSIS.md` — Deep dive into X's recommendation algorithm

**Discovery log**: `/tmp/x-strategy-{YYYYMMDD-HHMMSS}.md`

## The Growth Model (from reference)

```
E = S × (N × D + R × U_oon)
```

- **S** (Content Score) — multiplies everything; quality > quantity
- **D** (Engagement Density) — % of followers who engage; protect this
- **R** (Retrieval Alignment) — niche focus; stay consistent
- **N** (Followers) — output of optimizing S, D, R; not a goal

**Phases** (state-based, not time-based):
1. **Build R** — Train algorithm via engagement before posting (when N ≈ 0)
2. **Build D** — Convert engagement to reciprocal network (when N small)
3. **Maximize S** — Optimize content score indefinitely (steady state)

**Invariants**: Quality > quantity, protect D, niche focus, avoid negative signals.

## Workflow

### Create todo list (immediately)

```
- [ ] Read references/; done when model internalized
- [ ] Create discovery log
- [ ] Discover current state→log; done when N, D, R assessed
- [ ] Discover niche positioning→log; done when angle clear
- [ ] Discover goals & constraints→log; done when realistic picture formed
- [ ] (expand: areas as discovery reveals)
- [ ] Assess current phase; done when phase determined with reasoning
- [ ] Refresh: read full discovery log
- [ ] Generate X_STRATEGY.md; done when strategy complete + validated
```

### Create discovery log

```markdown
# X Strategy Discovery
Started: {timestamp}

## Current State
(populated incrementally)

## Niche & Positioning
(populated incrementally)

## Goals & Constraints
(populated incrementally)

## Phase Assessment
(populated after discovery)

## Refinement
(populated during validation)
```

## Discovery Areas

Discover enough to assess phase and create actionable strategy. Use AskUserQuestion for all questions.

### Current State

Understand where they are:
- Account status (new, growing, established)
- Engagement patterns (do posts get traction?)
- Posting history (consistent? strategic? sporadic?)
- Network quality (followers who engage vs. dead followers)

### Niche & Positioning

Understand their angle:
- Topic/expertise area
- What makes their perspective unique
- Target audience on X
- Competitive landscape in their niche

### Goals & Constraints

Understand their reality:
- What they want from X (audience, leads, networking, brand)
- Time available (determines viable strategies)
- Content creation preferences (formats, strengths)
- Engagement comfort level

### Expand as Needed

| Discovery Reveals | Add Todo For |
|-------------------|--------------|
| Multiple potential niches | Niche narrowing |
| Very limited time | Minimum viable strategy |
| Product/service to promote | Aligned content strategy |
| Audience elsewhere | Cross-platform leverage |
| Past failures | Failure analysis |

**Write findings to log after each discovery step.**

## Phase Assessment

After discovery, determine their phase:

| Indicators | Phase |
|------------|-------|
| N < 100, little engagement history | Phase 1: Build R |
| N small, engaged core forming | Phase 2: Build D |
| N > 500, D > 30%, consistent posting | Phase 3: Maximize S |

Document reasoning in log.

## Output: X_STRATEGY.md

Generate strategy document. Structure should include:

```markdown
# X Growth Strategy: {Niche/Name}

> **North Star**: {One sentence goal}

## Current State

**Phase**: {1/2/3} — {Phase name}
**Focus**: {Primary variable to optimize}

{Current metrics assessment: N, D, R}

## The Model

{Brief explanation of exposure equation relevant to their phase}

## Your Niche Position

**Topic**: {Their niche}
**Angle**: {Unique perspective}
**Audience**: {Who they're reaching}
**Positioning**: {One sentence: "I help [audience] with [topic] by [angle]"}

## Phase-Appropriate Actions

{Actions specific to their current phase, fitted to their time budget}

{For Phase 1: engagement-focused, no posting yet}
{For Phase 2: posting + reciprocal network building}
{For Phase 3: content optimization + D maintenance}

## Content Strategy

{Based on their strengths and formats}

### Content Principles
{Pillars aligned with their niche and strengths}

### Multi-Signal Checklist
{Engagement triggers relevant to their content type}

### What to Avoid
{Anti-patterns specific to their situation}

## Engagement Strategy

{Time allocation based on their constraints}
{Engagement rules for their phase}

## Metrics to Track

{Phase-appropriate metrics}
{Transition triggers to next phase}

## Anti-Patterns

{Specific to their situation and common mistakes for their phase}

## Quick Reference

{Daily/weekly checklist fitted to their time budget}

---
*Strategy created: {date}*
*Phase: {current}*
*Review when: {transition trigger}*
```

**Adapt structure to what discovery revealed.** Add/remove sections as needed.

## Validation

Present key sections for validation:
- Does positioning capture them?
- Are actions realistic given constraints?
- Does phase assessment match their experience?

Update based on feedback. Write refinements to log.

## Principles

| Principle | Rule |
|-----------|------|
| Reference first | Read references/ before interviewing |
| Write before proceed | Log findings after each discovery step |
| Phase-appropriate | Strategy must match current state |
| Realistic constraints | Actions must fit their actual time/capacity |
| Principle over prescription | Give frameworks, not rigid scripts |
| State-based transitions | No time promises; transition when conditions met |

## Completion

Strategy complete when:
- [ ] Phase correctly assessed with reasoning
- [ ] Actions appropriate for phase and constraints
- [ ] Content strategy aligned with strengths
- [ ] Metrics tied to phase transitions
- [ ] User validates key sections

Write `X_STRATEGY.md` to current directory.
