---
name: a2a-messages-parts
description: Implement A2A messages and parts — TextPart, FilePart, DataPart, message roles, metadata, and content negotiation. Use when building message construction, parsing, or content type handling in A2A agents.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Messages and Parts

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` for the Message and Part schemas
2. Web-search `site:github.com a2aproject A2A message parts TextPart FilePart DataPart` for schema details
3. Web-search `site:github.com a2aproject a2a-samples message` for message construction examples
4. Fetch SDK docs for message builder classes and part types

## Conceptual Architecture

### What Messages Are

Messages are the **communication units** between agents in A2A. Each message belongs to a task and contains one or more Parts that carry the actual content. Messages have roles indicating direction.

### Message Structure

- **role** — `user` (from client agent) or `agent` (from server agent)
- **parts** — Array of Part objects (the actual content)
- **metadata** — Optional key-value pairs for custom data

### Three Part Types

#### TextPart
Plain text or markdown content.
- **kind**: `"text"`
- **text**: The text content string
- **metadata**: Optional key-value pairs

Use for: Natural language instructions, responses, explanations, formatted output.

#### FilePart
File content, either inline or by reference.
- **kind**: `"file"`
- **file**: Object containing either:
  - **bytes**: Base64-encoded file content + **mimeType**
  - **uri**: URL to the file + optional **mimeType**
- **metadata**: Optional key-value pairs

Use for: Images, documents, code files, generated files, binary data.

#### DataPart
Structured JSON data.
- **kind**: `"data"`
- **data**: Any valid JSON value (object, array, string, number, etc.)
- **metadata**: Optional key-value pairs

Use for: Structured results, API responses, configuration, machine-readable output.

### Content Negotiation

Agents declare supported MIME types in their Agent Card:
- **defaultInputModes** — What the agent can receive
- **defaultOutputModes** — What the agent can produce

Clients can specify preferred output modes in the request:
- **acceptedOutputModes** — MIME types the client wants (in the configuration object)

If there's a mismatch, the server returns error `-32005` (incompatible content types).

### Message Flow in a Task

```
Client message (role: user)    → Server creates/continues task
Server response (role: agent)  → Client processes result
Client follow-up (role: user)  → Server continues task (multi-turn)
Server final (role: agent)     → Task reaches terminal state
```

### Composing Rich Messages

Messages can contain multiple parts of mixed types:
```json
{
  "role": "user",
  "parts": [
    { "kind": "text", "text": "Analyze this image and provide structured results" },
    { "kind": "file", "file": { "uri": "https://example.com/chart.png", "mimeType": "image/png" } }
  ]
}
```

### Best Practices

- Use TextPart for natural language, DataPart for structured data — don't serialize JSON into TextPart
- Include mimeType with FileParts for proper content handling
- Prefer URI-based FileParts over inline bytes for large files
- Validate that message parts match the agent's declared input modes
- Keep metadata lightweight — don't store large payloads there
- For multi-modal interactions, combine TextParts with FileParts in the same message
- Parse all part types when receiving messages — don't assume text-only

Fetch the specification for exact Part schemas, all fields, metadata conventions, and content type handling rules before implementing.
