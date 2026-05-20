---
name: session-query
description: Query previous pi sessions to retrieve context, decisions, code changes, or other information. Use when you need to look up what happened in a parent session or any other session file.
disable-model-invocation: true
---

# Session Query

Query pi session files to retrieve context from past conversations.

This skill is automatically invoked in handed-off sessions when you need to look up details from the parent session.

## Usage

Use the `session_query` tool:

```
session_query(sessionPath, question)
```

- `sessionPath`: Full path to the session file (provided in the "Parent session:" line)
- `question`: Specific question about that session (e.g., "What files were modified?" or "What approach was chosen?")

## Examples

```
session_query("/path/to/session.jsonl", "What files were modified?")
session_query("/path/to/session.jsonl", "What approach was chosen for authentication?")
session_query("/path/to/session.jsonl", "Summarize the key decisions made")
```

The tool loads the session and uses an LLM to answer your question based on its contents. Ask specific questions for best results.
