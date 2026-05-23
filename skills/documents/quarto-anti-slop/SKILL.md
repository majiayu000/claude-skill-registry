---
name: quarto-anti-slop
description: >
  Enforce reproducible research document standards for Quarto and RMarkdown.
  Prevents generic AI-generated documents through proper cross-referencing,
  bibliography management, and PDF-first practices for papers.
applies_to:
  - "**/*.qmd"
  - "**/*.Rmd"
  - "**/*.ipynb"
tags: [quarto, rmarkdown, reproducibility, academic-writing, literate-programming]
related_skills:
  - r/anti-slop
  - python/anti-slop
  - text/anti-slop
  - external/posit-skills/quarto/authoring
version: 2.0.0
---

# Quarto & RMarkdown Anti-Slop Skill

## When to Use This Skill

Use quarto-anti-slop when:
- ✓ Creating academic papers or technical reports
- ✓ Building reproducible research documents
- ✓ Reviewing AI-generated Quarto/RMarkdown documents
- ✓ Preparing manuscripts for journal submission
- ✓ Creating data analysis notebooks
- ✓ Building presentations with code
- ✓ Enforcing reproducibility standards

Do NOT use when:
- Writing quick exploratory notebooks (though standards still help)
- Working with non-technical documents (use text/anti-slop)
- Creating pure code projects (use language-specific anti-slop)

## Quick Example

**Before (AI Slop)**:
```yaml
---
title: "Analysis"
output: pdf_document
---

Figure 1 shows the results.

```{r}
data <- read.csv("data.csv")
plot(data$x, data$y)
```
```

**After (Anti-Slop)**:
```yaml
---
title: "Customer Retention Analysis"
author:
  - name: Jane Researcher
    affiliation: University Name
date: today
format:
  pdf:
    number-sections: true
    keep-tex: true
bibliography: references.bib
execute:
  echo: false
  cache: true
---

@fig-retention shows customer retention rates across cohorts.

```{r}
#| label: fig-retention
#| fig-cap: "Customer Retention by Cohort"
#| fig-width: 7
#| fig-height: 5

customer_data <- readr::read_csv("data/customers.csv")

ggplot2::ggplot(customer_data, ggplot2::aes(x = month, y = retention_rate)) +
  ggplot2::geom_line() +
  ggplot2::theme_minimal()
```
```

**What changed**:
- ✓ Complete metadata (author, affiliation, date)
- ✓ Proper cross-references (`@fig-retention`)
- ✓ Labeled code chunks with descriptive names
- ✓ Bibliography configuration
- ✓ Caching for reproducibility
- ✓ Descriptive figure captions

## When to Use What

| If you need to... | Do this | Reference |
|-------------------|---------|-----------|
| Academic paper | PDF format + cross-refs + citations | workflow-1-pdf-paper |
| Technical report | HTML format + code folding | workflow-2-html-report |
| Presentation | Revealjs or Beamer | YAML section |
| Cross-reference figures | `@fig-label` | Cross-Referencing |
| Cross-reference tables | `@tbl-label` | Cross-Referencing |
| Cross-reference equations | `@eq-label` | Mathematical Typesetting |
| Manage citations | BibTeX + CSL | Citations and References |
| Cache computations | `cache: true` + `dependson:` | Caching Strategy |
| Reproducibility | Session info + relative paths | Reproducibility Documentation |
| Fix generic YAML | Use complete metadata | YAML Configuration |

## Core Workflow

### 5-Step Quality Check

1. **Complete YAML metadata**
   ```yaml
   ---
   title: "Specific Descriptive Title"
   author:
     - name: Author Name
       affiliation: Institution
   date: today
   format:
     pdf:  # or html
       number-sections: true
   bibliography: references.bib
   ---
   ```

2. **Label all outputs**
   ```{r}
   #| label: fig-descriptive-name
   #| fig-cap: "Complete descriptive caption"
   ```

3. **Use cross-references**
   ```markdown
   @fig-name shows... @tbl-name presents... @eq-name defines...
   ```

4. **Cite properly**
   ```markdown
   Recent work [@author2023; @other2024] demonstrates...
   ```

