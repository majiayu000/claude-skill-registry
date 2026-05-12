---
name: internal-link-builder
description: Strategic internal link building for WordPress sites. Analyzes all published content, maps topic relationships, identifies high-value linking opportunities, and presents a clear plan for approval before making any changes. Use when user says "build internal links", "fix orphaned pages", "improve internal linking", "topic clusters", "pillar pages", or "improve site interlinking for SEO".
license: MIT
metadata:
  author: Respira for WordPress
  author_url: https://respira.press
  version: 1.0.0
  mcp-server: respira-wordpress
  category: seo
---

# Internal Link Builder

Strategic internal link building for WordPress sites. Analyzes all published content, maps topic relationships, identifies high-value linking opportunities between pages, and presents a clear plan for approval before making any changes. Use this skill whenever someone mentions internal links, link building, content interlinking, orphaned pages that need links, topic clusters, pillar pages, or wants to improve their site's internal link structure for SEO.

## What This Skill Does

Internal links are one of the highest-leverage on-page SEO tactics — they distribute page authority, help search engines understand site structure, and guide visitors to related content. Most WordPress sites under-link dramatically, leaving value on the table.

This skill reads every published page and post, builds a content relationship map, and finds natural opportunities to connect related content through contextual links. It always shows you the full plan before touching anything.

**Finds:**
- Orphaned content (pages/posts with zero or few inbound internal links)
- Hub pages that should link to related sub-pages but don't
- Blog posts that reference topics covered by other pages without linking
- Pillar/cluster opportunities (topically related content that should be interlinked)
- Pages with high authority potential that aren't distributing link equity
- Over-linked pages (too many outbound links diluting value)
- Missing contextual links (mentions of topics without corresponding links)

**Recommends:**
- Specific source page → target page link pairs
- Suggested anchor text (natural, descriptive, not keyword-stuffed)
- Link placement context (which paragraph/section the link belongs in)
- Priority ranking (high/medium/low impact)
- Reasoning for each recommendation (why this link makes sense)

## Requirements

- Respira for WordPress plugin installed and connected
- MCP connection active (desktop or WebMCP)
- Read access to scan site content
- Write access to create duplicates (only if user approves changes)

## Trigger Phrase

- "build internal links"

## Alternative Triggers

- "improve internal linking"
- "find internal link opportunities"
- "interlink my content"
- "fix orphaned pages"
- "create topic clusters"
- "link my pages together"
- "internal link audit"

## Execution Workflow

### Phase 1: Content Inventory & Mapping

1. Verify Respira + MCP connection via `wordpress_get_site_context`. If unavailable, stop and show setup guidance.
2. Fetch all published content:
   - `wordpress_list_pages` — get all pages
   - `wordpress_list_posts` — get all posts
3. For each content item, load full content:
   - `wordpress_read_page` or `wordpress_read_post`
   - Extract: title, URL/slug, headings, main topics, existing internal links, word count
4. Build a **content map** — a structured index of:
   - Each page/post's primary topic and subtopics
   - Keywords and phrases each piece targets
   - Existing internal links (source → target pairs)
   - Inbound link count per page
   - Content type (pillar page, blog post, product page, landing page, etc.)

### Phase 2: Opportunity Analysis

Analyze the content map to find linking opportunities. For each potential link, evaluate:

1. **Topical relevance** — Does the source content naturally relate to the target? Only recommend links where the connection is genuinely useful to a reader. A link should feel like a helpful "read more about this" moment, not a forced SEO play.

2. **Context fit** — Is there a natural place in the source content where the link fits? Look for:
   - Mentions of the target page's topic without an existing link
   - Paragraphs that discuss related concepts
   - Lists or resource sections where the target would be a natural addition
   - Introductions or conclusions that reference broader topics

3. **Link equity value** — Consider:
   - Orphaned pages (0-1 inbound links) get priority as targets
   - High-traffic/high-authority pages are valuable as sources
   - Deep pages that are hard to reach from navigation benefit most
   - Don't over-link any single page (diminishing returns after ~3-5 new links per page)

4. **Anchor text quality** — Suggest anchor text that:
   - Reads naturally in context
   - Describes what the reader will find (not "click here")
   - Uses relevant keywords without being spammy
   - Varies across different links to the same target

### Phase 3: Present the Plan

Present the linking plan as a clear, scannable report. Group recommendations by priority:

