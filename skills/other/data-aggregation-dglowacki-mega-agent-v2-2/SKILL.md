---
name: data-aggregation
description: Aggregate and merge data from multiple sources including App Store sales, GitHub commits, Skillz events, and more. Use when combining data for reports, dashboards, or analysis.
---

# Data Aggregation

Tools for aggregating, transforming, and merging data from multiple sources.

## Quick Start

Aggregate App Store sales:
```bash
python scripts/aggregate_sales.py --input sales_reports/ --output aggregated.json
```

Aggregate GitHub commits:
```bash
python scripts/aggregate_commits.py --input commits.json --period week --output summary.json
```

Merge multiple sources:
```bash
python scripts/merge_sources.py --sources app_store.json github.json skillz.json --output combined.json
```

## Aggregation Types

### 1. Time-Based Aggregation

Group data by time periods (day, week, month).

**Example: Daily sales totals**
```python
from aggregate_sales import aggregate_by_time

# Input: List of sales records
sales = [
    {"date": "2026-01-14", "revenue": 123.45, "units": 5},
    {"date": "2026-01-14", "revenue": 67.89, "units": 3},
    {"date": "2026-01-15", "revenue": 234.56, "units": 8}
]

# Output: Aggregated by day
result = aggregate_by_time(sales, period='day')
# {
#     "2026-01-14": {"revenue": 191.34, "units": 8},
#     "2026-01-15": {"revenue": 234.56, "units": 8}
# }
```

### 2. Entity-Based Aggregation

Group data by entities (apps, users, repos, etc.).

**Example: Per-app metrics**
```python
from aggregate_sales import aggregate_by_entity

sales = [
    {"app": "App A", "revenue": 100, "units": 5},
    {"app": "App A", "revenue": 50, "units": 2},
    {"app": "App B", "revenue": 200, "units": 10}
]

result = aggregate_by_entity(sales, entity_field='app')
# {
#     "App A": {"revenue": 150, "units": 7},
#     "App B": {"revenue": 200, "units": 10}
# }
```

### 3. Statistical Aggregation

Calculate statistics (sum, avg, min, max, percentiles).

**Example: Commit statistics**
```python
from aggregate_commits import calculate_stats

commits = [
    {"author": "John", "lines": 125},
    {"author": "Jane", "lines": 87},
    {"author": "John", "lines": 43}
]

result = calculate_stats(commits, group_by='author', metric='lines')
# {
#     "John": {"sum": 168, "avg": 84, "min": 43, "max": 125, "count": 2},
#     "Jane": {"sum": 87, "avg": 87, "min": 87, "max": 87, "count": 1}
# }
```

## Data Sources

### App Store Sales

**Input format (TSV from App Store Connect):**
```
Provider	Provider Country	SKU	Developer	Title	Version	Product Type Identifier	Units	Developer Proceeds	Begin Date	End Date	Customer Currency	Country Code	Currency of Proceeds	Apple Identifier	Customer Price	Promo Code	Parent Identifier	Subscription	Period	Category	CMB	Device	Supported Platforms	Proceeds Reason	Preserved Pricing	Client
```

**Aggregated output:**
```json
{
  "period": "2026-01-14",
  "apps": {
    "com.example.app": {
      "name": "My App",
      "downloads": 1234,
      "revenue": 567.89,
      "updates": 45,
      "countries": ["US", "CA", "UK"]
    }
  },
  "totals": {
    "total_downloads": 5678,
    "total_revenue": 2345.67,
    "total_apps": 5
  }
}
```

### GitHub Commits

**Input format (from GitHub API):**
```json
[
  {
    "sha": "abc123",
    "author": {"name": "John Doe", "email": "john@example.com"},
    "commit": {
      "message": "Add feature X",
      "author": {"date": "2026-01-14T10:30:00Z"}
    },
    "stats": {"additions": 125, "deletions": 45}
  }
]
```

**Aggregated output:**
```json
{
  "period": "week",
  "date_range": "2026-01-07 to 2026-01-14",
  "summary": {
    "total_commits": 45,
    "total_contributors": 5,
    "total_lines": 2345,
    "total_files": 123
  },
  "by_author": {
    "John Doe": {
      "commits": 15,
      "lines_added": 1234,
      "lines_deleted": 456,
      "files_changed": 45
    }
  },
  "by_day": {
    "2026-01-14": {"commits": 8, "lines": 567}
  }
}
```

