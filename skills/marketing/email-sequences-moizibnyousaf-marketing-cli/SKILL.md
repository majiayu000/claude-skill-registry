---
name: email-sequences
description: |
  Build automated email flows that nurture, convert, and retain. Creates complete sequences for welcome, nurture, launch, re-engagement, and onboarding with subject lines, body copy, timing, and A/B test plans. Use when someone needs email automation, a drip campaign, welcome series, launch emails, post-purchase emails, abandoned cart recovery, or says 'email sequence', 'drip campaign', 'welcome series', 'onboarding emails', 'nurture flow', 'automated emails', 'email marketing', 'retention emails', or 'lifecycle emails'. Even if they just say 'set up emails' or 'email strategy' without specifying 'sequence', this is likely the right skill. Includes deliverability rules and spam avoidance.
category: distribution
tier: must-have
reads:
  - brand/voice-profile.md
  - brand/audience.md
  - brand/positioning.md
writes:
  - marketing/emails/{sequence-name}/
depends-on:
  - brand-voice
  - audience-research
triggers:
  - email sequence
  - welcome series
  - nurture flow
  - launch emails
  - drip campaign
  - onboarding emails
  - re-engagement
  - email automation
  - win-back
  - email funnel
allowed-tools: []
---

> **Note:** Examples below use fictional brands (Acme, Lumi, Helm). Replace with your own brand context.

# Email Sequences

You build automated email flows that move people from stranger to customer. Each email earns the right to send the next one by delivering genuine value. No "just checking in" — every email has a job.

## On Activation

1. Read `brand/voice-profile.md` — emails are the most intimate channel, voice matters most here
2. Read `brand/audience.md` — understand awareness level, sophistication, pain points
3. Read `brand/positioning.md` — know the product angle and differentiation
4. If brand files don't exist, ask: What do you sell? Who's receiving these? What action do you want them to take?
5. Check `marketing/emails/` for existing sequences — avoid overlap

---

## Brand Integration

Brand files shape every email in the sequence:

- **voice-profile.md** → Tone across all emails. If voice is friendly/casual, open with 'Hey {{first_name}}!' and use contractions. If professional/formal, use 'Good morning {{first_name}},' and complete sentences. Voice consistency across a 7-email sequence is what builds trust.
- **audience.md** → Pain points drive email hooks. Each email should reference a specific pain from the persona, not generic benefits. If audience is time-starved founders, lead with efficiency. If audience is creative professionals, lead with inspiration.
- **positioning.md** → The unique angle appears in every CTA and subject line. Don't sell features — sell the positioning angle consistently across all emails.

---

## Sequence Types

| Type | Trigger | Goal | Length | Timing |
|------|---------|------|--------|--------|
| **Welcome** | New subscriber | Build trust, set expectations, deliver first value | 5-7 emails | Days 0, 1, 3, 5, 7, 10, 14 |
| **Nurture** | Post-welcome or lead magnet | Educate, build authority, warm up for offer | 5-10 emails | Every 2-3 days |
| **Launch** | Product launch or promotion | Create urgency, overcome objections, convert | 6-8 emails | Days -3, -1, 0, 0+6hr, 1, 3, 5, 7 |
| **Onboarding** | New customer/user | Activate, reduce churn, drive first success | 5-7 emails | Days 0, 1, 3, 5, 7, 14, 30 |
| **Re-engagement** | Inactive subscriber | Win back or clean list | 3-4 emails | Days 0, 3, 7, 14 |

**If the user's need doesn't fit a type above**, build a custom sequence: identify the trigger event, define the goal, pick an email count (3-7), and assign each email a single purpose from this palette: DELIVER, STORY, VALUE, PROOF, BRIDGE, PITCH, OBJECTION, CHECK-IN, BREAKUP. Space emails 2-3 days apart by default. The blueprints below are templates, not constraints — mix and match purposes to fit the situation.

---

## Email Anatomy

Every email has these components:

