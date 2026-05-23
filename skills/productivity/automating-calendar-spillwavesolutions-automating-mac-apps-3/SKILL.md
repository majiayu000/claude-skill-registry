---
name: automating-calendar
description: Automates macOS Calendar via JXA with AppleScript dictionary discovery. Use when asked to "create calendar events", "automate calendar", "JXA calendar scripting", "EventKit automation", or "PyXA calendar automation". Covers events, calendars, recurrence, time zones, batch operations, and EventKit ObjC bridge.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Automating Calendar (JXA with AppleScript Discovery)

## Contents
- [Relationship to the macOS automation skill](#relationship-to-the-macos-automation-skill)
- [Core Framing](#core-framing)
- [Workflow (default)](#workflow-default)
- [Core Examples](#core-examples)
- [What to load](#what-to-load)

## Relationship to the macOS automation skill
- Use `automating-mac-apps` for general app permissions, shell commands, UI scripting, and cross-app automation patterns.
- This skill focuses specifically on Calendar events, calendars, and EventKit bridge functionality.
- **PyXA Installation:** To use PyXA examples in this skill, see the installation instructions in `automating-mac-apps` skill (PyXA Installation section).

## Core Framing
- Calendar dictionary is AppleScript-first; discover there
- JXA provides logic, data handling, and ObjC/EventKit bridge access
- PyXA offers modern Python alternative with cleaner syntax

**Implementation Notes:** See `automating-calendar/references/calendar-basics.md`

## Workflow (default)
1) [ ] Discover Calendar dictionary terms in Script Editor.
2) [ ] Prototype minimal AppleScript commands.
3) [ ] Port to JXA with defensive error handling.
4) [ ] Implemented batch reads (avoided heavy `.whose()`).
5) [ ] Added EventKit bridge for advanced queries.
6) [ ] Tested with sample events and verified results.

### Error Handling
- Wrap operations in try-catch blocks
- Verify calendar access: `Calendar.calendars.length > 0`
- Check event creation: `if (!event.id()) throw new Error('Event creation failed')`
- Log operations for debugging

### Validation Checklist
- [ ] Calendar permissions granted (System Settings > Privacy & Security > Calendars)
- [ ] Calendar access confirmed: `Calendar.calendars.length > 0`
- [ ] Event created with valid start/end dates
- [ ] Event visible in Calendar UI after save
- [ ] EventKit bridge queries return expected results
- [ ] Error handling wraps all operations
- [ ] Output matches expected event properties

## Core Examples

**Basic Event Creation (JXA - Legacy):**
```javascript
const Calendar = Application("Calendar");
const event = Calendar.calendars[0].events.push(Calendar.Event({
  summary: "Meeting",
  startDate: new Date(),
  endDate: new Date(Date.now() + 3600000)
}));
```

**Basic Event Creation (PyXA - Recommended):**
```python
import PyXA
from datetime import datetime, timedelta

calendar = PyXA.Calendar()

# Get first calendar
work_calendar = calendar.calendars()[0]

# Create event
event = work_calendar.events().push({
    "summary": "Meeting",
    "start_date": datetime.now(),
    "end_date": datetime.now() + timedelta(hours=1),
    "location": "Conference Room A"
})

print(f"Created event: {event.summary()}")
```

**PyObjC with EventKit (Advanced):**
```python
from EventKit import EKEventStore, EKEvent, EKCalendar
from Foundation import NSDate, NSTimeInterval
import objc

# Initialize event store
store = EKEventStore.alloc().init()

# Request access (async in real implementation)
# store.requestAccessToEntityType_completion_(EKEntityTypeEvent, None)

# Get default calendar
calendars = store.calendarsForEntityType_(EKEntityTypeEvent)
if calendars:
    default_calendar = calendars[0]

    # Create event
    event = EKEvent.eventWithEventStore_(store)
    event.setTitle_("Meeting")
    event.setStartDate_(NSDate.date())
    event.setEndDate_(NSDate.dateWithTimeIntervalSinceNow_(3600))  # 1 hour
    event.setCalendar_(default_calendar)

    # Save event
    error = objc.nil
    success = store.saveEvent_span_error_(event, EKSpanThisEvent, error)

    if success:
        print(f"Event created: {event.title()}")
    else:
        print(f"Error creating event: {error}")
```

**EventKit Bridge Query (JXA - Legacy):**
```javascript
ObjC.import('EventKit');
const store = $.EKEventStore.alloc.init;
// See 'eventkit-query.md' for full predicate implementation
```

**EventKit Bridge Query (PyObjC - Modern):**
```python
from EventKit import EKEventStore, EKEntityTypeEvent, NSPredicate
from Foundation import NSDate

store = EKEventStore.alloc().init()

# Get events for today
start_date = NSDate.date()  # Today
end_date = NSDate.dateWithTimeIntervalSinceNow_(86400)  # Tomorrow

calendars = store.calendarsForEntityType_(EKEntityTypeEvent)
predicate = store.predicateForEventsWithStartDate_endDate_calendars_(
    start_date, end_date, calendars)

events = store.eventsMatchingPredicate_(predicate)

for event in events:
    print(f"Event: {event.title()}, Start: {event.startDate()}")
```

## When Not to Use
- Cross-platform calendar automation (use Google Calendar API or CalDAV)
- iCloud sync operations (use EventKit directly)
- Non-macOS platforms
- Simple AppleScript-only tasks (skip JXA complexity)
- Calendar sharing or permissions management (use Calendar UI)

## What to load
- Calendar JXA basics: `automating-calendar/references/calendar-basics.md`
- Recipes (events, alarms, recurrence): `automating-calendar/references/calendar-recipes.md`
- Advanced patterns (time zones, batch reads, EventKit bridge): `automating-calendar/references/calendar-advanced.md`
- Dictionary translation table: `automating-calendar/references/calendar-dictionary.md`
- **PyXA API Reference** (complete class/method docs): `automating-calendar/references/calendar-pyxa-api-reference.md`
- EventKit query example: `automating-calendar/references/eventkit-query.md`
- EventKit create with recurrence: `automating-calendar/references/eventkit-create.md`
- EventKit time zone example: `automating-calendar/references/eventkit-timezones.md`
- EventKit exceptions/occurrences: `automating-calendar/references/eventkit-exceptions.md`
- EventKit cancel occurrence example: `automating-calendar/references/eventkit-occurrence-cancel.md`