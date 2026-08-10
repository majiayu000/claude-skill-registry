---
name: sales-email-sequences
description: Design multi-touch outbound email sequences with personalized messaging, timing cadences, and conversion-aware copy for prospecting or re-engagement. Use when the user needs a coordinated sales campaign across several touches; use email-drafting for a single message or reply.
license: MIT
metadata:
  author: community
  version: "1.0"
---

# Sales Email Sequences

Design end-to-end outbound email sequences that move prospects from cold outreach to booked meetings. This skill builds persona-targeted messaging across multiple touches — intros, follow-ups, value-adds, and breakup emails — with personalization tokens, subject line variants, and send-timing cadences optimized for reply rates.

## Workflow

1. **Define ICP and Persona** — Establish the ideal customer profile (industry, company size, revenue range, geography) and the target persona (title, seniority, responsibilities, pain points). This determines tone, vocabulary, value framing, and which proof points resonate.

2. **Craft the Core Value Proposition** — Distill your product's relevance to this persona into a single compelling statement. Focus on a specific, measurable outcome (e.g., "reduce month-end close from 10 days to 3") rather than feature lists. This value prop threads through every email in the sequence.

3. **Write the Email Sequence** — Build a multi-touch sequence: an opening email that earns attention with a relevant hook, follow-ups that introduce new angles or proof points, a value-add email offering a resource, and a breakup email that creates urgency through finality. Each email should be 50–120 words in the body.

4. **Add Personalization Tokens** — Insert dynamic fields for prospect name, company, industry, recent trigger events (funding rounds, job changes, earnings calls), and any known tech stack details. Personalization beyond `{{first_name}}` dramatically lifts reply rates.

5. **Set Timing and Cadence** — Define send days, times, and intervals between touches. B2B sequences typically perform best with Tuesday–Thursday sends between 8–10 AM local time, with 2–4 day gaps between early touches and longer gaps (5–7 days) before the breakup.

## Usage

Specify the target persona, your product/service, the core pain point you solve, and desired sequence length. Optionally include trigger events or specific personalization data.

**Example prompt:**
> Create a 5-email cold outreach sequence targeting VP of Engineering at Series B+ SaaS companies. We sell an automated code review platform that cuts PR review time by 60%. Include subject lines, body copy, and send timing for each email.

## Examples

### Example 1: 5-Email Cold Outreach Sequence (B2B SaaS)

**Target:** VP of Engineering at Series B+ SaaS companies (100–500 employees)
**Product:** Automated code review platform
**Value prop:** Cut PR review time by 60%, ship 2x faster

---

**Email 1 — The Hook (Day 1, Tuesday 9:00 AM)**

Subject: `{{company}}'s PR bottleneck`

Hi {{first_name}},

Saw {{company}} just shipped {{recent_launch}} — congrats. Curious if your team is feeling the review bottleneck that usually comes with scaling engineering velocity post-Series B.

Our platform plugs into your existing GitHub workflow and automates 60% of code review — teams our size typically cut PR cycle time from 24 hours to under 4.

Worth a 15-min look? I can show you results from {{similar_company}} in your space.

Best,
{{sender_name}}

---

**Email 2 — Social Proof (Day 3, Thursday 8:30 AM)**

Subject: `How {{similar_company}} ships 2x faster`

{{first_name}}, quick follow-up.

{{similar_company}} was averaging 22-hour PR cycle times with a 40-person eng team. After deploying our automated review, they dropped to 3.5 hours and increased weekly deploys by 94%.

Happy to share their playbook — no strings.

{{sender_name}}

---

**Email 3 — Value-Add (Day 7, Monday 9:00 AM)**

Subject: `Code review benchmarks for {{industry}} teams`

{{first_name}},

We just published our 2025 Engineering Velocity Report — covers review cycle benchmarks across 200+ SaaS teams your size.

