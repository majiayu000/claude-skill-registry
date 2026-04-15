---
name: data-visualization
description: Grammar of graphics, chart type selection, color theory, interactive visualization, dashboards, and the principles of honest, effective data display. Covers Tufte's data-ink ratio, Bertin's visual variables, perceptual principles, accessibility, small multiples, annotation, and the full workflow from exploratory plots to publication-quality graphics. Use when creating charts, designing dashboards, critiquing visualizations, or choosing how to display data.
type: skill
category: data-science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/data-science/data-visualization/SKILL.md
superseded_by: null
---
# Data Visualization

Data visualization is the translation of data into visual form for the purpose of communication, exploration, or analysis. A good visualization reveals what the data has to say; a bad one obscures or distorts it. This skill covers the principles, techniques, and design decisions involved in creating honest, effective data displays, drawing primarily on Edward Tufte's principles, Leland Wilkinson's Grammar of Graphics, and Jacques Bertin's visual semiology.

**Agent affinity:** tufte (design principles, critique), nightingale (routing visualization tasks), cairo (pedagogy of visual literacy)

**Concept IDs:** data-chart-types, data-visual-design, data-misleading-graphs, data-data-storytelling

## Core Principles

### Tufte's Principles

Edward Tufte's work established the foundational principles of honest data display:

1. **Data-ink ratio.** Maximize the proportion of ink devoted to data. Every element that does not convey data is potential chartjunk -- decorative gridlines, 3D effects, gradient fills, clip art.

2. **Chartjunk.** Visual elements that do not represent data: moiré patterns, heavy gridlines, unnecessary ornamentation, 3D perspective on 2D data. Remove it.

3. **Lie factor.** The ratio of the visual effect to the numerical effect. A bar chart where a 2x increase in data is represented by a 4x increase in area has a lie factor of 2. Lie factor should be between 0.95 and 1.05.

4. **Small multiples.** Repeating the same chart structure across panels to show variation across a categorical variable. More effective than animation or overlapping colors for showing change.

5. **Data density.** The amount of data per unit area of the graphic. High data density is efficient -- sparklines, for example, embed a time series in the space of a word.

6. **Micro/macro readings.** A good visualization works at both levels: the overall pattern is visible at a glance (macro), and individual data points can be read precisely (micro).

### Bertin's Visual Variables

Jacques Bertin (1967) identified the fundamental visual channels available for encoding data:

| Variable | Data type | Effectiveness | Notes |
|---|---|---|---|
| **Position** | Quantitative | Highest | Most accurately perceived; always the first choice for the most important variable |
| **Length** | Quantitative | Very high | Bar charts; humans compare lengths well |
| **Angle/Slope** | Quantitative | Moderate | Scatterplot slopes; pie chart angles are poorly perceived |
| **Area** | Quantitative | Low-moderate | Bubble charts; humans underestimate area differences |
| **Color saturation** | Quantitative (ordered) | Low-moderate | Sequential palettes; limited dynamic range |
| **Color hue** | Categorical | High for categories | Qualitative palettes; maximum ~8 distinguishable hues |
| **Shape** | Categorical | Moderate | Point markers; maximum ~6 distinguishable shapes |
| **Texture** | Categorical | Low | Rarely used in modern visualization |

**Design implication:** Map the most important variable to position, the second most important to length or color, and use less effective channels for less important variables. Never use area or angle for the primary quantitative comparison.

### Perceptual Principles

- **Weber's law:** We perceive relative differences, not absolute ones. A 10% change is equally noticeable whether the baseline is 100 or 1000.
- **Pre-attentive processing:** Color, orientation, size, and motion are detected before conscious attention. Use these for the feature you want the viewer to notice immediately.
- **Gestalt principles:** Proximity, similarity, enclosure, connection, and continuity govern how we group visual elements. Leverage these for layout.
- **Change blindness:** Small changes in a complex display go unnoticed. If comparison is the goal, place the things being compared adjacent or overlapping.

## Chart Selection Guide

### Choosing by Data Relationship

