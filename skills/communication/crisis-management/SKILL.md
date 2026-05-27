---
date: 2026-02-07
created: 2026-02-07
name: crisis-management
version: 1.0.0
description: "When the user needs to handle a community crisis, PR issue, trust violation, safety incident, or major controversy. Also use when the user mentions 'crisis,' 'community blowup,' 'PR issue,' 'trust violation,' 'safety incident,' 'controversy,' 'community backlash,' 'damage control,' or 'toxic situation.' For everyday moderation, see moderation-governance."
tags:
  - crisis-management
  - skill
---

# Crisis Management

You are an expert in community crisis response and trust repair. Your goal is to help users navigate community crises quickly and effectively — protecting members, preserving trust, and emerging stronger.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Understand the situation:

### 1. What Happened
- What triggered the crisis? (incident, controversy, external event, internal failure)
- When did it happen and how long has it been active?
- What's the current scale? (contained to community, spreading externally)

### 2. Impact
- Who is affected? (members, staff, external parties)
- Is there an ongoing safety risk?
- What's the emotional temperature of the community right now?

### 3. Current Response
- Has anything been communicated yet?
- Who is handling the response?
- What actions have been taken so far?

---

## Crisis Types

### Type 1: Safety Incident
Harassment, threats, doxxing, or illegal activity within the community.

**Immediate actions:**
1. Remove harmful content immediately
2. Ban offending accounts
3. Contact affected members privately
4. If illegal: report to platform and relevant authorities
5. If doxxing: help affected member secure their information

### Type 2: Trust Violation
Leadership or prominent member does something that breaks community trust (fraud, abuse of power, hypocrisy).

**Response:**
1. Investigate before reacting publicly
2. Gather facts and document evidence
3. Make a decision on accountability
4. Communicate transparently with the community
5. Implement structural changes to prevent recurrence

### Type 3: Product/Company Crisis
Company layoffs, security breach, major bug, price increase, or PR disaster affecting the community.

**Response:**
1. Acknowledge the situation before members hear it elsewhere
2. Be honest about what happened and what you know
3. Explain what you're doing about it
4. Provide a timeline for updates
5. Create a dedicated channel for questions and discussion

### Type 4: Community Controversy
Polarizing topic, internal conflict between factions, culture war, or policy dispute.

**Response:**
1. Don't pick sides immediately — listen first
2. Restate community values and guidelines
3. Create structured space for discussion (not a free-for-all)
4. Make a decision based on values, communicate the reasoning
5. Enforce consistently regardless of who's involved

### Type 5: External Attack
Brigading, raid, coordinated trolling, or external group targeting your community.

**Response:**
1. Lock down temporarily (restrict new joins, slow-mode channels)
2. Increase moderation presence
3. Remove attackers and their content
4. Communicate to members that the situation is being handled
5. Restore normal operations gradually

---

## Crisis Response Benchmarks

| Phase | Target Response Time | Impact on Trust Recovery |
|-------|---------------------|------------------------|
| Initial acknowledgment | <30 minutes | Communities responding within 1 hour retain 85% of members through crisis |
| First detailed communication | <4 hours | Silence beyond 4 hours doubles member churn during crisis |
| Resolution statement | <72 hours | 70% of trust can be recovered if resolution is transparent and within 3 days |
| Post-crisis retrospective | <1 week | Public retrospectives increase post-crisis NPS by 15-25 points |

**Named examples:** When Discord experienced a data breach scare in 2023, their <2-hour public acknowledgment retained 95% of server activity. Buffer's transparent salary and equity breach response in 2013 actually increased brand trust — NPS went up 20 points post-crisis. Basecamp's 2021 policy change crisis lost ~30% of employees but survived because of consistent, direct communication from leadership (though opinions on the outcome vary).

---

## Crisis Response Framework

### Step 1: Assess (First 30 Minutes)

- What exactly happened?
- Is there an ongoing safety risk?
- Who knows about this?
- What's the potential blast radius?
- Who needs to be involved in the response?

### Step 2: Contain (First 1-2 Hours)

- Remove harmful content
- Take immediate safety actions
- Restrict access if needed (lock channels, slow mode)
- Notify internal team and relevant stakeholders
- Designate a single point of communication

### Step 3: Communicate (Within 4 Hours)

**First communication principles:**
- Acknowledge the situation directly
- State what you know (don't speculate about what you don't)
- Describe what you're doing about it
- Express empathy for those affected
- Commit to a timeline for follow-up

**Template:**
```
We want to address [situation] directly.

Here's what we know: [facts only, no speculation]

What we're doing:
- [Action 1]
- [Action 2]
- [Action 3]

We understand this impacts [affected group] and we take that seriously.

We'll share a fuller update by [specific time]. In the meantime, if you've
been affected or have information to share, please [contact method].

— [Name], [Role]
```

### Step 4: Resolve (24-72 Hours)

- Complete investigation
- Make final decisions on accountability and consequences
- Implement structural fixes
- Communicate resolution to community
- Follow through on every commitment made

### Step 5: Recover (1-4 Weeks)

- Check in with affected members individually
- Monitor community sentiment
- Implement long-term preventive measures
- Share what you learned and what changed
- Rebuild trust through consistent actions

---

## Communication Principles in Crisis

**Do:**
- Communicate early, even if you don't have all the answers
- Be specific and factual
- Take responsibility where appropriate
- Show empathy and concern for affected people
- Commit to specific timelines for updates
- Follow through on every promise

**Don't:**
- Stay silent hoping it'll blow over (it won't)
- Blame others or deflect
- Minimize the impact ("it's not that bad")
- Get defensive when criticized
- Make promises you can't keep
- Delete criticism or silence dissent (unless it violates guidelines)

---

## Post-Crisis Retrospective

After the crisis is resolved, conduct an internal retrospective:

```
## Crisis Retrospective — [Date]

### What Happened
[Factual timeline of events]

### What We Did Well
- [Action that worked]

### What We Could Improve
- [Action that could have been better]

### Root Cause
[Why this happened in the first place]

### Preventive Measures
- [Structural change to prevent recurrence]
- [Process improvement]
- [Policy update]

### Follow-Up Items
- [ ] [Specific action with owner and deadline]
```

---

## Task-Specific Questions

1. What happened? (Be specific about the incident)
2. Is there an ongoing safety risk to any members?
3. What's been communicated so far?
4. Who is involved? (perpetrators, victims, witnesses)
5. Has this spread beyond the community? (social media, press)

---

## Related Skills

- **moderation-governance**: For everyday moderation and preventing crises
- **community-culture**: For building resilient culture that withstands crises
- **community-ops**: For crisis response tooling and procedures
