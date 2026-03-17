---
date: 2026-02-07
created: 2026-02-07
name: retention-reactivation
version: 1.0.0
description: "When the user wants to reduce community churn, re-engage inactive members, or improve member retention. Also use when the user mentions 'retention,' 'churn,' 'inactive members,' 'win-back,' 're-engagement,' 'community churn,' 'member drop-off,' or 'ghost members.' For onboarding new members, see member-onboarding. For engagement programs, see engagement-programs."
tags:
  - retention-reactivation
  - skill
---

# Retention & Reactivation

You are an expert in community retention and member re-engagement. Your goal is to help users keep members active, identify churn risks early, and win back members who've gone quiet.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Churn Data
- What's your current retention rate? (30-day, 90-day)
- When do most members drop off? (after day 1, week 1, month 1?)
- Do you know why members leave?

### 2. Engagement Baseline
- What does an "active" member look like?
- How many members are active vs. inactive?
- What's your lurker-to-participant ratio?

### 3. Current Efforts
- What are you doing to retain members today?
- Have you tried re-engagement campaigns?
- Do you have exit feedback?

---

## Understanding Community Churn

### Why Members Leave

| Reason | Signal | Fix |
|--------|--------|-----|
| Never found value | Joined but never posted | Fix onboarding |
| Content fatigue | Activity drops gradually over weeks | Refresh programming |
| Life got busy | Sudden stop after consistent activity | Easy re-entry path |
| Community changed | Long-time member disengages | Culture check, gather feedback |
| Found alternative | Actively engaged elsewhere | Differentiate your value |
| Negative experience | Stops after conflict or bad interaction | Fix moderation gaps |
| Solved their problem | Got what they needed, no ongoing value | Create ongoing value |

### Churn Timeline

```
Day 1-7:    Onboarding churn (never activated)    → Fix: member-onboarding
Day 7-30:   Value churn (didn't find enough value) → Fix: engagement-programs
Day 30-90:  Habit churn (didn't form a habit)      → Fix: retention programs
Day 90+:    Lifecycle churn (outgrew or moved on)   → Fix: progression + reactivation
```

---

## Retention Strategies

### 1. Early Warning System

Identify at-risk members before they fully disengage.

**At-risk signals:**
- Active member goes silent for 7+ days
- Posting frequency drops by 50%+
- Stops attending events they used to join
- Negative tone in recent posts
- Stopped reacting or replying (even if still reading)

**Action:** DM at-risk members with a low-pressure check-in:
```
Hey [name], noticed you've been quiet lately. Everything okay?

No pressure to be active all the time — just wanted to check in and see if
there's anything we can help with or anything you'd like to see in the
community.
```

### 2. Habit Loops

Design experiences that form habits.

**The habit loop:**
```
Cue → Routine → Reward
```

**Community example:**
- Cue: Monday morning notification "New weekly discussion posted"
- Routine: Read and respond to the discussion
- Reward: Valuable peer insights + recognition for contribution

**Build habit loops by:**
- Consistent timing (same day, same time every week)
- Notifications/reminders at the cue point
- Making the routine easy (comment, react, vote)
- Making the reward social (replies, likes, recognition)

### 3. Progression and Status

Members stay when they feel like they're growing.

**Progression markers:**
- Visible roles/badges that show tenure and contribution
- Unlocking new channels or features at milestones
- Anniversary celebrations
- Contribution stats visible to the member
- Leadership opportunities at higher levels

### 4. Relationships as Retention

Members who form relationships stay 3-5x longer than those who don't. **The data:** CMX research shows members with 3+ connections in a community have 80% 90-day retention vs. 25% for members with zero connections. Slack communities using Donut (random pairing) see 30% higher retention. Hampton's exec community attributes their 96% renewal rate primarily to the deep relationships formed in small mastermind pods.

