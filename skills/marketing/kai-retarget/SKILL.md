---
name: kai-retarget
description: Design retargeting and remarketing campaign architecture across platforms — audience segmentation, creative strategy, frequency caps, and platform-specific setup with ad policy compliance. Use when "retargeting", "remarketing", "retarget", "re-engage visitors", "abandoned cart", "pixel setup", or any request to bring back visitors who didn't convert.
---

# Kai Retarget Skill

Design retargeting/remarketing campaign architecture across platforms with audience segmentation, creative strategy, and policy compliance.

---

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Phase 1: Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Traffic sources** — Where do visitors come from? (organic, paid, social, email)
2. **Conversion points** — What actions matter? (purchase, signup, demo, download)
3. **Drop-off data** — Where do people leave? (homepage, pricing, checkout, form)
4. **Pixel/tag status** — Which platforms have tracking installed?
5. **Budget** — Monthly retargeting spend available
6. **Platforms** — Which ad platforms to retarget on? (Meta, Google, LinkedIn, TikTok, etc.)
7. **Product type** — B2B or B2C? High-ticket or impulse? Long or short sales cycle?

---

## Phase 2: Plan

Build the retargeting architecture:

1. **Load retargeting playbook**: `E:\Dev2\kai-cmo-harness-work\knowledge\playbooks\retargeting-reMARKETING.md`
2. **Load platform policy references** (for each active platform):
   - Meta: `E:\Dev2\kai-cmo-harness-work\harness\references\meta-ads-rules.md`
   - Google: `E:\Dev2\kai-cmo-harness-work\harness\references\google-ads-policy-reference.md`
   - LinkedIn: `E:\Dev2\kai-cmo-harness-work\harness\references\linkedin-ads-rules.md`
   - TikTok: `E:\Dev2\kai-cmo-harness-work\harness\references\tiktok-ads-policy-reference.md`
   - Microsoft: `E:\Dev2\kai-cmo-harness-work\harness\references\microsoft-ads-rules.md`
   - Pinterest: `E:\Dev2\kai-cmo-harness-work\harness\references\pinterest-ads-rules.md`
   - Snapchat: `E:\Dev2\kai-cmo-harness-work\harness\references\snapchat-ads-policy-reference.md`
   - Amazon: `E:\Dev2\kai-cmo-harness-work\harness\references\amazon-ads-policy-reference.md`
   - X/Twitter: `E:\Dev2\kai-cmo-harness-work\harness\references\x-ads-policy-reference.md`
3. **Load compliance framework**: `E:\Dev2\kai-cmo-harness-work\harness\references\advertising-compliance.md`
4. **Define audience segments**:
   - Segment by intent level (visited homepage vs. visited pricing vs. started checkout)
   - Set recency windows (1-3 days, 3-7 days, 7-30 days, 30-90 days)
   - Exclude converters from retargeting pools
5. **Map creative to segment** — Different message for each intent level
6. **Set frequency caps** — Prevent ad fatigue (typically 3-5 impressions/day max)
7. **Define exclusion rules** — Suppress ads for existing customers, employees, competitors

---

## Phase 3: Produce

Build the campaign assets:

1. **Audience definitions** — Platform-ready segment specs (pixel events, URL rules, time windows)
2. **Creative briefs per segment**:
   - **Low intent** (homepage visitors): Brand awareness, social proof
   - **Medium intent** (product/pricing viewers): Value props, comparison, objection handling
   - **High intent** (cart/form abandoners): Urgency, incentive, friction removal
3. **Ad copy per platform** — Respect character limits and format rules per platform
4. **Sequence timing** — When each segment sees each creative
5. **Budget allocation** — Higher spend on higher-intent segments

---

## Phase 4: Quality Gates

Validate before launch:

1. **Four U's Score** (on ad copy): `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\four_us_score.py <file>`
   - Minimum: **10/16** (ad threshold)
2. **Banned Word Check**: `python E:\Dev2\kai-cmo-harness-work\scripts\quality_gates\banned_word_check.py <file>`
3. **Platform policy compliance** — Check each ad against its platform's TOS
4. **Frequency cap validation** — Confirm caps are set per segment
5. **Exclusion list verification** — Confirm converters are excluded

Max 2 auto-retry cycles on gate failures.

---

## Phase 5: Output

Deliver the retargeting package:

- **Campaign architecture diagram** (segments, creative, timing)
- **Audience segment definitions** (platform-ready specs)
- **Ad copy per segment per platform**
- **Budget allocation table**
- **Frequency cap settings**
- **Exclusion rules**
- **Policy compliance checklist** (per platform)
- **Gate pass/fail summary**

Write output to `E:\Dev2\kai-cmo-harness-work\workspace\` with filename pattern: `retarget-campaign-YYYY-MM-DD.md`
