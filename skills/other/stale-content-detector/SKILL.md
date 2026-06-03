---
name: stale-content-detector
description: "Find pages and posts that haven't been updated in a long time. Categorize as fresh / aging / stale / archive-candidate. Suggest refresh, redirect, or archive per item — based on age, traffic signal, and internal link count."
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: audit
---

# Stale Content Detector

**Version:** 1.0.0
**Updated:** 2026-05-24
**Category:** audit
**Status:** stable
**Requires:** Respira for WordPress plugin 7.1+ + MCP server

---

## Description

Find pages and posts that haven't been updated in a long time, categorize them as fresh / aging / stale / archive-candidate, and suggest action per item: refresh, redirect, archive, or leave alone. Stale content is an SEO drag and a credibility tax — if your "2023 trends" article still ranks but nobody's touched it since 2023, you're losing trust the day a reader notices the date.

This skill is intentionally focused. It's not a content audit (use [SEO & AEO Amplifier](https://respira.press/skills/seo-aeo-amplifier) for that). It's the "what's old" question, answered fast.

---

## What it categorizes

| Bucket | Age since last update | Suggested action |
|---|---|---|
| Fresh | < 6 months | leave alone |
| Aging | 6–12 months | review the headline + opening paragraph; if still accurate, leave; if outdated, refresh the date |
| Stale | 12–24 months | refresh the content meaningfully (new data, new examples), update the modified date |
| Archive-candidate | 24+ months **and** low traffic / orphan | archive, redirect, or 410 — depends on if anything links to it |

Plus an "evergreen" override: pages tagged as evergreen (`/about/`, `/contact/`, `/pricing/`, `/privacy/`) skip the staleness check entirely.

---

## When to Use

- Quarterly content review
- Migrating a site and trying to decide what to bring vs leave behind
- After a content team change — find the inherited backlog of old work
- Before publishing the next batch of new content (so the old stuff doesn't drag the rankings of the new stuff)
- After a Google update that emphasizes "freshness" signals

---

## Trigger Phrases

- "find old content"
- "what's stale"
- "what needs refreshing"
- "audit my content age"
- "find content to update"
- "stale content scan"
- "what should i archive"

---

## Execution Workflow

### Step 1 — Confirm site

Call `respira_get_active_site` + `respira_get_site_context`.

### Step 2 — Pull pages and posts

Call:

- `respira_list_pages(per_page=100)` for pages
- `respira_list_posts(per_page=100, status=publish)` for posts
- `respira_list_custom_posts(post_type=<each non-default CPT>, per_page=100)` for any CPT detected via `respira_list_post_types`

Each result includes `modified` and `date`. Sort by `modified` ascending — oldest first.

### Step 3 — Identify evergreen pages

Pull the list of pages and check each against the evergreen list (`/about`, `/contact`, `/pricing`, `/privacy`, `/terms`, `/legal`, `/imprint`, `/faq`, `/support`). If the URL or slug matches, flag as evergreen and skip the staleness check.

Also check if the post type has `has_archive=false` and a single URL pattern matching contact/legal/utility — those are usually evergreen.

### Step 4 — Compute staleness

For each non-evergreen page or post, compute days-since-modified. Bucket:

- 0–180 days → **fresh**
- 181–365 days → **aging**
- 366–730 days → **stale**
- 731+ days → **archive-candidate** (further filtering in Step 5)

### Step 5 — Add traffic + orphan signals (archive-candidate filter)

For items in the archive-candidate bucket, we need to know if anyone is reading them or linking to them. Two signals:

1. **Internal link count.** Call `respira_find_element` with the page's URL as a search term. Count incoming internal links. If zero, the page is an orphan.
2. **External traffic** (if available — depends on whether the site has Plausible / GA4 / similar wired to Respira). If not available, skip.

Recompute:

- Archive-candidate + orphan + no traffic → **archive (or 410)**
- Archive-candidate + has internal links + no traffic → **archive + redirect** (preserve link equity)
- Archive-candidate + has traffic → **refresh** (downgrade from archive-candidate to stale)

### Step 6 — Output the report

```markdown
## Content age audit for {site_url}

Scanned {n_pages} pages + {n_posts} posts + {n_custom} custom posts ({n_total} total). Evergreen pages skipped: {n_evergreen}.

### Summary

| Bucket | Count | % |
|---|---|---|
| Fresh (<6mo) | {n_fresh} | {pct_fresh}% |
| Aging (6–12mo) | {n_aging} | {pct_aging}% |
| Stale (12–24mo) | {n_stale} | {pct_stale}% |
| Archive-candidate (24+mo) | {n_archive} | {pct_archive}% |

### Stale (12–24 months)

| Title | Last modified | Action |
|---|---|---|
| {title} | {modified} ({days_ago}d) | refresh |
| ... | | |

### Archive-candidate (24+ months)

| Title | Last modified | Internal links | Suggested action |
|---|---|---|---|
| {title} | {modified} ({days_ago}d) | {link_count} | {action} |
| ... | | | |

### What I'd refresh first (top 5 by traffic or link equity)

1. **{title}** ({days_ago}d old) — {one-line reason: high incoming link count / high traffic / topical relevance to current focus}
2. ...
```

### Step 7 — Offer to act on a chosen item

Ask: *"Want me to refresh one of these now? I can pull the existing content, suggest updates, create a duplicate with the refresh applied, and you review."*

If yes, route to the SEO & AEO Amplifier skill or directly compose `respira_create_page_duplicate` + targeted updates.

---

## Hard rules

- **Never delete a page directly.** Even archive-candidates get a recommendation, not a deletion. The user decides. Use `respira_delete_page` only if the user explicitly asks for deletion of a specific named page.
- **The evergreen list is opinionated but overridable.** Output the list at the top of the report so the user can see what got skipped and add/remove items.
- **Don't conflate stale with bad.** A 2-year-old page that still has 1,000 monthly views is not a problem. The "refresh" recommendation is based on age, not quality.
- **Modified date is canonical.** Don't read `date` (published) as a staleness signal. A 2018 post updated last month is fresh.
- **Custom post types matter.** Case studies, podcast episodes, properties — these often need different staleness windows. If the user runs a podcast and the latest episode is 6 months old, that's stale for podcast content even though "fresh" for blog posts. Offer to set per-CPT windows on a v1.1 of this skill.

---

## Telemetry

Records: site URL hash, n_pages / n_posts / n_custom counted, bucket distribution, success/failure, total duration. No page titles, no URLs, no decisions sent.

Endpoint: `POST https://www.respira.press/api/skills/track-usage`
