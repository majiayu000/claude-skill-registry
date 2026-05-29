---
name: report-generation
description: Generate HTML reports, charts, and dashboards with neo-brutal design. Use for creating GitHub activity reports, Fieldy summaries, Skillz analytics, and other data visualizations.
---

# Report Generation

Generate professional HTML reports with charts, tables, and dashboards using neo-brutal design aesthetic.

## Quick Start

Generate a report:
```bash
python scripts/generate_html_report.py data.json --template daily-summary --output report.html
```

Create charts:
```bash
python scripts/create_charts.py metrics.json --type bar --output chart.png
```

## Design Principles

### Neo-Brutal Aesthetic

All reports follow these design rules:

1. **Bold Typography**
   - Strong, thick fonts (Arial Black, system sans-serif)
   - Clear hierarchy with size contrast

2. **High Contrast**
   - Black text on white backgrounds
   - Bold borders (3-4px solid black)
   - No gradients or shadows (except hard box-shadow)

3. **Geometric Layouts**
   - Grid-based layouts
   - Sharp corners, no border-radius
   - Consistent spacing

4. **Flat Colors**
   - Solid colors only
   - Color palette:
     - Primary: #000 (black)
     - Background: #fff (white)
     - Accent: #f5f5f5 (light gray)
     - Success: #4ade80 (green)
     - Warning: #fbbf24 (yellow)
     - Error: #f87171 (red)
     - Info: #60a5fa (blue)

## Report Templates

### 1. Daily Summary

**Use for:** GitHub activity, Fieldy coaching, general daily reports

**Sections:**
- Header with title and date
- Summary statistics (grid of metric cards)
- Timeline of events
- Top items (tables)
- Footer with timestamp

**Example:**
```bash
python scripts/generate_html_report.py daily_data.json \
    --template daily-summary \
    --title "GitHub Daily Activity" \
    --output report.html
```

### 2. Analytics Dashboard

**Use for:** Multi-metric dashboards, KPI tracking

**Sections:**
- KPI cards grid
- Charts (bar, line, pie)
- Comparison tables
- Trends over time

**Example:**
```bash
python scripts/generate_html_report.py analytics.json \
    --template dashboard \
    --period week \
    --output dashboard.html
```

### 3. Comparison Report

**Use for:** Before/after, A/B testing, performance comparisons

**Sections:**
- Side-by-side comparison tables
- Delta calculations
- Visual indicators (↑↓)
- Summary of changes

**Example:**
```bash
python scripts/generate_html_report.py comparison.json \
    --template comparison \
    --output comparison.html
```

### 4. Leaderboard

**Use for:** Contributor rankings, performance rankings

**Sections:**
- Ranked table with badges
- Top 3 highlight
- Detailed metrics per entry
- Trends

**Example:**
```bash
python scripts/generate_html_report.py leaderboard.json \
    --template leaderboard \
    --output leaderboard.html
```

### 5. Timeline Report

**Use for:** Event sequences, activity logs, chronological data

**Sections:**
- Chronological event list
- Time markers
- Event categories
- Activity heatmap

**Example:**
```bash
python scripts/generate_html_report.py events.json \
    --template timeline \
    --output timeline.html
```

## Data Input Format

### Generic Report Data

```json
{
  "title": "Report Title",
  "subtitle": "Report subtitle or date",
  "summary": {
    "metrics": [
      {
        "label": "Total Items",
        "value": "42",
        "change": "+5",
        "trend": "up"
      }
    ]
  },
  "sections": [
    {
      "title": "Section Title",
      "type": "table|list|chart|text",
      "data": {}
    }
  ],
  "footer": "Custom footer text"
}
```

### Chart Data

```json
{
  "title": "Chart Title",
  "type": "bar|line|pie|area",
  "data": {
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [
      {
        "label": "Series 1",
        "values": [10, 20, 15],
        "color": "#4ade80"
      }
    ]
  }
}
```

## HTML Components

### Metric Card

```html
<div class="metric-card">
    <div class="metric-value">42</div>
    <div class="metric-label">Total Commits</div>
    <div class="metric-change positive">+5 ↑</div>
</div>
```

### Table with Styling

```html
<table class="data-table">
    <thead>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </tbody>
</table>
```

### Status Badge

```html
<span class="badge badge-success">Active</span>
<span class="badge badge-warning">Pending</span>
<span class="badge badge-error">Failed</span>
```

### Section with Border

```html
<div class="section">
    <div class="section-title">Section Title</div>
    <div class="section-content">
        <!-- Content here -->
    </div>
</div>
```

## Charting

### Chart Types

1. **Bar Chart**
   - Compare discrete values
   - Horizontal or vertical bars
   - Good for rankings, comparisons

2. **Line Chart**
   - Show trends over time
   - Multiple series support
   - Good for time series data

3. **Pie Chart**
   - Show proportions
   - Good for composition breakdown
   - Limited to 8 segments max

