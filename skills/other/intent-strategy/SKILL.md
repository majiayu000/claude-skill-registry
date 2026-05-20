---
name: intent-strategy
description: Intent mapping and content type decision framework for MD Home Care. Determines what content type to create for a given keyword based on search intent, detects cannibalization, and guides location page expansion.
---

# Intent Strategy for MD Home Care

Maps search intent to the correct content type. Use this skill before creating any new content to ensure the right page type is chosen and no cannibalization occurs.

## CRITICAL RULES

- **NO EM DASHES.** Use commas, full stops, semicolons, or restructure.
- **Always run cannibalization check** before creating new content.
- **One page per intent cluster.** Do not create multiple pages targeting the same keyword.

---

## Intent Types and Content Mapping

### Informational Intent
**User wants to learn or understand something.**

Signals: "what is", "how to", "guide", "explained", "meaning of", "types of"

Examples:
- "what is SIL" -> Blog post
- "NDIS funding guide" -> Blog post
- "how to apply for home care packages" -> Blog post
- "difference between NDIS core and capacity building" -> Blog post

**Content type:** Blog post (in `src/content/blog/`)

### Transactional/Commercial Intent
**User wants to find or hire a service provider.**

Signals: "services", "provider", "near me", "cost", "pricing", "hire", "get started"

Examples:
- "SIL services Sydney" -> Service page
- "NDIS provider near me" -> Service page
- "support coordination cost" -> Service page
- "home care packages provider" -> Service page

**Content type:** Service page (in `src/content/services/`)

### Local Intent
**User wants a provider in a specific location.**

Signals: suburb names, "near me", "in [location]", city names

Examples:
- "support coordination Parramatta" -> Location page
- "NDIS provider Blacktown" -> Location page
- "SIL accommodation Richmond" -> Location page
- "home care Melbourne CBD" -> Location page

**Content type:** Location page (suburb-specific service page)

### Comparison Intent
**User is evaluating providers against each other.**

Signals: "vs", "versus", "compared to", "best", "top", "review", "alternative"

Examples:
- "Feros Care vs MD Home Care" -> Blog post (comparison format)
- "best NDIS providers Sydney" -> Blog post (top X format)
- "Bolton Clarke alternative" -> Blog post or service page with comparison table

**Content type:** Blog post (comparison format) for brand-vs-brand queries. Service pages handle comparison tables for generic "best provider" queries.

### Template/Tool Intent
**User wants a downloadable template or practical tool.**

Signals: "template", "form", "checklist", "printable", "download", "example"

Examples:
- "NDIS incident report template" -> Blog post (template format)
- "progress notes template aged care" -> Blog post (template format)
- "care plan template" -> Blog post (template format)
- "NDIS goal examples" -> Blog post

**Content type:** Blog post (template format, with inline template content)

### Navigation Intent
**User wants to find a specific page or brand.**

Signals: brand names, specific page names, "login", "contact"

Examples:
- "MD Home Care" -> Homepage
- "MD Home Care SIL" -> Relevant service page
- "MD Home Care contact" -> Contact page

**Content type:** No new content needed. Ensure existing pages are optimized.

---

## Content Type Decision Tree

```
1. Does the keyword contain a suburb/city name or "near me"?
   YES -> Local intent -> Location page
   NO -> Continue

2. Does the keyword contain "vs", "best", "top X", "compare"?
   YES -> Comparison intent -> Blog post (comparison format)
   NO -> Continue

3. Does the keyword contain "template", "form", "checklist", "example"?
   YES -> Template intent -> Blog post (template format)
   NO -> Continue

4. Does the keyword contain "services", "provider", "cost", "pricing", "hire"?
   YES -> Transactional intent -> Service page
   NO -> Continue

5. Does the keyword contain "what is", "how to", "guide", "explained"?
   YES -> Informational intent -> Blog post
   NO -> Continue

6. Is it a brand name query?
   YES -> Navigation intent -> Ensure existing page is optimized
   NO -> Evaluate manually based on SERP analysis
```

