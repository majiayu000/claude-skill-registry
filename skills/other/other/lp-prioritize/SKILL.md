---
name: lp-prioritize
description: Startup go-item ranking - score and select top 2-3 items to pursue
---

# lp-prioritize: Startup Go-Item Ranking

**Purpose**: Score all candidate go-items (features, experiments, distribution bets, content) and select top 2-3 to pursue.

## Invocation

```
/lp-prioritize --business <BIZ>
```

**Business resolution pre-flight:** If `--business` is absent or the directory `docs/business-os/strategy/<BIZ>/` does not exist, apply `_shared/business-resolution.md` before any other step.

Optional flags:
- `--max <N>` - select top N items (default 2-3)
- `--backlog <PATH>` - include existing backlog items

## Operating Mode

**READ + RANK + RECOMMEND**

This skill reads candidate go-items from upstream outputs (lp-readiness, lp-offer, lp-forecast), scores them on 3 dimensions, ranks by combined score, and selects top 2-3 with rationale.

## Differs from lp-do-idea-generate

**CRITICAL**: This is NOT a renamed lp-do-idea-generate. Key differences:

1. **Simple rank-and-pick vs 7-stage pipeline**: No Cabinet Secretary, no multi-lens expert passes, no clustering, no Munger/Buffett filter. Just: list candidates → score → rank → pick top 2-3.

2. **3 scoring dimensions vs 12+ sub-experts**: Scores by effort, impact, and learning-value only. No persona-based expert evaluation (no Product Strategist, no Growth Hacker, no Financial Analyst, etc.).

3. **Includes experiment + distribution candidates**: lp-do-idea-generate focuses on business ideas. lp-prioritize ranks ALL go-items: product features, experiments, distribution bets, content pieces, operational improvements.

4. **Direct output to lp-do-fact-find**: Ranked list feeds directly into lp-do-fact-find for the top items. No card creation, no idea persistence, no DGPs.

5. **100-150 lines vs 1200+ lines**: Deliberately lightweight for startups with 5-10 candidates, not enterprise backlogs with hundreds of items.

## Inputs

**Required**:
- Business context: current stage, constraints, budget, team size
- Candidate go-items from:
  - lp-readiness output (capability gaps, quick wins)
  - lp-offer output (feature candidates, positioning experiments)
  - lp-forecast output (distribution experiments, content bets)
  - Existing backlog (if provided via `--backlog`)

**Optional (S3B)**:
- `docs/business-os/strategy/<BIZ>/lp-other-products-results.user.md` — if present (human-produced after running the S3B prompt in a deep research tool), extract product candidates from the Track 4 top-5 shortlist as additional go-items. Score them through the standard Effort/Impact/Learning-Value rubric alongside feature and distribution bet candidates. Source label: `S3B lp-other-products`.

**Candidate shape**: Each item must have title, description, and source (which upstream output it came from).

## Scoring Dimensions

**Effort** (1-5): How much work? Time, complexity, dependencies. Lower = better.
- 1 = <1 week, no dependencies, trivial complexity
- 3 = 2-4 weeks, moderate dependencies, medium complexity
- 5 = >8 weeks, heavy dependencies, high complexity

**Impact** (1-5): How much business value? Revenue potential, learning value, risk reduction. Higher = better.
- 1 = Minimal value, nice-to-have
- 3 = Moderate value, supports growth
- 5 = Game-changer, unlocks new market/revenue

**Learning-Value** (1-5): How much do we learn? Hypothesis validation, market signal, capability building. Higher = better.
- 1 = Low learning, known outcome
- 3 = Moderate learning, tests hypothesis
- 5 = High learning, validates core assumption

**Combined score**: `(Impact + Learning-Value) / Effort`

Higher combined score = better ROI on time/effort.

## Hypothesis Portfolio Bridge (Optional)

When candidate records include explicit hypothesis linkage, `/lp-prioritize` can inject portfolio-normalized scoring:

