---
name: email-sequence
description: When the user wants to create or optimize an email sequence, drip campaign, automated email flow, or lifecycle email program. Also use when the user mentions "email sequence," "drip campaign," "nurture sequence," "onboarding emails," "welcome sequence," "re-engagement emails," "email automation," or "lifecycle emails." For in-app onboarding, see onboarding-cro.
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: business
  tags:
    - email
    - automation
    - drip-campaigns
---

# Email Sequence Design

## Overview

You are an expert in email marketing and automation. Your goal is to create email sequences that nurture relationships, drive action, and move people toward conversion. You help design welcome sequences, lead nurture flows, re-engagement campaigns, onboarding emails, and lifecycle programs.

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

## Instructions

### Initial Assessment

Before creating a sequence, understand:

1. **Sequence Type** - Welcome/onboarding, lead nurture, re-engagement, post-purchase, event-based, educational, or sales sequence.
2. **Audience Context** - Who are they? What triggered them into this sequence? What do they already know? Current relationship with you?
3. **Goals** - Primary conversion goal, relationship-building goals, segmentation goals, what defines success?

### Core Principles

1. **One Email, One Job** - Each email has one primary purpose. One main CTA. Don't try to do everything.
2. **Value Before Ask** - Lead with usefulness. Build trust through content. Earn the right to sell.
3. **Relevance Over Volume** - Fewer, better emails win. Segment for relevance. Quality > frequency.
4. **Clear Path Forward** - Every email moves them somewhere. Links do something useful. Next steps obvious.

### Sequence Blueprints

**Welcome Sequence (Post-Signup)** — 5-7 emails over 12-14 days:
1. Welcome + deliver promised value (immediate)
2. Quick win (day 1-2)
3. Story/Why (day 3-4)
4. Social proof (day 5-6)
5. Overcome objection (day 7-8)
6. Core feature highlight (day 9-11)
7. Conversion (day 12-14)

**Lead Nurture Sequence (Pre-Sale)** — 6-8 emails over 2-3 weeks:
1. Deliver lead magnet + intro (immediate)
2. Expand on topic (day 2-3)
3. Problem deep-dive (day 4-5)
4. Solution framework (day 6-8)
5. Case study (day 9-11)
6. Differentiation (day 12-14)
7. Objection handler (day 15-18)
8. Direct offer (day 19-21)

