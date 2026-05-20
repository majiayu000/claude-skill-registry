---
name: script-translator
description: "Use this skill whenever the user wants to translate, convert, or port a script from one statistical programming language to another — STATA, Python (pandas/numpy/statsmodels), or R (tidyverse/base R). Trigger even if the user says 'rewrite in R', 'convert to Python', 'port to STATA', or asks how code would look in another language."
argument-hint: "[source file] to [python|stata|r]"
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]
---

# Script Translator

Faithful line-by-line translation between Stata, Python, and R.

## 1. Detect Source and Target Languages

**From the user message:** Look for keywords like "to Python", "in R", "port to Stata", "convert to R", "rewrite in Python".

**From file extension:**
- `.do` → Stata
- `.py` → Python
- `.R` / `.r` → R

**If ambiguous:** Ask the user to confirm source and target before proceeding.

## 2. Load the Language-Pair Body File

Before writing ANY translated code, read the relevant body file:

| Direction | File to read |
|-----------|-------------|
| Python → R | `bodies/python-to-r.md` |
| Python → Stata | `bodies/python-to-stata.md` |
| R → Python | `bodies/r-to-python.md` |
| R → Stata | `bodies/r-to-stata.md` |
| Stata → Python | `bodies/stata-to-python.md` |
| Stata → R | `bodies/stata-to-r.md` |

The body file contains the construct mapping table, idiomatic equivalences, required imports, and known traps for that specific pair. Follow it closely.

## 3. Core Translation Rules (All Language Pairs)

These rules are absolute and override any instinct to "improve" the code:

### 3a. Structure and Logic
1. **Translate line by line**, preserving the order and structure of the original
2. **Keep variable names identical** — never rename columns, variables, or macros
3. **Preserve all data filters and conditions exactly** — same logic, same thresholds
4. **DO NOT refactor, optimize, or restructure** the code
5. **DO NOT change the order of operations** unless strictly required by the target language
6. **If the original has a bug, translate the bug faithfully** and add `# REVIEW: possible bug in original`
7. **Add short inline comments** when a translated line is non-obvious (e.g., `# Stata's egen mean() equivalent`)
8. **Flag with `# REVIEW:`** any construct that has no direct equivalent or requires manual verification

### 3b. Methodology (Non-Negotiable)
The translated script must produce **statistically identical results**:

9. **Same estimator** — OLS stays OLS, logit stays logit, probit stays probit. Never substitute.
10. **Same standard errors** — `robust` (HC1) stays HC1. `cluster(var)` stays clustered at the same variable. Never change the SE type or clustering level. Verify the target language's default matches (e.g., Stata `robust` = HC1, statsmodels `HC1` = HC1, but statsmodels default is not robust).
11. **Same fixed effects** — `areg, absorb(fe)` → must absorb the same variable, not include as dummies unless no absorb equivalent exists. Flag with `# REVIEW:` if the approach differs.
12. **Same merge logic** — left join stays left join, m:1 stays m:1. Preserve `validate` checks. Add `_merge` diagnostics if the original inspects them.
13. **Same sample restrictions** — every `keep if`, `drop if`, filter, and subsetting condition must be translated exactly. Missing value handling differs across languages — explicitly handle this (see body files for language-specific traps).
14. **Same weighting** — `[pw=wt]`, `[aw=wt]`, `[fw=wt]` must map to the exact equivalent. Flag if the target language doesn't distinguish weight types.
15. **Same test statistics** — F-tests, t-tests, Wald tests, correlation tests must use the same test. `pwcorr, sig` → Pearson with p-values, not Spearman.
16. **Same confidence level** — if the original uses 95% CI, the translation uses 95% CI. Same for significance stars (* 0.10 ** 0.05 *** 0.01).

### 3c. Visual Fidelity (Non-Negotiable)
The translated figure must be **visually identical** to the original. Go through every visual property line by line:

17. **Same plot type** — scatter stays scatter, bar stays bar, line stays line
18. **Same colors** — `blue` stays `blue`, `red` stays `red`. Match the exact color name or hex code.
19. **Same transparency/alpha** — `alpha=0.7` → `%70` in Stata, `alpha = 0.7` in R. Never omit.
20. **Same marker properties** — marker shape, size, edge color, edge width. If the original has `edgecolors="white", linewidth=0.5`, the translation must replicate this (Stata: `mlcolor(white) mlwidth(vthin)`).
21. **Same grid** — if the original has `ax.grid(True, alpha=0.3)`, the translation must include grid lines. If there is no grid, the translation must not add one.
22. **Same axis labels, title, and legend** — identical text, same position, same ordering
23. **Same legend position** — `position(5) ring(0)` = lower right inside. Default upper-right → translate to upper-right. Never leave to default if the original specifies a position.
24. **Same point labels/annotations** — if points are labeled with state names, font size, position offset, and alignment must all be replicated as closely as the target language allows.
25. **Same axis range and ticks** — if the original sets `ylim`, `xlim`, or custom tick marks, replicate them. If it uses auto-scaling, let the target auto-scale too.
26. **Same figure size** — `figsize=(8, 6)` → target equivalent (Stata: `xsize(8) ysize(6)`; R: `width = 8, height = 6`)
27. **Same background** — white background must be explicitly set in every language (it is NOT the default in Stata or base R)
28. **Same output format and resolution** — PNG at 300 DPI. Always.

**If a visual property cannot be exactly replicated**, add a `# REVIEW: [property] has no exact equivalent in [target language]` comment explaining the closest approximation used.

## 4. Apply Project Boilerplate

After translation, wrap the script in the project's conventions:

**Python target:**
- `import config as cfg` for paths
- `cfg.FIGURES / "name.png"` for figure output
- `dpi=300`, `bbox_inches='tight'`, `plt.close(fig)`
- Module docstring with inputs/outputs

**Stata target:**
- `version 17`, `clear all`, `set more off`
- `do "$root/code/stata/config_local.do"` for `$data_root`
- `log using "$root/quality_reports/stata_logs/[name].log", replace`
- `graphregion(color(white)) bgcolor(white)`, `width(2400)`
- `log close` at end

**R target:**
- `library()` calls at top
- `here::here()` for paths
- `ggsave(width = 8, height = 6, dpi = 300)`
- `set.seed(42)` if stochastic

## 5. Output Format

Present the translation as:

1. **Translated script** in a fenced code block
2. **Translation notes** section listing:
   - Any `# REVIEW:` items and why they were flagged
   - Differences in default behavior between languages (e.g., 0-vs-1 indexing)
   - Packages/libraries the target script requires

## 6. Run and Verify

After writing the translated script, run it and check for errors:

- **Python:** `python code/py/<script>.py`
- **Stata:** `stata -b do code/stata/<script>.do` (ALWAYS use the `stata` wrapper, never call `StataSE-64.exe` directly — the wrapper auto-moves batch logs to `quality_reports/stata_logs/`). Then check log for `r(`
- **R:** `Rscript code/R/<script>.R`

If it fails, fix only the syntax error (not the logic) and re-run. If the failure is due to a bug in the original, note it in Translation Notes.
