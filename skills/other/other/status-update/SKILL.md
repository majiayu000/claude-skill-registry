---
name: status-update
description: Generate stakeholder status updates. Creates clear, concise progress reports for different audiences.
disable-model-invocation: false
user-invocable: true
---

## Quick Start

Tell me:
1. **Who is this update for?** (your team, your manager, execs, cross-functional stakeholders)
2. **What time period?** (daily, weekly, monthly, project milestone)
3. **Any specific topics to highlight?** (launches, blockers, metrics, decisions)

I'll pull context from your PRDs, meetings, and metrics automatically.

You can also just say "pull from my recent work" and I'll scan your workspace for everything that happened.

**Shortcut:** `/status-update weekly for my manager` -- and I'll handle the rest.

---

# /status-update - Weekly Updates That Actually Get Read

When the PM types `/status-update`, create status updates that communicate progress, surface blockers, and keep stakeholders aligned.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Recent PRDs | `context-library/prds/*.md` | feature being updated | Feature status and changes |
| Meeting Notes | `context-library/meetings/*.md` | this week's meetings | Decisions, action items, blockers |
| Action Items | `context-library/meetings/` | completed / in progress / blocked | Track completion of commitments |
| Strategy | `context-library/strategy/*.md` | strategic pillars | Tie accomplishments to strategy |
| Metrics | `context-library/metrics/*.md` | baseline, trends | Metric movement and progress |
| Stakeholder Profiles | Stakeholder templates | your audience | Communication style for audience |

**Context Priority:**
1. Your recent work (PRDs, meetings) FIRST
2. Completed action items SECOND
3. Strategic context (pillars, goals) THIRD
4. Metrics and progress FOURTH

**Cross-Skill Links:**
- If action items from meetings → Reference `/meeting-notes`
- If progress on features → Reference `/prd-draft` or `/feature-results`
- If metric updates → Reference `/metrics-framework` and North Star
- If blockers → Link to relevant skill for resolution (e.g., `/prd-draft` if scope unclear)

---

## Step 0: Understanding Your Update Context

Before drafting, let me gather what happened...

**Checking:**
- `context-library/meetings/` for recent meetings this week/period
- `context-library/prds/` for features you're working on
- `context-library/metrics/` for recent metric changes
- `context-library/strategy/` for strategic context
- Stakeholder profiles for communication style of audience

**Based on what I find, I'll show you:**

### Your Recent Work

**Completed This Week:**
- [Shipped features / completed action items]
- [Decisions made]
- [Blockers resolved]

**In Progress:**
- [Features in development]
- [Research underway]
- [Outstanding action items]

