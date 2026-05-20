---
name: quarto
description: This skill should be used when users need to create, configure, or render Quarto documents (.qmd files). Use this skill for generating reports, analysis documents, or presentations with HTML or Typst output formats, integrating code chunks (Python, R, Stata), and troubleshooting rendering issues.
---

# Quarto Document Generation Skill

## Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Quick Start](#quick-start)
- [Output Formats](#output-formats)
- [Code Chunks](#code-chunks)
- [Document Workflow](#document-workflow)
- [Project Configuration](#project-configuration)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## When to Use This Skill

| Task | Use This Skill |
| ------ | ---------------- |
| Create .qmd documents | Yes |
| Configure HTML/Typst output | Yes |
| Embed Python/R/Stata code | Yes |
| Set up Quarto projects | Yes |
| Debug rendering issues | Yes |
| Generate reports from templates | Yes |

## Quick Start

### Basic Document Structure

```markdown
---
title: "Document Title"
author: "Author Name"
date: "2025-01-05"
format:
  html:
    toc: true
    code-fold: true
---

# Introduction

Content here...

```{python}
# Code chunk
import pandas as pd
```

### Render Commands

```bash
quarto render document.qmd          # Default format
quarto render document.qmd --to html
quarto render document.qmd --to typst
quarto preview document.qmd         # Live preview
```

## Output Formats

### HTML vs Typst

| Feature | HTML | Typst |
| --------- | ------ | ------- |
| Best for | Web, interactive | Print, PDF |
| Code folding | Yes | No |
| Embedded resources | Yes | N/A |
| Math rendering | KaTeX/MathJax | Native |
| Custom fonts | CSS | Direct |

### HTML Configuration

```yaml
format:
  html:
    toc: true
    toc-depth: 3
    code-fold: true
    code-tools: true
    embed-resources: true
    theme: cosmo
```

### Typst Configuration

```yaml
format:
  typst:
    toc: true
    number-sections: true
    papersize: us-letter
    margin:
      x: 1.25in
      y: 1.25in
    fontsize: 11pt
```

### Multiple Formats

```yaml
format:
  html:
    toc: true
  typst:
    toc: true
```

## Code Chunks

### Cell Options

| Option | Effect |
| -------- | -------- |
| `echo: false` | Hide code, show output |
| `eval: false` | Show code, don't run |
| `output: false` | Hide all output |
| `warning: false` | Suppress warnings |
| `include: false` | Run but show nothing |
| `error: true` | Show errors, don't fail |
| `cache: true` | Cache results |

### Python Example

````markdown
```{python}
#| label: fig-plot
#| fig-cap: "My Figure"
#| echo: false

import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [1, 4, 9])
plt.show()
```

````

### Cross-References

````markdown
See @fig-plot for visualization.
Results in @tbl-results.
Methods in @sec-methods.

## Methods {#sec-methods}

```{python}
#| label: fig-plot
#| fig-cap: "My plot"
```

````

## Document Workflow

### 1. Create Document

```bash
# Using template script
uv run python .claude/skills/quarto/scripts/create_quarto.py \
  --output report.qmd \
  --title "My Report" \
  --format html \
  --template analysis
```

Template types: `analysis`, `report`, `presentation`, `article`

### 2. Validate YAML

```bash
uv run python .claude/skills/quarto/scripts/validate_yaml.py document.qmd
```

### 3. Edit Content

- Write markdown and code chunks
- Use cell options to control output
- Add cross-references for figures/tables

### 4. Preview

```bash
quarto preview document.qmd
```

### 5. Render Final

```bash
quarto render document.qmd
quarto render document.qmd --to all  # All formats
```

### 6. Batch Render

```bash
uv run python .claude/skills/quarto/scripts/render_all.py \
  --pattern "reports/*.qmd"
```

## Project Configuration

### _quarto.yml

```yaml
project:
  type: default
  output-dir: _output

format:
  html:
    theme: cosmo
    toc: true
    code-fold: true
  typst:
    toc: true

execute:
  echo: true
  warning: false
  cache: true
```

### Recommended Structure

```
project/
├── analysis/
│   ├── 01_import.qmd
│   └── 02_analyze.qmd
├── reports/
│   └── summary.qmd
├── _quarto.yml
├── references.bib
└── data/
```

## Troubleshooting

### YAML Errors

1. Use spaces, not tabs for indentation
2. Ensure colons have space after: `key: value`
3. Quote strings with special characters
4. Validate with: `uv run python .claude/skills/quarto/scripts/validate_yaml.py`

### Code Execution Errors

1. Verify kernel is installed (`jupyter`, `IRkernel`)
2. Check code chunk syntax (triple backticks + language)
3. Use `#| error: true` to show errors without failing
4. Check file paths are relative and correct

### Rendering Failures

1. Run `quarto check` to verify installation
2. Use `quarto render --verbose` for details
3. Check for missing packages in code chunks
4. For Typst: ensure Quarto 1.4+ is installed

### Debug Commands

```bash
quarto check              # Verify installation
quarto render --verbose   # Detailed output
quarto render --keep-md   # Keep intermediate files
```

## References

### Project References

- [Quick Reference](references/quarto_quick_reference.md) - Comprehensive syntax reference

### Available Assets

| Template | Description |
| ---------- | ------------- |
| `assets/template_html.qmd` | Basic HTML analysis |
| `assets/template_typst.qmd` | Basic Typst document |
| `assets/template_dual.qmd` | Both formats |
| `assets/template_report.qmd` | Formal report |
| `assets/_quarto.yml` | Project configuration |

### Available Scripts

| Script | Purpose |
| -------- | --------- |
| `scripts/create_quarto.py` | Generate from templates |
| `scripts/render_all.py` | Batch render |
| `scripts/validate_yaml.py` | Check YAML syntax |

### External Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [HTML Format Guide](https://quarto.org/docs/output-formats/html-basics.html)
- [Typst Format Guide](https://quarto.org/docs/output-formats/typst.html)
- [Code Execution](https://quarto.org/docs/computations/execution-options.html)
- [Cross-References](https://quarto.org/docs/authoring/cross-references.html)

## Best Practices

1. **Use relative paths** - Keep documents portable
2. **Cache long computations** - `cache: true` for expensive chunks
3. **Test incrementally** - Render frequently during development
4. **Use project config** - Set common options in `_quarto.yml`
5. **Version control .qmd** - Commit source, not rendered output
6. **Document dependencies** - List required packages in setup chunk
