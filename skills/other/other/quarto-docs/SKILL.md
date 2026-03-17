---
name: quarto-docs
description: >
  Quarto document conventions for data science analysis scripts (.qmd). Use when creating or
  rendering .qmd analysis scripts in data science projects with numbered scripts, status fields,
  git hash capture, and BUILD_INFO.txt. Do NOT load for Quarto books, websites, or documentation
  projects — those use standard Quarto conventions without numbered script prefixes or BUILD_INFO.txt.
user-invocable: false
---

# Quarto Documents

All analysis scripts — both R and Python — are Quarto `.qmd` documents. Use `.py` files only for standalone utilities, CLI tools, and library code (in `python/`), not for data analysis.

## Rendering (CRITICAL)

**Always use `quarto render`, never use `rmarkdown::render()`** for `.qmd` files.

```bash
# CORRECT: Use quarto CLI
quarto render path/to/script.qmd

# WRONG: Do NOT use rmarkdown
Rscript -e "rmarkdown::render('script.qmd')"  # Will fail with pandoc error
```

If quarto is not in PATH, try `/usr/local/bin/quarto` or check your conda environment.

### Python QMDs require conda activation

**CRITICAL:** For Python `.qmd` files, the project's conda environment must be active before rendering. Otherwise Quarto will use the wrong Python or fail to find packages.

```bash
# R QMD — no activation needed (renv handles it)
quarto render scripts/01_analysis.qmd --output-dir outs/01_analysis/

# Python QMD — MUST activate conda first
source ~/miniconda3/etc/profile.d/conda.sh && conda activate PROJECT_ENV && \
  quarto render scripts/02_plots.qmd --output-dir outs/02_plots/
```

## Rendering Options

```bash
# Render to default format, output to outs/
quarto render scripts/XX_name.qmd --output-dir outs/XX_name/

# Render to specific format
quarto render scripts/XX_name.qmd --to html --output-dir outs/XX_name/
quarto render scripts/XX_name.qmd --to pdf --output-dir outs/XX_name/

# Render with execution
quarto render scripts/XX_name.qmd --execute --output-dir outs/XX_name/
```

## Rendering Output Location

**CRITICAL:** Always use `--output-dir` to render HTML directly into the script's `outs/` folder. Never leave rendered HTML next to the `.qmd` source file.

```bash
# CORRECT: Render directly to outs/ folder
quarto render scripts/01_analysis.qmd --output-dir outs/01_analysis/

# CORRECT: With R 4.5 override
QUARTO_R=/Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/bin/R \
  quarto render scripts/01_analysis.qmd --output-dir outs/01_analysis/

# WRONG: Do NOT render in place (pollutes scripts/ with HTML)
quarto render scripts/01_analysis.qmd
```

The `--output-dir` path is relative to the project root (where you run the command from).

## Format Choice

| Format | Best for | Notes |
|--------|----------|-------|
| **HTML** | GitHub, web sharing | Reliable text wrapping, self-contained |
| **PDF** | Print, formal docs | Requires LaTeX workarounds for line wrapping |

**Recommendation:** Use HTML for GitHub/web. Use PDF only when print is required.

## Running Code Without Rendering

When you just need outputs, not the rendered document:

**R:**
- Extract R code and run with `Rscript` directly
- Or use `quarto render script.qmd --execute`

**Python:**
- Extract Python code and run with `python` directly (with conda env active)
- Or use `quarto render script.qmd --execute` (with conda env active)

---

## QMD Templates

Templates include a `status` lifecycle field, git hash capture, and BUILD_INFO.txt provenance (see the `script-organization` skill for the conventions behind these).

### Shared YAML Header

The YAML header is identical for R and Python, except Python adds `jupyter: python3`:

**R:**
```yaml
---
title: "Script Title"
subtitle: "Brief description"
author: "Your Name"
date: today
status: development        # development | finalized | deprecated
format:
  html:
    toc: true
    toc-depth: 2
    number-sections: true
    code-overflow: wrap
    code-fold: false
    code-tools: true
    highlight-style: github
    theme: cosmo
    fontsize: 1rem
    linestretch: 1.5
    self-contained: true
execute:
  echo: true
  message: false
  warning: false
  cache: false
---
```

**Python** — same, but add `jupyter: python3` and drop `message: false` (not applicable):
```yaml
---
title: "Script Title"
subtitle: "Brief description"
author: "Your Name"
date: today
status: development        # development | finalized | deprecated
jupyter: python3
format:
  html:
    toc: true
    toc-depth: 2
    number-sections: true
    code-overflow: wrap
    code-fold: false
    code-tools: true
    highlight-style: github
    theme: cosmo
    fontsize: 1rem
    linestretch: 1.5
    self-contained: true
execute:
  echo: true
  warning: false
  cache: false
---
```

---

### R Template Chunks

**Setup chunk:**

