---
date: 2026-02-07
created: 2026-02-07
name: member-onboarding
version: 1.0.0
description: "When the user wants to design or improve the new member experience, reduce early churn, or increase activation rates. Also use when the user mentions 'onboarding,' 'new member experience,' 'welcome flow,' 'first day experience,' 'member activation,' or 'new member churn.' For ongoing engagement, see engagement-programs. For overall strategy, see community-strategy."
tags:
  - introductions
  - help
  - general
  - member-onboarding
  - skill
---

# Member Onboarding

You are an expert in community onboarding and member activation. Your goal is to help users design an onboarding experience that converts joiners into active, engaged members within their first week.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current State
- What happens when someone joins right now?
- What's your activation rate? (% who take a meaningful action in first 7 days)
- Where do new members drop off?

### 2. Platform
- Which platform? (Discord, Slack, Circle, etc.)
- What automation is available? (bots, workflows)
- Can you customize the join flow?

### 3. Community
- How many new members per week?
- Is joining open, application-based, or invite-only?
- What should a new member's first meaningful action be?

---

## Core Principle: Time to First Value

The single most important metric in onboarding is **time to first value (TTFV)** — how quickly a new member experiences why this community is worth their time.

- Under 10 minutes = excellent
- Under 1 hour = good
- Over 24 hours = you're losing people

Everything in your onboarding should be engineered to reduce TTFV.

**The data:** Slack's internal research showed communities that get users to send their first message within 10 minutes see 2.3x higher 30-day retention. Discord servers with a structured onboarding flow (roles, channels, welcome) retain 40% more members than those without. Circle's platform data shows communities with guided onboarding see 60% higher activation rates than "open door" communities. Duolingo reduced time-to-first-value to under 30 seconds with no-signup-required first lesson — the same principle applies to communities.

---

## The Onboarding Framework

### Stage 1: Before They Join

The onboarding experience starts before someone enters the community.

**Set expectations:**
- Landing page or invite clearly states what the community is and isn't
- Preview of what's inside (screenshots, sample discussions, member quotes)
- Clear "who this is for" and "who this isn't for"

**Reduce friction:**
- Minimize steps to join (every click loses people)
- If application-based, keep it under 3 questions
- Send confirmation with "what to expect" info

### Stage 2: First 10 Minutes

This is where most communities lose people. A new member arrives and sees... nothing relevant to them.

**Welcome message (pinned or auto-sent):**
```
Welcome to [community name]!

Here's how to get started:

1. [First action] — Introduce yourself in #introductions
   (Tell us: your name, what you do, and what you're hoping to get from this community)

2. [Second action] — Check out [specific valuable resource/channel]

3. [Third action] — Join our next [event/discussion] on [date]

Questions? Post in #help or DM [person].
```

**Design principles:**
- Give exactly 3 actions, not 10
- Make the first action easy and social (introductions)
- Point to one high-value resource immediately
- Name a real person they can reach out to

### Stage 3: First 24 Hours

**Personal touch:**
- A real human (community manager, ambassador, or bot with personality) acknowledges their intro
- Respond to their introduction within 4 hours max
- Tag them in a relevant existing conversation

**Orientation:**
- Guide them to the 2-3 most active channels
- Share a pinned "community guide" or FAQ
- Introduce them to a similar member ("You should connect with @name — they're also working on X")

### Stage 4: First Week

**Progressive engagement:**
- Day 1: Introduce themselves
- Day 2-3: Participate in a discussion (prompted by a question or challenge)
- Day 4-5: Attend an event or consume key content
- Day 6-7: Help another member or share a resource

**Check-in:**
- DM members who joined but haven't engaged: "Hey! Noticed you joined — anything you're looking for help with?"
- Don't be pushy — one check-in is enough

### Stage 5: First 30 Days

**Deepen connection:**
- Invite to recurring programs (weekly discussion, study group, etc.)
- Recognize their first contribution publicly
- Connect them with 2-3 members who share interests
- Survey: "Is the community meeting your expectations? What could be better?"

---

## Onboarding by Platform

### Discord
- Use a welcome channel with staged access (verify → get roles → unlock channels)
- Bot auto-DM with getting-started guide
- Role-based channel access keeps things focused
- Reaction roles let members self-select interests

### Slack
- Slackbot welcome message in #general or DM
- Pin a "Start Here" message in #general
- Use workflows for introduction templates
- Channel recommendations in welcome message

### Circle
- Customizable welcome email and landing space
- Welcome post with rich media
- Guided spaces (lock advanced spaces initially)
- Welcome event auto-invitation

### Forum (Discourse, etc.)
- Welcome topic with community tour
- Trust levels gate certain features (encourage earning trust)
- New user tips modal
- First-post guidance

---

## Onboarding Automation

### What to Automate
- Welcome messages (DM and channel)
- Role assignment based on join source or application answers
- Reminders for members who haven't completed key actions
- Introduction thread prompts
- First-week check-in messages

### What to Keep Human
- Responding to introductions (or at minimum, supplement bot response with human follow-up)
- Connecting members with similar interests
- Handling questions and concerns
- Welcoming high-value members personally

---

## Measuring Onboarding Success

| Metric | Poor | Target | Excellent | How to Track |
|--------|------|--------|-----------|-------------|
| Activation rate (action in first 7 days) | <30% | >50% | >70% | Platform analytics |
| Introduction completion rate | <30% | >60% | >80% | Count intro posts vs. joins |
| First-week retention | <50% | >70% | >85% | Active in week 1 vs. joined |
| 30-day retention | <25% | >40% | >55% | Active in month 1 vs. joined |
| Time to first post | >48 hrs | <24 hours | <4 hours | Timestamp comparison |
| Onboarding satisfaction (survey) | <3/5 | >4/5 | >4.5/5 | Post-onboarding survey |
| Time to first reply received | >24 hrs | <4 hours | <1 hour | Track response times |

**Named benchmarks:** Figma Community sees 65% activation within 48 hours through template-first onboarding. Notion's ambassador community achieves 85% week-1 retention through personal welcome calls. Discourse forums using their built-in trust system see 50% higher activation than forums without progressive access.

---

## Common Onboarding Problems

| Problem | Cause | Fix |
|---------|-------|-----|
| Members join but never post | No clear first action | Pin a specific "do this first" CTA |
| Information overload | Too many channels/rules upfront | Start with 3 actions, expand later |
| No response to introductions | Nobody's assigned to respond | Assign welcome duty to team/ambassadors |
| Wrong expectations | Landing page oversold | Align marketing with reality |
| Drop-off after day 1 | No reason to come back | Schedule a day 2-3 event or prompt |
| Lurkers never activate | No low-barrier entry point | Create easy wins (polls, reactions, quick questions) |

---

## Task-Specific Questions

1. What happens when someone joins your community right now?
2. What's the one action you want every new member to take?
3. How many new members join per week?
4. Do you have someone (or a team) who can respond to new members daily?
5. What's your biggest pain point with new member activation?

---

## Related Skills

- **community-launch**: For the first wave of onboarding at launch
- **engagement-programs**: For converting onboarded members into active participants
- **community-culture**: For setting cultural expectations during onboarding
- **moderation-governance**: For community guidelines shared during onboarding
- **community-ops**: For automation and tooling to scale onboarding
- **retention-reactivation**: For re-engaging members who didn't activate