| Relationship | Chart type | Example |
|---|---|---|
| **Distribution (1 variable)** | Histogram, density plot, box plot, violin plot | Distribution of household incomes |
| **Comparison (categories)** | Bar chart (horizontal for many categories), dot plot | Revenue by department |
| **Trend (time series)** | Line chart | Monthly temperature over 10 years |
| **Correlation (2 quantitative)** | Scatter plot | Height vs. weight |
| **Part-to-whole** | Stacked bar, treemap, waffle chart | Market share by company |
| **Ranking** | Sorted bar chart, bump chart | Top 20 countries by GDP |
| **Geospatial** | Choropleth, dot map, cartogram | COVID cases by county |
| **Flow/Network** | Sankey, alluvial, node-link diagram | Customer journey through website |
| **Composition over time** | Stacked area, streamgraph | Energy sources as share of total over decades |

### Charts to Avoid

| Chart | Problem | Better alternative |
|---|---|---|
| **Pie chart** | Angle perception is poor; cannot compare non-adjacent slices | Bar chart or dot plot |
| **3D bar chart** | Perspective distorts lengths; occlusion hides data | 2D bar chart |
| **Dual-axis chart** | Arbitrary scaling creates false correlations | Two separate panels with aligned x-axes |
| **Radar/spider chart** | Area is meaningless; axis order affects shape | Parallel coordinates or small multiples of bar charts |
| **Stacked 100% area (many categories)** | Inner series are impossible to read | Small multiples of line charts |

Pie charts are acceptable only when: (a) showing parts of a whole, (b) with 2-3 slices, (c) where the takeaway is "roughly half" or "roughly a quarter." For anything more precise, use a bar chart.

## Color

### Color Palette Types

| Type | Use | Example |
|---|---|---|
| **Sequential** | Ordered data (low to high) | Light yellow to dark blue for temperature |
| **Diverging** | Data with a meaningful midpoint | Red-white-blue for above/below average |
| **Qualitative** | Categorical data (no order) | Distinct hues for product lines |

### Color Rules

1. **Never use rainbow.** Rainbow colormaps (jet) have perceptual non-uniformity: yellow and cyan appear brighter, creating false features. Use perceptually uniform palettes (viridis, cividis, inferno).
2. **Design for color blindness.** ~8% of males have color vision deficiency. Avoid red-green as the only distinguisher. Use blue-orange or include shape/pattern redundancy.
3. **Limit hue count.** Maximum 6-8 qualitative colors. Beyond that, use small multiples or interactive filtering.
4. **Gray for context.** When highlighting a subset, gray out everything else. The eye is drawn to color against gray.
5. **Consistent color mapping.** If "revenue" is blue in one chart, it must be blue in every chart in the same dashboard or report.

### Accessibility

- Test with a color-blindness simulator (Coblis, Sim Daltonism).
- Provide text labels or patterns in addition to color.
- Ensure sufficient contrast (WCAG 2.1 AA: 4.5:1 for text, 3:1 for large text and UI components).
- Use descriptive alt text for all charts in web/document contexts.

## Grammar of Graphics

Leland Wilkinson's Grammar of Graphics (1999), implemented in Hadley Wickham's ggplot2 (2005), decomposes every visualization into layered components:

| Component | What it specifies | Example |
|---|---|---|
| **Data** | The dataset | A table of countries, years, and GDP |
| **Aesthetics (aes)** | Mappings from variables to visual channels | x = year, y = GDP, color = continent |
| **Geometry (geom)** | The visual mark type | Points (scatter), lines, bars, areas |
| **Statistics (stat)** | Transformations computed on the data | Mean, count, regression line, density |
| **Scales** | How data values map to aesthetic values | Linear, log, discrete color palette |
| **Coordinates** | The coordinate system | Cartesian, polar, geographic projection |
| **Facets** | Subdivision into small multiples | One panel per continent |
| **Theme** | Non-data visual styling | Font size, background color, grid visibility |

This grammar is powerful because it is composable: any data can be mapped to any aesthetic, rendered with any geometry, in any coordinate system, faceted by any variable. Understanding the grammar means you can construct any chart type from first principles rather than memorizing a chart catalog.

## Interactive Visualization

### When to Make It Interactive

- **Exploration:** The analyst needs to zoom, filter, hover, and drill down. Interactive tools (Plotly, Bokeh, D3, Observable) are essential.
- **Dashboards:** Stakeholders need to slice data by different dimensions. Filtering and linked views are valuable.
- **Presentation:** Usually, static is better. Animation and interaction distract from the narrative. The author should curate the view.

