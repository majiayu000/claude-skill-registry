---
name: writing-hugo-blog
description: "Create Hugo blog posts in Chinese. Triggers when user asks to write a blog post, create a draft article, or convert research into blog format. Follows a structured workflow: explore blog config, understand content formats, gather topic requirements, generate draft, and review writing quality."
---

# Writing Hugo Blog

Create Chinese blog posts for Hugo static sites with proper front matter, content structure, and AI labeling.

## References

**Hugo Documentation:**
- Configuration: https://gohugo.io/configuration/all/
- Content Formats: https://gohugo.io/content-management/formats/
- Front Matter: https://gohugo.io/content-management/front-matter/

**Writing Style:**
- `references/chinese-writing-style.md` - Detailed Chinese writing style guide (based on https://github.com/ruanyf/document-style-guide)

---

## Workflow

### Step 1: Explore Blog Configuration

Before creating any article, read the user's Hugo configuration to understand their blog setup.

**Find and read the config file:**
- `config.yml` or `config.yaml` (YAML)
- `config.toml` (TOML)
- `hugo.toml` (newer Hugo versions)
- `config/_default/` (directory-based config)

**Key values to extract:**
- `baseURL`: Blog URL
- `title`: Site title
- `theme`: Theme name (affects available front matter fields)
- `params.author`: Default author
- `params` section: Theme-specific settings

**Action:** Use Glob to find config files, then Read to understand the structure.

### Step 2: Recognize Content Formats and Structure

Understand how the user organizes their content.

**Check content directory structure:**
```
content/
├── posts/           # Blog posts (most common)
│   └── YYYY/        # Year-based organization
├── pages/           # Static pages
└── archives.md      # Archives page
```

**Content format options:**
- `.md` - Markdown (most common)
- `.markdown` - Markdown (alternative extension)
- `.html` - Raw HTML

**Action:** Use Glob to explore `content/posts/` structure and identify patterns.

### Step 3: Recognize Front Matter Requirements

Determine what front matter fields the blog expects.

**Standard front matter fields:**
```yaml
---
title: "Article Title"           # Required: Chinese title
date: YYYY-MM-DDTHH:MM:SS+08:00  # Required: ISO 8601 format
draft: true                      # true for drafts, false for published
author: "<AgentName>"            # Article author
categories: ["Category"]         # Content categories
showToc: true                    # Table of contents
tags: ["tag1", "tag2", "AI generated"]  # Content tags
---
```

**Field purposes:**
| Field | Purpose | Notes |
|-------|---------|-------|
| `title` | Article title | In Chinese |
| `date` | Publication date | Use China timezone +08:00 |
| `draft` | Publication status | `true` for drafts |
| `author` | Author name | Usually from config or agent name |
| `categories` | Content grouping | e.g., "Things I Learned" |
| `showToc` | Enable TOC | `true` for longer articles |
| `tags` | Discoverability | MUST include "AI generated" |

**Action:** Check existing posts to see what fields are consistently used.

### Step 4: Ask User About Blog Topic

Gather requirements before writing.

**Use AskUserQuestion to clarify:**

```yaml
questions:
  - question: "What topic should the blog post cover?"
    header: "Topic"
    options:
      - label: "Technical Tutorial"
        description: "Step-by-step guide for a technology or tool"
      - label: "Project Experience"
        description: "Share practical experience from a project"
      - label: "Research Summary"
        description: "Summarize findings from research or reading"
      - label: "Quick Insight"
        description: "Brief thought or observation worth sharing"

  - question: "What depth should the article have?"
    header: "Depth"
    options:
      - label: "Quick Summary"
        description: "500-1500 words, ~3 min read"
      - label: "Deep Dive"
        description: "2000-3000 words, ~5+ min read"
```

**Gather from user:**
- Main topic and key points to cover
- Target audience (beginners vs advanced)
- Source materials (URLs, files, or conversation context)
- Any specific requirements or constraints

### Step 5: Generate Draft Article

Create the blog post with proper structure.

**Front matter (set `draft: true`):**
```yaml
---
title: "文章标题"
date: 2026-02-28T14:30:00+08:00
draft: true
author: "<AgentName>"
categories: ["Things I Learned"]
showToc: true
tags: ["tag1", "tag2", "AI generated"]
---
```

**Content structure:**

```markdown
## 参考资料

- [Source Title 1](url-1)
- [Source Title 2](url-2)

---

## Main Heading

Introduction paragraph...

### Subheading

Body content...

### Another Subheading

More content...

---

*本文包含AI生成内容*
```

**Structure requirements:**
1. **Reference Sources FIRST** - List all source materials at the beginning
2. **Main content** - Clear headings, logical flow
3. **AI disclaimer LAST** - Required for all AI-generated content

**Save location:**
- Directory: `content/posts/YYYY/` (current year)
- Filename: lowercase-with-hyphens.md
- Example: `content/posts/2026/my-article-title.md`

### Step 6: Review Writing Quality

Review the generated content for style and accuracy. For detailed guidelines, see `references/chinese-writing-style.md`.

**Writing Style Checklist:**

| Aspect | Requirement |
|--------|-------------|
| **Tone** | Professional yet conversational |
| **Voice** | First-person for personal insights |
| **Clarity** | Explain technical concepts simply |
| **Engagement** | Use examples and practical applications |
| **Brevity** | Match length to article type |

**Fact Verification:**
- All facts must have a source provided by the user
- If a claim lacks a source, either:
  - Ask the user for the source, or
  - Remove or qualify the claim
- Mark unsourced claims with "据称" or " reportedly" when necessary

### Step 7: Publish Article

After reviewing, set `draft: false` to publish the article.

**Action:**
1. Ask user: "Review complete. Would you like to publish this article now?"
2. If yes, update front matter: `draft: false`
3. Confirm the article is now publicly visible

**Note:** Only publish after user approval. Keep `draft: true` if user wants to make more changes.

---

## Article Content Guidelines

### Length by Article Type

| Type | Word Count | Reading Time |
|------|------------|--------------|
| Quick Summary/Sharing | 500-1500 | ~3 minutes |
| Project Analysis/Deep Dive | 2000-3000 | ~5+ minutes |

**General rule:** Average reading speed is 400-600 Chinese characters/minute. Keep under 5 minutes for most content.

### Language Requirements

- **Language**: Simplified Chinese (简体中文)
- **Style**: Natural, fluent, avoid translation-ese
- **Structure**: Short paragraphs, clear headings
- **Code**: Use proper syntax highlighting with language tags

### Required Elements

1. **Reference Sources** (first section after front matter)
2. **Main content** with logical headings
3. **AI disclaimer** (at the very end):
   ```markdown
   ---

   *本文包含AI生成内容*
   ```

---

## Examples

### Complete Draft Article

```markdown
---
title: "使用 Docker 部署 Go 应用"
date: 2026-02-28T14:30:00+08:00
draft: true
author: "Claude"
categories: ["Things I Learned"]
showToc: true
tags: ["Docker", "Go", "DevOps", "AI generated"]
---

## 参考资料

- [Docker 官方文档](https://docs.docker.com/)
- [Go 部署最佳实践](https://example.com/go-deploy)

---

## 为什么选择 Docker

Docker 提供了一致的部署环境...

### 基本概念

容器化部署的核心优势...

## 实践步骤

### 1. 创建 Dockerfile

```dockerfile
FROM golang:1.21-alpine
WORKDIR /app
COPY . .
RUN go build -o main .
CMD ["./main"]
```

### 2. 构建镜像

```bash
docker build -t my-go-app .
```

---

*本文包含AI生成内容*
```

---

## Quick Reference

### Workflow Summary

1. **Config** → Read Hugo config file
2. **Structure** → Check content directory organization
3. **Front Matter** → Identify required fields
4. **Ask** → Clarify topic with user
5. **Draft** → Generate with `draft: true`
6. **Review** → Check style and sources
7. **Publish** → Set `draft: false` after approval

### File Locations

| Item | Location |
|------|----------|
| Config | `config.yml` / `config.toml` / `hugo.toml` |
| Posts | `content/posts/YYYY/` |
| Archives | `content/archives.md` |

### Common Tags

- Technical: `["技术名", "AI generated"]`
- Tutorial: `["Tutorial", "技术名", "AI generated"]`
- Experience: `["实践经验", "技术名", "AI generated"]`
