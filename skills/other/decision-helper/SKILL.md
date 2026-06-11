---
name: decision-helper
description: "Weighted decision scoring for architectural choices."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - "weigh options"
    - "decision matrix"
    - "compare approaches"
    - "help me decide"
    - "pros and cons"
    - "trade-offs"
    - "which is better"
    - "should I use"
    - "evaluate options"
  category: process
  pairs_with:
    - multi-persona-critique
    - adr-consultation
    - planning
---

# Decision Helper Skill

Structured weighted scoring for architectural and technology choices. Runs inline (no context fork) because users adjust criteria and weights interactively.

## Instructions

### Step 1: Frame the Decision

**Goal**: Turn the user's question into a clear, scorable decision.

- State the decision in one sentence (e.g., "Which HTTP router should we use for the API service?")
- List 2-4 concrete options. If the user provides more than 4, help them eliminate or group options before proceeding -- never score more than 4 at once because larger matrices dilute focus and invite analysis paralysis
- Identify hard constraints that eliminate options immediately (e.g., "must be MIT licensed" eliminates Option C)

If the user's request is too vague to frame, ask clarifying questions. Do not guess at options. If someone invoked this skill, the decision is not obvious -- run the full framework even when a quick answer feels tempting.

**Gate**: Decision statement defined, 2-4 options listed, hard constraints applied.

### Step 2: Define Criteria

**Goal**: Establish what matters for this decision and how much.

Present the default criteria table unless the user provides custom criteria. Ask if they want to adjust weights or add/remove criteria.

| Criterion | Weight | What It Measures |
|-----------|--------|-----------------|
| Correctness | 5 | Does it solve the actual problem? |
| Complexity | 3 | How much complexity does it add? (lower = better) |
| Maintainability | 3 | How easy to change/debug later? |
| Risk | 3 | What can go wrong? How bad is the failure mode? |
| Effort | 2 | Implementation time and difficulty |
| Familiarity | 2 | Team/user comfort with this approach |
| Ecosystem | 1 | Library support, documentation, community |

WHY these defaults: Correctness dominates because a wrong solution has zero value regardless of other factors. Complexity/Maintainability/Risk form a middle tier because they determine long-term cost. Effort/Familiarity are lower because they're temporary (teams learn, effort is one-time). Ecosystem is lowest because it rarely decides between otherwise-equal options.

Use defaults unless the user has a strong reason to change them. Agonizing over whether Complexity should be weight 3 or 4 rarely changes the outcome -- the framework exists to make decisions faster, not slower. Set weights before scoring; adjusting weights after seeing results to make a preferred option win is confirmation bias with extra steps.

If the user wants sensitivity analysis, re-score with adjusted weights after the initial pass to test recommendation stability.

**Gate**: Criteria and weights confirmed (default or custom).

### Step 3: Score Each Option

**Goal**: Rate each option against each criterion with justification.

Score every criterion 1-10 (1-3 poor, 4-6 adequate, 7-9 strong, 10 exceptional). Provide a one-sentence justification per score -- this prevents arbitrary numbers and makes disagreements productive.

Calculate weighted score: `sum(score * weight) / sum(weights)`

Treat scores as subjective estimates, not measurements. A difference of 0.03 between two options is noise, not signal -- the close-call detection in Step 4 handles this.

**Gate**: All options scored, all scores justified, weighted scores calculated.

### Step 4: Analyze Results

**Goal**: Interpret the scores and provide a clear recommendation.

Apply these rules in order:

1. **No Good Option** (all weighted scores <6.0): Flag that none of the options are strong. Suggest the user explore alternatives or revisit constraints
2. **Close Call** (top two within 0.5): Always flag as "close call -- additional factors should decide." Identify which criteria drive the difference and ask the user what matters most. Never hand-wave a close call with "close enough, just pick one" -- these deserve explicit acknowledgment
3. **Clear Winner** (top option leads by >0.5): Recommend the winner. Note which high-weight criteria drove the result
4. **Dominant Option** (top option leads on ALL weight-5 criteria): Note the dominance -- this is a high-confidence recommendation

If the matrix contradicts the user's intuition, do not override the math. Instead, ask which criterion is missing or mis-weighted. Add it, re-score, and see if the matrix now agrees. If it does, you found the hidden factor. If it still disagrees, trust the matrix -- it surfaces the reasoning that gut feelings obscure.

Present the output table:

```
## Decision: [statement]

| Criterion (weight) | Option A | Option B | Option C |
|---------------------|----------|----------|----------|
| Correctness (5)     | 8        | 7        | 9        |
| Complexity (3)      | 6        | 8        | 4        |
| Maintainability (3) | 7        | 7        | 5        |
| Risk (3)            | 6        | 8        | 4        |
| Effort (2)          | 7        | 5        | 3        |
| Familiarity (2)     | 8        | 4        | 2        |
| Ecosystem (1)       | 7        | 6        | 8        |
| **Weighted Score**  | **7.0**  | **6.7**  | **5.2**  |

**Recommendation**: Option A (7.0) — [key reasoning]
**Confidence**: High / Medium (scores within 0.5) / Low (no option >6.0)
```

**Gate**: Recommendation stated with confidence level. Close calls flagged.

### Step 5: Persist Decision

**Goal**: Record the decision for future reference.

Check for an active ADR session:

```bash
cat .adr-session.json 2>/dev/null
```

**If ADR exists**: Append a decision record (statement, options, winner, key reasoning, confidence, date) to the ADR's decisions section.

**If no ADR**: Note the decision in the active task plan (`plan/active/*.md`). If neither exists, present the record to the user for manual recording.

The user can skip persistence for informal exploration by requesting it.

**Gate**: Decision recorded or presented. Workflow complete.

---

## Error Handling

### Error: "Too many options"
**Cause**: User presents 5+ options
**Solution**: Help decompose. Group similar options or eliminate clearly inferior ones first. Then score the remaining 2-4.

### Error: "Criteria don't fit this decision"
**Cause**: Default criteria aren't relevant (e.g., scoring a content strategy, not a technical choice)
**Solution**: Ask the user to define custom criteria. Suggest domain-appropriate alternatives.

### Error: "Scores feel wrong"
**Cause**: User disagrees with a score after seeing the matrix
**Solution**: Adjust the score and recalculate. The matrix is a tool for the user, not an authority over them. If many scores feel wrong, the criteria may need revisiting.

---

## References

- Repository CLAUDE.md files (read before execution for project-specific constraints)

### Reference Loading Table

Load these files when the corresponding signals appear in the decision request:

| Signal | Reference File | What It Adds |
|--------|---------------|-------------|
| "build vs buy", "vendor", "SaaS", "self-host", database, cloud provider, framework, library, API design | `references/decision-archetypes.md` | Archetype-specific criteria weight adjustments, hard-constraint checklists, detection commands |
| User adjusts weights after scoring, adds options mid-scoring, scores feel arbitrary, "something feels off" | `references/decision-preferred-patterns.md` | Failure mode identification, intervention scripts, error-fix mappings |
| 5+ options presented, close call (<0.5 margin), repeated score changes | `references/decision-preferred-patterns.md` | Structural failure modes and fixes |
