---
name: plan-brainstorm
description: Explore creative approaches and ideas with external source validation.
---

# Plan Brainstorm

The Planner drives this workflow. Generate creative approaches to a problem using the Diverge → Converge → Synthesize framework. Actively seek external sources (documentation, upstream repos, specifications) to validate and enrich ideas.

---

## Phase 1: Frame the Challenge

Define the problem space before generating ideas.

### Steps

1. State the problem or design challenge clearly
2. Identify constraints that are truly fixed vs. those that can be relaxed
3. Define success criteria for the brainstorm output
4. Note any "sacred cows" — assumptions worth questioning

### Output

Produce a challenge frame covering: challenge statement, fixed constraints, bendable constraints, sacred cows.

**Approval Required:** No

---

## Phase 2: Diverge

Generate options without judgment.

### Steps

1. List at least 3 distinct approaches — aim for breadth over depth
2. Include at least one unconventional or contrarian option
3. Consider "do nothing" as a valid option
4. Draw from analogies in other domains, projects, or ecosystems
5. For each option, seek external inspiration:
   - Use `WebFetch` to read how others solved similar problems
   - Use `mcp__github__search_repositories` to explore prior art in open source
   - Cite external sources for ideas that come from outside the codebase

### Rules for Divergence

- No evaluation during this phase — capture everything
- Quantity over quality at this stage
- Each option gets a one-paragraph description with optional external inspiration note

### Output

Produce a diverged options list: each option gets a name, one-paragraph description, and optional inspiration source.

**Approval Required:** No

---

## Phase 3: Converge

Evaluate options against explicit criteria.

### Steps

1. Define evaluation criteria upfront (cost, complexity, risk, alignment, reversibility)
2. Score or rank each option per criterion
3. Identify deal-breakers and must-haves
4. Note which options can be combined
5. Validate key assumptions with external sources where possible

### Output

Produce a convergence evaluation covering: criteria table (criterion | weight | description), option scoring table, combinable options, deal-breakers.

**Approval Required:** No

---

## Phase 4: Synthesize

Produce a clear recommendation.

### Steps

1. State the recommended approach with clear rationale
2. Document rejected alternatives and why
3. Identify risks and mitigations
4. Define the decision's reversibility
5. Note if this warrants an ADR (use `/skill:plan-adr` if so)

### Output

Produce a synthesis covering: recommended approach with rationale, rejected alternatives table (alternative | reason rejected), risks table (risk | likelihood | mitigation), reversibility assessment, external sources consulted table.

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human approves or redirects the recommendation.

**Approval Required:** Yes

---

## Error Handling

| Error                          | Recovery                                                   |
| ------------------------------ | ---------------------------------------------------------- |
| Too few options generated      | Expand search to adjacent domains, question constraints    |
| All options have deal-breakers | Revisit constraints with human, explore hybrid approaches  |
| External sources disagree      | Document the disagreement, present both perspectives       |
| No clear winner                | Present top 2 with explicit trade-off, ask human to decide |
