---
name: search-calendar
description: >-
  Search Google Calendar with natural language. Find events by date, title, attendees, or email domains.
  Optimized for time-based briefings with explicit timestamps and rich event context.
  
  Parameters:
  - date (string): 'tomorrow', 'next Monday', 'Oct 25'
  - time_range: {start: ISO datetime, end: ISO datetime}
  - subject (string): Search in event titles
  - attendees (string[]): Filter by attendee names
  - emails (string[]): Filter by email/domains
  
  Returns: [{
    event_id: string,
    title: string,
    start_time: ISO datetime (Asia/Singapore timezone),
    end_time: ISO datetime (Asia/Singapore timezone),
    duration_minutes: number,
    attendees: {name: string, email: string, response_status: string}[],
    location?: string,
    description?: string,
    has_attachments: boolean,
    prep_needed: boolean,
    conferencing?: {type: string, url: string}
  }]
---

# Search Calendar Skill

This skill teaches Claude how to intelligently search your Google Calendar with multiple search criteria and flexible natural language understanding.

## When to Use This Skill

Use this skill when users ask questions like:
- "Show me events on Monday with Eddie"
- "Find all 'SnR:Huddle' meetings this week"
- "What do I have on 21 Oct 2025?"
- "List standup meetings with John Hor next week"
- "Events with sentient.io emails today"
- "When am I meeting with Wilson Ang?"

## How to Search Calendars Effectively

### Search Dimensions

Claude can search calendars across these dimensions:

#### 1. **By Day** (Today, Tomorrow, Specific Weekdays)
- "today", "tomorrow", "yesterday"
- Weekday names: "Monday", "Tuesday", etc.
- With modifiers: "next Monday", "last Friday", "this Thursday"

#### 2. **By Date** (Specific Dates)
- Multiple formats supported: "21 Oct 2025", "October 21", "2025-10-21", "21/10/2025"
- Claude can parse these flexibly

#### 3. **By Week** (Calendar Weeks)
- "this week", "next week", "last week"

#### 4. **By Subject/Title** (Event Names)
- Search event titles: "SnR:Huddle", "standup", "planning", "review"
- Use partial matches: "huddle" finds "SnR:Huddle"

#### 5. **By Attendee Name** (People Invited)
- Search by name: "Eddie", "Wilson Ang", "John Hor"
- Use first name, last name, or abbreviations: "Ed" finds "Eddie"
- Names are fuzzy-matched to handle variations

#### 6. **By Email Address** (Attendee Emails)
- Full or partial emails: "eddie@sentient.io", "sentient.io", "mani@"
- Searches attendee email list

### Combining Criteria (AND Logic)

Combine multiple search dimensions to narrow results:
- Date + Attendee: "Show me events with Eddie on Monday"
- Subject + Week: "Find all 'standup' meetings this week"
- Subject + Attendee + Date: "'SnR:Huddle' with John on Friday"
- Multiple attendees: "Events with Eddie and Mani next week"

### Implementation Strategy

When searching calendars, Claude should:

1. **Parse the user query** to identify:
   - Time reference (day, date, week)
   - Subject/keywords
   - Attendee names or emails

2. **Use Google Calendar tools** to:
   - Get list of calendars accessible using `list_gcal_calendars`
   - Retrieve events for the identified time range using `list_gcal_events`
   - Filter by subject, attendees, and other criteria

3. **Enrich each event** with:
   - Precise start/end times in Asia/Singapore timezone (ISO 8601 format)
   - Duration calculation (end_time - start_time in minutes)
   - Prep time indicator based on:
     * Presence of Drive links in description
     * Number of attendees (>5 = needs prep)
     * Attachments or conferenceData
   - Full event description (no truncation)
   - Conferencing details extracted from event data

4. **Format results** with:
   - Event title and time (with explicit timezone)
   - Duration in minutes
   - Location
   - Full attendee list with email addresses and RSVP status
   - Link to the calendar event
   - Description (if present)
   - Prep needed flag
   - Conference link (if present)

5. **Apply filtering logic**:
   - Exclude cancelled events
   - Include all other event statuses (accepted, tentative, needs action, declined)
   - Limit to 50 most recent results
   - Sort by start time (chronological order for briefings)

### Natural Language Processing

Claude should understand:
- Flexible phrasing: "What's on my calendar?" vs "Show me my events"
- Fuzzy matching: "Wil" for "Wilson", "Ed" for "Eddie"
- Multiple date formats naturally
- Partial information: "meetings with sentient.io" or just "Eddie" without full context
- Relative time references: "this week", "next Monday", "last Friday"

