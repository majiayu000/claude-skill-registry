---
name: mcp-development
description: "Create, test, and audit MCP (Model Context Protocol) servers, tools, resources, and prompts. Use when building MCP components, writing tool schemas, designing transport layers (stdio/http), or validating MCP servers. Includes prompt-engineered descriptions, Zod validation, authentication patterns, and `test_mcp.sh` for validation. Not for manual tool configuration or non-MCP integrations."
---

# MCP Development

**Skill Location**: This file

## Quick Start

**Create MCP server:** `/toolkit:build:package` → Full structure with SDK setup

**Define tools:** Follow `<tool_schema>` template with JSON Schema validation

**Choose transport:** stdio (local) or http (remote) based on use case

**Validate server:** `scripts/test_mcp.sh` → Quick integration testing

**Why:** MCP provides structured tool definitions with type safety—prevents runtime errors from malformed inputs.

## Navigation

| If you need...          | Read...                                    |
| :---------------------- | :----------------------------------------- |
| Create MCP server       | ## Quick Start → /toolkit:build:package    |
| Define tool schema      | ## Implementation Patterns                 |
| Choose transport        | ## Implementation Patterns                 |
| Context engineering     | `context-engineering` skill                       |
| Authentication patterns | `references/pattern_auth_patterns.md`      |
| Validate server         | See validation section in this file        |
| 2026 syntax features    | `references/pattern_2026_syntax.md`        |
| Plugin integration      | `references/pattern_plugin_integration.md` |

## Critical Reference Loading

**Key Reference**: Authentication patterns in `pattern_auth_patterns.md` contain JSON Schema validation rules critical for runtime stability. Read these patterns in full when implementing authentication—summarization causes validation failures.

## System Requirements

- **MCP SDK**: `@modelcontextprotocol/sdk` (latest via npm/pnpm)
- **TypeScript**: >= 5.0
- **Node.js**: >= 18
- **Validation**: `scripts/test_mcp.sh` (bundled CLI abstraction)
- **Transport**: stdio (local) or http (remote)
- **Schema**: Valid JSON Schema for tool input/output

## Operational Patterns

This skill follows these behavioral patterns:

- **Planning**: Switch to planning mode for architectural decisions
- **Discovery**: Locate files matching patterns and search file contents for MCP integration
- **Delegation**: Delegate planning and exploration to specialized workers
- **Tracking**: Maintain a visible task list for MCP development

<critical_constraint>
Use native tools to fulfill these patterns. The System Prompt selects the correct implementation for semantic directives.
</critical_constraint>

## Implementation Patterns

### Pattern: Tool Definition Template

```json
{
  "name": "tool_name",
  "description": "Tool to <verb> <resource>. Use when <condition>. Constraints: <limits>.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string",
        "description": "Parameter description",
        "enum": ["value1", "value2"],
        "format": "email"
      }
    },
    "required": ["param_name"],
    "additionalProperties": false
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "result": { "type": "string", "description": "Result description" }
    }
  }
}
```

### Pattern: stdio Transport (Local)

```json
{
  "transport": {
    "type": "stdio",
    "command": "node",
    "args": ["server.js"]
  }
}
```

### Pattern: http Transport (Remote)

```json
{
  "transport": {
    "type": "http",
    "url": "http://localhost:3000",
    "authentication": {
      "type": "bearer",
      "token": "${API_TOKEN}"
    }
  }
}
```

### Pattern: Error Message

```
"Invalid input: parameter must be a valid email address. Please provide a valid email like user@example.com."
```

## Troubleshooting

| Issue                      | Symptom              | Solution                                                  |
| -------------------------- | -------------------- | --------------------------------------------------------- |
| Schema validation fails    | Tool calls rejected  | Ensure valid JSON Schema, add descriptions                |
| Agent doesn't use tool     | Poor description     | Use formula: "Tool to X. Use when Y. Constraints: Z."     |
| Missing required fields    | Runtime errors       | Add `required` array in inputSchema                       |
| Wrong parameter type       | Type errors          | Match type in schema (string/number/boolean/array/object) |
| Enum values not recognized | Unexpected behavior  | Use enums for finite value sets                           |
| Transport connection fails | Server not reachable | Verify stdio command or http URL                          |

