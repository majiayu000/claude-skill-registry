---
name: readwise-chat
description: Chat with Readwise highlights using GPT-5.1 RAG. Use when the user wants to ask questions about their reading library, get summaries across documents, or have a conversation about their highlights. Triggers on "ask readwise", "chat about my highlights", "what do my notes say about", "summarize my reading on".
context: fork
agent: librarian
user-invocable: false
---

# Readwise Chat (RAG over Highlights)

Uses GPT-5.1 to answer questions with RAG over the user's full highlight library via WebSocket streaming.

## Prerequisites

Chat requires session cookies (not API token). Check if configured:

```bash
grep SESSION_COOKIES ~/.readwise/env
```

If missing, run:

```bash
readwise-custom auth session
```

This launches Chrome, navigates to readwise.io/chat, and extracts httpOnly session cookies via CDP.

## Commands

### One-Shot Query

Streams the response to stdout as it arrives:

```bash
readwise-custom chat "What are my highlights about fiduciary duty?"
readwise-custom chat "Summarize my notes on proxy advisors"
readwise-custom chat "Compare what I've read about SEC regulation vs FINRA"
```

With JSON output (includes related highlights):

```bash
readwise-custom chat "What do my highlights say about broker-dealer regulation?" --json
```

### Interactive REPL

Multi-turn conversation with context preserved:

```bash
readwise-custom chat-interactive
readwise-custom chat-interactive --model 5.1-thinking  # reasoning model
```

Type `exit` to quit.

### Conversation Management

```bash
readwise-custom chat-list                           # List all conversations
readwise-custom chat-get <id>                       # Get conversation with messages
readwise-custom chat-delete <id>                    # Delete conversation
readwise-custom chat-rename <id> "Better Title"     # Rename conversation
```

## Model Options

| Model ID | Name | Use Case |
|----------|------|----------|
| `5.1` | Fast (default) | Quick answers, simple lookups |
| `5.1-thinking` | Thinking | Complex synthesis, reasoning |

## Chat vs Search

| Feature | `readwise-custom chat` | `readwise readwise-search-highlights` |
|---------|-----------------|-------------------|
| Returns | Synthesized answer + highlights | Raw highlight matches |
| Model | GPT-5.1 RAG | Vector similarity |
| Auth | Session cookies | API token |
| Speed | ~3-10s (streaming) | ~2s |
| Highlights returned | Up to 69 | Top-N vector matches |
| Multi-turn | Yes (interactive) | No |

**Use chat when:** You want a synthesized answer, cross-document analysis, or conversational exploration.

**Use search when:** You want raw highlight matches, exact quotes, or structured data for further processing.
