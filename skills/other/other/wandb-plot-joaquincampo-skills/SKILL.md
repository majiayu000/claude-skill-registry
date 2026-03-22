---
name: wandb-plot
description: |
  Download and generate plots from Weights & Biases runs. Use when you need to:
  - List projects you have access to
  - List runs in a W&B project
  - Inspect available metrics for a run
  - Download existing plot images from a run
  - Generate line plots from metric history (loss, accuracy, etc.)
---

# W&B Plot Skill

## MANDATORY Setup (Run First)

**IMPORTANT:** Before running ANY script, you MUST execute this setup block to ensure the correct working directory and virtual environment.

```bash
# Determine skill directory (Claude Code plugin or Codex/local)
if [ -n "${CLAUDE_PLUGIN_ROOT}" ]; then
  SKILL_DIR="${CLAUDE_PLUGIN_ROOT}/skills/wandb-plot"
elif [ -d "${HOME}/.codex/wandb-plot-skill/skills/wandb-plot" ]; then
  SKILL_DIR="${HOME}/.codex/wandb-plot-skill/skills/wandb-plot"
else
  SKILL_DIR="$(pwd)"
fi
cd "$SKILL_DIR"

# Create/activate venv and install deps (uv preferred, pip fallback)
if [ ! -d ".venv" ]; then
  if command -v uv &> /dev/null; then
    uv venv .venv && . .venv/bin/activate && uv pip install -e .
  else
    python3 -m venv .venv && . .venv/bin/activate && pip install -e .
  fi
else
  . .venv/bin/activate
fi
```

After setup completes, all `python3 scripts/*.py` commands will work correctly from this directory.

## Prereqs

- Auth: set `WANDB_API_KEY` environment variable (recommended) or run `wandb login`.

## Tools (Scripts)

### `scripts/list_projects.py`

**Inputs**
- `--entity <entity>` (optional; defaults to current user or org)
- `--limit <n>` (optional, default: 100)
- `--json` (optional)

**Output**
- Stdout table (default) or JSON list (with `--json`), where each item includes:
  - `name`, `entity`, `description`, `created_at`, `url`

### `scripts/list_runs.py`

**Inputs**
- `<entity/project>` (required)
- `--state <state>` (optional)
- `--limit <n>` (optional, default: 100)
- `--json` (optional)

**Output**
- Stdout table (default) or JSON list (with `--json`), where each item includes:
  - `id`, `name`, `state`, `created_at`, `summary_metrics`, `tags`

### `scripts/list_metrics.py`

**Inputs**
- `<entity/project>` (required)
- `<run_id>` (required; run id or run name)
- `--include-system` (optional; include `_step`, `_timestamp`, etc.)
- `--json` (optional)

**Output**
- Stdout table (default) or JSON dict (with `--json`) keyed by metric name.
- Each metric entry includes `type`, `count`, `non_null_count`, and for numeric metrics: `min`, `max`, `mean`, `std`.

### `scripts/download_plots.py`

**Inputs**
- `<entity/project>` (required)
- `<run_id>` (required)
- `--pattern "<glob>"` (optional; defaults to common image paths)
- `--output <dir>` (optional; overrides default output location)
- `--force` (optional; re-download if file exists)

**Output**
- Writes downloaded images to the output directory (flat filenames).
- Updates/creates `metadata.json` in the same directory.
- Stdout lists downloaded/skipped files; returns an empty list (and prints “No plot files found…”) when nothing matches.

### `scripts/generate_plots.py`

**Inputs**
- `<entity/project>` (required)
- `<run_id>` (required; comma-separated for multiple runs)
- `--metrics "<m1,m2,...>"` (required; metric names as shown by `list_metrics.py`)
- `--all-metrics` (optional; plot all metrics)
- `--full-res` (optional; uses full `scan_history`)
- `--smooth <n>` (optional; rolling average window)
- `--output <dir>` (optional)
- `--ema-weight <w>` (optional; default: 0.99)
- `--viewport-scale <n>` (optional; default: 1000)
- `--no-ema` (optional; disable EMA smoothing)
- `--group-by-prefix` (optional; group outputs by metric prefix)
- `--include-system` (optional; include system metrics like `_step` and `system/*` with `--all-metrics`)

**Output**
- Writes `<metric>.png` for each generated plot plus `metadata.json` to the output directory.
- Stdout lists generated files; missing metrics raise an error listing available metrics.

## Workflow

```bash
python3 scripts/list_projects.py --limit 10
python3 scripts/list_runs.py <entity/project> --limit 10
python3 scripts/list_metrics.py <entity/project> <run_id>
python3 scripts/download_plots.py <entity/project> <run_id>
python3 scripts/generate_plots.py <entity/project> <run_id> --metrics loss,accuracy
python3 scripts/generate_plots.py <entity/project> run1,run2 --metrics loss --ema-weight 0.99 --viewport-scale 1000
python3 scripts/generate_plots.py <entity/project> run1,run2 --metrics rewards/total_mean,rewards/total_std --output /path/to/folder --group-by-prefix
python3 scripts/generate_plots.py <entity/project> run1,run2 --all-metrics --output /path/to/folder --group-by-prefix
```

## Outputs

Default output directory:

```
wandb_plots/<entity>_<project>/<run_name>_<run_id>/
  - *.png
  - metadata.json
```

If `download_plots.py` finds no images, fall back to `generate_plots.py`.
