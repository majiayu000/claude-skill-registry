---
name: Meeting Scheduler
slug: meeting-scheduler
description: Schedule, coordinate, and optimize meetings with agenda creation and follow-up automation
category: project
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "schedule meeting"
  - "set up meeting"
  - "find meeting time"
  - "book meeting"
  - "coordinate meeting"
tags:
  - meetings
  - scheduling
  - coordination
  - calendar
  - productivity
---

# Meeting Scheduler

The Meeting Scheduler skill helps you efficiently schedule, prepare, run, and follow up on meetings. It emphasizes meeting effectiveness: clear purpose, proper preparation, time-boxing, and actionable outcomes. The skill integrates with calendar systems and automates meeting logistics.

This skill excels at finding optimal meeting times across time zones, creating structured agendas, ensuring the right people are invited, facilitating productive discussions, and capturing action items with clear owners.

Meeting Scheduler follows the principle that most meetings should be eliminated, shortened, or replaced with async communication. When meetings are necessary, they should be intentional, prepared, and productive.

## Core Workflows

### Workflow 1: Schedule Effective Meeting

**Steps:**
1. **Validate Meeting Need**
   - Ask: Could this be an email, document, or async update?
   - Is real-time discussion truly necessary?
   - Will this meeting make a decision or move work forward?
   - If NO to above, consider alternatives to meeting

2. **Define Meeting Purpose**
   - Write clear objective: "By end of meeting, we will have [outcome]"
   - Meeting types:
     - **Decision**: Decide on specific options
     - **Brainstorm**: Generate ideas or solutions
     - **Review**: Evaluate work and provide feedback
     - **Planning**: Create plan or roadmap
     - **Sync**: Share updates and align
     - **Learning**: Share knowledge or train

3. **Identify Required Attendees**
   - Who needs to make decisions?
   - Who has critical information?
   - Limit to 8 people or fewer (ideally 3-5)
   - Optional attendees should get notes instead

4. **Choose Duration**
   - Default to 25 or 50 minutes (not 30/60)
   - Leaves buffer between meetings
   - Time-box based on agenda, not availability
   - Shorter is better; respect people's time

5. **Find Optimal Time**
   - Check all attendees' calendars
   - Consider time zones for remote teams
   - Avoid late Friday or early Monday if possible
   - Respect focus time and no-meeting blocks
   - Use scheduling tools: Calendly, Cal.com, or calendar assistant

6. **Create Agenda**
   - List topics with time allocations
   - Include desired outcome for each topic
   - Share pre-read materials 24h in advance
   - Assign facilitator and note-taker
   - Set expectations for preparation

7. **Send Invite**
   - Clear title with meeting type: "DECISION: Q2 Roadmap"
   - Include purpose, agenda, and pre-read in description
   - Add video link (Zoom, Meet, Teams)
   - Send at least 24 hours in advance
   - Confirm critical attendees can join

**Output:** Calendar invite with clear purpose, agenda, and materials.

### Workflow 2: Prepare for Meeting

**As organizer:**
1. Review agenda and materials
2. Prepare any slides or artifacts
3. Confirm attendees are prepared
4. Test video/screen sharing setup
5. Prepare time-keeping mechanism

**As attendee:**
1. Read pre-read materials
2. Prepare questions or input
3. Gather necessary data or context
4. Clear your mind from previous tasks (5 min buffer)

### Workflow 3: Run Effective Meeting

**Opening (2 min):**
- Start on time
- Restate purpose and desired outcome
- Review agenda and time allocations
- Assign note-taker

**During (80% of time):**
- Follow agenda strictly; time-box each topic
- Facilitate discussion; ensure all voices heard
- Capture decisions and action items in real-time
- Park off-topic discussions for later
- Keep energy up; take breaks if > 50 min

**Closing (5 min):**
- Summarize key decisions
- Review action items with owners and dates
- Clarify next steps
- Set follow-up meetings if needed
- End on time or early

**Output:** Meeting notes with decisions and action items.

### Workflow 4: Meeting Follow-Up

**Within 1 hour of meeting:**
1. Share meeting notes with attendees
2. Post action items to project management tool
3. Update relevant documents or systems
4. Send calendar invites for follow-up meetings
5. Notify stakeholders who weren't present

**Within 24 hours:**
- Owners confirm they've seen their action items
- Clarify any ambiguities from notes
- Begin work on action items

**Weekly:**
- Review outstanding action items
- Follow up on delayed items
- Update project tracking

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Schedule meeting | "schedule meeting for [topic]" |
| Find time slot | "find time for [attendees]" |
| Create agenda | "create agenda for [meeting]" |
| Meeting template | "meeting template for [type]" |
| Reschedule | "reschedule [meeting]" |
| Cancel meeting | "cancel [meeting]" |
| Send reminder | "remind attendees about [meeting]" |
| Share notes | "share meeting notes" |
| Track action items | "meeting action items" |

## Best Practices

