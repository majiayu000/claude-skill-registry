---
name: ice-score
description: "Use to prioritize solutions or opportunities using ICE scoring with evidence-backed confidence."
metadata:
  instruction_budget: "35"
---

# ICE Score Skill

ICE scoring with integrated confidence meter.

## Preflight: Read target canvas file(s) before any Write/Edit

**Hard rule.** Before issuing `Write` or `Edit` against any `.claude/canvas/*.yml`, use the **Read tool** on that file in this session. Claude Code's Read-before-Write check requires the `Read` tool specifically — `cat`/`head`/`grep` via Bash do NOT satisfy it.

**Edit vs Write — different cost profiles** (verified 2026-05-14):
- **`Edit`** (exact-string replacement): `Read` with `limit: 1` satisfies the check at ~50 tokens. State-tracking is per-file, not per-byte — subsequent `Edit` calls work anywhere in the file. Use this for partial updates against large canvas files (e.g., `purpose.yml` at 800+ lines).
- **`Write`** (full replacement): do a **full Read** first. Write obliterates the file; you should see what you're about to replace. The `limit:1` shortcut is *not* appropriate here.

**ID-bearing entries — scan the ID space before assigning** (added 2026-05-15, v0.23.19): When adding a new component, opportunity, solution, or any other ID-bearing entry to a canvas file, run a Bash grep first to confirm the next ID in your prefix sequence is actually free:

```
grep "^  - id: <prefix>-" .claude/canvas/<file>.yml | sort -u
```

Replace `<prefix>` with the canvas's ID prefix (`comp` for landscape, `opp` for opportunities, `sol` for solutions, `ht` for human-tasks, etc.). Then pick the next free integer. `validate_canvas.py` has a duplicate-ID check (lines 230-239) that catches the failure on CI, but a duplicate can persist in the working tree for days if CI isn't run between edit and discovery — see roadmap-repo `corrections.md` 2026-05-15 "Duplicate canvas ID created in landscape.yml" for the worked example.

Original failure mode: anti-pattern #7 instance #5, 2026-05-09 — agent conflated Bash `head` with the Read tool, lost ~14k tokens to a Write-fail → remedial-full-Read → re-Write loop. The `limit:1` discipline (graduated 2026-05-14, v0.23.18) prevents the second-order cost where the agent *correctly* follows the rule but full-Reads every time. The ID-scan discipline (graduated 2026-05-15, v0.23.19) prevents the related class where the agent reads enough of the file to satisfy the Edit check but not enough to see existing ID assignments — kin to anti-pattern #8 (Stale State Read).

If this skill writes to multiple canvas files, register each one first (limit:1 for Edit-only paths; full Read for Write paths) AND ID-scan any prefix you intend to assign.

See `CLAUDE.md` *Canvas writes — Read before Write* for the canonical rule.

## Workflow

ICE scoring is applied to **OST solution leaves**. Each leaf must have a Four Risks assessment (Torres Product Trio) before it can be scored — the risks are the inputs, ICE is the output.

### Step 1: Verify Four Risks exist

For each solution leaf in `.claude/canvas/opportunities.yml`, check that `four_risks` has been assessed:
- **Value** (product lens): Do users want/need this?
- **Usability** (design lens): Can users figure it out?
- **Feasibility** (engineering lens): Can we build it within constraints?
- **Viability** (cross-cutting): Does it align with business/legal/ethical constraints?

If any risk dimension is missing, assess it first. Each dimension must have its own evidence — a single combined statement fails (Torres Product Trio rule).

### Step 2: Derive ICE from the Four Risks

For each solution, score three dimensions (1-10):

**Impact** — derived from value + usability + viability risks:
- What does the value risk assessment say about user demand?
- What does the usability assessment say about adoption likelihood?
- What does the viability assessment say about business alignment?
- 1-3: Low value evidence, high usability risk, or poor viability fit
- 4-6: Moderate value evidence, some usability unknowns
- 7-10: Strong value evidence, low usability risk, clear viability

**Confidence** — how well-tested are the risk assessments?

