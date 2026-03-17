---
name: meeting-synthesizer
version: 1.0.0
description: |
  Processes meeting notes or transcripts to extract structured information.
  Use after meetings to quickly generate action items, capture decisions, and create follow-up tasks.
  Extracts: action items with owners, decisions made, key discussion points, follow-up tasks with priorities.
---

# Meeting Synthesizer Skill

Transform raw meeting notes and transcripts into actionable intelligence. This skill extracts critical information from unstructured meeting data and organizes it into structured formats that drive follow-through and accountability.

## Overview

The Meeting Synthesizer processes meeting notes or transcripts to produce:

- **Action Items**: Clear tasks with owners, due dates, and context
- **Decisions Made**: Key decisions with justification and implications
- **Discussion Points**: Important topics, debates, and consensus areas
- **Follow-up Tasks**: Prioritized task list with next steps
- **Key Insights**: Patterns, concerns, and emerging themes

## When to Use This Skill

- After team meetings, standups, or planning sessions
- When converting transcript/notes into structured action items
- When you need to quickly extract decisions and assign accountability
- When synthesizing notes for stakeholders who missed the meeting
- When creating task lists from meeting discussions

## How to Use This Skill

### Basic Workflow

1. **Provide the Meeting Content**
   - Share meeting notes (typed or pasted)
   - Share a transcript (from Zoom, Teams, or other platform)
   - Share a voice-to-text transcription

2. **Request Processing**
   - Ask the skill to synthesize the meeting
   - Optionally specify which elements to focus on
   - Optionally provide format preferences (markdown, JSON, etc.)

3. **Review & Act**
   - Review the extracted information
   - Assign owners and deadlines
   - Create tickets or calendar items
   - Share results with team

### Example Prompts

#### Comprehensive Synthesis
```
Synthesize this meeting:
[paste meeting notes/transcript]

Extract all action items, decisions, and key points.
Organize by priority and due date.
```

#### Focused on Action Items
```
Extract action items from this meeting:
[paste meeting notes]

For each action item, provide:
- Task description
- Owner/responsible person
- Due date (if mentioned)
- Context/why it matters
- Dependencies
```

#### Decision Extraction
```
What decisions were made in this meeting?
[paste meeting notes]

For each decision, provide:
- What was decided
- Why (reasoning/justification)
- Who made the decision
- Who is affected
- Any dissent or concerns
```

#### Priority Ordering
```
Synthesize this meeting with priority ordering:
[paste meeting notes]

Order action items by urgency and impact.
Identify any blocking items or critical path items.
Flag any decisions that need follow-up or clarification.
```

## Processing Instructions

### 1. Parse Meeting Content

**Input Recognition:**
- Detect format: structured notes, transcript, bullet points, freeform text
- Identify participants: who attended, who spoke, roles
- Extract timestamps: when discussed (if available)
- Recognize context: meeting type, agenda, goals

**Normalization:**
- Clean up formatting inconsistencies
- Expand abbreviations where possible
- Clarify ambiguous references
- Group related items

### 2. Extract Action Items

**Identification:**
- Look for explicit assignments: "Alice will...", "We need to..."
- Identify implicit tasks: decisions requiring implementation
- Find time-bound items: "by Friday", "next sprint", "ASAP"
- Recognize dependencies: "after X is done"

**Structuring:**
```
Action Item:
  Description: [Clear, specific task]
  Owner: [Person responsible]
  Due: [Date/timeline]
  Context: [Why it matters]
  Dependencies: [What must happen first]
  Priority: [High/Medium/Low]
```

### 3. Identify Decisions

**Detection:**
- Explicit decisions: "We decided to...", "We will..."
- Consensus moments: "Everyone agreed...", "Consensus is..."
- Choices made: "We chose X over Y"
- Direction changes: "We're shifting from X to Y"

**Documentation:**
```
Decision:
  What: [The decision]
  Why: [Reasoning/justification]
  Decided By: [Who decided]
  Affected: [Who is impacted]
  Dissent: [Any concerns/opposition]
  Implementation: [How will it work]
```

### 4. Capture Discussion Points

**Extraction:**
- Main topics discussed
- Debates or different viewpoints
- Open questions or uncertainties
- Agreed-upon principles or approaches

**Organization:**
```
Discussion Point:
  Topic: [What was discussed]
  Viewpoints: [Different perspectives]
  Consensus: [What was agreed]
  Open Issues: [Unresolved items]
```

### 5. Generate Follow-up Tasks

**Identification:**
- Clarification needed: "We should confirm with X"
- Information gathering: "Research options for Y"
- Scheduling: "Schedule sync with Z"
- Communication: "Update stakeholders on decision"

