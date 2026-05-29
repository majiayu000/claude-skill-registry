---
name: unsplash-header-images
description: Search Unsplash for relevant blog header images and add header_image front matter fields to Jekyll blog posts. Use this skill when creating new blog posts or when the user asks to add/update a header image. Automatically finds appropriate images based on article topic and adds complete attribution metadata (image URL, alt text, photographer credit, source links).
tags: [jekyll, unsplash, images, blog, header]
---

# Unsplash Header Images Skill

You help find relevant images on Unsplash and properly integrate them into Jekyll blog posts with complete attribution metadata.

## When to Use This Skill

This skill is automatically invoked when:
- Creating a new blog post
- User asks to add a header image to an article
- User asks to update/change an existing header image

## Required Front Matter Fields

Every blog post should have these header image fields:

```yaml
header_image: "https://images.unsplash.com/photo-XXXXX?w=1600&q=80"
header_image_alt: "Meaningful description for accessibility"
header_image_credit: "Photographer Name"
header_image_credit_url: "https://unsplash.com/@photographer"
header_image_source: "Unsplash"
header_image_source_url: "https://unsplash.com"
```

### Field Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `header_image` | Yes | Unsplash URL with `?w=1600&q=80` optimization |
| `header_image_alt` | Yes | 5-15 word description for screen readers |
| `header_image_credit` | Recommended | Photographer's name |
| `header_image_credit_url` | Recommended | Photographer's Unsplash profile |
| `header_image_source` | Optional | "Unsplash" |
| `header_image_source_url` | Optional | "https://unsplash.com" |

## Step-by-Step Process

### 1. Understand the Article Topic

Read the article's:
- **Title**: Primary source for keywords
- **Categories**: Additional context
- **Excerpt**: Core theme
- **Content**: Deep understanding of the topic

### 2. Generate Search Keywords

Extract 2-3 specific keywords that represent the article's theme:

**Examples:**

| Article Title | Good Keywords | Bad Keywords |
|--------------|---------------|--------------|
| "AI Reveals: Effort Isn't Value" | "artificial intelligence work", "automation productivity" | "effort", "value" |
| "MySQL to S3 with AWS DMS" | "server room technology", "database infrastructure" | "mysql", "code" |
| "Google Is Dead. Follow The Eyes" | "hockey strategy", "marketing attention" | "google", "search" |

**Rules:**
- ✅ Use concrete, visual concepts
- ✅ Think metaphorically (e.g., "paths" for "journey", "fog" for "confusion")
- ❌ Avoid generic terms like "blog", "article", "business"
- ❌ Avoid overly technical terms that won't have good photos

### 3. Search Unsplash

Use the WebSearch tool to find images on Unsplash:

```
Search: site:unsplash.com [your keywords]
```

Then visit the Unsplash photo page to get the full details.

**Alternative:** Use WebFetch to directly access Unsplash search results and extract photo information.

### 4. Select the Best Image

Choose an image that:
- **Visually reinforces** the article's theme
- **Has strong composition** (clear focal point, good colors)
- **Matches blog aesthetic** (check other articles for consistency)
- **Is not cliché** (avoid obvious stock photo looks)
- **Has clear attribution** (photographer name visible)

### 5. Extract Photo Information

From the Unsplash photo page, extract:

**Photo URL:**
```
https://images.unsplash.com/photo-1558494949-ef010cbdcc31
```

**Add optimization parameters:**
```
?w=1600&q=80
```

**Photographer info:**
- Name: e.g., "Taylor Vick"
- Profile: e.g., "https://unsplash.com/@tvick"

**Alt text:**
Write a 5-15 word description focusing on what the image shows (not what it symbolizes):
- ✅ "Server room with blue lights"
- ❌ "Technology and infrastructure concept"

### 6. Add to Front Matter

Edit the post file to add all header image fields after the `excerpt` field:

```yaml
---
layout: post
title: "Your Article Title"
date: 2025-12-30
categories: [category1, category2]
excerpt: "Your excerpt..."
header_image: "https://images.unsplash.com/photo-XXXXX?w=1600&q=80"
header_image_alt: "Descriptive alt text"
header_image_credit: "Photographer Name"
header_image_credit_url: "https://unsplash.com/@photographer"
header_image_source: "Unsplash"
header_image_source_url: "https://unsplash.com"
---
```

