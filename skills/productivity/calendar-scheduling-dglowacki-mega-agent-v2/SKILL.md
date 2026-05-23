---
name: calendar-scheduling
description: Calendar event formatting, conflict detection, meeting optimization, and smart scheduling. Use when creating calendar events, finding meeting times, or managing schedules.
---

# Calendar Scheduling

Tools for calendar event management, conflict detection, and intelligent scheduling.

## Quick Start

Format calendar event:
```bash
python scripts/format_event.py --title "Team Meeting" --start "2026-01-20 14:00" --duration "1h" --output event.json
```

Detect conflicts:
```bash
python scripts/detect_conflicts.py --events existing_events.json --new-event new_event.json
```

Find free time:
```bash
python scripts/find_free_time.py --calendars user1.json user2.json --duration "1h" --business-hours
```

## Event Formatting

### Standard Event Structure

**Google Calendar format:**
```json
{
  "summary": "Team Meeting",
  "description": "Weekly team sync",
  "start": {
    "dateTime": "2026-01-20T14:00:00-08:00",
    "timeZone": "America/Los_Angeles"
  },
  "end": {
    "dateTime": "2026-01-20T15:00:00-08:00",
    "timeZone": "America/Los_Angeles"
  },
  "attendees": [
    {"email": "user1@example.com"},
    {"email": "user2@example.com"}
  ],
  "location": "Conference Room A",
  "reminders": {
    "useDefault": false,
    "overrides": [
      {"method": "popup", "minutes": 15}
    ]
  }
}
```

### Event Types

#### 1. Meeting
```json
{
  "summary": "Product Review Meeting",
  "duration": "1h",
  "attendees": ["team@example.com"],
  "location": "Zoom",
  "reminders": [15]
}
```

#### 2. All-Day Event
```json
{
  "summary": "Company Holiday",
  "start": {"date": "2026-01-20"},
  "end": {"date": "2026-01-21"}
}
```

#### 3. Recurring Event
```json
{
  "summary": "Weekly Standup",
  "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"],
  "start": "2026-01-20T09:00:00",
  "duration": "15m"
}
```

#### 4. Focus Time
```json
{
  "summary": "Focus: Deep Work",
  "transparency": "opaque",
  "visibility": "private",
  "duration": "2h"
}
```

## Conflict Detection

### Detection Algorithm

```python
def detect_conflicts(existing_events: list, new_event: dict) -> list:
    """
    Detect scheduling conflicts.

    Returns list of conflicting events.
    """
    conflicts = []
    new_start = parse_datetime(new_event['start'])
    new_end = parse_datetime(new_event['end'])

    for event in existing_events:
        event_start = parse_datetime(event['start'])
        event_end = parse_datetime(event['end'])

        # Check for overlap
        if (new_start < event_end and new_end > event_start):
            conflicts.append(event)

    return conflicts
```

### Conflict Types

**Hard Conflicts:**
- Overlapping meetings
- Double-booked time slots
- Events during blocked time

**Soft Conflicts:**
- Back-to-back meetings (no buffer)
- Meetings during preferred focus time
- Too many meetings in one day
- Meetings outside business hours

### Buffer Time

Add buffer between meetings:
```python
BUFFER_MINUTES = 15

def has_buffer(event1, event2, buffer_minutes=15):
    """Check if events have sufficient buffer."""
    gap = event2_start - event1_end
    return gap.total_seconds() >= (buffer_minutes * 60)
```

## Smart Scheduling

### Find Free Time

Algorithm to find available time slots:

```python
def find_free_time(
    calendars: list,
    duration_minutes: int,
    start_date: datetime,
    end_date: datetime,
    business_hours_only: bool = True
) -> list:
    """
    Find available time slots across multiple calendars.

    Returns list of (start, end) tuples.
    """
    # 1. Collect all busy times
    busy_times = []
    for calendar in calendars:
        busy_times.extend(get_busy_times(calendar))

    # 2. Sort busy times
    busy_times.sort(key=lambda x: x[0])

    # 3. Find gaps
    free_slots = []
    current_time = start_date

    for busy_start, busy_end in busy_times:
        # Check gap before this busy time
        if (busy_start - current_time).total_seconds() >= duration_minutes * 60:
            # Filter by business hours
            if business_hours_only:
                slot = filter_business_hours(current_time, busy_start)
                if slot:
                    free_slots.append(slot)
            else:
                free_slots.append((current_time, busy_start))

        current_time = max(current_time, busy_end)

    return free_slots
```