---

## Cannibalization Detection

### When Cannibalization Happens

Cannibalization occurs when two or more pages compete for the same keyword. Common scenarios for MD Home Care:

1. **Blog post vs service page** competing for the same service keyword
   - Example: Blog "What is SIL?" and service page "SIL Services" both targeting "SIL services"
   - Fix: Blog should target informational intent ("what is SIL NDIS"), service page targets transactional ("SIL services Sydney")

2. **Service page vs location page** competing for location keywords
   - Example: "SIL Services" page and "SIL Services Parramatta" both ranking for "SIL Parramatta"
   - Fix: Main service page should not target specific suburbs. Location pages own suburb keywords.

3. **Multiple blog posts** targeting the same topic
   - Example: Two posts about NDIS funding
   - Fix: Consolidate into one comprehensive post

### Detection Process

```bash
cd ~/Projects/mdhomecarebuild

# Check if any existing pages rank for target keyword
python3 src/scripts/advanced_gsc_analyzer.py --keywords "[target keyword]"

# If pages found, analyze what they rank for
python3 src/scripts/advanced_gsc_analyzer.py --page "/[found-page-path]"
```

### Resolution Rules

- If a **service page** already ranks for the keyword, do NOT create a blog post for it. Optimize the service page instead.
- If a **blog post** ranks for a transactional keyword, consider whether the blog should be redirected to a service page or refocused on informational intent.
- If **two blog posts** compete, merge them into one authoritative post and redirect the weaker one.
- If a **location page** and **service page** compete, ensure the service page links to location pages and does not target suburb-specific keywords itself.

---

## Create New vs Optimize Existing

### Create New Page When:
- No existing page ranks for the target keyword (confirmed via GSC check)
- The intent is clearly different from existing pages
- A new location page is needed for an unserved suburb
- A new comparison or template format is needed

### Optimize Existing Page When:
- An existing page already ranks (even poorly) for the target keyword
- The page ranks in striking distance (positions 11-20)
- Adding content to an existing page would strengthen it without bloating it
- The existing page has authority signals (backlinks, age) worth preserving

---

## Location Page Expansion Framework

### Suburb Prioritization Criteria

Rank potential suburbs by:

1. **Search volume** (GSC data for "[service] [suburb]" queries)
2. **NDIS participant density** (higher density = more potential clients)
3. **Population size** (larger suburbs have more searches)
4. **Current MD Home Care coverage** (only create pages for areas actually served)
5. **Competition level** (fewer competing providers = easier to rank)

### High-Priority Sydney Suburbs

Western Sydney (high NDIS density):
- Parramatta, Blacktown, Liverpool, Penrith, Campbelltown

South West Sydney:
- Fairfield, Bankstown, Canterbury

North Shore / Northern:
- Hornsby, Ryde, Chatswood

South / South East:
- Sutherland, Hurstville, Kogarah

### High-Priority Melbourne Suburbs

South East (high NDIS density):
- Dandenong, Casey, Frankston

North West:
- Hume, Brimbank

East:
- Whitehorse, Monash

West (fast growing):
- Wyndham, Melton

### Location Page Creation Rules

- Only create location pages for suburbs MD Home Care actually serves
- Each location page must have unique local content (not just find-and-replace suburb names)
- Reference local landmarks, hospitals, transport hubs
- Mention neighbouring suburbs covered
- Link back to the parent service page
- Do not create location pages for suburbs with very low search volume (check GSC first)

---

## Usage

**Determine content type for a keyword:**
```
/intent-strategy "SIL accommodation western sydney"
```

**Check for cannibalization:**
```
/intent-strategy --cannibal "ndis provider parramatta"
```

**Get location expansion recommendations:**
```
/intent-strategy --locations "support-coordination"
```

**Full intent audit across all content:**
```
/intent-strategy --audit
```
