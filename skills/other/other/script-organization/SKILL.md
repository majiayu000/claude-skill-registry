---
name: script-organization
description: >
  Script organization for data science analysis projects with numbered scripts, data/outs/
  directories, and reproducibility conventions. Use when creating new analysis scripts in
  projects that follow data science conventions (numbered XX_ prefix scripts, outs/ directories,
  BUILD_INFO.txt). Do NOT load for documentation projects (Quarto books), infrastructure repos,
  or projects without data/outs/ directory structure.
user-invocable: false
---

# Script Organization and Reproducibility

Conventions for script numbering, input/output tracking, directory structure, and build provenance. The goal is to make data flow between scripts self-documenting through directory structure and path references, without requiring separate manifest files or pipeline tools.

---

## Directory Structure

### Flat Layout

For small projects with <10 scripts on a single topic:

```
project/
  R/                          # Shared R helpers
  python/                     # Shared Python helpers
  scripts/
    01_analysis.qmd
    02_plots.qmd
    exploratory/              # One-off analyses
  data/                       # External/immutable inputs only
  outs/
    01_analysis/              # Outputs from script 01
      mdata.rds
      01_analysis.html        # Rendered HTML
      BUILD_INFO.txt
    02_plots/
      volcano.pdf
      02_plots.html
      BUILD_INFO.txt
    exploratory/
```

### Sectioned Layout

For larger projects with multiple analytical threads:

```
project/
  R/                          # Shared R helpers (project-level)
  python/                     # Shared Python helpers (project-level)
  scripts/
    phosphoproteomics/
      01_analysis.qmd
      02_volcano_plots.qmd
    transcriptomics/
      01_heatmaps.qmd
    exploratory/
  data/
    gene_naming/              # Shared external data
    phosphoproteomics/        # Section-specific external data
    transcriptomics/
  outs/
    phosphoproteomics/
      01_analysis/
      02_volcano_plots/
    transcriptomics/
      01_heatmaps/
    exploratory/
  .claude/
    PHOSPHOPROTEOMICS_PLAN.md
    TRANSCRIPTOMICS_PLAN.md
```

Each section has its own script numbering (starting at `01_`). Sections may have one or more planning documents in `.claude/`.

### Choosing a Subdirectory

When creating a new script in a sectioned project:

1. Check the project's CLAUDE.md for a **Script Subdirectories** table listing each subdirectory and its scope
2. If the task clearly fits one subdirectory, use it
3. **If ambiguous, ask the user** which subdirectory to use before creating the script
4. If none of the existing subdirectories fit, propose creating a new one

### When to Use Each Layout

- **Flat**: Single topic, small scope, fewer than ~10 scripts
- **Sectioned**: Multiple distinct analytical threads, especially when different people work on different sections

---

## `data/` vs `outs/`

| Folder | Contains | Written by |
|--------|----------|------------|
| `data/` | External/immutable inputs: raw data, collaborator files, annotations, database exports | Nothing in this project — files arrive from outside |
| `outs/<script_name>/` | All outputs produced by a script (data files, plots, rendered HTML, BUILD_INFO.txt) | That script only |

**Rule:** If your code produced it, it goes in `outs/`. If it came from anywhere else, it goes in `data/`. Scripts never write to `data/`.

---

## Script Numbering

Scripts are numbered per-section (`01_`, `02_`, etc.) so `ls` shows them in a sensible order. **Numbers are labels, not dependency order.** Dependencies are encoded entirely by input paths within each script.

- Assign the next available number when adding a script
- Never renumber existing scripts when one is archived or deleted
- In sectioned projects, numbering restarts at `01_` in each section

---

## Script Lifecycle

Every `.qmd` script includes a `status` field in its YAML frontmatter:

| Status | Meaning | Location |
|--------|---------|----------|
| `development` | In active development, outputs are provisional | `scripts/` |
| `finalized` | Outputs are publication-ready; modify only with deliberate re-validation | `scripts/` |
| `deprecated` | Superseded; kept for reference | `scripts/old/` or `scripts/<section>/old/` |

When deprecating a script, add a `deprecated_by` field:

```yaml
status: deprecated
deprecated_by: 05_improved_analysis.qmd
```

Planning documents remain the authoritative tracker of script status across the project. The YAML `status` field makes the status visible when opening the file itself.

---

