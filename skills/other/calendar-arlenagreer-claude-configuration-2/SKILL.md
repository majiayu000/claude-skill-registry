---
name: calendar
description: Manage Google Calendar with full event operations including viewing schedule, creating/editing/deleting events, finding free time, managing attendees via Google Contacts, adding Google Meet links, and timezone handling. This skill should be used for ALL calendar-related requests.
category: productivity
version: 1.0.0
---

# Google Calendar Management Skill

## Purpose

Manage Arlen Greer's Google Calendar with comprehensive event operations:
- View schedule (today, this week, date ranges)
- Create events with attendees and Google Meet links
- Update and delete events
- Find free time slots during business hours
- Automatic attendee resolution via Google Contacts
- Timezone-aware scheduling
- Block time for focused work

**Primary Calendar**: Uses primary personal calendar by default

## When to Use This Skill

Use this skill when:
- User requests calendar information: "What's on my calendar?", "Show my schedule"
- User wants to create events: "Schedule a meeting", "Create an appointment"
- User wants to modify events: "Move my meeting", "Update the appointment"
- User asks about availability: "When am I free?", "Find time next week"
- User mentions scheduling with others: "Set up a call with [Name]"
- User requests Google Meet: "Add a video call", "Create a Google Meet"

## Core Workflows

### 1. View Schedule

**List today's events**:
```bash
scripts/calendar_manager.rb --operation list
```

**List specific date range**:
```bash
scripts/calendar_manager.rb --operation list \
  --time-min "2024-10-31T00:00:00" \
  --time-max "2024-10-31T23:59:59"
```

**List this week**:
```bash
scripts/calendar_manager.rb --operation list \
  --time-min "2024-10-28T00:00:00" \
  --time-max "2024-11-04T23:59:59" \
  --max-results 50
```

**Natural language time parsing**:
- Accepts ISO8601 format or natural language
- Example: "tomorrow at 3pm", "next Tuesday at 9am"

### 2. Create Events

**Simple event creation**:
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Team Meeting" \
  --start-time "2024-10-31T15:00:00" \
  --end-time "2024-10-31T16:00:00"
```

**Event with attendees (by name)**:
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Upgrade Database Discussion" \
  --start-time "2024-10-31T15:00:00" \
  --end-time "2024-10-31T16:00:00" \
  --attendees "Ed Korkuch,Mark Whitney"
```

**Attendee Resolution**:
- Automatically looks up contacts by name via Google Contacts API
- Falls back to email address if name includes '@'
- Returns error if contact not found (prompts user for email)

**Event with Google Meet**:
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Team Standup" \
  --start-time "2024-11-01T09:00:00" \
  --google-meet
```

**Block time for work**:
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Focus Time - Database Upgrade" \
  --description "Blocked time to work on database migration" \
  --start-time "2024-11-05T09:00:00" \
  --end-time "2024-11-05T11:00:00"
```

**Event with all options**:
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Client Meeting" \
  --description "Discuss Q4 requirements" \
  --location "Conference Room A" \
  --start-time "2024-11-01T14:00:00" \
  --end-time "2024-11-01T15:00:00" \
  --attendees "client@example.com" \
  --google-meet
```

### 3. Update Events

**Update event time**:
```bash
scripts/calendar_manager.rb --operation update \
  --event-id "abc123xyz" \
  --start-time "2024-10-31T16:00:00" \
  --end-time "2024-10-31T17:00:00"
```

**Update event details**:
```bash
scripts/calendar_manager.rb --operation update \
  --event-id "abc123xyz" \
  --summary "Updated Meeting Title" \
  --description "New description"
```

**Getting Event ID**:
- List events first to get the event ID
- Event IDs are returned in all list operations

### 4. Delete Events

```bash
scripts/calendar_manager.rb --operation delete \
  --event-id "abc123xyz"
```

### 5. Find Free Time

**Find next available slot**:
```bash
scripts/calendar_manager.rb --operation find_free \
  --time-min "2024-11-01T00:00:00" \
  --time-max "2024-11-08T23:59:59" \
  --duration 3600 \
  --max-results 5
