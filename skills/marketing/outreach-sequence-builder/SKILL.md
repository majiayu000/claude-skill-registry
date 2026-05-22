---
name: outreach-sequence-builder
description: "Use when creating outreach sequences, writing cold email campaigns, building multi-channel cadences, designing follow-up flows, or crafting signal-triggered messages. Triggers: 'build an outreach sequence', 'write a cold email sequence', 'create a cadence', 'outreach for [signal]', 'email sequence', 'follow-up sequence', 'multi-channel outreach'."
version: 1.0.0
---

# Outreach Sequence Builder

Build signal-triggered, multi-channel outreach sequences that convert. Maps **Signal --> Angle --> Channel --> Message --> Objection Pre-emption**. Produces ready-to-use sequences in markdown, written to `docs/sequences/`.

Can reference `docs/icp.md` for persona and pain-point data, and `docs/accounts/*.md` for account-level personalization. Works for any B2B product or service.

---

## Methodology

Follow these steps in order. Do not skip steps. Do not produce output until Step 7.

### Step 1 -- Context Loading

Check for existing files before asking questions.

1. **Read `docs/icp.md`** if it exists. Extract:
   - Target personas (titles, seniority, department)
   - Company profile (size, industry, stage)
   - Pain points (ranked by severity)
   - Language patterns (how prospects describe their problems in their own words)
   - Key differentiators of the product/service

2. **Glob `docs/accounts/*.md`** if any exist. Extract:
   - Account names and context
   - Known tech stack, recent news, or specific pain points
   - Any existing relationship context