### Event Enrichment Logic

After retrieving events from `list_gcal_events`, Claude must enrich each event:

**1. Duration Calculation:**
```
duration_minutes = (end_time - start_time).total_seconds() / 60
```

**2. Prep Time Detection - Set `prep_needed: true` if:**
- Description contains: `docs.google.com/document`, `docs.google.com/spreadsheets`, `docs.google.com/presentation`, `drive.google.com`
- Description contains keywords: `agenda`, `review`, `presentation`, `proposal`, `deck`
- Attendee count > 5
- Event has `attachments` or `conferenceData` fields

**3. Conference Link Extraction:**
- Check `conferenceData.entryPoints` for video conference URLs
- Fallback: Search description for `meet.google.com`, `zoom.us`, `teams.microsoft.com` links
- Return: `{type: "Google Meet", url: "https://..."}`

**4. Timezone Conversion:**
- Convert all event times to Asia/Singapore timezone (UTC+8)
- Format as ISO 8601: `2025-10-26T14:30:00+08:00`

**Reference:** See `/mnt/skills/user/search-calendar/search_calendar_helper.py` for example implementations of:
- `calculate_duration(start, end)` 
- `needs_prep_time(event)`
- `extract_conference_link(event)`

## Examples

### Example 1: Today's Events
**User:** "Show me my calendar for today"

**Claude should:**
1. Get current date
2. Use `list_gcal_events` to retrieve events for today from all accessible calendars
3. Enrich each event with duration, prep indicators, timezone conversion
4. Format and display them

### Example 2: Events with Specific Person
**User:** "Find all meetings with Eddie this week"

**Claude should:**
1. Identify time range: this week (Monday-Sunday)
2. Use `list_gcal_events` to query all calendars for events in that range
3. Filter for events where "Eddie" is an attendee (fuzzy match on attendee names)
4. Enrich each event with duration, prep indicators, conference links
5. Return matching events with full details

### Example 3: Subject + Attendee + Date
**User:** "Show me 'SnR:Huddle' meetings with John Hor next week"

**Claude should:**
1. Identify time range: next week
2. Use `list_gcal_events` to query calendars for events with "Huddle" or "SnR" in title
3. Filter for events where "John Hor" is invited
4. Enrich events with prep indicators, duration, conference links
5. Return combined results

### Example 4: Email-based Search
**User:** "What meetings do I have with people from sentient.io?"

**Claude should:**
1. Use `list_gcal_events` to query recent events (default: next 30 days)
2. Filter for events with attendees having @sentient.io email
3. Enrich events with all additional context
4. Return matching events

## Important Guidelines

### Timezone Handling (CRITICAL for briefings)
- **ALL timestamps MUST be returned in Asia/Singapore timezone (SGT / UTC+8)**
- Use ISO 8601 format with explicit timezone: `2025-10-26T14:30:00+08:00`
- Never return times without timezone information
- Ensure consistency across all events for time-based sorting and briefing integration
- If user is in different timezone, convert display times but maintain SGT in data structure

### Time Ranges
- **Day-based search**: Search that specific 24-hour period
- **Week-based search**: Search Monday through Sunday of that calendar week
- **Date-based search**: Search that specific date
- **No time specified**: Default to next 30 days for open searches

### Attendee Matching
- Use fuzzy matching for names (70% similarity threshold)
- Handle partial names and nicknames
- For emails: support partial matches (e.g., "eddie@" matches "eddie@sentient.io")
- Match against all visible attendees, not just organizer

### Event Status
- **Always exclude**: Cancelled events
- **Always include**: All other statuses (Accepted, Tentative, Declined, Needs Action)
- Display attendee RSVP status when listing events

### Result Limits
- Return maximum 50 events per search
- Show newest/most recent first
- Include full details: title, time, location, attendees, calendar link

### Enriched Event Data (for briefing integration)
- **Duration**: Calculate and return event duration in minutes
- **Prep Time Indicator**: Set `prep_needed: true` if event has:
  - Description containing Drive links (docs.google.com/document, docs.google.com/spreadsheet, etc.)
  - Description containing meeting agendas or action items
  - Attachments (check for conferenceData or attachments in event)
  - More than 5 attendees (larger meetings typically need prep)
