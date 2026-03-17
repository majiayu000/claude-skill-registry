---
name: context-passport
description: Solve context fragmentation across Claude sessions. Use when users mention re-explaining themselves, losing conversation context, starting over, "you forgot," context loss, session continuity, picking up where we left off, or wanting Claude to remember across chats. Also use when users want to create/update their passport, generate session summaries, or maintain project continuity.
---

# Context Passport

Maintain user and project context across Claude sessions via a structured GitHub-hosted document.

## Core Components

### 1. The Passport (`PASSPORT.md`)
Token-efficient markdown in user's GitHub repo. See `references/passport-template.md`.

Sections:
- **Identity**: Name, timezone, communication preferences
- **Brain Manual**: ADHD accommodations, learning style, energy patterns  
- **Active Projects**: Current focus, phase, blockers
- **Context Stack**: Recent decisions, open questions, where we left off
- **Don't Make Me Repeat**: Facts explained too many times

### 2. Session Summary
Run `scripts/session-summary.py` on conversation exports to extract updates.

### 3. Quick-Start Prompt
User pastes at session start: "Read my Context Passport at [URL] and continue where we left off."

## Workflows

### Creating a New Passport
1. Read `references/passport-template.md`
2. Interview user for core info (max 5 questions)
3. Generate PASSPORT.md
4. User commits to repo

### End-of-Session Update
1. Export conversation (JSON preferred)
2. Run session-summary.py
3. Append to Context Stack
4. Commit changes

### Resuming with Context
1. User provides passport URL or content
2. Acknowledge context without restating
3. Continue from Context Stack

## Design Principles
- Token-efficient: Passport under 500 words
- Low-friction: 2-min end-of-session ritual max
- Accountability: Git history shows evolution