<mission_control>
<objective>Create portable MCP servers with strict tool schema definitions, clear transport logic, and prompt-engineered descriptions that guide agent behavior</objective>
<success_criteria>Generated MCP server has valid JSON Schema for tools, prompt-engineered descriptions, and proper transport configuration</success_criteria>
<standards_gate>
Before creating MCP servers, review:

- Tool schema & transport → https://code.claude.com/docs/en/mcp.md
- Authentication patterns → `Glob: lookup_auth_patterns.md`
  </standards_gate>
  </mission_control>

<interaction_schema>
design → tool_schema_definition → transport_logic → validation → output</interaction_schema>

MCP (Model Context Protocol) servers provide structured integration between Claude and external systems. They define tools, resources, and prompts that Claude can access through standardized protocols.

**Core principle**: Treat every MCP tool like a tiny, well-written prompt for the agent. The descriptions and schemas you write directly influence how well Claude understands and uses your tools.

---

<pattern name="prompt_engineering_principle">
<principle>Tool descriptions and schemas are prompts to the agent. Write them as if explaining to a new hire—make implicit context explicit.</principle>
</pattern>

## Prompt Engineering for Tool Descriptions

<description_pattern>
<purpose>Structure tool descriptions to maximize agent understanding</purpose>

<template_formula>

**Standard description format:**

```yaml
description: "Brief description, non spoiling of the content. Use when {trigger condition + keywords + key sentences user might say that should lead the tool to be invoked}. Not for {exclusions}."
```

**Alternative formula (MCP-style):**

```
Tool to <verb> <resource>. Use when <trigger condition>. Constraints: <key limits>.
```

<examples>
<example type="simple">

```json
{
  "name": "create_channel",
  "description": "Tool to create a new Slack channel. Use when the user asks to create a new channel, make a new channel, or set up a channel."
}
```

</example>
<example type="with_constraint">

```json
{
  "name": "create_contact",
  "description": "Tool to create a new Salesforce contact. Use when the user wants to create a contact, add a new contact, or input contact data. Required workflow: call discover_required_fields('Contact') first to identify mandatory fields and prevent creation errors. Not for bulk imports."
}
```

</example>
<example type="with_alternative">

```json
{
  "name": "get_calls",
  "description": "Tool to list all calls in a date range. Use when the user asks for calls across a workspace without user/workspace filtering. Constraint: this tool does not support user or workspace filters; for filtered calls, use search_calls_extensive instead. Not for real-time or live call data."
}
```

</example>
</examples>

<structure_rules>

1. **Start with action**: Verb + resource (what the tool does)
2. **Add trigger condition**: Keywords and phrases that activate the tool
3. **Front-load constraints**: Required workflows, hard limits, alternatives
4. **End with exclusions**: "Not for" clause prevents misuse

</structure_rules>

<length_guidance>

- Keep descriptions 1-2 sentences
- Under 1024 characters in practice
- Avoid marketing fluff
- Focus on non-spoiling description

</length_guidance>

</description_pattern>

## Schema-Level Prompt Engineering

<schema_pattern>
<purpose>Use schemas not just for validation, but as prompts to the agent</purpose>

<parameter_level_guidance>

<property_pattern name="enum_preference">

**Use enums instead of free text when:**

- Finite set of values (status: ["pending", "approved", "rejected"])
- Predefined options (unit: ["celsius", "fahrenheit"])
- Boolean-like choices (severity: ["low", "medium", "high", "critical"])

**Why**: Enums remove ambiguity and act as strong constraints at the schema level.

</property_pattern>

<property_pattern name="format_constraints">

**Use format constraints:**

```json
"email": {
  "type": "string",
  "format": "email",
  "description": "User's email address"
}
```

**Common formats**: email, date, date-time, uri, uuid

</property_pattern>

<property_pattern name="conditional_requirements">

**State mutual exclusivity or requirements in descriptions:**

