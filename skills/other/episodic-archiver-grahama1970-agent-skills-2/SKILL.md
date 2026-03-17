---
name: episodic-archiver
description: >
  Episodic Memory Archiver. Stores full conversation transcripts with embeddings
  and analysis into ArangoDB. Tracks UNRESOLVED sessions for reflection.
allowed-tools: Bash
triggers:
  - archive conversation
  - save episode
  - store transcript
  - remember this conversation
  - list unresolved
metadata:
  short-description: Analyzes and stores episodic conversation memory
---

# Episodic Archiver

Analyzes conversation transcripts, embeds them for search, categorizes turns, and **tracks unresolved sessions** for later reflection.

## Commands

```bash
# Archive a conversation transcript
./run.sh archive transcript.json

# List unresolved sessions (for reflection)
./run.sh list-unresolved

# Mark a session as resolved after follow-up
./run.sh resolve <session_id>
```

## Unresolved Session Tracking

When archiving, the skill analyzes if the session was resolved:

| Condition | Result |
|-----------|--------|
| Session ends with error | Unresolved |
| Session ends with unanswered question | Unresolved |
| Errors without following solutions | Unresolved |
| Tasks without completion | Unresolved |

Unresolved sessions are stored in `unresolved_sessions` collection for reflection.

## Integration with /learn

```bash
# Reflect on past failures to find what to learn
/learn --from-gaps --scope horus_lore

# This queries:
# 1. unresolved_sessions (high priority)
# 2. agent_conversations (errors, questions)
# 3. Skill logs (failures)
```

## The Reflection Loop

```
Session ends → Archive → Detect unresolved → Store gap
                                    ↓
                            /learn --from-gaps
                                    ↓
                            Curiosity targets
                                    ↓
                            /dogpile → /learn
                                    ↓
                            Knowledge acquired
                                    ↓
                            ./run.sh resolve <session>
```

## Storage

**Collections:**
- `agent_conversations` - Individual turns with embeddings
- `unresolved_sessions` - Sessions needing follow-up

**Turn categories:** Task, Question, Solution, Error, Chat, Meta

## Input Format

```json
{
  "session_id": "task_123",
  "messages": [
    {"from": "User", "content": "Fix the bug in auth", "timestamp": 1234567890},
    {"from": "Agent", "content": "Looking at auth.py...", "timestamp": 1234567891}
  ]
}
```
