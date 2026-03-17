---
name: blog-writer
description: Professional blog writing agent for dev.to with SEO-optimized Markdown format. Use when writing technical blogs, tutorials, or experience sharing. Output includes frontmatter with title, tags, series, canonical URL, cover image, and SEO-optimized content.
license: MIT
metadata:
  author: nghi-danh-ai
  version: "1.0.0"
---

# ✍️ Dev.to Blog Writer Agent

This skill helps write professional blogs for the dev.to platform with SEO-optimized Markdown format, including complete frontmatter, optimized content structure, and best practices for technical writing.

## 🎯 When to Use

- Writing technical tutorial blogs
- Sharing programming experiences
- Reviewing tools/libraries/frameworks
- Writing article series
- Creating listicles (Top 10, Best practices, etc.)

## 📚 Rules

Detailed guidelines are in the `rules/` folder:

| Rule File | Description |
|---|---|
| [article-structure.md](rules/article-structure.md) | Frontmatter template, content structure, backlink strategy |
| [title-writing.md](rules/title-writing.md) | Title formulas and checklist |
| [tag-selection.md](rules/tag-selection.md) | Popular tags and selection strategy |
| [seo-best-practices.md](rules/seo-best-practices.md) | Keyword placement, content length, readability |
| [markdown-formatting.md](rules/markdown-formatting.md) | Code blocks, callouts, liquid tags |
| [publishing-checklist.md](rules/publishing-checklist.md) | Pre/post publish checklist + article templates |

## 🚀 Quick Commands

When using this agent, you can request:

1. **"Write a tutorial blog about [topic]"** → Uses Tutorial Template (see [publishing-checklist.md](rules/publishing-checklist.md))
2. **"Write a listicle [number] [noun]"** → Uses Listicle Template (see [publishing-checklist.md](rules/publishing-checklist.md))
3. **"Generate frontmatter for article about [topic]"** → Creates only frontmatter
4. **"Suggest tags for [topic] article"** → Suggests 4 appropriate tags
5. **"Optimize SEO for title [title]"** → Improves title for SEO

## 🔗 References

- [dev.to Editor Guide](https://dev.to/p/editor_guide)
- [dev.to API Documentation](https://developers.forem.com/api)
- [Markdown Guide](https://www.markdownguide.org/)

