---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Chart Designer
# ═══════════════════════════════════════════════════════════════════════════════

name: chart-designer
description: "Design effective data visualizations and charts. Generate chart configurations for ECharts, Chart.js, and other libraries. Create dashboards and reports."
version: "1.0.0"
author: claude-office-skills
license: MIT

category: visualization
tags:
  - chart
  - data-visualization
  - echarts
  - dashboard
  - analytics
department: Data/Analytics

models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

mcp:
  server: office-mcp
  tools:
    - create_chart
    - read_xlsx
    - create_xlsx

capabilities:
  - chart_selection
  - data_visualization
  - dashboard_design
  - configuration_generation
  - best_practices

languages:
  - en
  - zh

related_skills:
  - data-analysis
  - infographic
  - report-generator
---

# Chart Designer Skill

## Overview

I help you design effective data visualizations by recommending the right chart types, generating configurations for popular charting libraries, and applying data visualization best practices.

**What I can do:**
- Recommend appropriate chart types for your data
- Generate ECharts/Chart.js configurations
- Design dashboard layouts
- Apply visualization best practices
- Create Excel chart specifications
- Suggest color schemes and styling

**What I cannot do:**
- Render charts directly (use generated configs in tools)
- Create custom chart types from scratch
- Access your data directly

---

## How to Use Me

### Step 1: Describe Your Data

Tell me:
- What type of data you have
- What story you want to tell
- Your audience (technical, executive, public)
- Where it will be displayed (presentation, dashboard, report)

### Step 2: Get Recommendations

I'll suggest:
- Best chart type(s) for your data
- Configuration options
- Color schemes
- Layout considerations

### Step 3: Receive Chart Configs

I'll provide:
- ECharts JSON configuration
- Chart.js configuration
- Excel chart setup instructions
- CSS/styling recommendations

---

## Chart Selection Guide

### Comparison Charts
| Chart Type | Best For | Data Requirements |
|------------|----------|-------------------|
| Bar Chart | Comparing categories | Categories + values |
| Grouped Bar | Multiple series comparison | Categories + multiple series |
| Stacked Bar | Part-to-whole comparison | Categories + component values |

### Trend Charts
| Chart Type | Best For | Data Requirements |
|------------|----------|-------------------|
| Line Chart | Change over time | Time series data |
| Area Chart | Cumulative trends | Time series (stacked optional) |
| Sparkline | Compact trends | Simple time series |

### Distribution Charts
| Chart Type | Best For | Data Requirements |
|------------|----------|-------------------|
| Histogram | Value distribution | Numeric values |
| Box Plot | Distribution summary | Numeric values with quartiles |
| Scatter Plot | Correlation | Two numeric variables |

### Part-to-Whole Charts
| Chart Type | Best For | Data Requirements |
|------------|----------|-------------------|
| Pie Chart | Simple proportions (≤5 items) | Categories + percentages |
| Donut Chart | Proportions with total | Categories + percentages |
| Treemap | Hierarchical proportions | Hierarchical data + values |

### Specialized Charts
| Chart Type | Best For | Data Requirements |
|------------|----------|-------------------|
| Funnel | Process stages/conversion | Stages + values |
| Gauge | Single KPI vs target | Current value + target |
| Heatmap | Matrix comparisons | Row + Column + Value |
| Radar | Multi-dimensional comparison | Multiple metrics per item |
| Sankey | Flow/transitions | Source + Target + Value |

---

## Decision Tree

```
What do you want to show?
│
├─ Comparison
│   ├─ Among items → Bar Chart
│   ├─ Over time → Line Chart
│   └─ Multiple series → Grouped/Stacked Bar
│
├─ Composition
│   ├─ Static → Pie/Donut (≤5) or Treemap
│   ├─ Over time → Stacked Area
│   └─ Hierarchical → Treemap/Sunburst
│
├─ Distribution
│   ├─ Single variable → Histogram
│   ├─ Multiple datasets → Box Plot
│   └─ Two variables → Scatter Plot
│
├─ Relationship
│   ├─ Two variables → Scatter Plot
│   ├─ Three variables → Bubble Chart
│   └─ Correlation matrix → Heatmap
│
└─ Flow/Process
    ├─ Sequential stages → Funnel
    ├─ Transitions → Sankey
    └─ Single metric → Gauge
```

---

## Output Format

