---
name: blog
description: Creates SEO+AEO optimized blog posts for MD Home Care. Handles informational NDIS/aged care content, provider comparisons, template posts, and guides with YMYL compliance and E-E-A-T standards.
---

# Blog Creator for MD Home Care

Creates high-quality blog posts optimized for both traditional search and AI answer engines. All content must meet YMYL standards for aged care and disability services.

## CRITICAL RULES

- **NO EM DASHES.** Use commas, full stops, semicolons, or restructure.
- **NO EMOJIS** in blog content. Ever.
- **NO "Updated Month Year" callout lines.** Use `updatedAt` frontmatter only.
- **NO manufactured expertise.** Do not invent statistics, case studies, or credentials.
- **Cite sources** for all NDIS/aged care stats and regulatory claims.
- **H2 headings: max ~35 characters** (for TOC sidebar display).
- **Clean minimal styling.** No heavy UI components. Text-focused content.

---

## Step 1: Cannibalization Check (MANDATORY)

**STOP. Before creating any new content, check if existing pages already rank for the target keyword.**

```bash
cd ~/Projects/mdhomecarebuild
python3 src/scripts/advanced_gsc_analyzer.py --keywords "[TARGET_KEYWORD]"
```

**If pages ARE found ranking:** Do NOT create a new post. Update the existing top-ranking page instead. Run a full page analysis:
```bash
python3 src/scripts/advanced_gsc_analyzer.py --page "/blog/[existing-slug]"
```

**If NO pages are found ranking:** Proceed to Step 2.

**Also check for blog vs service page conflicts.** If a service page already ranks for a keyword, a blog post will cannibalize it. Blog posts should target informational intent, not transactional intent. See the intent-strategy skill for guidance.

---

## Step 2: Web Research

**MANDATORY before writing or updating any post.** Use web search to gather current information.

**Run these 3 searches:**

1. **Current landscape:** `[PRIMARY_KEYWORD] Australia 2026` - latest developments, policy changes, regulatory updates
2. **User intent:** `[PRIMARY_KEYWORD] reddit` or `[PRIMARY_KEYWORD] forum` - what real people are asking, common frustrations, gaps in existing content
3. **Competitor content:** `[PRIMARY_KEYWORD] guide` or `[PRIMARY_KEYWORD] explained` - what's currently ranking, what they cover, what they miss

**For NDIS/aged care topics, also search:**
- `[TOPIC] NDIS price guide 2024-25` for current pricing
- `[TOPIC] NDIS quality and safeguards commission` for regulatory context
- `site:ndis.gov.au [TOPIC]` for official NDIS guidance

**Extract from research:**
- Key facts, stats, and figures (with sources)
- Common questions people ask (for FAQ section)
- Gaps in existing content you can fill
- Current regulatory requirements or recent changes
- What competitors cover that you should match or beat

**Do not skip this step.** YMYL content with outdated or inaccurate information will be penalized by Google.

---

## Step 3: Choose Post Format

### Standard Guide Post
For informational queries: "what is SIL", "NDIS funding guide", "how to apply for home care packages"

### Template/Download Post
For template queries: "NDIS incident report template", "progress notes template", "care plan template". These rank well and drive high-intent traffic.

**Template post structure:**
- Explain what the template is and why it matters
- Provide the template content inline (not just a download)
- Include a filled example
- FAQ about using the template
- CTA to MD Home Care services

### Top X Providers Comparison Post
For comparison queries: "best NDIS providers Sydney", "top SIL providers Melbourne". These generate immediate AEO traffic because AI assistants love structured comparison content.

