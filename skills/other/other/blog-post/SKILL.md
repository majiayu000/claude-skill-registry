---
name: blog-post
description: Create or update a blog post by researching the topic, drafting the article, humanizing text, refining structure and SEO, and validating it against repository conventions.
---

# Blog Post

End-to-end workflow for long-form blog content.

## 1. Gather Context

Read:

1. Root `AGENTS.md` and blog conventions (directory, frontmatter format, naming)
2. Existing posts in the blog directory for cross-link opportunities
3. If updating — read the existing post, note what needs to change

## 2. Research and Brief

Define before writing:

- **Audience**: developers, decision-makers, general public
- **Angle**: what makes this post unique
- **Primary keyword** and 2-3 secondary keywords
- **Outline**: H2 sections with what each covers
- **Key data points**: stats with sources
- **Cross-link targets**: existing posts to link to/from
- **Word count target**

Use `content-creation` skill (`content-tools-guide.md`) for research workflows and brief templates.

Present the brief to the user. Wait for approval before proceeding.

## 3. Draft

Write the post following the approved outline:

- Hook introduction — surprising stat, question, or pain point
- Short paragraphs (2-3 sentences), break up with lists, tables, blockquotes
- Minimum 3 internal links to existing posts
- 1-2 external authoritative sources
- Key takeaways bullet list
- Natural, value-first CTA
- Specify alt text and placement for visuals

## 4. Humanize

Apply `humanizer` skill to the draft:

1. Scan for AI writing patterns (see pattern catalog)
2. Rewrite problematic sections — remove AI-isms, add natural voice
3. Anti-AI audit — ask "What makes this obviously AI generated?", list remaining tells
4. Revise based on the audit
5. Verify the humanized text preserves accuracy and outline compliance

Do NOT skip this step.

## 5. SEO Optimization

Refine:

- Title tag: primary keyword, compelling, 50-60 characters
- Meta description: unique, includes keyword, 120-160 characters
- Heading hierarchy: logical H1 → H2 → H3, keywords in H2s naturally
- URL slug: short, descriptive, hyphenated
- First paragraph: contains primary keyword naturally
- Image alt text: descriptive, keyword where natural
- Internal links: minimum 3, descriptive anchor text
- Structured data: `BlogPosting` JSON-LD where applicable

## 6. Quality Review

Review the complete post against the original brief:

- [ ] All outline sections covered, angle maintained
- [ ] Facts, statistics, and claims are correct and cited
- [ ] Language and depth match the target audience
- [ ] Minimum 3 internal links present and relevant
- [ ] CTA is natural and value-first
- [ ] SEO elements optimized (title, meta, headings, keywords)
- [ ] No secrets, PII, or internal-only data
- [ ] Text sounds natural — no AI writing patterns remain
- [ ] Brand voice consistent with project tone

If issues found:

| Issue | Route to |
|---|---|
| Content gaps, accuracy, tone | Step 3 |
| AI-sounding text | Step 4 |
| SEO issues | Step 5 |
| Brief was wrong | Step 2 |

## 7. Publish

Set frontmatter status based on user intent:

- Publish now: status = published, date = today
- Schedule: status = draft, note target date
- Series: status = draft, add series metadata

Final checks:

- [ ] Frontmatter complete
- [ ] File in correct directory with correct naming
- [ ] No TODO or placeholder text remains
- [ ] Discovery assets updated (sitemap, llms.txt if maintained)

## 8. Report

Summarize:

- Title and file path
- Status (published / draft / scheduled)
- Target keyword and word count
- Review rounds and cross-links added
- Follow-ups (cover image, social media, etc.)

## Integration

- **Skills**: `content-creation` (content brief, tools, quality gates), `humanizer` (AI writing pattern removal — step 4)
- **Rules**: `humanize-content` (enforces humanizer pass on all public-facing text)
- **Follow-up**: `seo-review`, `pre-commit`, `create-pr`