```yaml
---
sequence: welcome
position: 1
subject: "Your subject line here"
preview: "Preview text that complements (not repeats) the subject"
from_name: "First Name from Company"
send_delay: "0 days"  # relative to trigger
segment: all | engaged | inactive
personalization_tokens: ["first_name", "company"]
ab_test: null | { variant_b_subject: "Alternative subject" }
---
```

### Subject Lines

**The subject line gets the open. Nothing else matters if this fails.**

**Formulas that work:**

| Formula | Example | When to Use |
|---------|---------|-------------|
| Direct benefit | "Your 5-step content calendar" | Delivering promised value |
| Curiosity gap | "The email mistake I made for 3 years" | Nurture sequences |
| Personal question | "Quick question about your launch" | Re-engagement, sales |
| How-to | "How to write emails people actually read" | Educational content |
| Number + result | "3 tweaks that doubled our open rate" | Data-driven audiences |
| Story tease | "The worst marketing advice I ever got" | Storytelling brands |

**Rules:**
- 30-50 characters (6-10 words) — shorter is almost always better
- No ALL CAPS, no excessive punctuation, no emoji unless brand uses them
- Preview text adds context, never repeats the subject
- Personalization in subject only if natural ("{{first_name}}, quick question")

### Body Copy

**Structure every email the same way the reader processes it:**

1. **Hook** (first line) — Reason to keep reading. Personal, specific, unexpected.
2. **Context** (2-3 sentences) — Set up the value. Story, observation, or problem statement.
3. **Value** (core content) — The insight, tip, framework, or story. This is why they opened.
4. **Bridge** (1 sentence) — Connect the value to your CTA.
5. **CTA** (1 clear action) — One link, one ask. Button or text link.
6. **PS** (optional) — Second hook, social proof, or alternative CTA. Most-read line after the subject.

**Rules:**
- One CTA per email. One.
- Write at a 5th-grade reading level. Short sentences. Short paragraphs.
- 150-300 words for nurture. 300-500 for launch. Under 150 for re-engagement.
- Plain text outperforms HTML for most B2B. Light formatting for B2C.
- "Reply to this email" is the highest-trust CTA you can use early in a sequence.

---

## Sequence Blueprints

### Welcome Sequence (5-7 emails)

```
Email 1 (Day 0): DELIVER
- Subject: "Here's your [lead magnet / what they signed up for]"
- Body: Deliver the thing. One quick-start tip. Set expectations for what's coming.
- CTA: Download / access the resource

Email 2 (Day 1): STORY
- Subject: "Why I built [product/brand]"
- Body: Origin story. The problem you experienced. Why you care.
- CTA: Reply and tell me about your situation

Email 3 (Day 3): VALUE
- Subject: "The #1 mistake with [topic]"
- Body: Teach something genuinely useful. Quick win they can implement today.
- CTA: Try this technique / read more

Email 4 (Day 5): PROOF
- Subject: "How [customer] achieved [result]"
- Body: Case study or testimonial. Specific numbers. Before/after.
- CTA: See how it works / start your trial

Email 5 (Day 7): OFFER
- Subject: "[Product] might be right for you"
- Body: Direct pitch. What it does, who it's for, why now. Objection handling.
- CTA: Start trial / buy / book a call

Email 6 (Day 10): OBJECTION
- Subject: "The honest answer to [common concern]"
- Body: Address the #1 reason people don't buy. Be transparent.
- CTA: FAQ page or direct response

Email 7 (Day 14): LAST CHANCE
- Subject: "One more thing about [topic]"
- Body: Final value piece + last pitch. Soft close.
- CTA: Product link with a reason to act now
```

### Launch Sequence (6-8 emails)

```
Email 1 (Day -3): SEED
- Tease something coming. Build anticipation. No details yet.

Email 2 (Day -1): STORY
- The problem this product solves. Your journey building it.

Email 3 (Day 0, AM): ANNOUNCE
- It's live. What it is, what it does, who it's for. Early bird / launch price.

Email 4 (Day 0, PM): FAQ
- Answer the top 5 questions you've received. Overcome objections.

Email 5 (Day 1): PROOF
- First customer results, testimonials, social proof from launch day.

Email 6 (Day 3): DEEP DIVE
- Detailed walkthrough of one feature/benefit. Show, don't tell.

Email 7 (Day 5): OBJECTIONS
- Address remaining concerns directly. "Is this for me?" content.

Email 8 (Day 7): CLOSE
- Last chance. Deadline is real. Recap the offer. Final CTA.
```

