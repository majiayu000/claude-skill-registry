---
name: dst-visualization
description: Create interactive Chart.js visualizations for DST data analysis. Use when generating charts, creating visual reports, building dashboards, or displaying trends from database tables.
---

# DST Visualize Skill

## Purpose

Create professional, interactive Chart.js visualizations for Danmarks Statistik data. This skill provides templates, color palettes, and implementation patterns for transforming DST data into compelling visual insights.

## When to Use

- User asks to visualize DST data
- Creating interactive dashboards
- Generating trend analysis charts
- Building data reports with visual elements
- Comparing regional or temporal data
- Presenting statistical findings visually

## Key Features

- **Line Charts** - Temporal trends and time series
- **Bar Charts** - Comparisons and distributions
- **DST Professional Colors** - Brand-aligned color schemes
- **Responsive Design** - Mobile and desktop optimized
- **Interactive Elements** - Hover tooltips, legends, drill-down
- **Data Export** - Download charts as images

## Chart Types

### 1. Line Chart (Time Series)

**Best for**: Population trends, economic indicators, time-based metrics

**Template**:
```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .chart-container { position: relative; width: 90%; margin: 20px auto; }
        canvas { max-height: 400px; }
    </style>
</head>
<body>
    <h2>Population Trend Analysis</h2>
    <div class="chart-container">
        <canvas id="lineChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('lineChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['2019', '2020', '2021', '2022', '2023', '2024'],
                datasets: [
                    {
                        label: 'Denmark Total',
                        data: [5841503, 5856002, 5867410, 5882261, 5914284, 5945119],
                        borderColor: '#1A4D2E',
                        backgroundColor: 'rgba(26, 77, 46, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: '#1A4D2E',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    },
                    {
                        label: 'Capital Region',
                        data: [1856062, 1860403, 1863532, 1871312, 1895143, 1916284],
                        borderColor: '#D4A574',
                        backgroundColor: 'rgba(212, 165, 116, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        pointBackgroundColor: '#D4A574',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top',
                        labels: {
                            font: { size: 14, weight: 'bold' },
                            padding: 15,
                            usePointStyle: true
                        }
                    },
                    title: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: { size: 14, weight: 'bold' },
                        bodyFont: { size: 13 },
                        borderColor: '#1A4D2E',
                        borderWidth: 2,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' +
                                       context.parsed.y.toLocaleString('da-DK');
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        title: { display: true, text: 'Population' },
                        ticks: {
                            callback: function(value) {
                                return value.toLocaleString('da-DK');
                            },
                            font: { size: 12 }
                        },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { font: { size: 12 } }
                    }
                }
            }
        });
    </script>
</body>
</html>
```

### 2. Bar Chart (Comparisons)

**Best for**: Regional comparisons, category analysis, distribution data

**Template**:
```html
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .chart-container { position: relative; width: 90%; margin: 20px auto; }
        canvas { max-height: 400px; }
    </style>
</head>
<body>
    <h2>Regional Population Comparison (2024)</h2>
    <div class="chart-container">
        <canvas id="barChart"></canvas>
    </div>
    <script>
        const ctx = document.getElementById('barChart').getContext('2d');
        const chart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [
                    'Capital Region',
                    'Zealand',
                    'Funen',
                    'South Jutland',
                    'Central Jutland',
                    'North Jutland'
                ],
                datasets: [
                    {
                        label: 'Population 2024',
                        data: [1916284, 1310459, 598374, 419682, 1312119, 590782],
                        backgroundColor: [
                            '#1A4D2E',
                            '#2E7D54',
                            '#4A9B7F',
                            '#6EB9A0',
                            '#D4A574',
                            '#E8C9A0'
                        ],
                        borderColor: '#1A4D2E',
                        borderWidth: 2,
                        borderRadius: 4,
                        hoverBackgroundColor: '#1A4D2E',
                        hoverBorderColor: '#fff',
                        hoverBorderWidth: 3
                    }
                ]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        padding: 12,
                        titleFont: { size: 14, weight: 'bold' },
                        bodyFont: { size: 13 },
                        borderColor: '#1A4D2E',
                        borderWidth: 2,
                        callbacks: {
                            label: function(context) {
                                return 'Population: ' +
                                       context.parsed.x.toLocaleString('da-DK');
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return (value / 1000).toFixed(0) + 'K';
                            },
                            font: { size: 12 }
                        },
                        grid: { color: 'rgba(0, 0, 0, 0.05)' }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { font: { size: 12 } }
                    }
                }
            }
        });
    </script>
</body>
</html>
```

