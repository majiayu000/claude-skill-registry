---
name: create-blog
description: Create an SEO-optimized blog post from a topic or keyword.
argument-hint: <topic> [audience=general] [word_count=1500]
disable-model-invocation: true
---

Create a blog post: $ARGUMENTS

## 1. Research

Research the topic for the target audience.

- Search for top-ranking content on this topic
- Identify common themes, questions, and angles
- Note content gaps and opportunities
- Extract key terms and phrases competitors use
- Collect People Also Ask questions
- Search brand knowledge base for relevant product info
- Save research findings (top competitor outlines, common questions, key terminology, content gaps)

## 2. Outline

Create a detailed outline referencing brand voice.

### Outline format

- H1: article title
- H2 sections with notes on what to cover
- H3 for subsections where needed
- FAQ section with questions and answer guidance

### Header rules

- Sentence case (first word capitalized, rest lowercase except proper nouns)
- No colons or em-dashes in headers
- Use questions where natural ("What is X" not "Definition of X")
- Maximum 5-6 H2 sections (excluding FAQ)
- H3s only for lists, steps, or subtopics

Target the specified word count. Include a checkpoint to review outline before drafting if the user wants it.

## 3. Draft

Write the full article based on the outline.

- Delegate to the content-writer agent for a fresh context window
- Follow brand voice from the first word
- Follow outline structure exactly
- Target word count, 8th grade reading level, 2-3 sentence paragraphs
- Define terms when introduced; no unverified statistics or claims; no filler
- Apply SEO best practices (see seo-guidelines skill)
- Verify all outline sections addressed; remove repetition; check brand voice

## 4. Finalize

Review and create final deliverable.

- Run the content-critic agent to validate brand voice
- Final checks: word count, headers follow style, no walls of text, FAQ answers standalone
- Create full article in markdown with title tag (50-60 chars), meta description (150-160 chars), recommended slug
