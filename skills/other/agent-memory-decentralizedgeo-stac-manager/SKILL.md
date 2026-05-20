---
name: agent-memory
description: Use to maintain technical continuity, architecture context, and user preferences across multiple development sessions
---

# Agent Memory: Persistent Context Retention

## Overview

Use this skill to treat the `.github/memory/` directory as a "Long-Term Memory" store. This ensures that technical insights, user preferences, and implementation patterns survive beyond a single session, preventing context resets.

**Announce at start:** "I'm using the agent-memory skill to synchronize project context."

## Memory Components

The memory is stored in specific files within `.github/memory/`:

1.  **`episodic.md`**: Chronological log of major decisions, research breakouts, and milestones (The "What happened and why").
2.  **`semantic.md`**: Technical glossary and architectural map. Core abstractions and library quirks (The "How things work here").
3.  **`procedural.md`**: Evolving best practices and common pitfalls found during TDD/debugging (The "How we build here").
4.  **`preferences.md`**: stylistic nuances and specific user directives (The "User's personality").

## The Process

### Step 1: Memory Recall (Associative Activation)
At the start of any major phase (Planning or Execution):
1.  **Scan**: Read all files in `.github/memory/`.
2.  **Chain**: Link current requirements to past successes or failures documented in memory.
3.  **Synthesize**: State how past context influences your current approach.

### Step 2: Consolidation & Retention
After every implementation batch or design approval:
1.  **Selective Retention**: Identify 1-3 critical insights worth saving. Avoid noise.
2.  **Update State**: Update the relevant memory file. 
3.  **Abstraction**: Once a pattern repeats 3 times, move it from `episodic.md` to a high-level rule in `procedural.md`.

### Step 3: Temporal Chaining (Episodic Logging)
When logging a milestone in `episodic.md`, maintain the link:
- **Format**: `[ID: EVENT_NAME] -> Follows [PREVIOUS_ID]. Context: [Details].`

## Rules
- **No Hallucination**: Only store verified facts (tests, docs, or explicit user approval).
- **Brevity is Depth**: Use concise bullet points.
- **Forget the Noise**: Do not store minor lint fixes or temporary variables. Store **Architectural Intent**.

## Initialization
If `.github/memory/` doesn't exist, create it. Initialize empty files with headers if necessary.