5. **Verify reproducibility**
   - All paths relative to project root
   - Computations cached appropriately
   - Session info included

## Quick Reference Checklist

Before rendering final document:

- [ ] Title, author, affiliation complete
- [ ] Abstract present (if academic paper)
- [ ] All figures labeled: `#| label: fig-*`
- [ ] All tables labeled: `#| label: tbl-*`
- [ ] All equations labeled: `{#eq-*}`
- [ ] Cross-references use `@` syntax
- [ ] `bibliography:` in YAML with valid .bib file
- [ ] All citations use `@key` format
- [ ] Echo settings appropriate (false for papers)
- [ ] All paths relative to project root
- [ ] Long computations cached with `cache: true`
- [ ] Session info included in appendix
- [ ] Document renders from clean state
- [ ] No `editor: visual` line in YAML

## Common Workflows

### Workflow 1: Create PDF Research Paper

**Context**: Writing academic paper with statistical analysis.

**Steps**:

1. **Set up YAML with complete metadata**
   ```yaml
   ---
   title: "Your Research Title"
   author:
     - name: First Author
       affiliation: University Name
       email: author@university.edu
   date: today
   date-format: "MMMM D, YYYY"
   format:
     pdf:
       documentclass: article
       geometry: margin=1in
       number-sections: true
       colorlinks: true
       keep-tex: true
   abstract: |
     Brief summary of research question, methods, and findings.
   keywords: [keyword1, keyword2, keyword3]
   bibliography: references.bib
   csl: american-statistical-association.csl
   execute:
     echo: false
     warning: false
     message: false
     cache: true
   ---
   ```

2. **Structure with cross-referenced sections**
   ```markdown
   # Introduction {#sec-intro}

   # Data {#sec-data}

   # Methods {#sec-methods}

   # Results {#sec-results}

   As discussed in @sec-methods, we use...
   ```

3. **Create labeled figures**
   ```{r}
   #| label: fig-scatterplot
   #| fig-cap: "Relationship between X and Y with regression line"
   #| fig-width: 7
   #| fig-height: 5
   #| echo: false

   library(ggplot2)

   ggplot2::ggplot(data, ggplot2::aes(x = predictor, y = outcome)) +
     ggplot2::geom_point(alpha = 0.5) +
     ggplot2::geom_smooth(method = "lm", se = TRUE) +
     ggplot2::theme_minimal(base_size = 12) +
     ggplot2::labs(
       x = "Predictor Variable",
       y = "Outcome Variable"
     )
   ```

4. **Add regression tables**
   ```{r}
   #| label: tbl-regression
   #| tbl-cap: "Linear Regression Results"

   library(modelsummary)

   models <- list(
     "Model 1" = lm(outcome ~ predictor1, data = data),
     "Model 2" = lm(outcome ~ predictor1 + predictor2, data = data)
   )

   modelsummary::modelsummary(
     models,
     stars = c('*' = 0.1, '**' = 0.05, '***' = 0.01),
     gof_map = c("nobs", "r.squared", "adj.r.squared")
   )
   ```

5. **Add citations and references**
   ```markdown
   Recent work [@smith2020; @jones2021] shows...

   # References {.unnumbered}

   ::: {#refs}
   :::
   ```

6. **Include reproducibility info**
   ```markdown
   # Appendix: Computational Details {.unnumbered}

   ```{r}
   #| label: session-info
   #| echo: false

   sessionInfo()
   ```
   ```

**Expected outcome**: Publication-ready PDF with all cross-references working

---

### Workflow 2: Build HTML Technical Report

**Context**: Creating interactive analysis report with code visibility.

**Steps**:

1. **Set up HTML-specific YAML**
   ```yaml
   ---
   title: "Technical Analysis Report"
   author: "Your Name"
   date: today
   format:
     html:
       toc: true
       toc-depth: 3
       toc-location: left
       code-fold: true
       code-tools: true
       embed-resources: true
       theme: cosmo
   execute:
     echo: true
     warning: false
     message: false
   ---
   ```