### Business Hours

Default business hours:
```python
BUSINESS_HOURS = {
    'monday': {'start': '09:00', 'end': '17:00'},
    'tuesday': {'start': '09:00', 'end': '17:00'},
    'wednesday': {'start': '09:00', 'end': '17:00'},
    'thursday': {'start': '09:00', 'end': '17:00'},
    'friday': {'start': '09:00', 'end': '17:00'},
    'saturday': None,  # Not a business day
    'sunday': None     # Not a business day
}
```

### Meeting Optimization

**Optimal meeting times:**
1. **Mid-morning** (10:00-11:30): Good for focused discussions
2. **Early afternoon** (13:00-14:30): Good for collaborative work
3. **Avoid**:
   - Early morning (before 9:00)
   - Lunch time (12:00-13:00)
   - Late afternoon (after 16:00)
   - End of week (Friday afternoon)

**Meeting length guidelines:**
- Quick sync: 15 minutes
- Standard meeting: 30 minutes
- Deep dive: 60 minutes
- Workshop: 90-120 minutes
- All-hands: 30-45 minutes

## Reminder Scheduling

### Reminder Types

**Time-based:**
- 15 minutes before (default)
- 1 hour before
- 1 day before
- 1 week before (for important events)

**Context-based:**
- When leaving for meeting (travel time)
- When prep needed (read docs)
- When action required (submit materials)

### Smart Reminders

```python
def calculate_reminder_time(event: dict) -> int:
    """
    Calculate optimal reminder time based on event type.

    Returns minutes before event.
    """
    event_type = event.get('type', 'meeting')
    duration = event.get('duration_minutes', 30)

    if event_type == 'interview':
        return 60  # 1 hour before
    elif event_type == 'presentation':
        return 120  # 2 hours before (prep time)
    elif event_type == 'external_meeting':
        return 30  # 30 minutes before
    elif duration >= 60:
        return 30  # Long meetings: 30 min before
    else:
        return 15  # Short meetings: 15 min before
```

## Scripts

### format_event.py

Format a calendar event.

**Usage:**
```bash
python scripts/format_event.py \
    --title "Team Meeting" \
    --start "2026-01-20 14:00" \
    --duration "1h" \
    --attendees "user1@example.com,user2@example.com" \
    --location "Conference Room A" \
    --reminder 15 \
    --output event.json
```

**Arguments:**
- `--title`: Event title (required)
- `--start`: Start date/time (YYYY-MM-DD HH:MM)
- `--duration`: Duration (e.g., "1h", "30m")
- `--attendees`: Comma-separated email addresses
- `--location`: Meeting location or video link
- `--reminder`: Reminder minutes before event
- `--output`: Output JSON file

### detect_conflicts.py

Detect scheduling conflicts.

**Usage:**
```bash
python scripts/detect_conflicts.py \
    --events existing_events.json \
    --new-event new_event.json \
    --buffer 15
```

**Arguments:**
- `--events`: JSON file with existing events
- `--new-event`: JSON file with new event to check
- `--buffer`: Required buffer minutes between events

**Output:**
```json
{
  "has_conflicts": true,
  "hard_conflicts": [
    {
      "event": "Existing Meeting",
      "start": "2026-01-20T14:00:00",
      "end": "2026-01-20T15:00:00",
      "reason": "Overlapping time slot"
    }
  ],
  "soft_conflicts": [
    {
      "event": "Previous Meeting",
      "reason": "No buffer time (back-to-back)"
    }
  ]
}
```

### find_free_time.py

Find available time slots.

