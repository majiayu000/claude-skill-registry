---
name: meeting-agenda
description: Create structured meeting agendas for effective collaboration
---

## Quick Start

Tell me:
1. **What is this meeting about?** (topic, decision needed, or problem to solve)
2. **Who needs to be there?** (names and roles)
3. **How long should it be?** (default: 25 minutes)
4. **Is this recurring or one-off?**

I'll check your past meetings, stakeholder profiles, and PRDs to build a focused agenda with pre-reads, time boxes, and clear outcomes.

**Shortcut:** `/meeting-agenda decision on X with Y and Z` -- and I'll draft the full agenda.

**More shortcuts:**
- `/meeting-agenda 1:1 with Maya` -- Weekly manager 1:1
- `/meeting-agenda sprint planning` -- Sprint planning with eng team
- `/meeting-agenda difficult: scope negotiation with Sales` -- Conflict resolution meeting

---

# Meeting Agenda Skill

Generate clear, purposeful meeting agendas that drive decisions and action. Every meeting should have a clear goal, timeboxed topics, and defined outcomes.

## Step 0: Meeting Necessity Diagnostic

Before creating an agenda, first ask these diagnostic questions:

1. **Is this meeting actually necessary?** Could the outcome be achieved async (Slack thread, shared doc, or `/status-update`)?
2. **Who genuinely needs to be there?** If someone is only there "to stay informed," they should get notes instead.
3. **What specific decisions or outcomes are expected?** If you can't name one, the meeting probably should not happen.

If the PM realizes the meeting is not necessary, suggest an async alternative:
- **For alignment:** Shared doc with comment deadline
- **For updates:** `/status-update` sent to stakeholders
- **For quick decisions:** Slack thread with a 24-hour decision deadline
- **For feedback:** Async review in Figma/Google Docs with specific questions

Only proceed with agenda creation if a synchronous meeting is genuinely needed.

---

## Recurring vs One-Off Meetings

Ask which type this is -- the approach differs significantly.

**Recurring meetings** need progressive agendas that evolve week-to-week:
```
Week 1: Deep dive on one topic (60 min)
Week 2: Rapid updates + decisions (30 min)
Week 3: Planning session (45 min)
Week 4: Retro + learnings (30 min)
```
For recurring meetings, check `context-library/meetings/` and `outputs/meeting-notes/` for previous agendas and notes. Reference what was discussed last time, carry over open items, and avoid repeating the same format every week.

**One-off meetings** need a clear single outcome and should default to 25 minutes. If you cannot define the single outcome, push back on scheduling it.

---

## When to Use This Skill

