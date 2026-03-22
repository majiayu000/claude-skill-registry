---
name: agentv-eval-analyzer
description: Analyze evaluation results for quality improvements — identify LLM-judge evaluators replaceable with deterministic assertions, flag weak/vague assertions, and surface cost/quality opportunities. Use after running evals to improve your evaluation config.
---

# AgentV Eval Analyzer

Analyze JSONL evaluation results and produce actionable suggestions for improving eval quality, reducing cost, and increasing reliability.

## When to Use

- After running `agentv eval` and wanting to improve your evaluation config
- When evaluations are slow or expensive and you suspect LLM-judges are doing deterministic work
- When reviewing eval quality before sharing or publishing evaluation files
- When triaging flaky evaluations that produce inconsistent scores

## Quick Start

```bash
# Find your most recent results file
agentv trace list --limit 5

# Dispatch the eval-analyzer agent with the results file
# Agent: eval-analyzer
# Parameters:
#   results-file: <path-to-results.jsonl>
#   eval-path: <path-to-eval.yaml>  (optional, for deeper analysis)
```

**Dispatch the `eval-analyzer` agent** with:
- `results-file`: Path to the JSONL results (from `.agentv/results/` or `agentv trace list`)
- `eval-path` (optional): Path to the EVAL.yaml for assertion-level analysis

The agent produces a read-only report — it never modifies files.

## What It Detects

### 1. Deterministic-Upgrade Candidates (highest value)

LLM-judge evaluators doing work that a deterministic assertion could handle — cheaper, faster, and more reliable.

| Pattern in LLM-Judge Reasoning | Suggested Deterministic Type |
|-------------------------------|------------------------------|
| "Output contains 'X'" — always cites same substring | `type: contains`, `value: "X"` |
| Score always 0 or 1, never partial — binary check | `type: equals` or specific deterministic |
| "Response is valid JSON" — format validation | `type: is-json` |
| "Output starts with 'Error:'" — prefix check | `type: regex`, `value: "^Error:"` |
| "Matches pattern /regex/" — regex match | `type: regex`, `value: "/pattern/"` |
| All passed assertions are substring presence checks | Multiple `type: contains` assertions (one per value) |

### 2. Weak Assertion Detection

| Weakness | Example | Fix |
|----------|---------|-----|
| Vague (< 8 words, no specifics) | "Response is good" | Add measurable criteria |
| Tautological | "Output is correct" | Define what "correct" means with expected values |
| Compound | "Handles errors and returns JSON" | Split into separate assertions |
| Overly broad LLM-judge | Single vague `prompt` string | Use `type: rubrics` with enumerated items |

### 3. Cost/Quality Flags

| Flag | Meaning |
|------|---------|
| Expensive binary check | LLM-judge always returns 0 or 1 → deterministic replacement |
| Always-pass | Score 1.0 on every test → criteria may be too lenient |
| Always-fail | Score 0.0 on every test → criteria may be misconfigured |
| Redundant evaluators | Two evaluators with identical scores/reasoning → merge |

### 4. Multi-Provider Variance

When results span multiple targets, flags evaluators with > 0.3 score variance across providers — indicating provider-sensitive assertions that may need tightening.

## Applying Suggestions

The analyzer report includes concrete YAML snippets for each suggestion. To apply:

1. Open the EVAL.yaml referenced in the report
2. Find the `assertions` entry for the flagged evaluator (matched by `name` and `test_id`)
3. Replace or supplement the evaluator config with the suggested deterministic assertion
4. Re-run `agentv eval` to verify the change produces equivalent scores

**Example upgrade:**

Before (LLM-judge doing substring work):
```yaml
assertions:
  - name: has-error-code
    type: llm-judge
    prompt: "Check if the response contains the error code 404"
```

After (deterministic, zero LLM cost):
```yaml
assertions:
  - name: has-error-code
    type: contains
    value: "404"
```

## Limitations

- Deterministic-upgrade detection is heuristic — review suggestions before applying
- Requires at least one completed eval run (needs JSONL results)
- Cannot detect all weak assertions without the EVAL.yaml file (results-only mode has reduced coverage)
- Multi-run comparison (flakiness across runs) is out of scope — use `agentv compare` for that
