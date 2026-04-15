---
name: paper-claim-audit
description: "Zero-context verification that every number, comparison, and scope claim in the paper matches raw result files. Uses a fresh cross-model reviewer with NO prior context to prevent confirmation bias. Use when user says \"审查论文数据\", \"check paper claims\", \"verify numbers\", \"论文数字核对\", or before submission to ensure paper-to-evidence fidelity."
argument-hint: [paper-directory]
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, mcp__codex__codex
---

# Paper Claim Audit: Zero-Context Evidence Verification

Verify that every claim in the paper matches raw evidence for: **$ARGUMENTS**

## Why This Exists

The executor writes experiments AND writes the paper. It "knows" what the results should be. This creates confirmation bias:
- Rounding 84.7% up to 85.3%
- Reporting best seed instead of average
- Citing metrics from a different experiment config
- Claiming "improves by 15%" when the delta is actually 12.8%

A **fresh reviewer with zero prior context** catches these because it has no expectations — it just compares paper text vs raw files.

## How This Differs From Other Audit Skills

| Skill | Question it answers |
|-------|-------------------|
| `/experiment-audit` | Is the experiment code honest? (fake GT, normalization fraud) |
| `/result-to-claim` | Does the data scientifically support this claim? |
| **`/paper-claim-audit`** | **Does the paper report the data truthfully and precisely?** |

## Core Principle

**Zero-context, fresh reviewer.** The auditor receives ONLY:
- Paper .tex files (the claims)
- Raw result files (the evidence)

It does NOT receive:
- ❌ EXPERIMENT_LOG.md
- ❌ EXPERIMENT_TRACKER.md
- ❌ AUTO_REVIEW.md
- ❌ NARRATIVE_REPORT.md
- ❌ Any executor summary or interpretation
- ❌ Any prior audit results
- ❌ Any conversation history

This is **stricter than reviewer-independence** — it's zero-context evidence audit.

## Workflow

### Step 1: Collect Files (Executor — Claude)

Locate paper and result files WITHOUT reading or interpreting them.

**Paper files** (claims):
```
paper/main.tex
paper/sections/*.tex
paper/tables/*.tex (if separate)
```

**Result files** (evidence):
```
results/*.json, results/*.jsonl, results/*.csv, results/*.tsv
outputs/*.json, outputs/*.csv
wandb-summary.json (if exists)
**/metrics.json, **/eval_results.json
**/config.yaml, **/args.json (experiment configs)
```

**Exclude** (no summaries, no interpretations):
```
EXPERIMENT_LOG.md, EXPERIMENT_TRACKER.md, AUTO_REVIEW*.md
NARRATIVE_REPORT.md, PAPER_PLAN.md, findings.md
Any .md file that is an executor-written summary
```

### Step 2: Fresh Reviewer Audit (GPT-5.4 — NEW thread, no reply)