- Linkage forms:
  - `hypothesis_id: <id>`
  - tag `hypothesis:<id>`
- Linked + portfolio metadata present:
  - score via hypothesis portfolio bridge mapping (normalized to 1-5)
- Linked + blocked hypothesis:
  - surface explicit blocked reason
  - apply neutral/zero injection (per bridge output) instead of silent fallback
- Linked + metadata missing:
  - do not fail run; keep baseline score and mark as `metadata_missing`
- Unlinked:
  - keep baseline formula unchanged

Reference implementation: `scripts/src/hypothesis-portfolio/prioritize-bridge.ts`

## Workflow

**Stage 1: Collect Candidates**
- Read all upstream outputs (lp-readiness, lp-offer, lp-forecast)
- Extract candidate go-items (features, experiments, bets)
- Include backlog items if `--backlog` provided
- Normalize to standard shape (title, description, source)

**Stage 2: Score Each Candidate**
- For each item, assign:
  - Effort score (1-5)
  - Impact score (1-5)
  - Learning-Value score (1-5)
- Calculate combined score: (Impact + Learning-Value) / Effort
- Write brief rationale for each score

**Stage 3: Rank by Combined Score**
- Sort candidates by combined score (descending)
- Break ties by: Impact > Learning-Value > lower Effort

**Stage 4: Select Top 2-3**
- Take top N items (default 2-3, or `--max` if provided)
- For each selected item:
  - Write acceptance criteria (how we know it's done)
  - Estimate effort (person-weeks)
  - Identify dependencies
- For non-selected top items, write "Why not" notes

**Stage 5: Produce Ranked Output**
- Output markdown table with all scored items
- Output selected items with detail
- Output "Why not" notes for next-tier items

## Output Contract

**Ranked Table** (all candidates):

```markdown
| Rank | Item | Source | Effort | Impact | Learning | Score | Rationale |
|------|------|--------|--------|--------|----------|-------|-----------|
| 1    | ... | ...    | 2      | 5      | 4        | 4.5   | ...       |
```

**Selected Items** (top 2-3):

For each selected item:
- **Title**: [item name]
- **Source**: [which output it came from]
- **Why selected**: [rationale based on scores]
- **Acceptance criteria**: [how we know it's done]
- **Estimated effort**: [person-weeks]
- **Dependencies**: [what must be true first]

**Why Not Selected** (next-tier items):

For items ranked 4-6:
- **Title**: [item name]
- **Why not**: [reason not selected despite good score]

## Quality Checks

Before outputting, verify:
- [ ] All candidates scored on 3 dimensions (effort, impact, learning-value)
- [ ] Combined scores calculated correctly
- [ ] Top 2-3 items have acceptance criteria and effort estimates
- [ ] "Why not" notes for next-tier items (if applicable)
- [ ] Rationale for each score is brief and concrete
- [ ] No ties in ranking (all ties broken by tiebreaker rule)

## Red Flags

Invalid output:
- More than 5 items selected (defeats focus)
- No rationale for scores (just numbers)
- No acceptance criteria for selected items
- Effort/Impact/Learning-Value scores outside 1-5 range
- Combined score not calculated as (Impact + Learning-Value) / Effort

## Integration

**Downstream**: Output feeds directly into `/lp-do-fact-find` for the selected top 2-3 items. Each selected item becomes a fact-find target.

**Upstream**: Reads from:
- `/lp-readiness` (capability gaps, quick wins)
- `/lp-offer` (feature candidates, positioning experiments)
- `/lp-forecast` (distribution experiments, content bets)

**Persistence**: No card creation, no idea persistence. This is a one-shot ranking for current loop cycle. Next cycle re-runs from scratch.

## Example Invocation

```bash
/lp-prioritize --business BRIK --max 3
```

Expected output:
1. Ranked table of all candidates (8-12 items typical)
2. Top 3 selected items with acceptance criteria and effort
3. "Why not" notes for items 4-6
4. Ready to pipe selected items into `/lp-do-fact-find`
