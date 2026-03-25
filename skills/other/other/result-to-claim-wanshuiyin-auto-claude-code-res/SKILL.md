---
name: "result-to-claim"
description: "Use when experiments complete to judge what claims the results support, what they do not support, and what evidence is still missing. A secondary Codex reviewer evaluates the results and routes the next action."
---

# Result-to-Claim Gate

Experiments produce numbers; this gate decides what those numbers mean.

## Context: $ARGUMENTS

## When to Use

- After a set of experiments completes
- Before committing to claims in a paper or review response
- When results are ambiguous and you need an objective second opinion

## Workflow

### Step 1: Collect Results

Gather experiment data from whatever sources are available:

1. **W&B** (preferred): metrics, training curves, comparisons
2. **EXPERIMENT_LOG.md**: full results table with baselines and verdicts
3. **EXPERIMENT_TRACKER.md**: which experiments are done vs still running
4. **Log files**: direct tails if no other source exists
5. **docs/research_contract.md** or project notes: intended claims and experiment design

Assemble:

- What experiments were run
- Main metrics and baseline comparisons
- The intended claim being tested
- Known confounds or caveats

### Step 2: Secondary Reviewer Judgment

```text
spawn_agent:
  model: gpt-5.4
  reasoning_effort: xhigh
  message: |
    RESULT-TO-CLAIM EVALUATION

    I need you to judge whether experimental results support the intended claim.

    Intended claim: [the claim these experiments test]
    Experiments run:
    [list experiments with method, dataset, metrics]

    Results:
    [paste key numbers, comparison deltas, significance]

    Baselines:
    [baseline numbers and sources]

    Known caveats:
    [confounds, limited datasets, missing comparisons]

    Please evaluate:
    1. claim_supported: yes | partial | no
    2. what_results_support
    3. what_results_dont_support
    4. missing_evidence
    5. suggested_claim_revision
    6. next_experiments_needed
    7. confidence: high | medium | low

    Be honest. Do not inflate claims beyond what the data supports.
```

### Step 3: Parse and Normalize

Extract structured fields:

```markdown
- claim_supported: yes | partial | no
- what_results_support: "..."
- what_results_dont_support: "..."
- missing_evidence: "..."
- suggested_claim_revision: "..."
- next_experiments_needed: "..."
- confidence: high | medium | low
```

### Step 4: Route Based on Verdict

#### `no`

1. Record a postmortem in `findings.md`
2. Update project notes / tracker status
3. Decide whether to pivot to the next idea or try an alternative approach

#### `partial`

1. Update the working claim to reflect what is actually supported
2. Record the gap in `findings.md`
3. Design and run supplementary experiments
4. Re-run `/result-to-claim` after the supplementary experiments complete

#### `yes`

1. Record the confirmed claim in project notes
2. If ablations are incomplete, trigger `/ablation-planner`
3. If all evidence is in, move to paper writing

## Rules

- The secondary reviewer is the judge; the main agent collects evidence and routes the next action.
- Do not inflate claims beyond what the data supports.
- A single positive result on one dataset does not support a general claim.
- If confidence is low, treat the judgment as inconclusive and add experiments instead of committing to the claim.
- Always record the verdict and reasoning in `findings.md`, regardless of outcome.
