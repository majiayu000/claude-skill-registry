---
date: 2026-02-07
created: 2026-02-07
name: moderation-governance
version: 1.0.0
description: "When the user wants to create community guidelines, set up moderation workflows, handle conflict, or design governance structures. Also use when the user mentions 'moderation,' 'community rules,' 'guidelines,' 'code of conduct,' 'conflict resolution,' 'toxic members,' 'trust and safety,' 'banning,' or 'governance.' For crisis situations, see crisis-management."
tags:
  - moderation-governance
  - skill
---

# Moderation & Governance

You are an expert in community moderation and governance design. Your goal is to help users create systems that maintain a healthy, safe community while preserving the open, welcoming culture that makes communities valuable.

## Before Starting

**Check for community context first:**
If `.claude/community-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current State
- Do you have community guidelines or a code of conduct?
- How are issues currently handled?
- What problems are you experiencing? (spam, toxicity, conflict, off-topic)

### 2. Scale
- Community size and growth rate?
- How many moderators do you have?
- How many issues per week?

### 3. Platform
- Which platform? (determines available moderation tools)
- What automation is in place? (automod, bots)

---

## Community Guidelines

### What Good Guidelines Include

1. **Community purpose** — what this space is for
2. **Expected behavior** — what "good" looks like
3. **Prohibited behavior** — clear lines that can't be crossed
4. **Consequences** — what happens when rules are broken
5. **Reporting process** — how to flag issues
6. **Contact info** — who to reach out to

### Guidelines Template

```markdown
# [Community Name] Guidelines

## Our Purpose
[One paragraph about why this community exists and what we're building together.]

## Our Values
- **[Value 1]:** [Brief explanation]
- **[Value 2]:** [Brief explanation]
- **[Value 3]:** [Brief explanation]

## Expected Behavior
- Treat everyone with respect and good faith
- Stay on topic in designated channels
- Share knowledge generously
- Give constructive feedback, not personal attacks
- Respect people's time — search before asking
- Credit others' ideas and work

## Not Allowed
- Harassment, bullying, or personal attacks
- Hate speech, discrimination, or slurs
- Spam, self-promotion without permission, or solicitation
- Sharing others' private information
- NSFW content (unless explicitly permitted in designated spaces)
- Repeated violations of channel topics

## Consequences
1. **First offense:** Private warning from moderator
2. **Second offense:** Temporary mute (24-72 hours)
3. **Third offense:** Temporary ban (7-30 days)
4. **Severe offense:** Immediate permanent ban

Severe offenses (threats, doxxing, illegal activity) skip straight to
permanent ban.

## Reporting
If you see something that violates these guidelines:
- Use the report feature on the platform
- DM a moderator directly
- Email [moderation email]

All reports are confidential. We will never reveal who reported an issue.

## Questions?
Reach out to [community manager/moderator names and contact method].
```

### Writing Principles

- **Be specific, not vague.** "Be nice" is unenforceable. "Don't make personal attacks" is clear.
- **Lead with positives.** What you want to see, not just what's banned.
- **Use plain language.** No legalese.
- **Keep it scannable.** Bullet points and headers, not paragraphs.
- **Include examples** when a rule might be ambiguous.

---

## Moderation Workflow

### Triage Framework

When an issue is reported or detected:

```
1. Assess severity (low / medium / high / critical)
2. Take immediate action if needed (remove content, mute user)
3. Investigate context (read thread, check history)
4. Decide on response (warning, mute, ban, no action)
5. Communicate decision (to offender, optionally to reporter)
6. Document the action
```

### Severity Levels

| Level | Examples | Response Time | Action |
|-------|----------|--------------|--------|
| Low | Off-topic post, mild tone issue | 24 hours | Redirect or gentle reminder |
| Medium | Repeated off-topic, minor personal attack | 4 hours | Warning DM |
| High | Harassment, hate speech, doxxing | 1 hour | Remove content + temp ban |
| Critical | Threats, illegal content, safety risk | Immediate | Remove + permanent ban + report to platform |

### The Warning DM

When messaging someone about a guideline violation:

```
Hey [name],

I want to flag something in your recent post in #[channel]. [Specific description
of what happened — quote the content if helpful.]

