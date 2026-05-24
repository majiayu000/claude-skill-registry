---
name: swarmkit-dev
description: |
  SwarmKit SDK development for TypeScript and Python. Use when building applications with SwarmKit to run AI agents (Claude, Codex, Gemini, Qwen) in secure sandboxes. Triggers: (1) Creating SwarmKit applications, (2) Configuring agents with skills, Composio, MCP servers, (3) Using Swarm abstractions (map, filter, reduce, best_of), (4) Building Pipelines, (5) Structured output with schemas, (6) Session management, streaming, observability. Covers both TypeScript (@swarmkit/sdk) and Python (swarmkit) SDKs.
---

# SwarmKit SDK

Run terminal-based AI agents in secure sandboxes with built-in observability.

> **Repo:** https://github.com/brandomagnani/swarmkit — cookbooks in `cookbooks/`, skills in `skills/`

## SDK Choice

| Language | Package | Syntax Reference |
|----------|---------|------------------|
| TypeScript | `@swarmkit/sdk` | [references/typescript.md](references/typescript.md) |
| Python | `swarmkit` | [references/python.md](references/python.md) |

Both SDKs are functionally identical. Choose based on application language.

## Quick Start

```bash
# TypeScript
npm install @swarmkit/sdk

# Python
pip install swarmkit
```

## Core Concepts

### 1. SwarmKit (Single Agent)

For single-agent tasks with multi-turn conversations.

```
SwarmKit → run() → getOutputFiles()
```

**Key capabilities:**
- Agent configuration (type, model, reasoning effort)
- Skills (pdf, docx, pptx, etc.)
- Composio integrations (GitHub, Gmail, Slack, etc.)
- MCP servers for custom tools
- Structured output via schema
- Context/files upload, session management

### 2. Swarm (Parallel Agents)

For parallel processing with functional abstractions.

| Operation | Type | Description |
|-----------|------|-------------|
| `map` | transform | Process items in parallel → outputs |
| `filter` | gate | Evaluate items, condition decides pass/fail |
| `reduce` | synthesize | Many items → single output |
| `best_of` | select | N candidates → judge picks winner |

**When to use:**
- `map`: Batch processing (analyze 100 docs)
- `filter`: Quality gates (keep only critical items)
- `reduce`: Synthesis (combine into report)
- `best_of`: Quality (run 3 agents, pick best)

### 3. Pipeline (Chained Operations)

**Preferred API for most workflows.** Fluent, readable, reusable.

```
Pipeline → .map() → .filter() → .reduce() → .run()
```

Reusable across different data batches.

**Pipeline vs standalone Swarm calls:**
- Use **Pipeline** for chains (map → filter → reduce) - cleaner API
- Use **Swarm.bestOf()** only for standalone best-of-N on single item (not available as pipeline step)

**Pipeline restrictions:**
- `best_of` only available as option within `.map({ bestOf })`, not as standalone step
- `.reduce()` is terminal - no steps after

## Authentication

API keys auto-resolve from environment variables.

| Mode | Setup | Included |
|------|-------|----------|
| Gateway | `SWARMKIT_API_KEY` | E2B, browser-use, tracing |
| BYOK | Provider key + `E2B_API_KEY` | Direct provider access |
| Claude Max | `CLAUDE_CODE_OAUTH_TOKEN` + `E2B_API_KEY` | Use existing subscription |

> **Note:** In Gateway mode, `SWARMKIT_API_KEY` is automatically injected into this sandbox by the parent SwarmKit process. The SDK picks it up from the environment—no manual configuration needed.

### Gateway Mode

```bash
# .env
SWARMKIT_API_KEY=sk-...
```

```
SwarmKit().withAgent({ type: "claude", apiKey: SWARMKIT_API_KEY })
```

**Included:** E2B sandbox auto-provisioned, `browser-use` integrated, tracing at dashboard.evolvingmachines.ai

### BYOK Mode

```bash
# .env
ANTHROPIC_API_KEY=sk-...   # or OPENAI_API_KEY, GEMINI_API_KEY
E2B_API_KEY=e2b_...
```

