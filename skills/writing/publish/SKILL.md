---
name: publish
description: |
  Content-publishing umbrella covering the blog pipeline from blueprint to
  upload: post outlining, pre-publication validation, SEO optimization, bulk
  find/replace and frontmatter editing, link auditing, image auditing,
  taxonomy management, and WordPress upload. Use for "outline post",
  "article outline", "pre-publish check", "frontmatter validation", "check
  SEO", "keyword analysis", "meta description", "batch edit posts", "bulk
  frontmatter update", "mass edit", "audit links", "broken links", "audit
  images", "alt text check", "audit taxonomy", "fix tags", "merge
  categories", "upload to wordpress", "create wordpress draft", "post to
  wordpress", "edit wordpress post", "create wp categories", "auto-create
  categories", "search wp media", or "find existing wordpress image".
user-invocable: false
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebFetch
routing:
  triggers:
    - "outline post"
    - "blog structure"
    - "article outline"
    - "pre-publish check"
    - "Hugo validation"
    - "front matter check"
    - "frontmatter validation"
    - "check SEO"
    - "optimize SEO"
    - "keyword analysis"
    - "meta description"
    - "batch edit posts"
    - "bulk frontmatter update"
    - "find replace across files"
    - "mass edit"
    - "audit links"
    - "find broken links"
    - "broken links"
    - "dead links"
    - "audit images"
    - "image accessibility"
    - "alt text check"
    - "audit taxonomy"
    - "fix tags"
    - "merge categories"
    - "tag cleanup"
    - "upload to wordpress"
    - "create wordpress draft"
    - "wordpress draft"
    - "upload article"
    - "post to wordpress"
    - "edit wordpress post"
    - "update wordpress post"
    - "wordpress media"
    - "create wp categories"
    - "auto-create categories"
    - "search wp media"
    - "search wordpress media"
    - "find existing wordpress image"
  not_for: "writing article prose (use voice-writer), live rendering verification (use wordpress-live-validation)"
  category: content-publishing
  complexity: medium
  pairs_with:
    - content-calendar
    - wordpress-live-validation
    - html-artifact
---

# Publish Skill

Umbrella skill for the content-publishing pipeline. Routes to the correct reference based on the intent requested: outline a post, run a pre-publication check, optimize SEO, bulk-edit posts, audit links, audit images, manage taxonomy, or upload to WordPress.

## Routing

Detect the user's intent and load the appropriate reference file:

| Intent | Trigger phrases | Reference |
|--------|----------------|-----------|
| **Outline** | "outline post", "blog structure", "content blueprint", "article outline", "content structure" | `${CLAUDE_SKILL_DIR}/references/outline.md` |
| **Pre-publish** | "pre-publish check", "Hugo validation", "front matter check", "publication check", "frontmatter validation" | `${CLAUDE_SKILL_DIR}/references/pre-publish.md` |
| **SEO** | "check SEO", "optimize SEO", "keyword analysis", "meta description", "keyword optimization" | `${CLAUDE_SKILL_DIR}/references/seo.md` |
| **Batch-edit** | "batch edit posts", "bulk frontmatter update", "find replace across files", "mass edit", "bulk update" | `${CLAUDE_SKILL_DIR}/references/batch-edit.md` |
| **Link-audit** | "audit links", "find broken links", "link health", "broken links", "dead links" | `${CLAUDE_SKILL_DIR}/references/link-audit.md` |
| **Image-audit** | "audit images", "check broken images", "image accessibility", "alt text check", "image optimization" | `${CLAUDE_SKILL_DIR}/references/image-audit.md` |
| **Taxonomy** | "audit taxonomy", "fix tags", "merge categories", "tag cleanup", "category management" | `${CLAUDE_SKILL_DIR}/references/taxonomy.md` |
| **WordPress-upload** | "upload to wordpress", "create wordpress draft", "post to wordpress", "wordpress draft", "upload article", "upload image to wordpress", "edit wordpress post", "update wordpress post", "wordpress media", "create wp categories", "auto-create categories", "create missing categories", "search wp media", "search wordpress media", "search media library", "find existing wordpress image", "find existing image", "reuse existing media" | `${CLAUDE_SKILL_DIR}/references/wordpress-upload.md` |

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| "outline post", "blog structure", "content blueprint", "article outline", "content structure" | `outline.md` | **Outline** |
| "pre-publish check", "Hugo validation", "front matter check", "publication check", "frontmatter validation" | `pre-publish.md` | **Pre-publish** |
| "check SEO", "optimize SEO", "keyword analysis", "meta description", "keyword optimization" | `seo.md` | **SEO** |
| "batch edit posts", "bulk frontmatter update", "find replace across files", "mass edit", "bulk update" | `batch-edit.md` | **Batch-edit** |
| "audit links", "find broken links", "link health", "broken links", "dead links" | `link-audit.md` | **Link-audit** |
| "audit images", "check broken images", "image accessibility", "alt text check", "image optimization" | `image-audit.md` | **Image-audit** |
| "audit taxonomy", "fix tags", "merge categories", "tag cleanup", "category management" | `taxonomy.md` | **Taxonomy** |
| "upload to wordpress", "create wordpress draft", "post to wordpress", "wordpress draft", "upload article", "upload image to wordpress", "edit wordpress post", "update wordpress post", "wordpress media", "create wp categories", "auto-create categories", "create missing categories", "search wp media", "search wordpress media", "search media library", "find existing wordpress image", "find existing image", "reuse existing media" | `wordpress-upload.md` | **WordPress-upload** |

## Instructions

1. Identify the user's publishing task from their message
2. Load the matching reference file from the table above
3. Follow the instructions in that reference file exactly

See also: `wordpress-live-validation` skill for the post-upload live-validation step (browser-based rendering verification after WordPress upload).