> *Scale note: Mycelium uses 0.0-1.0. Gilad's original Confidence Meter uses 0-10 non-linear (0.01=opinion, 1=anecdotal, 5=market data, 8=A/B test, 10=launch data). The non-linear penalty is preserved through evidence-class weighting.*
- 1-3: Risk assessments based on gut feel or desk research
- 4-6: Some direct evidence (interviews, analogues, small tests)
- 7-10: Strong evidence (user tests, prototypes, data). Requires test-validated evidence.

**Ease** — derived from feasibility risk:
- What does the engineering assessment say about complexity?
- What dependencies, unknowns, or technical spikes were identified?
- 1-3: High feasibility risk. Major unknowns, new capabilities needed.
- 4-6: Moderate feasibility risk. Known patterns, some complexity.
- 7-10: Low feasibility risk. Quick win, existing patterns.

### Step 3: Calculate and rank

ICE = Impact x Confidence x Ease. Rank solution leaves by ICE score.

### Step 4: Identify riskiest assumptions

For the top-ranked solutions, extract the **highest-risk assumptions** from the Four Risks assessment — these are what `/mycelium:assumption-test` should target first. Prioritize assumptions where importance is high but evidence is low.

### Step 5: Bias check

Are high-scoring items benefiting from availability bias, IKEA effect, anchoring, or **hyperbolic discounting** (overweighting near-term Impact at the expense of longer-horizon outcomes)? Review for bias after scoring, before acting. *Source for hyperbolic discounting: Laibson, "Golden Eggs and Hyperbolic Discounting" (1997) — when the Impact dimension is rewarded for "what we can ship this sprint," delayed-payoff opportunities get systematically under-scored.*

### Output

```
| Solution | Value | Usability | Feasibility | Viability | I | C | E | ICE | Riskiest Assumption |
|----------|-------|-----------|-------------|-----------|---|---|---|-----|---------------------|
| ...      | risk  | risk      | risk        | risk      | X | X | X | XXX | [what to test]      |
```

## Rules
- Every ICE score must trace back to a Four Risks assessment — no scoring without risk evaluation first.
- Each risk dimension must have separate evidence (Product Trio rule).
- Confidence of 7+ requires test-validated evidence, not analogy or assumption.
- If all items score similarly, the risk assessments need more depth.
- Review for bias after scoring, before acting.

## Canvas Output
Update `.claude/canvas/opportunities.yml` — write `four_risks` and `ice_score` per solution leaf.
Update `.claude/canvas/gist.yml` with idea ICE scores and confidence levels.

## Theory Citations
- Ellis: ICE scoring (Impact × Confidence × Ease — Sean Ellis invented the ICE framework as part of growth methodology)
- Gilad: Evidence-Guided (Confidence Meter — the evidence-grading layer on top of Ellis's ICE, mapping evidence types to confidence levels)
- Torres: Continuous Discovery Habits (OST leaves as unit of evaluation)
- Torres: Product Trio (three perspectives feeding risk assessment)
- Cagan: Inspired (Four Risks as structured evaluation)
- Kahneman: Thinking, Fast and Slow (bias in estimation)
- Kahneman, Sibony & Sunstein: Noise (2021) — unwanted variability in judgment (see Noise Check below)

### Noise Check (Kahneman, Sibony & Sunstein, 2021)

ICE scores are susceptible to **noise** — unwanted variability where different sessions or assessors produce different scores for the same evidence. Unlike bias (systematic skew in one direction), noise is random scatter.

**Detection**: Re-score the same evidence independently (different session or assessor) and compare. If scores diverge by >1 point on any dimension, investigate why before proceeding.

**Mitigation**: Use structured assessment criteria (the Four Risks inputs above), apply scores independently before discussion, and anchor to evidence types rather than gut feel.

**Noise audit procedure**: Score the same evidence independently twice (different session or different assessor). If ICE scores diverge by >1 point on any dimension, the gap is noise — investigate the scoring criteria before proceeding. For solo developers: re-score after a 24h break to detect temporal noise.
