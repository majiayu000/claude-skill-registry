---
name: quarto-authoring
description: >
  Writing and authoring Quarto documents (.qmd), including code cell options,
  figure and table captions, cross-references, callout blocks (notes, warnings,
  tips), citations and bibliography, page layout and columns, Mermaid diagrams,
  YAML metadata configuration, and Quarto extensions. Also covers converting and
  migrating R Markdown (.Rmd), bookdown, blogdown, xaringan, and distill projects
  to Quarto, and creating Quarto websites, books, presentations, and reports.
metadata:
  author: Mickaël Canouil (@mcanouil)
  version: "1.1"
license: MIT
---

# Quarto Authoring

> This skill is based on Quarto CLI v1.8.26.

## When to Use What

Task: Write a new Quarto document
Use: Follow "QMD Essentials" below, then see specific reference files

Task: Convert R Markdown to Quarto
Use: [references/conversion-rmarkdown.md](references/conversion-rmarkdown.md)

Task: Migrate bookdown project
Use: [references/conversion-bookdown.md](references/conversion-bookdown.md)

Task: Migrate xaringan slides
Use: [references/conversion-xaringan.md](references/conversion-xaringan.md)

Task: Migrate distill article
Use: [references/conversion-distill.md](references/conversion-distill.md)

Task: Migrate blogdown site
Use: [references/conversion-blogdown.md](references/conversion-blogdown.md)

Task: Add cross-references
Use: [references/cross-references.md](references/cross-references.md)

Task: Configure code cells
Use: [references/code-cells.md](references/code-cells.md)

Task: Add figures with captions
Use: [references/figures.md](references/figures.md)

Task: Create tables
Use: [references/tables.md](references/tables.md)

Task: Add citations and bibliography
Use: [references/citations.md](references/citations.md)

Task: Add callout blocks
Use: [references/callouts.md](references/callouts.md)

Task: Add diagrams (Mermaid, Graphviz)
Use: [references/diagrams.md](references/diagrams.md)

Task: Control page layout
Use: [references/layout.md](references/layout.md)

Task: Use shortcodes
Use: [references/shortcodes.md](references/shortcodes.md)

Task: Add conditional content
Use: [references/conditional-content.md](references/conditional-content.md)

Task: Use divs and spans
Use: [references/divs-and-spans.md](references/divs-and-spans.md)

Task: Configure YAML front matter
Use: [references/yaml-front-matter.md](references/yaml-front-matter.md)

Task: Find and use extensions
Use: [references/extensions.md](references/extensions.md)

Task: Apply markdown linting rules
Use: [references/markdown-linting.md](references/markdown-linting.md)

## QMD Essentials

### Basic Document Structure

```markdown
---
title: "Document Title"
author: "Author Name"
date: today
format: html
---

Content goes here.
```

A Quarto document consists of two main parts:

1. **YAML Front Matter**: Metadata and configuration at the top, enclosed by `---`.
2. **Markdown Content**: Main body using standard markdown syntax.

### Divs and Spans

Divs use fenced syntax with three colons:

```markdown
::: {.class-name}
Content inside the div.
:::
```

Spans use bracketed syntax:

```markdown
This is [important text]{.highlight}.
```

Details: [references/divs-and-spans.md](references/divs-and-spans.md)

### Code Cell Options Syntax

A code cell starts with triple backticks and a language identifier between curly braces.
Code cells are code blocks that can be executed to produce output.

Quarto uses the language's comment symbol + `|` for cell options. Options use **dashes, not dots** (e.g., `fig-cap` not `fig.cap`).

- R, Python: `#|`
- Mermaid: `%%|`
- Graphviz/DOT: `//|`

````markdown
```{r}
#| label: fig-example
#| echo: false
#| fig-cap: "A scatter plot example."

plot(x, y)
```
````

Common execution options:

| Option    | Description       | Values                    |
| --------- | ----------------- | ------------------------- |
| `eval`    | Evaluate code     | `true`, `false`           |
| `echo`    | Show code         | `true`, `false`, `fenced` |
| `output`  | Include output    | `true`, `false`, `asis`   |
| `warning` | Show warnings     | `true`, `false`           |
| `error`   | Show errors       | `true`, `false`           |
| `include` | Include in output | `true`, `false`           |

Set document-level defaults in YAML front matter:

```yaml
execute:
  echo: false
  warning: false
```

Details: [references/code-cells.md](references/code-cells.md)

### Cross-References

Labels must start with a type prefix. Reference with `@`:

- Figure: `fig-` prefix, e.g., `#| label: fig-plot` → `@fig-plot`
- Table: `tbl-` prefix, e.g., `#| label: tbl-data` → `@tbl-data`
- Section: `sec-` prefix, e.g., `{#sec-intro}` → `@sec-intro`
- Equation: `eq-` prefix, e.g., `{#eq-model}` → `@eq-model`

````markdown
```{r}
#| label: fig-plot
#| fig-cap: "A caption for the plot."
plot(1)
```

See @fig-plot for the results.
````

Details: [references/cross-references.md](references/cross-references.md)

### Callout Blocks

Five types: `note`, `warning`, `important`, `tip`, `caution`.

```markdown
::: {.callout-note}
This is a note callout.
:::

::: {.callout-warning}

## Custom Title

This is a warning with a custom title.

:::
```

Details: [references/callouts.md](references/callouts.md)

### Figures

```markdown
![Caption text](image.png){#fig-name fig-alt="Alt text"}
```

Subfigures:

```markdown
::: {#fig-group layout-ncol=2}
![Sub caption 1](image1.png){#fig-sub1}

![Sub caption 2](image2.png){#fig-sub2}

Main caption for the group.
:::
```

Details: [references/figures.md](references/figures.md)

### Tables

```markdown
::: {#tbl-example}

| Column 1 | Column 2 |
| -------- | -------- |
| Data 1   | Data 2   |

Table caption.
:::
```

Details: [references/tables.md](references/tables.md)

### Citations

```markdown
According to @smith2020, the results show...
Multiple citations [@smith2020; @jones2021].
```

Configure in YAML:

```yaml
bibliography: references.bib
csl: apa.csl
```

Details: [references/citations.md](references/citations.md)

## Common Workflows

### Creating an HTML Document

```yaml
title: "My Report"
author: "Your Name"
date: today
format:
  html:
    toc: true
    code-fold: true
    theme: cosmo
```

### Creating a PDF Document

```yaml
title: "My Report"
format:
  pdf:
    documentclass: article
    papersize: a4
```

### Creating a RevealJS Presentation

```markdown
---
title: "My Presentation"
format: revealjs
---

## First Slide

Content here.

## Second Slide

More content.
```

### Setting Up a Quarto Project

Create `_quarto.yml` in the project root:

```yaml
project:
  type: website

website:
  title: "My Site"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: about.qmd
        text: About

format:
  html:
    theme: cosmo
```

## Resources

- [Quarto Documentation](https://quarto.org/docs/)
- [Quarto Guide](https://quarto.org/docs/guide/)
- [Quarto Extensions](https://quarto.org/docs/extensions/)
- [Community Extensions List](https://m.canouil.dev/quarto-extensions/)
