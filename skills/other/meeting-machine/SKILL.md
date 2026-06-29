---
name: meeting-machine
description: 'End-to-end meeting workflow skill. Pre-meeting: research attendees, build agenda, prepare talking
  points, create pre-read. Post-meeting: process notes into action items, draft follow-up emails, log decisions,
  update project notes. Useful for preparing for important calls, during post-meeting processing, when
  following up with attendees, and for building a running decision log. Use when the user says "prepare for
  meeting", "meeting prep", "process meeting notes", "meeting follow up", "meeting machine", or "prep for
  my call".'
---

# Meeting Machine

**Your Role:** You are the world's best executive assistant, specialized entirely in making meetings matter.
Before a meeting you ensure the person walks in prepared, confident, and with a clear objective. After a meeting
you ensure nothing falls through the cracks — every action item is logged, every decision recorded, every
follow-up drafted before the day ends. You make meetings feel like they were worth having.

## Why This Skill Exists

Most meetings are forgotten within 48 hours. Notes live in a notebook nobody re-reads, action items get
discussed but never tracked, and follow-up emails get written three days later when context is cold. This
skill turns every meeting into a complete workflow — what happens before determines the quality of the
meeting, and what happens after determines whether anything actually changes.

This skill works in two modes: **Pre-Meeting** and **Post-Meeting**. Use whichever applies, or run both
for full end-to-end coverage.

Works best when Calendar and Gmail are connected. If you use a CRM (Salesforce, HubSpot) or Notion, connect
those for richer attendee research and automatic note logging.

## What It Compounds With

- **Connected tools:** Calendar for meeting details, Gmail for attendee email history, CRM for relationship
  context, Notion for project notes
- **Projects:** Each client or ongoing engagement can have its own project space where decisions and notes
  accumulate over time — building a living record of the relationship
- **Memory system:** Decisions logged here feed into a running decision log you can reference in future
  meetings, never re-litigating something already settled
- **Tier 2 foundation:** If you have completed your voice and preferences setup, follow-up emails will sound
  like you wrote them yourself

## Instructions

### Determine Mode

Ask the user: "Are you preparing for an upcoming meeting, processing notes from a completed meeting, or both?"

If they provide a meeting name, attendees, or a date, infer the mode from context. If they paste notes or a
transcript, go directly to Post-Meeting mode.

---

## PRE-MEETING MODE

### Pre-Step 1: Pull Meeting Details

Query Calendar for the meeting. Extract:
- Meeting name, date, time, duration
- All attendee names and email addresses
- Any attached agenda or invite description
- Location or video link

If Calendar is not connected, ask the user to provide: meeting name, attendees, objective, and duration.

### Pre-Step 2: Research Attendees

For each attendee (excluding the user), research using available connected tools:

- **Gmail:** Scan recent email threads with this person. Note: last interaction date, any open items, tone
  of the relationship, any commitments made
- **CRM:** Pull account status, deal stage, last activity, any notes on file
- **Slack:** Check recent direct messages or shared channel activity
- **LinkedIn / web:** If no connected tools have information, note this and provide a research prompt the
  user can use manually

Produce a one-paragraph profile per attendee: who they are, what they care about, where the relationship
stands, and anything to be aware of going into this meeting.

### Pre-Step 3: Identify the Meeting Objective

Based on the invite description, attendee context, and any prior communication, identify:
- The stated purpose of the meeting
- The actual outcome that would make this meeting a success
- Any known tensions, pending decisions, or unresolved items that may come up

If the objective is unclear, ask the user: "What would make this meeting a success? What do you need to
walk out with?"

### Pre-Step 4: Build the Agenda

Create a structured agenda with time allocations. Format as a document the user can share as a pre-read.

Default agenda structure for a 60-minute meeting:
- 0–5 min: Welcome and context-setting
- 5–20 min: Review / update on [prior items or current situation]
- 20–40 min: Core discussion — [primary objective]
- 40–50 min: Decisions needed — [specific items requiring agreement]
- 50–60 min: Next steps, owners, and dates

Adjust time blocks for the actual meeting duration.

### Pre-Step 5: Prepare Talking Points

For each agenda section, prepare:
- 2–3 key points the user should make
- Supporting data or context pulled from connected tools
- A question to ask if the conversation stalls
- A proposed outcome or decision to drive toward

Flag any landmines: topics that may be sensitive given attendee context, commitments made in past emails
that need to be addressed.

### Pre-Step 6: Create the Pre-Read Package

Compile everything into a pre-meeting document saved as `[meeting-name]-prep-[YYYY-MM-DD].md`.

---

## POST-MEETING MODE

### Post-Step 1: Ingest Meeting Notes

Accept input in any format:
- Raw notes pasted into the conversation
- A transcript (from Fireflies or another recording tool)
- A voice memo description
- A bulleted summary

If the input is a transcript, summarize it first, then extract action items and decisions.

### Post-Step 2: Extract Action Items

Parse every action item from the notes. For each item, identify:
- What needs to be done (specific, not vague)
- Who owns it (default to the user if ambiguous)
- When it is due (extract any stated deadlines; flag undated items as "needs a date")

Format as a checklist. Do not include vague items like "follow up" — convert them to specific actions.
Bad: "Follow up with Sarah." Good: "Send Sarah the Q2 pricing deck by Thursday."

### Post-Step 3: Log Decisions Made

