---
name: blog-article-writer
description: Complete blog article creation workflow with automatic OG image generation. Use for creating new blog articles - supports prime (research), plan, execute, validate, and generate-og-prompt subcommands. Automatically generates OG images using Gemini API if GEMINI_API_KEY is configured.
license: Apache-2.0
---

# Blog Article Writer

Complete workflow for creating blog articles on pawellipowczan.pl with automatic OG image generation.

## Quick Reference

### Available Subcommands

| Command | Purpose |
|---------|---------|
| `/blog-article-writer:prime` | Research and analyze source materials |
| `/blog-article-writer:plan` | Create detailed article plan |
| `/blog-article-writer:execute` | Write article following approved plan |
| `/blog-article-writer:validate` | Validate article + generate OG image + update sitemap |
| `/blog-article-writer:generate-og-prompt` | Generate Gemini API prompt for OG image |

### Workflow Overview

```text
1. /blog-article-writer:prime
   ↓ (Research source materials, analyze style)

2. /blog-article-writer:plan
   ↓ (Create detailed implementation plan)

3. USER APPROVAL of plan
   ↓

4. /blog-article-writer:execute
   ↓ (Write article using portfolio-copywriting skill)

5. /blog-article-writer:validate (invoke after execute)
   ↓ (Validate quality, generate OG image, update sitemap)

6. Done - Article ready for commit
```

## Prerequisites

- Source materials in `docs/blog/`
- GEMINI_API_KEY in `.env` file (for OG image generation)
- `scripts/generate-image.js` available
- Dev server available (`npm run dev`)

## File Locations

| Artifact | Path |
|----------|------|
| Prime Context | `.claude/agents/context/blog-prime-{topic}.md` |
| Plans | `.claude/agents/plans/blog-{slug}.md` |
| Articles | `src/content/blog/{slug}.md` |
| Validation Reports | `.claude/agents/reports/validation-blog-{slug}.md` |
| OG Images | `public/images/og-{slug}.webp` |
| OG Prompts | `.claude/agents/prompts/og-{slug}-prompt.txt` |

## Critical Requirements

### Code Blocks
- ALL code blocks MUST have language tag
- Use `text` if no specific language applies
- Validation will fail if blocks lack tags

### Language
- Polish + natural English technical terms
- NEVER polonize: "komendyfikacja" → use "commandification" or describe
- Keep English: React, API, hooks, deployment, skills

### Style
- Pawel's voice: direct, practical, personal
- Short paragraphs (2-4 sentences)
- Bold key concepts on first mention
- First-person perspective

### FAQ Section (Required)
- 4-6 questions optimized for LLM discovery
- Natural Polish questions (10-25 words each)
- Snippet-style answers (2-4 sentences)
- Use `<details open>` accordion format
- See `docs/blog/FAQ_TEMPLATE.md` for structure