- **No agenda, no meeting**: Every meeting must have clear agenda shared 24h in advance
- **Default to NO meeting**: Question every meeting; default to async communication
- **Invite only who's essential**: Every person adds coordination cost; be ruthless about attendees
- **Start and end on time**: Respect people's calendars; late start punishes punctual people
- **One topic, one meeting**: Don't mix unrelated topics; keeps meetings focused and efficient
- **Decision meetings need deciders**: Don't schedule decision meetings without decision-makers present
- **Time-box ruthlessly**: When time is up, move on; schedule follow-up if needed
- **Capture in real-time**: Don't rely on memory; document decisions and actions during meeting
- **Assign clear owners**: Every action item needs name and due date, not "team will..."
- **Share notes within 1 hour**: Fast follow-up maintains momentum and clarity
- **Recurring meetings need recurring value**: Review quarterly; cancel if not delivering value
- **Stand-ups should be standing**: 15 min max, standing keeps it brief
- **Make meetings optional when possible**: Trust people to opt-in if they need to be there

## Meeting Types & Templates

### 1. Decision Meeting
**Purpose**: Make specific decision(s)
**Duration**: 25-50 min
**Agenda Template**:
- Context & background (5 min)
- Options analysis (15 min)
- Discussion & questions (15 min)
- Decision & next steps (10 min)

**Required**:
- Pre-read with options and recommendations
- Decision-maker(s) present
- Clear decision criteria

### 2. Brainstorming Session
**Purpose**: Generate ideas for problem/opportunity
**Duration**: 50-90 min
**Agenda Template**:
- Problem definition (5 min)
- Silent idea generation (10 min)
- Idea sharing round-robin (20 min)
- Grouping & discussion (20 min)
- Voting & prioritization (10 min)

**Required**:
- Diverse perspectives
- No criticism during generation
- Capture all ideas

### 3. Sprint Planning
**Purpose**: Plan next sprint's work
**Duration**: 2-4 hours
**Agenda Template**:
- Review velocity & capacity (15 min)
- Set sprint goal (15 min)
- Story review & estimation (90 min)
- Task breakdown (60 min)
- Commitment (15 min)

**Required**:
- Groomed backlog
- Full team present
- Product owner available

### 4. Retrospective
**Purpose**: Reflect and improve
**Duration**: 60 min
**Agenda Template**:
- Set the stage (5 min)
- Gather data (15 min)
- Generate insights (15 min)
- Decide actions (15 min)
- Close (10 min)

**Required**:
- Psychological safety
- Full team participation
- Commit to 1-3 improvements

### 5. 1-on-1
**Purpose**: Manager-report connection and growth
**Duration**: 25-50 min
**Frequency**: Weekly or bi-weekly
**Agenda Template**:
- How are you? (5 min)
- Your topics (15 min)
- My topics (10 min)
- Growth & development (10 min)
- Actions (5 min)

**Required**:
- Report drives agenda
- Consistent schedule
- Private, safe space

### 6. All-Hands
**Purpose**: Company/team updates and alignment
**Duration**: 30-60 min
**Frequency**: Weekly, bi-weekly, or monthly
**Agenda Template**:
- Wins & celebrations (10 min)
- Metrics & progress (10 min)
- Updates from teams (15 min)
- Q&A (15 min)

**Required**:
- Visual slides
- Interactive components
- Recording for async viewing

## Time Zone Coordination

**Tools:**
- World Time Buddy
- Every Time Zone
- Calendar apps with time zone conversion

**Best Practices:**
- Rotate meeting times if spanning many time zones
- Record meetings for those who can't attend live
- Use async for non-urgent updates
- Be explicit: "2 PM EST (11 AM PST, 7 PM GMT)"
- Consider "golden hours" when time zones overlap

**Golden Hours (US team + Europe):**
- 9-11 AM EST / 2-4 PM GMT

**Golden Hours (US West + Asia):**
- 6-8 PM PST / 9-11 AM next day JST

## Action Item Tracking

**Every action item must have:**
- [ ] Clear description of what needs to be done
- [ ] Owner (single person responsible)
- [ ] Due date
- [ ] Success criteria (how do we know it's done?)

**Action Item Template:**
```
[Owner] will [action verb] [deliverable] by [date]

Example:
Sarah will draft API specification document by Friday 3/15
```

**Track in:**
- Meeting notes
- Project management tool (Jira, Linear, Asana)
- Shared document or spreadsheet
- Slack/Discord thread

## Meeting Metrics

Track these to improve meeting culture:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Meeting hours/week | < 30% of work week | Calendar analysis |
| Meetings with agenda | 100% | Audit calendar invites |
| Meetings starting on time | > 90% | Spot checks |
| Meeting satisfaction | > 4/5 | Quick post-meeting survey |
| Action item completion | > 85% | Review at follow-up meetings |
| Canceled/declined meetings | Increasing | Shows critical evaluation |

## Integration Points

- **Calendar APIs**: Google Calendar, Outlook, Cal.com
- **Video conferencing**: Zoom, Google Meet, Microsoft Teams
- **Scheduling tools**: Calendly, Cal.com, Doodle
- **Note-taking**: Notion, Google Docs, Confluence
- **Project management**: Jira, Linear, Asana, GitHub Issues
- **Slack/Discord**: Meeting reminders and action item notifications
