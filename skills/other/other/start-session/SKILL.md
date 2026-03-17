---
name: start-session
description: Start a new learning session on a topic. Use when user wants to learn something new, begin studying, get taught a topic, or start a teaching conversation. Triggers on "teach me", "let's learn", "start session", "study [topic]", "explain [topic]".
model: claude-opus-4-5-20251101
argument-hint: [topic or file path]
allowed-tools: Read, Write, Glob
---

Start a new learning session on: $ARGUMENTS

## Setup

1. Read `.claude/learning-sessions/learning-plan.json`
2. Check for topics due for review (compare `last_covered` + interval vs today)
3. Read `.claude/learning-sessions/index.json`
4. Generate session ID: `YYYY-MM-DD-NNN` (increment if sessions exist today)
5. Read last 3-5 completed sessions to rebuild context
6. Create session file per `references/session-schema.md`
7. Update index.json
8. If file path provided: read it, identify gaps, note TODOs

## Retrieval Warm-up

If topic covered before:
- Ask: "Before we dive in, what do you remember about [topic]?"
- Let user attempt recall WITHOUT hints
- Log as `retrieval_attempt` entry (see `references/entry-types.md`)

## Begin

- Confirm session started
- Mention any topics due for review
- Acknowledge what they remembered, note gaps
- Ask what aspect to focus on
- Follow teaching approach in SKILL.md

## During Session

Log entries per `references/entry-types.md`. Use `/log-session` for long sessions.

## End

Use `/end-session` when done.
