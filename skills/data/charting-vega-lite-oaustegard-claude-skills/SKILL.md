---
name: charting-vega-lite
description: Create interactive data visualizations using Vega-Lite declarative JSON grammar. Supports 20+ chart types (bar, line, scatter, histogram, boxplot, grouped/stacked variations, etc.) via templates and programmatic builders. Use when users upload data for charting, request specific chart types, or mention visualizations. Produces portable JSON specs with inline data islands that work in Claude artifacts and can be adapted for production.
metadata:
  version: 0.1.0
---

## Overview

This skill creates interactive Vega-Lite visualizations from uploaded data. The workflow:
1. Analyze data structure and context
2. Select 5-10 meaningful chart types based on what the data represents
3. Build chart specifications programmatically
4. Generate React artifact with embedded visualizations

## Critical Technical Constraint: Inline Data Island

**Claude artifacts cannot use fetch() for computer:// URLs.**

All data must be embedded as an inline JavaScript constant:

```javascript
const DATA = [ /* embedded data array */ ];

// Later in chart specs:
spec.data = { values: DATA };
```

**DO NOT:**
- Use fetch() to load external files
- Reference external data URLs
- Create separate data files

This is the only pattern that works in Claude's artifact environment.

## Primary Workflow: Data Upload → Chart Explorer

Execute this sequence when user uploads data without specifying chart type:

### 1. Analyze Data Structure

```bash
python /mnt/skills/user/charting-vega-lite/scripts/analyze_data.py /mnt/user-data/uploads/<filename>
```

**Extract from output:** 
- `fields[]` (with types and statistics)
- `suggested_charts[]` (suggested chart types with encodings)
- `sample_data` (first 10 rows for understanding context)

**If script fails:** Use manual pandas analysis
```python
import pandas as pd
df = pd.read_csv('/mnt/user-data/uploads/<filename>')
# Classify: numeric→quantitative, datetime→temporal, <20 unique→nominal
```

### 2. Understand Data Context

**Read sample data and column names to infer what the data represents:**

- **Biomedical data?** → Biomarkers, patient outcomes, clinical relevance
- **Financial data?** → Trends, comparisons, performance metrics
- **Sensor data?** → Temporal patterns, anomalies, correlations
- **E-commerce?** → Sales trends, product comparisons, conversions

**Ask:** What questions would someone analyzing this data want answered?

Examples:
- Assay data: Which biomarkers strongest? Patterns across samples? Variability?
- Financial: What are trends? How volatile? Seasonal patterns?
- IoT: Temporal patterns? Anomalies? Sensor correlations?

### 3. Select Meaningful Charts (5-10 suggestions)

**Filter analyze_data.py suggestions based on context and readability:**

**Apply readability filters:**
- Pie chart with >7 categories → Skip (unreadable)
- Heatmap with >50 categories per axis → Aggregate first
- Multi-line with >10 series → Consider faceting

**Prioritize charts that answer domain questions:**
- Comparison needs → Bar, box plot, grouped bar
- Distribution analysis → Histogram, box plot
- Pattern recognition → Heatmap, scatter
- Temporal trends → Line, area
- Part-to-whole → Stacked bar (pie only if <7 categories)

**Don't suggest charts just because data types match - choose charts that reveal insights.**

### 4. Generate Chart Specs

**Build specs programmatically using analyze_data.py encodings:**

For each suggested chart type, construct spec using:
- Templates from `assets/templates/` for basic types (bar, line, scatter, pie, heatmap, area)
- Builder patterns from `references/spec-builder-patterns.md` for variations (histogram, boxplot, grouped-bar, etc.)
- Vega-Lite examples from `references/vega-lite-examples-inventory.md` for uncommon types

Structure each chart as:
```python
{"type": "Chart Name", "reason": "Why this chart", "spec": {/* vega-lite spec */}}
```

### 5. Create Artifact with Inline Data Island

Load data, read template, replace `__DATA__` and `__CHART_SPECS__` placeholders, write using bash heredoc.

### 6. Provide Link

```
[View chart explorer](computer:///mnt/user-data/outputs/ChartExplorer.jsx)

Created 7 contextually relevant charts for your data.
```

## Secondary Workflow: Specific Chart Request