## Exploratory Directory

`scripts/exploratory/` (or `scripts/<section>/exploratory/`) is for one-off analyses, quick tests, and feasibility checks:

- No number prefixes or BUILD_INFO.txt required
- Other scripts must **never** depend on exploratory outputs (one-way dependency: exploratory scripts can read from any section's `outs/`)
- Can be cleaned out periodically without breaking anything
- No planning document needed
- Good candidates for promotion: if an exploratory script proves useful, promote it to a numbered script in the appropriate section

---

## Input/Output Tracking

Dependencies between scripts are self-documenting through paths. Group all input reads at the top of each script (or in the setup chunk), with comments distinguishing external data from other scripts' outputs.

**R example:**

```r
# --- Inputs (from other scripts) ---
mdata <- readRDS(here("outs/phosphoproteomics/01_analysis/mdata.rds"))
modules <- read_tsv(here("outs/phosphoproteomics/02_module_lists/modules.tsv"))

# --- Inputs (external data) ---
gene_names <- read_tsv(here("data/gene_naming/spongilla_gene_names_final.tsv"))
```

**Python example:**

```python
# --- Inputs (from other scripts) ---
modules = pd.read_csv(PROJECT_ROOT / "outs/phosphoproteomics/02_module_lists/modules.tsv", sep="\t")

# --- Inputs (external data) ---
gene_names = pd.read_csv(PROJECT_ROOT / "data/gene_naming/spongilla_gene_names_final.tsv", sep="\t")
```

Reading the top of any script shows exactly what it depends on and which upstream scripts produced those files. No separate DAG documentation needed.

---

## Provenance

### Git Hash

Every script captures the current git commit hash in its setup chunk and prints it into the rendered output. Six months later, you can check out that exact commit to see the state of all code at the time the output was produced.

### BUILD_INFO.txt

Every script writes a `BUILD_INFO.txt` to its output folder as its last action:

```
script: 01_analysis.qmd
commit: a1b2c3d
date: 2026-02-14 15:30:00
```

This answers: "When was this output folder last regenerated, and from what version of the code?" If downstream plots look wrong, check the upstream folder's BUILD_INFO.txt to see whether it was generated from current code or something stale.

BUILD_INFO.txt lives in `outs/` and is not tracked by git (since `outs/` is in `.gitignore`).

### Rendered HTML

Rendered `.html` output goes into `outs/<script_name>/` alongside data outputs, keeping `scripts/` clean.

See the `quarto-docs` skill for complete QMD templates with git hash and BUILD_INFO.txt chunks.

---

## Helper Functions

### Project-Level

Shared helper functions live in `R/` and `python/` at the project root:

```r
# R scripts load helpers with:
source(here("R/gene_name_helpers.R"))
```

```python
# Python scripts load helpers with:
import sys
sys.path.insert(0, str(PROJECT_ROOT / "python"))
from gene_name_helpers import normalize_name
```

**Rules:**
- **Do not version function names** (`make_gene_short`, not `make_gene_short_v2`). Fix functions in place; git tracks the history. If a function's interface genuinely changes (different inputs/outputs/purpose), give it a descriptive name reflecting what it does, not when it was written.
- **Do not duplicate the same function in both R and Python** within a project. Each function lives in one language. If a script in the other language needs that logic, rewrite it once in the new language and retire the old one.

### Cross-Project

Functions shared across multiple projects live in `~/lib/R/` and `~/lib/python/`:

```r
source("~/lib/R/plotting_helpers.R")
```

When a project-level function proves useful across 2+ projects, promote it to `~/lib/`. The `~/lib/` directory should be a git repository for version tracking.

**Future**: When distributing functions to collaborators, graduate shared functions into installable R/Python packages.

---

## Cross-Language Data Interchange

When data produced by an R script will be read by a Python script (or vice versa), use **Parquet**:

- Smaller than TSV, preserves column types, fast in both languages
- R: `arrow::write_parquet()` / `arrow::read_parquet()`
- Python: `pd.to_parquet()` / `pd.read_parquet()`

Avoid `.rds` (R-only) or `.pkl` (Python-only) for data that crosses the language boundary. Within a single language, native formats (`.rds` for R) are fine.

**Do not mix R and Python chunks in a single `.qmd`.** Each script uses one language. Scripts communicate through files in `outs/`, not shared memory.