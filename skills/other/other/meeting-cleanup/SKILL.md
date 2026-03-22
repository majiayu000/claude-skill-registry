---
name: meeting-cleanup
description: Batch process multiple meetings from a single day. Consolidates action items and insights across meetings.
disable-model-invocation: false
user-invocable: true
---

## Quick Start

Upload or paste all of today's meeting transcripts, and I'll:
1. Summarize each meeting in 3 bullets
2. Extract all decisions and action items with owners
3. Deduplicate action items across meetings
4. Flag conflicts and cross-meeting patterns
5. Create a single consolidated action item list

**Shortcut:** Just paste your transcripts and say `/meeting-cleanup` -- I'll handle the rest.

---

# Meeting Day Cleanup Workflow

Process all your meetings in one batch at the end of the day using AI.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Business Info | `context-library/business-info-template.md` | company, product, team | Company context for interpreting discussions |
| Stakeholder Profiles | `context-library/stakeholder-template.md` | attendees' names | Communication preferences, roles, decision authority |
| Active PRDs | `context-library/prds/*.md` | features discussed | Link action items to active PRDs |
| Previous Meetings | `context-library/meetings/*.md`, `outputs/meeting-notes/` | same meeting name, same attendees | Carry-over items, open questions from last time |
| Strategy | `context-library/strategy/*.md` | strategic pillars, OKRs | Align decisions to strategic context |
| Decisions | `context-library/decisions/*.md` | related decisions | Check for conflicts with past decisions |

**Context Priority:**
1. Previous meeting notes for same recurring meetings FIRST
2. Active PRDs and strategy docs SECOND
3. Stakeholder profiles THIRD
4. Business info for general context FOURTH

---

## Overview

**Tools:** Otter.ai or Lindy + Claude
**When:** End of day with 3+ meetings

---

## Workflow

### Step 1: Gather All Meeting Transcripts

**From Otter.ai:**
- Export all today's transcripts
- Download as text files

**From Zoom/Meet/Teams:**
- Download auto-generated transcripts
- Save to folder

### Step 2: Batch Process with Claude (10 min)

```bash
claude "Process these meeting transcripts:
[upload all transcripts]

For each meeting:
1. Summary (3 bullets)
2. Decisions made
3. Action items (with owners)
4. Open questions
5. Follow-up needed

Then: Consolidated action item list across ALL meetings"
```

### Per-Meeting Quality Checks

For each meeting processed, verify:

1. **All decisions have clear owners** -- if a decision was made but no one owns execution, flag it: "Decision made but no owner assigned -- who drives this?"
2. **All action items have deadlines** -- if an action item lacks a date, assign a reasonable default and flag it: "No deadline stated -- defaulting to [date], confirm?"
3. **No duplicate action items across meetings** -- if the same action appears in multiple meetings, consolidate into one entry and note which meetings referenced it
4. **Conflicting decisions across meetings are flagged** -- if Meeting 1 decided "launch in March" and Meeting 3 discussed "push to April," flag the conflict explicitly
5. **Strategic alignment is noted for each decision** -- tie decisions to strategic pillars from `context-library/strategy/` when relevant

### Step 3: Update Systems (5 min)

- [ ] Add action items to Jira/Linear
- [ ] Calendar follow-up meetings
- [ ] Send summary emails where needed
- [ ] Update project docs

---

## Automated Version

**Using Lindy or Relay:**

**Trigger:** End of day (6pm)  
**Actions:**
1. Pull all meeting transcripts
2. Process with Claude
3. Create Jira tickets for action items
4. Send summary email to each meeting's attendees
5. Post consolidated list to Slack

**Setup once, runs forever.**

---

## Template Output