```json
"agent_id": {
  "type": "string",
  "description": "Unique identifier for agent. At least one of agent_id, user_id, app_id, or run_id must be provided."
}
```

</property_pattern>

</parameter_level_guidance>

<output_schema>

**Define outputSchema for complex responses:**

```json
{
  "name": "get_weather",
  "description": "Get weather conditions for a city",
  "inputSchema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "enum": ["New York", "Chicago", "Los Angeles"],
        "description": "Choose city"
      }
    }
  },
  "outputSchema": {
    "type": "object",
    "properties": {
      "temperature": {
        "type": "number",
        "description": "Temperature in Fahrenheit"
      },
      "conditions": { "type": "string", "description": "Weather conditions" },
      "humidity": { "type": "number", "description": "Humidity percentage" }
    }
  }
}
```

**Why**: outputSchema guides the agent about what shape to expect, improving reasoning about downstream tools.

</output_schema>

</schema_pattern>

## When and How to Use Strong Language

<strong_language>
<purpose>Directive language (must, always, never, required) for agent guidance</purpose>

<where_to_use>

<location type="safety">

**Safety and guardrails:**

```json
"description": "Tool to delete a user record. Use only when the user has confirmed deletion and has appropriate permissions. Never allow deletion without explicit user consent."
```

</location>

<location type="preconditions">

**Preconditions and ordering:**

```json
"description": "Tool to create a contact. Required workflow: call discover_required_fields('Contact') first to identify mandatory fields."
```

</location>

<location type="constraints">

**Format and cardinality constraints:**

```json
"title": {
  "type": "string",
  "description": "Title must be between 5 and 120 characters"
}
```

</location>

<location type="error_recovery">

**Error messages for agent recovery:**

```
"Invalid date_range: date_from is after date_to. Please ensure date_from is earlier than date_to and try again."
```

</location>

</where_to_use>

<guidance>

**Use strong language for:**

- Safety requirements (never expose credentials)
- Required workflows (must call X first)
- Non-negotiable constraints (must be <= 100)
- Error recovery instructions

**Avoid overusing strong language for:**

- General behavior descriptions
- Optional features
- Documentation-level details (put these in schema)

**Trade-off**: Too much strong language causes token bloat and over-constraint. Use sparingly where it matters most.

</guidance>

</strong_language>

## Guiding Agents with Errors

<error_guidance>
<purpose>Error messages are micro-prompts that guide agents to self-correct</purpose>

<pattern>

**Error message formula:**

```
<Problem>. <Why>. <Fix>.
```

<examples>

<example type="validation">

```
"Invalid date_from: date_from must be earlier than date_to. Please adjust date_from to a value before date_to and retry."
```

</example>

<example type="missing_inputs">

```
"Missing required parameter: repo_path is required. Please provide the path to the Git repository and retry."
```

</example>

<example type="permissions">

```
"Access denied: token lacks write scope. Ask the user to grant write permissions or use a read-only tool."
```

</example>

<example type="truncation">

```
"Result truncated: returned first 500 of 3,000 rows. To reduce truncation, specify a narrower date range or use filters (user_id, event_type)."
```

</example>

</examples>

<rules>

- Return structured errors with isError flag
- Use natural language, not stack traces
- Include concrete examples of correct parameters
- Suggest recovery actions explicitly

</rules>

</error_guidance>

## Balancing Power vs Complexity

<complexity_management>
<purpose>Achieve maximum capability with minimum cognitive load</purpose>

<per_tool_targets>

- **One clear, atomic action** per tool
- **1-3 required parameters**, small number of optional (total < 6-7)
- **Short descriptions** (1-2 sentences, < 1024 chars)
- **Narrow scope**: Don't create "manage" tools; prefer "create", "delete", "list", "search"

</per_tool_targets>

<per_server_targets>

- **Coherent domain**: Group related tools by service (git*\*, slack*\_, jira\_\_)
- **Small surface**: Each server should do one thing well
- **Consolidate chains**: Merge tools that are almost always called together

</per_server_targets>

<annotations>

**Use MCP annotations for client guidance:**

- `readOnlyHint`: tool doesn't modify state
- `destructiveHint`: may cause destructive changes (triggers confirmations)
- `idempotentHint`: repeating the call is safe

