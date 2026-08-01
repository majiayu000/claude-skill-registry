---
name: kai-social
description: Plan and batch-produce social media content across platforms (Instagram, X/Twitter, TikTok, LinkedIn, YouTube). Generates a week or month of posts with platform-specific formatting, hashtags, hooks, and posting schedule. Use when "social media posts", "social calendar", "plan social content", "Instagram posts", "tweets", "LinkedIn posts", "TikTok ideas", "social media strategy", "batch social", or any request to systematically produce social media content.
---

# /kai-social — A Week or Month of Posts, Ready to Schedule

> **Kai root note:** `knowledge/`, `harness/`, and `scripts/` paths in this skill live in the Kai install, not the user's project. Resolve them against the first ancestor directory of this SKILL.md that contains a `knowledge/` folder (the Kai plugin root, `~/.claude/kai`, or the kai-cmo-harness repo). `MARKETING.md`, `memory/`, and any output files live in the current project. If a referenced `scripts/` command is not available in this install, say so, skip it, and continue with the file-based guidance — never fabricate its output.

## Objective

A calendar the user approves, then a batch of finished posts against it — each one written natively for its platform, each carrying a hook that survives the first line or first three seconds, and none of which could have been written for any other brand. The batch is scheduleable as-is: copy, hashtags where they apply, visual direction, posting time.

The failure mode this skill exists to prevent is one post reformatted five ways. Platform-native means written for the platform, not resized for it.

## Done when

Work type `social-post` — floor **E5/C2/O3** (`harness/eco-floors.yaml`), read per post.

- **E5** — the provider returns a post id and the public permalink read-back matches the approved text. Drafting reaches E2 (`harness/skill-contracts/social-post.yaml` satisfied); the calendar's approval reaches E3; only publishing carries a post to E5. A batch sitting in `workspace/social/` is not shipped.
- **C2** — `four_us_score` at **10/16** minimum and `banned_word_check` pass on every post.
- **O3** — reach, engagement rate, profile clicks, and link clicks read from platform insights at 7 days.

## Constraints

- **Approval gate before production.** Present the calendar and get sign-off before writing posts. Publishing is a second, separate approval — this skill does not post to any live account.
- **Load the platform's organic posting rules before writing for that platform**, same as ad policy references bind ad copy: `harness/references/x-organic-posting-rules.md`, `harness/references/meta-organic-posting-rules.md` (Instagram/Facebook/Threads), `harness/references/linkedin-organic-posting-rules.md`, `harness/references/tiktok-organic-posting-rules.md`, `harness/references/youtube-organic-posting-rules.md`, `harness/references/pinterest-organic-posting-rules.md`, `harness/references/snapchat-organic-posting-rules.md`, `harness/references/reddit-organic-posting-rules.md`. Automation and volume limits: `harness/references/social-automation-rules.md`.
- **Material connections get disclosed** — paid, gifted, affiliate, or employee-authored content follows `harness/references/creator-disclosure.md`. No buried `#ad`.
- **No invented proof.** Customer results, metrics, testimonials, and case-study numbers come from a source or they do not appear. A social-proof pillar with no proof is a data gap, not a creative prompt.
- **Read `MARKETING.md` from the project root before asking the user anything.** If it does not exist, build it from the codebase — README, manifests, landing pages, route files, analytics and email config — and confirm the draft.

**Per-post bar** — every post clears all six:

1. Hook in the first line. No warm-up, no preamble.
2. Zero banned words.
3. Zero AI slop.
4. Platform character limits respected.
5. One CTA, or none for a pure value post.
6. Not generic — it could only have come from this brand.

**Pillar mix** — the default balance, adjusted only for a stated reason:

| Pillar | Share |
|---|---|
| Value / educational | 40% |
| Social proof | 25% |
| Product | 20% |
| Culture / behind-the-scenes | 15% |

**Platform format contracts:**

| Platform | Format |
|---|---|
| LinkedIn | Hook line (pattern interrupt or bold claim), 3–5 short paragraphs, line breaks between every thought, CTA at the end, 1200–1500 chars optimal |
| X/Twitter | Single tweets max 280 chars with the hook front-loaded; threads 3–7 tweets, each standalone valuable, numbered, CTA or summary at the end |
| Instagram | Captions 150–300 words with the hook before the "…more" cut; carousels 5–10 slides, one idea per slide, bold text; Reels scripted with the hook in the first 3 seconds |
| TikTok | Hook in the first 2 seconds (question, bold claim, or visual pattern interrupt), 15–60 second script, trending format adaptation, CTA as the last frame |
| YouTube | Shorts 30–60 second hook-first script; community posts as a poll or discussion question |

## Context

Seven things must be known before the calendar is built — `MARKETING.md` answers most: what the brand is posting about, which platforms, the time horizon (one week or one month), cadence per platform, the content pillars (educational, behind-the-scenes, product, social proof, culture), tone (professional, casual, bold, irreverent), and what existing content — blog posts, videos, assets — can be repurposed.

| Need | Load |
|---|---|
| Output structure, gate thresholds | `harness/skill-contracts/social-post.yaml` |
| Cross-platform strategy and cadence | `knowledge/playbooks/social-media-strategy.md` |
| Instagram formats and behavior | `knowledge/channels/instagram.md` |
| X/Twitter formats and behavior | `knowledge/channels/x-twitter.md` |
| TikTok distribution mechanics | `knowledge/channels/tiktok-algorithm.md` |
| YouTube formats | `knowledge/channels/youtube.md` |
| LinkedIn long-form | `knowledge/channels/linkedin-articles.md` |
| Product, ICP, voice, current channels | `MARKETING.md` (project root) |

**Output** goes to `workspace/social/`: `_calendar.md` (day, platform, pillar, format, hook, status), one file per post under a per-platform folder (`linkedin/`, `x-twitter/`, `instagram/`, `tiktok/`), and `_quality-report.md`. Each post file carries format, hook, copy, hashtags where applicable, visual direction, and posting notes (best time, cross-post targets). Same paths as v1 — downstream tooling does not branch on version.

## Escalate when

- A pillar the user asked for has no sourced material behind it — social proof without results, product posts without a shipped feature.
- The requested cadence exceeds what the platform's automation rules allow for the account type.
- A post would make a regulated, health, financial, or comparative claim needing substantiation.
- Content involves a creator, employee, or partner and the disclosure obligation is unresolved.
- The user asks to publish or schedule directly to a live account.
