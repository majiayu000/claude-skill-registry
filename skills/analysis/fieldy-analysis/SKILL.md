---
name: fieldy-analysis
description: Analyze Field Labs coaching transcription data, calculate session metrics, and generate daily summaries. Use for processing Fieldy voice transcriptions and creating coaching reports.
---

# Fieldy Analysis

Process and analyze Field Labs coaching transcription data to generate daily email summaries.

## Quick Start

Analyze today's Fieldy data:
```bash
python scripts/analyze_fieldy.py data/fieldy/fieldy_2026-01-04.json
```

Generate daily summary:
```bash
python scripts/generate_fieldy_summary.py data/fieldy/fieldy_2026-01-04.json --output summary.json
```

## Data Structure

### Input Format (fieldy_YYYY-MM-DD.json)

```json
{
  "date": "2026-01-04",
  "transcriptions": [
    {
      "timestamp": "2026-01-04T10:30:00.000000+00:00",
      "transcription": "Full text of the transcription...",
      "transcriptions": [
        {
          "text": "Individual sentence or phrase",
          "speaker": "Unknown",
          "start": 0.704,
          "end": 7.184,
          "duration": null
        }
      ],
      "metadata": {
        "ip_address": "192.168.1.1",
        "user_agent": "python-httpx/0.28.1",
        "received_at": "2026-01-04T10:30:00.000000"
      }
    }
  ]
}
```

## Metrics to Calculate

### Session Metrics

1. **Total Sessions**
   - Count of transcription entries for the day
   - Each entry = one coaching session/call

2. **Total Duration**
   - Calculate from start/end times of transcription segments
   - Sum of all segment durations

3. **Average Session Length**
   - Total duration / number of sessions
   - Measured in minutes

4. **Session Timeline**
   - Timestamps of each session
   - Distribution throughout the day

### Content Metrics

1. **Total Words**
   - Word count across all transcriptions
   - Indicates session depth/engagement

2. **Average Words per Session**
   - Total words / number of sessions

3. **Speakers**
   - Identify unique speakers (if available)
   - Track multi-speaker sessions

4. **Topics/Keywords**
   - Extract common topics from transcriptions
   - Identify coaching themes

## Analysis Scripts

### analyze_fieldy.py

Analyze Fieldy transcription data and calculate metrics.

**Usage:**
```bash
python scripts/analyze_fieldy.py input.json --output analysis.json
```

**Output:**
```json
{
  "date": "2026-01-04",
  "summary": {
    "total_sessions": 12,
    "total_duration_minutes": 145.3,
    "avg_session_minutes": 12.1,
    "total_words": 5234,
    "avg_words_per_session": 436,
    "first_session": "2026-01-04T08:15:00",
    "last_session": "2026-01-04T17:45:00"
  },
  "sessions": [
    {
      "timestamp": "2026-01-04T08:15:00",
      "duration_minutes": 8.5,
      "word_count": 342,
      "segment_count": 15
    }
  ]
}
```

### generate_fieldy_summary.py

Generate formatted summary for daily email report.

**Usage:**
```bash
python scripts/generate_fieldy_summary.py input.json \
    --output summary.json \
    --format report
```

**Output (report format):**
```json
{
  "title": "Fieldy Daily Summary",
  "subtitle": "Friday, January 4, 2026",
  "metrics": [
    {
      "label": "Total Sessions",
      "value": "12",
      "trend": "up",
      "change": "+2"
    },
    {
      "label": "Total Duration",
      "value": "145 min",
      "trend": "up",
      "change": "+15 min"
    },
    {
      "label": "Avg Session Length",
      "value": "12.1 min",
      "trend": "neutral"
    }
  ],
  "sections": [
    {
      "title": "Session Timeline",
      "type": "timeline",
      "data": {
        "events": [...]
      }
    }
  ]
}
```

### extract_insights.py

Extract key topics and insights from transcriptions using text analysis.

**Usage:**
```bash
python scripts/extract_insights.py input.json --top-keywords 10
```

**Features:**
- Keyword frequency analysis
- Topic clustering
- Sentiment indicators
- Common phrases

## Report Templates

### Daily Email Summary

Standard format for daily Fieldy email:

**Subject:** Fieldy Daily Summary - [Date]

**Content:**
- Total sessions count
- Total duration in minutes
- Average session length
- Session timeline (first/last session times)
- Notable keywords or topics (if available)

### Weekly Rollup

Aggregate metrics for the week:
- Sessions per day
- Trend analysis (increasing/decreasing)
- Busiest day
- Total weekly duration

## Integration with Agents

### Fieldy Agent Workflow

```python
# 1. Read today's Fieldy data
fieldy_file = f"data/fieldy/fieldy_{today}.json"

# 2. Analyze with fieldy-analysis skill
python scripts/analyze_fieldy.py {fieldy_file} --output analysis.json

# 3. Generate summary for report
python scripts/generate_fieldy_summary.py analysis.json --format report

# 4. Use report-generation skill to create HTML
python ../report-generation/scripts/generate_html_report.py \
    summary.json --template daily-summary --output fieldy_report.html

# 5. Delegate to communication-agent to send email
task(agent="communication-agent",
     prompt=f"Send fieldy_report.html to dave+mega@flycowgames.com")
```

### Reporting Agent Integration

For weekly reports combining Fieldy with other metrics:

```python
# Aggregate week's Fieldy data
fieldy_weekly = aggregate_fieldy_week(start_date, end_date)

# Combine with GitHub, Skillz, etc.
combined_report = {
    "fieldy": fieldy_weekly,
    "github": github_weekly,
    "skillz": skillz_weekly
}

# Generate comprehensive weekly report
python ../report-generation/scripts/generate_html_report.py \
    combined_report.json --template weekly-summary
```

## Data Quality

### Validation Checks

1. **Missing Data**
   - Check for empty transcriptions
   - Validate timestamp format
   - Ensure duration calculations are positive

2. **Outliers**
   - Flag sessions > 60 minutes (likely errors)
   - Flag sessions < 1 minute (incomplete)
   - Check for duplicate timestamps

3. **Completeness**
   - Verify all required fields present
   - Check transcriptions array not empty
   - Validate metadata structure

## Scheduling

The Fieldy Agent runs daily at:
- **Time:** 11:00 AM UTC (3:00 AM PT)
- **Trigger:** systemd timer (daily-fieldy-email.timer)
- **Recipients:** dave+mega@flycowgames.com

## Tips

1. **Duration Calculation**
   - Use segment start/end times when available
   - Fall back to word count estimation (150 words/min)
   - Handle missing duration gracefully

2. **Timezone Handling**
   - Fieldy timestamps are in UTC
   - Convert to PT for email display
   - Ensure date boundaries are correct

3. **Error Handling**
   - Handle missing files gracefully
   - Continue processing if one session fails
   - Log errors for debugging

4. **Performance**
   - Cache parsed data to avoid re-parsing
   - Process sessions in parallel if many
   - Limit keyword extraction to top N

## Example Daily Report

```
Fieldy Daily Summary
Friday, January 4, 2026

Summary:
✓ 12 total coaching sessions
✓ 145 minutes total duration
✓ 12.1 minutes average session length

Timeline:
• First session: 8:15 AM PT
• Last session: 5:45 PM PT
• Most active period: 2:00 PM - 4:00 PM

Top Keywords:
• technique (45 mentions)
• training (38 mentions)
• form (32 mentions)
• practice (28 mentions)
```

## Reference

- Fieldy data location: `data/fieldy/fieldy_YYYY-MM-DD.json`
- Archive location: `data/fieldy/archive/` (optional)
- Report recipients: See `config/email_accounts.json`