2. **Create analysis sections with code folding**
   ```markdown
   # Data Loading {#sec-data}

   ```{r}
   #| label: load-data
   #| code-fold: show

   customer_data <- readr::read_csv("data/customers.csv")
   ```

   # Exploratory Analysis {#sec-eda}

   ```{r}
   #| label: fig-distribution
   #| fig-cap: "Distribution of Customer Ages"

   ggplot2::ggplot(customer_data, ggplot2::aes(x = age)) +
     ggplot2::geom_histogram(bins = 30)
   ```
   ```

3. **Add interactive tables**
   ```{r}
   #| label: tbl-summary
   #| tbl-cap: "Summary Statistics by Region"

   library(gtsummary)

   customer_data |>
     dplyr::select(region, age, revenue) |>
     gtsummary::tbl_summary(
       by = region,
       statistic = list(
         gtsummary::all_continuous() ~ "{mean} ({sd})"
       )
     )
   ```

4. **Use tabsets for multiple views**
   ```markdown
   ## Results by Region {.tabset}

   ### East

   Content for East region...

   ### West

   Content for West region...
   ```

5. **Test embedded resources**
   - Verify document is self-contained
   - Check all images display
   - Confirm code folding works

**Expected outcome**: Self-contained HTML with interactive features

---

### Workflow 3: Fix Generic Quarto Document

**Context**: AI generated a document with generic patterns.

**Steps**:

1. **Fix incomplete YAML**
   ```yaml
   # Before
   ---
   title: "Analysis"
   output: pdf_document
   ---

   # After
   ---
   title: "Customer Retention Analysis: 2023 Cohort Study"
   author:
     - name: Jane Researcher
       affiliation: Data Science Team
   date: today
   format:
     pdf:
       number-sections: true
       keep-tex: true
   bibliography: references.bib
   execute:
     echo: false
     cache: true
   ---
   ```

2. **Replace hard-coded references with cross-refs**
   ```markdown
   # Before
   Figure 1 shows the results.
   Table 2 presents the estimates.

   # After
   @fig-results shows the distribution across cohorts.
   @tbl-estimates presents the regression coefficients.
   ```

3. **Add labels to all code chunks**
   ```{r}
   # Before
   ```{r}
   plot(x, y)
   ```

   # After
   ```{r}
   #| label: fig-scatter
   #| fig-cap: "Relationship between X and Y"
   #| fig-width: 6
   #| fig-height: 4

   ggplot2::ggplot(data, ggplot2::aes(x = x, y = y)) +
     ggplot2::geom_point() +
     ggplot2::theme_minimal()
   ```
   ```

4. **Fix relative paths**
   ```{r}
   # Before
   data <- read.csv("/Users/someone/Desktop/data.csv")

   # After
   data <- readr::read_csv("data/analysis_data.csv")
   ```

5. **Add caching to long computations**
   ```{r}
   #| label: expensive-model
   #| cache: true

   large_model <- fit_complex_model(data)
   ```

6. **Include session info**
   ```markdown
   # Appendix {.unnumbered}

   ```{r}
   #| label: session-info
   sessionInfo()
   ```
   ```

**Expected outcome**: Professional document that follows reproducibility standards

---

### Workflow 4: Prepare Manuscript for Journal

**Context**: Converting analysis notebook to journal submission format.

**Steps**:

1. **Update YAML for journal requirements**
   ```yaml
   ---
   title: "Full Paper Title"
   author:
     - name: First Author
       affiliation: University
       orcid: 0000-0000-0000-0000
   abstract: |
     Complete abstract following journal guidelines.
   keywords: [key1, key2, key3]
   format:
     pdf:
       documentclass: article
       geometry: margin=1in
       number-sections: true
       keep-tex: true
   bibliography: references.bib
   csl: journal-of-statistics.csl  # Journal-specific
   ---
   ```

2. **Verify all cross-references**
   ```bash
   # Check for hard-coded references
   grep -n "Figure [0-9]" manuscript.qmd
   grep -n "Table [0-9]" manuscript.qmd

   # Should find none - all should use @fig-* or @tbl-*
   ```

3. **Format equations with labels**
   ```markdown
   $$
   y_i = \beta_0 + \beta_1 x_i + \epsilon_i
   $$ {#eq-model}

   The model in @eq-model assumes...
   ```

