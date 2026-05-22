---
name: reports
description: Report templating with Jinja2 and MJML for SignalRoom. Use when creating new reports, modifying templates, debugging report rendering, or adding new notification channels.
---

# Report Templating System

## Architecture

```
reports/
├── registry.py      # Report definitions (name, templates, query)
├── renderer.py      # Jinja2 + MJML rendering
├── runner.py        # Execute reports (query → render → send)
├── templates/       # .j2 (Slack/SMS) and .mjml (Email)
└── queries/         # SQL files for report data
```

## Creating a New Report

### 1. Add SQL Query

Create `src/signalroom/reports/queries/{report_name}.sql`:

```sql
-- Parameters available: :date, :start_date, :end_date
SELECT
    :date AS report_date,
    SUM(conversions) AS total_conversions,
    SUM(revenue) AS total_revenue
FROM everflow.daily_stats
WHERE date = :date
```

### 2. Create Templates

**Slack** (`templates/{report_name}.slack.j2`):
```jinja
*{{ title }}* — {{ report_date }}

:chart_with_upwards_trend: *Performance Summary*
• Conversions: {{ "{:,}".format(total_conversions) }}
• Revenue: ${{ "{:,.2f}".format(total_revenue) }}
```

**Email** (`templates/{report_name}.email.mjml`):
```mjml
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text>
          <h1>{{ title }}</h1>
          <p>Conversions: {{ total_conversions }}</p>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

**SMS** (`templates/{report_name}.sms.j2`):
```jinja
{{ title }}: {{ total_conversions }} conv, ${{ total_revenue }} rev
```

### 3. Register Report

Add to `src/signalroom/reports/registry.py`:

```python
REPORTS = {
    "my_report": Report(
        name="my_report",
        title="My Report Title",
        query_file="my_report.sql",
        templates={
            "slack": "my_report.slack.j2",
            "email": "my_report.email.mjml",
            "sms": "my_report.sms.j2",
        },
    ),
}
```

## Running Reports

### Local Testing (No Send)

```bash
python -c "
from signalroom.reports import run_report
print(run_report('daily_ccw', channel='slack'))
"
```

### With Custom Parameters

```bash
python -c "
from signalroom.reports import run_report
print(run_report('daily_ccw', params={'date': '2025-12-18'}))
"
```

### Send to Channel

```bash
python -c "
from signalroom.reports import run_report
run_report('daily_ccw', channel='slack', send=True)
"
```

### Via Temporal

```bash
python scripts/trigger_workflow.py --report daily_ccw -w
```

## Available Reports

| Report | Channels | Description |
|--------|----------|-------------|
| `daily_ccw` | slack, email, sms | Daily CCW performance summary |
| `test_sync` | slack | Simple Everflow + Redtrack totals |
| `alert` | slack, email, sms | Error/warning/info alerts |

## Channel-Specific Formatting

### Slack (mrkdwn)

```jinja
*bold* _italic_ ~strikethrough~
:emoji_name:
• bullet point
```code```
```

### Email (MJML)

MJML compiles to responsive HTML. Use components:
- `<mj-section>` — row container
- `<mj-column>` — column within section
- `<mj-text>` — text content
- `<mj-button>` — CTA button
- `<mj-image>` — images

### SMS

Keep under 160 characters. No formatting.

## Jinja2 Patterns

### Number Formatting

```jinja
{{ "{:,}".format(value) }}           # 1,234,567
{{ "{:.2f}".format(value) }}         # 1234.56
{{ "${:,.2f}".format(value) }}       # $1,234.56
{{ "{:.1%}".format(value) }}         # 12.3%
```

### Conditionals

```jinja
{% if value > 0 %}
:arrow_up: Up {{ value }}%
{% else %}
:arrow_down: Down {{ value|abs }}%
{% endif %}
```

### Loops

```jinja
{% for row in affiliates %}
• {{ row.name }}: {{ row.conversions }} conv
{% endfor %}
```

### Date Formatting

```jinja
{{ report_date.strftime('%B %d, %Y') }}  # December 19, 2025
{{ report_date.strftime('%m/%d') }}       # 12/19
```

## Alert Helper

For quick alerts without full reports:

```python
from signalroom.reports import render_alert

message = render_alert(
    title="Pipeline Failed",
    message="Everflow sync failed with timeout",
    level="error"  # error, warning, info
)
```

## Debugging

### Template Not Found

Check path in registry matches actual file in `templates/`

### SQL Error

Run query directly:
```bash
python -c "
from signalroom.reports.runner import execute_query
print(execute_query('daily_ccw', {'date': '2025-12-18'}))
"
```

### MJML Compile Error

Test MJML syntax: https://mjml.io/try-it-live

## Resources

- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [MJML Documentation](https://mjml.io/documentation/)
- [Slack mrkdwn](https://api.slack.com/reference/surfaces/formatting)
