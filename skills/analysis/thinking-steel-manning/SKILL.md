---
name: thinking-steel-manning
description: Argue against the strongest version of opposing positions, not the weakest. Use for design reviews, evaluating alternatives, conflict resolution, and decision validation.
---

# Steel-Manning

## Overview

Steel-manning is the opposite of straw-manning. Instead of attacking the weakest version of an opposing argument, you construct and address the strongest possible version. This leads to better decisions, more productive debates, and deeper understanding of trade-offs.

**Core Principle:** To truly evaluate an idea, argue against its best form. If you can defeat the strongest version, you've actually learned something.

## When to Use

- Design reviews
- Evaluating alternative approaches
- Conflict resolution
- Validating your own decisions
- Code review discussions
- Architecture debates
- When you disagree with someone's proposal
- Before rejecting an idea

Decision flow:

```
Disagreeing with a proposal?
  → Can you state their best argument? → no → STEEL-MAN FIRST
  → Are you attacking a weak version? → yes → CONSTRUCT STRONGER VERSION
  → Have you found the core insight? → no → DIG DEEPER
```

## The Steel-Manning Process

### Step 1: Understand the Original Argument

Before improving, understand:

```markdown
## Original Proposal

Proposal: "We should rewrite the backend in Rust"

Stated reasons:
- Memory safety
- Better performance
- Modern language

Apparent weaknesses:
- Team doesn't know Rust
- Rewrite is risky
- Current system works
```

### Step 2: Identify the Core Insight

What's the strongest kernel of truth?

```markdown
## Core Insight

Behind "rewrite in Rust" is:
- Concern about memory-related bugs in production
- Performance problems that are hard to solve in current language
- Technical debt making changes slow

The proposal might be wrong, but the concerns are valid.
```

### Step 3: Construct the Strongest Version

Build the best possible case:

```markdown
## Steel-Manned Argument

"Our memory-safety issues have caused 3 major outages this year,
costing us ~$500K in engineering time and customer trust.
Our performance problems stem from GC pauses that are fundamental
to our current runtime. While a rewrite is risky, the incremental
cost of working around these limitations is growing.

A gradual rewrite of performance-critical paths to Rust would:
- Eliminate a class of bugs (memory safety)
- Solve GC-related latency issues
- Attract engineers who want modern tooling
- Create optionality for high-performance features

The risk can be mitigated by:
- Starting with one isolated service
- Keeping the team small and focused
- Maintaining the old system during transition
- Having clear rollback criteria"
```

### Step 4: Address the Steel-Manned Version

Now engage with the strongest argument:

```markdown
## Response to Steel-Manned Argument

The strongest case for Rust addresses real problems. However:

Memory safety issues:
- 2 of 3 outages were logic bugs, not memory bugs
- Could be addressed with better testing in current language
- Rust learning curve might introduce new bug classes

Performance:
- GC issues could be addressed with tuning
- Critical path is <5% of codebase
- FFI to native code is an option without full rewrite

The 6-month investment in Rust might be better spent:
- 2 months: Performance profiling and GC tuning
- 2 months: Targeted native extensions for hot paths
- 2 months: Improved testing/monitoring

This addresses the concerns with lower risk.
```

### Step 5: Find the Synthesis

What's the best answer considering both sides?

```markdown
## Synthesis

The Rust proposal was right about the problems, less right about the solution.

Agreed:
- Memory safety is a real concern (but smaller than stated)
- Performance needs improvement (but addressable incrementally)
- Technical modernization has value (but not at rewrite cost)

Plan:
1. Address immediate performance with profiling + tuning
2. Build one small service in Rust as learning experiment
3. Evaluate Rust for future services based on learnings
4. Don't rewrite existing system

This takes the best of both positions.
```

## Steel-Manning Patterns

### In Design Reviews

```markdown
## Design Review: Microservices Proposal

Weak version to avoid:
"They just want to use trendy tech"

Steel-manned version:
"The monolith has become a development bottleneck.
Deploy conflicts are causing delays. Different teams
need different scaling characteristics. The proposal
addresses real coordination problems."

Now address:
"The coordination problems are real, but can we solve them
with modular monolith patterns before taking on distributed
systems complexity?"
```

