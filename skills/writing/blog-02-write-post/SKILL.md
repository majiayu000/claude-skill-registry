---
name: blog-02-write-post
description: Create a new technical blog post with deep educational value and professional quality
---

Use the `blog-content-architect` agent to create high-quality technical blog content.

## Process

### 1. Explore & Research

- Search `packages/blog/content/2.blog/` for similar posts
- Use parallel subagents to WebSearch the topic
- Identify key sources, tools, and libraries

### 2. Plan & Question

Create a blog outline, then ask 3-5 focused questions (one at a time):

- User's experience with the topic
- Specific examples or use cases to include
- Preferred content structure (tutorial, guide, case study)

Prefer yes/no questions with smart defaults.

### 3. Confirm Plan

Show the outline to user and confirm direction before writing.

### 4. Write Post

Focus on:

- **Educational value**: Explain WHY, not just HOW
- **Technical accuracy**: Include working code examples
- **Authentic voice**: Share real experience and lessons learned
- **Practical insights**: Common pitfalls and troubleshooting

## File Format

Save to `packages/blog/content/2.blog/YYYYMMDD.your-post-title.md`

```yaml
---
title: 'Your Blog Post Title'
description: 'Brief description explaining value and key takeaways'
date: '2025-01-26'
image:
  src: '/images/todo-place-holder-image.png'
  alt: 'Descriptive alt text'
authors:
  - name: Chris Towles
    to: https://twitter.com/Chris_Towles
    avatar:
      src: /images/ctowles-profile-512x512.png
badge:
  label: 'Development' # AI Tools, DevOps, Tutorial, Architecture
---
##
```

## Final Reminder

A great blog post:

- Teaches ONE thing really well
- Feels like a conversation with a knowledgeable peer who's still learning
- Shows vulnerability and authentic experience
- Provides immediate practical value
- Is tight, focused, and leaves the reader wanting more (not overwhelmed)