4. **Check bibliography completeness**
   - All citations in .bib file
   - DOIs included where available
   - Journal names not abbreviated

5. **Add line numbers (if required)**
   ```yaml
   format:
     pdf:
       include-in-header:
         text: |
           \usepackage{lineno}
           \linenumbers
   ```

6. **Verify reproducibility**
   ```bash
   # Clean render from scratch
   quarto render manuscript.qmd
   ```

**Expected outcome**: Submission-ready manuscript meeting journal standards

## Mandatory Rules Summary

### 1. Complete YAML Metadata
**ALWAYS include**: title, author with affiliation, date, format settings

### 2. Label All Outputs
**Figures**: `#| label: fig-name`
**Tables**: `#| label: tbl-name`
**Equations**: `{#eq-name}`

### 3. Use Cross-References
**Never**: "Figure 1", "Table 2"
**Always**: `@fig-name`, `@tbl-name`, `@eq-name`

### 4. Relative Paths Only
**Never**: `/Users/name/Desktop/data.csv`
**Always**: `data/analysis_data.csv`

### 5. Bibliography Management
**ALWAYS**: Use BibTeX + `bibliography:` in YAML
**Never**: Manual reference lists

### 6. Reproducibility Documentation
**ALWAYS**: Include session info, cache long computations, set seeds

## Quarto vs RMarkdown

**Quarto** (recommended for new projects):
- Language-agnostic (R, Python, Julia, Observable)
- Modern YAML with `#|` chunk options
- Better cross-referencing
- Native multiple format support

**RMarkdown** (legacy, still widely used):
- R-specific but mature ecosystem
- Traditional chunk options in header
- Needs bookdown for advanced cross-refs

**This skill covers both** - most patterns are compatible.

## Forbidden Patterns

### Never Do These

**1. Hard-Coded Figure References**
```markdown
# WRONG
Figure 1 shows the results.

# CORRECT
@fig-results shows the distribution.
```

**2. Missing Chunk Labels**
```{r}
# WRONG - no label
plot(x, y)

# CORRECT
#| label: fig-scatter
#| fig-cap: "X vs Y relationship"
plot(x, y)
```

**3. Absolute Paths**
```{r}
# WRONG
data <- read_csv("/Users/me/Desktop/data.csv")

# CORRECT
data <- readr::read_csv("data/analysis_data.csv")
```

**4. Visual Editor Artifacts**
```yaml
# WRONG - remove this
editor: visual
```

**5. Inline Code for Papers (OK for reports)**
```markdown
# WRONG in published papers
The sample size is `r nrow(data)`.

# CORRECT in papers
The sample size is 1,542 observations.

# OK in technical reports/notebooks
The sample size is `r nrow(data)`.
```

## Mathematical Typesetting

### Inline vs Display

```markdown
CORRECT inline: The mean is $\bar{x} = \frac{1}{n}\sum_{i=1}^n x_i$.

CORRECT display:
$$
\hat{\beta} = (X^TX)^{-1}X^Ty
$$ {#eq-ols}

Reference: The OLS estimator (@eq-ols) minimizes...
```

### Common Notation

```latex
# Greek letters
$\alpha, \beta, \gamma, \mu, \sigma$

# Statistics
$\bar{x}$ (mean), $\hat{\beta}$ (estimate), $\tilde{x}$ (alternative)
$\mathbb{E}[X]$ (expectation), $\text{Var}(X)$ (variance)

# Matrices
$X^T$ (transpose), $X^{-1}$ (inverse), $\|x\|$ (norm)
```

## Citations and References

### Setup

```yaml
bibliography: references.bib
csl: journal-style.csl  # From https://github.com/citation-style-language/styles
link-citations: true
```

### In-Text Citations

```markdown
Recent work [@smith2020; @jones2021] shows...

According to @brown2019, the effect is significant.

Multiple studies [e.g., @davis2018; @wilson2022] demonstrate...
```

### BibTeX Format

