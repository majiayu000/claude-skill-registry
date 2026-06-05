---
name: execution-grounded-selection
description: >
  Pick among candidate outputs (code, configs, plans) by running them on
  diverse inputs and clustering by behavioural fingerprint, rather than
  by textual aggregation or log-probability. Activates when an executor
  returns multiple plausible candidates that need disambiguation, when
  output-majority voting would be the default choice, or when reviewing
  generated code that has not yet been validated. The 2026 evidence
  (Semantic Voting, arxiv 2605.08680v1) is that any execution-based
  selector dominates output-majority voting by 19-52pp; sketch-generated
  inputs beat random fuzz by 11.3pp. Triggers: "pick the best candidate",
  "majority vote on code", "select from N samples", "validate the
  generated output", "behavioural verification".
user-invocable: true
version: 1.0.0
format: 2025-10-02
triggers:
  - "pick the best candidate"
  - "majority vote on code"
  - "select from N samples"
  - "validate the generated output"
  - "behavioural verification of code"
updated: 2026-05-16
status: ACTIVE
source: arxiv 2605.08680v1 (Semantic Voting), 2605.07248v1 (Plan-on-Trigger)
---

# Execution-Grounded Selection

## Why

Output-majority voting (pick the most common string output) is dominated by *any* selector that actually runs the candidates. Semantic Voting (arxiv 2605.08680v1) shows 19-52pp improvement over output voting across multiple code benchmarks. The specific aggregation rule (majority, weighted, MBR-Exec) is statistically indistinguishable once execution evidence is present — *execution is the dominant signal, aggregation is the residual*.

This is the code-domain analogue of the **noise-as-exploration** Rosetta concept: execution diversity is the exploration mechanism; behavioural fingerprint is the equilibrium signal.

## How

The Semantic Voting pipeline:

1. **Sample N candidates** — generate at temperature > 0 (typical N = 5-10).
2. **Generate diverse inputs** — sketch-generated inputs (derived from candidate population structure) beat random fuzz by ~11pp. If sketch generation is infeasible, fall back to LLM-generated test inputs > random fuzz.
3. **Execute each candidate on each input** — collect (candidate_i, input_j, output_ij) tuples. Crash counts as a distinct fingerprint, not a discard.
4. **Cluster by fingerprint** — equivalence on `[output_ij for j in inputs]` defines the cluster.
5. **Pick the largest cluster** — break ties by candidate self-confidence or by Pareto on execution cost.

## When to skip

- Generation is deterministic (temperature = 0) — there's nothing to select among.
- Execution is expensive or has side effects (touches the network, modifies state) — fall back to dry-run / static analysis.
- The output isn't executable (e.g., natural-language summary) — use paired-trace audit instead.

## Integration

- `wrap:verify` and `gsd-verify-work` — pre-merge gate when verification produces multiple candidate fixes.
- `gsd-code-fixer` — when the fixer proposes more than one fix per finding.
- `code-review` — adds a "did you actually run it?" subsection to the review rubric.

## Cross-references

- Rosetta concept #9 (Execution-Grounded Selection) — canonical definition
- College: `agent-systems / agentic-code-generation / agent-execution-grounded-selection`
- Related skills: `test-generator` (generates the inputs; pair with this skill for the full loop)