```markdown
# Chart Design: [Title]

**Data Type**: [Description]
**Purpose**: [What story to tell]
**Recommended Chart**: [Chart type]

---

## Chart Configuration

### ECharts

```javascript
const option = {
  title: {
    text: 'Chart Title',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['Series 1', 'Series 2'],
    bottom: 10
  },
  xAxis: {
    type: 'category',
    data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: 'Series 1',
      type: 'bar',
      data: [120, 200, 150, 80, 70, 110]
    },
    {
      name: 'Series 2',
      type: 'line',
      data: [100, 180, 160, 90, 80, 100]
    }
  ]
};
```

### Chart.js

```javascript
const config = {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [{
      label: 'Series 1',
      data: [120, 200, 150, 80, 70, 110],
      backgroundColor: 'rgba(54, 162, 235, 0.8)'
    }]
  },
  options: {
    responsive: true,
    plugins: {
      title: {
        display: true,
        text: 'Chart Title'
      }
    }
  }
};
```

---

## Styling Recommendations

### Color Palette
- Primary: `#5470c6`
- Secondary: `#91cc75`
- Accent: `#fac858`
- Neutral: `#73c0de`

### Typography
- Title: 16px, bold
- Labels: 12px, regular
- Axis: 11px, light

---

## Best Practices Applied

1. [Practice 1]
2. [Practice 2]
3. [Practice 3]

---

## Alternative Charts

If this doesn't work well, consider:
1. [Alternative 1] - when [condition]
2. [Alternative 2] - when [condition]
```

---

## ECharts Common Configurations

### Bar Chart
```javascript
{
  xAxis: { type: 'category', data: categories },
  yAxis: { type: 'value' },
  series: [{
    type: 'bar',
    data: values,
    itemStyle: { color: '#5470c6' }
  }]
}
```

### Line Chart
```javascript
{
  xAxis: { type: 'category', data: categories },
  yAxis: { type: 'value' },
  series: [{
    type: 'line',
    data: values,
    smooth: true,
    areaStyle: {} // for area chart
  }]
}
```

### Pie Chart
```javascript
{
  series: [{
    type: 'pie',
    radius: ['40%', '70%'], // donut
    data: [
      { value: 100, name: 'A' },
      { value: 200, name: 'B' }
    ]
  }]
}
```

### Scatter Plot
```javascript
{
  xAxis: { type: 'value' },
  yAxis: { type: 'value' },
  series: [{
    type: 'scatter',
    data: [[x1, y1], [x2, y2]],
    symbolSize: 10
  }]
}
```

---

## Color Palettes

### Professional
```
#5470c6, #91cc75, #fac858, #ee6666, #73c0de, #3ba272, #fc8452, #9a60b4
```

### Cool
```
#1f77b4, #aec7e8, #17becf, #9edae5, #6baed6, #c6dbef, #08519c, #3182bd
```

### Warm
```
#ff7f0e, #ffbb78, #d62728, #ff9896, #e377c2, #f7b6d2, #bcbd22, #dbdb8d
```

### Accessible (colorblind-friendly)
```
#0077BB, #33BBEE, #009988, #EE7733, #CC3311, #EE3377, #BBBBBB
```

---

## Best Practices

### Data Ink Ratio
- Remove unnecessary gridlines
- Minimize chart junk
- Let data be the focus

### Clarity
- Clear, descriptive titles
- Labeled axes with units
- Appropriate precision (not too many decimals)

### Comparison
- Start y-axis at zero for bar charts
- Use consistent scales for comparison
- Sort data logically

### Color
- Use color purposefully
- Consider colorblind users
- Don't use too many colors (≤7)

### Interaction
- Tooltips for details
- Zoom for dense data
- Drill-down for hierarchies

---

## Tips for Better Charts

1. **Know your audience** - technical vs. executive
2. **Start with the question** - what are you trying to answer?
3. **Choose the right chart** - don't force data into wrong formats
4. **Simplify** - less is more
5. **Label clearly** - assume viewers have no context
6. **Test with real users** - is the message clear?
7. **Consider accessibility** - colors, contrast, alt text

---

## Limitations

- Cannot render charts directly
- Configuration may need adjustment for specific tools
- Complex custom visualizations may require code
- Real-time data requires additional setup

---

*Built by the Claude Office Skills community. Contributions welcome!*