- **Descriptions**: Always include event descriptions by default (don't truncate)
- **Attendee Context**: Include full attendee list with emails and response status
- **Conferencing**: Extract and return video conference links (Meet, Zoom, Teams, etc.)

## Tips for Better Results

1. **Be specific**: Include attendee names or subjects when possible to narrow results
2. **Use natural dates**: "next Monday" works better than calculating dates manually
3. **Combine criteria**: Rather than "all my meetings with Eddie", use "Eddie next week" for faster results
4. **Verify attendee names**: If unsure of spelling, use nicknames - fuzzy matching handles it

## Handling Edge Cases

**Multiple people with similar names:**
- Display all matches and ask user to clarify if needed
- Show email addresses to help distinguish

**Events without attendees:**
- Include in results when subject matches
- Mark "No attendees" or "Private" if applicable

**All-day events:**
- Include in results
- Display as "All day" rather than specific times

**Recurring events:**
- Return individual instances for the date range queried
- Show the full series context if available

**No results:**
- Explain why no events were found
- Suggest broadening the search (e.g., "try searching all week instead of just Monday")

## Integration with Other Tools

This skill works with Claude's existing calendar tools and can be combined with:
- **Email searches** (find emails about specific meetings) - use `recent-emails` with aligned timestamps
- **Document searches** (find prep materials) - use `work-day-files` to locate meeting-related documents
- **Task management** (create tasks from meeting discussions)
- **Daily briefings** - provides the timeline anchor for time-based organization

### Briefing Integration (Primary Use Case)

This skill is optimized to serve as the **timeline anchor** for daily briefings:

1. **Timestamp Alignment**: All events return precise start/end times in Asia/Singapore timezone matching the format used by `recent-emails` and `work-day-files`

2. **Prep Time Intelligence**: The `prep_needed` flag helps briefings surface:
   - Events requiring document review (Drive links in description)
   - Large meetings (>5 attendees)
   - Events with attachments or agendas

3. **Contextual Linking**: When building briefings:
   - Check if recent emails (from `recent-emails`) are from meeting attendees
   - Check if recent file modifications (from `work-day-files`) relate to meeting topics
   - Flag "action items" by correlating email subjects with event titles

4. **Time-Based Output**: Sort events chronologically to create a clear timeline that other briefing components can reference

**Example Briefing Flow:**
```
08:00 - Check work-day-files for documents modified overnight
09:00 - Morning standup (from search-calendar) 
        ↳ prep_needed: true (has agenda doc)
        ↳ Related file: "Standup Notes 2025-10-26.docx" modified at 08:30
10:00 - Review recent-emails for urgent items from standup attendees
14:00 - Client meeting (from search-calendar)
        ↳ prep_needed: true (>5 attendees)
        ↳ Related email: "Q4 Proposal" from client@example.com at 13:45
```

## Security and Privacy

- Search only calendars the user has read access to
- Don't expose private event details beyond what the user authorized
- Respect calendar sharing permissions
- Only display information the user can see

## Troubleshooting

**"No calendars found"**
- User may need to grant calendar access
- Verify Google Calendar permissions

**"No events matching"**
- Try broader search terms
- Check spelling of names/subjects
- Extend date range

**"Wrong person matched"**
- For ambiguous names, ask user to clarify
- Use email addresses for specific identification
- Provide full names in results to avoid confusion

---

## Quick Start for Claude

When a user asks about their calendar:

1. **Parse their request** for: **time** (when), **subject** (what), **people** (who)

2. **Use calendar tools** to fetch events:
   - `list_gcal_calendars` to get available calendars
   - `list_gcal_events` with appropriate date range filters

3. **Enrich each event** with:
   - Duration calculation (in minutes)
   - Prep time indicator (Drive links, >5 attendees, attachments, keywords)
   - Conference link extraction (Meet, Zoom, Teams)
   - Ensure timestamps are in Asia/Singapore timezone (SGT/UTC+8)

4. **Apply intelligent filtering** based on all criteria provided:
   - Attendee name matching (fuzzy)
   - Email domain filtering
   - Subject/title matching

5. **Format results clearly** with:
   - Event details with explicit SGT timestamps
   - Duration, prep indicators, conference links
   - Full attendee context with RSVP status
   - Calendar event links

6. For unclear queries, ask clarifying questions

**Reference Implementation:** The `search_calendar_helper.py` file contains example code for the enrichment logic (duration calculation, prep time detection, conference link extraction). Claude can reference these functions when implementing the enrichment steps.

The skill is designed to be conversational - Claude should handle natural language calendar queries without requiring specific syntax or complex instructions from the user.
```