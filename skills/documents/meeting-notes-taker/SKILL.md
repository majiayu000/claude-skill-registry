---
name: Meeting Notes Taker
slug: meeting-notes-taker
description: Summarize meetings into clear, actionable notes with decisions and next steps
category: communication
complexity: simple
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "take meeting notes"
  - "summarize meeting"
  - "meeting recap"
  - "meeting minutes"
tags:
  - meetings
  - notes
  - documentation
  - action-items
---

# Meeting Notes Taker

The Meeting Notes Taker skill transforms meeting discussions into clear, structured, actionable documentation. Whether you're summarizing a quick standup, a client call, a strategy session, or a board meeting, this skill ensures key decisions, action items, and context are captured and communicated effectively.

This skill creates meeting notes that are scannable, searchable, and useful. It separates signal from noise, highlighting what matters: decisions made, actions assigned, and critical discussion points. The format makes it easy for attendees to remember what was discussed and for non-attendees to catch up quickly.

Good meeting notes save time, reduce confusion, and ensure accountability. This skill makes creating them fast and consistent, so they actually get done instead of being skipped.

## Core Workflows

### Workflow 1: Real-Time Meeting Notes
1. **Capture Key Points**: Record decisions, action items, and important discussion points
2. **Structure as You Go**: Organize into sections during the meeting
3. **Tag Owners**: Assign action items to specific people
4. **Note Parking Lot**: Capture off-topic items for later
5. **Quick Review**: Scan for completeness before ending meeting

### Workflow 2: Post-Meeting Summary
1. **Review Recording/Notes**: Process meeting content
2. **Extract Key Elements**: Identify decisions, actions, blockers
3. **Structure Document**: Organize into standard format
4. **Add Context**: Include relevant links and references
5. **Distribute**: Share with attendees and stakeholders

### Workflow 3: Recurring Meeting Template
1. **Define Meeting Type**: Understand regular format and goals
2. **Create Template**: Build reusable structure
3. **Include Standard Sections**: Pre-populate recurring agenda items
4. **Add Guidelines**: Note what to capture in each section
5. **Iterate**: Improve template based on team feedback

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Create meeting notes | "Take notes for [meeting type/topic]" |
| Summarize discussion | "Summarize the meeting about [topic]" |
| Extract action items | "Pull out action items from meeting" |
| Create template | "Build meeting notes template for [recurring meeting]" |
| Format raw notes | "Structure these meeting notes: [paste]" |
| Quick recap | "Quick meeting recap with key points" |
| Decision log | "Document decisions from meeting" |
| Share summary | "Create shareable meeting summary" |

## Meeting Note Structure

### Standard Format
```markdown
# [Meeting Title]

**Date:** [Date]
**Time:** [Start - End Time]
**Attendees:** [Names/Roles]
**No-shows:** [If relevant]

## Purpose
[One sentence: Why we met]

## Key Decisions
- Decision 1 [Owner if applicable]
- Decision 2
- Decision 3

## Action Items
- [ ] Action 1 (@Owner - Due: Date)
- [ ] Action 2 (@Owner - Due: Date)
- [ ] Action 3 (@Owner - Due: Date)

## Discussion Highlights
### [Topic 1]
- Key point
- Key point

### [Topic 2]
- Key point
- Key point

## Blockers/Concerns
- Issue 1 [Owner to resolve]
- Issue 2

## Next Meeting
- **Date/Time:** [When]
- **Agenda:** [Key topics]

## Parking Lot
- Item to revisit later
- Off-topic item for different discussion
```

## Meeting Type Templates

### Template 1: Sprint Planning
```markdown
# Sprint [X] Planning

**Sprint Duration:** [Start Date] - [End Date]
**Team:** [Team Name]
**Sprint Goal:** [One sentence goal]

## Committed Stories
- [TICKET-123] Story title (X points) - @Owner
- [TICKET-124] Story title (X points) - @Owner

**Total Points:** X
**Team Capacity:** Y

## Risks
- Risk 1 [Mitigation plan]
- Risk 2

## Carry Over from Last Sprint
- [TICKET-100] Reason for carry-over

## Action Items
- [ ] Action (@Owner - Due)
```

### Template 2: Standup/Daily Sync
```markdown
# [Team] Standup - [Date]

## @Person1
**Yesterday:** Completed X, worked on Y
**Today:** Plan to finish Y, start Z
**Blockers:** None

## @Person2
**Yesterday:** [Updates]
**Today:** [Plans]
**Blockers:** [Issues]

## Team Updates
- Update 1
- Update 2

## Action Items
- [ ] Action (@Owner)
```

### Template 3: Client Meeting
```markdown
# [Client Name] - [Topic]

**Date:** [Date]
**Attendees:**
- [Client]: [Names]
- [Our Team]: [Names]

## Meeting Purpose
[Why we met]

## Client Needs/Requests
- Request 1
- Request 2

## Our Recommendations
- Recommendation 1
- Recommendation 2

## Decisions Made
- Decision 1
- Decision 2

## Next Steps
- [ ] Action 1 (@Owner - Due: Date)
- [ ] Action 2 (@Owner - Due: Date)

## Follow-up Items
- Item to address in next meeting

## Next Meeting
**Scheduled:** [Date/Time]
**Agenda:** [Topics]
```

### Template 4: Retrospective
```markdown
# Sprint [X] Retrospective

**Date:** [Date]
**Team:** [Team Name]

## What Went Well 🎉
- Win 1
- Win 2
- Win 3

## What Could Be Better 🤔
- Issue 1
- Issue 2
- Issue 3

## Action Items for Next Sprint
- [ ] Experiment/Change 1 (@Owner)
- [ ] Experiment/Change 2 (@Owner)

## Appreciation Shoutouts 👏
- @Person for [contribution]
- @Person for [contribution]
```

