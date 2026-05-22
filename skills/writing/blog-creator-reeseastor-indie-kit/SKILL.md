---
name: blog-creator
description: Create SEO-optimized MDX blog posts with proper frontmatter
---

# Blog Post Creator Skill

This skill helps you create high-quality, SEO-optimized blog posts using the MDX content engine.

## Directory Structure

- **Content Location**: `src/content/blog/*.mdx`
- **Images**: `/public/assets/images/` (reference as `/assets/images/...`)
- **Engine**: `src/lib/mdx/blogs.ts`
- **Frontend**: `src/app/(website-layout)/blog/`

## File Format

Each blog post must be a `.mdx` file with specific frontmatter:

```markdown
---
title: "Your Engaging Title Here"
tags: ["tag1", "tag2", "seo-keyword"]
featuredImage: "/assets/images/your-image.png"
createdDate: "YYYY-MM-DD"
description: "A compelling meta description for SEO (150-160 chars recommended)"
---

# Your Title H1

Introduction paragraph...

## Section H2

Content...
```

## Best Practices

1.  **Slug Generation**: The filename becomes the slug (e.g., `my-post.mdx` -> `/blog/my-post`). Use kebab-case.
2.  **Images**: Place images in `public/assets/images` and reference them with absolute paths.
3.  **Tags**: Used for "Related Articles" logic. Include 3-5 relevant tags.
4.  **Components**: You can import and use React components inside MDX files (if configured in `mdx-components.tsx`).
5.  **SEO**: - `title`: Used for `<title>` and `og:title`. - `description`: Used for `<meta name="description">` and `og:description`. - `featuredImage`: Used for `og:image`.
    **DO NOT USE single quotes in the frontmatter. Use double quotes instead.**

## Workflow

1.  Create a new file: `src/content/blog/your-slug.mdx`.
2.  Add the frontmatter.
3.  Write content using Markdown syntax.
4.  (Optional) Add images to `public/assets/images/`.

## Example

File: `src/content/blog/getting-started.mdx`

```markdown
---
title: "Getting Started with Indie Kit"
tags: ["guide", "tutorial", "indie-kit"]
featuredImage: "/assets/images/og.png"
createdDate: "2024-03-20"
description: "A complete guide to setting up your new SaaS project with Indie Kit in under 10 minutes."
---

# Getting Started

Welcome to the future of SaaS development...
```

Refer to [reference.md](reference.md) for more details.
