---
name: kai-newsletter
description: Plan and produce newsletter editions — content selection, subject lines, scheduling, and production with quality gates. Use when "newsletter", "plan newsletter", "newsletter content", "email newsletter", "weekly digest", or any request to create or manage a newsletter.
---

# Kai Newsletter Skill

Plan and produce newsletter editions with strategy, content selection, subject lines, and full production pipeline.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Newsletter purpose** — What is the goal? (nurture, educate, drive traffic, retain)
2. **Audience** — Which persona(s) from the harness? Load from `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`
3. **Cadence** — Weekly, biweekly, monthly?
4. **Existing content** — Any blog posts, articles, or assets to feature?
5. **Brand voice** — Formal, conversational, irreverent?
6. **Past performance** — Open rates, click rates, unsubscribe trends?

---

## Phase 2: Plan

Build the newsletter edition plan:

1. **Load strategy framework**: `E:\Dev2\kai-cmo-harness-work\knowledge\channels\newsletter-strategy.md`
2. **Load email lifecycle patterns**: `E:\Dev2\kai-cmo-harness-work\knowledge\channels\email-lifecycle.md`
3. **Load skill contract**: `E:\Dev2\kai-cmo-harness-work\harness\skill-contracts\email-lifecycle.yaml`
4. **Define edition structure**:
   - Hero story / lead piece
   - Supporting content (2-3 items)
   - Quick links / resource roundup
   - CTA (one primary, one secondary max)
5. **Subject line candidates** — Generate 5+ options, score for open-rate potential
6. **Preview text** — Complement (not repeat) the subject line
7. **Segment targeting** — Which list segment receives this edition?

---

## Phase 3: Produce

Write the newsletter content:

1. **Hero section** — Lead with the most valuable piece. Hook in the first line.
2. **Supporting sections** — Brief summaries with clear value. Link out to full content.
3. **Tone** — Match persona language patterns. No corporate filler.
4. **CTA** — One clear action per edition. Make it specific.
5. **Footer** — Manage expectations (next edition date, what to expect).

Apply these rules from the harness:
- Conditions AFTER main clause ("Do X if Y")
- Instructions start with verbs
- Sentences under 20 words where possible
- Bold the answer, not the query terms

---

## Phase 4: Quality Gates

Run all gates before delivery:

1. **Four U's Score**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
   - Minimum: **10/16** (email threshold)
2. **Banned Word Check**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
   - Zero Tier 1 violations
3. **AI Slop Check** — No phrases like "In conclusion", "It's important to note", "In today's rapidly evolving"
4. **Subject line validation** — Under 50 characters, no spam trigger words, no ALL CAPS

Max 2 auto-retry cycles. After 2 failures, surface to human with specific failure reasons.

---

## Phase 5: Output

Deliver the final newsletter package:

- **Subject line** (final selection with rationale)
- **Preview text**
- **Full newsletter body** (HTML-ready or plain text as requested)
- **Send time recommendation** (based on audience segment)
- **Four U's scorecard**
- **Gate pass/fail summary**

Write output to `E:\Dev2\kai-cmo-harness-work\workspace\` with filename pattern: `newsletter-YYYY-MM-DD.md`