````
```{r setup}
suppressPackageStartupMessages({
  library(tidyverse)
  library(here)
  # ... other packages
})

source(here("R/helpers.R"))  # if needed

# ---- Options ----
options(stringsAsFactors = FALSE)
set.seed(42)

git_hash <- system("git rev-parse --short HEAD", intern = TRUE)
cat("Rendered from commit:", git_hash, "\n")
```
````

**Input section** (immediately after setup):

````
```{r inputs}
# --- Inputs (from other scripts) ---
mdata <- readRDS(here("outs/01_analysis/mdata.rds"))

# --- Inputs (external data) ---
gene_names <- read_tsv(here("data/gene_naming/names.tsv"))
```
````

**Final chunk** (after all outputs are written):

````
```{r build-info}
out_dir <- here("outs/XX_script_name")
dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)

writeLines(
  c(
    paste("script:", "XX_script_name.qmd"),
    paste("commit:", git_hash),
    paste("date:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"))
  ),
  file.path(out_dir, "BUILD_INFO.txt")
)

sessionInfo()
```
````

---

### Python Template Chunks

**Setup chunk:**

````
```{python}
#| label: setup

import subprocess
import sys
import random
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

PROJECT_ROOT = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"]).decode().strip())
sys.path.insert(0, str(PROJECT_ROOT / "python"))
# from helpers import ...  # if needed

# ---- Options ----
random.seed(42)
np.random.seed(42)
pd.set_option("display.max_columns", None)
sns.set_theme(style="whitegrid")

# ---- Paths ----
out_dir = PROJECT_ROOT / "outs/XX_script_name"
out_dir.mkdir(parents=True, exist_ok=True)

git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
print(f"Rendered from commit: {git_hash}")
```
````

**Input section** (immediately after setup):

````
```{python}
#| label: inputs

# --- Inputs (from other scripts) ---
modules = pd.read_csv(PROJECT_ROOT / "outs/02_module_lists/modules.tsv", sep="\t")

# --- Inputs (external data) ---
gene_names = pd.read_csv(PROJECT_ROOT / "data/gene_naming/names.tsv", sep="\t")
```
````

**Saving figures:**

````
```{python}
#| label: fig-example
#| fig-cap: "Description of figure"

fig, ax = plt.subplots(figsize=(6, 4))
# ... plotting code ...
plt.tight_layout()

# Save to outs/ AND display inline
fig.savefig(out_dir / "figure_name.pdf", dpi=300, bbox_inches="tight")
fig.savefig(out_dir / "figure_name.png", dpi=300, bbox_inches="tight")
plt.show()
```
````

For seaborn:
````
```{python}
g = sns.catplot(data=df, x="condition", y="value", kind="box")
g.savefig(out_dir / "boxplot.pdf", dpi=300, bbox_inches="tight")
plt.show()
```
````

**Final chunk:**

````
```{python}
#| label: build-info

(out_dir / "BUILD_INFO.txt").write_text(
    f"script: XX_script_name.qmd\n"
    f"commit: {git_hash}\n"
    f"date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
)

import session_info
session_info.show()
```
````

---

### R vs Python Quick Reference

| Convention | R | Python |
|------------|---|--------|
| **Project root** | `here::here()` | `PROJECT_ROOT` (from git) |
| **Read CSV** | `read_csv(here("data/file.csv"))` | `pd.read_csv(PROJECT_ROOT / "data/file.csv")` |
| **Read TSV** | `read_tsv(here("data/file.tsv"))` | `pd.read_csv(PROJECT_ROOT / "data/file.tsv", sep="\t")` |
| **Read Parquet** | `arrow::read_parquet(here(...))` | `pd.read_parquet(PROJECT_ROOT / ...)` |
| **Read RDS** | `readRDS(here(...))` | N/A (use Parquet for cross-language) |
| **Save figure** | `ggsave(file.path(out_dir, "fig.pdf"))` | `fig.savefig(out_dir / "fig.pdf")` |
| **Random seed** | `set.seed(42)` | `random.seed(42)` + `np.random.seed(42)` |
| **Session info** | `sessionInfo()` | `session_info.show()` |
| **Suppress startup** | `suppressPackageStartupMessages()` | N/A (Python imports are quiet) |
| **Chunk label** | `{r label-name}` or `#| label:` | `#| label:` only |
| **Helper loading** | `source(here("R/helpers.R"))` | `sys.path.insert(0, str(PROJECT_ROOT / "python"))` |

---

### Language Mixing

**Do not mix R and Python chunks in a single `.qmd`.** Each script uses one language. Scripts communicate through files in `outs/`, not shared memory. Use interchange formats (TSV, CSV, Parquet) for data that crosses the language boundary.

---

## Reference Files

| Topic | File |
|-------|------|
| Publication-quality YAML templates (HTML and PDF) | `references/pdf-formatting.md` |