---
name: new-blog-post
description: Create a new blog post with proper Quarto structure, frontmatter, and directory layout. Use when adding articles, tutorials, thoughts, or any blog content.
allowed-tools: Write, Bash(mkdir:*), Bash(date:*)
---

# Creating a New Blog Post

## Instructions

When creating a new blog post:

1. **Generate the slug** from the title:
   - Convert to lowercase
   - Replace spaces with hyphens
   - Remove special characters
   - Example: "My Awesome Post!" -> "my-awesome-post"

2. **Create the directory structure**:
   ```
   posts/<slug>/
   └── index.qmd
   ```

3. **Create index.qmd with this frontmatter**:
   ```yaml
   ---
   title: "Post Title"
   author: "Glenn Matlin"
   date: YYYY-MM-DD
   categories: [category1, category2]
   description: "Brief description for previews and SEO (under 160 characters)"
   image: featured.png
   draft: false
   ---
   ```

4. **Add initial content structure**:
   ```markdown
   Brief introduction paragraph...

   ## Section Heading

   Content...

   ## Conclusion

   Wrap-up...
   ```

## Category Suggestions

Common categories for this academic site:
- AI, Machine Learning, NLP, LLMs
- Research, Publications
- Python, Programming, Tools
- Career, PhD Life, Academia
- Tutorials, How-To

## Example

For a post titled "Understanding Transformer Architectures":

**File**: `posts/understanding-transformer-architectures/index.qmd`

```yaml
---
title: "Understanding Transformer Architectures"
author: "Glenn Matlin"
date: 2025-01-15
categories: [AI, Machine Learning, Deep Learning]
description: "A deep dive into transformer architectures and their impact on modern NLP"
draft: false
---

The transformer architecture has revolutionized natural language processing...
```

## After Creation

Suggest running `quarto preview` to verify the post renders correctly.
