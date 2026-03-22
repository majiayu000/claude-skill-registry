---
name: meeting-feedback
description: Post-meeting effectiveness feedback and continuous improvement
---

## Quick Start

Tell me:
1. **Which meeting are you rating?** (name, date, and who ran it)
2. **Did it achieve its goal?** (yes/no/partially)
3. **What's the one thing you'd change?**

I'll walk you through a structured evaluation, score the meeting across 5 dimensions, check for trends if this is a recurring meeting, and give you specific recommendations.

**Shortcut:** `/meeting-feedback [meeting name] -- 3/5, pre-read was late` -- and I'll build the full assessment.

---

# Meeting Feedback Skill

Evaluate meeting effectiveness and identify improvements. Quick retrospective to make future meetings better.

## When to Use This Skill

- Immediately after important meetings (within 10 minutes)
- After recurring meetings (to improve cadence)
- When a meeting felt unproductive (diagnose what went wrong)
- For team retrospectives on meeting culture

## Quick Feedback

Use after any meeting:

```
Meeting: [Meeting name]
Date: [Date]

⭐ Rating: [1-5 stars]

What worked:
- [One thing that was effective]

What didn't:
- [One thing that was wasteful]

One change for next time:
- [Specific improvement]
```

## Full Feedback

Use after high-stakes or recurring meetings:

### Step 1: Meeting Details

```
Meeting: [Name]
Date: [Date]
Duration: [Scheduled time] → [Actual time]
Attendees: [Number of people]
Owner: [Who ran it]
```

### Step 2: Objectives Assessment

```
## Did We Achieve the Goal?

Original purpose: [What the agenda said]

✅ / ❌ Goal achieved?

If no:
- What was missing? [Explanation]
- What blocked us? [Blocker]
```

### Step 3: Effectiveness Scoring

Rate each dimension (1-5 scale) using these scoring anchors:

```
## Effectiveness Scores

### 1. Preparation (1-5): ⭐⭐⭐⭐⭐

Scoring anchors:
  1 - No agenda shared, attendees didn't know the purpose
  2 - Agenda existed but was vague or shared less than 1 hour before
  3 - Clear agenda shared day-before, most attendees came prepared
  4 - Detailed agenda with pre-reads linked, all attendees prepared
  5 - Pre-reads reviewed by all, discussion started at full speed from minute one

- Pre-read sent on time?
- Attendees came prepared?
- Agenda was clear?

### 2. Time Management (1-5): ⭐⭐⭐⭐⭐

Scoring anchors:
  1 - Started 10+ min late, ran over by 15+ min, no time for decisions
  2 - Started late or ran over, some agenda items skipped
  3 - Started roughly on time, mostly followed agenda, ended within 5 min of scheduled
  4 - Started on time, all agenda items covered, ended on time
  5 - Started on time, agenda covered with time to spare, ended early or used extra time for bonus discussion

- Started on time?
- Stayed on agenda?
- Ended on time?

### 3. Participation (1-5): ⭐⭐⭐⭐⭐

Scoring anchors:
  1 - One person talked the entire time, multiple attendees were silent, wrong people in room
  2 - Two or three people dominated, several attendees disengaged or multitasking
  3 - Most people contributed at least once, some imbalance in airtime
  4 - Balanced discussion, facilitator drew out quiet voices, all key perspectives heard
  5 - Every attendee contributed meaningfully, active listening evident, diverse perspectives surfaced and built upon

- Right people in room?
- Everyone contributed?
- No one dominated?

### 4. Decisions (1-5): ⭐⭐⭐⭐⭐

Scoring anchors:
  1 - No decisions made, unclear who had authority, meeting ended with "let's discuss more"
  2 - Decision was vaguely reached but not stated explicitly, rationale unclear
  3 - Decision made and stated aloud, decision-maker was clear, but rationale not documented
  4 - Decision made with clear rationale, dissent captured, communicated to stakeholders
  5 - Decision made using structured process (options evaluated, criteria applied), rationale documented, dissent recorded, communication plan in place

- Clear decision-maker?
- Decision was made?
- Rationale documented?

### 5. Action Items (1-5): ⭐⭐⭐⭐⭐

Scoring anchors:
  1 - No action items captured, vague "we should do X" statements, no owners
  2 - Some action items noted but missing owners or deadlines
  3 - Action items listed with owners, but deadlines vague ("next week" instead of specific dates)
  4 - All action items have specific owners and due dates, sent to attendees within 2 hours
  5 - Action items with owners, dates, and success criteria; tracked in project management tool; follow-up mechanism confirmed

- Clear next steps?
- Owners assigned?
- Due dates set?

**Overall Score:** [Average] / 5
```

