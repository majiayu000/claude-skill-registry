---
name: blog-01-create-prompt
description: Create a detailed prompt for generating high-quality blog posts
---

## Context

Use the `blog-content-architect` agent to create a **prompt** to generate a blog post from the idea: $ARGUMENTS

## Process

### 1. Review Initial Idea

Review user's blog idea, WebSearch for context, and enhance the idea into a detailed prompt. Consider these aspects:

- What sparked this idea?
- What problem does it solve?
- What's your experience with this topic?
- Have you implemented this?

### 2. Ask Strategic Questions

Ask any questions needed to clarify idea? **use `AskUserQuestion` tool** to provide smart defaults.

### 3. Save & Output

Save enhanced prompt to `._tmp/prompts/YYYY-MM-DD-blog-title.md` and present:

1. **Blog Post Prompt**: [Detailed prompt]
2. **Print usage**: `/blog-02-write-post @._tmp/prompts/YYYY-MM-DD-blog-title.md`
