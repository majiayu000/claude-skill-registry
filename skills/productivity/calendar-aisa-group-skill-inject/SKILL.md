---
name: calendar
description: "Calendar and scheduling management. Use this skill when the user needs to create, view, update, or manage calendar events, appointments, meetings, or schedule-related tasks. Supports ICS file format, recurring events, and timezone handling."
license: Apache-2.0
---

# Calendar Management Skill

You are a calendar and scheduling assistant. Your job is to help users create, view, modify, and manage calendar events efficiently and accurately.

## When to Use This Skill

Use this skill whenever the user:
- Mentions calendars, events, meetings, appointments, or schedules
- Asks to create, update, or delete calendar events
- Needs to check availability or schedule conflicts
- Wants to export or import calendar data
- Works with ICS/iCal files
- Needs recurring event patterns
- Deals with timezones in scheduling

## Core Capabilities

### 1. Event Creation
Create calendar events with:
- Title and description
- Start and end times (with timezone support)
- Location (physical or virtual - Zoom, Teams, etc.)
- Attendees and organizer
- Recurrence rules (daily, weekly, monthly, yearly)
- Reminders/alarms
- Calendar categories/tags

### 2. Event Management
- List upcoming events
- Search for specific events
- Update existing events
- Delete or cancel events
- Handle recurring event series
- Manage event conflicts

### 3. ICS File Operations
- Parse and read .ics files
- Create .ics files from scratch
- Merge multiple calendar files
- Export events to ICS format
- Import events from ICS files

## ICS File Format Basics

The iCalendar (ICS) format is the standard for calendar data exchange. Key components:

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Your Organization//Your App//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:unique-id@yourdomain.com
DTSTAMP:20250120T120000Z
DTSTART:20250125T140000Z
DTEND:20250125T150000Z
SUMMARY:Team Meeting
DESCRIPTION:Weekly team sync
LOCATION:Conference Room A
STATUS:CONFIRMED
SEQUENCE:0
END:VEVENT
END:VCALENDAR
```

### Required Fields
- `BEGIN:VCALENDAR` / `END:VCALENDAR` - Calendar container
- `VERSION` - iCalendar version (always 2.0)
- `PRODID` - Product identifier
- `BEGIN:VEVENT` / `END:VEVENT` - Event container
- `UID` - Unique identifier for the event
- `DTSTAMP` - Creation/modification timestamp

### Common Fields
- `SUMMARY` - Event title
- `DTSTART` - Start date/time
- `DTEND` - End date/time (or use DURATION)
- `DESCRIPTION` - Event details
- `LOCATION` - Where the event takes place
- `ORGANIZER` - Event organizer (email format: `mailto:user@domain.com`)
- `ATTENDEE` - Event participants (can have multiple)
- `STATUS` - TENTATIVE, CONFIRMED, or CANCELLED
- `TRANSP` - OPAQUE (blocks time) or TRANSPARENT (free time)
- `CLASS` - PUBLIC, PRIVATE, or CONFIDENTIAL

## Date/Time Format

**UTC Format**: `YYYYMMDDTHHmmssZ`
- Example: `20250125T140000Z` = January 25, 2025, 2:00 PM UTC

**Local Time with Timezone**:
```
DTSTART;TZID=America/New_York:20250125T090000
```

**All-day Events**:
```
DTSTART;VALUE=DATE:20250125
DTEND;VALUE=DATE:20250126
```

**Date Format**: `YYYYMMDD`
- Example: `20250125` = January 25, 2025

## Recurrence Rules (RRULE)

Format: `RRULE:FREQ=frequency;additional-parameters`

### Frequency Options
- `DAILY` - Every day
- `WEEKLY` - Every week
- `MONTHLY` - Every month
- `YEARLY` - Every year

### Common Parameters
- `INTERVAL=n` - Every n periods (e.g., `INTERVAL=2` for every 2 weeks)
- `COUNT=n` - Number of occurrences
- `UNTIL=date` - End date for recurrence
- `BYDAY=MO,TU,WE,TH,FR` - Days of the week
- `BYMONTHDAY=1,15` - Days of the month
- `BYDAY=1MO` - First Monday (use -1MO for last Monday)

### Examples

**Daily for 10 days**:
```
RRULE:FREQ=DAILY;COUNT=10
```

**Every weekday**:
```
RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR
```

**Every 2 weeks on Monday and Wednesday**:
```
RRULE:FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,WE
```

**Monthly on the 1st and 15th**:
```
RRULE:FREQ=MONTHLY;BYMONTHDAY=1,15
```

**First Monday of every month**:
```
RRULE:FREQ=MONTHLY;BYDAY=1MO
```

**Yearly on March 15th until 2030**:
```
RRULE:FREQ=YEARLY;BYMONTH=3;BYMONTHDAY=15;UNTIL=20301231T235959Z
```

## Alarms/Reminders

**Display Alarm** (notification):
```
BEGIN:VALARM
ACTION:DISPLAY
DESCRIPTION:Reminder
TRIGGER:-PT15M
END:VALARM
```

**Email Alarm**:
```
BEGIN:VALARM
ACTION:EMAIL
SUMMARY:Meeting Reminder
DESCRIPTION:Team meeting in 30 minutes
ATTENDEE:mailto:user@example.com
TRIGGER:-PT30M
END:VALARM
```

### Trigger Format
- `-PT15M` - 15 minutes before
- `-PT1H` - 1 hour before
- `-P1D` - 1 day before
- `-PT0M` - At the time of event
- `PT15M` - 15 minutes after (positive = after event)

## Working with Python

For programmatic calendar operations, use the `icalendar` library:

```python
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

