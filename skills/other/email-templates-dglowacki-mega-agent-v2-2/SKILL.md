---
name: email-templates
description: Professional HTML email templates for reports, summaries, and notifications. Includes daily summaries, GitHub digests, App Store metrics, and calendar reminders. Use when creating formatted email communications.
---

# Email Templates

Professional HTML email templates for various reporting and notification needs.

## Quick Start

Render a template:
```bash
python scripts/render_template.py --template daily-summary --data data.json
```

Format email with template:
```bash
python scripts/format_email.py --template github-digest --output email.html
```

## Available Templates

### 1. Daily Summary (`daily-summary.html`)

Complete daily activity summary across all systems.

**Use for:**
- End-of-day reports
- Morning briefings
- Weekly summaries

**Data structure:**
```json
{
  "date": "2026-01-14",
  "sections": [
    {
      "title": "GitHub Activity",
      "icon": "💻",
      "items": [
        {"label": "Commits", "value": "12", "color": "green"},
        {"label": "PRs", "value": "3", "color": "blue"}
      ],
      "details": "Brief summary text"
    },
    {
      "title": "App Store",
      "icon": "📱",
      "items": [
        {"label": "Downloads", "value": "1,234", "color": "yellow"},
        {"label": "Revenue", "value": "$567", "color": "green"}
      ]
    }
  ],
  "summary": "Overall summary text"
}
```

### 2. GitHub Digest (`github-digest.html`)

GitHub activity report with commit details and leaderboard.

**Use for:**
- Daily GitHub summaries
- Weekly activity reports
- Team performance reviews

**Data structure:**
```json
{
  "period": "Last 7 Days",
  "date_range": "Jan 7-14, 2026",
  "stats": {
    "total_commits": 45,
    "total_prs": 8,
    "total_reviews": 12,
    "contributors": 5
  },
  "top_contributors": [
    {
      "name": "John Doe",
      "commits": 15,
      "lines_changed": 1234,
      "score": 45.2
    }
  ],
  "recent_commits": [
    {
      "sha": "abc123",
      "author": "John Doe",
      "message": "Add feature X",
      "date": "2026-01-14T10:30:00Z",
      "repo": "owner/repo"
    }
  ]
}
```

### 3. App Store Metrics (`appstore-metrics.html`)

App Store sales, downloads, and analytics summary.

**Use for:**
- Daily sales reports
- Weekly performance summaries
- Monthly analytics reviews

**Data structure:**
```json
{
  "date": "2026-01-14",
  "apps": [
    {
      "name": "My App",
      "icon_url": "https://...",
      "metrics": {
        "downloads": 1234,
        "revenue": 567.89,
        "updates": 45,
        "crashes": 2
      },
      "trending": "up"
    }
  ],
  "totals": {
    "total_downloads": 5678,
    "total_revenue": 2345.67,
    "avg_rating": 4.5
  }
}
```

### 4. Calendar Reminder (`calendar-reminder.html`)

Meeting and event notifications.

**Use for:**
- Meeting reminders
- Event notifications
- Schedule updates

**Data structure:**
```json
{
  "event": {
    "title": "Team Meeting",
    "start": "2026-01-14T14:00:00Z",
    "end": "2026-01-14T15:00:00Z",
    "location": "Conference Room A",
    "attendees": ["john@example.com", "jane@example.com"],
    "description": "Discuss Q1 planning"
  },
  "reminder_type": "1 hour before",
  "actions": [
    {"label": "Join Meeting", "url": "https://..."},
    {"label": "View Calendar", "url": "https://..."}
  ]
}
```

## Design System

All templates use a consistent neo-brutal design aesthetic:

### Colors
```
Primary:   #000000 (black)
Background: #FFFFFF (white)
Accent 1:  #FFEB3B (yellow)
Accent 2:  #4CAF50 (green)
Accent 3:  #F44336 (red)
Accent 4:  #2196F3 (blue)
Gray:      #F5F5F5 (light gray)
```

### Typography
- **Headings**: 900 weight, uppercase
- **Body**: 400 weight, 16px
- **Stats**: 700 weight, large numbers

### Components
- **Borders**: 3-4px solid black
- **Sections**: Clear separation with thick borders
- **Stats boxes**: Colored backgrounds with thick borders
- **Tables**: Bold headers, clear grid lines

## Template Structure

Each template follows this base structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Base styles */
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; border: 4px solid black; }
        .header { background-color: black; color: white; padding: 20px; }
        /* Template-specific styles */
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><!-- Title --></div>
        <!-- Content sections -->
    </div>
</body>
</html>
```

## Scripts

### render_template.py

Renders a template with data.

**Usage:**
```bash
python scripts/render_template.py \
    --template daily-summary \
    --data data.json \
    --output email.html
```

**Arguments:**
- `--template`: Template name (daily-summary, github-digest, etc.)
- `--data`: JSON file with template data
- `--output`: Output HTML file

### format_email.py

Formats and optionally sends an email.

**Usage:**
```bash
python scripts/format_email.py \
    --template github-digest \
    --data data.json \
    --subject "GitHub Weekly Digest" \
    --to user@example.com \
    --send
```

**Arguments:**
- `--template`: Template name
- `--data`: JSON file with data
- `--subject`: Email subject
- `--to`: Recipient email
- `--send`: Send email (optional, otherwise just outputs HTML)

## Integration with Agents

### Communication Agent

```python
from email_templates import render_template

# Render template
html = render_template('daily-summary', data)

# Send via Gmail
gmail.send_email(
    to='user@example.com',
    subject='Daily Summary - Jan 14',
    body_html=html
)
```

### Reporting Agent

```python
# Generate report data
report_data = {
    'date': '2026-01-14',
    'sections': [...]
}

# Render template
html = render_template('appstore-metrics', report_data)

# Delegate to communication-agent
orchestrator.delegate_to('communication-agent', {
    'action': 'send_email',
    'to': 'dave@example.com',
    'subject': 'App Store Daily Report',
    'html': html
})
```

## Examples

See `examples/` directory for sample data files and rendered outputs.
