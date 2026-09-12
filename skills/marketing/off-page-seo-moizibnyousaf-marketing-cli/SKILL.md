---
name: off-page-seo
description: "Ongoing link-building campaigns that raise domain authority and expand a site's KD ceiling beyond what on-page work alone can earn. Use when the user mentions 'off-page SEO', 'link building', 'directory link building', 'backlink campaign', 'listicle placements', 'guest posts', 'outreach targets', 'get listed in listicles', or asks 'how do I get more domain authority'. Generates a prioritized, researched target list across directories, listicles, and guest-post candidates — does NOT submit anything on the user's behalf. Pairs with `mktg-backlink-prospector` agent for parallel research. For a launch-day push (submit to directories, Product Hunt, BetaList), see /startup-launcher. For measured backlink data — referring domains, backlink counts, rank tracking — see /openseo. Distinct from `seo-machine` (on-page programmatic) and `seo-audit` (technical diagnostic). The off-page half of the SEO operation."
category: seo
tier: nice-to-have
reads:
  - brand/positioning.md
  - brand/competitors.md
  - brand/audience.md
  - brand/voice-profile.md
writes: []
triggers:
  - off-page seo
  - link building
  - directory link building
  - backlink campaign
  - guest posts
  - outreach targets
  - listicle placements
  - get listed in listicles
  - domain authority
---

# Off-Page SEO

