---
name: alt-text
description: >
  Generate and improve accessible alt text for data visualizations and images
  in R packages and Quarto documents. Use when the user wants to add, improve,
  or audit alt text for figures in a pkgdown site or .qmd files. Activate for
  requests that mention fig-alt, fig.alt, figure descriptions, or alt text in
  the context of an R package or Quarto document.
metadata:
  author: Emil Hvitfeldt (@emilhvitfeldt)
  version: "1.0"
license: MIT
---

# Write Accessible Alt Text

Generate accessible alt text for data visualizations and images in this project.

ARGUMENTS
- label: (optional) specific figure label or chunk to target
- file: (optional) specific file to process

## Detect project type

Before proceeding, identify the project context and read the relevant reference.
Check for a `_pkgdown.yml` file in the project root to detect a pkgdown site:

```bash
ls _pkgdown.yml 2>/dev/null && echo "pkgdown" || echo "not pkgdown"
```

- **pkgdown site** (`_pkgdown.yml` present) → read `references/pkgdown.md`
- **Quarto documents** (no `_pkgdown.yml`, `.qmd` files present) → read `references/quarto.md`

If the context is still ambiguous, ask the user which format they are working in.

## Key advantage: source code access

Unlike typical alt text scenarios where you only see an image, **we have access to the code that generates each chart**. Use this to extract precise details:

**From plotting code:**
- Variable mappings → exact variable names for axes
- Color/fill mappings → what color encodes
- Plot type functions → scatter, histogram, line chart, etc.
- Trend lines or fitted curves → overlaid statistical fits
- Faceting/subplots → number of panels and what varies
- Color scales → encoding scheme (sequential, diverging, categorical)
- Axis labels and titles → customized labels

**From data generation code:**
- Random distributions → expected distribution shape
- Transformations → what was done to data
- Feature engineering → preprocessing applied
- Filtering/subsetting → what subset is shown

**From surrounding prose:**
- Text before/after the chunk explains the **purpose** and **key insight**
- Chapter context tells you what the figure is meant to teach
- This is often the best source for the "key insight" part of alt text

## Three-part structure (Amy Cesal's formula)

1. **Chart type** — first words identify the format
2. **Data description** — axes, variables, what is shown
3. **Key insight** — the pattern or takeaway (often found in surrounding text)

## Relationship to captions

Read the caption (`fig-cap`, `fig.cap`) first. Alt text should **complement, not duplicate** it:
- If the caption states the insight, alt text can focus on describing the visual structure
- If the caption is generic, alt text should include the key insight
- Together they should give a complete understanding

## Content rules

**Include:**
- Chart type as first words
- Axis labels and what they represent
- Specific values/ranges when code reveals them (e.g., "peaks between 25–50")
- Number of panels/facets
- What color/size encodes if used
- The key pattern that supports the surrounding point

**Exclude:**
- "Image of…" or "Chart showing…" (screen readers announce this)
- Decorative color descriptions (unless color encodes data)
- Information already in the caption
- Implementation details (package names, function internals)

## Length guidelines

| Complexity | Sentences | When to use                                  |
|------------|-----------|----------------------------------------------|
| Simple     | 2–3       | Single geom, no facets, obvious pattern      |
| Standard   | 3–4       | Multiple geoms or color encoding             |
| Complex    | 4–5       | Faceted, multiple overlays, nuanced insight  |

## Quality checklist

- [ ] Starts with chart type (Scatter chart, Histogram, Faceted bar chart, etc.)
- [ ] Names the axis variables
- [ ] Includes specific values/ranges from code when informative
- [ ] States the key insight from surrounding prose
- [ ] Complements (not duplicates) the caption
- [ ] Would make sense to someone who cannot see the image
- [ ] Uses plain language (avoid jargon like "geom" or "aesthetic")

## Template patterns

**Scatter chart:**
```
Scatter chart. [X var] along the x-axis, [Y var] along the y-axis.
[Shape: linear/curved/clustered]. [Specific pattern, e.g., "peaks when X is 25–50"].
[Any overlaid fits or annotations].
```

**Histogram:**
```
Histogram of [variable]. [Shape: right-skewed/bimodal/normal/uniform].
[If transformed: "after [transformation], the distribution [result]"].
[Notable features: outliers, gaps, multiple modes].
```

**Bar chart:**
```
Bar chart. [Categories] along the x-axis, [measure] along the y-axis.
[Key comparison: which is highest/lowest, relative differences].
[Pattern: increasing/decreasing/grouped].
```

**Tile/raster chart:**
```
Tile chart [or heatmap]. [Row variable] along the y-axis, [column variable] along the x-axis.
Color encodes [what value]. [Pattern: where values are high/low].
[If faceted: "N panels showing [what varies]"].
```

**Faceted chart:**
```
Faceted [chart type] with [N] panels, one per [faceting variable].
[What's constant across panels]. [What changes/varies].
[Key comparison or insight across panels].
```

**Correlation heatmap:**
```
Correlation [matrix/heatmap] of [what variables]. [Arrangement].
[Overall pattern: mostly positive/negative/mixed].
[Notable clusters or strong/weak pairs].
[If relevant: contrast with expected behavior].
```

**Before/after comparison:**
```
[N] [chart type]s arranged [vertically/in grid]. [Top/Left] shows [original].
[Bottom/Right] shows [transformed]. [Key difference/similarity].
[If overlay: "[color] curve shows [reference]"].
```

**Line chart with overlays:**
```
[Line/Scatter] chart with overlaid [fits/curves]. [Axes].
[Number] of [lines/fits] shown: [list what each represents].
[Which fits well vs. poorly and why].
```

## Example

**Code context:**
```r
plotting_data |>
  ggplot(aes(value)) +
  geom_histogram(binwidth = 0.2) +
  facet_grid(name~., scales = "free_y") +
  geom_line(aes(x, y), data = norm_curve, color = "green4")
```

**Surrounding prose says:** "Normalization doesn't make data more normal"

**Caption:** "Normalization doesn't make data more normal. The green curve indicates the density of the unit normal distribution."

**Good alt text:**
```
Faceted histogram with two panels stacked vertically. Top panel shows
original data with a bimodal distribution. Bottom panel shows the same
data after z-score normalization, retaining the bimodal shape. A green
normal distribution curve overlaid on the bottom panel clearly does not
match the data, demonstrating that normalization preserves distribution
shape rather than creating normality.
```
