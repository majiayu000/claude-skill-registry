---
name: email-sequence
description: Build email nurture flows using lifecycle marketing + perception engineering frameworks. Generates subject lines, body copy, and send timing.
---

# /email-sequence — The Email Marketer

Build email nurture sequences using the harness's lifecycle marketing and perception engineering frameworks. Generates subject lines, body copy, send timing, and personalization tokens.

## Arguments

Required:
- **type**: welcome | nurture | reactivation | onboarding | cart-abandon | cold-outreach
- **site**: Site key
- **goal**: The sequence goal in quotes

Example: `/email-sequence nurture kaicalls "Convert trial users to paid within 14 days"`
Example: `/email-sequence cold-outreach kaicalls "Book demo calls with law firm office managers"`

## The Skill

### Step 1: Load Frameworks

Read the relevant knowledge files:

- `knowledge/channels/email-lifecycle.md` — lifecycle marketing guide
- `knowledge/frameworks/content-copywriting/perception-engineering.md` — persuasion framework
- `harness/references/cold-email-rules.md` — CAN-SPAM rules (for cold-outreach type)
- `harness/skill-contracts/email-lifecycle.yaml` or `cold-email.yaml` — constraints
- `~/.kai-marketing/voice.md` — voice profile (if exists)

### Step 2: Design the Sequence

Based on the type and goal, design a sequence with:
- Number of emails (3-7 depending on type)
- Send timing (days between emails)
- Each email's role in the sequence arc

```
EMAIL SEQUENCE — {type} for {site}
══════════════════════════════════════

Goal: {goal}
Emails: {N}
Duration: {days} days

SEQUENCE MAP:
  Day 0:  Email 1 — {role} (e.g., "Welcome + quick win")
  Day 2:  Email 2 — {role} (e.g., "Social proof + feature highlight")
  Day 5:  Email 3 — {role} (e.g., "Pain agitate + case study")
  Day 8:  Email 4 — {role} (e.g., "Objection handling")
  Day 12: Email 5 — {role} (e.g., "Urgency + final CTA")
```

### Step 3: Write Each Email

For each email in the sequence, generate:
- **Subject line** (3 options, each under 50 chars)
- **Preview text** (under 90 chars)
- **Body copy** (following perception engineering layers)
- **CTA** (single, clear action)
- **Personalization tokens** (e.g., {{first_name}}, {{company}})

Apply quality rules:
- No banned words (Tier 1 = instant reject)
- Subject lines score 10+/16 on Four U's
- Body follows voice profile
- Cold outreach includes CAN-SPAM compliance (physical address, unsubscribe)

### Step 4: Display the Sequence

Show each email with subject line options and body preview:

```
EMAIL 1 of 5 — Welcome + Quick Win (Day 0)
────────────────────────────────────────────

Subject options:
  A) "Your AI receptionist is ready" (32 chars)
  B) "First call answered in 0.4 seconds" (35 chars)
  C) "{first_name}, you're live" (25 chars)

Preview: "Here's what to set up in the first 10 minutes"

Body:
  {full email body}

CTA: [Complete Your Setup →]
Personalization: {{first_name}}, {{company}}, {{plan_name}}
```

### Step 5: Compliance Check (Cold Outreach)

For cold-outreach type, verify CAN-SPAM compliance:
- Physical mailing address present
- Unsubscribe mechanism mentioned
- No deceptive subject lines
- Sender identity clear
- "Advertisement" label if required

## Error Handling

- **Unknown type**: List valid types
- **No voice profile**: Generate with default professional tone, suggest creating `~/.kai-marketing/voice.md`

## Chain State

**Standalone:** Does not require prior chain steps
**Optional reads:** `~/.kai-marketing/voice.md`, `~/.kai-marketing/marketing-defaults.md`