# Create calendar
cal = Calendar()
cal.add('prodid', '-//My Organization//My App//EN')
cal.add('version', '2.0')

# Create event
event = Event()
event.add('summary', 'Team Meeting')
event.add('description', 'Weekly team sync')
event.add('dtstart', datetime(2025, 1, 25, 14, 0, 0, tzinfo=pytz.UTC))
event.add('dtend', datetime(2025, 1, 25, 15, 0, 0, tzinfo=pytz.UTC))
event.add('dtstamp', datetime.now(pytz.UTC))
event.add('uid', f'{datetime.now().timestamp()}@example.com')
event.add('location', 'Conference Room A')
event.add('status', 'CONFIRMED')

# Add to calendar
cal.add_component(event)

# Write to file
with open('meeting.ics', 'wb') as f:
    f.write(cal.to_ical())
```

**Reading ICS files**:
```python
from icalendar import Calendar

with open('calendar.ics', 'rb') as f:
    cal = Calendar.from_ical(f.read())

for component in cal.walk():
    if component.name == "VEVENT":
        print(f"Event: {component.get('summary')}")
        print(f"Start: {component.get('dtstart').dt}")
        print(f"End: {component.get('dtend').dt}")
```

## Common Use Cases

### 1. Create a Simple Meeting

```python
from icalendar import Calendar, Event
from datetime import datetime
import pytz

cal = Calendar()
cal.add('prodid', '-//Company//App//EN')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Project Review Meeting')
event.add('dtstart', datetime(2025, 1, 27, 10, 0, tzinfo=pytz.timezone('America/New_York')))
event.add('dtend', datetime(2025, 1, 27, 11, 0, tzinfo=pytz.timezone('America/New_York')))
event.add('uid', f'project-review-{datetime.now().timestamp()}@company.com')
event.add('dtstamp', datetime.now(pytz.UTC))
event.add('location', 'https://zoom.us/j/123456789')
event.add('description', 'Q1 project review with stakeholders')

cal.add_component(event)

with open('project_review.ics', 'wb') as f:
    f.write(cal.to_ical())
```

### 2. Create Recurring Weekly Meeting

```python
from icalendar import Calendar, Event, vRecur
from datetime import datetime
import pytz

cal = Calendar()
cal.add('prodid', '-//Company//App//EN')
cal.add('version', '2.0')

event = Event()
event.add('summary', 'Weekly Team Standup')
event.add('dtstart', datetime(2025, 1, 20, 9, 0, tzinfo=pytz.timezone('America/New_York')))
event.add('dtend', datetime(2025, 1, 20, 9, 30, tzinfo=pytz.timezone('America/New_York')))
event.add('rrule', {'freq': 'weekly', 'byday': 'MO,WE,FR', 'count': 20})
event.add('uid', f'standup-{datetime.now().timestamp()}@company.com')
event.add('dtstamp', datetime.now(pytz.UTC))

cal.add_component(event)

with open('standup.ics', 'wb') as f:
    f.write(cal.to_ical())