</annotations>

</complexity_management>

## Community Patterns and Examples

<community_examples>
<purpose>Reference patterns from official MCP servers and community implementations</purpose>

<pattern name="naming">

**Consistent snake_case with namespace prefixes:**

```json
{
  "git_status": "Shows working tree status",
  "git_diff_unstaged": "Shows unstaged changes",
  "git_commit": "Records changes to the repository"
}
```

</pattern>

<pattern name="description">

**Concise descriptions following the formula:**

```json
{
  "name": "get_structured_content",
  "description": "Returns structured content along with an output schema for client data validation"
}
```

</pattern>

<pattern name="schema">

**Strong typing with enums and descriptions:**

```json
{
  "location": {
    "type": "string",
    "enum": ["New York", "Chicago", "Los Angeles"],
    "description": "Choose city"
  }
}
```

</pattern>

<pattern name="server_description">

**One dense description for server capability (not individual tools):**

```json
{
  "description": "Integrates with Slack Lists to enable creation, retrieval, filtering, and management of list items with support for bulk operations, data export to JSON/CSV formats"
}
```

</pattern>

</community_examples>

---

<pattern name="tool_schema_enforcement">
<principle>Use `<tool_schema>` tags to ensure generated MCP servers have valid JSON Schema for tool parameters.</principle>
</pattern>

<tool_schema>
<purpose>Strict template for generating valid tool definitions</purpose>

<tool_definition_template>

```json
{
  "name": "{{TOOL_NAME}}",
  "description": "{{PROMPT_ENGINEERED_DESCRIPTION}}",
  "inputSchema": {
    "type": "object",
    "properties": {
      {{PARAMETER_DEFINITIONS}}
    },
    "required": [{{REQUIRED_PARAMS}}],
    "additionalProperties": false
  },
  "outputSchema": {{OUTPUT_SCHEMA}}
}
```

</tool_definition_template>

<parameter_template>

```json
"{{PARAM_NAME}}": {
  "type": "{{PARAM_TYPE}}",
  "description": "{{PARAM_DESCRIPTION}}",
  "enum": [{{ENUM_VALUES}}],
  "format": "{{FORMAT}}",
  "default": "{{DEFAULT_VALUE}}"
}
```

</parameter_template>

<validation_rules>

- Tool names use snake_case with namespace prefix (e.g., `service_action`)
- Descriptions achieve clarity when following: "Tool to <verb> <resource>. Use when <condition>. Constraints: <limits>."
- Valid JSON Schema ensures runtime reliability for inputSchema
- Parameter descriptions prevent misuse by explaining meaning and constraints
- The required field lists all non-optional parameters
- Set additionalProperties to false for strict validation
- Enums improve reliability for finite value sets
- Format constraints (email, date, etc.) add automatic validation

</validation_rules>

<common_types>

- string - Text values
- number - Numeric values (int or float)
- boolean - true/false
- array - Lists of items
- object - Nested structures
- enum - Fixed set of values

</common_types>

<common_formats>

- email - Valid email address
- date - ISO date (YYYY-MM-DD)
- date-time - ISO datetime
- uri - Valid URI
- uuid - Valid UUID

</common_formats>

</tool_schema>

## Transport Logic

<transport_selection>
<purpose>Define when to use stdio vs http transport</purpose>

<transports>
<transport type="stdio">
<use_case>Local development, subprocess communication</use_case>
<advantages>
- Direct Claude integration
- Simple setup
- No network overhead
- Ideal for CLI tools
</advantages>
<disadvantages>
- Single client only
- Local only
</disadvantages>
<example>
```json
{
  "transport": {
    "type": "stdio",
    "command": "node",
    "args": ["server.js"]
  }
}
```
</example>
</transport>

<transport type="http">
<use_case>Remote servers, multi-client scenarios</use_case>
<advantages>
- Multiple clients
- Remote access
- Network transport
- Load balancing
</advantages>
<disadvantages>
- Requires server setup
- Network dependency
- Authentication needed
</disadvantages>
<example>
```json
{
  "transport": {
    "type": "http",
    "url": "http://localhost:3000",
    "authentication": {
      "type": "bearer",
      "token": "${API_TOKEN}"
    }
  }
}
```
</example>
</transport>
</transports>