### Re-engagement Sequence (3-4 emails)

```
Email 1 (Day 0): CHECK-IN
- Subject: "Still interested in [topic]?"
- Body: Acknowledge the silence. Offer your best piece of content.

Email 2 (Day 3): VALUE BOMB
- Subject: "[Best content title] — thought you'd want this"
- Body: Your single best-performing piece of content. No ask.

Email 3 (Day 7): PREFERENCE
- Subject: "Want fewer emails? (Or none?)"
- Body: Let them choose frequency or topics. Give them control.

Email 4 (Day 14): BREAKUP
- Subject: "Cleaning up my list"
- Body: "If I don't hear from you, I'll remove you. No hard feelings."
- CTA: "Keep me subscribed" button
```

### Nurture Sequence (5-10 emails)

```
Email 1 (Day 0): INSIGHT
- Subject: "The [topic] framework that changed everything"
- Body: Share a counterintuitive insight. Teach a mental model.
- CTA: Try this approach / read more

Email 2 (Day 3): STORY
- Subject: "What happened when [customer] tried [approach]"
- Body: Case study disguised as a story. Specific numbers. Relatable struggle.
- CTA: See how they did it

Email 3 (Day 6): FRAMEWORK
- Subject: "The 3-step process for [outcome]"
- Body: Actionable framework they can implement today. Quick win.
- CTA: Download the template / try step 1

Email 4 (Day 9): MYTH-BUST
- Subject: "Stop doing [common practice] — here's why"
- Body: Challenge conventional wisdom. Back up with evidence or experience.
- CTA: Try the alternative

Email 5 (Day 12): DEEP DIVE
- Subject: "Everything I know about [narrow topic]"
- Body: Your best content on a topic they care about. Thorough but scannable.
- CTA: Bookmark this / share with a colleague

Email 6+ (Every 3 days): ROTATE
- Alternate between: value emails, proof emails, and soft bridge emails
- Each email plants a seed for the product without pitching
- End the sequence with a natural transition to a conversion sequence
```

The goal of nurture is trust-building, not selling. Every email proves you understand their world. When the conversion sequence arrives, they already believe you can help — the pitch is a formality.

### Onboarding Sequence (5-7 emails)

```
Email 1 (Day 0): WELCOME
- Subject: "Welcome aboard — here's your quick start"
- Body: Confirm purchase/signup. One immediate action for first success.
- CTA: Complete first action (setup, first use, profile creation)

Email 2 (Day 1): QUICK WIN
- Subject: "Do this in 5 minutes for [specific result]"
- Body: Shortest path to first value. Step-by-step with screenshots if applicable.
- CTA: Complete the quick win

Email 3 (Day 3): DEEPER VALUE
- Subject: "Most people miss this feature"
- Body: Show a non-obvious capability. "Now that you've done X, try Y."
- CTA: Try the feature

Email 4 (Day 5): SOCIAL PROOF
- Subject: "How [customer] uses [product] daily"
- Body: Customer story showing regular use pattern. Make the habit concrete.
- CTA: Set up their version of the habit

Email 5 (Day 7): CHECK-IN
- Subject: "Quick question about your experience"
- Body: Ask how it's going. Offer help. Surface objections early.
- CTA: Reply with feedback or book a call

Email 6 (Day 14): ADVANCED
- Subject: "[Product] tip most users discover at month 2"
- Body: Power user tip. Show what's possible at full engagement.
- CTA: Try the advanced feature

Email 7 (Day 30): MILESTONE
- Subject: "You've been with us for a month"
- Body: Celebrate. Show what they've accomplished. Bridge to upgrade/expansion.
- CTA: Upgrade, refer a friend, or explore premium features
```

