---
name: kai-write
description: Write a single piece of marketing content using Kai CMO Harness frameworks and quality gates. Supports blog posts, LinkedIn articles, emails, cold outreach, press releases, ad copy, and TikTok scripts. Automatically loads the right framework, skill contract, and persona. Use when "write a blog post", "draft an email", "LinkedIn article", "cold outreach", "write ad copy", "press release", "TikTok script", or any single content creation request. For building a complete email system, use /kai-email-system instead.
---

Write one piece of content using the Kai CMO Harness. Loads the right framework, applies quality gates, outputs ready-to-publish copy.

## Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions. It has the product name, ICP, value prop, monetization, brand voice, current channels, and competitive landscape.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

---

## Step 1: Identify Format and Load Context

Determine the content format from the user's request, then load the corresponding files from the harness at `E:\Dev2\kai-cmo-harness-work`:

| Format | Framework | Contract | Checklist |
|--------|-----------|----------|-----------|
| Blog post | `knowledge/frameworks/content-copywriting/algorithmic-authorship.md` | `harness/skill-contracts/blog-post.yaml` | `knowledge/checklists/content-checklist.md` |
| LinkedIn | `knowledge/channels/linkedin-articles.md` | `harness/skill-contracts/linkedin-article.yaml` | — |
| Email (lifecycle) | `knowledge/channels/email-lifecycle.md` | `harness/skill-contracts/email-lifecycle.yaml` | — |
| Email (cold) | `knowledge/channels/email-lifecycle.md` + `harness/references/cold-email-rules.md` | `harness/skill-contracts/cold-email.yaml` | — |
| Meta ads | `knowledge/channels/meta-advertising.md` + `harness/references/meta-ads-rules.md` | `harness/skill-contracts/meta-ads.yaml` | `knowledge/checklists/meta-advertising-checklist.md` |
| Google ads | `knowledge/channels/paid-acquisition.md` + `harness/references/google-ads-policy-reference.md` | `harness/skill-contracts/google-ads.yaml` | `knowledge/checklists/paid-acquisition-checklist.md` |
| Press release | `knowledge/channels/press-releases.md` | — | `knowledge/checklists/pr-checklist.md` |
| TikTok | `knowledge/channels/tiktok-algorithm.md` | — | `knowledge/checklists/tiktok-checklist.md` |
| SEO content | `knowledge/frameworks/content-copywriting/algorithmic-authorship.md` + `knowledge/frameworks/aeo-ai-search/aeo-ai-search-playbook-2026.md` | `harness/skill-contracts/blog-post.yaml` | `knowledge/checklists/seo-checklist.md` |

Read the framework file(s) and skill contract before writing. Do not guess at rules — load them.

## Step 2: Brief

If the user hasn't provided a brief, create one using `harness/brief-schema.md`. At minimum, confirm:
- **Persona** — which of the 8 personas from `knowledge/personas/_persona-index.md`?
- **Angle** — what's the specific frame? (not just the topic)
- **CTA** — what do we want the reader to do?

For ad copy, also confirm the platform so the right policy reference gets loaded.

## Step 3: Write

Apply the framework rules. Key universal rules:
- No banned words (leverage, utilize, synergy, innovative, deep dive, circle back, touch base, moving forward, at the end of the day)
- No AI slop ("In conclusion", "It's important to note", "In today's rapidly evolving")
- **No X-not-Y binary clichés** — every form: "X, not Y" / "isn't X — it's Y" / "It's a Y, not a Z" / "X — not Y". The pattern reads as LinkedIn slop and slips past subjective scoring. Use parallel-positive contrast or a single load-bearing claim instead.
- Match the persona's language patterns and pain points
- Single primary CTA
- Follow word count from the skill contract

For SEO content, also apply Algorithmic Authorship rules:
1. Conditions AFTER main clause ("Do X if Y")
2. Instructions start with verbs
3. Sentences under 20 words
4. Bold the answer, not query-matching terms

## Step 4: Quality Gate

Score and validate before delivering:

1. **Four U's** — Unique, Useful, Ultra-specific, Urgent (each 1-4). Min 12/16 for blog/SEO, 10/16 for email/ads.
2. **Banned words** — zero Tier 1 violations
3. **AI slop** — zero instances
4. **Voice patterns (programmatic — DO NOT skip)** — grep the draft with the Grep tool for these regexes. Any hit fails the gate.
   - `, not [a-z]` (catches "X, not Y")
   - `— not [a-z]` (catches "X — not Y")
   - `\bisn'?t [a-z][^.\n]+ — it'?s\b` (catches "isn't X — it's Y")
   - `\bIt'?s (a\|the\|an) [^.\n]+, not (a\|the\|an)\b` (catches "It's a X, not a Y")
   - `\bIf you [a-z][^,.]+, [a-z]` (catches "If you X, Y")
   - `\bHere'?s the thing\b` / `\bLet that sink in\b` / `\bHot take\b` / `\bI'?ll be honest\b` (LinkedIn slop)

   Skip matches inside HTML comments and code fences. Replacements: collapse to a single load-bearing claim, or use parallel-positive contrast where both halves are affirmative.

5. **Format-specific gates** — from the skill contract (subject line length, word count, CTA count, etc.).

**Hook integration:** if the project has `.claude/hooks/voice-gate.py`, the hook fires PostToolUse on Edit/Write and catches voice violations at draft time. The gate step still runs the regexes — belt and suspenders.

If the piece fails, fix the specific issues and re-score. Max 2 retries. After 2 failures, deliver with failures noted.

## Step 5: Deliver

Output the content with quality gate scores visible. Save to `workspace/` if requested.