<selection_criteria>

- Local tool → stdio
- Remote service → http
- Multi-user → http
- Development → stdio
- Production → http
  </selection_criteria>
  </transport_selection>

---

MCP servers provide:

- **Tool definitions**: Structured capabilities Claude can invoke
- **Resource access**: Shared data and context
- **Prompt templates**: Reusable interaction patterns
- **Transport mechanisms**: Communication protocols
- **Portability**: Work across different environments

### MCP Architecture

**Server-Based**: MCPs run as separate servers that Claude connects to

**Three Component Types**:

1. **Tools**: Invocable functions with parameters
2. **Resources**: Data sources and context providers
3. **Prompts**: Template-based interaction patterns

---

## Core Structure

### Server Configuration (McpServer)

<critical_constraint>
**Use McpServer from `@modelcontextprotocol/sdk/server/mcp.js`** (the legacy `Server` is deprecated)
</critical_constraint>

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "mcp-server-name",
  version: "1.0.0",
});

// Tool registration with Zod
server.tool(
  "tool-name",
  "Tool description",
  {
    param: z.string().describe("Parameter description"),
  },
  async ({ param }) => {
    // Implementation
    return { content: [{ type: "text", text: result }] };
  },
);

// Transport connection
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Validation Framework

<critical_constraint>
**Use `scripts/test_mcp.sh` for MCP server validation**—this script abstracts `@modelcontextprotocol/inspector` complexity into a simple CLI.
</critical_constraint>

**Quick validation commands:**

```bash
# Health check (verifies server starts and responds)
scripts/test_mcp.sh Custom_MCP/{project}/dist/server.js health

# List all tools (verify schema and descriptions)
scripts/test_mcp.sh Custom_MCP/{project}/dist/server.js tools

# List resources
scripts/test_mcp.sh Custom_MCP/{project}/dist/server.js resources

# List prompts
scripts/test_mcp.sh Custom_MCP/{project}/dist/server.js prompts

# Call a tool (happy path)
scripts/test_mcp.sh Custom_MCP/{project}/dist/server.js call myTool --arg key=value

# Call with JSON arguments
scripts/test_mcp.sh Custom_MCP/{project}/dist/server.js call myTool --json '{"key": "value"}'

# Run full test suite
scripts/test_mcp.sh Custom_MCP/{project}/dist/server.js all
```

**CI/CD validation with exit codes:**

```bash
#!/bin/bash
set -e

PROJECT="your-project-name"
SERVER_PATH="Custom_MCP/${PROJECT}/dist/server.js"

# Health check (exit 0 = server running)
scripts/test_mcp.sh "$SERVER_PATH" health || exit 1

# List tools (verify definitions)
TOOLS=$(scripts/test_mcp.sh "$SERVER_PATH" tools)
echo "$TOOLS" | jq -e '.tools | length > 0' || exit 1

# Test critical tool
scripts/test_mcp.sh "$SERVER_PATH" call myCriticalTool --arg input="test" || exit 1

echo "MCP server validation: PASS"
```

**For deep spec compliance**, combine with external validators like `mcp-validator`:

```bash
# STDIO compliance test
python -m mcp_testing.scripts.compliance_report \
  --server-command "node Custom_MCP/${PROJECT}/dist/server.js" \
  --protocol-version 2025-06-18
```

---

## Relevance Heuristic

<freshness_gate>
<purpose>Validate URL freshness before trusting documentation</purpose>

<rule>

**Freshness Gate:** Before trusting any code snippets from a URL:

1. Fetch the URL and check for last-updated metadata (Last-Modified header, date in content, or commit history)
2. If content is > 6 months old, search for a more recent version before using the code
3. Prefer recent commits over branch files for SDK documentation
4. Document the freshness check result in the session

</rule>

<exception>

Skip freshness check when:

- Checking npm/GitHub version info (timestamp is the version)
- The URL is clearly versioned (e.g., /v1/, /2026/)
- Official SDK changelog confirms stability

</exception>

<freshness_check>

```bash
# Check GitHub file last commit date
gh api repos/modelcontextprotocol/specification/commits?path=specification.md --jq '.[0].commit.author.date'

# Or fetch and parse for dates
curl -sI https://github.com/modelcontextprotocol/specification | grep -i last-modified
```

</freshness_check>

</freshness_gate>

**Protocol: Check Principles → Freshness Gate → Fetch Instance → Extract Delta → Dispose**

Before fetching MCP specification URLs:

1. **Check Principles** - This skill covers tool schema design, transport selection, error guidance, and prompt engineering. The patterns here are stable.

2. **Freshness Gate** - Verify URL is < 6 months old. If older, search for updated version or use npm package version instead.

3. **Fetch Instance Only When**:
   - MCP SDK version has breaking changes
   - Transport mechanism differs from documented patterns
   - New primitive types not covered
   - Authentication flow has changed

4. **Extract Delta** - Keep only what this skill doesn't cover:
   - SDK-specific initialization changes
   - New transport options
   - Updated security requirements
   - Protocol version differences

5. **Dispose Context** - Remove fetched content after extracting delta

**Delta Pattern**: Fetch the URL, identify current tool-calling syntax, apply directly to the local file. Store patterns, not documentation. Documentation becomes stale; patterns remain actionable.

**When NOT to fetch:**

- Tool description formula (covered in skill)
- Schema patterns (covered with templates)
- Transport selection criteria (covered in tables)
- Error guidance (covered with examples)
- Strong language usage (covered in patterns)

**Official Documentation** (fetch for current MCP syntax):

- Tool schema & transport → https://code.claude.com/docs/en/mcp.md
- Inspector CLI (testing) → https://github.com/modelcontextprotocol/inspector
- MCP Validator (compliance) → https://github.com/Janix-ai/mcp-validator
- Protocol spec → https://modelcontextprotocol.io/
- Best practices → https://modelcontextprotocol.info/docs/best-practices
- SDK docs → https://modelcontextprotocol.io/quickstart/server
- Testing guide → https://www.stainless.com/mcp/how-to-test-mcp-servers

**Workflow:** Freshness check → Verify npm package version → Consult skill patterns → Fetch spec only if behavior differs → Extract delta → Dispose

---

## Dynamic Sourcing Protocol

<fetch_protocol>
**Before creating MCP servers**, fetch current syntax from:

- https://code.claude.com/docs/en/mcp.md (tool schema and transport)

**Note**: For CLI testing, use `scripts/test_mcp.sh` instead of fetching inspector documentation.
</fetch_protocol>

---

## Navigation

**Official Documentation**:

- Tool schema & transport → https://code.claude.com/docs/en/mcp.md
- Inspector CLI (testing) → https://github.com/modelcontextprotocol/inspector
- MCP Validator (compliance) → https://github.com/Janix-ai/mcp-validator
- Protocol spec → https://modelcontextprotocol.io/
- Best practices → https://modelcontextprotocol.info/docs/best-practices
- SDK docs → https://modelcontextprotocol.io/quickstart/server
- Testing guide → https://www.stainless.com/mcp/how-to-test-mcp-servers

| If you need...     | Reference                                 |
| ------------------ | ----------------------------------------- |
| Testing MCP server | `scripts/test_mcp.sh`                     |
| Authentication     | `references/lookup_auth_patterns.md`      |
| Plugin integration | `references/lookup_plugin_integration.md` |
| 2026 features      | `references/lookup_2026_syntax.md`        |

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
All components work with zero CLAUDE.md, CLAUDE.local.md, or .claude/rules/ dependencies (portability invariant).
Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session).
Use What-When-Not-Includes format in descriptions (third person).
Progressive disclosure: SKILL.md contains core philosophy; references/ contains detailed content.
Use XML for control (mission_control, critical_constraint), Markdown for data.
When referencing other skills: use "invoke `skill-name`" or "invoke `skill-name` and read its file". Never cite absolute paths or reference .claude/rules/ from skills.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