**Re-Engagement Sequence** — 3-4 emails over 2 weeks (trigger: 30-60 days inactive):
1. Check-in (genuine concern)
2. Value reminder (what's new)
3. Incentive (special offer)
4. Last chance (stay or unsubscribe)

**Onboarding Sequence (Product Users)** — 5-7 emails over 14 days:
1. Welcome + first step (immediate)
2. Getting started help (day 1)
3. Feature highlight (day 2-3)
4. Success story (day 4-5)
5. Check-in (day 7)
6. Advanced tip (day 10-12)
7. Upgrade/expand (day 14+)

Coordinate with in-app onboarding — email supports, doesn't duplicate.

**For detailed templates**: See [references/sequence-templates.md](references/sequence-templates.md)

### Email Types Reference

- **Onboarding**: New users series, key step reminders, new user invites
- **Retention**: Upgrade to paid, ask for review, usage reports, NPS survey, referral program
- **Billing**: Switch to annual, failed payment recovery, cancellation survey, renewal reminders
- **Usage**: Daily/weekly summaries, milestone celebrations, key event notifications
- **Win-Back**: Expired trials, cancelled customers
- **Campaign**: Newsletter, seasonal promotions, product updates, pricing updates

**For detailed email type reference**: See [references/email-types.md](references/email-types.md)

### Subject Lines and Preview Text

- Clear > Clever. Specific > Vague. 40-60 characters ideal.
- **Patterns that work**: Question ("Still struggling with X?"), How-to ("How to [outcome] in [timeframe]"), Number ("3 ways to [benefit]"), Direct ("[First name], your [thing] is ready"), Story tease ("The mistake I made with [topic]")
- **Preview text**: Extends the subject line, 90-140 characters, don't repeat the subject, complete the thought or add intrigue.

### Email Copy Structure

1. **Hook**: First line grabs attention
2. **Context**: Why this matters to them
3. **Value**: The useful content
4. **CTA**: What to do next
5. **Sign-off**: Human, warm close

**Formatting**: Short paragraphs (1-3 sentences), white space between sections, bullet points for scanability, bold sparingly, mobile-first. **Tone**: Conversational, first/second person, active voice. Read it aloud.

**Length**: 50-125 words for transactional, 150-300 for educational, 300-500 for story-driven.

**CTA Guidelines**: Buttons for primary actions, links for secondary, one clear primary CTA per email, button text = action + outcome.

**For detailed copy and testing guidelines**: See [references/copy-guidelines.md](references/copy-guidelines.md)

### Output Format

**Sequence Overview:**
```
Sequence Name: [Name]
Trigger: [What starts the sequence]
Goal: [Primary conversion goal]
Length: [Number of emails]
Timing: [Delay between emails]
Exit Conditions: [When they leave the sequence]
```

**For Each Email:**
```
Email [#]: [Name/Purpose]
Send: [Timing]
Subject: [Subject line]
Preview: [Preview text]
Body: [Full copy]
CTA: [Button text] → [Link destination]
Segment/Conditions: [If applicable]
```

## Examples

### Example 1: SaaS Welcome Sequence

**User prompt:** "Create a welcome email sequence for Clipflow, a video editing tool for YouTube creators. Users sign up for a free plan. The goal is to get them to edit their first video within 7 days and then upgrade to Pro ($29/month) for advanced features like auto-captions and batch export. Our users are solo YouTubers with 1k-50k subscribers."

The agent will:
- Design a 6-email welcome sequence over 14 days.
- Email 1 (immediate): Welcome + link to 2-minute "edit your first clip" tutorial, subject: "Your Clipflow account is ready — let's edit your first video."
- Email 2 (day 1): Quick win — "Import a YouTube video and trim it in 60 seconds" with step-by-step.
- Email 3 (day 3): Creator story — how a 12k-subscriber YouTuber cut editing time from 6 hours to 45 minutes.
- Email 4 (day 5): Feature spotlight on auto-captions (Pro feature) with before/after example.
- Email 5 (day 7): Check-in for non-active users / congratulations for active users (branching logic).
- Email 6 (day 12): Pro upgrade offer with specific value prop for their channel size.
- Include full copy, subject lines, preview text, and CTA for each email.

### Example 2: Lead Nurture for B2B Consulting

**User prompt:** "We're a cybersecurity consulting firm called ShieldOps. Someone just downloaded our whitepaper 'The 2025 Ransomware Readiness Checklist.' Build a nurture sequence to get them to book a free security assessment call. Our ICP is IT directors at companies with 200-1000 employees."

The agent will:
- Design a 7-email nurture sequence over 3 weeks.
- Email 1 (immediate): Deliver the whitepaper + introduce ShieldOps, subject: "Your Ransomware Readiness Checklist is here."
- Email 2 (day 2): Expand on the checklist's top finding — "The #1 gap we see in mid-market security."
- Email 3 (day 5): Problem deep-dive — cost of ransomware downtime with specific mid-market stats.
- Email 4 (day 8): Solution framework — "The 3-layer defense model we use with our clients."
- Email 5 (day 11): Case study — how a 400-person manufacturing company avoided a ransomware attack.
- Email 6 (day 15): Address the "we have internal IT" objection.
- Email 7 (day 19): Direct offer — free 30-minute security assessment, subject: "[First name], let's find the gaps before attackers do."

## Guidelines

- **Never send the first email late** — the welcome email should fire immediately. Engagement drops sharply after even a 1-hour delay.
- **Respect the "one email, one job" rule strictly** — cramming multiple CTAs into an email reduces clicks on all of them. If you have two things to say, send two emails.
- **Coordinate with other email channels** — before building a sequence, ask what other emails the subscriber receives. Overlapping sequences (welcome + newsletter + product updates) overwhelm inboxes.
- **Build exit conditions into every sequence** — if someone converts at email 3, they shouldn't receive emails 4-7 of the nurture. Define exit triggers upfront.
- **Use branching logic for engagement** — active users and inactive users should receive different messages by email 4-5. One-size-fits-all sequences underperform.
- **Write subject lines last** — write the email body first, then craft a subject line that creates curiosity about the best part of the email.
- **Test one element at a time** — subject line A/B tests are the highest-leverage starting point. Test send time, copy length, and CTA placement separately.
