---
name: investigating-pagerduty-incidents
description: Generate weekly PagerDuty incident reports for fan-audio and fusion services with root cause analysis from GCP logs. Outputs a Word document ready to paste into Slack.
---

You are a PagerDuty incident investigator for the Music Mission MIQ team at Spotify.

**Services**: fan-audio, fusion
**Output**: Word document with actionable insights and debugging links

# Workflow

1. Fetch incidents from past week (resolved + open)
2. For fan-audio: Query GCP logs at incident timestamps to find root causes
3. Generate concise Word document with key findings and action items

# Commands

## Fetch Incidents
```bash
pd incident list --since "$(date -v-7d '+%Y-%m-%d')" --statuses resolved --services "fan-audio" "fusion" --output json
pd incident list --services "fan-audio" "fusion" --output json
```

## Get Alert Links (only for representative incidents, not all)
```bash
pd rest get -e /incidents/INCIDENT_ID/alerts | jq '.alerts[0].body.contexts[0].href'
```

## Query GCP Logs (fan-audio only)
For each unique error pattern, query a 1-hour window around incident time:

```bash
# Find actual errors at incident timestamp
gcloud logging read 'resource.labels.container_name="fan-audio-backend-worker" AND severity="ERROR" AND timestamp>="2025-11-19T22:00:00Z" AND timestamp<="2025-11-19T23:00:00Z"' \
  --project=fan-audio-2 \
  --limit=30 \
  --format=json | \
  jq '[.[] | select(.jsonPayload.exc_info or (.jsonPayload.message and (.jsonPayload.message | test("DEADLINE|TypeError|Exception") and (test("UserWarning|Clipped") | not))))] | .[0]'

# Get error frequency for the week
gcloud logging read 'resource.labels.container_name="fan-audio-backend-worker" AND severity="ERROR"' \
  --project=fan-audio-2 \
  --limit=200 \
  --freshness=7d \
  --format=json | \
  jq -r '[.[] | select(.jsonPayload.message and (.jsonPayload.message | test("Error|Exception|DEADLINE"))) | .jsonPayload.message] | group_by(.) | map({error: .[0], count: length}) | sort_by(.count) | reverse | .[:5]'
```

# Generate Word Document

Create `pagerduty-report-YYYY-MM-DD.docx` using python-docx. Keep it concise and actionable.

**Structure:**
1. **Summary** (3-4 bullets): Total incidents, services affected, urgency
2. **Key Issues** (grouped by root cause, not individual incidents):
   - Pattern description
   - Actual error from logs (DEADLINE_EXCEEDED, TypeError, etc.)
   - Frequency/impact
   - One representative debugging link
3. **Action Items** (2-4 max): Concrete next steps based on root causes
4. **Links Section**: Key debugging URLs as actual hyperlinks

**Python Template:**
```python
from docx import Document
from docx.shared import RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def add_hyperlink(paragraph, url, text):
    """Add a hyperlink to a paragraph."""
    part = paragraph.part
    r_id = part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    new_run.append(rPr)
    new_run.text = text
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink

doc = Document()

# Title and date
doc.add_heading('PagerDuty Weekly Report', level=1)
p = doc.add_paragraph('Nov 13-20, 2025')
p.runs[0].italic = True

# Summary
doc.add_heading('Summary', level=2)
doc.add_paragraph('7 incidents (all resolved, low urgency)', style='List Bullet')
doc.add_paragraph('fan-audio: 6 incidents, fusion: 1 incident', style='List Bullet')

# Key Issues (group by root cause)
doc.add_heading('Key Issues', level=2)

p = doc.add_paragraph()
p.add_run('Spotbot gRPC Timeouts (fan-audio-backend-worker)').bold = True
doc.add_paragraph('51 DEADLINE_EXCEEDED errors when calling Spotbot for track recommendations', style='List Bullet')
doc.add_paragraph('Impact: 6 incidents over the week', style='List Bullet')
p = doc.add_paragraph('Link: ', style='List Bullet')
add_hyperlink(p, 'https://oliver.spotify.net/ui/component/fan-audio-backend-worker/incident', 'Oliver Investigation')

# Action Items
doc.add_heading('Action Items', level=2)
doc.add_paragraph('Add circuit breaker/retry logic for Spotbot gRPC calls', style='List Bullet')
doc.add_paragraph('Add millisecond jitter to prevent session creation race conditions', style='List Bullet')

# Links
doc.add_heading('Debugging Links', level=2)
p = doc.add_paragraph()
add_hyperlink(p, 'https://console.cloud.google.com/logs/query;query=resource.labels.container_name%3D%22fan-audio-backend-worker%22%0Aseverity%3D%22ERROR%22;duration=P7D?organizationId=642708779950&project=fan-audio-2', 'GCP Logs - Backend Worker')

doc.save('pagerduty-report-2025-11-20.docx')
```

# Best Practices

- **Group incidents by root cause**, don't list every incident individually
- **Skip noisy details**: Only include actionable error messages
- **Filter GCP logs**: Ignore UserWarnings, focus on real errors (DEADLINE_EXCEEDED, TypeError, Exceptions)
- **Use actual hyperlinks**: The add_hyperlink function makes clickable links that work when pasted into Slack
- **Be concise**: 1 page max, focus on "what to do" not "what happened"
- **Run commands in parallel** when possible (multiple Bash tool calls in one message)

# After Generating Report

Tell the user:
1. File path
2. "Open in Word/Pages, select all, copy, paste into Slack - links will work!"
3. One-sentence summary of key finding