- Before scheduling any meeting (if no agenda, don't schedule)
- Converting vague meeting requests into structured discussions
- Preparing for stakeholder reviews, planning sessions, or decision meetings
- Ensuring cross-functional meetings stay focused and productive

## Core Principles

### 1. Every Meeting Needs a Clear Purpose
- ✅ "Decide on pricing strategy for Enterprise tier"
- ❌ "Discuss pricing"

### 2. Time Limits Force Prioritization
- 30-minute default (enough for most topics)
- 60-minute max (beyond this, break into multiple meetings)
- Each agenda item gets a time box

### 3. Pre-Read > Presentation
- Send context before meeting (docs, data, proposals)
- Use meeting time for discussion, not information transfer
- "Read this doc before the meeting" should be expected

### 4. Output-Driven
- Every meeting should produce: Decision, Action Items, or Alignment
- If it doesn't, it shouldn't be a meeting

## Workflow

### Step 1: Define Meeting Metadata

```
Meeting Title: [Clear, specific title]

Date/Time: [When]
Duration: [15/30/45/60 minutes]
Format: [In-person / Zoom / Hybrid]

Attendees:
- [Name] - [Role] (Required)
- [Name] - [Role] (Required)
- [Name] - [Role] (Optional)

Meeting Owner: [Who's driving this meeting?]
Notetaker: [Who's documenting?]
```

### Step 2: State Meeting Purpose

```
## Purpose

[One sentence: What is this meeting for?]

Example:
- "Decide whether to build or buy our analytics platform"
- "Align on Q2 roadmap priorities across product teams"
- "Review user research findings and identify top 3 insights"

## Success Criteria

This meeting will be successful if:
- [ ] [Outcome 1: e.g., "We have a go/no-go decision on Feature X"]
- [ ] [Outcome 2: e.g., "Engineering understands scope and timeline"]
- [ ] [Outcome 3: e.g., "All blockers are identified with owners"]
```

### Step 3: Pre-Meeting Requirements

```
## Pre-Read (Required Before Meeting)

Please review before attending:
- [Document 1: Link + "5 min read"]
- [Document 2: Link + "10 min read"]
- [Data/Dashboard: Link + "quick review"]

Time required: [Total time to prep]

If you haven't reviewed the pre-read, please decline the meeting.
```

### Step 4: Build Time-Boxed Agenda

```
## Agenda

### [Time: 0-5 min] Context Setting
- Quick recap of background
- Confirm goals for this meeting
- Assign notetaker

### [Time: 5-20 min] [Agenda Item 1]
**Goal:** [What we're trying to accomplish]
**Format:** [Discussion / Presentation / Brainstorm / Decision]
**Presenter:** [Who's leading this section]

Key questions:
- [Question 1]
- [Question 2]
- [Question 3]

### [Time: 20-40 min] [Agenda Item 2]
**Goal:** [What we're trying to accomplish]
**Format:** [Discussion / Presentation / Brainstorm / Decision]
**Presenter:** [Who's leading this section]

Key questions:
- [Question 1]
- [Question 2]

### [Time: 40-55 min] Decision Time
**Decision needed:** [Specific decision to make]
**Decision maker:** [Who has final say]
**Options:** [List options A, B, C]

Vote/discuss to reach decision.

### [Time: 55-60 min] Next Steps & Closing
- Recap decisions made
- Assign action items with owners and due dates
- Schedule follow-ups if needed
```

## Meeting Type Templates

### Product Review Meeting

```markdown
# Product Review: [Feature Name]

**Purpose:** Review [Feature] design and decide on go-to-build

**Duration:** 45 min | **Owner:** [PM Name]

---

## Pre-Read (15 min)
- PRD: [Link]
- Design mockups: [Figma link]
- User research summary: [Link]

---

## Agenda

### [0-5 min] Context
- Problem we're solving
- Strategic fit

### [5-15 min] Solution Walkthrough
- Design demo (Designer leads)
- User flow explanation

### [15-30 min] Q&A and Feedback
Focus areas:
- Technical feasibility (Engineering)
- User experience concerns (Design)
- Edge cases and risks (Everyone)

### [30-40 min] Decision Discussion
- Go / No-go / Needs changes
- If "needs changes": what specifically?

### [40-45 min] Next Steps
- Decision: [Go/No-go/Iterate]
- Action items with owners
- Timeline confirmation

---

## Success Criteria
- [ ] Decision made: Build / Don't build / Iterate
- [ ] If build: Engineering timeline confirmed
- [ ] If iterate: Specific changes documented

## Estimated Prep Time: 20 minutes
- Review PRD: 10 min
- Review design mockups in Figma: 5 min
- Skim user research summary: 5 min
```

### Strategic Planning Meeting

```markdown
# Q2 Roadmap Planning

**Purpose:** Prioritize Q2 initiatives and align on goals

**Duration:** 60 min | **Owner:** [PM Name]

---

## Pre-Read (20 min)
- Q1 retro doc: [Link]
- Q2 initiative proposals (6 proposals): [Link]
- Company OKRs for Q2: [Link]

---

## Agenda

### [0-10 min] Q1 Retrospective
- What worked
- What didn't
- Lessons for Q2

### [10-40 min] Q2 Initiative Review
Review each proposal (5 min each):
1. [Initiative 1]: Impact, effort, strategic fit
2. [Initiative 2]: Impact, effort, strategic fit
3. [Initiative 3]: Impact, effort, strategic fit
4. [Initiative 4]: Impact, effort, strategic fit
5. [Initiative 5]: Impact, effort, strategic fit
6. [Initiative 6]: Impact, effort, strategic fit

### [40-55 min] Prioritization Exercise
- Stack rank initiatives
- Discuss trade-offs
- Confirm capacity (what fits in Q2?)

### [55-60 min] Final Decisions
- Committed: [List of initiatives we're doing]
- Backlog: [List of initiatives deferred]
- Action items: Owners for each initiative

---

## Success Criteria
- [ ] Clear Q2 roadmap (3-5 committed initiatives)
- [ ] Each initiative has exec sponsor
- [ ] Capacity confirmed with eng leadership

## Estimated Prep Time: 30 minutes
- Review Q1 retro doc: 10 min
- Skim all 6 initiative proposals: 15 min
- Review company OKRs for Q2: 5 min
```

### Decision Meeting

```markdown
# Decision: [Topic]

**Purpose:** Make go/no-go decision on [Topic]

**Duration:** 30 min | **Owner:** [Name] | **Decider:** [Name]

---

## Pre-Read (10 min)
- Decision doc: [Link - outlines options, pros/cons, recommendation]
- Supporting data: [Link]

---

## Agenda

### [0-5 min] Frame the Decision
- What we're deciding
- Why now
- Who decides (confirm decision-maker)

### [5-20 min] Evaluate Options
**Option A:** [Pros, cons, risks]
**Option B:** [Pros, cons, risks]
**Option C:** [Pros, cons, risks]

Discuss:
- What evidence supports each option?
- What are we uncertain about?
- What can't we undo later?

### [20-28 min] Make Decision
- Decision-maker's call: [Option chosen]
- Rationale: [Why]
- Dissent captured: [Any concerns to note]

### [28-30 min] Next Steps
- Action items to execute decision
- Communication plan (who needs to know?)
- Timeline for implementation

---

## Success Criteria
- [ ] Clear decision made (Option A/B/C)
- [ ] Rationale documented
- [ ] Action items assigned with owners

## Estimated Prep Time: 15 minutes
- Read decision doc (options, pros/cons, recommendation): 10 min
- Review supporting data: 5 min
```

### Difficult Conversation / Conflict Resolution Meeting

For meetings where tension or disagreement is expected:

```markdown
# Discussion: [Topic Where Perspectives Differ]

**Purpose:** Reach alignment on [Topic] despite differing perspectives

**Duration:** 45 min | **Owner:** [Neutral facilitator, ideally not a party to the disagreement]

---

## Pre-Read (10 min)
- Shared facts and data: [Link - agreed-upon data, not interpretations]
- Perspective A summary: [Link or 3-bullet summary]
- Perspective B summary: [Link or 3-bullet summary]

---

## Ground Rules
- We assume good intent from everyone
- Critique ideas, not people
- Focus on user/business impact, not personal preference
- The decision-maker will decide, but all perspectives will be heard

## Agenda

### [0-5 min] Acknowledge the Tension
- Name the disagreement explicitly (don't pretend it doesn't exist)
- Confirm shared goals: "We all want [X], we disagree on how to get there"
- Remind everyone of the ground rules

### [5-10 min] Present Shared Facts & Data
- Walk through the data everyone agrees on
- Identify where interpretations diverge
- Separate facts from opinions

### [10-25 min] Each Perspective Gets Equal Airtime
**Perspective A** (7 min):
- State your position
- Share your reasoning
- Name your biggest concern if we go the other way

**Perspective B** (7 min):
- State your position
- Share your reasoning
- Name your biggest concern if we go the other way

(No interruptions during each person's time)

### [25-35 min] Structured Decision Process
- What do both sides agree on?
- Where is the core disagreement?
- Can we find a compromise or hybrid?
- What would change each side's mind?
- Is there a way to test with data (A/B test, pilot)?

### [35-45 min] Decision & Clear Next Steps
- Decision-maker states decision and rationale
- Capture dissent (it's OK to disagree and commit)
- Define clear next steps regardless of outcome
- Set a check-in date to revisit if needed

---

## Success Criteria
- [ ] All perspectives were heard and documented
- [ ] A clear decision was made (or a decision process was agreed upon)
- [ ] Everyone can articulate the rationale, even if they disagree
- [ ] Next steps have owners and dates
- [ ] Relationships are intact (no lingering resentment)

## Estimated Prep Time: 15 minutes
- Review shared facts and data: 5 min
- Read Perspective A and Perspective B summaries: 5 min
- Reflect on your own position and potential compromises: 5 min
```

**When to use this template:**
- Two teams disagree on approach (build vs buy, feature scope, timeline)
- A stakeholder is pushing for something that conflicts with strategy
- Past discussions have gone in circles without resolution
- There's visible tension that needs to be addressed directly

---

### Brainstorm / Ideation Meeting

```markdown
# Brainstorm: [Topic]

**Purpose:** Generate ideas for [Problem/Opportunity]

**Duration:** 45 min | **Owner:** [Name]

---

## Pre-Read (5 min)
- Problem statement: [Link]
- Constraints: [What we can't change]
- Success metrics: [How we'll measure good ideas]

---

## Agenda

### [0-5 min] Set the Stage
- Problem we're solving
- Rules: No bad ideas, quantity > quality, build on others' ideas

### [5-30 min] Idea Generation
**Round 1:** Individual brainstorm (10 min)
- Everyone writes ideas independently (Miro/Figjam/Post-its)

**Round 2:** Group sharing (15 min)
- Go around, share 1-2 ideas each
- Build on others' ideas

**Round 3:** Wild ideas (5 min)
- "What if we had unlimited budget/time?"
- "What would [Company X] do?"

### [30-40 min] Clustering & Themes
- Group similar ideas
- Identify themes
- Spot patterns

### [40-45 min] Next Steps
- Top 5-10 ideas to explore further
- Owners for quick prototypes/research
- Timeline for follow-up evaluation

---

## Success Criteria
- [ ] 20+ ideas generated
- [ ] Top 5-10 ideas identified for further exploration
- [ ] Owners assigned to prototype/validate top ideas

## Estimated Prep Time: 10 minutes
- Read problem statement and constraints: 5 min
- Brainstorm 3-5 initial ideas on your own before the meeting: 5 min
```

## Output Format

```markdown
# [Meeting Title]

📅 **Date/Time:** [When]
⏱️ **Duration:** [Length]
👥 **Attendees:** [List]
🎯 **Owner:** [Name]

---

## Purpose

[One-sentence goal]

**Success criteria:**
- [ ] [Outcome 1]
- [ ] [Outcome 2]

---

## Pre-Read (Required)

⏰ Time required: [X minutes]

- [Doc 1]: [Link] (X min read)
- [Doc 2]: [Link] (X min read)

⚠️ If you haven't reviewed the pre-read, please decline this meeting.

---

## Agenda

### [0-X min] [Section Title]
**Goal:** [What this section accomplishes]

[Details, questions, or discussion points]

### [X-Y min] [Section Title]
**Goal:** [What this section accomplishes]

[Details, questions, or discussion points]

[Continue for all sections...]

---

## Decisions Needed

1. **[Decision 1]**
   - Options: A, B, C
   - Decision maker: [Name]

2. **[Decision 2]**
   - Options: A, B
   - Decision maker: [Name]

---

## Action Items Template

[Will be filled during meeting]

| Action Item | Owner | Due Date |
|-------------|-------|----------|
| [Task 1] | [Name] | [Date] |
| [Task 2] | [Name] | [Date] |

---

## Follow-Up

- Next meeting (if needed): [Date/topic]
- Decisions to communicate: [Who needs to know?]

---

## Estimated Prep Time: [X] minutes

- [Prep task 1]: [estimated time] (e.g., "Review Q1 metrics dashboard: 5 min")
- [Prep task 2]: [estimated time] (e.g., "Skim stakeholder's last 3 updates: 3 min")
```

## Advanced Techniques

### The "No Agenda, No Attenda" Rule

```
If someone sends you a meeting invite without an agenda:

"Thanks for the invite! To make best use of everyone's time, could you send:
1. Meeting goal (one sentence)
2. Pre-read materials (if any)
3. Time-boxed agenda

Happy to join once I know how to prepare!"
```

### Progressive Agendas

For recurring meetings, alternate formats:

```
Week 1: Deep dive on one topic (60 min)
Week 2: Rapid updates + decisions (30 min)
Week 3: Planning session (45 min)
Week 4: Retro + learnings (30 min)
```

### Asynchronous Pre-Meeting Voting

For decisions, collect input before meeting:

```
Pre-meeting survey (5 min to complete):
1. Which option do you prefer? (A/B/C)
2. What concerns do you have?
3. What information would change your mind?

Results: [Link to responses]
Meeting focuses on discussing concerns, not rehashing basics.
```

## Common Mistakes to Avoid

❌ No time limits (topics expand to fill time)
✅ Strict time boxes for each section

❌ "Status update" meetings (send async instead)
✅ Meetings for decisions, discussion, or collaboration only

❌ 10+ people (too many voices, no decisions)
✅ 3-7 people ideal (Amazon "two-pizza rule")

❌ Back-to-back meetings (no processing time)
✅ 25/50-minute meetings (built-in buffer)

❌ Presenters reading slides (waste of time)
✅ Pre-read decks, use meeting for Q&A

## Pro Tips

1. **Default to 25 minutes:** Not 30. Build in processing time.
2. **Send agenda 24 hours before:** Give people time to prepare
3. **Required vs optional attendees:** Be explicit
4. **Assign a notetaker:** Not the meeting owner
5. **End with recap:** Decisions + action items, stated aloud
6. **Cancel if not needed:** If async would work, cancel meeting
7. **No-laptop rule:** (for some meetings) Full attention

## Integration with Other Skills

**After the meeting:**
- `/meeting-notes` - Document outcomes and action items
- `/meeting-cleanup` - Process batch of meetings from one day
- `/decision-doc` - Formalize decisions made in meeting

**Before the meeting:**
- `/prd-draft` - Create spec to review in meeting
- `/status-update` - Pre-read for stakeholder meetings

## Questions to Ask Before Creating Agenda

1. **Is this meeting necessary?** (Could it be async?)
2. **Who's the decision-maker?** (If none, maybe it's not a meeting)
3. **What's the pre-read?** (How do people prepare?)
4. **What's the one thing?** (If we only accomplish one thing, what is it?)
5. **Who really needs to be there?** (Optional vs required)