```bibtex
@article{smith2020,
  title = {An Important Study},
  author = {Smith, John and Doe, Jane},
  journal = {Journal of Important Research},
  volume = {10},
  pages = {123--145},
  year = {2020},
  doi = {10.1234/journal.2020.001}
}
```

## Caching Strategy

### Document-Level
```yaml
execute:
  cache: true
  freeze: auto  # Prevents re-execution unless code changes
```

### Chunk-Level with Dependencies
```{r}
#| label: load-data
#| cache: true

raw_data <- readr::read_csv("large_dataset.csv")
```

```{r}
#| label: analyze
#| cache: true
#| dependson: "load-data"

model <- lm(outcome ~ predictor, data = raw_data)
```

## Code Chunk Best Practices

### Quarto Syntax
```{r}
#| label: fig-name
#| fig-cap: "Caption here"
#| fig-width: 7
#| fig-height: 5
#| echo: false
#| message: false

# Code here
```

### Critical Options

**For Figures:**
- `label: fig-*` - Required for cross-refs
- `fig-cap:` - Descriptive caption
- `fig-width:`, `fig-height:` - Explicit dimensions

**For Tables:**
- `label: tbl-*` - Required for cross-refs
- `tbl-cap:` - Descriptive caption

**For Computations:**
- `cache: true` - Cache expensive operations
- `dependson:` - Specify dependencies

## Document Structure Templates

### Research Paper
```markdown
# Introduction {#sec-intro}

# Literature Review {#sec-literature}

# Data {#sec-data}

# Methods {#sec-methods}

# Results {#sec-results}

# Discussion {#sec-discussion}

# Conclusion {#sec-conclusion}

# References {.unnumbered}

::: {#refs}
:::

# Appendix {.unnumbered #sec-appendix}
```

### Technical Report
```markdown
# Setup {#sec-setup}

# Data Loading {#sec-data}

# Exploratory Analysis {#sec-eda}

# Statistical Modeling {#sec-modeling}

# Conclusions {#sec-conclusions}
```

## Reproducibility Documentation

### Session Information
```{r}
#| label: session-info
#| echo: false

sessionInfo()
# Or more detailed:
# sessioninfo::session_info()
```

### Computational Environment
```markdown
# Appendix: Computational Details {.unnumbered}

All analyses conducted in R version `r R.version.string`.
```

## Presentations

### Reveal.js (HTML)
```markdown
## Slide Title

Content goes here

::: {.incremental}
- Appears first
- Appears second
:::

## Columns

:::: {.columns}
::: {.column width="50%"}
Left content
:::

::: {.column width="50%"}
Right content
:::
::::
```

### Beamer (PDF)
```yaml
---
title: "Presentation"
format:
  beamer:
    theme: Madrid
    colortheme: default
---
```

## Resources & Advanced Topics

### Reference Materials

Comprehensive coverage in main document above covers:
- YAML configuration patterns
- Cross-referencing systems
- Bibliography management
- Code chunk options
- Caching strategies
- Mathematical typesetting
- Document structure templates

### Related Skills

- **r/anti-slop** - For cleaning R code in chunks
- **python/anti-slop** - For cleaning Python code in chunks
- **text/anti-slop** - For cleaning prose sections
- **external/posit-skills/quarto/authoring** - For Quarto syntax and features

### Tools

- `quarto render` - Render document
- `quarto preview` - Live preview
- `quarto check` - Verify installation

## Integration with Posit Skills

This skill focuses on **preventing generic AI-generated documents** through reproducibility standards.

Use together with Posit skills for complete coverage:

| Task | Use This Skill | + Posit Skill |
|------|----------------|---------------|
| Write new Quarto doc | quarto/anti-slop (quality) | + quarto/authoring (syntax) |
| Convert from Rmd | quarto/anti-slop (standards) | + quarto/authoring (migration) |
| Cross-reference figures | quarto/anti-slop (enforce) | + quarto/authoring (syntax) |
| Create presentation | quarto/anti-slop (quality) | + quarto/authoring (features) |

**Key distinction**:
- **Posit skills** teach Quarto syntax and features
- **This skill** enforces quality and prevents generic patterns

Both are complementary equals for creating professional reproducible documents.
