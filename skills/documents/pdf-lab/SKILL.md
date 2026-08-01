---
name: pdf-lab
description: /pdf-lab is a convergence loop that diagnoses PDF extraction failures,
---

---
name: pdf-lab
description: >
  Self-improving PDF extraction convergence loop. Diagnoses extraction failures
  by computing the delta between S00 estimates and actual extraction, reproduces
  issues on synthetic PDFs, discovers optimal parameters, and writes fixes back
  to the extractor pipeline code permanently.
allowed-tools: [Bash, Read, Write, Edit, Glob, Grep]
triggers:
  - pdf lab
  - tune pdf extraction
  - improve pdf extraction
  - converge extraction parameters
  - fix extraction delta
  - self improve extractor
  - write back pipeline fix
metadata:
  short-description: Self-improving PDF extraction with convergence + write-back
  version: "1.0.0"

provides:
  - pdf-lab
composes: [, task-monitor]
---

# pdf-lab

`/pdf-lab` is a convergence loop that diagnoses PDF extraction failures,
reproduces them on synthetic PDFs, discovers optimal parameters, and
**writes those fixes back to the extractor pipeline code** permanently.

## Why This Exists

There is no absolute ground truth for real PDFs. The system works with
**deltas** between S00's estimate and actual extraction results. When S00
predicts 40 sections but extraction finds 15, something is wrong. `/pdf-lab`
figures out what, fixes it, and makes the fix permanent.

## Quick Start

```bash
cd /home/graham/workspace/experiments/pi-mono/.pi/skills/pdf-lab

# Main: diagnose, reproduce, converge, and write fix back
./run.sh tune /path/to/real.pdf \
  --review-json /path/to/review_result.json \
  --debug-json /path/to/debug_patterns.json \
  --converge --write-back --json

# Dry run: find the fix but don't write it
./run.sh tune /path/to/real.pdf \
  --review-json ... --debug-json ... \
  --converge --dry-run --json

# Quick diagnosis only (compute delta, no tuning)
./run.sh diagnose /path/to/real.pdf \
  --profile-json /path/to/profile.json \
  --structural-json /path/to/structural.json

# Generate synthetic reproduction PDF only
./run.sh synthetic \
  --patterns '["multi_column","split_tables"]' \
  --output /tmp/repro.pdf

# Show recent tuning results
./run.sh status

# List all pdf-lab code changes
./run.sh history

# Rollback a specific fix
./run.sh rollback --sha abc123
```

## How Fixes Get Written Back

The pipeline has a tiered configuration system. `/pdf-lab` writes to the
appropriate tier:

| Tier | Target | Example |
|------|--------|---------|
| 1 | Env var defaults in step files | `CAMELOT_LINE_SCALE_DEFAULT` 15 -> 40 |
| 2 | Heuristic thresholds (code constants) | `LARGE_FONT_THRESHOLD` 11.0 -> 9.5 |
| 3 | Pattern rules (regex, filters) | New citation pattern in S04 |
| 4 | Preset YAML | `line_scale: 80` in arxiv twin_config.yml |
| 5 | Calibration records (ArangoDB) | Learned pattern in `learned_patterns` |
| 6 | /memory (runtime recall) | Winning params stored for instant recall |

## Persona Attribution

Every code change is traceable to the persona who flagged the issue via
git commit trailers (`Reviewed-By`, `Persona-Role`, `Issue-Codes`).

## Integration

Called by `inline_review_loop.py` when a persona review score is below
threshold. Falls back to heuristic adaptive params if convergence fails.

## Memory + Taxonomy Integration

The skill integrates with the shared memory and taxonomy systems via
`memory_integration.py` for cross-session learning:

- **Pre-hook (`recall_prior_convergence`)**: Before tuning, recalls prior convergence
  results for the same PDF type or URL. Enables the tuner to skip failed strategies
  and start from previously winning parameters.
- **Post-hook (`learn_convergence`)**: After tuning completes, stores the convergence
  outcome (strategy, iterations, final score, improvements, write-back results) to
  memory with taxonomy bridge tags for cross-skill recall.
- **Bridge keywords**: Precision, Resilience, Fragility, Corruption, Loyalty, Stealth
  (tuned to PDF extraction domain).
- **Tags**: `["pdf_lab", "convergence"] + bridges`

Gracefully degrades if `common.memory_client` or `taxonomy/taxonomy.py` are unavailable.

## File Structure

```
pdf-lab/
  SKILL.md                   # This file
  run.sh                     # Shell entry point
  pdf_lab.py                 # Typer CLI entry point
  memory_integration.py      # Memory + Taxonomy hooks
  pyproject.toml             # Dependencies
  lib/                       # Core libraries (delta, tuner, writer, etc.)
  data/                      # Local state and convergence events
  docs/                      # Additional documentation
```

## Outputs

- Code changes written to `src/extractor/pipeline/steps/`
- `/memory` entries for future recall (synthetic creation, convergence, reverts)
- Git commits with persona attribution trailers
- JSON report of convergence results
