---
name: 023-assumption-analysis
description: Use when a framed and root-caused problem needs its assumptions made explicit before design or planning begins — explicit Assumptions, Unknowns, and a Validation plan. This should trigger when an issue's Assumption Analysis point of view needs evaluation, or when a maintainer directly asks to surface hidden assumptions and unknowns before committing to an approach. Part of Plinth Toolkit
license: Apache-2.0
metadata:
  author: Juan Antonio Breña Moral
  version: 0.18.0
---
# Assumption Analysis

Guide production of explicit Assumptions, a list of Unknowns, and a Validation plan for a problem under exploration. **This is an interactive SKILL**.

**What is covered in this Skill?**

- Surfacing assumptions implicit in the problem frame and root-cause findings
- Distinguishing an assumption (believed true, not yet verified) from an unknown (not yet known either way)
- Ranking assumptions and unknowns by impact and confidence
- Defining a validation plan that names how and when each risky assumption or unknown will be checked
- Feeding assumption and unknown findings into `024-context-mapping` and the remaining Functional Specification lenses

## Constraints

Make assumptions and unknowns explicit before they become undiscussed risk. When this technique is orchestrated by another workflow, the orchestrator owns clarifying-question sequencing; when applied standalone, ask directly.

- **MUST** read `references/023-assumption-analysis.md` before applying Assumption Analysis guidance
- **MUST** state each assumption as a falsifiable claim believed true but not yet verified
- **MUST** distinguish assumptions (believed true) from unknowns (not yet known either way)
- **MUST** rank assumptions and unknowns by impact if wrong and by current confidence
- **MUST** define a validation plan naming how and when each high-impact, low-confidence assumption or unknown will be checked
- **MUST NOT** invent an assumption, unknown, or validation step when the available content is vague or ambiguous; flag the gap for a clarifying question instead

## When to use this skill

- Surface the assumptions behind this problem
- List the unknowns for this issue
- Build a validation plan for these assumptions
- Apply assumption analysis before design begins
- Draft the Assumption Analysis section of a Functional Specification

## Workflow

1. **Read the Reference**

Read `references/023-assumption-analysis.md`, then review the problem frame and root-cause findings for implicit beliefs.

2. **Surface Explicit Assumptions**

State each assumption as a falsifiable claim believed true but not yet verified.

3. **List Unknowns**

List facts that are not yet known either way, distinct from assumptions.

4. **Rank by Impact and Confidence**

Rank assumptions and unknowns by impact if wrong and by current confidence, prioritizing high-impact, low-confidence items.

5. **Define the Validation Plan**

Name how and when each high-priority assumption or unknown will be validated.

6. **Report the Assumption Analysis**

Report the Assumptions, Unknowns, and Validation plan, and flag any item left open pending a clarifying answer.

## Reference

For detailed guidance, examples, and constraints, see [references/023-assumption-analysis.md](references/023-assumption-analysis.md).