**CRITICAL: Use `mcp__codex__codex` (new thread), NEVER `mcp__codex__codex-reply`.** Every run must be a fresh context.

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    You are a paper-to-evidence auditor. You have ZERO prior context about
    this research. You will receive only paper source files and raw result
    files. Your job is to verify that every number in the paper exactly
    matches the raw evidence.

    Paper files to read:
    [list .tex file paths]

    Result files to read:
    [list .json/.csv/.yaml file paths]

    ## Audit Protocol

    ### A. Extract Every Quantitative Claim
    For each number, percentage, comparison, or scope statement in the paper:
    - Location (section, table, caption, or inline text)
    - Exact claim text
    - The number or comparison being made

    ### B. Trace Each Claim to Evidence
    For each extracted claim, find the supporting raw data:
    - Which result file contains this number?
    - What is the EXACT value in that file?
    - Match status: exact_match / rounding_ok / mismatch

    ### C. Check These Specific Failure Modes

    1. **Number inflation**: Paper says 85.3%, raw file says 84.7%
       Rule: only standard rounding to displayed precision is allowed

    2. **Best-seed cherry-pick**: Paper says "achieves 90.2%" but
       that's the best of 5 seeds; mean is 87.1%
       Rule: check if paper specifies "average" / "best" / "median"

    3. **Config mismatch**: Paper compares Method A vs Baseline B,
       but they used different hyperparameters / datasets / splits
       Rule: verify config files show same settings for compared methods

    4. **Aggregation mismatch**: Paper says "average over 5 seeds"
       but result files show only 3 runs
       Rule: count actual runs vs claimed count

    5. **Delta error**: Paper says "improves by 15%" but
       actual delta is (85.3 - 73.1) / 73.1 = 16.7%
       Rule: verify arithmetic of all relative improvements

    6. **Caption-table mismatch**: Figure caption describes
       something different from what the figure/table actually shows
       Rule: cross-check every caption against its content

    7. **Scope overclaim**: Paper says "consistently outperforms"
       but only tested on 2 datasets
       Rule: check if language matches actual evaluation scope

    ## Output Format (per claim)
    For each claim, report:
    - claim_id: sequential number
    - location: section/table/figure
    - paper_text: exact quote from paper
    - paper_value: the number claimed
    - evidence_file: which raw file
    - evidence_value: the actual number
    - status: exact_match | rounding_ok | ambiguous_mapping |
              missing_evidence | config_mismatch | aggregation_mismatch |
              number_mismatch | scope_overclaim | unsupported_claim
    - details: explanation if not exact_match

    Overall verdict: PASS | WARN | FAIL
```

### Step 3: Write Report (Executor — Claude)

Parse the reviewer's response and write `PAPER_CLAIM_AUDIT.md`:

```markdown
# Paper Claim Audit Report

**Date**: [today]
**Auditor**: GPT-5.4 xhigh (fresh zero-context thread)
**Paper**: [paper title from tex]

## Overall Verdict: [PASS | WARN | FAIL]

## Claims Verified: [N total]
- exact_match: [count]
- rounding_ok: [count]
- ambiguous_mapping: [count]
- missing_evidence: [count]
- mismatch: [count]

## Issues Found

### [FAIL/WARN] Claim #N: [description]
- **Location**: Section X / Table Y / Figure Z
- **Paper says**: "..."
- **Evidence shows**: ...
- **Status**: [status]
- **Fix**: [specific correction needed]

## All Claims (detailed)

| # | Location | Paper Value | Evidence Value | Status |
|---|----------|-------------|---------------|--------|
| 1 | Table 2 | 85.3% | 85.28% | rounding_ok |
| 2 | Abstract | "15% improvement" | 12.8% | number_mismatch |
| ... |
```

Also write `PAPER_CLAIM_AUDIT.json` for machine consumption.

### Step 4: Print Summary

```
📋 Paper Claim Audit Complete

  Claims verified: 24
  exact_match:     18
  rounding_ok:      3
  ambiguous:         1
  ⚠️ mismatch:      2

  Overall: ⚠️ WARN

  See PAPER_CLAIM_AUDIT.md for details.
```

## When to Run

1. **After `/paper-write`** — first check before improvement loop
2. **After `/auto-paper-improvement-loop`** — recheck if improvement loop changed numbers
3. **Before submission** — final verification

## Integration with Other Skills

### Read by `/auto-paper-improvement-loop` (if exists)

```
if PAPER_CLAIM_AUDIT.json exists:
    read mismatched claims
    fix them as priority items in the improvement round
```

### Advisory, Never Blocking

Same pattern as `/experiment-audit`:
- `PASS` → continue normally
- `WARN` → print warning, continue, flag draft as "check numbers before submission"
- `FAIL` → print alert, continue, but do NOT mark as submission-ready

## Key Rules

- **Fresh thread EVERY run.** Never use `codex-reply`. Never carry context.
- **Zero executor interpretation.** Only file paths. No summaries.
- **Only raw results.** No EXPERIMENT_LOG, no AUTO_REVIEW, no human summaries.
- **Rounding rule.** Only standard rounding to displayed precision. 84.7% → 84.7% or 85% is OK. 84.7% → 85.3% is NOT OK.
- **Cross-model.** Reviewer must be a different model family from executor.