```

**Find 2-hour blocks during business hours**:
```bash
scripts/calendar_manager.rb --operation find_free \
  --time-min "2024-11-05T00:00:00" \
  --time-max "2024-11-05T23:59:59" \
  --duration 7200 \
  --business-start 9 \
  --business-end 17
```

**Find time parameters**:
- `--duration`: Slot duration in seconds (default: 3600 = 1 hour)
- `--business-start`: Business day start hour (default: 9)
- `--business-end`: Business day end hour (default: 17)
- `--interval`: Check interval in seconds (default: 1800 = 30 min)

**IMPORTANT - Lunchtime Policy**:
- **AVOID scheduling meetings during lunch hours (12:00 PM - 1:00 PM) on weekdays**
- When finding free time, filter out any slots that overlap with noon-1pm
- Only suggest lunchtime slots if user explicitly requests them or no other times available
- This applies to all availability checks and meeting scheduling requests

## Natural Language Examples

### User Says: "What's on my calendar today?"
```bash
# Get today's date from <env> context
scripts/calendar_manager.rb --operation list \
  --time-min "[TODAY]T00:00:00" \
  --time-max "[TODAY]T23:59:59"
```

### User Says: "Schedule a meeting with Ed Korkuch for 3:00 p.m. on the 31st of October and name it 'Upgrade Database'"
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Upgrade Database" \
  --start-time "2024-10-31T15:00:00" \
  --end-time "2024-10-31T16:00:00" \
  --attendees "Ed Korkuch"
```

### User Says: "Find a time when I am free next week during business hours"
```bash
# Calculate next week dates
# NOTE: Filter out lunchtime slots (12:00 PM - 1:00 PM) from results unless user explicitly requests lunch hours
scripts/calendar_manager.rb --operation find_free \
  --time-min "[NEXT_WEEK_START]T00:00:00" \
  --time-max "[NEXT_WEEK_END]T23:59:59" \
  --duration 3600 \
  --business-start 9 \
  --business-end 17 \
  --max-results 10
```

### User Says: "Block off two hours during the normal business day next Tuesday for me to work on [issue]"
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Focus Time - [Issue]" \
  --description "Blocked time to work on [issue description]" \
  --start-time "[NEXT_TUESDAY]T09:00:00" \
  --end-time "[NEXT_TUESDAY]T11:00:00"
```

### User Says: "Move my 3pm meeting to 4pm"
```bash
# First list events to find the 3pm meeting
scripts/calendar_manager.rb --operation list --time-min "[TODAY]T15:00:00" --time-max "[TODAY]T15:01:00"

# Then update with new time
scripts/calendar_manager.rb --operation update \
  --event-id "[EVENT_ID_FROM_LIST]" \
  --start-time "[TODAY]T16:00:00" \
  --end-time "[TODAY]T17:00:00"
```

## Timezone Handling

**Default Timezone**: `America/Chicago`

**Specify different timezone**:
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Meeting" \
  --start-time "2024-10-31T15:00:00" \
  --timezone "America/New_York"
```

**Timezone considerations**:
- All times are stored in the calendar's timezone
- Use `--timezone` flag to specify event timezone
- List operations return times in original timezone
- See `references/timezone_guide.md` for timezone codes

## Authentication Setup

**Shared with Email Skill**:
- Uses same OAuth credentials and token
- Located at: `~/.claude/.google/client_secret.json` and `~/.claude/.google/token.json`
- Requires both Calendar and Contacts API scopes

**First Time Setup**:
1. Run any calendar operation
2. Script will prompt for authorization URL
3. Visit URL and authorize
4. Enter authorization code when prompted
5. Token stored for future use

**Re-authorization**:
- Token automatically refreshes when expired
- If refresh fails, re-run authorization flow

## Bundled Resources

### Scripts

**`scripts/calendar_manager.rb`**
- Comprehensive Google Calendar API wrapper
- All CRUD operations: list, create, update, delete
- Free time finding with business hours logic
- Automatic attendee resolution via Google Contacts
- Google Meet link generation
- Timezone support

**Operations**:
- `list`: View calendar events
- `create`: Create new events
- `update`: Modify existing events
- `delete`: Remove events
- `find_free`: Find available time slots

