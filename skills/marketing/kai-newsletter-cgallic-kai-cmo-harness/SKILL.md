---
name: kai-newsletter
description: Plan and produce newsletter editions — content selection, subject lines, scheduling, and production with quality gates. Use when "newsletter", "plan newsletter", "newsletter content", "email newsletter", "weekly digest", or any request to create or manage a newsletter.
---

# /kai-newsletter — An Edition Subscribers Open Twice

## Objective

A send-ready newsletter edition: one lead story worth the open, two or three supporting items, one primary CTA, a subject line and preview text that work as a pair, and a segment and send time chosen on purpose. The edition earns the next open — the footer sets expectations for what comes next and when.

## Done when

Work type `email-lifecycle` — floor **E5/C3/O3** (`harness/eco-floors.yaml`, contract `harness/skill-contracts/email-lifecycle.yaml`).

- **E5** — the ESP reports the send completed with a recipient count reconciled to the approved segment, verified by someone other than the producer. An edition approved in a file is E3.
- **C3** — `four_us_score` ≥ **10/16**, zero Tier 1 banned words, no AI slop, and a named non-producer reads the edition end to end. Unsubscribe handling and sender identity are a C4 field-standard item, not a lint pass — check them against `harness/references/advertising-compliance.md` before send.
- **O3** — open rate, click rate, reply rate, unsubscribe rate, or revenue per recipient read from the ESP at the 14-day window against a threshold declared before send.

## Constraints

- **Subject line:** under 50 characters, no spam trigger words, no ALL CAPS. Generate 5+ candidates and pick with a stated rationale.
- **Preview text complements the subject line.** It never repeats it.
- **One primary CTA per edition, one secondary at most.** Specific action, not "learn more".
- **Gates before delivery:** `python scripts/quality_gates/four_us_score.py <file>` (min 10/16) and `python scripts/quality_gates/banned_word_check.py <file>` (zero Tier 1). Max 2 retry cycles, each naming the specific failing rule. After 2 failures, surface to a human with the specific failures and log the diagnosis in `memory/lessons.md`.
- **Writing rules from the harness apply to every section:** conditions after the main clause ("Do X if Y") · instructions start with verbs · sentences under 20 words where possible · bold the answer, not the query terms.
- Match persona language. No corporate filler, no AI slop ("In conclusion", "It's important to note", "In today's rapidly evolving").
- Any statistic, benchmark, or performance number in the edition needs a real source. Missing data is a gap, not a rounded claim.
- Kai drafts and schedules recommendations. Sending is a human action against an approved segment.
- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — README, manifests, landing pages, route files, analytics and email config — and confirm the draft. Do not open with discovery questions the repo can answer.

**Know these before writing** (from `MARKETING.md` first; ask only for what it cannot answer): the edition's goal (nurture, educate, drive traffic, retain) · the persona(s) receiving it · cadence · which existing content is available to feature · brand voice · past performance (open, click, unsubscribe trends) · which list segment gets this edition.

## Context

| Need | Load |
|---|---|
| Newsletter strategy and edition design | `knowledge/channels/newsletter-strategy.md` |
| Lifecycle email patterns | `knowledge/channels/email-lifecycle.md` |
| Format contract, word counts, thresholds | `harness/skill-contracts/email-lifecycle.yaml` |
| List growth, acquisition budget, subscriber value, list-quality diagnosis | `knowledge/playbooks/newsletter-growth-economics.md` — load only when the request involves these |
| Persona language and hooks | `knowledge/personas/_persona-index.md` |
| Unsubscribe, sender identity, CAN-SPAM/GDPR | `harness/references/advertising-compliance.md` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Edition structure:** hero story or lead piece (the most valuable item, hook in the first line) · 2-3 supporting items (brief summaries with clear value, linking out to the full content) · quick links or resource roundup · CTA · footer that sets the next edition's date and expectation.

**Delivered package:** final subject line with rationale · preview text · full body (HTML-ready or plain text as requested) · send-time recommendation for the target segment · Four U's scorecard · gate pass/fail summary.

**Output** goes to `workspace/` with the filename pattern `newsletter-YYYY-MM-DD.md`.

## Escalate when

- The edition has no lead story worth the open — say so rather than promoting filler.
- A featured claim or statistic cannot be sourced.
- Past performance data is unavailable and the send time or segment choice would be a guess.
- Unsubscribe handling, sender identity, or consent basis for the segment is unresolved.
- The requested segment does not match the edition's content.
- Gates fail twice for the same reason.
