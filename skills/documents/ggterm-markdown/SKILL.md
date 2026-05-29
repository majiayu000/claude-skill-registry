---
name: ggterm-markdown
description: Generate markdown reports with embedded ggterm visualizations. Use when creating analysis reports, documenting results, exporting findings, or when the user wants plots in markdown format for sharing or documentation.
allowed-tools: Write, Read, Bash(bun:*), Bash(npx:*)
---

# Markdown Reports with ggterm

Generate analysis reports with embedded terminal visualizations and reproducible plot specifications.

## Report Structure

A well-structured analysis report includes:

1. **Title and Overview** - What was analyzed and why
2. **Data Summary** - Shape, columns, key statistics
3. **Visualizations** - Embedded plots with interpretations
4. **Findings** - Key insights from the analysis
5. **Appendix** - Plot specifications for reproducibility

## Basic Report Template

```typescript
import { gg, geom_point, geom_line } from '@ggterm/core'
import { writeFileSync } from 'fs'

// Create plots
const scatterPlot = gg(data)
  .aes({ x: 'x', y: 'y', color: 'category' })
  .geom(geom_point())
  .labs({ title: 'Relationship Analysis' })

const trendPlot = gg(data)
  .aes({ x: 'time', y: 'value' })
  .geom(geom_line())
  .labs({ title: 'Trend Over Time' })

// Render plots to strings
const scatter = scatterPlot.render({ width: 72, height: 18 })
const trend = trendPlot.render({ width: 72, height: 18 })

// Build markdown report
const report = `# Analysis Report: ${datasetName}

## Overview

This report analyzes ${data.length} observations across ${Object.keys(data[0]).length} variables.

## Data Summary

| Metric | Value |
|--------|-------|
| Rows | ${data.length} |
| Columns | ${Object.keys(data[0]).length} |
| Date Range | ${minDate} to ${maxDate} |

## Visualizations

### Scatter Plot

\`\`\`
${scatter}
\`\`\`

**Interpretation**: The scatter plot shows [describe the relationship observed].

### Trend Analysis

\`\`\`
${trend}
\`\`\`

**Interpretation**: The trend indicates [describe the pattern observed].

## Key Findings

1. **Finding 1**: Description of first key insight
2. **Finding 2**: Description of second key insight
3. **Finding 3**: Description of third key insight

## Appendix: Plot Specifications

<details>
<summary>Scatter Plot Spec (JSON)</summary>

\`\`\`json
${JSON.stringify(scatterPlot.spec(), null, 2)}
\`\`\`

</details>

<details>
<summary>Trend Plot Spec (JSON)</summary>

\`\`\`json
${JSON.stringify(trendPlot.spec(), null, 2)}
\`\`\`

</details>

---
*Generated with ggterm*
`

writeFileSync('analysis-report.md', report)
console.log('Report saved to analysis-report.md')
```

## Embedding Multiple Plots

For reports with many visualizations:

```typescript
interface PlotSection {
  title: string
  plot: GGPlot
  interpretation: string
}

function generateReport(
  title: string,
  overview: string,
  sections: PlotSection[],
  findings: string[]
): string {
  const plotSections = sections.map(({ title, plot, interpretation }) => `
### ${title}

\`\`\`
${plot.render({ width: 72, height: 16 })}
\`\`\`

**Interpretation**: ${interpretation}
`).join('\n')

  const findingsList = findings
    .map((f, i) => `${i + 1}. ${f}`)
    .join('\n')

  const specs = sections.map(({ title, plot }) => `
<details>
<summary>${title} Spec</summary>

\`\`\`json
${JSON.stringify(plot.spec(), null, 2)}
\`\`\`

</details>
`).join('\n')

  return `# ${title}

## Overview

${overview}

## Visualizations

${plotSections}

## Key Findings

${findingsList}

## Appendix: Reproducibility

${specs}

---
*Generated with ggterm*
`
}
```

## Width Guidelines

Choose plot width based on target context:

| Context | Width | Height | Notes |
|---------|-------|--------|-------|
| GitHub README | 72-80 | 16-20 | Standard terminal width |
| GitHub Issues | 72 | 14-18 | Compact for discussions |
| Documentation | 80-100 | 20-24 | More detail |
| Presentations | 60-70 | 12-16 | Readable at distance |

## Including Data Tables

```typescript
function markdownTable(data: Record<string, unknown>[], columns?: string[]): string {
  const cols = columns || Object.keys(data[0])
  const header = `| ${cols.join(' | ')} |`
  const separator = `| ${cols.map(() => '---').join(' | ')} |`
  const rows = data.map(row =>
    `| ${cols.map(c => String(row[c] ?? '')).join(' | ')} |`
  ).join('\n')

  return `${header}\n${separator}\n${rows}`
}

// Usage
const summaryTable = markdownTable([
  { metric: 'Mean', value: mean.toFixed(2) },
  { metric: 'Median', value: median.toFixed(2) },
  { metric: 'Std Dev', value: std.toFixed(2) },
])
```

## Full Example: EDA Report

```typescript
import { gg, geom_histogram, geom_boxplot, geom_point, facet_wrap } from '@ggterm/core'
import { writeFileSync } from 'fs'

// Assume data is loaded
const numericCols = ['age', 'income', 'score']
const categoricalCols = ['region', 'segment']

// Generate distribution plots
const distributions = numericCols.map(col => ({
  title: `Distribution of ${col}`,
  plot: gg(data).aes({ x: col }).geom(geom_histogram({ bins: 20 })),
  interpretation: `Shows the distribution of ${col} values.`
}))

// Generate comparison plots
const comparisons = categoricalCols.map(cat => ({
  title: `Score by ${cat}`,
  plot: gg(data).aes({ x: cat, y: 'score' }).geom(geom_boxplot()),
  interpretation: `Compares score across ${cat} groups.`
}))

// Correlation scatter
const correlation = {
  title: 'Age vs Income',
  plot: gg(data)
    .aes({ x: 'age', y: 'income', color: 'region' })
    .geom(geom_point({ alpha: 0.6 })),
  interpretation: 'Shows relationship between age and income by region.'
}

const report = generateReport(
  'Exploratory Data Analysis',
  `Analysis of ${data.length} customer records.`,
  [...distributions, ...comparisons, correlation],
  [
    'Income is right-skewed with median $X',
    'Region A shows significantly higher scores',
    'Age and income show moderate positive correlation'
  ]
)

writeFileSync('eda-report.md', report)
```

## Tips

1. **Keep plots compact** - Use 16-20 lines height for readability
2. **Include interpretations** - Don't just show plots, explain them
3. **Save specs** - Always include PlotSpec JSON for reproducibility
4. **Use collapsible sections** - `<details>` tags keep reports clean
5. **Match audience** - Adjust technical depth to readers

For report templates, see [templates/](templates/).
