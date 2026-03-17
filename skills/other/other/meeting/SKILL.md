---
context: fork
model: haiku
---

# /meeting

Create a new meeting note in the Obsidian vault.

## Usage

```
/meeting <title>
/meeting <title> with <attendees>
/meeting <title> for <project>
```

## Examples

```
/meeting Weekly Sync
/meeting MyDataIntegration Review with Johann, Pat
/meeting NewProductLine Update for Project - 777-X EIS Programme
```

## Instructions

1. Parse the command for:
   - **title**: The meeting name (required)
   - **attendees**: People mentioned after "with" (optional)
   - **project**: Project mentioned after "for" (optional)

2. Generate filename: `Meeting - YYYY-MM-DD {{title}}.md`
   - Use today's date
   - Sanitize title (remove special characters)

3. Create the meeting note in the **+Meetings/** folder with this structure:

```markdown
---
type: Meeting
title: { { title } }
created: { { DATE } }
modified: { { DATE } }
tags: []
date: "{{DATE}}"
project: { { project_link or null } }
attendees: [{ { attendee_links } }]
summary:
collections: { { collections or null } }
---

# {{title}}

## Attendees

{{attendee_list}}

## Agenda

1.

## Discussion Notes

## Action Items

- [ ]

## Decisions Made

-

## Follow-up

-
```

4. For attendees:
   - Format as wiki-links: `[[Name]]`
   - In frontmatter: `["[[Jane Doe]]", "[[Johann Fender]]"]`
   - In body: bullet list with links

5. For project:
   - Format as wiki-link: `"[[Project - MyDataIntegration]]"`
   - Match against existing project names if partial match given

6. After creating, confirm and show the file path
