---
name: vibe-research-before-design
description: Dispatches SOTA research before proposing any new feature, architecture, or technology choice. Use when facing design decisions, not when implementing existing specs.
user-invocable: true
---

# vibe-research-before-design

Before proposing any design, architecture, or technology choice — research first. "Other people's documented failures count as observed failure."

## When to Use This Skill

- Designing a new feature or system
- Choosing between technologies, frameworks, or patterns
- Making architectural decisions with long-term consequences
- The user asks "how should we build X?"
- You're about to say "I recommend..." for a design choice

## When NOT to Use This Skill

- Implementing an already-designed spec (the research was done at design time)
- Fixing a bug (use `vibe-debugging-journal` instead)
- Simple refactoring with no architectural implications
- The user has explicitly chosen a technology and wants implementation

## Steps

1. **Identify the design question** — What decision are we making? What are the key constraints?

2. **Dispatch research** — For each major sub-problem, find:
   - 2+ named real-world projects/libraries with adoption metrics (GitHub stars, npm downloads, production users)
   - 1+ academic paper or technical blog with year and venue/source
   - The **mechanism** — how does it actually work? (Not marketing copy)
   - **Known failures** — what went wrong for others?
   - **Applicability assessment** — does this fit our constraints?

3. **Synthesize findings** — Present a comparison table:
   | Option | Adoption | Mechanism | Known Failures | Fit |
   |--------|----------|-----------|---------------|-----|

4. **Make a recommendation** — Based on evidence, not intuition. State confidence level.

5. **Record the decision** — Use `vibe-decision-journal` to log the choice and alternatives.

## Red Flags

- "This is obvious, we should just use X" — If it's obvious, proving it takes 2 minutes
- "I've used X before" — Past experience ≠ current best option
- "Everyone uses X" — Popularity ≠ fitness for your constraints
- "Let me just start building and we'll figure it out" — The most expensive approach

## Output Format

### Research Summary
- **Decision**: [What we're deciding]
- **Constraints**: [Key constraints]
- **Options Evaluated**: X

### Comparison Table
| Criteria | Option A | Option B | Option C |
|----------|----------|----------|----------|

### Recommendation
[Evidence-based recommendation with confidence level]

### Sources
[Links to projects, papers, docs referenced]
