---
name: agent-protocol
description: Defines and validates standard communication protocols between agents (A2A).
context_cost: low
---
# Agent Protocol Skill

## Triggers
- protocol
- handshake
- ipc
- agent-messaging
- a2a

## Purpose
To establish standard interfaces for agents to communicate, ensuring reliable data exchange and preventing format hallucinations.

## Instructions
When defining how agents talk to each other:

1.  **Define the Schema**: Use JSON Schema to define the structure of messages.
    -   `type`: (request, response, event, error)
    -   `payload`: The actual data content.
    -   `meta`: Timestamp, sender_id, correlation_id.
2.  **Establish the Handshake**:
    -   **Ping/Pong**: Verify availability.
    -   **Capability Query**: "What tools do you have?" -> "I have [tool_a, tool_b]".
3.  **Standardize Error Handling**:
    -   Define standard error codes (e.g., `AGENT_BUSY`, `INVALID_INPUT`, `CONTEXT_OVERFLOW`).
    -   Define retry policies (exponential backoff).
4.  **Documentation**:
    -   Write the protocol definition to a shared `contracts/` directory or a markdown file.

## Example Protocol (JSON)
```json
{
  "protocol": "v1",
  "type": "task_request",
  "id": "uuid-1234",
  "sender": "orchestrator",
  "recipient": "coder_agent",
  "payload": {
    "task": "Implement login function",
    "context": "User needs email/password auth...",
    "constraints": ["Use bcrypt", "No external auth providers"]
  }
}
```

## Best Practices
-   **Strict Typing**: Always validate payloads against the schema.
-   **Idempotency**: Ensure task requests can be retried without side effects if possible.
-   **Async First**: assume communication is asynchronous; use correlation IDs to match requests and responses.