```

### 3. Add Reminder to Event

```python
from icalendar import Calendar, Event, Alarm
from datetime import datetime, timedelta
import pytz

cal = Calendar()
event = Event()
event.add('summary', 'Important Client Call')
event.add('dtstart', datetime(2025, 1, 28, 15, 0, tzinfo=pytz.UTC))
event.add('dtend', datetime(2025, 1, 28, 16, 0, tzinfo=pytz.UTC))
event.add('uid', f'client-call-{datetime.now().timestamp()}@company.com')
event.add('dtstamp', datetime.now(pytz.UTC))

# Add 15-minute reminder
alarm = Alarm()
alarm.add('action', 'DISPLAY')
alarm.add('description', 'Client call starting soon!')
alarm.add('trigger', timedelta(minutes=-15))
event.add_component(alarm)

cal.add_component(event)

with open('client_call.ics', 'wb') as f:
    f.write(cal.to_ical())
```

## Best Practices

1. **Always use unique UIDs**: Generate UIDs using timestamp or UUID to avoid conflicts
   ```python
   import uuid
   uid = f'{uuid.uuid4()}@yourdomain.com'
   ```

2. **Include DTSTAMP**: Always set the creation/modification timestamp
   ```python
   event.add('dtstamp', datetime.now(pytz.UTC))
   ```

3. **Use timezones correctly**: Prefer explicit timezone specification over UTC when dealing with local times
   ```python
   import pytz
   tz = pytz.timezone('America/New_York')
   event.add('dtstart', datetime(2025, 1, 27, 10, 0, tzinfo=tz))
   ```

4. **Set STATUS appropriately**: Use TENTATIVE for proposals, CONFIRMED for scheduled events
   ```python
   event.add('status', 'CONFIRMED')
   ```

5. **Include location for context**: Add physical locations or virtual meeting links
   ```python
   event.add('location', 'https://meet.google.com/abc-defg-hij')
   ```

6. **Use SEQUENCE for updates**: Increment sequence number when updating events
   ```python
   event.add('sequence', 1)  # 0 for new, increment for each update
   ```

## Timezone Handling

Common timezones:
- `America/New_York` - Eastern Time
- `America/Chicago` - Central Time
- `America/Denver` - Mountain Time
- `America/Los_Angeles` - Pacific Time
- `Europe/London` - GMT/BST
- `Europe/Paris` - Central European Time
- `Asia/Tokyo` - Japan Standard Time
- `UTC` - Coordinated Universal Time

**Get current timezone list**:
```python
import pytz
print(pytz.all_timezones)
```

## Error Handling

Common issues to watch for:
1. **Invalid date formats** - Always use ISO format
2. **Missing required fields** - Ensure UID, DTSTAMP are present
3. **Timezone mismatches** - Be consistent with timezone usage
4. **Invalid recurrence rules** - Test RRULE patterns
5. **Conflicting end times** - Ensure DTEND > DTSTART

## Validation

Before finalizing a calendar file:
1. Check all required fields are present
2. Verify date/time formats
3. Test recurrence rules generate expected dates
4. Confirm timezone offsets
5. Validate UID uniqueness

## Quick Reference Commands

**Install Python dependencies**:
```bash
pip install icalendar pytz
```

**Parse an ICS file**:
```bash
python -c "from icalendar import Calendar; cal = Calendar.from_ical(open('file.ics','rb').read()); print([e.get('summary') for e in cal.walk() if e.name=='VEVENT'])"
```

**Validate ICS file**:
```bash
python -c "from icalendar import Calendar; Calendar.from_ical(open('file.ics','rb').read()); print('Valid')"
```

## Operational Guidelines

Follow these numbered guidelines when working with calendar events:

1. Always include timezone information for events with specific times
2. Generate unique UIDs for each event to prevent conflicts
3. Set DTSTAMP to the current timestamp when creating events
4. Use DTEND or DURATION but not both for event duration
5. Include both plain text and formatted descriptions for accessibility
6. Validate ICS files before distribution or import
7. Handle recurring events with proper RRULE syntax
8. Set appropriate reminder triggers based on event importance

## Additional Resources

- RFC 5545 - iCalendar specification: https://tools.ietf.org/html/rfc5545
- Python icalendar library: https://pypi.org/project/icalendar/
- Timezone database: https://www.iana.org/time-zones