```
## Internal Link Building Plan

### Site Overview
- Total pages/posts scanned: X
- Existing internal links found: X
- Orphaned content (0-1 inbound links): X
- New links recommended: X

### High Priority (orphaned pages & pillar connections)

1. **[Source Page Title]** → **[Target Page Title]**
   - Why: [Brief reasoning — e.g., "Source discusses WordPress security but doesn't link to your dedicated security guide"]
   - Anchor text: "[suggested anchor text]"
   - Placement: [Where in the source content — e.g., "In the paragraph about plugin vulnerabilities (under H2 'Keeping Your Site Safe')"]

2. ...

### Medium Priority (topical cluster links)
...

### Low Priority (nice-to-have contextual links)
...

### Summary
- High priority: X links (strongly recommended)
- Medium priority: X links (good for SEO)
- Low priority: X links (optional enhancement)
```

Then ask:

> Here's the internal linking plan. Would you like me to:
> 1. Apply all recommendations (creates duplicates for review)
> 2. Apply only high-priority links
> 3. Let you pick specific links to apply
> 4. Just keep this as a reference — no changes

Wait for explicit confirmation before proceeding.

### Phase 4: Apply Links (Only If Approved)

1. For each page that needs link additions:
   - Create a duplicate via `wordpress_create_page_duplicate` or `wordpress_create_post_duplicate`
2. On the duplicate, add the approved links:
   - Insert `<a href="...">anchor text</a>` at the recommended placement points
   - Respect the page builder format (Gutenberg blocks, Divi shortcodes, Elementor data, etc.)
   - Use `wordpress_extract_builder_content` to understand the content structure
   - Use `wordpress_inject_builder_content` or `wordpress_update_page` / `wordpress_update_post` to apply changes
3. After all duplicates are created, provide a summary:
   - Number of duplicates created
   - Total links added
   - List of pages modified with links to review them in WordPress admin

## Link Quality Rules

These rules prevent the skill from making harmful or spammy recommendations:

- **Relevance first** — Never recommend a link purely for SEO mechanics. Every link must be genuinely useful to a human reader navigating between the two pages.
- **No self-links** — Don't link a page to itself.
- **No duplicate links** — Don't recommend a link that already exists on the source page.
- **Respect existing links** — If a paragraph already has 2+ links, don't add more to it. Link density matters for readability.
- **Natural anchor text** — No exact-match keyword stuffing. Anchor text should read as part of the sentence.
- **Builder-aware** — When inserting links, preserve the page builder's content format. Don't break Divi shortcodes, Elementor JSON, or Gutenberg block markup.
- **Conservative by default** — When in doubt about a link's relevance, leave it out. It's better to recommend 10 great links than 30 mediocre ones.

## Output Format

Always include:

1. **Site content summary** (pages/posts scanned, existing link density)
2. **Content map highlights** (topic clusters identified, orphaned content found)
3. **Prioritized linking plan** (high/medium/low with reasoning for each)
4. **Clear confirmation prompt** — never proceed without approval
5. **Impact estimate** (which orphaned pages get rescued, which clusters get strengthened)

If changes are applied, also include:

6. **Change summary** (duplicates created, links added)
7. **Review instructions** (where to find and review duplicates in WordPress)

## Safety Model

- Read-only analysis first — full content scan before any changes
- Explicit user confirmation before creating any duplicates
- Duplicate-first only — never modifies live/published content
- Never auto-publish duplicates
- Provides rollback guidance (delete duplicates if not wanted)
- Preserves all existing content and links — only adds, never removes

## Honest Disclaimer

This skill identifies internal linking opportunities and creates optimized duplicates for review.

It cannot:
- Guarantee ranking improvements
- Fix external/backlink profile
- Replace a proper content strategy
- Publish changes without your review

It can:
- Find genuine content relationships you've missed
- Rescue orphaned pages from obscurity
- Strengthen topical clusters with contextual links
- Save hours of manual content auditing

## Tooling

**Core WordPress tools**
- `wordpress_get_site_context`
- `wordpress_list_pages`
- `wordpress_list_posts`
- `wordpress_read_page`
- `wordpress_read_post`
- `wordpress_extract_builder_content`
- `wordpress_inject_builder_content`
- `wordpress_create_page_duplicate`
- `wordpress_create_post_duplicate`
- `wordpress_update_page`
- `wordpress_update_post`

## Telemetry

After run completion, send fire-and-forget usage tracking to:

- `POST https://www.respira.press/api/skills/track-usage`

Include:
- `skill_slug = internal-link-builder`
- site/version context
- duration and success
- pages scanned, links recommended, links applied counts
- tools used

Never block user flow on telemetry failure.

## Related Skills

- SEO & AEO Amplifier (complements this — run SEO audit first, then build links)
- WordPress Site DNA (understand site structure before linking)
- Technical Debt Audit

---

Built by Respira Team
https://respira.press/skills/internal-link-builder