**Prioritization:**
- Critical: Blocks other work, high impact
- High: Important, needed soon
- Medium: Should be done, no immediate urgency
- Low: Nice to have, lower priority

## Output Format

### Option 1: Markdown (Default)

```markdown
# Meeting Synthesis: [Meeting Title/Date]

## Participants
- Alice (Product Lead)
- Bob (Engineering)
- Carol (Design)

## Decisions Made
### Decision 1
- **What**: Adopt Vue 3 for new frontend
- **Why**: Better TypeScript support, smaller bundle size
- **Decided**: By consensus
- **Impact**: Requires training for team members using Vue 2

### Decision 2
- **What**: Delay launch by 2 weeks
- **Why**: Need more time for security review
- **Decided**: Product + Security alignment
- **Impact**: Affects Q4 roadmap planning

## Action Items

### High Priority
- [ ] Complete security audit (Bob, Due: Friday)
- [ ] Prepare Vue 3 migration plan (Carol, Due: Monday)

### Medium Priority
- [ ] Schedule team Vue 3 training (Alice, Due: Next week)

### Low Priority
- [ ] Document decision rationale (Bob, Due: End of sprint)

## Key Discussion Points
- Concerns about timeline slippage
- Team enthusiasm for Vue 3 adoption
- Need for better documentation

## Follow-up Required
- Confirm security audit scope with CTO
- Get client approval for 2-week delay
- Check team training capacity
```

### Option 2: JSON Structure

```json
{
  "meeting": {
    "title": "Q4 Planning",
    "date": "2024-11-08",
    "participants": ["Alice", "Bob", "Carol"]
  },
  "decisions": [
    {
      "id": "D1",
      "description": "Adopt Vue 3",
      "rationale": "Better TS support",
      "decider": "Consensus",
      "impact": "Requires team training"
    }
  ],
  "actionItems": [
    {
      "id": "A1",
      "task": "Complete security audit",
      "owner": "Bob",
      "dueDate": "2024-11-10",
      "priority": "HIGH",
      "context": "Required before launch"
    }
  ],
  "followUp": [
    "Confirm security audit scope",
    "Get client approval"
  ]
}
```

## Examples

### Example 1: Product Planning Meeting

**Input Meeting Notes:**
```
Meeting: Product Planning - Q1 2025
Attendees: Sarah (PM), Mike (Lead Dev), Lisa (Designer)

Topics:
1. User feedback analysis - lots of requests for dark mode
2. Performance issues reported in production
3. Q1 roadmap planning

Decisions:
- Will implement dark mode as primary feature
- Will address performance issues first (performance is blocking)
- Delaying mobile app until Q2

Action items:
Sarah will brief the team on user feedback by tomorrow
Mike will create performance improvement plan by Friday
Lisa will start dark mode design exploration next week
Need to schedule meeting with exec team for roadmap approval

Issues:
- Performance work might delay features
- Team capacity might be tight with both performance + dark mode
- Mobile app delay will disappoint some users
```

**Output:**
```markdown
# Q1 2025 Product Planning Synthesis

## Decisions
1. **Implement dark mode as primary Q1 feature**
   - Why: High user demand from feedback analysis
   - Impact: Becomes focus of design/feature work

2. **Prioritize performance issues before new features**
   - Why: Blocking production users
   - Impact: Requires dedicated engineering time first

3. **Delay mobile app to Q2**
   - Why: Capacity and roadmap constraints
   - Impact: Will disappoint some users, needs communication

## Action Items

### Critical Path
- [ ] Performance improvement plan (Mike, Due: Friday)
  - Context: Blocking roadmap
  - Unblocks: Dark mode feature work

### High Priority
- [ ] Team briefing on user feedback (Sarah, Due: Tomorrow)
- [ ] Dark mode design exploration (Lisa, Due: Next week)

### Follow-up Required
- [ ] Executive team meeting on Q1 roadmap
- [ ] Communication plan for mobile app delay
- [ ] Capacity planning for parallel work streams

## Key Concerns
- Tight team capacity with performance + dark mode
- Mobile app delay needs stakeholder management
- Performance work timeline might slip
```

### Example 2: Engineering Standup

**Input Transcript:**
```
Sarah: OK team, quick standup. Mike, how's the API work?

Mike: Good progress. Got the authentication endpoints done.
Got the rate limiting working. Should be done by EOW.

Sarah: Great. Any blockers?

Mike: Need DB schema review from Carol. That's blocking
the user service implementation.

Carol: Oh, I can look at that this afternoon. Will send feedback.

Sarah: Perfect. Lisa, how's the frontend?

Lisa: Integrated the new modal component. Ran into a
responsive design issue on mobile that I'm debugging.
Should have fixed by tomorrow.

Sarah: OK, don't spend too much time on that if it's complex.
We can handle edge cases later.

Mike: Also, we should probably do a load test before shipping.

Sarah: Agreed. Let's add that to the list. Carol, can you
help set that up?

Carol: Sure, I can coordinate with DevOps.

Sarah: Good. Let's reconvene Thursday to check in.
```

