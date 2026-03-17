---
name: Letta Conversations API
description: Guide for using the Letta Conversations API to manage isolated message threads on agents. Use when building multi-user chat applications, session management, or any scenario requiring separate conversation contexts on a single agent.
---

# Letta Conversations API

The Conversations API allows multiple isolated message threads on a single agent. Each conversation maintains its own message history while sharing the agent's memory blocks and tools.

## When to Use This Skill

- Building multi-user chat applications (each user gets their own conversation)
- Implementing session management with separate contexts
- A/B testing agent responses across isolated conversations
- Any scenario where you need multiple independent chat threads with one agent

## Key Concepts

| Concept | Description |
|---------|-------------|
| **Conversation** | An isolated message thread on an agent (`conv-xxx` ID) |
| **Isolation** | Each conversation has separate message history |
| **Shared State** | Memory blocks and tools are shared across conversations |
| **In-Context Messages** | Messages currently in the conversation's context window |

## Python SDK Usage

### Setup

```python
from letta_client import Letta

client = Letta(base_url="https://api.letta.com", api_key="your-key")
```

### Create a Conversation

```python
conversation = client.conversations.create(agent_id="agent-xxx")
# conversation.id -> "conv-xxx"
```

### Send Messages (Streaming)

```python
stream = client.conversations.messages.create(
    conversation_id=conversation.id,
    messages=[{"role": "user", "content": "Hello!"}],
)

for msg in stream:
    if hasattr(msg, "message_type") and msg.message_type == "assistant_message":
        print(msg.content)
```

### List Messages in a Conversation

```python
messages = client.conversations.messages.list(
    conversation_id=conversation.id,
    limit=50,  # Optional: default 100
    after="message-xxx",  # Optional: cursor for pagination
    before="message-yyy",  # Optional: cursor for pagination
)
```

### List All Conversations for an Agent

```python
conversations = client.conversations.list(
    agent_id="agent-xxx",
    limit=50,  # Optional
    after="conv-xxx",  # Optional: cursor for pagination
)
```

### Retrieve a Specific Conversation

```python
conv = client.conversations.retrieve(conversation_id="conv-xxx")
# conv.in_context_message_ids -> list of message IDs in context window
```

## REST API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/v1/conversations?agent_id=xxx` | Create a conversation |
| `GET` | `/v1/conversations?agent_id=xxx` | List conversations |
| `GET` | `/v1/conversations/{conversation_id}` | Get a conversation |
| `GET` | `/v1/conversations/{conversation_id}/messages` | List messages |
| `POST` | `/v1/conversations/{conversation_id}/messages` | Send message (streams response) |
| `POST` | `/v1/conversations/{conversation_id}/stream` | Resume a background stream |

### REST Example: Create and Send Message

```bash
# Create conversation
curl -X POST "https://api.letta.com/v1/conversations?agent_id=agent-xxx" \
  -H "Authorization: Bearer $LETTA_API_KEY" \
  -H "Content-Type: application/json"

# Send message (streaming response)
curl -X POST "https://api.letta.com/v1/conversations/conv-xxx/messages" \
  -H "Authorization: Bearer $LETTA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{"messages": [{"role": "user", "content": "Hello!"}]}'
```

## Conversation Schema

```python
class Conversation:
    id: str                      # "conv-xxx"
    agent_id: str                # Associated agent ID
    created_at: datetime         # Creation timestamp
    summary: Optional[str]       # Optional conversation summary
    in_context_message_ids: List[str]  # Message IDs in context window
```

## Common Patterns

### Multi-User Chat Application

```python
# Each user gets their own conversation
user_conversations = {}

def get_or_create_conversation(user_id: str, agent_id: str) -> str:
    if user_id not in user_conversations:
        conv = client.conversations.create(agent_id=agent_id)
        user_conversations[user_id] = conv.id
    return user_conversations[user_id]

def send_user_message(user_id: str, agent_id: str, message: str):
    conv_id = get_or_create_conversation(user_id, agent_id)
    return client.conversations.messages.create(
        conversation_id=conv_id,
        messages=[{"role": "user", "content": message}],
    )
```

### Paginating Through Message History

```python
def get_all_messages(conversation_id: str):
    all_messages = []
    after = None
    
    while True:
        batch = client.conversations.messages.list(
            conversation_id=conversation_id,
            limit=100,
            after=after,
        )
        if not batch:
            break
        all_messages.extend(batch)
        after = batch[-1].id
    
    return all_messages
```

## Important Notes

1. **Streaming by default**: The `messages.create` endpoint always streams responses
2. **Shared memory**: Memory block updates in one conversation are visible in all conversations for that agent
3. **Message isolation**: Conversation message history is completely isolated between conversations
4. **Pagination**: Use `after`/`before` cursors for efficient pagination, not offsets

## Example Scripts

This skill includes two example scripts in the `scripts/` directory:

1. **`conversations_demo.py`** - Comprehensive demo showing all API features
   - Basic conversation flow
   - Conversation isolation testing
   - Listing and retrieving conversations
   - Pagination examples
   - Shared memory demonstration

2. **`conversations_cli.py`** - Interactive TUI for managing conversations
   - Create/switch between conversations
   - Send messages with streaming responses
   - View message history
   - Switch between agents

### Running the Examples

```bash
# Run the demo script
LETTA_API_KEY=your-key uv run letta/conversations/scripts/conversations_demo.py

# Run the interactive CLI
LETTA_API_KEY=your-key uv run letta/conversations/scripts/conversations_cli.py

# CLI with specific agent
LETTA_API_KEY=your-key uv run letta/conversations/scripts/conversations_cli.py --agent agent-xxx
```

## SDK Gotchas

- Paginated responses use `.items` to access the list: `client.agents.list().items`
- Auth parameter is `api_key`, not `token`: `Letta(base_url=..., api_key=...)`
- Message streams must be consumed (iterate or `list()`) to complete the request
