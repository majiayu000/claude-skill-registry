---
name: create-listicle
description: Create a list-based article on a topic.
argument-hint: <topic> [count=10] [audience=general] [word_count=1500]
disable-model-invocation: true
---

Create a listicle: $ARGUMENTS

## 1. Research

Research the topic to find list candidates.

- Existing listicles on this topic (what's ranking)
- Common "table stakes" items in most lists
- Unique or overlooked items competitors miss
- Questions the audience asks about this topic
- Brand knowledge base for relevant product ties

## 2. Curate List

Select the specified number of items.

- Include essential table stakes; add 2-3 unique items that differentiate
- For each item: what it is, why it matters, one key detail or example
- Determine ordering: priority, chronological, or thematic
- Checkpoint to review curated list before outlining if the user wants it

## 3. Outline

Create detailed outline.

- H1: count + benefit-focused title about topic
- Introduction (hook with problem/opportunity for audience)
- One H2 per list item (benefit-focused title, notes on what to cover)
- Conclusion (summary and next steps)
- FAQ optional

Header rules: each item header benefit-focused; consistent structure; headers scannable. Target word count.

## 4. Draft

Write the full listicle.

- Delegate to the content-writer agent for a fresh context window
- Introduction 100-150 words; each item 100-150 words; conclusion 75-100 words
- Parallel structure across items; consistent depth; 8th grade reading level; no filler
- Verify parallel structure; headers alone tell the story; consistent depth

## 5. Finalize

Review and create final deliverable.

- Run the content-critic agent to validate brand voice
- Final checks: all items consistent depth, scannable, no repetition between items
- Full article in markdown, title tag, meta description, recommended slug