### Step 4: What Worked

```
## What Worked Well

✅ [Strength 1]
   - Why it worked: [Explanation]
   - Repeat next time: Yes/No

✅ [Strength 2]
   - Why it worked: [Explanation]
   - Repeat next time: Yes/No

✅ [Strength 3]
   - Why it worked: [Explanation]
   - Repeat next time: Yes/No
```

### Step 5: What Didn't Work

```
## What Didn't Work

❌ [Problem 1]
   - Impact: [How it hurt the meeting]
   - Root cause: [Why it happened]
   - Fix for next time: [Specific change]

❌ [Problem 2]
   - Impact: [How it hurt the meeting]
   - Root cause: [Why it happened]
   - Fix for next time: [Specific change]
```

### Step 6: Meeting Smells

Common antipatterns - check for these:

```
## Meeting Smells (Check all that apply)

[ ] **Status report meeting**
    - People just shared updates (could've been async)
    - Fix: Send updates in doc, use meeting for decisions

[ ] **Too many people**
    - 10+ attendees, most silent
    - Fix: Required vs optional attendees, record for others

[ ] **Rehashing decisions**
    - Revisiting previously made choices
    - Fix: Document decisions, share context better

[ ] **No clear owner**
    - Unclear who was driving the meeting
    - Fix: Assign meeting owner in agenda

[ ] **Presentation, not discussion**
    - Someone read slides for 30+ minutes
    - Fix: Send deck as pre-read, meeting for Q&A only

[ ] **Meeting to schedule another meeting**
    - No decision, just agreed to meet again
    - Fix: Make decision now or cancel

[ ] **Hidden agenda**
    - Real topic emerged mid-meeting
    - Fix: Be explicit about purpose upfront

[ ] **No pre-read**
    - First 20 min wasted on context-setting
    - Fix: Send materials 24 hours before

[ ] **Action items unclear**
    - Vague next steps, no owners
    - Fix: Use action item template with owners + dates
```

### Step 7: Recommendations

```
## Recommendations for Next Time

### Must Change
🔴 [Critical fix 1]: [Specific action]
🔴 [Critical fix 2]: [Specific action]

### Should Change
🟡 [Important fix 1]: [Specific action]
🟡 [Important fix 2]: [Specific action]

### Could Change
🟢 [Nice-to-have 1]: [Specific action]
```

### Step 8: Meeting Continuation Decision

```
## Should This Meeting Continue?

For recurring meetings:

✅ Keep as-is: Meeting is working well
🔄 Keep with changes: Meeting is valuable but needs fixes
⏸️ Pause: Revisit in [X weeks/months]
❌ Cancel: Not providing value, eliminate

If keeping:
- Frequency: [Current] → [Recommended]
- Duration: [Current] → [Recommended]
- Attendees: [Add/remove who?]
- Format: [What changes to agenda/structure?]
```

## Output Format

