---
name: new-post
description: Creates a new blog post in src/content/blog/ with valid frontmatter, slug, and author. Use when the user wants to write a new blog post, create an article, or add content to the blog.
argument-hint: "<title>"
disable-model-invocation: true
---

Create a new blog post in the `src/content/blog/` directory.

## Steps

1. Take the title from the user's argument. If no title is provided, ask for one.
2. Generate a kebab-case filename from the title (e.g., "My First Post" → `my-first-post.md`).
3. Get the author name by running `git config user.name`. Fall back to "Author" if not set.
4. Create `src/content/blog/<slug>.md` with this frontmatter:

```markdown
---
title: "<title>"
description: "<ask user or generate a one-sentence summary>"
author: "<git user.name>"
publishedAt: <today's date YYYY-MM-DD>
tags: []
draft: true
---

Write your post content here.
```

5. Tell the user:
   - The file was created at `src/content/blog/<slug>.md`
   - The post is in **draft mode** — set `draft: false` when ready to publish
   - They can add an optional `image` field to the frontmatter for a hero image
   - Tags can be added as an array of strings: `tags: ["astro", "tutorial"]`
