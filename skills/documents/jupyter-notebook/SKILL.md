---
name: jupyter-notebook
description: >-
  Use when the user asks to create, scaffold, or edit Jupyter notebooks (.ipynb)
  for experiments, explorations, or tutorials; classifies intent as experiment or
  tutorial, scaffolds from bundled templates via new_notebook.py, fills cells with
  small runnable steps, and validates the result against a quality checklist.
allowed-tools:
  - AskUserQuestion
  - Bash
  - NotebookEdit
  - Read
  - Write
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - builder
    - jupyter
    - notebook
    - data-science
  provenance:
    upstream_source: "jupyter-notebook"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T14:00:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.88
---

# Jupyter Notebook Skill

Create clean, reproducible Jupyter notebooks for experiments and tutorials.

## Overview

This skill scaffolds `.ipynb` notebooks from bundled templates, fills them with focused code and markdown cells, and validates the result for reproducibility.

**What it creates:**
- Experiment notebooks for hypothesis-driven exploration (data analysis, model comparison, ablation studies)
- Tutorial notebooks for step-by-step teaching (onboarding guides, API walkthroughs, concept introductions)

**Key features:**
- Template-based scaffolding via `scripts/new_notebook.py` avoids raw JSON authoring
- Decision tree classifies each request into experiment or tutorial
- Cell-level editing with `NotebookEdit` preserves notebook structure
- Quality checklist enforces top-to-bottom runnability and clean outputs

## When to Use

- Create a new `.ipynb` notebook from scratch
- Convert rough notes or scripts into a structured notebook
- Refactor an existing notebook for reproducibility and readability
- Build experiments or tutorials intended for sharing or re-running

## Decision Tree

```
User request
 |- Exploratory, analytical, hypothesis-driven, or benchmark-oriented
 |   -> KIND: experiment
 |- Instructional, step-by-step, audience-specific, or walkthrough
 |   -> KIND: tutorial
 |- Editing an existing notebook
     -> Treat as refactor: preserve intent, improve structure
```

When ambiguous, ask the user which mode fits their goal.

## Workflow

### Step 1: Gather Requirements

Ask the user for:
- **Objective**: What question, task, or concept the notebook addresses
- **Kind**: experiment or tutorial (use decision tree if unclear)
- **Title**: A descriptive name for the first heading cell
- **Output path**: Where to write the `.ipynb` (default: `output/jupyter-notebook/<slug>.ipynb`)

### Step 2: Scaffold from Template

```bash
SKILL_DIR="<path-to-this-skill>"
python3 "$SKILL_DIR/scripts/new_notebook.py" \
  --kind experiment \
  --title "Compare prompt latency across models" \
  --out output/jupyter-notebook/compare-prompt-latency.ipynb
```

```bash
python3 "$SKILL_DIR/scripts/new_notebook.py" \
  --kind tutorial \
  --title "Intro to vector embeddings" \
  --out output/jupyter-notebook/intro-vector-embeddings.ipynb
```

The script loads the matching template, sets the title cell, and writes a valid `.ipynb`. Use `--force` to overwrite.

### Step 3: Fill Cells

Use `NotebookEdit` to populate the notebook cell by cell:

- **One concept per code cell**: Each cell does one thing (import, compute, visualize)
- **Markdown before code**: Short explanation of purpose and expected output
- **Suppress noise**: Use semicolons, `_ =`, or `.head()` to keep outputs concise
- **Set state early**: Imports, seeds, and configuration in the first few cells

For experiments, follow `references/experiment-patterns.md`.
For tutorials, follow `references/tutorial-patterns.md`.

### Step 4: Validate

Run the notebook top-to-bottom when the environment allows:

```bash
jupyter nbconvert --to notebook --execute notebook.ipynb \
  --output executed.ipynb --ExecutePreprocessor.timeout=300
```

If execution is not possible, state this explicitly and describe local validation steps. Apply the checklist from `references/quality-checklist.md`.

## Editing Existing Notebooks

1. Read the notebook with `Read` to understand current structure
2. Use `NotebookEdit` for targeted cell edits (replace, insert, delete)
3. Preserve cell order unless reordering improves the narrative
4. Review `references/notebook-structure.md` before editing raw JSON
5. Reset `execution_count` to `null` and clear `outputs` on modified cells

## File Conventions

| Path | Purpose |
|------|---------|
| `tmp/jupyter-notebook/` | Intermediate files; delete when done |
| `output/jupyter-notebook/` | Final notebook artifacts |
| Filenames | Stable descriptive slugs (`ablation-temperature.ipynb`) |

## Dependencies

The scaffolding script uses only the Python standard library. For local notebook execution:

```bash
pip install jupyterlab ipykernel
```

## Examples

### Example 1: Scaffold an experiment

```
User: Create a notebook to compare embedding models on our FAQ dataset