## DST Professional Color Palette

### Primary Colors
```javascript
// DST Brand Greens
const dstGreens = {
    darkGreen: '#1A4D2E',     // Primary - strong, corporate
    mediumGreen: '#2E7D54',   // Secondary
    lightGreen: '#4A9B7F',    // Tertiary
    paleGreen: '#6EB9A0'      // Light accent
};

// DST Brand Tans/Golds
const dstGolds = {
    gold: '#D4A574',          // Warm accent
    lightGold: '#E8C9A0',     // Light accent
    darkGold: '#C18A3E'       // Deep accent
};

// Neutral Support Colors
const neutrals = {
    darkGray: '#333333',
    mediumGray: '#666666',
    lightGray: '#CCCCCC',
    white: '#FFFFFF'
};

// Data Series Palette (6-color recommended)
const dataPalette = [
    '#1A4D2E',   // Dark Green (Primary)
    '#D4A574',   // Gold (Accent)
    '#2E7D54',   // Medium Green
    '#E8C9A0',   // Light Gold
    '#4A9B7F',   // Light Green
    '#C18A3E'    // Dark Gold
];
```

### Color Usage Guidelines

| Color | Use Case | Best For |
|-------|----------|----------|
| #1A4D2E | Primary data series, main metrics | Top-level trends, primary indicators |
| #2E7D54 | Secondary data series | Secondary metrics, comparisons |
| #4A9B7F | Tertiary data series | Supporting data |
| #6EB9A0 | Highlights, annotations | Important changes, annotations |
| #D4A574 | Accent, contrast | Alternative categories, variations |
| #E8C9A0 | Light accents, backgrounds | Supporting information, secondary data |

## Implementation Steps

### Step 1: Prepare Data
Extract data from DuckDB query results:
```python
import duckdb
import json

# Connect to DuckDB
conn = duckdb.connect('data/dst.db')

# Query data
result = conn.execute("""
    SELECT tid, område, indhold
    FROM dst_folk1a
    WHERE område IN ('000', '101', '147')
    ORDER BY tid, område
""").fetchall()

# Transform to chart.js format
labels = sorted(set(row[0] for row in result))
datasets = {}

for tid, område, value in result:
    if område not in datasets:
        datasets[område] = []
    datasets[område].append(value)

chart_data = {
    "labels": labels,
    "datasets": [
        {
            "label": region_name,
            "data": values,
            "borderColor": color
        }
        for (region_name, values, color) in prepare_datasets(datasets)
    ]
}

print(json.dumps(chart_data))
```

### Step 2: Create HTML File
Use the appropriate chart template (line or bar) and customize:
1. Replace data values with your query results
2. Update labels with time periods or categories
3. Adjust colors from the DST palette
4. Customize titles and legends

### Step 3: Customize Appearance
```javascript
// Modify chart options:
options: {
    responsive: true,           // Mobile-friendly
    maintainAspectRatio: true,  // Prevent distortion
    plugins: {
        legend: {
            position: 'top',    // Move legend
            labels: { font: { size: 14 } }
        },
        tooltip: {
            // Custom formatting for tooltips
            callbacks: {
                label: function(context) {
                    // Format numbers with Danish locale
                    return context.dataset.label + ': ' +
                           context.parsed.y.toLocaleString('da-DK');
                }
            }
        }
    }
}
```

### Step 4: Save and Share
```bash
# Save as HTML file
# Open in browser for interactive viewing
# Use browser dev tools to save as image/PDF
```

## Best Practices

### Data Selection
- **Limit series**: Use 3-6 data series maximum for clarity
- **Choose appropriate time span**: Show enough data for trends but not overwhelming
- **Remove duplicates**: Aggregate or filter to single values per label
- **Handle missing data**: Use null or interpolate carefully

### Visual Design
- **Color consistency**: Use DST palette exclusively
- **Contrast**: Ensure distinct colors between series
- **Size appropriately**: Make fonts readable (min 12px)
- **Responsive**: Test on mobile and tablet views
- **Legend clarity**: Always include descriptive labels

