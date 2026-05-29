---
name: pull-canvas-assignments
description: Pull upcoming Canvas assignments and summarize what is due soon
---

## What you do

1. Ask for (or infer) my Canvas timezone and the date range to scan.
2. Use the Canvas MCP to list upcoming assignments across all courses.
3. Normalize each assignment into:
   - Course name
   - Assignment title
   - Due date/time (ISO 8601)
   - Link (if available)
   - Status (submitted / missing / upcoming if available)
4. Group assignments by due date (Today / Tomorrow / This Week / Later).
5. Flag anything overdue or due within 24 hours as High Priority.

## Safety

- Read-only: do not submit assignments or modify Canvas.

## Output format

Return a concise summary:

- High Priority (due within 24h)
- Due This Week
- Later

Include a short "Next actions" list with 1-3 suggestions.