```markdown
# Meeting Feedback: [Meeting Name]

**Date:** [Date] | **Duration:** [X min] | **Attendees:** [Count]

---

## Overall Assessment

**Rating:** ⭐⭐⭐⭐ (4/5)

**Goal achieved?** ✅ Yes / ❌ No

---

## Effectiveness Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| Preparation | ⭐⭐⭐ | Pre-read sent late |
| Time Management | ⭐⭐⭐⭐⭐ | Started/ended on time |
| Participation | ⭐⭐⭐⭐ | Good discussion |
| Decisions | ⭐⭐⭐ | Decision unclear |
| Action Items | ⭐⭐⭐⭐⭐ | Clear owners |

**Overall:** 4.0 / 5

---

## What Worked

✅ **[Strength 1]**
- [Why it worked]

✅ **[Strength 2]**
- [Why it worked]

---

## What Didn't Work

❌ **[Problem 1]**
- Impact: [Consequence]
- Fix: [Specific change]

❌ **[Problem 2]**
- Impact: [Consequence]
- Fix: [Specific change]

---

## Meeting Smells Detected

- [ ] Status report meeting
- [x] Too many people (12 attendees, 5 silent)
- [ ] Rehashing decisions
- [x] No pre-read sent

---

## Recommendations

### Must Change
🔴 Send pre-read 24 hours before (not day-of)
🔴 Reduce attendees to 6-7 (make others optional)

### Should Change
🟡 Add explicit decision-maker to agenda

### Could Change
🟢 Try 45-minute slot instead of 60

---

## Meeting Continuation

**Decision:** 🔄 Keep with changes

**Changes to implement:**
- Frequency: Weekly → Biweekly
- Pre-read requirement: Mandatory
- Attendee list: Cut from 12 to 7

**Next review:** [Date in 1 month]
```

### When to Trigger a Team Retro

**Automatic trigger:** Suggest a team meeting retrospective when ANY of these conditions are met:
- 3+ meetings scored below 3.0 on the same dimension within 30 days
- Same "meeting smell" detected in 3+ consecutive meetings of the same type
- Action items from meetings are consistently not completed (tracked via /meeting-cleanup)
- A stakeholder gives feedback that meetings are unproductive

**How to connect:** "Based on the last month of meeting feedback, [Dimension X] has scored below 3.0 in [N] meetings. This suggests a systemic issue rather than a one-off problem. Want to run a team retrospective focused on improving [Dimension X]?"

This turns the retro section from a standalone module into a natural escalation from individual meeting feedback.

---

## Team Retrospective Format

For team-wide meeting culture assessment:

```markdown
# Team Meeting Retrospective

**Period:** [Last month/quarter]
**Meetings evaluated:** [Count]
**Total time spent:** [Hours]

---

## Meeting Inventory

| Meeting | Frequency | Duration | Attendees | Avg Rating | Keep? |
|---------|-----------|----------|-----------|------------|-------|
| [Meeting 1] | Weekly | 60 min | 8 | ⭐⭐⭐⭐ | ✅ |
| [Meeting 2] | Daily | 15 min | 5 | ⭐⭐⭐ | 🔄 |
| [Meeting 3] | Monthly | 120 min | 15 | ⭐⭐ | ❌ |

---

## Time Analysis

**Total meeting time:** [X hours/week]
- Valuable meetings: [Y hours] ([Z%])
- Low-value meetings: [A hours] ([B%])

**Goal:** Reduce low-value meeting time by 50%

---

## Common Issues Across Meetings

1. **[Issue 1]** - Seen in [X/Y meetings]
   - Fix: [Team-wide change]

2. **[Issue 2]** - Seen in [X/Y meetings]
   - Fix: [Team-wide change]

---

## Team Meeting Norms

Based on feedback, we're establishing:

**Preparation:**
- [ ] Pre-reads sent 24 hours before
- [ ] Attendees review materials before joining
- [ ] Can decline if unprepared

**Execution:**
- [ ] Start/end on time (no grace period)
- [ ] 25/50-minute slots (not 30/60)
- [ ] Notetaker rotates
- [ ] Decisions documented in real-time

**Follow-up:**
- [ ] Action items sent within 2 hours
- [ ] Owners confirm receipt
- [ ] Next meeting reviews action item progress

---

## Meetings to Experiment With

**Cancel for 1 month:**
- [Meeting X] - Let's try async updates instead

**Change format:**
- [Meeting Y] - Move from weekly 60min to biweekly 30min

**New meeting to trial:**
- [Meeting Z] - Monthly deep dive on [topic]

**Review date:** [One month from now]
```