### OG Images
- NO TEXT (abstract visual design only)
- Uses portfolio design tokens (#00ff9d, #00b8ff, #0a0e1a, #151b2b)
- Generated via `scripts/generate-image.js` + Gemini API
- Auto-converted to WebP

## Subcommand Details

### /blog-article-writer:prime

**Purpose:** Research and analyze source materials before writing.

**Steps:**
1. Check `docs/blog/` for source materials
2. Read 2-3 recent articles from `src/content/blog/`
3. Review portfolio-copywriting skill guidelines
4. Extract key topics and concepts
5. Create prime artifact: `.claude/agents/context/blog-prime-{topic}.md`

**Output:** Prime artifact with comprehensive context

---

### /blog-article-writer:plan

**Purpose:** Create detailed implementation plan.

**Prerequisites:** Prime completed

**Steps:**
1. Load prime context
2. Determine next blog ID (grep existing IDs)
3. Design frontmatter (title, excerpt, slug, tags)
4. Plan article structure (H2 sections, word counts)
5. Plan FAQ questions (4-6)
6. Create plan artifact: `.claude/agents/plans/blog-{slug}.md`

**Output:** Complete plan ready for user approval

---

### /blog-article-writer:execute

**Purpose:** Write complete blog article following approved plan.

**Prerequisites:** Plan approved by user

**Steps:**
1. Load plan from `.claude/agents/plans/blog-{slug}.md`
2. Check for user feedback in plan
3. Use `portfolio-copywriting` skill to write article
4. Save to `src/content/blog/{slug}.md`
5. Notify user to run validate

**Output:** Complete article markdown file

---

### /blog-article-writer:validate

**Purpose:** Validate article and generate OG image.

**Prerequisites:** Article exists in `src/content/blog/`

**Steps:**

**Level 1: File Structure**
- Article file exists
- Frontmatter valid YAML
- All required fields present
- Blog ID unique

**Level 2: Content Quality**
- Code blocks have language tags
- No polonized terms
- FAQ section present
- CTA section present

**Level 3: Generate OG Image**

```bash
# 1. Generate prompt (internally)
# Uses article metadata + design tokens

# 2. Call generate-image.js
node scripts/generate-image.js "{PROMPT}" \
  --filename og-{slug} \
  --output public/images \
  --model gemini-3-pro-image-preview

# 3. Convert to WebP
node scripts/convert-to-webp.js public/images/og-{slug}.png

# 4. Remove PNG (keep only WebP)
```

**Level 4: Update Sitemap**
```bash
node scripts/update-sitemap.js
```

**Level 5: Create Validation Report**
- Save to `.claude/agents/reports/validation-blog-{slug}.md`

**Output:** Validation report + OG image generated

---

### /blog-article-writer:generate-og-prompt

**Purpose:** Generate Gemini API prompt for OG image.

**Input:** Article slug

**Steps:**
1. Read article frontmatter from `src/content/blog/{slug}.md`
2. Load design tokens from `.claude/reference/design/design-tokens.json`
3. Build Gemini-optimized prompt
4. Save to `.claude/agents/prompts/og-{slug}-prompt.txt`
5. Display prompt and usage instructions

**Prompt Template:**
```text
Create an abstract Open Graph image (1200x630px aspect ratio) for a blog article about [{category}]:

**Article Context:**
- Title: {title}
- Topic: {category}

**Visual Design Requirements:**

Background:
- Deep dark gradient from #0a0e1a (bottom) to #151b2b (top)

Primary Visual Elements (bright green #00ff9d):
- Abstract geometric shapes suggesting code/technology
- Neural network node patterns
- Circuit board pathways
- Floating hexagons

Secondary Visual Elements (cyan #00b8ff):
- Complementary geometric shapes
- Terminal window outlines (no text)
- Data flow visualization

**CRITICAL CONSTRAINTS:**
- ABSOLUTELY NO TEXT, LETTERS, NUMBERS, WORDS
- Pure abstract visual art only
- Professional enough for LinkedIn/Twitter previews

**Aspect Ratio:** 1200x630 pixels
```

## Integration with Scripts

### generate-image.js

Located at: `scripts/generate-image.js`

**Usage:**
```bash
node scripts/generate-image.js "prompt text" \
  --filename og-slug-name \
  --output public/images \
  --model gemini-3-pro-image-preview
```

**Requirements:**
- GEMINI_API_KEY in `.env`
- Default model: gemini-3-pro-image-preview

### convert-to-webp.js

Located at: `scripts/convert-to-webp.js`

**Usage:**
```bash
node scripts/convert-to-webp.js public/images/og-slug.png
```

### update-sitemap.js

Located at: `scripts/update-sitemap.js`

**Usage:**
```bash
node scripts/update-sitemap.js
```

## Error Handling

### Missing GEMINI_API_KEY

If API key not configured:
1. Skip automatic OG generation
2. Generate prompt and save to file
3. Notify user to generate manually or add API key

### Image Generation Failure

If Gemini API fails:
1. Log error details
2. Save prompt for manual retry
3. Continue with other validation steps
4. Mark OG image as pending in report

### Article Validation Failure

If validation finds issues:
1. List all failures
2. DO NOT proceed with OG generation
3. Wait for user fixes
4. Re-run validation after fixes

## See Also

- **Portfolio Copywriting:** `.claude/skills/portfolio-copywriting/SKILL.md`
- **Design Tokens:** `.claude/reference/design/design-tokens.json`
- **FAQ Guidelines:** `docs/blog/FAQ_TEMPLATE.md`
- **Article Examples:** `src/content/blog/`

---

**Last Updated:** 2026-01-26
**Status:** Active
