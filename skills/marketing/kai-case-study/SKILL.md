---
name: kai-case-study
description: Produce customer case studies from interviews or data — Problem, Solution, Results structure with perception engineering and quality gates. Use when "case study", "customer story", "testimonial", "success story", "client results", or any request to document a customer win.
---

# Kai Case Study Skill

Produce compelling customer case studies using a Problem, Solution, Results structure with perception engineering layers.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Customer info** — Company name, industry, size, role of contact
2. **Source material** — Interview transcript, survey responses, data points, screenshots
3. **The problem** — What was broken before? Quantify the pain.
4. **The solution** — What did we do? Be specific about the product/service.
5. **The results** — Hard numbers. Revenue, time saved, conversion lift, cost reduction.
6. **Persona alignment** — Which harness persona does this customer map to? Load from `E:\Dev2\kai-cmo-harness-work\knowledge\personas\_persona-index.md`
7. **Permission** — Does the customer approve named use? Or anonymized?

---

## Phase 2: Plan

Structure the case study:

1. **Load content checklist**: `E:\Dev2\kai-cmo-harness-work\knowledge\checklists\content-checklist.md`
2. **Load perception engineering**: `E:\Dev2\kai-cmo-harness-work\knowledge\frameworks\content-copywriting\perception-engineering.md`
3. **Define the narrative arc**:
   - **Before state** — The specific pain, in the customer's words
   - **Turning point** — Why they chose us (decision trigger)
   - **After state** — Measurable transformation
4. **Key quote selection** — Pull 2-3 direct quotes that carry emotion + specificity
5. **Proof points** — List every number, metric, and data point available
6. **Distribution plan** — Where will this live? (website, sales deck, email, social)

---

## Phase 3: Produce

Write the case study:

1. **Headline** — Lead with the result, not the company name. Example: "73% Faster Onboarding: How [Company] Rebuilt Their Workflow"
2. **Snapshot box** — Company, industry, challenge, result (scannable summary)
3. **The Challenge** — 2-3 paragraphs. Paint the before state. Use customer language.
4. **The Solution** — 2-3 paragraphs. What we did, how it worked. Be concrete.
5. **The Results** — Lead with the biggest number. Use a data table or callout boxes.
6. **Customer quote** — Close with their strongest testimonial line.
7. **CTA** — What should the reader do next?

Apply perception engineering layers:
- **Perception layer**: Re-index the old way as the problem (not just "less good")
- **Context layer**: Make the new approach feel inevitable
- **Permission layer**: Remove risk from taking action

---

## Phase 4: Quality Gates

Run all gates before delivery:

1. **Four U's Score**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
   - Minimum: **12/16** (content threshold)
2. **Banned Word Check**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
   - Zero Tier 1 violations
3. **AI Slop Check** — No filler phrases ("In conclusion", "It's worth noting that", etc.)
4. **Specificity check** — Every claim has a number or named example. No vague praise.

Max 2 auto-retry cycles. After 2 failures, surface to human with specific failure reasons.

---

## Phase 5: Output

Deliver the final case study package:

- **Full case study** (long-form, 800-1500 words)
- **One-page summary** (for sales team, 250 words max)
- **Pull quotes** (2-3 standalone quotes for social/email use)
- **Headline variants** (3 options for different channels)
- **Four U's scorecard**
- **Gate pass/fail summary**

Write output to `E:\Dev2\kai-cmo-harness-work\workspace\` with filename pattern: `case-study-[company]-YYYY-MM-DD.md`
