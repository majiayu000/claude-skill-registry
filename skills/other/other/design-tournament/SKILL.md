---
name: design-tournament
description: Run a parallel diverge-then-converge design tournament — 3-5 independent agents explore a problem, then 2 ranking agents evaluate and stack-rank the results with confidence scores
---

# Design Tournament

A two-phase "wisdom of crowds" pattern for design work. Multiple independent
agents explore the same problem in isolation, then independent rankers evaluate
and merge the findings into a confidence-weighted stack ranking.

## When to Use

- Designing a new feature, data structure, algorithm, or API
- Exploring multiple valid architectural approaches
- Story/task breakdown where the "right" decomposition isn't obvious
- Any design decision where independent perspectives reduce blind spots

## Invocation

```
design-tournament <problem statement>
```

The `<problem statement>` is the full description of what needs to be designed.
If no argument is given, ask the user for the problem statement before
proceeding.

## Phase 1 — Diverge (Parallel Exploration)

Launch **5 independent agents in parallel** using the Codex agent tools (`spawn_agent`, `send_input`, `wait`) with
`agent_type=default`. Every agent receives **identical instructions**
so that their outputs are independently generated with zero cross-contamination.

**All 5 agents MUST be launched in a single message** (one message, five `spawn_agent` calls) so they run concurrently.

### Agent Prompt Template (identical for all 5)

Each agent receives this prompt, with `{PROBLEM}` replaced by the user's
problem statement and `{AGENT_ID}` set to a unique label (Alpha, Beta, Gamma,
Delta, Epsilon):

```
You are Design Agent {AGENT_ID} in an independent design tournament.

## Problem
{PROBLEM}

## Your Task

Produce a COMPLETE, standalone design proposal. You are working independently —
do not assume anyone else's output exists.

### Required Sections

1. **Problem Restatement** — Restate the problem in your own words to confirm
   understanding. Call out any ambiguities or assumptions you are making.

2. **Design Proposal** — Your recommended design. Include:
   - Core idea / approach (1-2 sentence summary)
   - Detailed description with concrete types, signatures, or pseudocode
   - Key invariants or contracts the design enforces
   - How the design handles edge cases and failure modes

3. **Alternatives Considered** — At least 2 alternative approaches you
   evaluated and why you rejected them.

4. **Trade-offs** — Explicit trade-off analysis:
   - What does this design optimize for?
   - What does it sacrifice?
   - Under what conditions would a different design be better?

5. **Risks & Open Questions** — What could go wrong? What remains uncertain?

6. **Self-Assessment** — Rate your own confidence (0-100) in this design and
   explain why.

### Rules

- Be specific and concrete — pseudocode or type signatures over hand-waving.
- Do NOT hedge with "it depends" — commit to a design and defend it.
- Explore the codebase if you need context (use `rg --files`, `rg`, and targeted file reads).
- Aim for depth over breadth. One well-defended design beats three sketches.

### Output Format

Return your response as a single markdown document with the sections above.
Start with: `# Design Proposal — Agent {AGENT_ID}`
```

### Collecting Results

After all 5 agents complete, gather their outputs. If any agent fails or times
out, proceed with the agents that succeeded (minimum 3 required).

## Phase 2 — Converge (Parallel Ranking)

Launch **2 independent ranking agents in parallel** using the Codex agent tools (`spawn_agent`, `send_input`, `wait`) with
`agent_type=default`. Both receive **identical instructions** and
the collected Phase 1 outputs.

**Both rankers MUST be launched in a single message** (one message, two `spawn_agent` calls) so they run concurrently.

### Ranker Prompt Template (identical for both)

```
You are Ranking Judge {JUDGE_ID} in a design tournament.

## Original Problem
{PROBLEM}

## Design Proposals

Below are {N} independently generated design proposals for the same problem.
Evaluate them WITHOUT knowing which agent produced each one (they are labeled
Alpha through Epsilon for reference only).

{PROPOSALS}

## Your Task

### 1. Evaluation Criteria

