---
name: strapi-blog-image-unique
description: Enforce unique featured images for Strapi blog posts. Use when (1) Creating new blog posts, (2) Updating blog post images, (3) Auditing blog content for duplicates, (4) Publishing blog content. ZERO TOLERANCE - Every blog post MUST have a unique featured image, never reuse images across posts.
---

# MANDATORY: Strapi Blog Post Featured Image Uniqueness

**CRITICAL RULE - ZERO TOLERANCE**

## DUPLICATE IMAGES = UNPROFESSIONAL AND CONFUSING

When creating or updating ANY Strapi blog post, you **MUST ENSURE** that each post has a **UNIQUE featured image** used **ONLY ONCE**.

### Why This Is Critical

Featured images are the first visual element users see on:
- Blog listing pages
- Blog detail pages
- Social media shares (OpenGraph images)
- Search engine results

**With duplicate images:**
- Users think multiple posts are the same content
- Unprofessional appearance
- Reduced click-through rates
- Confused users and poor UX
- Damaged brand perception

**With unique images:**
- Each post is visually distinct
- Professional appearance
- Higher engagement
- Clear visual hierarchy
- Strong brand identity

---

## MANDATORY RULES

### Rule 1: One Image, One Post
**NEVER use the same featured image on multiple blog posts.**

Before assigning a featured image:
1. Check if the image is already used on another post
2. If yes, choose or create a different image
3. If no, proceed with the assignment

### Rule 2: Check Before Assigning
**ALWAYS run an image duplication check before publishing.**

Use the audit script:
```bash
node /tmp/check_blog_images.js
```

Or manually query Strapi:
```bash
curl https://ainative-community-production.up.railway.app/api/blog-posts?populate=featured_image
```

### Rule 3: Fix Duplicates Immediately
**If duplicates are found, fix them before any other work.**

Priority order:
1. Keep the image on the FIRST published post (oldest)
2. Assign NEW unique images to all other posts
3. Never leave posts without featured images

### Rule 4: Document Image Sources
**Track where images come from to avoid accidental reuse.**

In the blog post metadata or CMS:
- Source: "Custom designed for this post"
- Source: "Stock photo from Unsplash (link)"
- Source: "AI-generated via DALL-E (prompt)"

---

## Important: Images from External API

**Featured images are NOT stored in Strapi's media library.**

Featured images come from an **external API**. The `featured_image` field contains:
- Image URL from external API
- API reference/ID
- Direct URL to hosted image

**This means:**
- Do NOT use Strapi's upload/media library
- DO use external API URLs or references
- Ensure each API image URL is unique per post
- Document which external API is being used

---

## How to Check for Duplicate Images

### Option 1: Automated Script (Recommended)
```bash
# Check all blog posts for duplicate image URLs/references
node scripts/strapi_check_blog_images.js

# If duplicates found (exit code 1), fix them immediately
```

### Option 2: Manual MCP Check
```typescript
// Fetch all posts with featured images
const posts = await mcp__ainative-strapi__strapi_list_blog_posts({
  pageSize: 100,
  page: 1
})

// Check featured_image field for each post
// Compare image URLs/API references for duplicates
```

### Option 3: Strapi Admin Panel
1. Go to: `https://ainative-community-production.up.railway.app/admin`
2. Navigate to: Content Manager → Blog Posts
3. Check featured_image field values (URLs or API references)
4. Identify any duplicate URLs/references
5. Click to edit and assign new API images

---

## Correct Workflow Examples

### CORRECT - Check before assigning

```typescript
// Step 1: Check if image is already used
const allPosts = await mcp__ainative-strapi__strapi_list_blog_posts({
  pageSize: 100
});

// Step 2: Verify no post uses this image ID
const imageId = "proposed-image-123";
const alreadyUsed = allPosts.data.some(
  post => post.featured_image?.id === imageId
);

// Step 3: Only assign if unique
if (!alreadyUsed) {
  await mcp__ainative-strapi__strapi_update_blog_post({
    document_id: "abc123",
    slug: "my-post",
    featured_image: imageId  // SAFE
  });
} else {
  // Choose a different image
}
```

### WRONG - Assign without checking

```typescript
// Blindly assigning an image without checking if it's already used
await mcp__ainative-strapi__strapi_update_blog_post({
  document_id: "abc123",
  slug: "my-post",
  featured_image: "some-image-id"  // MIGHT BE DUPLICATE!
});
```

---

## Image Selection Guidelines

### What Makes a Good Featured Image?

| Criteria | Good | Bad |
|----------|------|-----|
| **Relevance** | Directly related to post topic | Generic stock photo |
| **Quality** | High resolution (1200x630+ px) | Low resolution, pixelated |
| **Uniqueness** | Custom design or rare stock | Overused stock photo |
| **Brand** | Matches AINative color scheme | Off-brand colors |
| **Clarity** | Clear focal point | Busy, cluttered |
| **Format** | WebP or optimized JPG/PNG | Huge unoptimized files |

### Recommended Image Sources

1. **Custom Design** (Best)
   - Figma/Canva custom graphics
   - AINative brand elements
   - Product screenshots with branding

2. **AI-Generated** (Good)
   - DALL-E 3 with specific prompts
   - Midjourney for abstract concepts
   - Stable Diffusion for technical visuals

3. **Stock Photos** (Acceptable)
   - Unsplash (high quality, free)
   - Pexels (diverse selection)
   - Pixabay (CC0 license)

4. **Product Screenshots** (Post-Specific)
   - Dashboard screenshots
   - Code examples with syntax highlighting
   - API response examples

---

## Pre-Publication Checklist

Before publishing or updating ANY blog post:
- [ ] **Featured image is assigned**
- [ ] **Image is unique** (not used on other posts)
- [ ] **Image is high quality** (1200x630+ px)
- [ ] **Image is relevant** to post content
- [ ] **Image is optimized** (WebP or compressed JPG/PNG)
- [ ] **Image source is documented** (in case of licensing issues)

---

## Remember

**DUPLICATE IMAGES = UNPROFESSIONAL AND CONFUSING**

If you assign a duplicate image, users will:
- Think the posts are identical
- Skip reading what might be valuable content
- Lose trust in the quality of your content

**ALWAYS check for duplicates. ALWAYS use unique images. NO EXCEPTIONS.**
