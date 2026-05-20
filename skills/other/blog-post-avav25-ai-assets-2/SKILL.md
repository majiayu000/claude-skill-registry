---
name: blog-post
description: Blog post workflow — research topic, create content brief, write article, SEO optimize, quality review with feedback loop. Orchestrates product-manager, content-writer, and seo-engineer roles for public blog content creation and updates.
context: fork
argument-hint: [topic or content brief]
---

# Blog Post

End-to-end workflow for creating and updating blog posts. Orchestrates multi-role collaboration: `Agent(product-manager)` (research, brief, quality gate), `Agent(content-writer)` (authoring), `Agent(seo-engineer)` (optimization). Includes a review loop until the post meets quality standards.

## 1. Define Scope

Ask the user (or extract from context):

- **Action**: Create new post / update existing / create series
- **Topic**: Subject, angle, or user-provided idea
- **Target audience**: Who reads this? (developers, decision-makers, general public)
- **Goal**: Educate, announce, promote, thought leadership, SEO traffic
- **Constraints**: Deadline, word count, related posts, brand guidelines

If updating an existing post — read it first, note what needs to change.

## 2. Research and Content Brief

**Apply `Agent(product-manager)`.**

### 2a. Topic Research

Conduct research before writing:

1. **Web search** — find 3-5 top-ranking articles on the topic. Note their angle, depth, and gaps
2. **Competitive analysis** — what do competitors cover? What's missing in the market?
3. **Data and statistics** — find recent, citable data points (studies, surveys, benchmarks)
4. **Keyword research** — identify primary keyword, 2-3 secondary keywords, search intent (informational / commercial / transactional)
5. **Existing content audit** — scan the project's blog directory for related posts. Identify cross-link opportunities

### 2b. Content Brief

Produce a brief using the **Blog Content Brief Template** from `content-creation` skill (`content-tools-guide.md` → Content Research Workflows section). The brief must include at minimum:

- **Working title and angle** (what makes this post unique)
- **Target audience and search intent** (primary + secondary keywords)
- **Outline** (H2 sections with what each covers)
- **Key data points** (stats with sources from research)
- **Cross-link opportunities** (existing posts to link to/from)
- **Visual needs** (cover image, diagrams, screenshots)
- **Word count target**

Present the brief to the user. **Wait for user approval before proceeding.** Adjust outline based on feedback.

## 3. Write Draft

**Apply `Agent(content-writer)`.** Use `content-creation` skill — Blog Post pattern from `page-content-patterns.md`.

### 3a. Create the Post File

1. **Read project's `CLAUDE.md`** — get blog file conventions (directory, frontmatter format, naming)
2. **Create the file** with correct frontmatter as defined in the project's conventions
3. If no project conventions exist — use `kebab-case.md` naming, ask the user about frontmatter format

### 3b. Write Content

Follow the approved outline. For each section:

