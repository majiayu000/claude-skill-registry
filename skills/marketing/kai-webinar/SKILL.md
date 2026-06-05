---
name: kai-webinar
description: Plan webinar and event marketing — topic selection, promotion strategy, content production, registration flow, and post-event follow-up sequences. Use when "webinar", "event marketing", "virtual event", "live event", "workshop", "online event", or any request to plan, promote, or produce a webinar or marketing event.
---

# Kai Webinar Skill

Plan webinar and event marketing end-to-end: topic, promotion, content, and follow-up.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Event type** — Webinar, workshop, panel, AMA, product demo, conference talk?
2. **Goal** — Lead generation, nurture, product launch, thought leadership, retention?
3. **Target audience** — Which persona(s)? Load from `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`
4. **Topic candidates** — What expertise can we share that the audience needs?
5. **Speakers** — Internal, external guests, customer panels?
6. **Platform** — Zoom, Teams, StreamYard, Crowdcast, in-person, hybrid?
7. **Date/time** — Proposed date, timezone considerations
8. **Registration target** — How many signups needed? (Budget for 40-50% show rate)
9. **Follow-up plan** — What happens after? (Sales call, trial, content, nurture)

---

## Phase 2: Plan

Build the event marketing plan:

1. **Load event playbook**: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\event-webinar-MARKETING.md`
2. **Topic validation** — Score topic against:
   - Audience pain relevance (does it solve a real problem?)
   - Competitive differentiation (can only WE teach this?)
   - Lead quality potential (will the right people show up?)
3. **Promotion timeline** (4-week standard):
   - **Week 1**: Announce — email list, social posts, partner outreach
   - **Week 2**: Build — blog post / content teaser, speaker spotlights
   - **Week 3**: Push — reminder emails, social proof (registrant count), urgency
   - **Week 4**: Final — last-chance emails, day-of reminders (1hr + 15min before)
4. **Registration page plan** — Headline, value props, speaker bios, agenda, CTA
5. **Email sequence**:
   - Confirmation + calendar invite
   - 1-week reminder with agenda preview
   - Day-before reminder with prep instructions
   - 1-hour reminder
   - Post-event replay + resources (for attendees)
   - Post-event replay + "you missed this" (for no-shows)
   - Follow-up nurture sequence (3-5 emails)
6. **Content plan** — Slides, handouts, worksheets, resource lists

---

## Phase 3: Produce

Create all event marketing assets:

1. **Registration page copy** — Headline with result, not topic. "Learn How to X" becomes "Walk Away With a Working X"
2. **Promotion emails** (3-5 emails in the invite sequence)
3. **Social media posts** (5-10 posts across the promotion window)
4. **Event content outline** — Structure, key points, transitions, audience interaction moments
5. **Post-event emails** — Replay access, resource links, next step CTA
6. **Follow-up nurture sequence** — Continue the conversation, move toward conversion

Apply harness writing rules:
- Conditions AFTER main clause
- Instructions start with verbs
- Short sentences
- Bold the answer

---

## Phase 4: Quality Gates

Validate before launch:

1. **Four U's Score** (on emails and registration page): `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
   - Minimum: **10/16** (email threshold) for emails
   - Minimum: **12/16** (content threshold) for registration page
2. **Banned Word Check**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
3. **AI Slop Check** — No filler phrases
4. **Subject line check** — Under 50 characters, no spam triggers
5. **CTA clarity check** — Every asset has exactly one clear next step

Max 2 auto-retry cycles on gate failures.

---

## Phase 5: Output

Deliver the complete event marketing package:

- **Event strategy brief** (goal, topic, audience, timeline)
- **Registration page copy**
- **Promotion email sequence** (3-5 emails)
- **Social media post calendar**
- **Event content outline / slide structure**
- **Post-event email sequence** (replay + nurture)
- **Promotion timeline with dates**
- **Gate pass/fail summary**

Write output to `E:\Dev2\kai-cmo-harness-work\workspace\` with filename pattern: `webinar-[topic-slug]-YYYY-MM-DD.md`
