---
name: documenting-tools
description: "Use when writing MCP tools, API endpoints, CLI commands, or any function that an LLM will invoke. Also use when LLMs misuse tools due to poor descriptions. Triggers: 'document this tool', 'write tool docs', 'MCP tool', 'tool description quality', 'model keeps calling this wrong', 'improve tool description'. For human-facing API docs, standard documentation practices apply instead."
version: 1.0.0
---

# Documenting Tools

<ROLE>
Tool Documentation Specialist. Your reputation depends on documentation that enables LLMs to use tools correctly without guessing. Ambiguous tool docs cause runtime errors, incorrect parameter values, and wasted tokens on retries.
</ROLE>

<CRITICAL>
Anthropic's "Building Effective Agents" guide states: "Spend as much effort on tool definitions as you do on prompts."

Tool documentation is not an afterthought. It is a first-class engineering artifact.
</CRITICAL>

## Invariant Principles

1. **Models read tool descriptions** to decide when and how to use tools
2. **Ambiguity causes errors**: If a parameter could mean two things, the model will guess wrong
3. **Edge cases must be documented**: Undocumented error states cause unrecoverable failures
4. **Examples prevent misuse**: One good example is worth ten paragraphs of description

## Reasoning Schema

<analysis>
Before documenting a tool, identify:
- What type of tool is this? (MCP, API, CLI, function)
- What does it do in one sentence?
- What are all the parameters?
- What errors can occur?
</analysis>

<reflection>
After documenting, verify:
- Can someone who's never seen this tool understand when to use it?
- Are ALL parameters documented with types?
- Are ALL error cases documented?
- Is there at least one example?
</reflection>

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `tool_type` | Yes | MCP tool, REST API, CLI command, function |
| `tool_code` | Yes | Implementation or signature to document |
| `existing_docs` | No | Current documentation to improve |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `tool_documentation` | Inline/JSON | Complete tool documentation |
| `quality_assessment` | Inline | Checklist verification |

---

## Documentation Checklist

For every tool, document ALL of these:

| Element | Required | Description |
|---------|----------|-------------|
| **Purpose** | Yes | What the tool does in one sentence |
| **When to use** | Yes | Conditions that make this tool appropriate |
| **When NOT to use** | Recommended | Common misuse cases, similar tools to use instead |
| **Parameters** | Yes | Each parameter with type, constraints, examples |
| **Return value** | Yes | What the tool returns on success |
| **Error cases** | Yes | What errors can occur and what they mean |
| **Side effects** | If any | What state changes the tool causes |
| **Examples** | Recommended | 1-2 usage examples |

---

## Parameter Documentation Format

For each parameter:

```
name (type, required/optional): Description.
  - Constraints: [valid ranges, formats, patterns]
  - Default: [if optional]
  - Example: [concrete value]
```

**Good:**
```
path (string, required): Path to the file to read.
  - Can be absolute (/Users/...) or relative to cwd (./src/...)
  - Must not contain null bytes
  - Example: "/Users/alice/project/README.md"
```

**Bad:**
```
path: The file path
```

---

## Error Documentation

Document what happens for each error condition:

| Error Case | Document |
|-----------|----------|
| Empty/null input | What happens if required field is empty? |
| Invalid type | What if wrong type passed? |
| Out of bounds | What if index exceeds array length? |
| Missing resource | What if file/URL/ID doesn't exist? |
| Permission denied | What if access is restricted? |
| Timeout | What if operation takes too long? |
| Rate limit | What if quota exceeded? |

Format:
```
errors: [
  "ERROR_CODE: Human-readable explanation of when this occurs"
]
```

---

## MCP Tool Schema

```json
{
  "name": "tool_name",
  "description": "What the tool does. When to use it. When NOT to use it (use X instead).",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string",
        "description": "What this parameter controls. Constraints. Example value."
      }
    },
    "required": ["param_name"]
  }
}
```

---

## Anti-Patterns

<FORBIDDEN>
- One-word descriptions ("Reads file", "Makes request")
- Missing parameter types or constraints
- No error documentation
- No examples
- Assuming the model knows your conventions
- Documenting only the happy path
- "See code for details" (the model can't see your code)
- Inconsistent terminology (file/path/filepath used interchangeably)
</FORBIDDEN>

---

## Good vs Bad Examples

### File Reading Tool

**Bad:**
```json
{
  "name": "read_file",
  "description": "Reads a file"
}
```

**Good:**
```json
{
  "name": "read_file",
  "description": "Reads file contents as UTF-8 string. Use for text files. Fails on binary files (use read_file_binary). Fails if file doesn't exist.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "File path. Absolute (/Users/...) or relative to cwd (./src/...). Example: '/Users/alice/README.md'"
      }
    },
    "required": ["path"]
  },
  "errors": [
    "FILE_NOT_FOUND: Path does not exist",
    "PERMISSION_DENIED: Cannot read file",
    "BINARY_FILE: File is binary, use read_file_binary"
  ]
}
```

### API Request Tool

**Bad:**
```json
{
  "name": "api_request",
  "description": "Makes an API request"
}
```

**Good:**
```json
{
  "name": "api_request",
  "description": "HTTP request to external API. Use for REST APIs. NOT for internal services (use internal_rpc). Auto-retries 5xx errors 3x.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "method": {
        "type": "string",
        "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "description": "HTTP method"
      },
      "url": {
        "type": "string",
        "description": "Full URL with protocol. Must be HTTPS for external APIs. Example: 'https://api.github.com/repos/owner/repo'"
      },
      "body": {
        "type": "object",
        "description": "Request body for POST/PUT/PATCH. Auto-serialized to JSON."
      },
      "timeout_ms": {
        "type": "number",
        "description": "Timeout in milliseconds. Default: 30000"
      }
    },
    "required": ["method", "url"]
  },
  "errors": [
    "TIMEOUT: Exceeded timeout_ms",
    "NETWORK_ERROR: Could not connect",
    "INVALID_URL: Malformed URL or disallowed protocol",
    "AUTH_REQUIRED: 401 returned, check credentials"
  ],
  "sideEffects": "POST/PUT/DELETE/PATCH may modify remote state"
}
```

---

## Self-Check

Before completing tool documentation:

- [ ] Purpose is one clear sentence (not "does stuff")
- [ ] "When to use" conditions specified
- [ ] "When NOT to use" specified for commonly confused tools
- [ ] ALL parameters have type, description, constraints
- [ ] At least one example value per parameter
- [ ] ALL error cases documented with codes and explanations
- [ ] Side effects stated if any
- [ ] At least one usage example
- [ ] Terminology is consistent throughout

If ANY unchecked: improve documentation before shipping.

<FINAL_EMPHASIS>
Tool documentation is the interface contract between you and every LLM that will use your tool. Ambiguity in that contract means the LLM will guess. Guessing means errors. Clear documentation means correct tool usage on the first try. Write for the model that has never seen your codebase.
</FINAL_EMPHASIS>
