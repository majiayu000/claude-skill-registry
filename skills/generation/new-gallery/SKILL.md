---
name: new-gallery
description: Creates a new gallery item in src/content/gallery/ with valid frontmatter and image reference. Use when adding a photo, artwork, or visual item to the gallery collection.
argument-hint: "<title>"
disable-model-invocation: true
---

Create a new gallery item in the `src/content/gallery/` directory.

## Steps

1. Take the title from the user's argument. If no title is provided, ask for one.
2. Generate a kebab-case filename from the title.
3. Ask the user for:
   - **Category** (e.g., "Photography", "Design", "Illustration")
   - **Image URL** — or note that they need to provide one
4. Create `src/content/gallery/<slug>.md` with this frontmatter:

```markdown
---
title: "<title>"
description: "<ask user or generate a short description>"
image: "<image URL>"
category: "<category>"
publishedAt: <today's date YYYY-MM-DD>
tags: []
---

Write a description of this gallery item here. This text appears on the detail page.
```

5. Tell the user:
   - The file was created at `src/content/gallery/<slug>.md`
   - The `image` field is **required** — they must set a valid image URL
   - Image transforms (`/cdn-cgi/image/`) only work on Cloudflare-served domains
   - Tags can be added for filtering: `tags: ["landscape", "nature"]`