## Post-Meeting: Pre-Formatted Notes Stub

After generating the agenda, also create a matching meeting notes stub that can be used with `/meeting-notes` after the meeting. This saves time and ensures continuity between agenda and notes.

```markdown
# Meeting Notes: [Meeting Title] - [Date]

**Attendees:** [Pre-filled from agenda]
**Notetaker:** [Assigned in agenda]

---

## Agenda Item 1: [Title from agenda]
**Discussion:**
-

**Decision:**
-

---

## Agenda Item 2: [Title from agenda]
**Discussion:**
-

**Decision:**
-

---

[Repeat for all agenda items]

---

## Action Items

| Action Item | Owner | Due Date |
|-------------|-------|----------|
|  |  |  |
|  |  |  |

## Open Questions / Parking Lot
-

## Follow-Up
- Next meeting needed?
- Notes to share with:
```

Save this stub alongside the agenda so the PM can fill it in during or right after the meeting.

---

## Output Quality Self-Check

Before delivering the agenda, verify:

- [ ] **Clear purpose:** The meeting purpose is one specific sentence, not vague ("discuss X")
- [ ] **Success criteria defined:** At least one measurable outcome for "this meeting was worth it"
- [ ] **Every section time-boxed:** No open-ended agenda items
- [ ] **Pre-read specified:** Materials linked with estimated read time (or explicitly "none needed")
- [ ] **Right attendees:** Required vs optional clearly marked; no more than 7 required attendees
- [ ] **Decision-maker identified:** If a decision is needed, the decider is named
- [ ] **Total time adds up:** Time boxes sum to the meeting duration (not over or under)
- [ ] **Meeting notes stub created:** A matching notes template is generated alongside the agenda
- [ ] **Async alternative considered:** The diagnostic confirmed this meeting is truly necessary
- [ ] **Context referenced:** Relevant past meetings, PRDs, or strategy docs are linked in pre-read
- [ ] **Prep time estimate included:** Specific prep tasks listed with estimated times for each