### Template 5: Strategy/Planning Session
```markdown
# [Strategy Topic] Planning

**Date:** [Date]
**Participants:** [Names]

## Context
[Background and why we're planning this]

## Goals
1. Goal 1
2. Goal 2
3. Goal 3

## Key Decisions
- Decision 1 [Rationale]
- Decision 2 [Rationale]

## Options Considered
**Option A:** [Description]
- Pros: X, Y
- Cons: A, B

**Option B:** [Description]
- Pros: X, Y
- Cons: A, B

**Selected:** [Option] because [reasoning]

## Timeline
- Milestone 1 (Date)
- Milestone 2 (Date)
- Milestone 3 (Date)

## Resources Needed
- Resource 1
- Resource 2

## Action Items
- [ ] Action (@Owner - Due)

## Open Questions
- Question 1 (Owner to research)
- Question 2
```

## Best Practices

- **Capture Live**: Take notes during the meeting, not after
- **Focus on Outcomes**: Decisions and actions matter more than full transcripts
- **Be Specific**: "John will update the docs by Friday" not "Someone should update docs"
- **Use Consistent Format**: Same structure for same meeting types
- **Distribute Quickly**: Share notes within 24 hours, ideally within hours
- **Tag Clearly**: Use @mentions so people see their action items
- **Link Resources**: Add URLs to relevant docs, tickets, designs
- **Separate Parking Lot**: Don't lose good ideas that are off-topic
- **Review Before Sharing**: Quick sanity check for completeness
- **Archive Properly**: Store where team can search and reference

## Effective Action Item Format

Good action items are:
- **Specific**: Clear what needs to be done
- **Assigned**: One owner (not multiple)
- **Time-bound**: Clear due date or time frame
- **Actionable**: Verb-based, concrete task

| ❌ Bad | ✅ Good |
|--------|---------|
| "Think about the redesign" | "Review 3 design options and share feedback in #design by Wednesday (@Sarah)" |
| "Someone should fix the bug" | "Fix login timeout bug [TICKET-456] by end of sprint (@Mike)" |
| "Update docs" | "Add API authentication section to developer docs by Jan 15 (@Alex)" |
| "Follow up with client" | "Send contract revision to Acme Corp by EOD Friday (@Jordan)" |

## Decision Documentation

When capturing decisions:
1. **State the Decision**: What was decided
2. **Provide Context**: Why it matters
3. **Note Alternatives**: What else was considered
4. **Record Rationale**: Why this option was chosen
5. **Identify Owner**: Who's responsible for implementation

Example:
```markdown
**Decision:** We're moving forward with PostgreSQL for the new analytics database.

**Context:** Current MySQL setup can't handle the query complexity we need.

**Alternatives Considered:**
- MongoDB: More scalable but team lacks expertise
- MySQL optimization: Would buy time but not solve long-term needs

**Rationale:** PostgreSQL offers better JSON support and complex queries while keeping relational benefits. Team has 2 engineers with deep PostgreSQL experience.

**Owner:** @Database team to lead migration (target: Q2 2026)
```

## Meeting Types Best Practices

### Standup/Daily Sync
- Keep it to 15 minutes or less
- Focus on blockers that need team help
- Save detailed discussions for after
- Update async if status is "more of the same"

### Sprint Planning
- Capture the "why" behind story selection
- Document capacity and velocity
- Note dependencies between stories
- Record any scope trade-offs made

### Retrospectives
- Balance positives and negatives
- Focus on actionable improvements
- Avoid blame - focus on systems
- Limit action items to 2-3 that can actually be done

### Client Meetings
- Capture exact client requests verbatim when important
- Note tone and sentiment, not just facts
- Document commitments made carefully
- Set clear expectations for follow-up

### 1:1s
- Keep notes private between participants
- Focus on career growth and feedback
- Track progress on long-term goals
- Note action items for manager and report

## Common Pitfalls to Avoid

- **Verbatim Transcripts**: Capture signal, not noise
- **Missing Owners**: Every action item needs one person responsible
- **Vague Actions**: "Follow up" isn't an action item
- **No Due Dates**: Without deadlines, actions don't happen
- **Waiting to Write**: Notes written days later are incomplete
- **Over-Structuring**: Let format serve content, not constrain it
- **Not Sharing**: Notes only help if people see them
- **No Follow-Through**: Review previous action items at start of next meeting

## Distribution & Storage

### Where to Share
- **Slack/Teams**: Quick summary with link to full notes
- **Email**: Formal meetings or external stakeholders
- **Project Management Tool**: Link to related epics/tickets
- **Wiki/Docs**: Permanent storage and searchability

### Template Sharing Message
```
📝 Meeting Notes: [Meeting Title]

Key takeaways:
• Decision 1
• Decision 2

Action items:
• Action 1 (@Owner - Due)
• Action 2 (@Owner - Due)

Full notes: [Link]

Questions? Drop them in the thread 👇
```

## Integration Points

- **Calendar**: Link to meeting invite and future meetings
- **Project Management**: Connect to related tickets, epics, sprints
- **Documentation**: Reference relevant wiki pages, specs, designs
- **Recording**: Link to video recording if available
- **Slides**: Attach presentation decks discussed
- **Chat Threads**: Link to relevant Slack/Teams discussions

## Follow-Up Best Practices

- **Next Meeting Check-In**: Review previous action items at start
- **Mid-Week Reminder**: Ping owners of due-this-week items
- **Decision Log**: Maintain running log of major decisions
- **Archive Searchably**: Use consistent naming and tags
- **Update Project Status**: Reflect decisions in project tracking tools