## Meeting Cost Calculator

Help teams visualize waste:

```
Meeting: [Name]
Frequency: [Weekly/Monthly/etc.]

Attendees & Costs:
- [Name 1]: $150/hr × 1hr = $150
- [Name 2]: $125/hr × 1hr = $125
- [Name 3]: $100/hr × 1hr = $100
[...]

**Per-meeting cost:** $800
**Annual cost:** $800 × 52 weeks = $41,600

**Question:** Is this meeting worth $41K/year?
If not, what changes would justify the cost?
```

## Pro Tips

1. **Rate immediately:** Memory fades fast
2. **Be specific:** "Meeting ran long" → "Started 10 min late, no time for decisions"
3. **Celebrate good meetings:** Positive reinforcement works
4. **Track trends:** One bad meeting is data, three is a pattern
5. **Share feedback:** Don't keep it private, send to meeting owner
6. **Act on insights:** Feedback without action is pointless
7. **Review quarterly:** Look at meeting portfolio, not just individual meetings

## Common Mistakes to Avoid

❌ Generic feedback ("meeting was fine")
✅ Specific observations ("pre-read sent day-of, not 24hr before")

❌ Blaming people ("John talked too much")
✅ Blaming process ("No facilitator to manage airtime")

❌ Collecting feedback, never acting
✅ Implement top 1-2 fixes for next meeting

❌ Only noting problems
✅ Also capture what worked well (repeat it)

## Integration with Other Skills

**Before meeting:**
- `/meeting-agenda` - Create structured agenda

**After meeting:**
- `/meeting-notes` - Document decisions and action items
- `/meeting-cleanup` - Batch process day's meetings

**Recurring use:**
- Run meeting-feedback monthly on recurring meetings
- Team retrospective quarterly on meeting culture

## Quick Questions for Any Meeting

After any meeting, ask yourself:

1. **Value:** Was this worth [cost in time/money]?
2. **Async:** Could this have been an email/doc?
3. **Attendees:** Did everyone need to be there?
4. **Outcome:** Did we make a decision or just talk?
5. **Next time:** One change that would make this 20% better?

---

## Trend Tracking

After scoring, check `outputs/meeting-notes/` and previous feedback files for the same recurring meeting. If previous feedback exists, show a trend:

```
## Meeting Effectiveness Trend: [Meeting Name]

Last 3 ratings: 3.0 -> 3.5 -> 4.0 (improving)

Dimension trends:
| Dimension       | 3 Weeks Ago | 2 Weeks Ago | This Week | Trend      |
|-----------------|-------------|-------------|-----------|------------|
| Preparation     | 2           | 3           | 4         | Improving  |
| Time Management | 4           | 4           | 4         | Stable     |
| Participation   | 3           | 3           | 3         | Stagnant   |
| Decisions       | 3           | 4           | 4         | Improved   |
| Action Items    | 3           | 3           | 5         | Improving  |

Key insight: Preparation has improved since we started sending pre-reads 24hr before.
Attention needed: Participation has been flat at 3 for three weeks -- consider
assigning a facilitator or using round-robin format.
```

If no previous feedback exists, note: "This is the first feedback for this meeting. Future ratings will show trends."

Save feedback files with consistent naming: `outputs/meeting-notes/feedback-[meeting-name]-[date].md` to enable trend tracking.

---

## Feedback Delivery Guidance

How to share meeting feedback constructively:

**For meetings you organized:**
- Share feedback openly with attendees
- Frame it as: "Here's how I'm planning to improve our next session based on what I observed"
- Commit to specific changes and ask for input