### 7. Validate

After adding the fields:
- ✅ Verify YAML syntax (proper quotes, no special characters)
- ✅ Check image URL includes `?w=1600&q=80`
- ✅ Ensure alt text is concise and descriptive
- ✅ Confirm photographer credit is accurate

## Image Selection Strategy by Topic

Common article topics and effective image approaches:

### AI & Technology
- Code on screens with glow/blue light
- Abstract digital patterns
- Futuristic minimal environments
- Avoid: Robots, humanoid AI (often cliché)

### Work & Productivity
- Minimal desks/workspaces
- Focused work moments
- Tools and craftsmanship
- Avoid: Corporate stock photos, fake enthusiasm

### Data & Engineering
- Server rooms
- Infrastructure (cables, networks)
- Abstract patterns/visualizations
- Avoid: Generic charts, stock business graphics

### Philosophy & Ideas
- Nature metaphors (paths, fog, horizons)
- Minimalist abstract compositions
- Thinking/contemplation moments
- Avoid: Literal representations

## Language Considerations

The blog accepts both English and French articles:
- Image selection is language-agnostic
- Alt text should match article language
- Photographer credits remain in English (standard)

**Example for French article:**
```yaml
header_image_alt: "Paysage brumeux avec chemin forestier"
header_image_credit: "John Smith"
```

## Common Patterns

### Pattern 1: New Article Creation
```
User: "Create a new blog post about X"
→ After creating the post, automatically invoke this skill
→ Add header image before committing
```

### Pattern 2: Update Existing Article
```
User: "Add a header image to the MySQL article"
→ Read the article to understand topic
→ Search and select appropriate image
→ Edit front matter to add fields
```

### Pattern 3: Batch Update
```
User: "Add header images to all articles without them"
→ Find articles without header_image field
→ Process each one individually
→ Report progress
```

## Integration with Blog Layout

The custom `_layouts/post.html` already supports header images:
- Displays as banner (max 400px height, 250px on mobile)
- Shows photographer credit below with link
- Applies `border-radius: 8px` styling
- Fully responsive

No additional setup needed - just add the YAML fields.

## Troubleshooting

**Issue: Image doesn't display**
- Check that `layout: post` is set in front matter
- Verify image URL is valid and includes `?w=1600&q=80`
- Ensure no YAML syntax errors

**Issue: Attribution not showing**
- Verify `header_image_credit` field is present
- Check `header_image_credit_url` has valid URL format

**Issue: Image too large/distorted**
- Ensure CSS is loaded (check `assets/main.scss` exists)
- Verify `object-fit: cover` is applied in CSS

## Success Criteria

A successful header image addition includes:
1. ✅ Relevant, high-quality image that matches article theme
2. ✅ All required front matter fields present
3. ✅ Proper attribution with photographer name and link
4. ✅ Optimized URL with `?w=1600&q=80` parameters
5. ✅ Descriptive alt text (5-15 words)
6. ✅ Valid YAML syntax
7. ✅ Commits the change with clear commit message

## Example Workflow

**Article:** "The Effort Trap: What AI Really Reveals About Work"

**Process:**
1. **Keywords:** "artificial intelligence work", "automation productivity"
2. **Search:** Visit Unsplash, search for "artificial intelligence work"
3. **Select:** Choose image of minimalist workspace with code/laptop
4. **Extract:**
   - URL: `https://images.unsplash.com/photo-1499951360447-b19be8fe80f5`
   - Photographer: "Domenico Loia" (@domenicoloia)
   - Alt: "Minimalist workspace with laptop"
5. **Add to front matter:**
```yaml
header_image: "https://images.unsplash.com/photo-1499951360447-b19be8fe80f5?w=1600&q=80"
header_image_alt: "Minimalist workspace with laptop"
header_image_credit: "Domenico Loia"
header_image_credit_url: "https://unsplash.com/@domenicoloia"
header_image_source: "Unsplash"
header_image_source_url: "https://unsplash.com"
```
6. **Validate:** Check YAML syntax, verify URL
7. **Done:** Image will display as banner on article page

---

**Note:** This skill complements the existing `jekyll-blog-post` skill for content creation and should be used together when creating new articles.