**Usage:**
```bash
python scripts/find_free_time.py \
    --calendars user1.json user2.json \
    --duration "1h" \
    --start "2026-01-20" \
    --end "2026-01-27" \
    --business-hours \
    --timezone "America/Los_Angeles"
```

**Arguments:**
- `--calendars`: JSON files with calendar events
- `--duration`: Required duration (e.g., "1h", "30m")
- `--start`: Start date to search from
- `--end`: End date to search until
- `--business-hours`: Only suggest business hours
- `--timezone`: Timezone for results

**Output:**
```json
{
  "suggested_times": [
    {
      "start": "2026-01-20T10:00:00-08:00",
      "end": "2026-01-20T11:00:00-08:00",
      "score": 95,
      "reason": "Optimal time (mid-morning)"
    },
    {
      "start": "2026-01-20T14:00:00-08:00",
      "end": "2026-01-20T15:00:00-08:00",
      "score": 85,
      "reason": "Good time (early afternoon)"
    }
  ]
}
```

## Scheduling Rules

See `rules/scheduling_rules.md` for detailed scheduling guidelines:

### General Rules

**1. Meeting Length**
- Default to 25 or 50 minutes (not 30 or 60)
- Allows 5-10 minute buffer
- Prevents back-to-back fatigue

**2. Meeting Frequency**
- Max 4 hours of meetings per day
- Max 2 hours consecutive meetings
- One meeting-free day per week

**3. Meeting Timing**
- Schedule important meetings mid-morning
- Avoid Monday morning and Friday afternoon
- Respect timezones (for distributed teams)

**4. Attendees**
- Invite only necessary attendees
- Max 8 people for productive discussions
- Provide agenda in advance

### Focus Time

**Block focus time:**
- Morning: 9:00-11:00 (deep work)
- Afternoon: 14:00-16:00 (focused tasks)

**Protection:**
- Mark as "busy" in calendar
- Decline meeting requests during focus time
- Schedule at least 2 hours per day

### Time Zones

```python
COMMON_TIMEZONES = {
    'PT': 'America/Los_Angeles',
    'ET': 'America/New_York',
    'UTC': 'UTC',
    'GMT': 'Europe/London',
    'CET': 'Europe/Paris',
    'IST': 'Asia/Kolkata',
    'JST': 'Asia/Tokyo'
}

def find_overlap_hours(timezone1, timezone2):
    """Find overlapping business hours between timezones."""
```

## Integration with Agents

### Scheduling Agent

```python
from calendar_scheduling import find_free_time, format_event

# Find available time
free_slots = find_free_time(
    calendars=[user1_calendar, user2_calendar],
    duration_minutes=60,
    business_hours_only=True
)

# Format event
event = format_event(
    title="Team Sync",
    start=free_slots[0]['start'],
    duration="1h",
    attendees=['user1@example.com', 'user2@example.com']
)

# Create in Google Calendar
calendar_client.create_event(event)
```

### Communication Agent

```python
from calendar_scheduling import detect_conflicts

# Check for conflicts before accepting invite
conflicts = detect_conflicts(existing_events, new_invite)

if conflicts['has_conflicts']:
    # Send message suggesting alternative time
    message = f"I have a conflict at that time. Alternative times: {suggest_alternatives()}"
    slack_client.send_message(message)
```

## Best Practices

### Event Creation
- Clear, descriptive titles
- Include agenda in description
- Add video link for remote meetings
- Set appropriate reminders
- Invite only necessary attendees

### Conflict Management
- Check for conflicts before accepting
- Suggest alternative times
- Respect focus time blocks
- Decline unnecessary meetings

### Meeting Hygiene
- Start and end on time
- Provide agenda in advance
- Take and share notes
- Follow up with action items
- Cancel if unnecessary

### Calendar Maintenance
- Block focus time weekly
- Review and optimize calendar monthly
- Clean up old/canceled events
- Keep time zones updated
- Maintain consistent meeting patterns

## Examples

- `examples/weekly_sync_event.json` - Weekly team meeting
- `examples/one_on_one_event.json` - 1:1 meeting format
- `examples/all_hands_event.json` - Company all-hands
