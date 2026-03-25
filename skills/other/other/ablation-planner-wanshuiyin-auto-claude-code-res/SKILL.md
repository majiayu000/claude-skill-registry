---
name: "ablation-planner"
description: "Use when main results pass result-to-claim (claim_supported=yes or partial) and ablation studies are needed for paper submission. A secondary Codex reviewer designs ablations from a reviewer's perspective, while the main agent checks feasibility and implementation."
---

# Ablation Planner

Systematically design ablation studies that answer the questions reviewers will ask.

## Context: $ARGUMENTS

## When to Use

- Main results pass `/result-to-claim` with `claim_supported = yes` or `partial`
- The user explicitly requests ablation planning
- `/auto-review-loop` identifies missing ablations

## Workflow

### Step 1: Prepare Context

Read available project files to build the full picture:

- Method description and components from `docs/research_contract.md`, project notes, or `AGENTS.md`
- Current experiment results from `EXPERIMENT_LOG.md`, `EXPERIMENT_TRACKER.md`, or W&B
- Confirmed and intended claims from `result-to-claim` output or project notes
- Available compute resources from project notes or environment config

### Step 2: Secondary Reviewer Designs Ablations

```text
spawn_agent:
  model: gpt-5.4
  reasoning_effort: xhigh
  message: |
    You are a rigorous ML reviewer planning ablation studies.
    Given this method and results, design ablations that:

    1. Isolate the contribution of each novel component
    2. Answer questions reviewers will definitely ask
    3. Test sensitivity to key hyperparameters
    4. Compare against natural alternative design choices

    Method: [description from project files]
    Components: [list of removable/replaceable components]
    Current results: [key metrics from experiments]
    Claims: [what we claim and current evidence]

    For each ablation, specify:
    - name: what to change
    - what_it_tests: the specific question this answers
    - expected_if_component_matters: what we predict if the component is important
    - priority: 1 (must-run) to 5 (nice-to-have)

    Also provide:
    - coverage_assessment
    - unnecessary_ablations
    - suggested_order
    - estimated_compute
```

### Step 3: Parse Ablation Plan

Normalize the response into:

```markdown
## Ablation Plan

### Component Ablations
| # | Name | What It Tests | Expected If Matters | Priority |
|---|------|---------------|---------------------|----------|

### Hyperparameter Sensitivity
| # | Parameter | Values to Test | What It Tests | Priority |
|---|-----------|---------------|---------------|----------|

### Design Choice Comparisons
| # | Name | What It Tests | Priority |
|---|------|---------------|----------|

### Coverage Assessment
[what reviewer questions these ablations answer]

### Unnecessary Ablations
[what to skip]

### Run Order
[optimized order]

### Estimated Compute
[total GPU-hours]
```

### Step 4: Review Feasibility

Before running anything, check:

- Compute budget
- Which ablations are config-only vs code-change
- Which ablations can run in parallel
- What should be cut first if budget is too tight

### Step 5: Implement and Run

1. Create configs/scripts for each ablation
2. Smoke test each ablation before the full run
3. Run in suggested order with descriptive names
4. Track results in `EXPERIMENT_LOG.md`
5. After completion, update findings with the ablation insights

## Rules

- The secondary reviewer leads the ablation design. Do not pre-filter the ablation list before the reviewer sees it.
- Every ablation must have a clear `what_it_tests` and `expected_if_component_matters`.
- Config-only ablations take priority over ablations that require code changes.
- If total compute exceeds budget, propose cuts explicitly instead of silently dropping ablations.
- Component ablations take priority over broad hyperparameter sweeps.
- Record all ablation results, including negative ones.