If any check fails, revise before delivering.

---

Remember: A great agenda is half the battle. The other half is actually sticking to it during the meeting.

---

## Context Routing Strategy

When the PM uses `/meeting-agenda`, I automatically:

### 1. Check Recent Meeting Context
**Source:** `context-library/meetings/`, recent decisions and action items
- **What I look for:** Related meetings, earlier discussions, open questions
- **How I use it:** Reference previous context in pre-read section
- **Example:** "You discussed pricing Thursday, this follow-up should assume people remember that"

### 2. Pull Stakeholder Communication Preferences
**Source:** `context-library/stakeholder-template.md`
- **What I look for:** How each stakeholder prefers communication, decision style
- **How I use it:** Format agenda and pre-read to match their preferences
- **Example:** "CFO prefers numbers first, I'll put financial data in pre-read"

### 3. Reference Relevant PRDs & Strategy
**Source:** `context-library/prds/`, `context-library/strategy/`
- **What I look for:** Strategic context that informs meeting purpose
- **How I use it:** Add strategic rationale to meeting purpose statement
- **Example:** "This decision affects H1 roadmap, reference that in purpose"

### 4. Check Attendee Availability & Context
**Source:** Stakeholder profiles, org structure
- **What I look for:** Who actually needs to be in this meeting
- **How I use it:** Suggest required vs optional attendees
- **Example:** "Design lead could be optional if this is strategy-only discussion"

### 5. Create Pre-Read Artifacts if Needed
**Source:** Related PRDs, decisions, data
- **What I look for:** Documentation that already exists and should be pre-read
- **How I use it:** Link to existing docs rather than recreating context
- **Example:** "Link to decision-doc from last week rather than re-explain it"

### 6. Route to Meeting Notes Post-Meeting
**Routing logic:**
- After meeting: Use `/meeting-notes` to capture outcomes
- Multiple meetings: Use `/meeting-cleanup` at end of day
- Decision made in meeting: Route to `/decision-doc` if it needs formal documentation
