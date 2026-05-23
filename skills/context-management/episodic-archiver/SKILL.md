---
name: episodic-archiver
description: >
  Episodic Memory Archiver. Stores full conversation transcripts with embeddings
  and analysis into ArangoDB. Use this to save the "User Story" or "Chain of Thought".
allowed-tools: Bash
triggers:
  - archive conversation
  - save episode
  - store transcript
  - remember this conversation
metadata:
  short-description: Analyzes and stores episodic conversation memory
---

# Episodic Archiver

This skill analyzes full conversation transcripts, embeds them for search, and categorizes turns.

## Usage

```bash
# Save a JSON transcript to episodic memory
.agents/skills/episodic-archiver/run.sh archive <transcript.json>
```

## Input Format

The JSON file should be a list of messages or an object with a `messages` list:

```json
{
  "session_id": "task_123",
  "messages": [
    {
      "from": "Coordinator",
      "to": "Worker",
      "message": "Please fix the bug...",
      "timestamp": 1234567890
    },
    ...
  ]
}
```

## Storage

Data is stored in ArangoDB collection `agent_conversations` with:

- `embedding`: Vector representation (768d)
- `category`: LLM-derived tag (Task, Question, Solution, etc.)

## Prerequisites

- ArangoDB credentials in `.env` (e.g., `ARANGO_URL`, `ARANGO_DB`, `ARANGO_USER`, `ARANGO_PASS`).
- **Embedding service** running (recommended): `EMBEDDING_SERVICE_URL=http://127.0.0.1:8602`
- Falls back to local `graph_memory` embedding model if service unavailable.
- Optional: `CHUTES_API_KEY` or `OPENAI_API_KEY` (for categorization).