**Output:**
```markdown
# Engineering Standup - 2024-11-08

## Current Status
- **Mike**: API auth endpoints complete, rate limiting working
  - On track: EOW completion
  - Blocker: Waiting on DB schema review

- **Lisa**: Modal component integrated, debugging responsive issue
  - On track: Mobile fix by tomorrow
  - Note: Don't over-engineer edge cases

- **Carol**: Available for schema review, coordinating load testing

## Action Items

### High Priority
- [ ] DB schema review (Carol, Due: Today afternoon)
  - Unblocks: Mike's user service implementation

- [ ] Mobile responsive debugging (Lisa, Due: Tomorrow)
  - Context: Modal component issue

### Medium Priority
- [ ] Coordinate load testing setup (Carol + DevOps, Due: This week)
  - Context: Required before shipping

## Decisions
- Load testing is required before deployment
- Don't over-engineer mobile edge cases yet

## Next Check-in
- Thursday team standup for progress review
```

## Processing Tips

### Handle Ambiguity
- If owner unclear: Note "TBD" and flag for clarification
- If timeline unclear: Use phrases like "asap", "this week", "unclear timeline"
- If decision unclear: List as "discussion item" vs "decision"

### Identify Hidden Items
- "We should..." often means someone needs to do it
- "Someone will need to..." is an implicit action item
- "We need to verify..." is a follow-up task
- "Can you..." is an action item for the person being asked

### Prioritize Effectively
- Critical: Blocks other work
- High: Time-sensitive or important
- Medium: Should be done soon
- Low: Nice to have

### Red Flags
- Vague ownership ("we'll figure it out")
- No timeline mentioned
- Conflicting decisions
- Unresolved concerns
- Unclear next steps

## Best Practices

### Input Quality
- More detail is better (full transcript > vague summary)
- Include speaker names if available
- Preserve disagreements and concerns
- Note time-sensitive items

### Output Quality
- Be specific: "review code" not clear, "review API endpoint authentication code" is clear
- Include context: Why matters, not just what to do
- Flag dependencies: What must happen first
- Highlight urgency: Critical path items

### Follow-Through
- Share results with team members assigned
- Create tickets/calendar items for action items
- Schedule follow-up for open items
- Update stakeholders on decisions

## Common Patterns

### Pattern 1: Decision with Cascading Action Items
```
Decision: Use PostgreSQL instead of MongoDB
  ↓
Action Items:
- Migrate existing data (Owner: DB team)
- Update ORM code (Owner: Backend team)
- Update schema documentation (Owner: Docs)
- Train team on SQL (Owner: Tech lead)
```

### Pattern 2: Blocking Dependencies
```
Task A: Complete security audit (BLOCKING)
  ↓
Task B: Deploy to production (BLOCKED)
  ↓
Task C: Start Q2 roadmap planning (BLOCKED)
```

### Pattern 3: Decision Reversal or Clarification Needed
```
Stated: "We'll use Vue"
But earlier: "React is better"
Follow-up: Clarify decision rationale and communicate to team
```

## Quality Checklist

After synthesizing a meeting, verify:

- [ ] All action items have clear owners
- [ ] All decisions are documented with rationale
- [ ] Critical items are flagged and prioritized
- [ ] Blocking dependencies are identified
- [ ] Follow-up tasks are clear
- [ ] Any concerns or dissent are captured
- [ ] Ambiguous items are flagged for clarification
- [ ] Results are ready to share with team

## Integration Points

### With Task Management
- Export action items to Jira, GitHub Issues, Asana
- Create calendar items for deadlines
- Set up reminders for owners

### With Communication
- Share synthesis with team
- Send to stakeholders who couldn't attend
- Create meeting summary email

### With Roadmap Planning
- Decisions impact roadmap/timeline
- Action items affect capacity planning
- Follow-up tasks might become next meeting agenda

## Limitations & Considerations

- Cannot identify non-verbal communication (tone, body language)
- May miss implicit context only meeting attendees understand
- Requires clear, interpretable notes or transcripts
- Ambiguous meeting notes produce ambiguous output
- Cannot follow up on decisions that weren't explicit

## See Also

- Action item tracking and management
- Decision log and decision history
- Meeting agenda templates
- Post-meeting communication templates