### In Code Reviews

```markdown
## Code Review: Complex Abstraction

Weak critique:
"This is over-engineered"

Steel-manned understanding:
"The author anticipated we'll need to support multiple
backends. This abstraction makes adding new backends
trivial. The complexity exists to serve future flexibility."

Better critique:
"I understand this enables multiple backends. Let's
validate that requirement—if we only ever need one,
the abstraction adds maintenance burden without benefit."
```

### In Conflict Resolution

```markdown
## Team Disagreement: Testing Strategy

Person A: "We need 100% code coverage"
Person B: "Code coverage is a vanity metric"

Steel-man A:
"Coverage ensures we think about edge cases and makes
refactoring safer. Without coverage requirements,
critical paths go untested."

Steel-man B:
"Coverage without quality gives false confidence.
Testing getters/setters wastes time better spent on
integration tests that catch real bugs."

Synthesis:
"Coverage is valuable for complex logic, less valuable
for trivial code. Let's require coverage for business
logic modules, but focus on integration tests for
overall system confidence."
```

### In Self-Critique

```markdown
## Validating My Own Decision

My decision: Use NoSQL for this project

Steel-man the opposite:
"SQL has survived 50 years because relational models
work for most data. NoSQL solves problems most projects
don't have. The flexibility of schemaless data becomes
a bug when requirements solidify. Joins are a feature,
not a limitation."

Now: Does my NoSQL choice survive this critique?
- Do I actually need schemaless flexibility?
- Will I regret not having joins?
- Am I solving a problem I don't have?
```

## Steel-Manning Red Flags

Signs you're straw-manning instead:

| Straw-Man Sign | Example | Fix |
|----------------|---------|-----|
| "They just want..." | "They just want to use new tech" | Find the legitimate concern |
| Attacking messenger | "They're inexperienced" | Address the argument |
| Cherry-picking worst example | "Remember when X failed?" | Consider best examples |
| Assuming bad faith | "They don't care about quality" | Assume they want good outcomes |
| Ignoring strong points | Skipping their best argument | Address strongest point first |

## Steel-Manning Template

```markdown
# Steel-Man Analysis: [Topic]

## Original Position
Who: [Person/group]
Position: [Their stated view]
Stated reasons: [Their explicit arguments]

## Apparent Weaknesses
[What seems wrong at first glance]

## Core Insight
[The legitimate concern or truth behind the position]

## Steel-Manned Version
[The strongest possible formulation of their argument]

"[Write it as if you were advocating for this position]"

## My Response to the Strong Version
[Now address the steel-manned argument]

## What I Learned
[How did steel-manning change my understanding?]

## Synthesis
[Best answer considering both positions]
```

## Verification Checklist

- [ ] Understood the original argument
- [ ] Identified the core insight/concern
- [ ] Constructed the strongest possible version
- [ ] Addressed the strong version, not a weak one
- [ ] Found what's legitimate in the opposing view
- [ ] Considered synthesis of positions
- [ ] Changed my mind if the steel-man is convincing

## Key Questions

- "What's the strongest version of this argument?"
- "What legitimate concern is behind this?"
- "Could I argue this position convincingly?"
- "What would make this position correct?"
- "Am I attacking the weakest or strongest form?"
- "If I were advocating for this, what would I say?"

## Rapoport's Rules (Related)

Daniel Dennett, channeling Anatol Rapoport, offers rules for criticizing:

1. Attempt to re-express the target's position so clearly that they say "Thanks, I wish I'd thought of putting it that way."
2. List any points of agreement (especially if not matters of widespread agreement).
3. Mention anything you learned from the target.
4. Only then are you permitted to say so much as a word of rebuttal or criticism.

This is steel-manning as ethical practice.

## Mill's Wisdom

"He who knows only his own side of the case knows little of that."

You don't truly understand your position until you can argue the opposition's best case. Steel-manning isn't weakness—it's the path to strong positions that can withstand strong criticism.
