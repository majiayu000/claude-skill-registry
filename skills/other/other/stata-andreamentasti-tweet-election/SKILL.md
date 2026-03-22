---
name: stata
description: Context and tools for working with Stata — writing .do files, running them in batch mode, and efficiently consulting the bundled PDF documentation.
allowed-tools: ["Read", "Bash", "Write", "Edit", "Grep", "Glob"]
---

# Stata Skill

Use this skill whenever writing, editing, running, or debugging Stata `.do` files,
or when you need to look up Stata syntax, commands, or options.

---

## 1. What is Stata

Stata is a statistical software package for data management, analysis, and graphics.
It is widely used in economics, political science, epidemiology, and other social sciences.

Key concepts:
- **`.do` files**: Scripts (plain text) containing Stata commands, executed sequentially.
- **`.dta` files**: Stata's binary data format.
- **`.log` files**: Text output captured during a Stata session or batch run.
- **`ado` files**: Stata programs (user-written or official) that extend functionality.
- **Macros**: `local` (temporary) and `global` (persistent within session) named values.
- **Factor variables**: `i.varname` notation for categorical regressors.
- **Postestimation**: Commands run after a model fit (e.g., `predict`, `margins`, `estat`).

---

## 2. Running Stata in This Environment

**Finding the installation:** Stata is installed in `C:\Program Files\` on Windows.
To auto-detect the path:
```bash
STATA_DIR=$(ls -d "/c/Program Files"/Stata* "/c/Program Files"/StataNow* 2>/dev/null | sort -V | tail -1)
echo "$STATA_DIR"
```

**From bash (Claude Code terminal):**
```bash
stata -b do path/to/script.do        # batch mode, creates .log file
stata path/to/script.do              # interactive window
```

**IMPORTANT:** ALWAYS use the `stata` wrapper command (at `~/bin/stata`), NEVER call
`StataSE-64.exe` directly. The wrapper auto-moves batch-mode logs from the current
directory to `quality_reports/stata_logs/`. Calling the exe directly leaves stray
`.log` files in the project root.

**From PowerShell (user terminal):**
```powershell
stata -b do path\to\script.do
```

The `stata` alias must point to `StataSE-64.exe` (or `StataMP-64.exe` depending on
edition). See `SETUP.md` for how to configure this.

**Checking for errors after batch run:**
```bash
grep "^r(" script.log    # Stata error codes start with r(
```
If the log contains `r(` lines, the script hit an error at that point.

---

## 3. Writing `.do` Files — Essentials

### File structure
```stata
version 17
clear all
set more off

* --- 0. Paths ---
do config_local.do          // sets $root

* --- 1. Load data ---
use "$root/data/processed/tweets_processed.dta", clear

* --- 2. Analysis ---
reg vote_share engagement_score, robust

* --- 3. Output ---
esttab using "$root/output/tables/table1.tex", booktabs label replace
graph export "$root/output/figures/fig1.png", replace width(2400)
```

### Key patterns
- `version 17` at top for reproducibility
- All paths via `$root` global macro (set in `config_local.do`)
- `clear all` / `set more off` at the start
- `replace` on all output commands (allows re-running)
- `width(2400)` for ~300 DPI figures at 8 inches
- `graphregion(color(white)) bgcolor(white)` for white backgrounds
- Line continuation with `///`

### Common pitfalls
- `encode` assigns codes alphabetically — verify ordering before interpreting
- `sort` is not stable — add enough keys to uniquely identify rows
- Use `vce(cluster var)` not just `robust` when observations are grouped
- `destring` for numeric-as-string; `encode` for true categoricals — never confuse them

---

## 4. Stata PDF Documentation

### Location
Stata bundles its full documentation as PDFs inside the installation directory:
```
<STATA_INSTALL_DIR>/docs/
```

To find the docs directory automatically:
```bash
STATA_DOCS=$(ls -d "/c/Program Files"/Stata*/docs "/c/Program Files"/StataNow*/docs 2>/dev/null | sort -V | tail -1)
echo "$STATA_DOCS"
```

### Complete manual index (37 PDFs, ~17,000 total pages)

| File | Manual | Pages | Key contents |
|------|--------|-------|--------------|
| `r.pdf` | **Base Reference** | 3,502 | regress, logit, probit, test, predict, margins — the most-used manual |
| `u.pdf` | **User's Guide** | 403 | Stata basics, syntax, data types, programming intro |
| `d.pdf` | **Data Management** | 1,000 | import, merge, reshape, append, encode, destring |
| `ts.pdf` | **Time Series** | 1,026 | arima, var, vec, irf, tsset |
| `xt.pdf` | **Panel Data** | 699 | xtreg, xtlogit, xtpoisson, xtset |
| `me.pdf` | **Mixed Effects** | 572 | mixed, melogit, mepoisson |
| `st.pdf` | **Survival Analysis** | 645 | stset, stcox, streg, sts |
| `mv.pdf` | **Multivariate** | 750 | factor, pca, cluster, manova |
| `sem.pdf` | **SEM** | 680 | sem, gsem, path diagrams |
| `g.pdf` | **Graphics** | 799 | twoway, graph bar, scheme, options |
| `p.pdf` | **Programming** | 667 | program, macro, mata interface |
| `m.pdf` | **Mata** | 1,214 | Stata's matrix programming language |
| `bayes.pdf` | **Bayesian** | 911 | bayesmh, bayesian estimation |
| `causal.pdf` | **Causal Inference** | 746 | teffects, didregress, stteffects |
| `lasso.pdf` | **Lasso** | 394 | lasso, elasticnet, cross-validation |
| `mi.pdf` | **Multiple Imputation** | 400 | mi impute, mi estimate |
| `svy.pdf` | **Survey** | 236 | svyset, svy: prefix |
| `tables.pdf` | **Tables** | 361 | collect, table, dtable, etable |
| `pss.pdf` | **Power/Sample Size** | 869 | power, sample size calculations |
| `meta.pdf` | **Meta-Analysis** | 439 | meta set, meta forestplot |
| `fn.pdf` | **Functions** | 193 | Built-in functions reference |
| `i.pdf` | **Glossary/Index** | 328 | Combined subject index |
| `stoc.pdf` | **Subject TOC** | 59 | Combined table of contents across all manuals |
| `adapt.pdf` | **Adaptive Designs** | 252 | Group sequential trials |
| `bma.pdf` | **Bayesian Model Averaging** | 241 | bmaregress, model selection |
| `cm.pdf` | **Choice Models** | 329 | cmclogit, conditional logit, mixed logit |
| `dsge.pdf` | **DSGE Models** | 179 | Dynamic stochastic general equilibrium |
| `erm.pdf` | **Extended Regression** | 307 | Extended regression models (endogeneity, selection, treatment) |
| `fmm.pdf` | **Finite Mixture Models** | 149 | fmm prefix, latent class |
| `gsm.pdf` | **Getting Started (Mac)** | 158 | Mac-specific setup guide |
| `gsu.pdf` | **Getting Started (Unix)** | 165 | Unix-specific setup guide |
| `gsw.pdf` | **Getting Started (Windows)** | 161 | Windows-specific setup guide |
| `h2oml.pdf` | **H2O Machine Learning** | 379 | h2oml, random forest, gradient boosting |
| `ig.pdf` | **Installation Guide** | 21 | License, installation |
| `irt.pdf` | **Item Response Theory** | 251 | irt, Rasch, 2PL, 3PL models |
| `rpt.pdf` | **Reporting** | 222 | putdocx, putpdf, collect, automated reports |
| `sp.pdf` | **Spatial** | 232 | spregress, spatial autoregressive models |

**Start with `stoc.pdf`** (59 pages) to find which manual covers a topic.

---

## 5. Reading Documentation Efficiently (Token-Saving Strategies)

**Problem:** 17,000 pages of PDFs. Reading even one manual wastes tokens.
**Solution:** Use targeted extraction — never read a full manual.

**Prerequisites:** `pdftotext` (bundled with poppler/mingw) and `pip install pdfplumber`.
See `SETUP.md` for installation.

### Tool 1: `pdftotext` (fast, plain text, best for prose)
```bash
# Auto-detect docs path
STATA_DOCS=$(ls -d "/c/Program Files"/Stata*/docs "/c/Program Files"/StataNow*/docs 2>/dev/null | sort -V | tail -1)

# Extract specific pages (e.g., pages 1200-1220 for regress)
pdftotext -f 1200 -l 1220 "$STATA_DOCS/r.pdf" -

# Search the subject TOC for a command
pdftotext "$STATA_DOCS/stoc.pdf" - | grep -i "regress"
```

### Tool 2: `pdfplumber` (Python, best for tables and structured content)
```python
import pdfplumber, glob, os

def find_stata_docs():
    """Auto-detect Stata docs directory."""
    for pattern in [r"C:\Program Files\StataNow*\docs",
                    r"C:\Program Files\Stata*\docs"]:
        matches = glob.glob(pattern)
        if matches:
            return sorted(matches)[-1]
    return None

def stata_doc_lookup(manual: str, start_page: int, end_page: int) -> str:
    """Extract text from a Stata manual. Pages are 0-indexed."""
    docs = find_stata_docs()
    path = os.path.join(docs, manual)
    with pdfplumber.open(path) as pdf:
        text = []
        for i in range(start_page, min(end_page, len(pdf.pages))):
            page_text = pdf.pages[i].extract_text()
            if page_text:
                text.append(page_text)
    return "\n".join(text)

# Example: read TOC of r.pdf to find page numbers
print(stata_doc_lookup("r.pdf", 2, 8))
```

### Tool 3: `pdftotext` + `grep` (search without reading)
```bash
STATA_DOCS=$(ls -d "/c/Program Files"/Stata*/docs "/c/Program Files"/StataNow*/docs 2>/dev/null | sort -V | tail -1)

# Find which page mentions "margins" in the base reference
pdftotext "$STATA_DOCS/r.pdf" - | grep -n "margins"

# Find a command across ALL manuals
for f in "$STATA_DOCS"/*.pdf; do
    if pdftotext "$f" - 2>/dev/null | grep -q "didregress"; then
        echo "Found in: $(basename $f)"
    fi
done
```

### Recommended lookup workflow
1. **Start with `stoc.pdf`** — search the subject TOC to identify which manual
2. **Read the manual's own TOC** (pages 2-8) to find the exact page range
3. **Extract only those pages** with `pdftotext -f START -l END manual.pdf -`
4. **Never extract more than 20 pages at once** — if you need more, narrow the search

### Token cost estimates
- 1 PDF page ~ 500-800 tokens
- Full `r.pdf` ~ 2.1M tokens (NEVER do this)
- `stoc.pdf` (59 pages) ~ 35K tokens (acceptable for initial lookup)
- Targeted 10-page extract ~ 6K tokens (ideal)

---

## 6. Quick Reference: Common Tasks

| Task | Where to look |
|------|--------------|
| Regression syntax | `r.pdf`, search TOC for "regress" |
| Merge datasets | `d.pdf`, search for "merge" |
| Panel data models | `xt.pdf`, search for "xtreg" |
| Export LaTeX tables | `r.pdf` search "esttab" or `tables.pdf` |
| Graph options | `g.pdf` TOC |
| String functions | `fn.pdf` or `d.pdf` search "string functions" |
| Date/time handling | `d.pdf` or `u.pdf` chapter on dates |
| Causal inference | `causal.pdf` TOC |
| Survey weights | `svy.pdf` TOC |
