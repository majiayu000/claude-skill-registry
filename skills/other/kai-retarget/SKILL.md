---
name: kai-retarget
description: Design retargeting and remarketing campaign architecture across platforms — audience segmentation, creative strategy, frequency caps, and platform-specific setup with ad policy compliance. Use when "retargeting", "remarketing", "retarget", "re-engage visitors", "abandoned cart", "pixel setup", or any request to bring back visitors who didn't convert.
---

## Objective

A retargeting architecture that is ready to build in the ad accounts: audience segments defined by intent and recency, creative matched to each segment's intent level, frequency caps, exclusion rules, sequence timing, budget split, and platform-compliant ad copy. The plan states which pixel events and URL rules define each audience, so someone can implement it without guessing.

Retargeting fails in two ways — showing the same ad to everyone regardless of how close they got, and showing it so often that it burns the brand. Segmentation and frequency caps exist to prevent both.

## Done when

Work type `paid-ad-campaign` — floor **E5/C4/O4** (`harness/eco-floors.yaml`), `spend_authority: true`.

- **E5** — the platform returns ad object ids and a read-back of the live entities confirms targeting, budget, schedule, and creative match the approved bundle field for field. **Hard stop: live-account mutation without recorded human approval is never SHIPPED, whatever the rest of the evidence shows.**
- **C4** — every platform's policy reference was loaded before the ad was written and the ad was checked against it; Four U's at **10/16** (ad threshold), `banned_word_check` clean, `mutation_risk_lint` clean; frequency caps set per segment; converters and exclusion lists verified in place. Max 2 auto-retry cycles, each naming the specific failure.
- **O4** — CAC, CPL, ROAS, or qualified-lead rate against a threshold declared before launch, read from the ads connector no earlier than the conversion window plus learning phase. Platform-reported ROAS is not attribution; a holdout or geo-split is what supports O5 (`knowledge/frameworks/marketing-science/attribution-and-incrementality.md`).

## Constraints

- **Read `MARKETING.md` from the project root first.** If it does not exist, build it from the codebase — CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, email/ad/analytics config — using the template from `/kai-email-system`, and confirm the draft. Do not ask the user what the product is.
- **Seven things must be known before designing segments:** traffic sources; conversion points that matter; where drop-off happens; which platforms have pixels or tags installed; monthly retargeting budget; which platforms to run; and product shape (B2B or B2C, high-ticket or impulse, long or short sales cycle).
- **Load the policy reference for every active platform before writing a single line of ad copy.** Compliance is not a review step applied afterward.
- **Exclude converters from every retargeting pool.** Also suppress existing customers, employees, and competitors.
- **Frequency caps are mandatory per segment** — typically 3–5 impressions/day maximum.
- **Segment by intent level, not just by "visited the site":** homepage visitors, pricing or product viewers, and cart or form abandoners are three different audiences with three different messages. Set recency windows at 1–3, 3–7, 7–30, and 30–90 days.
- **Budget skews toward higher intent**, and copy respects each platform's character limits and format rules.
- **No live-account mutation.** This skill produces the plan and the copy; building or editing audiences, budgets, and creative in a live account goes through human approval first.

## Context

| Need | Load |
|---|---|
| Retargeting and remarketing mechanics | `knowledge/playbooks/retargeting-remarketing.md` |
| FTC, GDPR consent, pixel and tracking law | `harness/references/advertising-compliance.md` |
| Ad copy structural guardrails | `harness/references/ad-write-guardrails.md` |
| Paid ad format contract and gate minimums | `harness/skill-contracts/meta-ads.yaml` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Platform policy — load the row for each active platform before writing:**

| Platform | Reference |
|---|---|
| Meta | `harness/references/meta-ads-rules.md` |
| Google | `harness/references/google-ads-policy-reference.md` |
| LinkedIn | `harness/references/linkedin-ads-rules.md` |
| TikTok | `harness/references/tiktok-ads-policy-reference.md` |
| Microsoft/Bing | `harness/references/microsoft-ads-rules.md` |
| Pinterest | `harness/references/pinterest-ads-rules.md` |
| Snapchat | `harness/references/snapchat-ads-policy-reference.md` |
| Amazon | `harness/references/amazon-ads-policy-reference.md` |
| X/Twitter | `harness/references/x-ads-policy-reference.md` |

**Creative by intent level:**

| Segment | Signal | Message |
|---|---|---|
| Low intent | Homepage visitors | Brand awareness, social proof |
| Medium intent | Product or pricing viewers | Value props, comparison, objection handling |
| High intent | Cart or form abandoners | Urgency, incentive, friction removal |

**Deliver:** campaign architecture (segments, creative, timing), platform-ready audience definitions (pixel events, URL rules, time windows), ad copy per segment per platform, budget allocation table, frequency cap settings, exclusion rules, a per-platform policy compliance checklist, and the gate pass/fail summary.

**Output** goes to `workspace/` as `retarget-campaign-YYYY-MM-DD.md`. Same path as v1.

## Escalate when

- Pixels or conversion tags are missing on a platform the plan depends on.
- Drop-off data does not exist, so segments would be guessed rather than observed, or consent basis for tracking is unresolved in a jurisdiction the audience covers.
- The product falls in a Special Ad Category (housing, employment, credit) or another restricted vertical where retargeting is limited or banned.
- Budget is too small to sustain frequency across the proposed segment count.
- Anyone asks for the campaign to be built or edited in a live account without recorded approval.
