---
name: plan-brainstorm
description: Explore creative approaches and ideas with external source validation
---

# Plan Brainstorm

Uses **Planner**. Generate creative approaches to a problem using the Diverge → Converge → Synthesize framework. Actively seek external sources (documentation, upstream repos, specifications) to validate and enrich ideas.

**Prerequisites:** A clear problem statement or design challenge

---

## Phase 1: Frame the Challenge

### Define the Creative Space

1. State the problem or design challenge clearly
2. Identify constraints that are truly fixed vs. those that can be relaxed
3. Define success criteria for the brainstorm output
4. Note any "sacred cows" — assumptions worth questioning

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title> (if applicable)
- **Phase:** 1 — Frame

## Challenge Statement

<Clear statement of the design challenge>

## Fixed Constraints

- <truly immovable constraint>

## Bendable Constraints

- <constraint that could be relaxed>

## Sacred Cows

- <assumption worth questioning>

## Next Step

Begin divergent exploration.

**Approval Required:** No
```

---

## Phase 2: Diverge

### Generate Options Without Judgment

1. List at least 3 distinct approaches — aim for breadth over depth
2. Include at least one unconventional or contrarian option
3. Consider "do nothing" as a valid option
4. Draw from analogies in other domains, projects, or ecosystems
5. For each option, seek external inspiration:
   - Use `web/fetch` to read how others solved similar problems
   - Use `web/githubRepo` to explore prior art in open source
   - Cite external sources for ideas that come from outside the codebase

### Rules for Divergence

- No evaluation during this phase — capture everything
- Quantity over quality at this stage
- Wild ideas welcome — they can be tamed later
- Each option gets a one-paragraph description

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 2 — Diverge

## Options Generated

### Option A: <name>

<one-paragraph description>
**Inspiration:** <source, if external>

### Option B: <name>

<one-paragraph description>
**Inspiration:** <source, if external>

### Option C: <name>

<one-paragraph description>

### Option D: <unconventional option name>

<one-paragraph description>
**Inspiration:** <source, if external>

## Next Step

Evaluate options against criteria.

**Approval Required:** No
```

---

## Phase 3: Converge

### Evaluate Options Against Criteria

1. Define evaluation criteria upfront (cost, complexity, risk, alignment, reversibility)
2. Score or rank each option per criterion
3. Identify deal-breakers and must-haves
4. Note which options can be combined
5. Validate key assumptions with external sources where possible

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 3 — Converge

## Evaluation Criteria

| Criterion | Weight       | Description            |
| --------- | ------------ | ---------------------- |
| <name>    | High/Med/Low | <what we're measuring> |

## Option Evaluation

| Option | <Criterion 1> | <Criterion 2> | <Criterion 3> | Notes   |
| ------ | ------------- | ------------- | ------------- | ------- |
| A      | <score>       | <score>       | <score>       | <notes> |
| B      | <score>       | <score>       | <score>       | <notes> |
| C      | <score>       | <score>       | <score>       | <notes> |

## Combinable Options

- <Option A + C could combine because...>

## Deal-Breakers Identified

- <option X eliminated because...>

## Next Step

Synthesize into a recommendation.

**Approval Required:** No
```

---

## Phase 4: Synthesize

### Produce Recommendation

1. State the recommended approach with clear rationale
2. Document rejected alternatives and why
3. Identify risks and mitigations
4. Define the decision's reversibility
5. Note if this warrants an ADR (use `/plan-adr` if so)

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title>
- **Phase:** 4 — Synthesize

## Recommendation

**<Recommended approach name>**

<Rationale — why this approach over the others>

## Rejected Alternatives

| Alternative | Reason Rejected |
| ----------- | --------------- |
| <option>    | <why not>       |

## Risks & Mitigations

| Risk   | Likelihood   | Mitigation   |
| ------ | ------------ | ------------ |
| <risk> | High/Med/Low | <mitigation> |

## Reversibility

<How easy is it to change course? What's the blast radius?>

## External Sources Consulted

| Source        | What It Told Us |
| ------------- | --------------- |
| <URL or repo> | <key insight>   |

## Next Step

Awaiting approval of the recommended approach.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human approves or redirects the recommendation.

---

## Error Handling

| Error                          | Recovery                                                   |
| ------------------------------ | ---------------------------------------------------------- |
| Too few options generated      | Expand search to adjacent domains, question constraints    |
| All options have deal-breakers | Revisit constraints with human, explore hybrid approaches  |
| External sources disagree      | Document the disagreement, present both perspectives       |
| No clear winner                | Present top 2 with explicit trade-off, ask human to decide |
