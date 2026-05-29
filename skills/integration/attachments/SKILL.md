---
name: attachments
description: This skill should be used when the user asks to "list attachments", "download attachment", "email attachment", "calendar invite", "meeting invite", or wants to work with files attached to emails. Lists, downloads, and extracts calendar events from ICS invites.
triggers:
  - list attachments
  - download attachment
  - email attachment
  - calendar invite
  - meeting invite
---

# /email:attachments - Email Attachments

List, download, and process email attachments including calendar invites.

## Usage

```
/email:attachments <id>           # List attachments for an email
/email:attachments <id> download  # Download a specific attachment
/email:attachments <id> calendar  # Extract calendar event from ICS
```

## When Invoked

### List Mode (default)
1. Call `list_attachments` with the email ID
2. Display attachment names, types, and sizes

### Download Mode
1. Call `list_attachments` to show available files
2. Ask user which attachment to download (if multiple)
3. Call `download_attachment` to save to temp directory
4. Return the file path for further processing

### Calendar Mode
1. Call `extract_calendar_event` to parse the ICS attachment
2. Display event details (title, date, time, location, organizer)
3. Ask if user wants to add to Apple Calendar
4. Call `create_calendar_event` with `confirm=true` only after user approval

## Safety Rules

- Calendar event creation requires explicit user confirmation
- Downloaded files go to temp directory (OS handles cleanup)
- Always show event details before creating calendar entry