```markdown
# Meeting Cleanup - [Date]

## Quick Stats
- Meetings attended: [X]
- Total time in meetings: [Y hours]
- Action items generated: [Z]

## Meeting 1: [Title] ([Time])
**Attendees:** [Names]
**Summary:** [3 bullets]
**Decisions:**
- [Decision 1]
- [Decision 2]

**Action Items:**
- [ ] [Action] - Owner: [Name] - Due: [Date]
- [ ] [Action] - Owner: [Name] - Due: [Date]

**Follow-up:** [Schedule next meeting? Send docs?]

---

[Repeat for each meeting]

---

## My Action Items (Consolidated)
1. [ ] [Action from Meeting 1]
2. [ ] [Action from Meeting 3]
3. [ ] [Action from Meeting 5]

## Waiting On Others
1. [Name] to [action] by [date]
2. [Name] to [action] by [date]

## Parking Lot (Questions/Ideas)
- [Question raised but not resolved]
- [Idea mentioned for later discussion]

---

## Cross-Meeting Intelligence

### Recurring Topics (with Priority Tags)

Tag each recurring topic with severity:
- **HIGH** -- Topic involves: CPO/CEO escalation, revenue-impacting deadline, at-risk OKR, or blocker affecting multiple teams
- **NORMAL** -- Topic involves: standard progress tracking, routine decisions, information sharing
- **LOW** -- Topic involves: nice-to-have discussions, future planning without urgency

Format: "[HIGH] [Topic]" came up in [Meeting 1] and [Meeting 3] -- consider scheduling a dedicated session
Example: "[HIGH] D30 Retention -- discussed in 3/4 meetings this week, CPO escalating to CEO"

### Stakeholder Load
[Who has the most action items across all meetings?]
| Person | Action Items | Meetings Involved |
|--------|-------------|-------------------|
| [Name] | [Count] | [Meeting list] |
| [Name] | [Count] | [Meeting list] |

**Overloaded?** If someone has 5+ action items across meetings, flag: "Consider whether [Name] can realistically deliver all of these by their deadlines."

### Timeline Conflicts
[Are any deadlines unrealistic given the workload?]
- [Name] has items due [Date A] (from Meeting 1) and [Date A] (from Meeting 3) -- are both achievable?
- [Feature] has conflicting timelines: Meeting 2 said "end of sprint" but Meeting 4 said "next quarter"

### Missing Follow-Ups
[Check previous weeks' meeting notes for action items that should have been discussed today but weren't]
- From [Date]: "[Action item]" assigned to [Name] -- not mentioned in today's meetings. Still open?

### Decisions Summary
[All decisions made across all meetings in one place]
| Decision | Made In | Owner | Strategic Alignment |
|----------|---------|-------|-------------------|
| [Decision] | [Meeting] | [Name] | [Pillar/OKR] |

### Cross-Meeting Conflict Detection

When the same topic or deliverable is discussed in multiple meetings, check for conflicts:

**Timeline conflicts:** Meeting A says "2 weeks" but Meeting B says "3 weeks" for the same deliverable
-> Flag: "CONFLICT: [Deliverable] timeline -- [Person A] estimated [X] (Meeting 1) vs [Y] (Meeting 2). Confirm which is accurate."

**Scope conflicts:** Meeting A scoped feature as X, but Meeting B expanded to X+Y without noting the change
-> Flag: "CONFLICT: Feature scope expanded in Meeting 2 without updating the original agreement from Meeting 1."

**Owner conflicts:** Meeting A assigned task to Person X, Meeting B assigned the same task to Person Y
-> Flag: "CONFLICT: Task '[Task name]' assigned to both [Person X] (Meeting 1) and [Person Y] (Meeting 2). Confirm owner."

**Priority conflicts:** Meeting A called feature P0, Meeting B called same feature P1
-> Flag: "CONFLICT: Feature priority downgraded from P0 (Meeting 1) to P1 (Meeting 2). Was this intentional?"

Always surface conflicts with the format:
"WARNING -- CONFLICT DETECTED: [description] -- Requires resolution by [suggested owner]"
```

---

**Action items tracked:** 100%
**Follow-through rate:** +40%

---

## Context Routing Strategy

When the PM uses `/meeting-cleanup`, I automatically:

### 1. Extract Action Items Intelligently
**Source:** All meeting transcripts provided
- **What I look for:** Implicit and explicit action items, owners, deadlines
- **How I use it:** Consolidate into single master list with owners
- **Example:** "Meeting 1: 'We'll coordinate on timeline' → Action: You sync with eng on timeline"

### 2. Identify Decisions Made
**Source:** All meeting transcripts
- **What I look for:** Decisions that came out of meetings
- **How I use it:** Flag for `/decision-doc` if significant
- **Example:** "Multiple meetings discuss same decision, consolidate for formal decision-doc"

### 3. Route Action Items to Right Systems
**Source:** Linear MCP, Jira MCP, task management systems
- **What I look for:** Which system to create tickets in
- **How I use it:** Auto-create tickets if MCP connected
- **Fallback:** Generate formatted action item list for manual entry

### 4. Consolidate Cross-Meeting Themes
**Source:** All transcripts analyzed together
- **What I look for:** Same topic discussed in multiple meetings
- **How I use it:** Note patterns and highlight for attention
- **Example:** "Onboarding mentioned in 3 meetings, might be emerging issue"

### 5. Update Status Automatically
**Source:** MCPs if task management connected
- **What I look for:** Related action items from earlier days
- **How I use it:** Note dependencies and blockers across meetings
- **Example:** "Design review action from yesterday blocks this implementation ticket"

### 6. Route for Follow-Up
**Routing logic:**
- **Action items created:** Tag owners, set due dates
- **Decisions identified:** Suggest `/decision-doc` for formal documentation
- **Cross-functional blockers:** Flag for escalation
- **Team patterns:** Suggest process improvements to leadership

---

## Output Quality Self-Check

Before delivering the meeting cleanup, verify:

- [ ] **Every decision has an owner** -- no orphaned decisions without someone responsible for execution
- [ ] **Every action item has a deadline** -- vague timelines are flagged with suggested dates
- [ ] **No duplicate action items** -- items appearing in multiple meetings are consolidated into one entry
- [ ] **Conflicting decisions flagged** -- if two meetings reached different conclusions on the same topic, the conflict is called out explicitly
- [ ] **Strategic alignment noted** -- major decisions reference the relevant strategic pillar or OKR
- [ ] **Cross-meeting intelligence included** -- recurring topics, stakeholder load, timeline conflicts, and missing follow-ups are analyzed
- [ ] **Previous meeting context checked** -- open items from prior meetings are referenced and tracked
- [ ] **Consolidated action list is complete** -- a single master list appears at the end with all items across all meetings
- [ ] **Cross-meeting conflicts checked and flagged** -- timelines, scope, owners, and priorities are compared across meetings for contradictions
- [ ] **Parking lot captured** -- unresolved questions and ideas that surfaced but were not actionable are noted
- [ ] **File saved correctly** -- output saved to `outputs/meeting-notes/cleanup-[date].md`

If any check fails, revise before delivering.
