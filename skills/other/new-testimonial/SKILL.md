---
name: new-testimonial
description: Creates a new testimonial in src/content/testimonials/ with valid frontmatter. Use when adding a customer quote, review, or endorsement.
argument-hint: "<author-name>"
disable-model-invocation: true
---

Create a new testimonial in the `src/content/testimonials/` directory.

## Steps

1. Take the author name from the user's argument. If not provided, ask for one.
2. Generate a kebab-case filename from the author name (e.g., "Jane Doe" → `jane-doe.md`).
3. Ask the user for:
   - **Role** (e.g., "Senior Developer", "CTO")
   - **Company** (optional)
   - **Rating** (optional, 1-5)
   - **Quote text** — the actual testimonial
4. Create `src/content/testimonials/<slug>.md`:

```markdown
---
author: "<author name>"
role: "<role>"
company: "<company>"       # omit if not provided
rating: <rating>            # omit if not provided
publishedAt: <today's date YYYY-MM-DD>
---

<quote text without quotation marks>
```

5. Tell the user:
   - The file was created at `src/content/testimonials/<slug>.md`
   - The markdown body IS the quote — do not wrap in quotation marks
   - Optional fields: `company`, `avatar` (image URL), `rating` (1-5)
