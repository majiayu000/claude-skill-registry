---
name: learning-system
description: Structured learning and spaced repetition system. Use when user wants to learn a topic, start a study session, review material, generate flashcards, create study notes, or track learning progress. Triggers on phrases like "let's learn", "teach me", "study session", "review [topic]", "flashcards", "study notes".
---

# Learning System

A structured system for learning new topics and retaining knowledge through spaced repetition.

## Workflows

| Command | Purpose |
|---------|---------|
| `/start-session [topic]` | Begin a teaching session on a topic |
| `/end-session` | End current session, update progress |
| `/log-session` | Log entries mid-session |
| `/review-session [topic]` | Retrieval practice (test retention) |
| `/flashcards [file/topic]` | Generate spaced repetition flashcards |
| `/study-notes [topic]` | Create comprehensive study notes |

## Data Storage

- Sessions: `.claude/learning-sessions/`
- Learning plan: `.claude/learning-sessions/learning-plan.json`
- Session index: `.claude/learning-sessions/index.json`

## References

- **Session structure**: See `references/session-schema.md`
- **Entry types**: See `references/entry-types.md`
- **Proficiency levels**: See `references/proficiency.md`
- **Flashcard syntax**: See `references/flashcard-syntax.md`

## Teaching Approach

- Teach conversationally with Q&A
- Explain concepts, then ask questions to check understanding
- Correct misconceptions as they arise
- Build from fundamentals to advanced
- Use ASCII diagrams and tables where helpful
- Reference existing notes in `my-vault/06 Knowledge Base/`

## Session Structure

1. **Assess** - What do they already know? (retrieval warm-up)
2. **Identify** - What do they want to learn?
3. **Teach** - Incrementally with checkpoints
4. **Correct** - Fix misconceptions
5. **Connect** - Link to other topics
6. **Summarize** - Key takeaways
