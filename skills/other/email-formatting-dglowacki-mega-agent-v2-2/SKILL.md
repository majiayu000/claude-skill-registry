---
name: email-formatting
description: Format emails with HTML templates using neo-brutal design aesthetic. Use when creating email reports, summaries, or formatted messages. Maintains consistent visual style across all communications.
---

# Email Formatting

Format emails with our signature neo-brutal design aesthetic.

## Quick Start

For plain text emails, use directly:
```python
# Plain text - no formatting needed
text = "Your message here"
```

For HTML emails, use templates:
```bash
python scripts/format_email.py --template daily-report --data data.json
```

## Neo-Brutal Design Principles

Our email design follows neo-brutal aesthetic:
- **Bold typography**: Strong, thick fonts
- **High contrast**: Black text on white, bright accent colors
- **Thick borders**: 3-4px solid black borders
- **Flat colors**: No gradients, solid blocks
- **Geometric shapes**: Rectangles, squares
- **Brutalist layout**: Grid-based, chunky sections

## Available Templates

### 1. Daily Report (`daily-report`)
For daily activity summaries (GitHub, Fieldy, etc.)

**Data structure:**
```json
{
  "title": "Daily GitHub Report",
  "date": "2026-01-04",
  "summary": "Brief overview",
  "sections": [
    {
      "title": "Commits",
      "content": "HTML content",
      "items": ["item 1", "item 2"]
    }
  ],
  "stats": {
    "total_commits": 5,
    "files_changed": 12
  }
}
```

### 2. Simple Message (`simple`)
For plain formatted messages

**Data structure:**
```json
{
  "title": "Message Title",
  "body": "Message body text",
  "footer": "Optional footer"
}
```

### 3. Data Table (`data-table`)
For tabular data display

**Data structure:**
```json
{
  "title": "Report Title",
  "headers": ["Column 1", "Column 2"],
  "rows": [
    ["Value 1", "Value 2"],
    ["Value 3", "Value 4"]
  ]
}
```

## Base HTML Template

All templates use this base structure:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: white;
            border: 4px solid black;
            padding: 0;
        }
        .header {
            background-color: black;
            color: white;
            padding: 20px;
            font-size: 24px;
            font-weight: 900;
            border-bottom: 4px solid black;
        }
        .section {
            padding: 20px;
            border-bottom: 3px solid black;
        }
        .section:last-child {
            border-bottom: none;
        }
        .section-title {
            font-size: 18px;
            font-weight: 800;
            margin-bottom: 10px;
            text-transform: uppercase;
        }
        .stat-box {
            display: inline-block;
            background-color: #ffeb3b;
            border: 3px solid black;
            padding: 10px 15px;
            margin: 5px;
            font-weight: 700;
        }
        .accent-green { background-color: #4caf50; color: white; }
        .accent-red { background-color: #f44336; color: white; }
        .accent-blue { background-color: #2196f3; color: white; }
        ul {
            list-style: none;
            padding: 0;
        }
        li {
            padding: 8px;
            margin: 5px 0;
            background-color: #f5f5f5;
            border-left: 4px solid black;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border: 2px solid black;
        }
        th {
            background-color: black;
            color: white;
            font-weight: 800;
        }
        .footer {
            padding: 15px 20px;
            background-color: #f5f5f5;
            border-top: 3px solid black;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <!-- Content here -->
</body>
</html>
```

## Color Palette

```
Primary:   #000000 (black)
Background: #FFFFFF (white)
Accent 1:  #FFEB3B (yellow)
Accent 2:  #4CAF50 (green)
Accent 3:  #F44336 (red)
Accent 4:  #2196F3 (blue)
Gray:      #F5F5F5 (light gray)
```

## Usage in Agents

### Communication Agent
```python
# Format and send HTML email
html = format_email_html(template='daily-report', data=report_data)
gmail.send_email(to=recipient, subject=subject, body_html=html)
```

### Reporting Agent
```python
# Generate report HTML
report_html = format_email_html(template='data-table', data=table_data)
# Delegate to communication-agent to send
```

## Scripts

See `scripts/format_email.py` for programmatic email formatting.
