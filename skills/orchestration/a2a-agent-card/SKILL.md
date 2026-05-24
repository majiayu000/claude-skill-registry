---
name: a2a-agent-card
description: Create and configure A2A Agent Cards — the discovery document describing an agent's capabilities, skills, authentication, and endpoint. Use when defining what your agent exposes to other agents.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch
---

# A2A Agent Card

## Before writing code

**Fetch live docs**:
1. Fetch `https://a2a-protocol.org/latest/specification/` and look for the Agent Card schema section
2. Web-search `site:github.com a2aproject A2A agent card schema` for the JSON Schema definition
3. Web-search `site:github.com a2aproject a2a-samples agent-card` for real-world Agent Card examples
4. Fetch SDK docs for Agent Card builder/helper classes

## Conceptual Architecture

### What the Agent Card Is

The Agent Card is a JSON document that describes an A2A agent to potential clients. It's the **discovery and capability advertisement mechanism** — analogous to an OpenAPI spec for REST APIs, but for agent-to-agent communication.

### Hosting

By convention, Agent Cards are served at:
```
{agent_base_url}/.well-known/agent-card.json
```

Agents can also be discovered via:
- Agent registries (centralized directories)
- Direct configuration (hard-coded URLs)
- Referral from other agents

### Key Sections

#### Identity
- **name** — Human-readable name
- **description** — What the agent does
- **url** — The agent's A2A endpoint (where JSON-RPC requests go)
- **version** — Semantic version of the agent
- **protocolVersion** — The A2A protocol version the agent supports (required)
- **provider** — Optional organization/owner information

#### Capabilities
Declares what protocol features the agent supports:
- **streaming** — Can the agent handle `message/stream`?
- **pushNotifications** — Can the agent send push notifications?
- **stateTransitionHistory** — Does the agent maintain full task state history?

#### Skills
Array of skills (capabilities) the agent offers:
- **id** — Unique skill identifier
- **name** — Human-readable skill name
- **description** — What the skill does
- **tags** — Categorization tags
- **examples** — Example inputs/prompts for this skill

Skills help client agents understand what tasks they can delegate.

#### Authentication
Declares required authentication via two top-level fields:
- **securitySchemes** — A map/object of named security scheme definitions (e.g., `apiKey`, `http` with `scheme: bearer`, `oauth2`, `openIdConnect`)
- **security** — An array of required scheme references (e.g., `[{ "schemeName": [] }]`)
- Each scheme has type-specific configuration (header name, OAuth URLs, OIDC discovery URL, etc.)

#### Input/Output Modes
- **defaultInputModes** — MIME types the agent accepts (e.g., `text/plain`, `application/json`, `image/png`)
- **defaultOutputModes** — MIME types the agent can produce

### Agent Card Design Principles

- **Be specific in descriptions** — Other agents (LLMs) will read this to decide whether to delegate tasks
- **Skills should be granular** — Each skill represents one capability, not the entire agent
- **Examples are critical** — They help client agents understand how to formulate requests
- **Declare all required auth** — Clients need to know upfront what credentials they need
- **Version meaningfully** — Update version when skills or capabilities change

### Use Cases

- Public-facing agent discovery (web-crawlable Agent Cards)
- Internal agent registry for enterprise multi-agent systems
- Marketplace listings where agents advertise their skills
- Framework integration points (ADK, LangGraph, CrewAI read Agent Cards)

### Best Practices

- Validate the Agent Card against the official JSON Schema
- Serve with appropriate CORS headers if agents run in browsers
- Include meaningful tags for skill categorization and search
- Keep descriptions concise but informative — they're read by LLMs
- Test that `/.well-known/agent-card.json` is accessible from client agents
- Update the Agent Card when adding/removing skills or changing capabilities

Fetch the specification for the exact Agent Card JSON Schema, all field types, and required vs optional fields before implementing.
