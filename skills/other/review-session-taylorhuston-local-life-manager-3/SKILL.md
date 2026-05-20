---
name: review-session
description: Retrieval practice session to test retention on a topic. Use when user wants to test their knowledge, practice recall, quiz themselves, or check what they remember. Triggers on "quiz me", "test my knowledge", "review [topic]", "what do I remember".
model: claude-haiku-4-5-20251001
argument-hint: [topic]
allowed-tools: Read, Write, Glob
---

Run a retrieval practice session on: $ARGUMENTS

This is NOT teaching. Goal: test retention through active recall.

## Setup

1. Read learning plan, find topic and proficiency
2. Read previous sessions on this topic
3. Gather concepts, corrections, misconceptions from past sessions
4. Create session file with `"type": "review"` per `references/session-schema.md`
5. Update index.json

## Conduct Review

1. Start broad: "Tell me everything you remember about [topic]"
2. Probe specific concepts from past sessions
3. For each response:
   - Ask confidence (1-5) BEFORE revealing if correct
   - DO NOT immediately correct - let them struggle (desirable difficulty)
   - Only after full attempt, provide feedback
4. Log `retrieval_test` entries per `references/entry-types.md`

## Question Types

| Past Entry | Question Style |
|------------|---------------|
| `concept` | "What is...?" or "Explain..." |
| `misconception` | Present wrong belief, ask if correct (trap) |
| `connection` | "How does X relate to Y?" |
| `elaboration` | "Why does X work that way?" |

## Scoring

Per `references/proficiency.md`:
- Full correct = 1, Partial = 0.5, Wrong = 0
- Score = (points / questions) × 100%

## End Session

Calculate retention score, update proficiency, show calibration report.
