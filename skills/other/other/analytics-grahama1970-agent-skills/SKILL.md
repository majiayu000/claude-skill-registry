---
name: analytics
description: >
  Flexible data science analytics for any dataset.
  Auto-discovers schema, recommends charts, exports to create-figure.
  Works with JSONL, JSON, CSV from any source.
allowed-tools: Bash, Read
triggers:
  - analyze data
  - analyze dataset
  - show insights
  - describe data
  - what's in this data
  - data exploration
  - EDA
  - schema discovery
  - chart recommendations
  - visualize this data
metadata:
  short-description: Schema discovery + chart recommendations for any data

provides:
  - analytics
composes:
  - create-figure
  - task-monitor
---

# Analytics Skill

Flexible data science analytics that works with **any dataset**. Auto-discovers schema, recommends visualizations, and exports in create-figure format.

## Quick Start (Any Dataset)

```bash
cd .pi/skills/analytics

# Step 1: Discover what's in the data
./run.sh describe data.jsonl

# Step 2: See recommendations and generate chart
./run.sh chart data.jsonl --name distribution_channel -o chart.json

# Step 3: Render with create-figure
cd .agent/skills/create-figure
./run.sh metrics -i /path/to/chart.json --type bar -o chart.pdf
```

## The Seamless Pipeline

```
Any Data (JSONL/JSON/CSV)
         │
         ▼
┌─────────────────────────────────┐
│     analytics describe          │  ← Discovers schema, recommends charts
│  "5 categorical, 2 numerical,   │
│   1 temporal column detected"   │
│  Recommendations:               │
│   - distribution_channel (bar)  │
│   - trend_by_date (line)        │
│   - heatmap_hour_x_day          │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     analytics chart/group-by    │  ← Generates chart data in create-figure format
│  --name distribution_channel    │
│  -o chart.json                  │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     create-figure metrics       │  ← Renders publication-quality PDF/PNG
│  -i chart.json --type bar       │
│  -o channel_distribution.pdf    │
└─────────────────────────────────┘
```

## Commands

### Discovery (Start Here)

| Command | Description |
|---------|-------------|
| `describe <file>` | Discover schema, detect column types, recommend charts |

```bash
./run.sh describe sales.jsonl
# Output:
# Columns: date (temporal), product (categorical), amount (numerical), region (categorical)
# Recommendations:
#   1. distribution_product - Distribution of product
#   2. distribution_region - Distribution of region
#   3. trend_by_date - Count over date
#   4. heatmap_product_x_region - product vs region
```

### Flexible Analysis

| Command | Description |
|---------|-------------|
| `group-by <file>` | Group by any column with aggregation |
| `stats <file>` | Numerical statistics and correlations |
| `chart <file>` | Generate chart spec for create-figure |

```bash
# Group by any column
./run.sh group-by data.jsonl --by channel --for-figure -o by_channel.json
./run.sh group-by data.jsonl --by category --agg price --func sum

# Numerical stats
./run.sh stats data.jsonl --columns revenue,cost,profit

# Generate chart from recommendation
./run.sh chart data.jsonl --name distribution_channel -o chart.json
```

### Timestamped Data (ingest-* outputs)

| Command | Description |
|---------|-------------|
| `insights <file>` | Full analysis summary (trends, sessions, patterns) |
| `trends <file>` | Viewing trends with rolling averages |
| `sessions <file>` | Session detection and binge analysis |
| `time-patterns <file>` | Hour/day distribution |
| `evolution <file>` | How preferences change over time |

### Output

| Command | Description |
|---------|-------------|
| `export <file>` | Batch export all standard charts |
| `report <file>` | Horus-style narrative report |

## Supported Formats

| Format | Extension | Auto-Detection |
|--------|-----------|----------------|
| JSONL | `.jsonl` | Line-delimited JSON |
| JSON | `.json` | Array or `{data: [...]}` |
| CSV | `.csv` | Comma-separated |

## Column Type Detection

The `describe` command auto-detects:

| Type | Detection Logic | Recommended Charts |
|------|-----------------|-------------------|
| **temporal** | datetime64, date-like strings | line, area, heatmap (time axis) |
| **numerical** | int64, float64 | histogram, scatter, stats |
| **categorical** | low cardinality (≤20 unique) | bar, pie, heatmap |
| **boolean** | bool dtype | pie (true/false) |
| **text** | high cardinality strings | word cloud, top-N |

## Chart Recommendations

Based on column types, analytics recommends:

| Data Pattern | Chart Type | create-figure Command |
|--------------|------------|----------------------|
| 1 categorical | bar, pie | `metrics --type bar` |
| 1 temporal | line | `training-curves` |
| 2 categorical | heatmap | `heatmap` |
| temporal + categorical | heatmap | `heatmap` |
| 2+ numerical | correlation matrix | `heatmap` |
| 1 numerical | histogram | `metrics --type bar` |

## Agent Workflow

For a project agent to analyze any dataset and visualize:

```python
# 1. Discover schema
result = run("./run.sh describe data.jsonl --json")
recommendations = result["recommendations"]

# 2. Pick first recommendation
chart_name = recommendations[0]["name"]
cmd = recommendations[0]["create_figure_cmd"]

# 3. Generate chart data
run(f"./run.sh chart data.jsonl --name {chart_name} -o chart.json")

# 4. Render
run(f"cd .agent/skills/create-figure && ./run.sh {cmd} -i chart.json -o chart.pdf")
```

## Examples

### E-commerce Sales Data

```bash
# Data: orders.jsonl with date, product, category, amount, region

./run.sh describe orders.jsonl
# → Recommends: distribution_category, distribution_region, trend_by_date

./run.sh group-by orders.jsonl --by category --agg amount --func sum --for-figure -o revenue_by_category.json
# → {"metrics": {"Electronics": 45000, "Clothing": 32000, ...}}

cd .agent/skills/create-figure
./run.sh metrics -i revenue_by_category.json --type bar -o revenue.pdf
```

### YouTube History (ingest-yt-history)

```bash
# Use specialized timestamped commands
./run.sh insights ~/.pi/ingest-yt-history/history.jsonl
./run.sh export ~/.pi/ingest-yt-history/history.jsonl -o ./charts --for-figure

cd .agent/skills/create-figure
./run.sh heatmap -i charts/heatmap.json -o viewing_heatmap.pdf
```

### API Response Data

```bash
# Data: api_logs.json with endpoint, status_code, response_time, user_id

./run.sh describe api_logs.json
./run.sh stats api_logs.json --columns response_time
# → mean=245.3ms, std=89.2ms, p50=220ms, p99=450ms

./run.sh group-by api_logs.json --by endpoint --agg response_time --func mean --for-figure -o latency.json
```

## Dependencies

```toml
# pyproject.toml
dependencies = [
    "pandas>=2.0.0",
    "typer>=0.9.0",
    "rich>=13.0.0",
]
```

## Integration with Horus

```bash
# Horus narrative style
./run.sh insights ~/.pi/ingest-yt-history/history.jsonl --horus

# Output:
# "Your viewing patterns reveal a nocturnal tendency toward melancholic content.
#  Peak activity occurs in the twilight hours, with music consumption intensifying
#  during introspective night sessions..."
```