3. **If neither file exists**, gather the minimum viable context by asking the user these four questions (all four are required before proceeding):
   - What does your product/service do? (one paragraph)
   - Who are you targeting? (job title, company size, industry)
   - What is the main problem you solve? (from the buyer's perspective)
   - What is your key differentiator? (why you over the alternative)

Do not proceed to Step 2 until context is loaded or gathered.

---

### Step 2 -- Trigger Selection

Present the trigger signal menu and ask the user to select one or more:

| # | Trigger Signal | Example |
|---|---------------|---------|
| 1 | **Post-Fundraise** | Company just raised a round -- they have budget and a mandate to grow |
| 2 | **Hiring Signal** | Company posting SDR, GTM, growth, or ops roles -- they are scaling a function you serve |
| 3 | **Competitor Displacement** | Prospect is using a competitor and showing frustration -- switching cost feels low |
| 4 | **Product Launch** | Company released a new product or feature -- adjacent needs surface |
| 5 | **Content Engagement** | Prospect liked, commented, or shared content relevant to your space |
| 6 | **Event Follow-up** | Met at a conference, attended the same webinar, or appeared on the same panel |
| 7 | **Job Change** | Contact moved to a new company -- fresh mandate, open to new vendors |

The user may select multiple triggers or describe a custom trigger. For custom triggers, map them into the same structure (signal, what it reveals, why it matters now).

---

### Step 3 -- Angle Development

For **each** selected trigger, develop four components:

1. **The Insight** -- What does this signal tell you about the prospect's current situation? Be specific. "They raised a Series B" is not an insight. "They raised a Series B and are hiring 4 SDRs, which means they are building outbound from scratch and will hit tooling decisions within 60 days" is an insight.

2. **The Bridge** -- How does your product connect to what this signal reveals? The bridge must feel inevitable, not forced. The prospect should think "that makes sense" not "nice try."

3. **The Opener** -- One sentence that proves you did your research. It must reference the specific signal. No generic openers. No "I came across your company and was impressed." The opener must contain a concrete detail only someone paying attention would know.

4. **The Ask** -- The minimum viable CTA. Not "book a 30-minute demo." Something the prospect can say yes to in under 10 seconds:
   - "Worth a 10-minute look?"
   - "Want me to send the comparison?"
   - "Happy to share how [similar company] handled this -- interested?"
   - "Mind if I send a 2-minute walkthrough?"

---

### Step 4 -- Channel Strategy

For each sequence, define the channel mix from these three channels:

- **Email** -- Best for: first touch with unknown contacts, detailed value propositions, case study sharing, async communication with busy executives. Strength: space for context. Weakness: crowded inbox.

- **LinkedIn** -- Best for: warm connections, social proof via mutual connections, content engagement before outreach, connection requests that build familiarity. Strength: profile visibility. Weakness: character limits, connection-gated.

- **Phone** -- Best for: hot leads where timing matters, time-sensitive signals (fundraise announced today), executives who ignore email, and as a pattern interrupt after email/LinkedIn touches. Strength: real-time conversation. Weakness: hard to reach, requires research on direct dials.

**Default cadence guidelines:**
- 3 to 5 touchpoints per sequence
- Never exceed 6 touchpoints
- Spread across 2 to 3 channels
- Total sequence duration: 10 to 14 days
- Minimum 2 days between touchpoints (no back-to-back days)
- Vary the channel -- never send the same channel type twice in a row

---

### Step 5 -- Message Writing

For each touchpoint in the sequence, write the complete message.

**Per-touchpoint deliverables:**

For **email** touchpoints:
- Subject line (primary)
- Subject line (A/B variant)
- Body (under 100 words -- hard cap)
- CTA (one clear ask)
- Tone note (one sentence on how to deliver this)

For **LinkedIn** touchpoints:
- Connection note or DM (under 300 characters -- hard cap)
- Tone note

For **phone** touchpoints:
- Opening line (under 20 words)
- Talk track (3 to 4 bullet points, not a script)
- Voicemail script (under 30 seconds when read aloud)
- Tone note

**Writing rules -- apply to every message, no exceptions:**

1. The first sentence must be about THEM. Not your company, not your product, not your excitement about reaching out. Them.
2. Reference the specific trigger signal. If the signal is a fundraise, mention the round. If it is a job posting, mention the role. Generic messages fail.
3. No buzzwords. Banned list: synergy, leverage, touch base, circle back, ping, loop in, alignment, move the needle, low-hanging fruit, deep dive, bandwidth, at the end of the day, innovative, cutting-edge, best-in-class, world-class, game-changing, disruptive.
4. No "I hope this email finds you well." No "I hope you are having a great week." No "Happy [day of week]." No pleasantries that waste the first line.
5. Ask a question, do not make a pitch. Questions create engagement. Pitches create delete buttons.
6. Each follow-up must add NEW value. New information, a new angle, a new resource, a new comparison. Never write "just following up" or "bumping this to the top of your inbox" or "wanted to circle back." If you have nothing new to add, do not send the message.
7. Objection pre-emption: weave responses to the most likely objection into the message naturally. Do not wait for them to object.
8. Every message must be READY TO SEND. No placeholder brackets like [Company Name] or [Pain Point]. Fill in everything from the loaded context. The only acceptable variable is the prospect's first name, written as `{{first_name}}`.

---

### Step 6 -- Objection Pre-emption

For each sequence, identify 3 to 4 likely objections and define how to address them within the messages:

| Objection | Strategy | How to weave it in |
|-----------|----------|-------------------|
| "We already have a solution for this" | Compare, do not compete. Acknowledge their current tool. Position yours as complementary or as the next evolution, not a replacement. | Include a line like "Most teams using [category] find they still need X for Y -- that is where this fits." |
| "Not the right time" | Tie directly to the signal that triggered the sequence. The signal IS the evidence that now is the right time. | Reference the signal: "The fact that you are [hiring/launching/scaling] suggests this is exactly when teams lock in [your category]." |
| "Too expensive" | Frame ROI, not cost. Anchor to a number they care about (pipeline generated, hours saved, revenue retained). Never lead with price. | Include a proof point: "Teams like yours typically see X within the first 90 days, which covers the investment 3x over." |
| "Need to involve more people" | Do not fight it. Offer a resource designed to be shared internally -- a one-pager, a comparison doc, a recorded walkthrough. Make it easy for your champion to sell internally. | Offer the resource: "Happy to send a one-pager your team can review async -- makes the internal conversation easier." |

Map each objection to specific touchpoints in the sequence where it gets addressed. At least two objections must be pre-empted before the final touchpoint.

---

### Step 7 -- Sequence Assembly

Write the complete sequence for each selected trigger. Use this structure:

```markdown
# [Trigger Name] Outreach Sequence

## Trigger
[Description of the signal and what it reveals]

## Target Persona
[Title, seniority, department, company profile -- pulled from ICP or gathered context]

## Angle
- **Insight:** [What the signal tells us]
- **Bridge:** [How the product connects]
- **Opener:** [The research-backed first line]
- **Ask:** [Minimum viable CTA]

## Sequence

### Day 1 -- [Channel]: [Touchpoint Purpose]

**Subject:** [primary subject line]
**Subject (A/B):** [variant]

[Full message body]

**Objection addressed:** [which objection this touchpoint pre-empts]

---

### Day X -- [Channel]: [Touchpoint Purpose]

[Continue for each touchpoint...]

---

## Objection Playbook

| Objection | Response | Used in |
|-----------|----------|---------|
| [Objection 1] | [Response strategy] | Day X touchpoint |
| [Objection 2] | [Response strategy] | Day X touchpoint |
| ... | ... | ... |

## KPI Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Email open rate | 45-55% | Signal-based subject lines outperform generic by 2-3x |
| Email reply rate | 8-12% | First reply often comes on touchpoint 2 or 3 |
| LinkedIn accept rate | 30-40% | Higher when connection note references shared context |
| Positive reply rate | 4-6% | Meetings booked as % of total sequence starts |
| Sequence completion rate | 70%+ | Prospects who receive all touchpoints without opting out |
```

---

### Step 8 -- Output

1. **Write each sequence** to `docs/sequences/{trigger-name}.md` using kebab-case naming:
   - `docs/sequences/post-fundraise.md`
   - `docs/sequences/hiring-signal.md`
   - `docs/sequences/competitor-displacement.md`
   - `docs/sequences/product-launch.md`
   - `docs/sequences/content-engagement.md`
   - `docs/sequences/event-follow-up.md`
   - `docs/sequences/job-change.md`
   - Custom triggers: `docs/sequences/{custom-trigger-name}.md`

2. **Create or update `docs/sequences/README.md`** listing all sequences:

   ```markdown
   # Outreach Sequences

   Signal-triggered outreach sequences. Each file contains a complete
   multi-channel cadence ready for execution.

   ## Active Sequences

   | Trigger | File | Channels | Touchpoints | Duration |
   |---------|------|----------|-------------|----------|
   | [Name] | [filename.md] | [channels] | [count] | [X days] |

   ## How to Use

   1. Identify the buying signal
   2. Open the matching sequence
   3. Replace {{first_name}} with the prospect's name
   4. Execute the cadence day by day
   5. Track opens, replies, and meetings booked

   ## Customization

   - Swap subject lines using the A/B variants provided
   - Adjust timing (keep minimum 2-day gaps between touches)
   - Add account-specific details from docs/accounts/ if available
   ```

3. **If `docs/sequences/` already contains sequences from a previous run**, read them first with Glob and merge -- do not overwrite existing sequences unless the user explicitly asks to replace them. Append new triggers alongside existing ones.

---

## Tools Used

- **Read** -- load `docs/icp.md` and `docs/accounts/*.md` for context
- **Glob** -- check for existing sequences in `docs/sequences/`
- **Write** -- output sequence files and README

---

## Rules

1. Every message must be READY TO SEND. No brackets except `{{first_name}}`. Fill in all product, persona, and pain-point details from loaded context.
2. The first message in any sequence must reference the trigger signal specifically. No generic first touches.
3. No more than 6 touchpoints per sequence. Most sequences should have 4 to 5.
4. Each follow-up must add new value. New information, new resource, new angle. Never "just following up."
5. Include subject line A/B variants for every email touchpoint.
6. Email body must stay under 100 words. LinkedIn messages under 300 characters. No exceptions.
7. Works for any B2B product or service. No references to internal tools, specific vendors, or proprietary systems.
8. Objection pre-emption must be woven into messages naturally, not bolted on as a separate section within the message itself.
9. Channel variety is mandatory. Never use the same channel for consecutive touchpoints.
10. The breakup email (final touchpoint) must leave the door open. No guilt trips, no passive aggression, no "I guess you are not interested." End with value and an open invitation.