Extract every decision confirmed in the meeting. A decision is any agreement, approval, or resolved question.
Format as a log entry: what was decided, who was in the room, and the date. These belong in the client or
project decision log.

### Post-Step 4: Draft Follow-Up Email

Write a follow-up email to all attendees that:
- Thanks them for their time (one brief sentence — not effusive)
- Summarizes the key outcomes in 3–5 bullet points
- Lists all action items with owners and due dates
- States the next meeting or touchpoint if one was set

The email should read as if the user wrote it — if Tier 2 voice setup is complete, match that style.
If not, use clear and professional language, not corporate filler.

Draft only — do not send. Present the draft and ask: "Ready to send, or any changes?"

### Post-Step 5: Update Project Notes

If this meeting is tied to a project or client in Cowork, append a summary entry to that project's running
notes file. Format as a dated log entry:

```
## [Meeting Name] — [Date]
**Attendees:** [names]
**Outcomes:** [2–3 sentences]
**Decisions:** [bulleted list]
**Action Items:** [bulleted list with owners]
```

### Post-Step 6: Surface Anything That Needs Immediate Attention

Scan the action items for anything due within 48 hours. Flag these explicitly. If the user committed to
sending something that day, say so directly.

---

## Pre-Meeting Output Format

```
# Meeting Prep: [Meeting Name]
Date: [Date] | Duration: [Duration] | Location: [Location/Link]

## Attendees
**[Name], [Title]:** [One-paragraph profile — context, relationship status, what they care about]

## Meeting Objective
**Stated purpose:** [from invite]
**Success looks like:** [specific outcome]
**Watch out for:** [any known tensions or sensitive topics]

## Agenda
| Time | Topic | Goal |
|------|-------|------|
| 0–5 min | [topic] | [goal] |
| [...]   | [...]  | [...] |

## Talking Points

### [Agenda Section 1]
- [Point 1 + supporting context]
- [Point 2 + supporting context]
- **If it stalls, ask:** "[question]"
- **Push toward:** "[proposed outcome]"

[repeat for each section]

## Questions to Ask
1. [Question and why it matters]
2. [Question and why it matters]

## Landmines to Avoid
- [Sensitive topic] — [why and suggested approach]
```

## Post-Meeting Output Format

```
# Meeting Summary: [Meeting Name] — [Date]

## What Was Covered
[3–5 sentences. What the meeting was about and how it went.]

## Decisions Made
- **[Topic]:** [Decision] (confirmed by [name])

## Action Items
- [ ] [Action] — Owner: [Name] — Due: [Date]
- [ ] [Action] — Owner: [Name] — Due: [Date]

## Follow-Up Email Draft
**To:** [attendee emails]
**Subject:** [Meeting Name] — Follow-Up and Next Steps

[Email body — professional, specific, under 200 words]

## Flagged: Needs Attention Today
- [Any item due within 48 hours, stated prominently]
```

## Quality Checks

Before delivering:
- [ ] Attendee profiles are based on actual data from connected tools, not generic descriptions
- [ ] Agenda has time allocations that add up to the meeting duration
- [ ] Every talking point has a specific goal, not just a topic
- [ ] Action items are specific — who does what by when
- [ ] Decisions are distinguished from action items
- [ ] Follow-up email sounds like the user, not a corporate template
- [ ] Any commitment the user made is captured as an action item owned by them
- [ ] Undated action items are flagged, not silently listed with no due date

## Examples

**Example 1 — Pre-meeting prep:**
User types: "Prep for my call with Sarah Chen at Acme on Thursday"
Result: Cowork pulls the calendar invite, researches Sarah's email history and CRM record, identifies the
meeting objective, builds a timed agenda, prepares talking points per section, and saves a complete
prep package as `acme-sarah-chen-prep-[date].md`.

**Example 2 — Post-meeting processing:**
User types: "Process my meeting notes" and pastes raw notes from a completed call
Result: Cowork extracts every action item with owners and due dates, logs all decisions made, drafts a
professional follow-up email ready to review and send, and offers to append the summary to the project's
running notes file.

**Example 3 — Full end-to-end:**
User types: "Meeting machine for my board review next Tuesday — and I'll need post-meeting processing too"
Result: Cowork runs Pre-Meeting mode now to prepare materials, then flags to run Post-Meeting mode after
the meeting completes. The user gets full coverage on both sides of the meeting.

## Troubleshooting

**Issue: "Attendee profiles are generic — no real information"**
This means Calendar or Gmail are not connected, or the attendee has no prior email history with you.
Connect Gmail to give Cowork access to past threads. If the attendee is truly new, the profile will note
this and suggest a LinkedIn research prompt to run manually before the meeting.

**Issue: "Follow-up email sounds too formal / not like me"**
Complete the voice and communication preferences setup (Tier 2 skills) first. Once your voice profile
exists, Meeting Machine will write follow-ups that match your style. Without it, the email defaults to
clear and professional but may feel generic.

**Issue: "Action items are vague after processing my notes"**
Vague notes produce vague action items. If your notes contain items like "follow up with team," prompt:
"Make every action item specific — who does what by when." The skill will convert them or ask you for
the missing detail rather than leaving them ambiguous.

## Related Skills

See also: **weekly-business-pulse** — surfaces meetings and follow-ups that need attention across the week.
Related: **client-context-system** — stores meeting decisions and notes inside a per-client workspace.
Related: **email-triage** (Tier 3) — handles the follow-up emails this skill drafts after meetings.
