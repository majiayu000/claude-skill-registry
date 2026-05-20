---
name: strapi-blog-slug-mandatory
description: Enforce mandatory slug parameter for Strapi blog post updates. Use when (1) Updating Strapi blog posts via MCP, (2) Creating blog content, (3) Fixing blog post issues. ZERO TOLERANCE - WITHOUT SLUG = WORK IS NULL AND VOID. The slug is required for blog detail pages to work correctly.
---

# MANDATORY: Strapi Blog Post Slug Requirement

**CRITICAL RULE - ZERO TOLERANCE**

## WITHOUT SLUG = WORK IS NULL AND VOID

When updating ANY Strapi blog post using the MCP server, you **MUST ALWAYS** include the `slug` parameter.

### Why This Is Critical

The slug is used in the blog detail route: `/blog/{slug}`

**Without the slug parameter:**
- Blog detail pages will 404
- All your table formatting work is useless
- Users cannot view the updated content
- The work is completely wasted

**With the slug parameter:**
- Blog detail pages work correctly
- Users can access the content
- All formatting displays properly

---

## MANDATORY CHECKLIST

Before calling `mcp__ainative-strapi__strapi_update_blog_post`, verify:

- [ ] **Slug parameter is included** (REQUIRED)
- [ ] **Content parameter is included** (REQUIRED)
- [ ] **Document ID is included** (REQUIRED)

---

## Correct Usage Examples

### CORRECT - Always include slug

```typescript
mcp__ainative-strapi__strapi_update_blog_post({
  document_id: "abc123",
  slug: "my-blog-post-title",        // REQUIRED!
  content: "# Updated content..."
})
```

### WRONG - Missing slug (NULL AND VOID)

```typescript
mcp__ainative-strapi__strapi_update_blog_post({
  document_id: "abc123",
  // slug: missing!                   // FATAL ERROR!
  content: "# Updated content..."
})
```

---

## How to Get the Slug

### Option 1: From existing post data
When you fetch a post with `strapi_get_blog_post`, the response includes the slug:

```json
{
  "data": {
    "slug": "existing-blog-post-slug"  // Use this!
  }
}
```

### Option 2: Generate from title (if creating new)
Convert title to URL-friendly slug:
- Lowercase
- Replace spaces with hyphens
- Remove special characters
- Example: "My Blog Post!" → "my-blog-post"

---

## When to Include Slug

**ALWAYS.**

Even if you're only updating:
- Content
- Excerpt
- Tags
- Any other field

**ALWAYS include the slug parameter.**

---

## Enforcement

This is a **ZERO TOLERANCE** rule:

1. **Before every Strapi blog update**, check: "Did I include the slug?"
2. **If slug is missing**, STOP and add it
3. **Never proceed** without the slug parameter
4. **No exceptions**

---

## Remember

**WITHOUT SLUG = WORK IS NULL AND VOID**

If you update a blog post without the slug, all your work is wasted because users cannot access the updated content.