### Skillz Events

**Input format (from Skillz Developer Portal):**
```json
{
  "event_id": "888831",
  "name": "Winter Tournament",
  "status": "active",
  "start_date": "2026-01-10",
  "end_date": "2026-01-20",
  "prize_pool": 1000,
  "entries": 234
}
```

**Aggregated output:**
```json
{
  "period": "active",
  "summary": {
    "total_events": 8,
    "total_prize_pool": 8000,
    "total_entries": 1234
  },
  "by_status": {
    "active": {"count": 5, "prize_pool": 5000},
    "completed": {"count": 3, "prize_pool": 3000}
  }
}
```

## Aggregation Scripts

### aggregate_sales.py

Aggregate App Store sales data.

**Usage:**
```bash
python scripts/aggregate_sales.py \
    --input sales_reports/ \
    --period week \
    --group-by app \
    --output aggregated.json
```

**Arguments:**
- `--input`: Input directory or file (TSV/JSON)
- `--period`: Time period (day, week, month)
- `--group-by`: Grouping field (app, country, category)
- `--output`: Output JSON file

### aggregate_commits.py

Aggregate GitHub commit data.

**Usage:**
```bash
python scripts/aggregate_commits.py \
    --input commits.json \
    --period week \
    --metrics lines,files,commits \
    --output summary.json
```

**Arguments:**
- `--input`: Input JSON file (commits array)
- `--period`: Time period (day, week, month)
- `--metrics`: Metrics to calculate (comma-separated)
- `--output`: Output JSON file

### aggregate_events.py

Aggregate Skillz event data.

**Usage:**
```bash
python scripts/aggregate_events.py \
    --input events/ \
    --status active,completed \
    --output summary.json
```

**Arguments:**
- `--input`: Input directory with event JSON files
- `--status`: Filter by status (comma-separated)
- `--output`: Output JSON file

### merge_sources.py

Merge data from multiple sources.

**Usage:**
```bash
python scripts/merge_sources.py \
    --sources app_store.json github.json skillz.json \
    --strategy combine \
    --output combined.json
```

**Arguments:**
- `--sources`: Space-separated list of JSON files
- `--strategy`: Merge strategy (combine, average, latest)
- `--output`: Output JSON file

**Merge strategies:**
- `combine`: Combine all data (keep all fields)
- `average`: Average numeric fields
- `latest`: Keep latest values (by timestamp)

## Data Transformations

### Filtering

```python
from aggregate_sales import filter_data

sales = [...]

# Filter by country
us_sales = filter_data(sales, country='US')

# Filter by date range
recent_sales = filter_data(sales, start_date='2026-01-01', end_date='2026-01-14')

# Filter by value
high_revenue = filter_data(sales, min_revenue=100)
```

### Grouping

```python
from aggregate_commits import group_data

commits = [...]

# Group by author
by_author = group_data(commits, group_by='author')

# Group by repository
by_repo = group_data(commits, group_by='repository')

# Group by date
by_date = group_data(commits, group_by='date', period='day')
```

### Sorting

```python
from merge_sources import sort_data

data = [...]

# Sort by revenue (descending)
sorted_data = sort_data(data, field='revenue', reverse=True)

# Sort by date (ascending)
sorted_data = sort_data(data, field='date')
```

## Integration with Agents

### Reporting Agent

```python
# Aggregate App Store sales
from aggregate_sales import aggregate_sales

sales_data = appstore_client.get_sales_report(days=7)
aggregated = aggregate_sales(sales_data, period='day', group_by='app')

# Use for report
html = render_template('appstore-metrics', aggregated)
```

### Automation Agent

```python
# Aggregate GitHub commits
from aggregate_commits import aggregate_commits

commits = github_client.get_commits(repo='owner/repo', days=7)
summary = aggregate_commits(commits, period='week')

# Create ClickUp task if high activity
if summary['total_commits'] > 50:
    clickup_client.create_task(
        title='High GitHub Activity',
        description=f"Total commits: {summary['total_commits']}"
    )
```

## Examples

See `examples/` directory for:
- `sample_sales_aggregation.json` - App Store sales example
- `sample_commit_aggregation.json` - GitHub commits example
- `sample_multi_source_merge.json` - Multi-source merge example