4. **Area Chart**
   - Stacked values over time
   - Good for cumulative metrics
   - Shows magnitude and trend

### Chart Generation

Uses matplotlib with neo-brutal styling:

```python
import matplotlib.pyplot as plt

# Neo-brutal chart styling
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['axes.edgecolor'] = '#000'
plt.rcParams['axes.linewidth'] = 3
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.grid'] = False
```

**Example:**
```bash
python scripts/create_charts.py data.json \
    --type bar \
    --title "Commits per Day" \
    --output chart.png \
    --width 800 \
    --height 400
```

## Email Integration

Reports can be embedded in emails using the email-formatting skill:

```bash
# Generate report HTML
python scripts/generate_html_report.py data.json --template daily-summary --output report.html

# Embed in email (via email-formatting skill)
python ../email-formatting/scripts/format_email.py \
    --template email-report \
    --content report.html \
    --output email.html
```

## Scripts

### generate_html_report.py

Generate complete HTML reports from JSON data.

**Usage:**
```bash
python scripts/generate_html_report.py input.json \
    --template [daily-summary|dashboard|comparison|leaderboard|timeline] \
    --title "Report Title" \
    --subtitle "Optional subtitle" \
    --output report.html
```

**Options:**
- `--template`: Report template to use
- `--title`: Report title
- `--subtitle`: Optional subtitle
- `--period`: Time period (day/week/month)
- `--output`: Output HTML file

### create_charts.py

Generate chart images from data.

**Usage:**
```bash
python scripts/create_charts.py data.json \
    --type [bar|line|pie|area] \
    --title "Chart Title" \
    --output chart.png \
    --width 800 \
    --height 400
```

**Options:**
- `--type`: Chart type
- `--title`: Chart title
- `--width`: Image width (px)
- `--height`: Image height (px)
- `--style`: Color scheme (default/success/warning/error)

### aggregate_data.py

Aggregate and transform data for reporting.

**Usage:**
```bash
python scripts/aggregate_data.py input.json \
    --group-by date \
    --metrics count,sum,avg \
    --output aggregated.json
```

**Options:**
- `--group-by`: Field to group by
- `--metrics`: Metrics to calculate
- `--filter`: Filter expression
- `--sort`: Sort field

## Integration with Agents

### Reporting Agent Workflow

```python
# 1. Gather data from domain agents
github_data = task(agent="code-agent", prompt="Get yesterday's commits")
fieldy_data = task(agent="fieldy-agent", prompt="Get today's coaching data")

# 2. Aggregate data
python scripts/aggregate_data.py combined_data.json --group-by date

# 3. Generate report
python scripts/generate_html_report.py aggregated.json \
    --template daily-summary \
    --output report.html

# 4. Send via communication-agent
task(agent="communication-agent",
     prompt=f"Send report.html to dave@flycowgames.com")
```

### Code Agent (GitHub Reports)

```python
# Generate GitHub activity report
commits = github.get_commits(days=1)
python scripts/generate_html_report.py commits.json \
    --template daily-summary \
    --title "GitHub Daily Activity"
```

### Fieldy Agent (Coaching Reports)

```python
# Generate Fieldy coaching report
coaching_data = fieldy.get_today_data()
python scripts/generate_html_report.py coaching_data.json \
    --template daily-summary \
    --title "Fieldy Daily Summary"
```

## Common Report Patterns

### Daily Activity Report

1. Load yesterday's data
2. Aggregate by repository/project
3. Calculate key metrics
4. Generate timeline
5. Create HTML report
6. Email to recipients

### Weekly Summary

1. Load week's data
2. Calculate trends (compare to previous week)
3. Identify top performers
4. Generate charts
5. Create dashboard HTML
6. Email with executive summary

### Performance Comparison

1. Load two datasets (before/after)
2. Calculate deltas
3. Generate comparison tables
4. Add visual indicators
5. Create comparison report
6. Highlight key changes

## Styling Reference

See `templates/base.css` for complete CSS stylesheet.

Key classes:
- `.container` - Main container (max-width, border, shadow)
- `.header` - Report header (black background)
- `.section` - Content section
- `.metric-card` - KPI card
- `.data-table` - Styled table
- `.badge` - Status badge
- `.timeline` - Event timeline
- `.chart-container` - Chart wrapper

## Tips

1. **Keep it Simple**
   - Don't overcomplicate layouts
   - Stick to neo-brutal aesthetic
   - Focus on data clarity

2. **Consistent Spacing**
   - Use 20px/30px/40px spacing units
   - Maintain visual rhythm
   - Align elements to grid

3. **Readable Typography**
   - Minimum 14px for body text
   - Bold for emphasis
   - High contrast always

4. **Data Density**
   - Show top 10-20 items max
   - Summarize the rest
   - Use pagination for long lists

5. **Performance**
   - Inline critical CSS
   - Optimize images
   - Keep HTML size under 500KB