**Comparison post structure:**
- Brief intro (who this list helps)
- Numbered provider entries with consistent criteria
- Comparison table summarizing all providers
- "How we chose this list" transparency section
- MD Home Care naturally included (not forced to #1)

### Explainer Post
For concept queries: "NDIS core supports explained", "difference between HCP levels"

---

## Step 4: Blog Structure

### Frontmatter

```yaml
---
title: "[Primary Keyword]: [Benefit or Qualifier]"
description: "Hook + keywords + benefit (under 160 chars)"
pubDate: YYYY-MM-DD
updatedAt: YYYY-MM-DD
author: "Camila"
tags: []
image: "/assets/carer.webp"
---
```

### Required Sections

1. **Key Points** (bullet summary at top, 4-6 bullets)
2. **Definition/Overview** (What is [topic]?)
3. **Main content sections** (H2s: max ~35 chars each)
4. **Tables** for any comparisons or structured data
5. **FAQ section** (H3 questions, 5-8 questions)
6. **Key Resources** (outbound links to authoritative sources)
7. **CTA** to relevant MD Home Care service page

### Formatting Rules

- Use `---` dividers between major sections
- Use `>` blockquotes for important callouts (sparingly)
- Tables with left-aligned columns
- Internal links to related blog posts and service pages
- **No emojis**
- **Minimum 2000 words** for standard posts, 1500 for template posts
- Use `<br>` sparingly. Prefer paragraph breaks.

---

## Step 5: Content Quality Standards (YMYL)

### Accuracy Requirements
- All NDIS pricing must reference the current NDIS Price Guide
- Regulatory information must be current and verifiable
- Statistics must have sources cited (inline or in resources section)
- Do not state capabilities MD Home Care does not have

### Outbound Linking Rules
- Link to authoritative government sources: NDIS website, Aged Care Quality and Safety Commission, myagedcare.gov.au
- Link to relevant legislation or guidelines when citing regulations
- 2-4 outbound links per post to authoritative sources
- Do not link to direct competitors in informational posts
- In comparison posts, link to each provider's official site

### Internal Linking Rules
- Link to the most relevant MD Home Care service page (1-2 links)
- Link to 2-3 related blog posts
- Use descriptive anchor text (not "click here")
- Do not over-link. 4-6 internal links per post maximum.

### DaisyUI Component Guidelines
- **Allowed:** Simple tables, blockquotes, horizontal rules
- **Use sparingly:** Accordion/collapse for FAQ if post is very long
- **Avoid:** Cards, heroes, carousels, badges, modals, complex layouts
- Blog posts should feel like articles, not landing pages

---

## Step 6: Post-Specific Guidelines

### Template/Download Posts
- Include the full template as formatted markdown (users should be able to copy it)
- Provide a filled-in example showing how to use it
- Explain each section of the template
- Link to NDIS or aged care guidelines the template relates to
- These posts often rank for high-intent keywords. Optimize the title for "[template name] template" format.

### Top X Provider Comparison Posts
- Research each provider via WebSearch before writing
- Use consistent evaluation criteria (services, locations, pricing transparency, specialties)
- Include MD Home Care naturally in the list (positioned honestly)
- Add a comparison summary table
- Be fair and accurate about all providers
- Disclose that MD Home Care is the publisher: "Disclosure: This post is published by MD Home Care."

### Location-Specific Blog Posts
- Target informational queries about services in specific areas
- Do not duplicate content from location service pages
- Focus on guides, tips, and local resources rather than service promotion

---

## Step 7: Save File

```
~/Projects/mdhomecarebuild/src/content/blog/[slug].md
```

Slug format: `lowercase-hyphenated-keywords.md`

---

## Quality Checklist

- [ ] Cannibalization check completed (Step 1)
- [ ] Decided: create new OR update existing
- [ ] Web search research completed (3 searches minimum)
- [ ] Primary keyword in title
- [ ] H2s are max ~35 characters
- [ ] No emojis anywhere in content
- [ ] No em dashes anywhere in content
- [ ] No "Updated Month Year" callout lines
- [ ] Keyword not repeated >5 times (stuffing check)
- [ ] Tables properly formatted
- [ ] FAQ section with 5+ questions
- [ ] 2-4 outbound links to authoritative sources
- [ ] 4-6 internal links (service pages + related blogs)
- [ ] Sources cited for statistics and regulatory claims
- [ ] MD Home Care CTA at end linking to relevant service page
- [ ] updatedAt frontmatter set
- [ ] Minimum word count met (2000 standard, 1500 template)
- [ ] DaisyUI components minimal (article feel, not landing page)

---

## Usage

**Create a new blog post:**
```
/blog "what is supported independent living"
```

**Create a template post:**
```
/blog --template "ndis incident report template"
```

**Create a comparison post:**
```
/blog --comparison "best ndis providers sydney"
```

**Update an existing post:**
```
/blog --update /blog/ndis-funding-guide
```