```
sandbox = E2BProvider({ apiKey: E2B_API_KEY })
SwarmKit().withAgent({ type: "claude", providerApiKey: ANTHROPIC_API_KEY }).withSandbox(sandbox)
```

### Claude Max (OAuth)

```bash
claude --setup-token  # Run in terminal → receive token
```

```bash
# .env
CLAUDE_CODE_OAUTH_TOKEN=sk-ant-...
E2B_API_KEY=e2b_...
```

```
SwarmKit().withAgent({ type: "claude", oauthToken: CLAUDE_CODE_OAUTH_TOKEN }).withSandbox(sandbox)
```

**Full docs:** See [references/typescript.md](references/typescript.md) or [references/python.md](references/python.md)

**BYOK Mode**: Set provider env vars (see Agent Types table) + `E2B_API_KEY`.

## Agent Types

| Type | Models | Default | Env Var |
|------|--------|---------|---------|
| `"claude"` | `"opus"` `"sonnet"` `"haiku"` | `"opus"` | `ANTHROPIC_API_KEY` |
| `"codex"` | `"gpt-5.2"` `"gpt-5.2-codex"` | `"gpt-5.2"` | `OPENAI_API_KEY` |
| `"gemini"` | `"gemini-3-pro-preview"` `"gemini-3-flash-preview"` | `"gemini-3-flash-preview"` | `GEMINI_API_KEY` |
| `"qwen"` | `"qwen3-coder-plus"` | `"qwen3-coder-plus"` | `OPENAI_API_KEY` |

## Workspace Structure

Agents run in sandboxes with this filesystem:

```
/home/user/workspace/
├── context/     # Input files (read-only)
├── scripts/     # Agent code
├── temp/        # Scratch space
└── output/      # Final deliverables
```

## Structured Output

Provide a schema (Zod/JSON Schema for TS, Pydantic/dict for Python) and the agent writes `output/result.json`.

```
withSchema(schema) → run() → getOutputFiles() → { files, data, error }
```

## Key Patterns

### Skills + Composio + MCP hierarchy

```
.withSkills([...])           # Agent capabilities (browser-use included by default with Gateway)
.withComposio(userId, {...}) # 1000+ integrations
.withMcpServers({...})       # Custom tools (advanced)
```

> **Note:** With `SWARMKIT_API_KEY`, browser-use is already integrated. Additional browser skills (dev-browser, agent-browser) are optional.

### Streaming Events

| Event | Description |
|-------|-------------|
| `content` | Parsed events (recommended) |
| `stdout` | Raw JSONL output |
| `stderr` | Error output |

Content events: `agent_message_chunk`, `agent_thought_chunk`, `tool_call`, `tool_call_update`, `plan`

### Session Management

```
run() → run() → run()     # Same session, maintains history
getSession() → save       # Persist session ID
setSession(id) → run()    # Reconnect later
pause() / resume()        # Suspend/reactivate billing
kill()                    # Destroy sandbox
```

## Swarm Operations Detail

### Input: FileMap

```
FileMap = { "path": content }  # path in context/, content is string or bytes
```

Items can be: single file, multiple files, or entire folders per worker.

### Result Types

**SwarmResult** (from map, filter, best_of):
- `status`: 'success' | 'filtered' | 'error'
- `data`: Parsed schema or null
- `files`: Output files
- `meta`: Operation metadata

**SwarmResultList** (from map, filter):
- `.success` / `.filtered` / `.error` accessors

**ReduceResult** (from reduce):
- Single result with `data`, `files`, `meta`

### Chaining

When chaining, `result.json` from previous step → `data.json` in next step's context.

### Quality Options

**verify**: LLM-as-judge verifies output, retries with feedback
```
verify: { criteria: "...", maxAttempts: 3 }
```

**bestOf**: Run N candidates, judge picks best
```
bestOf: { n: 3, judgeCriteria: "..." }
```

**retry**: Auto-retry on error with backoff
```
retry: { maxAttempts: 3, backoffMs: 1000 }
```

## Language-Specific Syntax

For complete syntax and examples:
- TypeScript: [references/typescript.md](references/typescript.md)
- Python: [references/python.md](references/python.md)
