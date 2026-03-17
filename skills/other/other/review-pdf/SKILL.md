---
name: review-pdf
description: >
  Comprehensive PDF extraction fidelity auditor for extractor pipeline quality.
  Compares S00 estimates, S11 structural output, and source PDF signals;
  emits per-document and aggregate reports; routes failures into classifier/prompt/
  fixture/debug self-improvement loops.
allowed-tools: [Bash, Read, Write, Glob, Grep]
triggers:
  - review pdf
  - audit pdf extraction
  - assess extractor quality
  - pdf fidelity
  - compare s00 s11
  - find pdf extraction regressions
  - self improve pdf extraction
metadata:
  short-description: PDF extraction QC gate with self-improvement escalation
  version: "2.0.0"
provides:
  - pdf-extraction
composes:
  - extractor
  - memory
  - create-figure
  - task-monitor

taxonomy:
  - validation
  - extraction
  - precision
---

# review-pdf

`review-pdf` is the hard quality gate for PDF extraction in:

- `/home/graham/workspace/experiments/extractor/src/extractor/pipeline`

It validates quality at document level and corpus level, then drives automatic escalation into helper skills when regressions are detected.

## Scope

The skill validates:

- S00 estimate quality vs S11 extracted structure
- section/table/figure/equation recall
- content coverage and structural integrity
- ordering quality, including y+x multi-column behavior
- classifier/prompt/heuristic drift signals

The skill is intended to be a composable module in a larger `learn-datalake` workflow.

## Inputs

You can pass:

- one run directory containing `00_profile_detector/profile.json` and `11_json_exporter/structural.json`
- one `profile.json`
- a corpus root containing many runs

Corpus example:

- `/mnt/storage12tb/extractor_corpus`

## Outputs (Required)

For every run:

- per-document reports (`per_doc/*.json`)
- aggregate report (`aggregate.json`, `aggregate.md`)
- memory event append (mandatory) to:
  - `/home/graham/workspace/experiments/pi-mono/.pi/skills/memory/.artifacts/review_pdf_events.jsonl`
- optional graph-memory acquire calls per reviewed PDF (`--ingest-memory`)
- optional taxonomy tags attached to per-doc reports (`--taxonomy-collection`)

## Commands

```bash
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/review-pdf

# Single run/doc check
./run.sh check /path/to/run_dir

# Corpus batch audit
./run.sh batch /mnt/storage12tb/extractor_corpus --limit 500

# Self-improvement loop (check -> escalate -> re-check)
./run.sh iterate /mnt/storage12tb/extractor_corpus --cycles 3 --execute-jobs

# Continuous datalake mode (watch + auto-extract missing + target integrity)
./run.sh loop /mnt/storage12tb/extractor_corpus \
  --target-score 0.95 \
  --execute-jobs \
  --extract-missing \
  --ingest-memory \
  --taxonomy-collection operational

# Compare two aggregate runs
./run.sh compare reports/run_a/aggregate.json reports/run_b/aggregate.json

# Convergence from history file
./run.sh convergence reports/review_pdf_iter_history.jsonl

# Quick status and recent memory history
./run.sh status reports/<run_id>/aggregate.json
./run.sh history --limit 50
```

## Quality Dimensions

Weighted dimensions:

- section alignment (18%)
- table fidelity (16%)
- figure fidelity (10%)
- equation fidelity (14%)
- content coverage (22%)
- ordering y+x (12%)
- data quality (8%)

Grading:

- `A+` >= 0.95
- `A` >= 0.88
- `B` >= 0.78
- `C` >= 0.65
- else `F`

Verdict:

- `FAIL` if any critical issue or score < 0.70
- `WARN` if high issues exist
- `PASS` otherwise

## Critical Failure Rules

- formulas expected in S00 but zero equations in S11 => critical fail
- major text loss vs source PDF => critical fail
- severe section/table under-recall => critical fail
- y+x ordering violations in positioned content => high/critical attention

## Self-Improvement Escalation

Issue signatures route to helper skills. Primary routes include:

- `table-lab`, `create-table-classifier`, `create-table`
- `create-classifier`, `classifier-lab`, `create-intent-map`
- `debug-pdf`, `create-pdf-fixture`, `fixture-tricky`
- `prompt-lab`, `normalize`, `pdf-screenshot`
- `extractor`, `fetcher`

Execution modes:

- planned mode: jobs listed in report (`escalation_jobs`)
- auto mode: use `--execute-jobs` to run auto-executable jobs immediately
- continuous mode: `loop/watch` runs until integrity targets are met and keeps monitoring new PDFs

Classifier policy for escalations:

- `classifier-lab` benchmark is mandatory before classifier promotion.
- `create-classifier` must run with:
  - `--benchmark-first`
  - `--classifier-lab-first`
  - `--require-classifier-lab`
  - `--require-selection-pass`
- if selection fails, treat as hard failure and keep the issue unresolved (no silent fallback).

Recommended promotion gate (quality-first):

- holdout `macro_f1 >= 0.90`
- holdout `accuracy >= 0.90`
- minimum per-class recall `>= 0.80` for all supported classes
- no class with support below review threshold without explicit waiver

Recommended HF augmentation license allowlist:

- `mit`
- `apache-2.0`
- `bsd-3-clause`
- `bsd-2-clause`
- `cc0-1.0`

## Recommended Compose Pattern

For full learning loop, compose:

1. `review-pdf` (measure + detect regressions)
2. helper skills (fix generation and model/prompt retraining)
3. `review-pdf` (re-check)
4. `quality-audit` and `batch-quality` (statistical quality gating)
5. `corpus-report` / `analytics` / `monitor-pdfs` (trend and ops views)

## Integration Notes

- This skill does not replace extractor; it audits extractor outcomes.
- Memory append is mandatory to track progress/regressions across iterations.
- Heuristics are not sufficient alone; escalation is classifier/prompt-first for persistent error classes.
- Keep outputs deterministic when possible (`--execute-jobs` off for pure measurement runs).
- For `learn-datalake` composition across formats, pair this with modality-specific reviewers
  (for example `extract-html`) and normalize all outputs into shared memory event contracts.

Memory/storage policy:

- store both success and failure events; failures are first-class training signals.
- retain unresolved failure buckets with issue signature + input artifacts + attempted fixes.
- write aggregate and per-doc events to memory sink each cycle so `classifier-lab` and
  `create-classifier` can mine historical regressions, not only latest runs.

## Visualization

After generating reports, offer to visualize via `/create-figure`:

```bash
# Quality dimension radar chart (section alignment, table fidelity, etc.)
create-figure radar --input aggregate.json --output quality-radar.pdf

# Grade distribution across corpus
create-figure metrics --input aggregate.json --output grades.png --type bar --title "Corpus Grade Distribution"

# Convergence curve across iterations
create-figure metrics --input review_pdf_iter_history.jsonl --output convergence.png --type line --title "Quality Convergence"

# Failure type breakdown
create-figure metrics --input aggregate.json --output failures.png --type pie --title "Failure Categories"

# Per-dimension heatmap across documents
create-figure heatmap --input aggregate.json --output dimension-heatmap.png
```

**When to offer:** After `batch`, `iterate`, or `loop` runs that produce aggregate reports. Especially useful for convergence tracking across self-improvement cycles.

## Definition of Done (for a review cycle)

- all target docs processed with per-doc reports
- aggregate report generated
- memory event appended for each doc and aggregate
- fail/warn issues mapped to concrete helper-skill escalations
- convergence history produced for iterative runs
