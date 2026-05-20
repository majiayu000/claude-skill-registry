---
name: publish-to-shopify
description: Publish finalized content to the Shopify storefront
user-invocable: true
---

You are helping the marketing team publish content to the Jocko Fuel Shopify store.

Follow these steps:

### Step 1: Get the Content

Ask the user for:
- **Content to publish** — pasted text/HTML, file path, or content from a previous skill run
- **Content type** — blog post, product description update, or page content
- **Publication timing** — publish immediately or schedule for a specific date/time

### Step 2: Pre-Publish Validation

Delegate to the pre-publish-agent to run final quality checks:
- DSHEA compliance verification
- SEO metadata completeness
- Formatting and link validation
- Required disclaimers present

If any checks fail, present the issues and ask the user to resolve them before proceeding.

### Step 3: Configure Publication Settings

For **blog posts**, collect:
- Title
- Author
- Blog category (e.g., "Nutrition", "Fitness", "Discipline")
- Tags
- Featured image (path or URL)
- SEO title and meta description
- URL handle (slug)

For **product descriptions**, collect:
- Product ID or handle
- Updated description HTML
- Updated metafields (if any)

### Step 4: Preview and Confirm

Present a publication preview showing:
- Content type and destination
- Title and URL
- SEO metadata
- Publication date/time
- Tags and categories

**Require explicit user confirmation before publishing.**

### Step 5: Publish

Delegate to the publishing-agent (ask-always mode) to execute the Shopify write operation. Report back:
- Published URL
- Publication timestamp
- Any warnings from the publishing process

### Error Handling

- If pre-publish validation fails, block publishing and show required fixes
- If Shopify API is unavailable, inform the user and suggest retrying later
- If content formatting breaks during upload, present the issue and offer to fix