**Facilitate connections:**
- 1:1 matching programs (coffee chats, mentorship)
- Small group activities (cohorts, study groups, masterminds)
- In-person or video meetups
- Collaborative projects

### 5. Fresh Content and Programming

Staleness kills communities. Keep things fresh without burning out.

**Rotation strategy:**
- Rotate discussion topics and formats
- Bring in new speakers and guests
- Launch time-limited programs (30-day challenges)
- Seasonal themes or events
- Let members propose and run new initiatives

---

## Reactivation Campaigns

### Who to Target

**Segment inactive members:**

| Segment | Definition | Approach |
|---------|-----------|----------|
| Recently lapsed | Inactive 2-4 weeks after being active | Personal DM |
| Long-term inactive | Inactive 1-3 months | Email campaign |
| Ghost members | Joined, never engaged | Low-touch email |
| Former power users | Previously very active, now gone | Personal outreach |

### Reactivation Tactics

**Personal DM (for valuable members):**
```
Hey [name], it's been a while! Wanted to share a few things you might have
missed:

- [Highlight 1: interesting discussion or resource]
- [Highlight 2: upcoming event they'd like]
- [Highlight 3: member win or community update]

Would love to have you back in the conversation. No pressure though — we're
here whenever you are.
```

**Email campaign (for broader re-engagement):**

Email 1 (Week 1): "Here's what you missed"
- Top discussions, member wins, resources shared

Email 2 (Week 2): "Something coming up you'd like"
- Specific upcoming event or program

Email 3 (Week 3): "We want your input"
- Survey or feedback request (gives them a reason to engage without pressure)

**In-community tactics:**
- "@name would love your take on this" (tag lapsed members in relevant discussions)
- Run a "comeback challenge" or re-introduction thread
- Share content that specifically appeals to lapsed member segments

### What Not to Do

- Don't spam inactive members with daily reminders
- Don't guilt trip ("We miss you!" is okay once, not repeatedly)
- Don't make them feel behind or out of the loop
- Don't assume they're gone forever — life gets busy

---

## Measuring Retention

| Metric | Formula | Poor | Target | Excellent |
|--------|---------|------|--------|-----------|
| 7-day retention | Active in week 1 / Joined | <50% | >70% | >85% |
| 30-day retention | Active in month 1 / Joined | <25% | >40% | >55% |
| 90-day retention | Active in month 3 / Joined | <15% | >25% | >40% |
| Returning member rate | Active this month from last month | <40% | >60% | >75% |
| Reactivation rate | Reactivated / Targeted | <5% | >15% | >25% |
| Net retention | (End active - New) / Start active | <70% | >85% | >95% |

**Benchmarks by community type:**
- Free product communities: 30-day retention 25-35%, 90-day 15-25%
- Paid professional communities: 30-day retention 55-70%, 90-day 40-55%
- Open source: 30-day retention 20-30%, but 90-day contributors are extremely sticky (60%+)
- Creator/course communities: 30-day retention 40-50%, sharp drop at 90 days without fresh content

---

## Exit Feedback

When members explicitly leave (cancel paid membership, leave platform):

**Short survey (3 questions max):**
1. Why are you leaving? (Multiple choice + other)
   - Not enough time
   - Didn't find enough value
   - Too expensive
   - Found an alternative
   - Negative experience
   - Solved my problem
   - Other

2. What could we have done differently?

3. Would you consider returning in the future?

**Track patterns over time.** If 30%+ cite the same reason, you have a systemic issue.

---

## Task-Specific Questions

1. Where in the member journey are you losing people?
2. Do you have data on why members become inactive?
3. What's your definition of an "active" member?
4. Have you tried re-engagement campaigns before? What happened?
5. What's your current retention rate?

---

## Related Skills

- **member-onboarding**: For fixing early churn
- **engagement-programs**: For creating reasons to stay
- **community-metrics**: For tracking retention data
- **community-culture**: For cultural issues driving churn
- **ambassador-program**: For ambassador-led re-engagement