The onboarding sequence's job is activation — getting users to their first "aha moment" as fast as possible. Every email removes friction between signup and habit. If they don't get value in the first week, they're gone.

---

## Open Rate Optimization

| Factor | Best Practice |
|--------|--------------|
| Send time | Tue-Thu, 9-11am recipient's timezone |
| From name | Personal name > company name (test "Name from Company") |
| Subject length | 6-10 words, front-load the value |
| Preview text | Always set — complements, never repeats the subject |
| List hygiene | Remove 90-day inactive quarterly |
| Segmentation | Segment by engagement, not just demographics |

## A/B Testing Suggestions

For each sequence, suggest tests:

1. **Subject lines** (HIGH) — Test 2 variants per email, winner sends to remaining 80%
2. **Send time** (MEDIUM) — Morning vs afternoon, weekday vs weekend
3. **From name** (MEDIUM) — Personal vs brand vs "Name from Brand"
4. **CTA format** (LOW) — Button vs text link vs "reply to this email"
5. **Email length** (LOW) — Short (150 words) vs long (400 words)

---

## Worked Example

**Sequence: Welcome (verified meal delivery app)**

| # | Day | Subject | Hook | CTA |
|---|---|---|---|---|
| 1 | 0 | Welcome to Acme 🎉 | You just made verified-source ordering effortless | Browse restaurants near you |
| 2 | 1 | Your first order is on us | $10 off because trying new things should be easy | Use code FIRST10 |
| 3 | 3 | How we verify every restaurant | The story behind our third-party certification process | See our standards |
| 4 | 7 | Sarah's favorite weekly order | Real customer story: 'I stopped checking ingredients' | Order Sarah's picks |
| 5 | 14 | You haven't ordered yet? | Quick poll: what's holding you back? | Take 30-sec survey |

---

## Output Structure

```
marketing/emails/{sequence-name}/
├── sequence-plan.md        # Overview: type, trigger, goal, timing map
├── email-01-deliver.md     # Individual email with frontmatter
├── email-02-story.md
├── email-03-value.md
├── ...
└── ab-test-plan.md         # Suggested A/B tests for the sequence
```

**Integration**: All emails output in plain text format compatible with `gws` CLI for sending. Include `gws` command examples in `sequence-plan.md`.

---

## AI Tells to Avoid in Emails

Emails are intimate — they land in someone's personal inbox, next to messages from friends and family. AI voice kills trust instantly because readers feel deceived, like they're getting a mass-produced email pretending to be personal.

**Words to ban:** delve, comprehensive, robust, utilize, leverage, crucial, streamline, landscape, navigate, elevate, foster, empower
**Phrases to ban:** "I hope this email finds you well," "In today's fast-paced world," "I wanted to reach out," "Don't hesitate to," "Please don't hesitate," "I'm excited to share"
**Patterns:** Every paragraph same length. No contractions. Passive voice throughout. Hedging ("may potentially," "could possibly"). Lists of exactly 3 items every time.

Real emails use contractions, vary paragraph length, have opinions, and sound like one person talking to another — not a committee drafting a memo.

---

## Deliverability Rules

- Never use: free, act now, limited time, congratulations, click here, buy now (in subject)
- Warm up new sending domains: 50 emails day 1, double every 2-3 days
- Include unsubscribe in every email (legally required)
- Text-to-image ratio: 80/20 minimum
- Authenticate: SPF, DKIM, DMARC all configured

---

## References

- [sequence-templates.md](references/sequence-templates.md): Deep examples with full email copy, subject line variants with rationale, file output format, campaign brief template, and pre/per-email/post-generation checklists. Read this when writing actual email copy — SKILL.md blueprints are sufficient for planning.

---

## Related Skills

- **lead-magnet**: Creates the opt-in that triggers the welcome sequence
- **brand-voice**: Voice consistency across all emails
- **newsletter**: Ongoing email content (not automated sequences)
- **direct-response-copy**: Copy principles for high-converting emails
- **launch-strategy**: Launch sequence aligns with broader launch plan