- **Hook introduction** — surprising stat, question, or pain point in the first paragraph
- **Structured body** — short paragraphs (2-3 sentences), break up with lists, tables, code blocks, blockquotes
- **Internal links** — minimum 3 links to existing blog posts or pages (from brief's cross-link list)
- **External links** — 1-2 authoritative sources (cite data points from research)
- **Key takeaways** — bullet list summarizing the post
- **CTA** — natural, value-first call to action related to the topic

### 3c. Visual Direction

For each visual need identified in the brief:

- Specify alt text (descriptive, includes keyword where natural)
- Note image placement relative to content
- If cover image needed — describe desired style, mood, composition

## 4. Humanize Content

**Apply `@humanizer` skill.** This step is mandatory for all blog content.

1. **Scan the draft** for AI writing patterns (see `@humanizer` pattern catalog)
2. **Rewrite** problematic sections — remove AI-isms, add natural voice
3. **Anti-AI audit** — ask "What makes this obviously AI generated?", list remaining tells, revise
4. **Verify** the humanized text preserves accuracy, maintains the approved outline, and sounds natural when read aloud

Do NOT skip this step. The `humanize-content` rule enforces this for all public-facing text.

## 5. SEO Optimization

**Apply `Agent(seo-engineer)`.**

Run an SEO pass on the draft:

### 4a. On-Page SEO

| Element | Check |
|---|---|
| Title tag | Primary keyword, compelling, 50-60 characters |
| Meta description | Unique, includes keyword, 120-160 characters |
| H1 | Matches title, one per page |
| Heading hierarchy | Logical H1→H2→H3, secondary keywords in H2s naturally |
| URL / slug | Short, descriptive, hyphenated, includes keyword |
| First paragraph | Contains primary keyword naturally |
| Image alt text | Descriptive, keyword where natural |

### 4b. Internal Link Audit

- [ ] Minimum 3 internal links with descriptive anchor text
- [ ] Check all internal links are valid (no broken references)
- [ ] Anchor text is descriptive (not "click here" or "read more")
- [ ] Links are contextually relevant (not forced)

### 4c. Structured Data

- Add `BlogPosting` JSON-LD schema (or verify the framework handles it automatically)
- Verify: `headline`, `author`, `datePublished`, `description`, `image`

### 4d. Discovery Assets

- [ ] New post URL will be included in sitemap (verify sitemap config)
- [ ] `robots.txt` does not block the blog path
- [ ] Update `llms.txt` if the project maintains one — add the new post entry
- [ ] Verify canonical URL is correct

## 6. Quality Review

**Apply `Agent(product-manager)`.**

Review the complete post against the original brief:

### 6a. Review Checklist

<review_checklist>
- [ ] **Brief compliance** — all outline sections covered, angle maintained
- [ ] **Accuracy** — facts, statistics, and claims are correct and cited
- [ ] **Audience fit** — language and depth match the target audience
- [ ] **Completeness** — no sections feel rushed or incomplete
- [ ] **Cross-links** — minimum 3 internal links present and relevant
- [ ] **CTA** — natural, value-first, not aggressive
- [ ] **Visual direction** — cover image and inline visuals specified
- [ ] **SEO** — title, meta, headings, keywords all optimized
- [ ] **No secrets or PII** — no internal data, credentials, or personal info
- [ ] **Brand voice** — consistent with project tone and terminology
</review_checklist>

### 6b. Decision Gate

| Result | Action |
|---|---|
| All checks pass | Proceed to Step 7 |
| Content issues (gaps, accuracy, tone) | Route to **Step 3** with specific feedback |
| AI-sounding text detected | Route to **Step 4** with specific patterns to fix |
| SEO issues (meta, links, structured data) | Route to **Step 5** with specific feedback |
| Brief was wrong (topic shifted, audience changed) | Route to **Step 2** to revise brief |

**Present review findings to the user.** If issues found — list them explicitly with the routing decision. Repeat the loop until the review passes.

## 7. Publish

### 7a. Set Publish Status

Based on user intent:

| Intent | Action |
|---|---|
| Publish now | Set frontmatter status to published, set publish date to today |
| Schedule for later | Set status to draft, note the target publish date |
| Part of a series | Set status to draft, add series metadata, link to previous/next parts |

### 7b. Final File Checks

- [ ] Frontmatter is complete (all required fields populated)
- [ ] File is in the correct directory
- [ ] File name follows project conventions
- [ ] No TODO or placeholder text remains in the content
- [ ] All images referenced exist or have clear generation instructions

### 7c. Discovery Assets Update

- [ ] `llms.txt` updated (if maintained)
- [ ] Sitemap will pick up new file automatically (verify config)
- [ ] No `noindex` on the new page

## 8. Summary

```
## Blog Post Summary

- **Title**: [post title]
- **File**: [file path]
- **Status**: [published / draft / scheduled for DATE]
- **Topic**: [one-sentence summary]
- **Target keyword**: [primary keyword]
- **Word count**: [count]
- **Roles applied**: Agent(product-manager) → Agent(content-writer) → @humanizer → Agent(seo-engineer) → Agent(product-manager)
- **Review rounds**: [number of iterations]
- **Cross-links added**: [count — list of linked posts]
- **Discovery assets**: [llms.txt updated: yes/no, sitemap: auto/manual]
- **Follow-ups**: [if any — e.g., create cover image, schedule social media]
```

## Content Series Pattern

When creating a multi-part series:

1. **Plan all parts upfront** — titles, topics, publish order in the content brief (Step 2)
2. **Cross-link between parts** — each post links to previous and next in series
3. **Teaser for upcoming parts** — end each post with a preview: "In Part 2, we'll cover [topic]"
4. **Draft all parts** before publishing the first — ensures consistency and cross-links work
5. **Stagger publishing** — space parts 3-7 days apart for engagement
6. **On publish day** — update previous part's teaser to a real link, remove any "(coming soon)" notes

## Integration

- **Roles**: `Agent(product-manager)` (research, brief, review), `Agent(content-writer)` (authoring), `Agent(seo-engineer)` (optimization)
- **Skills**: `content-creation` skill (Blog Post pattern, AI generation tools, content brief template), `@humanizer` (AI writing pattern removal — step 4)
- **Rules**: `humanize-content` (auto-enforces humanizer pass on all public-facing text)
- **Follow-up**: `/seo-review` (deep SEO audit if needed), `/pre-commit`, `/create-pr`
- **Related**: `/docs` (technical documentation), `/ui-ux-design` (visual design for blog assets)
