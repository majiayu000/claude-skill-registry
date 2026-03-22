---
name: a2a-multi-turn
description: Implement A2A multi-turn conversations — input-required state handling, context preservation, iterative refinement, and human-in-the-loop patterns. Use when building agents that need back-and-forth interaction.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Multi-Turn Conversations

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for multi-turn and input-required handling
2. Web-search `site:github.com a2aproject A2A multi-turn input-required` for multi-turn protocol details
3. Web-search `site:github.com a2aproject a2a-samples multi-turn` for conversation examples
4. Fetch SDK docs for multi-turn task handling patterns

## Conceptual Architecture

### What Multi-Turn Means in A2A

Multi-turn conversations allow agents to have **iterative exchanges** within a single task. The server agent can request more input from the client, creating a back-and-forth dialogue before reaching a final result.

### The input-required State

The key mechanism for multi-turn is the `input-required` task state:

```
Client sends message → Task created (submitted)
Server processes → working
Server needs more info → input-required (with a message explaining what's needed)
Client sends follow-up → working (task continues with same taskId)
Server completes → completed
```

### How It Works

1. **Initial request**: Client sends `message/send` or `message/stream` without `taskId`
2. **Server processes**: May transition to `input-required` if it needs clarification
3. **Server response**: Returns the task with `input-required` state and a message explaining what's needed
4. **Client responds**: Sends another `message/send` with the same `taskId` and the requested information
5. **Server continues**: Resumes processing with the additional context
6. **Repeat or complete**: May request more input or reach a terminal state

### Context Preservation

Within a multi-turn task:
- All messages are associated with the same `taskId`
- The server maintains the full conversation history
- Each new message from the client adds to the context
- The server can reference previous messages when processing

### Patterns

#### Clarification Loop
Agent asks for clarification when the request is ambiguous:
```
User: "Book a flight"
Agent: (input-required) "Where are you flying from and to? What dates?"
User: "NYC to London, March 15-22"
Agent: (input-required) "I found 3 options. Which do you prefer? [options]"
User: "Option 2"
Agent: (completed) "Booked! Confirmation #ABC123"
```

#### Progressive Refinement
Agent produces intermediate results and asks for feedback:
```
User: "Write a blog post about AI"
Agent: (input-required) "Here's an outline. Should I proceed? [outline]"
User: "Looks good, but add a section on safety"
Agent: (completed) "Here's the final post. [content]"
```

#### Human-in-the-Loop
Agent defers to a human for decisions it can't make:
```
User: "Process this insurance claim"
Agent: (input-required) "This claim requires manager approval for amounts over $10,000. Please confirm."
User: "Approved"
Agent: (completed) "Claim processed and approved."
```

#### Data Collection
Agent collects required information step by step:
```
User: "Set up my account"
Agent: (input-required) "What's your email address?"
User: "user@example.com"
Agent: (input-required) "What subscription plan? [Basic/Pro/Enterprise]"
User: "Pro"
Agent: (completed) "Account created with Pro plan."
```

### Server Implementation

The server must:
- Maintain task state across multiple requests
- Store conversation history for context
- Return clear messages when requesting input
- Handle both new tasks and task continuations
- Validate that continued tasks exist and are in the right state

### Client Implementation

The client must:
- Check response task state after each call
- Detect `input-required` and present the agent's message to the user (or auto-respond)
- Send follow-up messages with the same `taskId`
- Handle the possibility of multiple rounds
- Know when to give up (max turns, timeout)

### Best Practices

- Include clear, specific messages when entering `input-required` — the client needs to know what to provide
- Set maximum turn limits to prevent infinite loops
- Preserve full context across turns — don't lose earlier parts of the conversation
- Use DataPart for structured input requests (e.g., forms, multiple-choice)
- Consider timeouts for tasks waiting in `input-required` state
- Log all turns for debugging multi-turn flows
- Handle the case where the client never responds (timeout → canceled or failed)

Fetch the specification for exact multi-turn handling rules, message continuation semantics, and state transition constraints before implementing.