**For meetings others organized:**
- Frame as: "I noticed [specific observation] -- would you be open to trying [specific change]? I think it could help us [benefit]."
- Lead with what worked well before suggesting changes
- Never share raw scores without context or explanation
- Offer to help implement changes (e.g., "I can send pre-reads next time if that helps")

**For team-wide patterns:**
- Aggregate feedback across meetings before raising systemic issues
- Present data: "Over the last month, 4 of our 6 recurring meetings scored below 3 on Preparation"
- Propose a team norm rather than calling out individuals

**What NOT to do:**
- Don't share scores publicly without discussing privately first
- Don't use feedback as ammunition in unrelated discussions
- Don't wait months to share -- feedback is most useful within a week

---

### Evaluating Meetings You Didn't Attend

When asked to evaluate a meeting you weren't in (e.g., PM asks "how was my team's sprint retro?"):
- **Use the meeting notes** as primary input (from /meeting-notes output or raw notes)
- **Score only observable dimensions:** Decisions, Action Items, and Time Management can be assessed from notes. Participation and Preparation usually cannot -- note them as "Unable to assess from notes."
- **Flag the limitation:** "Note: This evaluation is based on meeting notes, not direct observation. Participation and Preparation scores may not be accurate."
- **Suggest:** "For a more complete assessment, ask an attendee to answer 3 quick questions about preparation and participation."

---

## Output Quality Self-Check

Before delivering the feedback, verify:

- [ ] **Specific observations:** Every "what worked" and "what didn't" cites a specific moment, not generalities
- [ ] **Scoring anchors used:** Each dimension score matches the anchor description, not just gut feeling
- [ ] **Actionable fixes:** Every problem identified has a specific, implementable recommendation
- [ ] **Balanced:** At least one "what worked" item is included (even for bad meetings)
- [ ] **Trend checked:** If this is a recurring meeting, previous feedback was searched for trend data
- [ ] **Delivery guidance included:** Feedback includes advice on how to share it constructively
- [ ] **Meeting smells checked:** The antipattern checklist was reviewed against this meeting
- [ ] **Continuation decision made:** For recurring meetings, a keep/change/pause/cancel recommendation is included
- [ ] **Root causes identified:** Problems trace to process issues, not blamed on individuals
- [ ] **Time cost noted:** The meeting cost (attendees x time) is contextualized against its value

If any check fails, revise before delivering.

---

Remember: Meeting culture is built one feedback loop at a time. Small improvements compound into massive time savings.

---

## Context Routing Strategy

When the PM uses `/meeting-feedback`, I automatically:

### 1. Check Meeting Norms from Context
**Source:** Past `/meeting-feedback` outputs, team patterns
- **What I look for:** What has worked well in your team's meetings before
- **How I use it:** Tailor feedback recommendations to your meeting culture
- **Example:** "Your team values async pre-reads, emphasize that in feedback"

### 2. Reference Related Decisions
**Source:** `context-library/decisions/` if this meeting made a decision
- **What I look for:** Decision that came out of the meeting
- **How I use it:** Note whether decision was crisp and clear
- **Example:** "Did the meeting achieve the decision that was supposed to be made?"

### 3. Track Meeting Effectiveness Trends
**Source:** Past meeting feedback (if available)
- **What I look for:** Patterns in what's working or failing
- **How I use it:** Flag if this is 3rd week of the same problem
- **Example:** "This is 3rd week 'pre-read sent late' — escalate as systemic issue"

### 4. Pull Attendee Context
**Source:** `context-library/stakeholder-template.md`
- **What I look for:** Attendees' roles, personality styles
- **How I use it:** Calibrate feedback (e.g., "Person X dominates, needs facilitation")
- **Example:** "VP Sales tends to redirect, consider appointing strong facilitator"

### 5. Route for Process Improvement
**Routing logic:**
- **Individual meeting:** Quick feedback loop
- **Recurring meeting:** Suggest changes for next occurrence
- **Team pattern:** Suggest `/meeting-cleanup` to batch-process and identify systemic issues
- **Major issue:** Flag for leadership discussion or team retrospective
