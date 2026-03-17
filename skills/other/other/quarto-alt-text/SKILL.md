---
name: quarto-alt-text
description: >
  Generate accessible alt text for data visualizations in Quarto documents. Use
  when the user wants to add, improve, or review alt text for figures in .qmd
  files. Triggers for requests about accessibility, figure descriptions, fig-alt,
  screen reader support, or making Quarto documents more accessible.
metadata:
  author: Emil Hvitfeldt (@emilhvitfeldt)
  version: "1.0"
license: MIT
---

# Write Chart Alt Text

Generate accessible alt text for data visualizations in this project.

ARGUMENTS
- label: (optional) specific fig- label to generate alt text for
- file: (optional) specific .qmd file to process

## Instructions

When invoked, analyze the figure(s) and generate alt text following these guidelines:

### Key Advantage: Source Code Access

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

### Three-Part Structure (Amy Cesal's Formula)

1. **Chart type** - First words identify the format
2. **Data description** - Axes, variables, what's shown
3. **Key insight** - The pattern or takeaway (often found in surrounding text)

### Relationship to fig-cap

Read the `fig-cap` first. The alt text should **complement, not duplicate** it:
- If caption states the insight, alt text can focus on describing the visual structure
- If caption is generic, alt text should include the key insight
- Together they should give a complete understanding

### Content Rules

**Include:**
- Chart type as first words
- Axis labels and what they represent
- Specific values/ranges when code reveals them (e.g., "peaks between 25-50")
- Number of panels/facets
- What color/size encodes if used
- The key pattern that supports the chapter's point

**Exclude:**
- "Image of..." or "Chart showing..." (screen readers announce this)
- Decorative color descriptions (unless color encodes data)
- Information already in fig-cap
- Implementation details (package names, function internals)

### Length Guidelines

| Complexity | Sentences | When to use                                 |
|------------|-----------|---------------------------------------------|
| Simple     | 2-3       | Single geom, no facets, obvious pattern     |
| Standard   | 3-4       | Multiple geoms or color encoding            |
| Complex    | 4-5       | Faceted, multiple overlays, nuanced insight |

### Quality Checklist

- [ ] Starts with chart type (Scatter chart, Histogram, Faceted bar chart, etc.)
- [ ] Names the axis variables
- [ ] Includes specific values/ranges from code when informative
- [ ] States the key insight from surrounding prose
- [ ] Complements (not duplicates) the fig-cap
- [ ] Would make sense to someone who cannot see the image
- [ ] Uses plain language (avoid jargon like "geom" or "aesthetic")

## Template Patterns

**Scatter chart:**
```
Scatter chart. [X var] along the x-axis, [Y var] along the y-axis.
[Shape: linear/curved/clustered]. [Specific pattern, e.g., "peaks when X is 25-50"].
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
[If relevant: contrast with expected behavior, e.g., "unlike PCA, these are not orthogonal"].
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

## Workflow

### Finding Figures

To find all figure chunks in the project:
```bash
# List all figure labels with file and line number
grep -n "#| label: fig-" *.qmd

# Find figures in a specific file
grep -n "#| label: fig-" numeric-splines.qmd

# Find a specific figure
grep -rn "#| label: fig-splines-predictor-outcome" *.qmd
```

### For Each Figure

1. **Locate** - Use grep to find file and line number
2. **Read context** - Read ~50 lines around the chunk (prose before + code + prose after)
3. **Extract details** - Note fig-cap, ggplot code, data generation, surrounding explanation
4. **Draft alt text** - Apply three-part structure (type → data → insight)
5. **Verify** - Check against quality checklist

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

**fig-cap:** "Normalization doesn't make data more normal. The green curve indicates the density of the unit normal distribution."

**Good alt text:**
```
#| fig-alt: |
#|   Faceted histogram with two panels stacked vertically. Top panel shows
#|   original data with a bimodal distribution. Bottom panel shows the same
#|   data after z-score normalization, retaining the bimodal shape. A green
#|   normal distribution curve overlaid on the bottom panel clearly does not
#|   match the data, demonstrating that normalization preserves distribution
#|   shape rather than creating normality.
```