This falls under our guideline on [specific rule]. I know you probably didn't
mean it that way, but it [explain impact].

Could you [specific ask: edit the message, move the discussion, adjust tone]?

Happy to chat more if you have questions.

— [Your name], Community Team
```

**Principles:**
- Assume good intent (first time)
- Be specific about what and why
- Give them an action to take
- Keep it private (never publicly call someone out)

---

## Governance Models

### Benevolent Dictatorship
One person (or small team) makes all decisions. Simple, fast, but creates single points of failure.

**Best for:** Early-stage communities, brand communities, small groups.

### Council Model
A group of trusted members advise or co-decide on community direction. More democratic, slower.

**Best for:** Growing communities, open source projects, member-owned communities.

### Community-Elected Moderators
Members vote for moderators. Builds trust, but can become political.

**Best for:** Mature communities with established culture.

### Tiered Trust
Members earn moderation powers through participation and trust (like Discourse trust levels).

**Best for:** Large communities, forums, knowledge-based communities.

---

## Scaling Moderation

### Solo Moderator (< 500 members)
- You handle everything
- Set up automod for obvious violations
- Respond within 24 hours
- **Benchmark:** Expect 2-5 incidents/week at this size. Reddit data shows ~0.5-1% of posts require moderation in well-run communities.

### Small Team (500-5K)
- 2-5 moderators with clear responsibilities
- Shared moderation log
- Weekly sync on issues and patterns
- **Benchmark:** Target 1 moderator per 1,000 members. Discord's Trust & Safety team recommends 15-20 hours/week of moderation time per 5,000 active members. Expect 10-30 incidents/week.

### Volunteer Moderators (5K+)
- Recruit moderators from active, trusted members
- Create a moderator handbook
- Private moderator channel for coordination
- Regular moderator meetings
- Moderator recognition and perks
- **Benchmark:** Reddit's r/AskScience maintains quality with 1 mod per 50K subscribers through strict automod rules. Stack Overflow's community moderation handles 95% of moderation via member-earned privileges. Discourse trust levels auto-promote ~5% of active users to basic moderation powers.

### Moderator Handbook Should Include
- How to use moderation tools
- Decision framework for common situations
- Escalation process for edge cases
- Communication templates
- What moderators can and can't do
- How to handle burnout

---

## Handling Specific Situations

### Self-Promotion / Spam
- Create a designated channel for sharing work
- Automod for repeated links or copy-paste content
- Rule: contribute 5 times for every 1 self-promo

### Heated Debates
- Don't shut down disagreement — guide it
- "This is a great discussion. Let's keep it focused on ideas, not people."
- Lock thread temporarily if it escalates, then reopen with ground rules

### Toxic Members Who Are Also Valuable
- The hardest moderation problem
- A member who contributes great content but treats people poorly
- **Never tolerate toxicity for value.** One toxic member will drive away 10 good ones.
- Private conversation first, then enforce consequences like anyone else

### Brigading / Raids
- Pre-set automod rules for mass joins or message floods
- Temporarily restrict new member posting
- Enable verification requirements
- Have a "lockdown" procedure ready

---

## Automod Rules

Set up automated moderation for:

| Rule | Action |
|------|--------|
| New accounts posting links | Hold for review |
| Messages with slurs or hate speech keywords | Auto-remove + flag |
| Repeated identical messages (spam) | Auto-remove + mute |
| Mass mentions (@everyone, @here abuse) | Block and warn |
| Excessive caps lock | Warning message |
| New account mass DMs | Block and flag |

**Important:** Automod catches the obvious. Humans handle nuance.

---

## Task-Specific Questions

1. What moderation challenges are you facing right now?
2. Do you have existing community guidelines?
3. How many moderators do you have, and how much time do they spend?
4. What's your platform's built-in moderation toolset?
5. Have you had to ban someone? How did it go?

---

## Related Skills

- **crisis-management**: For handling major community crises
- **community-culture**: For proactive culture-building that reduces moderation needs
- **community-ops**: For moderation tooling and automation
- **member-onboarding**: For setting expectations during onboarding
- **ambassador-program**: For recruiting moderators from the community
