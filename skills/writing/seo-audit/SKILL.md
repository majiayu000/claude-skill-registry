---
name: seo-audit
description: Audit any URL against 17-point technical SEO checklist + algorithmic authorship rules. Uses /browse if available, falls back to checklist-based audit.
---

# /seo-audit — The SEO Strategist

Audit any URL against the harness's technical SEO checklist and algorithmic authorship rules. If gstack's `/browse` is available, crawls the live page for real data. Otherwise, runs a checklist-based audit on provided content.

## Arguments

Required:
- **url**: The URL to audit (or file path for local content)

Optional:
- **--deep**: Run the full 17-point technical SEO audit (default: content-only)
- **--site**: Site key for GSC data context

Example: `/seo-audit https://kaicalls.com/blog/ai-receptionists`
Example: `/seo-audit article.md --site kaicalls`

## The Skill

### Step 1: Load SEO Checklists

Read from the knowledge base:
- `knowledge/checklists/technical-seo-audit-sop.md` — 17-point Screaming Frog SOP
- `knowledge/checklists/seo-checklist.md` — SEO validation checklist
- `knowledge/frameworks/content-copywriting/algorithmic-authorship.md` — writing rules
- `knowledge/frameworks/aeo-ai-search/aeo-ai-search-playbook-2026.md` — AI search optimization

### Step 2: Gather Page Data

**If /browse is available** (gstack installed):
Try using the browse skill to load the page:
```
$B navigate {url}
$B snapshot -i
```

Extract from the live page:
- Title tag and meta description
- H1, H2 hierarchy
- Word count
- Internal/external link count
- Image alt text coverage
- Schema markup presence
- Page load indicators

**If /browse is NOT available:**
Tell the user: "/browse not available — running checklist-based audit. For live page crawling, install gstack."

If the input is a URL, attempt to fetch basic metadata. If it's a file path, read the file directly.

### Step 3: Content Quality Audit

Run the quality scorer on the page content:
```bash
kai-gate score {content_file} --format json --rules aa,geo
```

Score specifically against:
- Algorithmic Authorship rules (conditions after clause, verbs first, sentence length)
- AEO signals (entity mentions, citation patterns, information gain)
- Content structure (heading hierarchy, list formatting, bold usage)

### Step 4: Technical SEO Checklist

Evaluate against the 17-point checklist:

```
SEO AUDIT — {url}
══════════════════════════════════════════

CONTENT QUALITY: {score}/100
  Algorithmic Authorship: {aa}%
  AEO/AI Search Signals:  {geo}%
  Content Structure:       {cs}%

TECHNICAL SEO:
  [PASS] Title tag present and under 60 chars
  [PASS] Meta description present and under 160 chars
  [FAIL] H1 missing or duplicate
  [PASS] H2 hierarchy logical
  [WARN] Only 1 internal link (recommend 3+)
  [PASS] Images have alt text (4/4)
  [FAIL] No schema markup detected
  [PASS] Word count: 1,423 (target: 1,200-1,800)
  [WARN] Keyword density: 0.8% (target: 1-2%)
  [PASS] Average sentence length: 16 words (target: <20)
  [N/A]  Page speed (requires /browse --deep)

AEO/AI SEARCH READINESS:
  [PASS] Entity mentioned 3+ times
  [WARN] No citation-style references
  [FAIL] No FAQ schema for passage extraction
  [PASS] Clear atomic facts in opening paragraph

OVERALL: {total_pass}/{total_checks} passed
```

### Step 5: Recommendations

Prioritize fixes by impact:

```
FIX PRIORITY:
  1. [HIGH]   Add FAQ schema markup — enables Featured Snippet extraction
  2. [HIGH]   Fix H1 tag — currently missing/duplicate
  3. [MEDIUM] Add 2 more internal links — improves PageRank flow
  4. [LOW]    Increase keyword density from 0.8% to 1.2%
```

### Step 6: Offer Fixes

If the content is a local file (not a live URL): "Want me to fix the content issues? The technical SEO issues (schema, H1) need to be fixed in the HTML template."

## Error Handling

- **/browse unavailable**: Graceful fallback to checklist-based audit
- **URL unreachable**: Suggest checking the URL, offer to audit a local file instead
- **No GSC data**: Audit without search performance context

## Chain State

**Standalone:** Does not require prior chain steps
**Optional reads:** GSC data via `kai-report` for keyword context
