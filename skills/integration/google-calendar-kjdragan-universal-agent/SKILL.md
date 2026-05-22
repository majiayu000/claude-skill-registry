---
name: google_calendar
description: Manage calendar events using Google Calendar via Composio.
metadata: {"requires": ["composio"]}
---

# Google Calendar Skill

This skill allows you to manage calendar events using the Composio Google Calendar integration.

## Tools
You have access to the following Composio tools (namespaces may vary, check `mcp__composio__*`):
- `GOOGLECALENDAR_CREATE_EVENT`: Create new events.
- `GOOGLECALENDAR_LIST_EVENTS`: List upcoming events.
- `GOOGLECALENDAR_UPDATE_EVENT`: Modify existing events.
- `GOOGLECALENDAR_DELETE_EVENT`: Remove events.

## Usage Guidelines
1.  **Authentication**: If auth is required, the tool will provide a link. Pass this to the user.
2.  **Date/Time**: Always use ISO format or relative terms that the tool understands.
3.  **Timezone**: Be aware of the user's timezone (check context).

## workflows
- **Schedule Meeting**: verify availability -> create event -> notify user.
- **Daily Briefing**: list events for today -> summarize.