When user specifies chart type (e.g., "make a bar chart"):

### 1. Analyze Data
```bash
python /mnt/skills/user/charting-vega-lite/scripts/analyze_data.py /mnt/user-data/uploads/<filename>
```

### 2. Validate Chart Fits Data

**Check requirements:**
- Bar: needs 1 nominal + 1 quantitative
- Line: needs 1 temporal + 1 quantitative
- Scatter: needs 2 quantitative
- Heatmap: needs 2 nominal + 1 quantitative
- Pie: needs 1 nominal + 1 quantitative + <7 categories

**If data doesn't fit:**
- Explain: "Bar chart needs categorical data, but all columns are numeric"
- Suggest 2-3 alternatives
- Use Primary Workflow to create explorer with alternatives

### 3. Generate Spec

Use templates or programmatic builders based on chart type complexity.

### 4. Create Artifact

Same pattern as Primary Workflow step 5, but with single chart.

## Error Prevention

**Common failures:**

1. **Using fetch() in artifacts**
   - Solution: Always use inline data island pattern
   - Never create external data files

2. **Chart doesn't render**
   - Verify scripts load: Vega → Vega-Lite → Vega-Embed
   - Check data is injected: `spec.data = {values: DATA}`
   - Confirm field names match data columns

3. **Generic/random chart suggestions**
   - Solution: Consider data context and meaning
   - Filter suggestions for relevance and readability
   - Prioritize charts that answer meaningful questions

## Resources

**Scripts:**
- `scripts/analyze_data.py` - analyze structure, suggest 8-12 chart types

**Components:**
- `assets/components/ChartExplorer.jsx` - multi-chart explorer template

**Templates:**
- `assets/templates/*.json` - 6 basic chart templates (bar, line, scatter, pie, heatmap, area)

**References - Progressive Disclosure:**

Read `spec-builder-patterns.md` when building charts programmatically (histogram, boxplot, grouped/stacked bars, multi-line, etc.)

Read `vega-lite-examples-inventory.md` when user requests uncommon chart type not in spec-builder-patterns

Read `chart-types.md` when validating specific chart requirements or user asks "what chart should I use for..."

Read `advanced-charts.md` for complete specs of specialized charts (sankey, waterfall, violin plots, complex layered compositions)

Read `contextual-chart-selection.md` for extended domain examples if unfamiliar with data domain (biomedical, financial, IoT, etc.)

Read `online-resources.md` to fetch Vega-Lite docs for advanced features (custom selections, transforms, conditional encoding)

## Complete Workflow Example

**User uploads assay data CSV (51 assays, 74 samples)**

```bash
# 1. Analyze
python /mnt/skills/user/charting-vega-lite/scripts/analyze_data.py /mnt/user-data/uploads/assay_data.csv

# 2. Understand context: Multi-analyte immunoassay
#    Questions: Which biomarkers strongest? Patterns across samples? Variability?

# 3. Build contextual charts (5-7 specs)
#    Bar: Mean signal by assay
#    Heatmap: Sample × Assay
#    Box plot: Signal distribution by assay
#    Histogram: Overall signal distribution
#    etc.

# 4. Load data and template
df = pd.read_csv('/mnt/user-data/uploads/assay_data.csv')
data = df.to_dict(orient='records')
template = open('/mnt/skills/user/charting-vega-lite/assets/components/ChartExplorer.jsx').read()

# 5. Replace placeholders and write
artifact = template.replace('__DATA__', json.dumps(data)).replace('__CHART_SPECS__', json.dumps(charts))
# Use bash heredoc to avoid XML conflicts in tool parameters

# 6. Provide link
```
[View chart explorer](computer:///mnt/user-data/outputs/ChartExplorer.jsx)

Created 7 charts for your assay data - bar charts show biomarker signals, heatmap reveals sample patterns, box plots display variability.

## Critical Rules

1. **ALWAYS use inline data island pattern** - No fetch(), no external files
2. **Consider data context** - Choose meaningful charts based on what data represents, not just data types
3. **Filter by readability** - Avoid charts with too many categories
4. **Use bash heredoc for file creation** - Prevents XML conflicts when creating artifacts
5. **Provide links, not content** - Output token efficiency