On-page work caps out around DR + 20 in achievable KD targets. Off-page work expands that ceiling. This skill generates a prioritized backlink target list across three lanes — directories, listicles, guest posts — and a starter-stack checklist of universal SaaS submission flows. **It does not submit anything.** The user (or the user's outreach team) does the actual submission.

The off-page half of the SEO operation. Pairs with `seo-machine` (on-page programmatic sprint) — ship pages with seo-machine, queue outreach with this skill, run them in parallel.

## On Activation

1. Load brand context: `positioning.md`, `competitors.md`, `audience.md`, `voice-profile.md`. Missing files are fine.
2. Surface what loaded:

## Backend Selection

Prefer OpenSEO `get_backlinks_overview` / `get_backlinks_profile` / `get_domain_overview` and `openseo-link-prospecting` outputs when configured. Preserve backlink target scope, filters, pagination, and provider limits; totals without scope are ambiguous. Otherwise use Exa/web with authority metrics `unknown`. Full contract: `skills/openseo/references/backend-contract.md`.

```
Brand context loaded:
├── Positioning    ✓/✗  (drives outreach angle + value-add framing)
├── Competitors    ✓/✗  (target list source — Recipe F runs on them)
├── Audience       ✓/✗  (selects niche-specific directories + communities)
└── Voice Profile  ✓/✗  (shapes outreach email tone if user chains into cold-email)
```
3. If `competitors.md` is missing, prompt the user for 3-7 direct competitors before running Recipe F (the researched-target-list recipe needs competitor domains as input).
4. Check for `.seo/backlink-targets.json` in the current project. If present, this is a re-run — show the user the existing target counts and ask whether to refresh or just present the existing list.

## When to use vs adjacent skills

| Skill | When | When NOT |
|---|---|---|
| `off-page-seo` (this) | Building a prioritized backlink target list + universal starter-stack checklist | Doing actual outreach (use `cold-email` for that) |
| `seo-machine` | On-page programmatic sprint (alternatives, comparison, use-case pages) | Off-page work — this skill |
| `seo-audit` | Diagnosing on-site technical issues | Building backlink target lists |
| `cold-email` (in direct-response-copy) | Writing the outreach emails after target list exists | Generating the target list itself |
| `startup-launcher` | Launch-day platform submissions (Product Hunt, BetaList, etc.) | Ongoing backlink work post-launch |

## The Starter Stack (universal SaaS submission flow)

Every new site should be submitted to these by week 4. Most are free; all are worth a one-time submission. This is the **mechanical work** — checklist, not creative.

### Directories (submit and check off)

| Directory | DR (approx) | Notes |
|---|---|---|
| **Product Hunt** | 90+ | Single biggest launch-day backlink + traffic source. Coordinate with `startup-launcher`. |
| **G2** | 88+ | Becomes a destination for "[brand] reviews" searches; needs screenshot + verification email. |
| **Capterra / GetApp / Software Advice** | 80+ | Gartner Digital Markets — same submission flow across all three. |
| **SaaSHub** | 65+ | Quick win, free. |
| **AlternativeTo** | 80+ | List as alternative to top 5 competitors. Required free submission. |
| **BetaList** | 70+ | Only if pre-launch or recently launched. |
| **Indie Hackers** | 75+ | Products section. Founder-friendly community. |
| **TopAlternatives.com / SimilarSiteSearch / Slant.co** | 50–65 | Niche but cumulatively useful. |
| **Crunchbase** | 92+ | Even free profile gets DR pass-through. |

### Community surfaces (selective)

| Surface | When to engage | Hard rule |
|---|---|---|
| **Niche subreddits** | Find via Exa search "site:reddit.com [audience] [problem]" or Ahrefs site-explorer on reddit.com for your keywords | Engage genuinely for 2+ weeks before mentioning the product. Never just post a link. |
| **Slack/Discord communities** | For your audience persona | Join 3-5, contribute substantively for 2 weeks before mentioning. |
| **Hacker News** | For technical products | Show HN posts can drive enormous traffic spikes — require a real launch story, not "we built another SaaS." |

### Founder outreach (slow-burn channel)

- **Founder link trades** with complementary (non-competitive) products. Reach out to 5-10 founders of products your audience also uses. Offer mutual blog mentions, "tools we love" pages, or guest posts.
- **Guest posts on DR 30+ niche blogs.** Find via Recipe F (competitor referring-domains). Pitch 1-2 strong posts per month — not spray-and-pray.

## Recipe F — Researched Target List

Use Exa MCP (mktg default) or Ahrefs MCP (if connected) to surface high-value link opportunities your competitors already have. The target list is built FROM your competitors' existing backlinks.

### Exa path (mktg default)

For each top-3 competitor:

```
mcp__exa__web_search_advanced_exa
query: "[competitor-domain] -site:[competitor-domain]"
filter: linksTo:[competitor-domain]
limit: 50
```

Then for each result, scrape the page (Exa `crawling_exa` or `firecrawl`) and extract: domain, page title, anchor text. Filter to DR≥30 sites via a separate `exa__company_research_exa` lookup, OR by manual triage of well-known authority domains.

### Ahrefs appendix (only if you have a paid sub)

If `mcp__ahrefs__subscription-info-limits-and-usage` returns data AND you want numeric precision on referring-domain DR, run:

```
mcp__ahrefs__site-explorer-referring-domains
target: <competitor-domain>
where: domain_rating >= 30 AND traffic_dofollow >= 100
order_by: domain_rating:desc
limit: 100
```

This replaces only the DR-proxy step in the Exa path above. Ahrefs MCP is not in mktg's chained-in ecosystem — keep this as a footnote, not a default.

Then for each candidate domain (Exa-path or Ahrefs-path), filter manually into buckets:

| Bucket | Signal |
|---|---|
| **Directory candidates** | Site name matches "[category] directory", "best of [category]", "[category] tools", "alternatives to [tool]" |
| **Listicle candidates** | Blog posts titled "Top X [category] in YYYY" — pitch yourself for inclusion |
| **Guest-post candidates** | Looks like a blog (`*.com/blog/...` URLs), DR 30+, posts on your niche topic |
| **Skip** | PR wires, paid networks, irrelevant niches, sites that link to *everyone* in the space |

### Output schema (.seo/backlink-targets.json)

```json
{
  "generated_at": "YYYY-MM-DD",
  "research_backend": "exa" | "ahrefs" | "manual",
  "directories": [
    { "domain": "g2.com", "dr": 88, "url_to_submit": "https://www.g2.com/products/new", "competitor_uses": ["hootsuite", "buffer"] }
  ],
  "listicles": [
    { "domain": "thedigitalprojectmanager.com", "dr": 65, "url": "https://...", "topic": "Best Twitter monitoring tools", "competitor_listed": "hootsuite" }
  ],
  "guest_posts": [
    { "domain": "indiehackers.com/blog", "dr": 81, "topic_fit": "founder-led marketing" }
  ]
}
```

This file lives at the project root under `.seo/` and is read by the `mktg-backlink-prospector` agent on future runs to avoid duplicate prospecting.

## Parallel research via mktg-backlink-prospector agent

When the user wants a fresh target list and there are 3+ competitors to research, /cmo should spawn the `mktg-backlink-prospector` agent rather than running Recipe F inline. The agent fans out competitor-by-competitor research in parallel, returns the consolidated `.seo/backlink-targets.json`, and frees /cmo's context for the next decision.

See `agents/research/backlink-prospector.md` for the spawn contract.

## Phase template (when seo-machine sprint integration is wanted)

When the user is also running a `seo-machine` sprint, off-page phases land near the end of the tracker:

```markdown
### Phase N — Starter-stack directory submissions

**Why:** baseline backlinks from high-DR directories. Cap at 2-3 hours of submission work.

**Scope:**
- [ ] Product Hunt — coordinate launch with startup-launcher
- [ ] G2 — submit product page
- [ ] Capterra — submit product page
- [ ] SaaSHub
- [ ] AlternativeTo — list as alternative to: <competitor-1>, <competitor-2>, ...
- [ ] Indie Hackers — claim product page
- [ ] Crunchbase — basic profile

**Files modified:** none (external work). Track status in `.seo/off-page-status.md`.

### Phase N+1 — Listicle outreach (top 10 targets)

**Why:** "Top X [category]" listicles already rank for our target keywords. Getting added is faster than displacing them.

**Targets (from .seo/backlink-targets.json):**
1. example.com/best-twitter-monitoring-tools (DR 65)
2. example.com/top-social-listening-tools-2026 (DR 72)
3. ... (top 10)

**Action:**
- [ ] For each, find the author via byline or about page
- [ ] Chain into `direct-response-copy` (cold-email mode) for the outreach email
- [ ] Send personalized note: short pitch + screenshot proof of value + link to demo
- [ ] Track reply status in `.seo/off-page-status.md`

**Verification:** 3+ listicles update to include the product within 60 days.
```

## What this skill explicitly does NOT do

- **Auto-submit anywhere.** Submission flows often need real human review (G2 needs screenshot + URL + verification email; Product Hunt needs a launch coordinator).
- **Generate outreach emails.** Use `direct-response-copy` (cold-email mode) for that. This skill produces the target list; the email writer is a separate skill.
- **Track ongoing referring-domain growth.** That's a weekly check-in task the user owns; this skill just provides the initial target list and refreshes it on demand.
- **Run paid networks or link buys.** Black-hat. mktg policy: white-hat only.

## Honest caveats

Off-page work is slower and more uncertain than on-page work. A great alternatives page ranks within 30–90 days. A great backlink campaign might produce 3 useful links in the first month, 10 in three months. **Don't gate the on-page sprint on off-page progress.** Ship pages; queue outreach in parallel.

The compounding effect is also lumpy: one DR 80+ listicle is worth ten DR 30 directories. Prioritize quality over quantity in the target list — 10 well-researched targets beat 100 spray-and-pray submissions.

## Anti-patterns

| Don't | Why |
|---|---|
| Submit to every directory you find | Low-DR directories don't move the needle; cumulative time cost is high, return is low. Stick to the curated starter stack + Recipe F targets. |
| Mass-pitch the same email to 50 listicle authors | Personalization rate-determines reply rate. 10 personalized pitches outperform 100 templated ones by 5–10× in reply rate. |
| Reciprocal link schemes ("you link to me, I link to you") | Google penalizes these patterns at scale. Founder link trades are different (they're editorial decisions); blind reciprocal exchanges are not. |
| Paid links from PBNs (private blog networks) | Black-hat, manually reviewed by Google, results in penalty when caught. Never. |
| Outreach without value-add | A pitch that's just "please add me" gets ignored. Lead with a screenshot, a stat, or a useful angle the author missed. |
| Gate the on-page sprint on backlink growth | Backlink campaigns are 3–6 month timelines. On-page work compounds in parallel — never let outreach uncertainty stop page shipping. |

## Cross-references

- `agents/research/backlink-prospector.md` — parallel-fan-out research agent that builds `.seo/backlink-targets.json`
- `skills/seo-machine/references/off-page.md` — the sibling reference doc inside seo-machine's run-time bundle
- `skills/competitive-intel/SKILL.md` — produces `brand/competitors.md`, the seed input for Recipe F
- `skills/direct-response-copy/SKILL.md` (cold-email mode) — writes the outreach emails once the target list exists
- `skills/startup-launcher/SKILL.md` — coordinates launch-day submission to 56 platforms (overlap on Product Hunt + BetaList; this skill handles the ongoing post-launch off-page work)
