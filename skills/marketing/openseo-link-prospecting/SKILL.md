---
name: openseo-link-prospecting
description: >-
  Find realistic link prospects with SERP and backlink evidence, discover
  contact paths via web tools, and draft personalized outreach — with targets
  saved to .seo/backlink-targets.json for off-page-seo campaigns. Use this
  skill when the user has a linkable asset (study, tool, guide, template,
  product page) and wants backlinks, resource-page inclusions, or comparison
  mentions. Triggers: "link prospecting", "find backlink opportunities",
  "resource page outreach", "get backlinks for", "link building outreach".
category: seo
tier: nice-to-have
layer: distribution
reads:
  - brand/positioning.md
env_vars:
  - OPENSEO_API_KEY
  - OPENSEO_MCP_URL
triggers:
  - link prospecting
  - find backlink opportunities
  - resource page outreach
  - get backlinks for
  - link building outreach
allowed-tools:
  - Bash(mktg catalog *)
  - Bash(mktg run *)
---

# OpenSEO Link Prospecting

Find pages, sites, and authors that might realistically reference the user's linkable asset — then hand `off-page-seo` a qualified target list at `.seo/backlink-targets.json` instead of a cold start.

## On Activation

1. **Readiness + binding**: `mktg seo status --json --fields readiness,catalog.endpointError,project`. `not_configured` → prospect with Exa search only (queries below still apply) and label authority data `unknown`. For a ready state, verify live access with the free `whoami` MCP tool before paid calls.
2. **Clarify the asset**: what page/study/tool/template is being promoted and WHY someone would reference it. No clear asset + reason → fix that first; outreach without a reason is spam.
3. Read `brand/positioning.md` for angle/audience fit (tolerate missing).

## OpenSEO MCP Tools

- `get_serp_results`: find ranking articles, listicles, resource pages, comparisons, statistics pages (≤10 queries per call).
- `get_backlinks_overview`: competitor backlink/referring-domain patterns — where do THEY get links (may be unavailable; continue without).
- `get_backlinks_profile`: page-level source/target/anchor/dofollow/lost/broken evidence. Preserve target scope, pagination, filters, and one-per-domain mode in `.seo/backlink-targets.json` provenance.
- `get_domain_overview`: qualify strong prospect domains.
- `get_ranked_keywords`: topical-fit checks on prospects/competitors.
- `research_keywords`: expand prospecting queries.

## Contact Discovery (NOT OpenSEO)

Contact paths come from web/search/browser tools (Firecrawl fetch, Exa search, browser automation) — never attribute these to OpenSEO:

- Author byline pages, contact pages, editorial guidelines, about/team pages
- LinkedIn/X/Bluesky profiles, newsletter mastheads
- Public emails in HTML or visible text; `Person`/`Organization`/`sameAs`/`email` structured data

Record only contact details actually found, each with its source URL.

## Prospecting Query Patterns

`<topic> resources` · `best <category> tools` · `<competitor> alternatives` · `<topic> statistics` · `<topic> guide` · `<topic> examples` · `<topic> templates` · `<topic> software` · `<topic> for <audience>`

## Workflow

1. Build 5–10 prospecting queries from the asset; `get_serp_results` in batches.
2. Competitors supplied? `get_backlinks_overview` their strongest domains first.
3. Filter: keep editorial pages, resource lists, comparisons, statistics, templates, curated directories. Drop homepages, login walls, thin affiliate, spam, and direct competitors (unless a comparison angle is valid).
4. Per prospect, define the angle: broken/missing resource, better current data, useful tool/template, comparison inclusion, expert quote.
5. Contact discovery on the strongest prospects via web tools (source URLs recorded).
6. Write targets to `.seo/backlink-targets.json`:

```json
{ "version": 1, "updatedAt": "<iso>", "asset": "<url>", "targets": [{ "url": "", "domain": "", "source": "", "relevance": "", "angle": "", "contactPath": "", "contactSource": "", "priority": "high|med|low", "status": "new" }] }
```

7. Draft 2–3 reusable outreach messages (resource inclusion, article update, comparison angle). Hand the list to `off-page-seo` for the campaign cadence.

## Output Format

| Prospect URL | Domain | Source | Relevance | Suggested angle | Contact path | Priority |
| ------------ | ------ | ------ | --------- | --------------- | ------------ | -------- |

## Anti-Patterns

- **Inventing emails, handles, or contact names** — because a single fabricated contact burns the user's credibility with a real human. Only record what was found, with the source URL; otherwise name the next discovery step.
- **Attributing contact discovery to OpenSEO** — because OpenSEO finds PROSPECTS; web/browser tools find CONTACTS. The misattribution teaches a wrong tool model and hides the real source when details need re-verification.
- **Mass-template outreach** — because editors can smell a blast, and one spam report damages the domain's future deliverability. Personalize by page and reason, or don't send.
- **Prospecting without a linkable asset and reason** — because "please link to my homepage" converts at ~0%. No asset + reason, no outreach.
- **Skipping competitor/paid-placement flags** — because pitching a direct competitor or a pay-to-play listicle wastes the user's outreach capital and can backfire publicly. Flag both in the target list.

## Close the loop

After writing files, log completion so `mktg plan` / `mktg status` count the work (bare `mktg run` only logs `loaded`):

```bash
mktg run openseo-link-prospecting --complete --writes <paths written> --result success --json
```


---

*Adapted from [every-app/open-seo](https://github.com/every-app/open-seo) `.agents/skills/link-prospecting` (MIT). Workflow upstream; mktg artifact paths, off-page-seo handoff, and contact-attribution discipline added here.*
