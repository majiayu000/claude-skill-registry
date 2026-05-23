---
name: study-notes
description: Create comprehensive study notes on a topic. Use when user wants detailed notes, a study guide, or documentation on a subject. Triggers on "study notes", "create notes", "document [topic]", "write up [topic]".
model: claude-opus-4-5-20251101
argument-hint: [topic] [destination path]
---

Create comprehensive study notes on: $1

**Save to:** $2 (or suggest location in `my-vault/06 Knowledge Base/`)

## Before Writing

- Search vault for existing related notes
- Ask what depth/focus user wants
- Confirm destination path

## Format

- Use Study class frontmatter
- Include flashcard tag for spaced repetition
- Clear headings and subheadings
- Tables for comparisons
- `> [!warning]` callouts for gotchas
- Practical examples and commands
- Quick Reference section with key numbers/facts
- Related links to existing vault notes

## Content Approach

- Start broad, then go deep
- Cover theory and practical application
- Include troubleshooting scenarios
- Add interview-style Q&A where appropriate
- Think about what's useful to review later
