---
name: aitask-stats
description: Calculate and display statistics of AI task completions (daily, global, per-label).
---

## Usage

Run the statistics script:

```bash
./.aitask-scripts/aitask_stats.sh [OPTIONS]
```

### Options

- `-d, --days N` - Show daily breakdown for last N days (default: 7)
- `-v, --verbose` - Show individual task IDs in daily breakdown
- `--csv [FILE]` - Export raw data to CSV (default: aitask_stats.csv)
- `-h, --help` - Show usage information

### Examples

Basic statistics (last 7 days):
```bash
./.aitask-scripts/aitask_stats.sh
```

Extended daily view (14 days):
```bash
./.aitask-scripts/aitask_stats.sh --days 14
```

Verbose output with task names:
```bash
./.aitask-scripts/aitask_stats.sh -v
```

Export to CSV for graphing in LibreOffice:
```bash
./.aitask-scripts/aitask_stats.sh --csv
```

## Statistics Provided

1. **Summary** - Total completions, 7-day and 30-day counts
2. **Daily Breakdown** - Completions per day with optional task IDs
3. **Day of Week Stats** - Current week counts + 30d/all-time averages per weekday
4. **Label Weekly Trends** - Per-label completions for last 4 weeks (W-3, W-2, W-1, This Week)
5. **Label Day-of-Week Breakdown** - Per-label averages by day of week
6. **Task Type Weekly Trends** - Parent/child and feature/bug trends for last 4 weeks
7. **Features/Bugs by Label Trends** - Combined label + issue type weekly trends

## Export Format

**CSV Export:** Raw task data with columns:
- date, day_of_week, week_offset, task_id, labels, issue_type, task_type

Open in LibreOffice Calc to create custom charts and pivot tables for trend analysis.

### Importing CSV in LibreOffice Calc

1. Open LibreOffice Calc
2. File -> Open -> Select the CSV file
3. In the import dialog:
   - Character set: UTF-8
   - Separator: Comma
   - Check "Quoted field as text"
4. Click OK

### Creating Charts

1. Select the data range
2. Insert -> Chart
3. Choose chart type (Line, Bar, or XY Scatter for trends)
4. Follow the wizard to customize

### Pivot Tables for Analysis

1. Select all data
2. Insert -> Pivot Table
3. Drag fields:
   - Row: `week_offset` or `day_of_week`
   - Column: `labels` or `issue_type`
   - Data: Count of `task_id`
4. Creates summary table for trends
