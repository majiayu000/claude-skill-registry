---
name: kai-webinar
description: Plan webinar and event marketing — topic selection, promotion strategy, content production, registration flow, and post-event follow-up sequences. Use when "webinar", "event marketing", "virtual event", "live event", "workshop", "online event", or any request to plan, promote, or produce a webinar or marketing event.
---

# /kai-webinar — an event with an audience in the room and a next step after it

## Objective

A complete event marketing package the team can execute without writing anything else: registration page copy, the promotion sequence that fills the seats, the event content structure, and the follow-up that converts attendees and no-shows. The deliverable is the whole arc — a webinar with registrations and no follow-up is a cost, not a campaign.

Registration targets are set from the show rate, not from signups. Budget 40–50% show rate when sizing the goal.

## Done when

Work type `campaign` — floor **E5/C3/O4** (`harness/eco-floors.yaml`), contract `harness/skill-contracts/campaign.yaml`. A campaign is composite: it is CLOSED only when every child asset is CLOSED and the campaign-level threshold is met. One unsent reminder keeps it open.

- **E5** — every asset reached its target and was read back: the registration page returns 200 with the approved copy, the ESP reports each send against the approved segment, the social posts return permalinks that match.
- **C3** — `four_us_score` at **10/16** for emails and **12/16** for the registration page, `banned_word_check` clean, zero AI slop, and a named non-producer read the package end to end.
- **O4** — registrations, show rate, and the post-event next-step conversion clear thresholds declared before promotion opened. Metrics window 45 days.

Assets stay drafts until a human approves them. This skill does not send, publish, or schedule anything.

## Constraints

- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not open with discovery questions the repo can answer.
- **Know these before planning:** event type (webinar, workshop, panel, AMA, demo, conference talk), goal (lead gen, nurture, launch, thought leadership, retention), persona, topic candidates, speakers, platform, date and timezone, registration target, and what happens after the event. Anything `MARKETING.md` answers is not a question.
- **Score the topic before producing anything.** Three tests: audience pain relevance (does it solve a real problem?), competitive differentiation (can only we teach this?), lead quality potential (will the right people show up?). A topic that fails differentiation produces a webinar nobody remembers.
- **Registration headlines promise a result, not a subject.** "Learn How to X" becomes "Walk Away With a Working X".
- **Harness writing rules apply to every asset:** conditions after the main clause, instructions start with verbs, short sentences, bold the answer. No banned words, no AI slop.
- **Subject lines under 50 characters, no spam triggers. Exactly one clear next step per asset.**
- **Gate failures get named fixes.** Max 2 auto-retry cycles; after that, surface the specific failures to a human.
- **No live-channel mutation.** Nothing is sent, posted, or published without human approval.

## Context

| Need | Load |
|---|---|
| Event and webinar mechanics | `knowledge/playbooks/event-webinar-marketing.md` |
| Persona selection | `knowledge/personas/_persona-index.md` |
| Product, ICP, voice, channels | `MARKETING.md` (project root) |
| Email format contract | `harness/skill-contracts/email-lifecycle.yaml` |
| Registration/landing page contract | `harness/skill-contracts/landing-page.yaml` |
| Gates | `python scripts/quality_gates/four_us_score.py <file>` · `banned_word_check.py <file>` |

**Promotion timeline** — the 4-week standard, worth carrying inline because it sets the asset count:

| Week | Move | Assets |
|---|---|---|
| 1 | Announce | Email to list, social posts, partner outreach |
| 2 | Build | Blog or content teaser, speaker spotlights |
| 3 | Push | Reminder emails, social proof (registrant count), urgency |
| 4 | Final | Last-chance emails, day-of reminders at 1 hour and 15 minutes |

**Email sequence** — confirmation with calendar invite, 1-week reminder with agenda preview, day-before with prep instructions, 1-hour reminder, post-event replay plus resources for attendees, post-event "you missed this" for no-shows, then a 3–5 email nurture.

**Registration page** carries headline, value props, speaker bios, agenda, and CTA. **Event content plan** covers structure, key points, transitions, audience interaction moments, plus slides, handouts, worksheets, and resource lists.

**Output** goes to `workspace/` as `webinar-[topic-slug]-YYYY-MM-DD.md`: strategy brief, registration page copy, promotion emails, social calendar, event content outline, post-event sequence, dated promotion timeline, and the gate pass/fail summary.

## Escalate when

- The registration target implies a list or audience size the brand does not have, and paid promotion would be needed to close the gap.
- The topic cannot pass the differentiation test with the brand's actual expertise.
- Speakers are external and their bios, claims, or likeness rights are unconfirmed.
- The date leaves less than the promotion timeline requires.
- Any asset would need to send or publish before a human has approved it.