### Interaction Techniques

| Technique | Purpose | Example |
|---|---|---|
| **Tooltip (hover)** | Show details for a data point | Hover over a dot to see country name and exact GDP |
| **Zoom + pan** | Navigate dense displays | Map exploration |
| **Filter** | Show a subset | Dropdown to select a specific year or category |
| **Brush + link** | Select in one view, highlight in another | Brush a scatterplot, see corresponding rows highlighted in a table |
| **Drill down** | Navigate hierarchical data | Click a country to see regional breakdown |

### Dashboard Design

1. **One question per dashboard.** A dashboard that tries to answer everything answers nothing.
2. **Key metric at top left.** The most important number gets prime visual real estate.
3. **Consistent time axis.** All time series on a dashboard should share the same x-axis range.
4. **Limit to 5-7 visual elements.** Cognitive load research (Miller, 1956) suggests 7 +/- 2 chunks of information is the working memory limit.
5. **Provide context.** Comparison baselines, targets, historical averages. A number without context is meaningless.

## Annotation and Storytelling

### The Annotation Layer

The most effective data visualizations are annotated. Annotations connect the visual to the narrative:

- **Title:** States the finding, not the chart type. "Renewable energy overtook coal in 2019" beats "Energy Sources Over Time."
- **Subtitle:** Adds context or methodology note.
- **Axis labels:** Always labeled with units. Never rely on the reader to guess.
- **Direct labels:** Label data points directly instead of using a legend when feasible. Reduces eye travel.
- **Callouts:** Arrow + text pointing to the specific feature you want the reader to notice.
- **Source and footnotes:** Always cite the data source. Note any exclusions or transformations.

### The Data Story Arc

A data story follows a narrative structure:

1. **Context:** What is the situation? What should the reader know before seeing the data?
2. **Finding:** What does the data show? This is the chart, annotated to highlight the key pattern.
3. **Implication:** What does this mean? Why should the reader care?
4. **Recommendation:** What action follows? (Optional, depends on audience.)

This arc is Alberto Cairo's "The Truthful Art" framework applied to presentation.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Truncated y-axis on bar chart | Exaggerates differences; lie factor > 1 | Start bar charts at zero |
| Using area to represent linear quantities | Humans underestimate area differences | Use length (bar chart) instead |
| Rainbow colormap | Perceptual non-uniformity creates false features | Use viridis, cividis, or sequential palettes |
| Too many colors | Indistinguishable hues; cognitive overload | Maximum 6-8 hues; use small multiples |
| Missing axis labels | Reader cannot interpret the chart | Always label axes with units |
| Chart without title | Reader must figure out what they are looking at | State the finding in the title |
| 3D effects on 2D data | Perspective distortion, occlusion | Use flat 2D charts |
| Ignoring color blindness | ~8% of male viewers cannot distinguish red-green | Test with color-blindness simulator; use blue-orange |

## Cross-References

- **tufte agent:** Design critique and the principles of honest data display. Primary agent for visualization quality review.
- **nightingale agent:** Department chair who routes visualization requests and synthesizes visual outputs.
- **cairo agent:** Data literacy pedagogy -- teaching others to read and create effective visualizations.
- **benjamin agent:** Ethical review of visualizations for bias, misleading framing, and equity implications.
- **data-wrangling skill:** Data preparation that determines what variables are available for visualization.
- **ethics-governance skill:** Responsible visualization practices -- not using charts to mislead.

## References

- Tufte, E. R. (2001). *The Visual Display of Quantitative Information*. 2nd edition. Graphics Press.
- Tufte, E. R. (1990). *Envisioning Information*. Graphics Press.
- Bertin, J. (1967/2010). *Semiology of Graphics*. ESRI Press (English translation).
- Wilkinson, L. (2005). *The Grammar of Graphics*. 2nd edition. Springer.
- Cairo, A. (2016). *The Truthful Art*. New Riders.
- Cairo, A. (2019). *How Charts Lie*. W. W. Norton.
- Wickham, H. (2010). "A Layered Grammar of Graphics." *Journal of Computational and Graphical Statistics*, 19(1), 3-28.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