### Accessibility
- **Color alone**: Don't rely solely on color to distinguish (add patterns if needed)
- **Contrast ratios**: Meet WCAG AA standards (4.5:1 minimum)
- **Text alternatives**: Provide data table alongside chart
- **Keyboard navigation**: Use standard browser features

### Performance
- **Data limits**: Avoid extremely large datasets (1000+ points)
- **Compression**: Minify JavaScript before deployment
- **Caching**: Allow browser caching of chart.js library
- **Load time**: Aim for < 1 second render time

## Common Patterns

### Pattern 1: Regional Trend Comparison
```javascript
// Query multiple regions over time
labels: years,
datasets: [
    { label: 'Capital Region', data: capital_values, borderColor: '#1A4D2E' },
    { label: 'Jutland', data: jutland_values, borderColor: '#D4A574' },
    { label: 'Islands', data: islands_values, borderColor: '#2E7D54' }
]
```

### Pattern 2: Time Series with Baseline
```javascript
// Show trends with comparison to baseline/average
datasets: [
    { label: 'Actual Values', data: values, borderColor: '#1A4D2E' },
    { label: 'Average', data: averages, borderColor: '#CCCCCC',
      borderDash: [5, 5], tension: 0.1 }
]
```

### Pattern 3: Stacked Bar Chart
```javascript
options: {
    scales: {
        x: { stacked: true },
        y: { stacked: true }
    }
}
// Useful for composition analysis
```

### Pattern 4: Multi-Axis Chart
```javascript
// For comparing different metrics with different scales
datasets: [
    { yAxisID: 'y', label: 'Population', ... },
    { yAxisID: 'y1', label: 'Growth Rate %', ... }
],
scales: {
    y: { type: 'linear', position: 'left' },
    y1: { type: 'linear', position: 'right' }
}
```

## Examples

### Example 1: Population Growth by Region
```html
<!-- Using bar chart template above -->
<!-- Replace regions and 2024 data with your query -->
```

### Example 2: Time Series Dashboard
```html
<!-- Multiple line charts, one per region -->
<!-- Use responsive grid for layout -->
<div style="display: grid; grid-template-columns: 1fr 1fr;">
    <div class="chart-container"><canvas id="capital"></canvas></div>
    <div class="chart-container"><canvas id="jutland"></canvas></div>
</div>
```

### Example 3: Export Chart
```javascript
// Save chart as image
const image = document.getElementById('lineChart').toDataURL('image/png');
const link = document.createElement('a');
link.href = image;
link.download = 'population-chart.png';
link.click();
```

## Troubleshooting

### Chart Not Displaying
- **Check**: Browser console for JavaScript errors
- **Verify**: Chart.js CDN is accessible
- **Confirm**: Canvas element exists and has unique ID
- **Test**: With simple sample data first

### Colors Look Wrong
- **Verify**: Using exact hex values from DST palette
- **Check**: Background colors aren't obscuring the chart
- **Review**: Browser color profile settings
- **Export**: May render differently in different formats

### Data Not Showing
- **Validate**: Data array matches labels array length
- **Check**: No null or undefined values
- **Confirm**: Data types are numeric where expected
- **Test**: Browser console logs data structure

### Performance Issues
- **Reduce**: Number of data points or series
- **Enable**: Caching in server headers
- **Optimize**: Image exports separately
- **Consider**: Aggregating data before visualization

## Dependencies

- **Chart.js 4.x**: `https://cdn.jsdelivr.net/npm/chart.js` (CDN)
- **Browser**: Modern browser with Canvas support (all current browsers)
- **No other dependencies** required

## Resources

- Chart.js Documentation: https://www.chartjs.org/docs/latest/
- DST API Data: Fetch via dst-data skill or dst-query skill
- Color Palette Reference: Use exact hex codes provided above
- Interactive Examples: Available in Chart.js documentation

## Tips

### Before Creating Charts
- Query data with dst-query or dst-data skills
- Validate data completeness and accuracy
- Check for outliers or unexpected values
- Determine appropriate chart type based on data structure

### While Building
- Start with template, customize incrementally
- Test locally before sharing
- Verify colors match DST brand
- Add meaningful titles and legends
- Include data source attribution

### After Completion
- Test responsiveness (resize browser)
- Check accessibility (no color-only indicators)
- Verify tooltips provide useful information
- Save/export in multiple formats if needed
- Document any custom modifications
