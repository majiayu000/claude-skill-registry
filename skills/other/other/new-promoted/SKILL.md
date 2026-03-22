---
name: new-promoted
description: Creates a new promoted card in src/content/promoted/ with valid frontmatter and ordering. Use when adding a featured item, call-to-action, or highlighted content to the homepage.
argument-hint: "<title>"
disable-model-invocation: true
---

Create a new promoted/featured card in the `src/content/promoted/` directory.

## Steps

1. Take the title from the user's argument. If not provided, ask for one.
2. Generate a kebab-case filename from the title.
3. Read existing promoted items in `src/content/promoted/` to determine the next `order` number (highest existing order + 1, or 1 if none exist).
4. Ask the user for:
   - **Description** — keep under 120 characters
   - **Link URL** — destination when the card is clicked
   - **Link text** — CTA button text (e.g., "Learn more", "View project")
   - **Image URL** — card image
5. Create `src/content/promoted/<slug>.md`:

```markdown
---
title: "<title>"
description: "<description>"
image: "<image URL>"
link: "<link URL>"
linkText: "<link text>"
order: <next order number>
publishedAt: <today's date YYYY-MM-DD>
---
```

6. Tell the user:
   - The file was created at `src/content/promoted/<slug>.md`
   - The `order` field controls display order on the homepage (lower = first)
   - Keep title under 60 characters and description under 120 characters
   - All fields are required for promoted cards