## Recognition Questions

| Question | Recognition |
| :------- | :---------- |
| Would Claude know this without being told? | Delete (zero delta) |
| Can this work standalone? | Fix if no (non-self-sufficient) |
| Did I read the actual file, or just see it in grep? | Verify before claiming |

---

## Validation Checklist

Before claiming MCP development complete:

- [ ] Prompt-engineered descriptions used
- [ ] Schema-first design followed
- [ ] Transport layer properly configured
- [ ] Tool schemas validated

---

<guiding_principles>

## The Path to MCP Server Quality

### 1. Prompt-Engineered Descriptions

Tool descriptions achieve optimal agent behavior when written as micro-prompts.

- **Description formula**: "Tool to <verb> <resource>. Use when <condition>. Constraints: <limits>."
- **Front-load constraints**: Place critical requirements and workflows first
- **Conciseness**: 1-2 sentences, under 1024 characters

### 2. Schema-First Design

Valid JSON Schema prevents runtime errors and guides agent behavior.

- **Use `<tool_schema>` template**: Follow the tool definition structure exactly
- **Kebab-case names**: Service_action format improves discoverability
- **Property descriptions**: Explain parameter meaning and constraints
- **Enums over free text**: Finite value sets reduce ambiguity
- **Format constraints**: Add automatic validation (email, date, uri, uuid)

### 3. Transport by Use Case

Choose stdio or http based on deployment requirements.

- **stdio for local**: Single client, direct integration, simpler setup
- **http for remote**: Multiple clients, network transport, load balancing
- **Define clearly**: Transport configuration affects deployment architecture

### 4. Error Messages as Micro-Prompts

Errors guide agents to self-correct when structured properly.

- **Pattern**: "<Problem>. <Why>. <Fix>."
- **Concrete suggestions**: Include examples of correct parameters
- **Recovery actions**: Explicit next steps instead of stack traces

### 5. Portability First

Servers work across environments when configured properly.

- **Environment variables**: Externalize configuration
- **Project-relative paths**: Use `${CLAUDE_PROJECT_DIR}` instead of hardcoding
- **Self-contained dependencies**: Bundle required packages
- **Graceful degradation**: Handle missing configuration safely

### 6. Security by Design

Input validation and sanitization prevent common vulnerabilities.

- **Validate all inputs**: Against schema before processing
- **Sanitize user input**: Prevent injection attacks
- **Parameterized queries**: Use prepared statements for databases
- **Rate limiting**: Prevent abuse and resource exhaustion
- **Mask sensitive data**: Never log credentials or tokens
- **HTTPS only**: Encrypt external communications

### 7. Performance Patterns

Servers remain responsive under load when optimized appropriately.

- **Cache repeated operations**: Use `@lru_cache` or equivalent
- **Paginate large results**: Return data in manageable chunks
- **Batch operations**: Group related calls when possible
- **Set timeouts**: Prevent indefinite waits
  </guiding_principles>

---

<critical_constraint>
**System Physics:**

1. **Skill portability**: The skill must function without CLAUDE.md, CLAUDE.local.md, or .claude/rules/ dependencies (core invariant)
2. **Optional tooling**: External validators (`mcp-validator`, `mcp_testing`) are recommended for deep compliance but not required—the skill provides manual review patterns as fallback
3. Use `McpServer` from `@modelcontextprotocol/sdk/server/mcp.js` (legacy `Server` deprecated)
4. Completion claims require verification evidence
5. Prompt-engineered descriptions required for protocol correctness
   </critical_constraint>

---

## Dynamic Knowledge Loading

This skill uses Blind Navigation for references. Load specialized knowledge ONLY when specific conditions are met:

| Context Condition             | Resource                                 | Action                                     |
| :---------------------------- | :--------------------------------------- | :----------------------------------------- |
| **Testing MCP server**        | `Glob: test_mcp.sh`                      | Execute for validation                     |
| **Authentication patterns**   | `Glob: lookup_auth_patterns.md`          | `Grep` for .env setup and header formats   |
| **Plugin integration**        | `Glob: lookup_plugin_integration.md`     | `Grep` for MCP client patterns             |
| **2026 syntax features**      | `Glob: lookup_2026_syntax.md`            | `Grep` for new primitives                  |
| **Tool schema templates**     | See tool_schema section                  | `Grep` for JSON Schema patterns            |
| **Enforcing tool invocation** | `Glob: lookup_anti_laziness_patterns.md` | `Grep` for confidence rating, CoT patterns |

