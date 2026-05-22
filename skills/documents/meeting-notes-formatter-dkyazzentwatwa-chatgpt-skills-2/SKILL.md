---
name: meeting-notes-formatter
description: Convert raw meeting notes to structured markdown or PDF with automatic section detection, action items extraction, and attendee parsing.
---

# Meeting Notes Formatter

Transform raw, unstructured meeting notes into clean, professional documents. Automatically detects sections, extracts action items, parses attendees, and exports to Markdown or PDF.

## Quick Start

```python
from scripts.notes_formatter import MeetingNotesFormatter

# Format raw notes
raw_notes = """
Project sync Jan 15
Attendees: John, Sarah, Mike

Discussed Q1 roadmap
- Feature A is priority
- Feature B pushed to Q2
Sarah to send updated timeline by Friday
Mike will review budget

Next meeting Jan 22
"""

formatter = MeetingNotesFormatter(raw_notes)
formatter.format()
formatter.save("meeting_notes.md")

# Or save as PDF
formatter.save("meeting_notes.pdf")
```

## Features

- **Auto-Detection**: Identifies title, attendees, sections, action items
- **Action Item Extraction**: Pulls out tasks with owners and due dates
- **Attendee Parsing**: Extracts participant list from various formats
- **Section Organization**: Groups content into logical sections
- **Output Formats**: Markdown, PDF
- **Templates**: Structured output with consistent formatting

## API Reference

### Initialization

```python
# From string
formatter = MeetingNotesFormatter(raw_notes_string)

# From file
formatter = MeetingNotesFormatter.from_file("notes.txt")
```

### Formatting

```python
# Auto-format (detects structure)
formatter.format()

# With manual overrides
formatter.set_title("Weekly Standup")
formatter.set_date("2024-01-15")
formatter.set_attendees(["John Smith", "Sarah Jones"])
formatter.format()
```

### Manual Configuration

```python
# Set meeting metadata
formatter.set_title("Project Review Meeting")
formatter.set_date("January 15, 2024")
formatter.set_time("2:00 PM - 3:00 PM")
formatter.set_location("Conference Room A")

# Set attendees
formatter.set_attendees(["John Smith", "Sarah Jones", "Mike Wilson"])

# Add sections manually
formatter.add_section("Discussion", [
    "Reviewed Q1 roadmap",
    "Discussed resource allocation",
    "Agreed on priorities"
])

# Add action items
formatter.add_action_item("Send timeline update", owner="Sarah", due="Friday")
formatter.add_action_item("Review budget proposal", owner="Mike")
```

### Output

```python
# Get formatted markdown
markdown = formatter.to_markdown()

# Save to file
formatter.save("notes.md")      # Markdown
formatter.save("notes.pdf")     # PDF

# Get structured data
data = formatter.to_dict()
```

## Auto-Detection Features

### Title Detection
Identifies meeting title from:
- First line if short and descriptive
- Lines containing "meeting", "sync", "standup", "review"
- Date patterns at start of notes

### Attendee Detection
Extracts attendees from:
- "Attendees: John, Sarah, Mike"
- "Present: John Smith, Sarah Jones"
- "Participants: @john @sarah @mike"
- Lists following attendee keywords

### Action Item Detection
Identifies tasks from:
- "ACTION: Send report"
- "TODO: Review document"
- "[John] to send update"
- "Sarah will review by Friday"
- Lines with owner/assignee patterns

### Date Detection
Extracts dates from:
- "January 15, 2024"
- "2024-01-15"
- "01/15/2024"
- "Jan 15"

## Output Formats

### Markdown Output

```markdown
# Weekly Project Sync

**Date:** January 15, 2024
**Time:** 2:00 PM - 3:00 PM
**Attendees:** John Smith, Sarah Jones, Mike Wilson

---

## Discussion

- Reviewed Q1 roadmap progress
- Feature A is on track for release
- Feature B moved to Q2 due to resource constraints

## Decisions

- Prioritize performance improvements
- Delay new feature development until Q2

## Action Items

| Task | Owner | Due Date |
|------|-------|----------|
| Send updated timeline | Sarah | Jan 19 |
| Review budget proposal | Mike | Jan 22 |
| Schedule follow-up | John | Jan 16 |

---

**Next Meeting:** January 22, 2024
```

### PDF Output
Professional formatted PDF with:
- Clean typography
- Organized sections
- Action item table
- Header with meeting details

## CLI Usage

```bash
# Format notes file
python notes_formatter.py --input raw_notes.txt --output formatted.md

# Output as PDF
python notes_formatter.py --input notes.txt --output notes.pdf

# With manual metadata
python notes_formatter.py --input notes.txt \
    --title "Weekly Standup" \
    --date "Jan 15, 2024" \
    --output standup.md
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input text file | Required |
| `--output` | Output file path | `notes.md` |
| `--title` | Meeting title override | Auto-detect |
| `--date` | Meeting date override | Auto-detect |
| `--template` | Output template | `standard` |

## Examples

### Raw Notes Input

```text
Team standup 1/15

john sarah mike present

Updates:
- John: finished API integration
- Sarah: working on frontend
- Mike: reviewing PRs

Blockers:
Sarah blocked on design specs
need mike to review sarah's PR

action items:
john to deploy to staging today
sarah follow up with design team
mike review PR by EOD

next standup wednesday
```

### Formatted Output

```markdown
# Team Standup

**Date:** January 15, 2024
**Attendees:** John, Sarah, Mike

---

## Updates

- **John:** Finished API integration
- **Sarah:** Working on frontend
- **Mike:** Reviewing PRs

## Blockers

- Sarah blocked on design specs
- Need Mike to review Sarah's PR

## Action Items

| Task | Owner | Due |
|------|-------|-----|
| Deploy to staging | John | Today |
| Follow up with design team | Sarah | - |
| Review PR | Mike | EOD |

---

**Next Meeting:** Wednesday
```

### Project Review Notes

```python
notes = """
Q4 Review - Dec 15

Present: Leadership team, Product, Engineering

Revenue exceeded targets by 12%
Customer satisfaction at 94%
Engineering delivered 15 of 18 planned features

Challenges:
- Hiring slower than expected
- Two key features delayed

2024 Planning:
Q1 focus on performance
Q2 new product launch
Need budget approval for new hires

Actions:
CEO to approve headcount by Dec 20
VP Eng to present technical roadmap
Product to finalize Q1 priorities
"""

formatter = MeetingNotesFormatter(notes)
formatter.format()
formatter.save("q4_review.pdf")
```

## Templates

### Standard (Default)
- Title and metadata header
- Sections with bullet points
- Action items table
- Next meeting footer

### Minimal
- Simple markdown
- No tables
- Compact format

### Detailed
- Full metadata
- Timestamps
- Expanded sections
- Decision log

## Dependencies

```
reportlab>=4.0.0
python-dateutil>=2.8.0
```

## Limitations

- English language only
- Best with structured raw notes
- May miss context in very informal notes
- PDF styling is basic