**Blockers:**
- [What's blocking progress]
- [Who needs to help]
- [When you need resolution by]

### PM-Specific Diagnosis Questions

1. **Accomplishment Type:** What's worth highlighting? (Shipped / learned / decided / shipped)
2. **Metric Movement:** Did metrics move? In expected direction?
3. **Blocker Severity:** Are blockers getting in the way? Need escalation?
4. **Strategic Tie:** How do accomplishments connect to Q# strategy?
5. **Stakeholder Expectations:** What does your audience care about most?

---

## When to Use

- Weekly team updates
- Monthly progress reports to leadership
- Daily standups (async)
- Project milestone updates
- Quarterly business reviews
- Manager 1:1 prep
- Stakeholder check-ins

---

## How It Works

### Step 1: Tell Me What's Happened
### Step 2: Get a Structured Update

---

## Step 1: Tell Me What's Happened

When the PM types `/status-update`, I'll ask:

```
Let's create your status update.

**What period is this covering?**
- Daily (standup)
- Weekly (team update)
- Monthly (leadership update)
- Project milestone
- Other: [specify]

**Who's the audience?**
- Your team
- Your manager
- Cross-functional stakeholders
- Executive leadership
- All of the above

**Update format?**
- Quick (3 bullets max)
- Standard (progress + blockers + next steps)
- Detailed (full context for executives)

Now, just tell me what happened this week. Don't structure it - 
just brain dump and I'll organize it.

You can also say "pull from my recent work" and I'll scan:
- Meeting notes from this week
- PRDs you've updated
- Action items you've completed
- Conversations in this chat
```

---

## Step 2: Get Your Structured Update

Once I understand what happened:

```
Got it. Creating your [weekly] status update for [audience].

I'm pulling from:
- Meeting notes: [X meetings this week]
- Completed action items: [Y items]
- PRD updates: [Z documents]
- Recent decisions: [Context from this chat]

Here's your update:
```

---

## Standard Weekly Update Format

```markdown
# Weekly Update: [Your Name] - [Date Range]

## 🎯 Key Accomplishments

**Shipped / Completed:**
- [Specific outcome with impact] - [Link]
- [Specific outcome with impact] - [Link]

**Progress Made:**
- [Initiative name]: [What moved forward and why it matters]
- [Initiative name]: [What moved forward and why it matters]

**Decisions Made:**
- [Decision]: [Impact and who was involved]

## 📊 Metrics & Impact

| Metric | Last Week | This Week | Target | Status |
|--------|-----------|-----------|--------|--------|
| [Primary metric] | [#] | [#] | [#] | 🟢 On track |
| [Guardrail metric] | [#] | [#] | [#] | 🟡 Watching |

**What this means:**
[One sentence on trajectory toward goals]

## 🚧 Blockers & Risks

**Blocking me:**
1. [Specific blocker] - **Need:** [Specific help] from @[Person] by [Date]
2. [Specific blocker] - **Need:** [Specific help] from @[Person] by [Date]

**Risks I'm watching:**
- [Risk description] - **Mitigation:** [What you're doing about it]

**Nothing blocking?** → ✅ No blockers this week

## 🔜 Next Week

**Top Priorities:**
1. [Specific deliverable] - Due [Date]
2. [Specific deliverable] - Due [Date]
3. [Specific deliverable] - Due [Date]

**Meetings/Milestones:**
- [Important meeting] on [Date] - [Purpose]
- [Milestone] target for [Date]

## 💬 Discussion

**Questions for the team:**
- [Question where you need input]
- [Question where you need input]

**Where I could use help:**
- [Specific area] - If you have experience with [X], would love to chat

---

**Full context:** [Link to detailed project board / PRD / doc]
```

---

## Format Variations by Audience

### For Your Manager (1:1 Prep)

```markdown
# 1:1 Prep: [Date]

## ✅ Since Last Time

- [Thing you committed to] - Done
- [Thing you committed to] - In progress (70%)
- [Thing you committed to] - Blocked by [X]

## 🎯 This Week's Wins

[1-2 things that went really well]

## 🤔 Where I'm Stuck

1. **[Problem]**
   - What I've tried: [A, B, C]
   - What I need: [Your advice on X]

## 💭 Topics for Discussion

- [Topic 1]: [Why it's important]
- [Topic 2]: [Why it's important]
- [Topic 3]: [Why it's important]

## 📈 Career Development

[Any progress on goals you've set together]

## 🔜 My Commitments for Next Week

1. [Commitment]
2. [Commitment]
3. [Commitment]
```

**Why this works:**
- Shows you're on top of commitments
- Highlights wins (self-advocacy matters)
- Makes it easy for manager to help you
- Drives the agenda (you're not passive)
- Tracks career growth
- Clear commitments (accountability)

---

### For Executive Leadership

```markdown
# Product Update: [Initiative Name] - [Date]

## Executive Summary

**Status:** 🟢 On Track / 🟡 At Risk / 🔴 Off Track

**This week in one sentence:**
[The single most important thing that happened]

## Progress

**What shipped:**
- [Feature/milestone] → [Business impact]

**What moved forward:**
- [Initiative]: [Progress and why it matters to the business]

**Key metrics:**
- [Metric]: [Number] → [Direction and why]

## Blockers Needing Leadership Support

1. **[Blocker]**
   - Impact: [What this is preventing]
   - Need: [Specific decision or resource]
   - By when: [Deadline]

*No escalations needed* → ✅ Team is unblocked

## Looking Ahead

**Next milestone:** [Milestone] on [Date]
**Biggest risk:** [Risk] - [How you're mitigating]
**Forecast:** [On track to hit/miss goal because...]

## Request

[One specific thing you need from leadership, or "None - just keeping you informed"]

---

**Details:** [Link to full project update]
```

**Why this works:**
- Status color (🟢🟡🔴) lets them triage instantly
- One sentence summary respects their time
- Business impact, not feature lists
- Only escalates what needs their level
- Forward-looking (they care about trajectory)
- Explicit ask (don't make them guess)

---

### For Cross-Functional Stakeholders

```markdown
# Project Update: [Initiative Name] - Week of [Date]

## TL;DR

- **What happened:** [One sentence]
- **Impact:** [Why stakeholders should care]
- **Action needed:** [What you need from them, if anything]

## Progress This Week

**Completed:**
✅ [Milestone with impact]
✅ [Milestone with impact]

**In Flight:**
🚧 [What's being worked on] - [% complete] - [ETA]

**Next Up:**
📅 [What starts next week]

## Decisions Made

**Decision:** [What was decided]
- **Rationale:** [Why]
- **Who was involved:** [Names]
- **Impact:** [What this affects]

## What I Need From You

**[Stakeholder Group]:**
- [ ] [Specific ask] by [Date]
- [ ] [Specific ask] by [Date]

**No action needed from:** [Teams that can ignore this]

## Risks & Blockers

[Any cross-functional dependencies or issues affecting their area]

**Or:** ✅ No cross-team blockers this week

## Timeline

- [Milestone]: [Date] - [Status]
- [Milestone]: [Date] - [Status]
- [Launch]: [Date] - [Status]

---

**More details:** [Link to project doc]
**Questions?** Reply here or Slack me
```

**Why this works:**
- TL;DR lets people decide if they need to read more
- Clear on what's needed from each group
- Explicitly says who can ignore it (respects time)
- Decisions section keeps everyone aligned
- Timeline gives visibility without meetings

---

### Daily Standup (Async)

```markdown
**Yesterday:**
- [Thing I completed]
- [Thing I completed]

**Today:**
- [Thing I'm focusing on]
- [Thing I'm focusing on]

**Blockers:**
- [Specific blocker] - need help from @[person]
- *Or:* None

**Available for:**
- [Questions/topics people can ping you about]
```

**Why this works:**
- Super fast to read and write
- Makes blockers visible immediately
- "Available for" encourages collaboration

---

## Smart Features

### Auto-Pull from Your Work

I'll scan:

**Recent meeting notes:**
- Decisions from stakeholder meetings
- Customer insights from interviews
- Action items you completed

**PRD updates:**
- Features moved to different stages
- Decisions documented
- Blockers flagged

**Your recent conversations:**
- Progress you mentioned
- Problems you discussed
- Help you received

**Action items across all sources:**
- Completed ✅
- In progress 🚧
- Blocked 🚫

Then I'll ask:
```
I found these from your recent work:

✅ Completed:
- Shipped voice task feature to beta (47% adoption in 24hrs)
- Finalized pricing page redesign
- Completed 8 customer interviews

🚧 In Progress:
- Legal review for voice feature (waiting 2 weeks)
- Onboarding redesign (in design review)

🚫 Blocked:
- API integration (need response from Legal)

**Should I include all of these, or want to adjust?**
```

### Metrics Tracking

I'll automatically format metrics tables:

```
**Want to include metrics?**

I can pull from:
- Your PRDs (success metrics defined there)
- Recent conversations (metrics you mentioned)
- Manual input (just tell me the numbers)

Format options:
- Simple: [Metric] is [up/down] [X%]
- Table: Week-over-week with targets
- Chart: I can suggest data visualization
```

### Blocker Intelligence

When you mention blockers, I'll:

1. **Categorize them:**
   - Waiting on others
   - Resource constraints
   - Technical blockers
   - Unclear requirements

2. **Suggest escalation:**
   - Who should unblock this
   - When to escalate to leadership
   - Alternative paths to explore

3. **Track recurrence:**
   - "This is the 3rd week this is blocked - recommend escalating"

### Progress Insights

I'll flag patterns:

```
⚠️ **Pattern detected:**
You've mentioned "waiting for design" in 3 consecutive updates.

**Suggestions:**
- Schedule dedicated design time
- Escalate to design lead
- Explore if you can prototype yourself
- Clarify design dependencies earlier in process
```

---

## Update Frequency Guide

### Daily (Async Standup)
**Length:** 3-4 bullets
**Focus:** Today's work + blockers
**Audience:** Immediate team

### Weekly (Team Update)
**Length:** 5-7 sections
**Focus:** Progress, metrics, next week
**Audience:** Cross-functional team

### Bi-Weekly (Stakeholder Update)
**Length:** Full format with decisions
**Focus:** Milestones, decisions, cross-team impact
**Audience:** Broader stakeholders

### Monthly (Leadership Update)
**Length:** Executive summary + details
**Focus:** Business impact, trajectory, escalations
**Audience:** Leadership team

### Quarterly (Business Review)
**Length:** Comprehensive with appendix
**Focus:** Results vs. goals, learnings, next quarter plan
**Audience:** Executive team + board

---

## Common Mistakes to Avoid

### ❌ Activity Lists, Not Outcomes

**Bad:** "Had 5 meetings, sent 12 emails, reviewed 3 PRDs"
**Good:** "Validated onboarding redesign with 8 users - 75% said it's clearer than current flow"

### ❌ Vague Progress Updates

**Bad:** "Making good progress on the API integration"
**Good:** "API integration 70% complete - Auth flow done, payment flow testing, shipping Friday"

### ❌ Buried Blockers

**Bad:** "Working through some challenges with the legal review process"
**Good:** "🚨 Blocker: Legal review pending for 2 weeks, need escalation to ship by Q1"

### ❌ No Clear Asks

**Bad:** "Looking forward to feedback"
**Good:** "Need: Design review by Wed to stay on track for Friday launch"

### ❌ TMI (Too Much Information)

**Bad:** 10 paragraphs of every task you did
**Good:** 3 key outcomes + link to details

### ❌ Sandbagging Problems

Don't hide risks hoping they'll resolve. Flag them early.

**Bad:** Mentioning a blocker for the first time when it's already caused a delay
**Good:** Mentioning risks when they're still manageable

---

## Pro Tips

### 1. Lead With Impact

Start with outcomes, not activities. What changed as a result of your work?

### 2. Use Consistent Format

Pick a format and stick with it. Makes it easier for people to scan week-over-week.

### 3. Be Honest About Blockers

Your job isn't to hide problems. It's to surface them early so they can be solved.

### 4. Make Asks Explicit

Don't hint. Clearly state: "I need X from Y by Z" or "No help needed"

### 5. Track Your Wins

Keep a running "wins" doc. Makes updates easier and helps with performance reviews.

### 6. Link Don't Repeat

Reference PRDs, docs, and previous updates instead of re-explaining context.

### 7. Celebrate Others

Call out teammates who helped you. Builds goodwill and visibility for them.

---

## Integration With Other Commands

### After Meeting Notes

```
Use `/meeting-notes` throughout the week.
Then use `/status-update` on Friday.

I'll pull:
- Decisions from your meetings
- Action items you completed
- Blockers that surfaced
- Customer insights you captured
```

### Before 1:1s

```
Use `/status-update` to prep for your manager 1:1.

I'll format it as:
- Wins (self-advocacy)
- Blockers (where you need help)
- Discussion topics (drive the agenda)
- Commitments (accountability)
```

### For Launch Updates

```
After a launch, use `/status-update` with "launch update" context.

I'll include:
- What shipped
- Early metrics
- User feedback
- Next iteration plans
```

---

## Weekly Update Workflow

**Monday morning:**
- Review last week's commitments
- Note what shipped or moved forward

**Throughout the week:**
- Keep a "wins" scratch pad
- Note blockers as they come up
- Track metrics in flight

**Friday afternoon:**
- Use `/status-update`
- I'll pull from your week's work
- Review and send

---

## After I Create Your Update

```
Here's your status update!

**Want me to:**
- [ ] Make it shorter (condense to key points)
- [ ] Make it more detailed (add context)
- [ ] Adjust tone (more formal/casual)
- [ ] Create versions for different audiences
- [ ] Draft a Slack message to share this
- [ ] Add metrics or data visualization
- [ ] Flag patterns or concerns I noticed

What would help?
```

---

## Special Situations

### When Everything is On Fire 🔥

```markdown
# Status Update: [Date] - URGENT

## 🚨 Critical Situation

**What happened:** [Incident/crisis in one sentence]

**Current status:** [Where things stand right now]

**Impact:**
- Users affected: [Number/percentage]
- Business impact: [Revenue/reputation/etc.]
- Timeline: [How long has this been happening]

## Immediate Actions Taken

1. [Action] - [Owner] - [Status]
2. [Action] - [Owner] - [Status]
3. [Action] - [Owner] - [Status]

## Root Cause

[What went wrong - be honest and technical]

## Next Steps

**In the next 24 hours:**
- [Action] - [Owner]
- [Action] - [Owner]

**This week:**
- [Action] - [Owner]

## Prevention

[What we're doing to prevent this from happening again]

## Help Needed

[Specific escalations or resources needed]
```

### When You're Behind

```markdown
# Status Update: [Date] - Adjusted Timeline

## Situation

**Original target:** [Date for milestone]
**New target:** [Date for milestone]
**Reason:** [Honest explanation]

## What Happened

[Clear, non-defensive explanation of why timeline shifted]

## Impact

**Who this affects:** [Teams/stakeholders]
**Dependencies:** [What's now blocked or delayed]
**Mitigation:** [How you're minimizing impact]

## Revised Plan

[New milestones and dates]

## Lessons Learned

[What you'll do differently next time]

## Discussion

[Open for questions and feedback]
```

### When You're Ahead of Schedule

```markdown
# Status Update: [Date] - Accelerated Progress

## Good News

We're ahead of schedule on [initiative]!

**Original timeline:** [X]
**Current pace:** [Y weeks ahead]
**Why:** [What went right]

## Options

Given the extra time, we could:
1. [Option A] - [Pros/cons]
2. [Option B] - [Pros/cons]
3. Ship early and move to next priority

**Recommendation:** [Your suggestion]

**Need decision by:** [Date] to capitalize on momentum
```

---

## Output Integration

### Where Files Go

**Status updates:**
- Weekly/recurring: Save to `outputs/status-updates/[date]-[audience].md`
- Archive: Move finalized updates to `context-library/meetings/status-updates/` for historical record
- Share: Send directly or paste into Slack/email

### Link to Other Work

After creating status update:
- **Share with team** - Post to Slack or email to stakeholders
- **Update PRDs** - Feature progress gets reflected in PRD status
- **Track metrics** - Reference current metric values and progress
- **Follow up on blockers** - Schedule follow-ups on items that need resolution
- **Archive for 1:1** - Use this in your manager 1:1 prep

### Cross-Skill Integration

**Feeds into:**
- Team alignment - Status updates keep stakeholders informed
- Manager 1:1s - Status gives your manager context for your work
- Quarterly reviews - Status updates are artifacts for performance reviews
- Strategy evaluation - Metric progress ties back to strategy

**Pulls from:**
- `/meeting-notes` - Recent decisions and action items from meetings
- `/prd-draft` - Feature status and progress on PRDs
- `/feature-results` - Shipped feature performance
- `/metrics-framework` - Current metric values and movement
- `context-library/strategy/` - Strategic context and goals

---

---

## Output Quality Self-Check

Before delivering the status update, verify:

- [ ] **Outcomes over activities:** Every bullet describes an outcome or impact, not just a task completed
- [ ] **Specificity:** Numbers, dates, and names are included -- no vague "making progress" language
- [ ] **Blocker clarity:** Each blocker has a specific ask, a named person, and a deadline
- [ ] **Strategic tie-in:** At least one accomplishment connects to a strategic pillar or OKR
- [ ] **Audience-appropriate tone:** Executive updates lead with impact; team updates lead with details
- [ ] **Actionable next steps:** Every "next week" item has a clear deliverable and date
- [ ] **No buried risks:** Risks and blockers are visible, not hidden in prose
- [ ] **Consistent format:** Matches the format used in previous updates (if any exist)
- [ ] **Right length:** Daily = 3-4 bullets, Weekly = 5-7 sections, Executive = 1-page max
- [ ] **Human voice:** Reads like the PM wrote it, not like AI generated it

If any check fails, revise before delivering.

---

**Remember:** Great status updates make collaboration easier. They surface problems early, celebrate wins publicly, and keep everyone aligned without requiring meetings.