---

## Dynamic Sourcing

**Syntax Source**: This skill focuses on _patterns_ and _philosophy_. For raw MCP tool schema syntax:

1. **Fetch**: `https://code.claude.com/docs/en/mcp.md`
2. **Extract**: The specific tool schema fields you need
3. **Discard**: Do not retain the fetch in context

---

## Common Mistakes to Avoid

### Mistake 1: Missing additionalProperties

❌ **Wrong:**
```json
"inputSchema": {
  "type": "object",
  "properties": { "param": { "type": "string" } }
}
```

✅ **Correct:**
```json
"inputSchema": {
  "type": "object",
  "properties": { "param": { "type": "string" } },
  "additionalProperties": false
}
```

### Mistake 2: Weak Tool Descriptions

❌ **Wrong:**
```json
"description": "Tool to get data"
```

✅ **Correct:**
```json
"description": "Tool to retrieve user authentication status. Use when checking if a user is logged in or verifying session validity. Not for authentication operations (use auth-tool instead)."
```

### Mistake 3: Missing Required Parameters

❌ **Wrong:**
```json
"inputSchema": {
  "type": "object",
  "properties": { "user_id": { "type": "string" } }
}
```

✅ **Correct:**
```json
"inputSchema": {
  "type": "object",
  "properties": { "user_id": { "type": "string", "description": "The user ID to look up" } },
  "required": ["user_id"],
  "additionalProperties": false
}
```

### Mistake 4: Using Deprecated Server Class

❌ **Wrong:**
```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js"
```

✅ **Correct:**
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"
```

### Mistake 5: Poor Error Messages

❌ **Wrong:**
```
"Invalid input"
```

✅ **Correct:**
```
"Invalid user_id: 'abc123' is not a valid UUID format. Please provide a valid UUID like '550e8400-e29b-41d4-a716-446655440000'."
```

---

## Validation Checklist

Before claiming MCP development complete:

**Tool Schema:**
- [ ] Valid JSON Schema for inputSchema
- [ ] All required parameters listed in `required` array
- [ ] additionalProperties set to false
- [ ] Parameter descriptions explain purpose and constraints

**Tool Description:**
- [ ] Follows formula: "Tool to X. Use when Y. Constraints: Z."
- [ ] Includes trigger conditions
- [ ] Excludes use cases clearly (Not for...)

**Transport:**
- [ ] stdio configured for local tools
- [ ] http configured for remote tools
- [ ] Authentication properly set up

**Server:**
- [ ] Uses McpServer (not deprecated Server class)
- [ ] Tools registered with valid schemas
- [ ] Server properly initialized

**Testing:**
- [ ] test_mcp.sh validation passes
- [ ] Tool calls work correctly
- [ ] Error messages are helpful

---

## Best Practices Summary

✅ **DO:**
- Use `additionalProperties: false` for strict validation
- Write tool descriptions as micro-prompts
- Include all required parameters in schema
- Use enums for finite value sets
- Set format constraints (email, date, etc.)
- Use McpServer from correct import path
- Test with test_mcp.sh before claiming complete

❌ **DON'T:**
- Skip parameter descriptions
- Use loose schemas without additionalProperties
- Write vague tool descriptions
- Forget required array for mandatory params
- Use deprecated Server class
- Skip error message improvement
- Skip validation testing

---

<critical_constraint>
**System Physics:**

1. Zero external dependencies (portability invariant)
2. Use `McpServer` from `@modelcontextprotocol/sdk/server/mcp.js` (legacy `Server` deprecated)
3. Completion claims require verification evidence
4. Prompt-engineered descriptions required for protocol correctness
5. additionalProperties: false required for tool schemas
</critical_constraint>
