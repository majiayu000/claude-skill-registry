---
name: meeting-scheduler
description: "Schedules meetings with internal and external stakeholders by parsing natural language requests, resolving time zones, checking calendar availability, proposing optimal slots, and managing invitations and RSVPs. Use when the user requests meeting scheduler or provides relevant inputs for this workflow."
license: "MIT"
metadata:
  author: "awesome-ai-agent-skills contributors"
  version: "1.1.0"
---

# Meeting Scheduler

This skill enables an AI agent to handle end-to-end meeting coordination. Given a natural language request, the agent identifies participants, resolves time zone differences, queries calendar availability, proposes conflict-free time slots, dispatches calendar invitations, and tracks RSVPs. It integrates with Google Calendar, Microsoft Outlook, and Calendly to cover the most common enterprise and freelance scheduling workflows.

## Workflow

1. **Parse the Meeting Request**
   Extract structured data from the user's natural language input. Identify all required participants (by name, email, or team alias), the meeting topic or agenda, the desired duration, and any date or time constraints such as "next Tuesday afternoon" or "before end of sprint." Flag any ambiguous references for clarification before proceeding.

2. **Resolve Time Zones**
   Look up each participant's configured time zone from their calendar profile or contact record. Convert all proposed windows into each participant's local time so that comparisons are accurate. When a participant's time zone is unknown, prompt the organizer to confirm it. Display all suggested times with explicit time zone labels (e.g., "3:00 PM EST / 12:00 PM PST") to avoid confusion.

3. **Check Calendar Availability**
   Query each participant's calendar through the appropriate integration (Google Calendar API, Microsoft Graph API, or Calendly availability endpoint). Collect busy blocks for the requested date range and compute the intersection of free windows. Respect each participant's working-hours preferences and any configured focus-time or no-meeting blocks. Apply a configurable buffer (default 10 minutes) between adjacent meetings to allow transition time.

4. **Propose Optimal Time Slots**
   Rank the available windows using a scoring heuristic: prefer slots that fall within standard working hours for all participants, minimize the number of early-morning or late-evening local times, and favor earlier dates when urgency is indicated. Present the top three ranked options to the organizer with a summary showing each participant's local time.

5. **Send Calendar Invitations**
   Once the organizer confirms a slot, create the calendar event via the appropriate API. Attach the agenda, video-conferencing link (Zoom, Google Meet, or Teams), and any relevant documents. Send invitation emails to all participants. For external participants without calendar integration, send a standalone email with an `.ics` attachment.

6. **Track RSVPs and Handle Changes**
   Monitor invitation responses as they arrive. Notify the organizer of acceptances, tentative replies, and declines. If a critical participant declines, automatically propose alternative slots from the remaining availability and initiate a rebooking flow. For recurring meetings, track attendance patterns and flag consistently conflicting participants so the organizer can adjust the cadence.

## Usage

Provide a natural language request that includes the participants, topic, approximate duration, and any scheduling constraints. The agent will handle the rest.

```
"Schedule a 30-minute meeting with John and Jane to discuss the Q3 report sometime next week. Prefer mornings."
```

You can also ask for recurring meetings, rescheduling, or cancellations:

```
"Reschedule tomorrow's design review to Thursday. Same time if possible, otherwise find a new slot."
```

```
"Set up a weekly 15-minute standup with the backend team every Monday at 9:30 AM ET starting next week."
```

## Examples

### Example 1 — Cross-Timezone Meeting with Availability Matrix

**User input:**
```
"Schedule a 1-hour architecture review with Priya (IST), Marcus (CET), and Li (CST, China) this Thursday or Friday. Avoid early mornings for everyone."
```

**Agent output:**
```
I checked calendars for Priya, Marcus, and Li. Here is the availability matrix:

                        Priya (IST)    Marcus (CET)    Li (CST)
Thu 10:00–11:00 UTC     3:30 PM        11:00 AM        6:00 PM
Thu 12:00–13:00 UTC     5:30 PM        1:00 PM         8:00 PM ⚠️
Fri 09:00–10:00 UTC     2:30 PM        10:00 AM        5:00 PM  ✅ Best

Recommended: Friday 09:00–10:00 UTC
 — Falls within working hours for all three participants.
 — No conflicts detected.

Shall I send the invitation for Friday 09:00–10:00 UTC with a Google Meet link?
```

### Example 2 — Rescheduling with Conflict Resolution

**User input:**
```
"The Wednesday product sync conflicts with Alice's dentist appointment. Move it to another day this week. Bob and Carol also attend."
```

**Agent output:**
```
Current meeting: Wednesday 2:00–2:30 PM ET (Alice, Bob, Carol)

Alice is unavailable Wednesday 1:00–4:00 PM ET (personal appointment).
Bob is unavailable Thursday all day (PTO).
Carol has no additional conflicts this week.

Available alternatives:
  1. Tuesday  2:00–2:30 PM ET  — all three free ✅
  2. Friday   10:00–10:30 AM ET — all three free
  3. Friday   3:00–3:30 PM ET  — all three free

Recommendation: Option 1 (Tuesday 2:00 PM ET) keeps the same time of day.

Shall I reschedule to Tuesday and notify all participants?
```

## Best Practices

- **Always display times with time zone labels.** Never present a bare time like "3:00 PM" without specifying the zone. This prevents the most common source of scheduling errors.
- **Include buffer time between meetings.** Default to 10 minutes. Back-to-back meetings cause fatigue and late arrivals. Allow organizers to configure this per-calendar.
- **Respect working-hours boundaries.** Do not propose 7:00 AM or 9:00 PM slots unless the participant has explicitly marked those hours as available.
- **Confirm before sending.** Always present the proposed slot and attendee list to the organizer for approval before dispatching invitations. Automated sends should be opt-in only.
- **Handle external participants gracefully.** When a participant has no connected calendar, fall back to email-based availability polling or attach an `.ics` file they can import manually.
- **Track recurring meeting health.** For recurring events, periodically report attendance rates and suggest cadence changes if attendance drops below a threshold (e.g., 60%).

## Edge Cases

- **No overlapping availability found.** When calendars have no common free window in the requested range, widen the search to the following week and inform the organizer. Alternatively, suggest splitting into two smaller meetings with partial attendance.
- **Unknown or ambiguous time zones.** If a participant's time zone cannot be determined from their profile, ask the organizer to confirm before proposing slots. Never assume a default zone silently.
- **Participant not found.** If a name cannot be resolved to a calendar or email address, list possible matches and ask the organizer to disambiguate.
- **Calendar API rate limits or outages.** If an availability check fails, retry with exponential backoff up to three times. If the service remains unavailable, inform the organizer and offer to try again later or proceed with partial availability data.
- **Last-minute cancellations.** If a participant declines within one hour of the meeting start, notify the organizer immediately and ask whether to proceed, cancel, or reschedule.
- **All-day events and focus blocks.** Treat all-day calendar events as tentative unless they are explicitly marked "busy." Respect focus-time blocks as unavailable by default but allow the organizer to override.
