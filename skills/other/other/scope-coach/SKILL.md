---
name: scope-coach
description: This skill should be used when the user mentions "scope", "MVP", "minimum viable", "too much", "overwhelmed", "where do I start", "feature creep", "simplify", "cut scope", "what's essential", or when a conversation reveals expanding complexity, multiple possible approaches, or analysis paralysis. Counterbalances the tendency to over-analyse and over-build.
version: 1.0.0
---

# Scope Coach

Anti-scope-creep skill. Counterbalances the natural tendency to over-analyse, over-build, and resist cutting features. Forces the question: "What's the smallest thing that delivers value?"

---

## When This Skill Applies

Use this skill when:
- A feature design is growing in complexity
- Multiple approaches are being weighed without resolution
- The conversation has been exploring options for too long without committing
- The user says "I'm not sure where to start"
- A domain model reveals more complexity than expected
- The implementation plan has more than 5-7 steps for a single feature
- The user is adding "nice to haves" to the core requirement
- Analysis is deepening but no code is being written

**This skill is a counterweight** — it fires when the natural instinct to understand deeply risks delaying action.

---

## Core Principle

**Systems thinkers see everything. Ship anyway.**

Depth of understanding is a strength. But understanding without shipping is just analysis. The goal is not to stop thinking deeply — it's to think deeply *and then scope ruthlessly*.

The best v1 is the smallest thing that proves the idea works.

---

## The Scope Test

For any feature or task, answer these three questions:

### 1. What's the single thing this must do?

Not the three things. Not the five things. The ONE thing that, if it worked, would prove the concept.

```
✗ "Users can create accounts, manage profiles, set preferences,
   invite team members, and customise their dashboard"
✓ "Users can create accounts"
```

### 2. What can be hardcoded, defaulted, or deferred?

Everything that isn't the core behaviour can wait.

```
✗ Build a configurable notification system with email, SMS, push,
   and in-app channels with user preferences
✓ Send one email on signup. Add channels later.
```

### 3. What's the manual fallback?

If a feature is too complex to automate right now, can it be done manually?

```
✗ Build an automated invoice reconciliation system
✓ Export CSV, reconcile in spreadsheet, automate later if it matters
```

---

## Scope Reduction Patterns

### Pattern: Spike First

When unsure about complexity, write a throwaway proof-of-concept:
- Time-box it (2 hours max)
- No tests, no polish, no error handling
- Answer one question: "Does this approach work?"
- Then plan the real implementation with evidence

### Pattern: Vertical Slice

Build one complete path through the system instead of building all features partially:
```
✗ Build User model + Course model + Enrolment model + Progress model
  (all incomplete, none usable)

✓ Build User model + one API endpoint + one UI page
  (one complete, usable path)
```

### Pattern: Feature Flags Off

Build the minimum, ship it behind a flag, gather feedback, iterate:
- v0: Core behaviour, no edge cases
- v1: Handle main edge cases, improve UX
- v2: Polish, optimise, extend

### Pattern: Delete the Second Feature

If you planned two features, delete one. Ship the other. See if anyone asks for the one you deleted.

---

## Scope Expansion Warning Signs

Watch for these in conversation:

| Signal | What's happening | Response |
|--------|-----------------|----------|
| "While we're at it..." | Scope creep | "That's a separate ticket" |
| "What about edge case X?" | Premature completeness | "Handle it when it happens" |
| "We should also..." | Feature accumulation | "Add to backlog, not this PR" |
| "It would be nice if..." | Gold plating | "Ship without it, add if requested" |
| 45+ minutes discussing approach | Analysis paralysis | "Pick one. Try it. Adjust if wrong" |
| Plan exceeds 7 steps | Over-engineering | "Which 3 steps deliver the core?" |

---

## How to Apply

This skill doesn't produce standalone output. It **challenges** other work:

### During Planning
```
⚠️ Scope: This plan has 12 steps. Which 3-4 deliver a working first version?
The rest can be follow-up tasks.
```

### During Design
```
⚠️ Scope: The domain model covers 8 entities. Which 2-3 are needed for the
first usable feature? Model those. The rest can wait.
```

### During Implementation
```
⚠️ Scope: This function handles 6 edge cases. The happy path covers 90%
of usage. Ship with happy path + one critical error case.
```

---

## The Think-Then-Ship Balance

This skill does NOT mean:
- Skip modelling (domain-modeller is still essential)
- Ignore ethics (ethics-reviewer is still a constraint)
- Write sloppy code (quality per line stays high)
- Never plan (planning is good — over-planning is the enemy)

It DOES mean:
- Model the domain, then cut to essential entities for v1
- Check ethics, but don't let perfect be the enemy of good
- Write clean code for fewer things
- Plan then ship, don't plan then plan then plan

---

## Integration Points

### With domain-modeller
Domain modelling often reveals complexity. Scope coach responds: "Good — now which entities are needed for the first slice?"

### With implementation-planner
Implementation plans can grow unbounded. Scope coach forces: "Which steps produce a shippable unit?"

### With ethics-reviewer
Ethics is a constraint, not a scope-expansion tool. Scope coach ensures ethical requirements are met for what's being built, not used as a reason to build more.

---

## Success Criteria

Scope coaching is effective when:
- First versions ship faster
- Features are smaller and more focused
- Analysis leads to action, not more analysis
- "v2" tasks exist in the backlog (proof that scope was cut, not forgotten)
- The user feels unblocked, not restricted
