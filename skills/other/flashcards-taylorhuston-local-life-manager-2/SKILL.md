---
name: flashcards
description: Generate spaced repetition flashcards from notes or topics. Use when user wants to create flashcards, make review cards, prepare for spaced repetition, or convert notes to quiz format. Triggers on "flashcards", "make cards", "spaced repetition", "review cards".
model: claude-sonnet-4-5-20250929
argument-hint: [file path or topic]
allowed-tools: Read, Edit, Glob, Grep
---

Generate flashcards for Obsidian Spaced Repetition from: $ARGUMENTS

## Syntax

See `references/flashcard-syntax.md` for formats:
- `::` single-sided
- `:::` bidirectional
- `;;` multi-line
- `==text==` cloze deletions

## Process

1. If file path: read and analyze it
2. If topic: search vault for relevant notes
3. Identify key concepts, terms, gotchas worth remembering
4. Generate cards grouped by subtopic
5. Ask where to add:
   - Inline within source note
   - Dedicated flashcards section at bottom
   - Separate flashcards file
6. Add cards to chosen location

## Guidelines

- **Atomic**: one concept per card
- **Bidirectional** for terminology, translations, concept ↔ example
- **Cloze** for port numbers, values, command syntax
- **Avoid**: yes/no questions, overly long answers, memorizing lists

Generate cards useful for recall, not trivial facts.