Score each proposal on these dimensions (1-10 scale):

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Correctness** | 25% | Does the design actually solve the problem? Are invariants sound? |
| **Simplicity** | 20% | Is this the simplest design that could work? Minimal moving parts? |
| **Robustness** | 20% | How well does it handle edge cases, failures, and adversarial inputs? |
| **Extensibility** | 15% | Can the design accommodate likely future requirements without rework? |
| **Specificity** | 10% | How concrete and implementable is the proposal? |
| **Trade-off Awareness** | 10% | Does the author understand what they're sacrificing? |

### 2. Per-Proposal Evaluation

For EACH proposal, provide:
- Scores on each criterion
- Weighted total score
- Top strength (1 sentence)
- Top weakness (1 sentence)
- Key insight unique to this proposal (if any)

### 3. Stack Ranking

Produce a final ranking from best to worst. For each position:
- Rank position (1 = best)
- Agent label
- Weighted total score
- Confidence in this ranking position (0-100):
  - 90-100: Clear winner/loser, large score gap
  - 70-89: Solid ranking, meaningful score gap
  - 50-69: Close call, could reasonably swap with adjacent rank
  - Below 50: Essentially tied, ranking is arbitrary

### 4. Synthesis Recommendation

After ranking, provide:
- **Recommended design**: Which proposal to use as the starting point
- **Cherry-pick list**: Specific ideas from OTHER proposals that should be
  incorporated into the winner
- **Composite confidence** (0-100): Your overall confidence that the #1
  ranked proposal (with cherry-picks) is the right design

### Rules

- Judge designs on MERIT, not on writing quality or verbosity.
- If two designs are substantively identical, say so — don't force a
  false distinction.
- Be willing to rank a simple, correct design above an elaborate one.
- Explore the codebase if you need context to evaluate feasibility.

### Output Format

Return your response as a single markdown document.
Start with: `# Ranking Report — Judge {JUDGE_ID}`
```

### Merging Rankings

After both rankers complete, merge their results:

1. **For each proposal**, average the weighted scores from both judges.
2. **For each rank position**, compute:
   - Average score
   - Agreement: did both judges assign the same rank? (yes/no)
   - Combined confidence: average of both judges' per-position confidence,
     reduced by 15 points if they disagree on rank position
3. **Final stack ranking** by averaged weighted score (descending).
4. **Synthesize cherry-pick lists** from both judges into a unified list.

## Final Output Format

Present the merged result to the user as:

```markdown
## Design Tournament Results

### Problem
{one-line restatement}

### Stack Ranking

| Rank | Agent | Avg Score | Judge Agreement | Confidence | Key Strength |
|------|-------|-----------|-----------------|------------|--------------|
| 1    | ...   | 8.2/10    | Yes             | 92%        | ...          |
| 2    | ...   | 7.5/10    | Yes             | 78%        | ...          |
| 3    | ...   | 6.8/10    | No (J1:#2,J2:#4)| 54%       | ...          |
| ...  | ...   | ...       | ...             | ...        | ...          |

### Recommended Design

**Base**: Agent {winner}'s proposal
**Cherry-picks from other proposals**:
- From Agent X: {specific idea}
- From Agent Y: {specific idea}

**Composite Confidence**: {average of both judges' composite}%

### Winning Proposal Summary
{2-3 paragraph summary of the #1 design with cherry-picks integrated}

### Full Proposals (collapsed)
<details><summary>Agent Alpha — Score: X.X</summary>
{full proposal text}
</details>
{repeat for each agent}

### Ranking Details (collapsed)
<details><summary>Judge 1 Report</summary>
{full ranking report}
</details>
<details><summary>Judge 2 Report</summary>
{full ranking report}
</details>
```

## Configuration

The default is 5 explorers + 2 rankers (7 total agents). If the user specifies
a different count (e.g., `design-tournament 3 agents: ...`), respect it but
enforce these minimums:
- Phase 1: at least 3 explorer agents
- Phase 2: always exactly 2 ranking agents

## Tips

- For large or ambiguous problems, include relevant file paths or context in
  the problem statement so explorer agents can read the codebase.
- If the problem involves existing code, tell agents which files to examine.
- The skill works for any design task: features, data structures, algorithms,
  API shapes, system architecture, task decomposition, migration plans.