Key finding: top-quartile teams automate 55%+ of review comments. Bottom quartile still relies on fully manual review and ships 3.2x slower.

Here's the report: [link]

Useful regardless of whether we chat — but if the data resonates, I'd love to show how we help teams move from bottom to top quartile in weeks.

{{sender_name}}

---

**Email 4 — New Angle (Day 11, Friday 8:00 AM)**

Subject: `Developer satisfaction at {{company}}`

{{first_name}},

One thing that doesn't show up in cycle-time metrics: developer frustration. Our latest survey found that 72% of engineers rank "waiting on code review" as their top workflow blocker.

If retention and developer experience are on your radar this year, automating the review bottleneck is low-hanging fruit with outsized impact.

Open to a quick call next week?

{{sender_name}}

---

**Email 5 — Breakup (Day 16, Wednesday 9:00 AM)**

Subject: `Closing the loop`

{{first_name}},

I've reached out a few times and haven't heard back — totally understand if the timing isn't right.

I'll leave you with this: {{company}} can trial our platform free for 30 days on a single repo, no integration work required. If review speed becomes a priority, you'll know where to find us.

Wishing you and the {{company}} team a strong quarter.

{{sender_name}}

---

### Example 2: 3-Email Re-Engagement Sequence (Dormant Leads)

**Target:** Marketing Directors who attended a webinar 90+ days ago but went dark.

**Email 1 — Re-engage with New Value (Day 1)**

Subject: `A lot's changed since {{webinar_name}}`

Hi {{first_name}},

You joined our {{webinar_name}} session back in {{month}} — since then, we've launched three features our marketing customers specifically asked for: multi-touch attribution, AI-powered content scoring, and Salesforce bi-directional sync.

Any of those hit a current pain point? Happy to do a 15-minute walkthrough tailored to {{company}}'s stack.

{{sender_name}}

**Email 2 — Peer Success Story (Day 5)**

Subject: `{{peer_company}} just hit 140% of pipeline target`

{{first_name}},

Since we last connected, {{peer_company}} (similar size and vertical to {{company}}) rolled out our attribution model. Result: 140% of pipeline target last quarter with 20% less ad spend.

Their director of demand gen did a 3-minute video case study — want me to send it over?

{{sender_name}}

**Email 3 — Breakup with Offer (Day 10)**

Subject: `Last note from me`

{{first_name}},

Don't want to clutter your inbox. If priorities have shifted, no worries — I'll close out this thread.

One parting offer: we're running a free pipeline audit for marketing teams through end of quarter. Takes 30 minutes, zero commitment, and you walk away with a benchmarked view of your funnel vs. industry peers.

Link to book: [link]

Either way, wishing {{company}} a strong quarter.

{{sender_name}}

## Best Practices

- Keep body copy under 120 words — every extra sentence drops reply rates measurably.
- Personalize beyond first name; reference company news, tech stack, or a recent trigger event.
- Each email should introduce a new angle (social proof, data, empathy, resource) rather than repeating the same pitch.
- Write subject lines under 6 words — shorter subjects outperform in B2B outreach.
- Send from a real person's address, never a generic team alias.
- A/B test the first email's subject line and opening line before scaling the sequence.

## Edge Cases

- **No trigger events available** — Fall back to industry-level trends or publicly available company metrics (headcount growth, job postings, tech stack signals).
- **Prospect replies mid-sequence** — Any reply (positive, negative, or out-of-office) should halt the automated sequence and route to a human rep immediately.
- **Multi-threaded deals** — When targeting multiple personas at the same company, stagger sequences by 3–5 days and vary the value prop angle to avoid the contacts comparing notes on identical emails.
- **Regulated industries (healthcare, finance)** — Remove aggressive urgency language, add compliance-safe disclaimers, and ensure CAN-SPAM / GDPR opt-out links are present.
- **Very small TAM (< 200 accounts)** — Increase manual personalization depth significantly; generic sequences burn through a limited addressable market too quickly.