**Output Format**:
- JSON with `status: 'success'` or `status: 'error'`
- Event objects include: id, summary, start, end, attendees, links
- See script help: `scripts/calendar_manager.rb --help`

### References

**`references/timezone_guide.md`**
- Common timezone codes
- Timezone conversion examples
- Daylight saving time considerations
- International timezone handling

**`references/business_hours.md`**
- Business hours logic and customization
- Finding optimal meeting times
- Blocking focus time strategies
- Calendar best practices

## Error Handling

**Attendee Not Found**:
```json
{
  "status": "error",
  "code": "ATTENDEE_NOT_FOUND",
  "message": "Could not find email for attendee: John Smith"
}
```
**Action**: Prompt user for email address, then retry

**Authentication Error**:
```json
{
  "status": "error",
  "code": "AUTH_ERROR",
  "message": "Token refresh failed: ..."
}
```
**Action**: Guide user through re-authorization

**Invalid Time**:
```json
{
  "status": "error",
  "code": "INVALID_TIME",
  "message": "Failed to parse time: ..."
}
```
**Action**: Ask user to clarify date/time format

**API Error**:
```json
{
  "status": "error",
  "code": "API_ERROR",
  "message": "Failed to create event: ..."
}
```
**Action**: Display error to user, suggest troubleshooting steps

## Best Practices

### Date/Time Parsing
1. Always check current date from `<env>` context
2. Never assume dates from knowledge cutoff
3. Parse natural language: "tomorrow", "next Tuesday", "3pm today"
4. Default to 1-hour duration if end time not specified

### Attendee Management
1. Try contact lookup first for names
2. Fall back to email address if lookup fails
3. Always confirm attendees before sending invites
4. Use comma-separated list for multiple attendees

### Google Meet
1. Add `--google-meet` flag for video calls
2. Meet link auto-generated and included in event
3. All attendees receive calendar invite with link

### Free Time Finding
1. Default to business hours (9am-5pm)
2. **AVOID LUNCHTIME**: Do not suggest times between 12:00 PM - 1:00 PM on weekdays unless user explicitly requests it
3. Use 30-minute intervals for checking
4. Return top 5 slots by default
5. Consider timezone when suggesting times

### Event Updates
1. Always list events first to get event ID
2. Only update specified fields (others unchanged)
3. Send notifications to attendees automatically

## Quick Reference

**View today's schedule**:
```bash
scripts/calendar_manager.rb --operation list
```

**Create meeting with contact**:
```bash
scripts/calendar_manager.rb --operation create \
  --summary "Meeting Title" \
  --start-time "2024-11-01T14:00:00" \
  --attendees "First Last"
```

**Add Google Meet**:
```bash
# Add --google-meet flag to any create operation
```

**Find free time next week**:
```bash
scripts/calendar_manager.rb --operation find_free \
  --time-min "[NEXT_WEEK]T00:00:00" \
  --time-max "[NEXT_WEEK_END]T23:59:59"
```

**Update event time**:
```bash
scripts/calendar_manager.rb --operation update \
  --event-id "[ID]" \
  --start-time "[NEW_TIME]"
```

## Example Workflow: Scheduling a Meeting

1. **Check availability**:
   ```bash
   scripts/calendar_manager.rb --operation find_free \
     --time-min "2024-11-01T00:00:00" \
     --time-max "2024-11-08T23:59:59" \
     --duration 3600
   ```

2. **Create event with attendees**:
   ```bash
   scripts/calendar_manager.rb --operation create \
     --summary "Project Review" \
     --start-time "2024-11-05T14:00:00" \
     --attendees "Ed Korkuch,Mark Whitney" \
     --google-meet
   ```

3. **Confirm creation**:
   - Script returns event ID, summary, links
   - Attendees receive calendar invites
   - Google Meet link automatically included

## Version History

- **1.0.0** (2024-10-28) - Initial calendar skill with full CRUD operations, Google Meet integration, contact lookup for attendees, free time finding, and timezone support

---

**Dependencies**: Ruby with `google-apis-calendar_v3`, `google-apis-people_v1`, `googleauth` gems (same as email skill)
