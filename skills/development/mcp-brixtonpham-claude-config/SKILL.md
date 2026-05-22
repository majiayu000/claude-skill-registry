---
name: mcp
description: "Model Context Protocol (MCP) server development and tool management. Languages: Python, TypeScript. Capabilities: build MCP servers, integrate external APIs, discover/execute MCP tools, manage multi-server configs, design agent-centric tools. Actions: create, build, integrate, discover, execute, configure MCP servers/tools. Keywords: MCP, Model Context Protocol, MCP server, MCP tool, stdio transport, SSE transport, tool discovery, resource provider, prompt template, external API integration, Gemini CLI MCP, Claude MCP, agent tools, tool execution, server config. Use when: building MCP servers, integrating external APIs as MCP tools, discovering available MCP tools, executing MCP capabilities, configuring multi-server setups, designing tools for AI agents."
license: Complete terms in LICENSE.txt
---

# MCP: Build & Manage Protocol Servers

Build MCP servers that integrate APIs, and execute tools from configured servers.

## When to Use

**Building**: Create MCP servers (Python/TypeScript), integrate APIs, design agent-centric tools, implement validation/error handling, create evaluations

**Managing**: Discover/execute tools via Gemini CLI, filter tools for tasks, manage multi-server configs

## Core Concepts

MCP = standardized protocol for AI agents to access external tools/data.

**Components**: Tools (executable functions), Resources (read-only data), Prompts (templates)
**Transports**: Stdio (local), HTTP (remote), SSE (real-time)

**Load**: `references/protocol-basics.md` for full protocol details

---

## Part 1: Building MCP Servers

Build high-quality MCP servers that enable LLMs to accomplish real-world tasks.

### Development Workflow

**Phase 1: Research & Planning**
1. Study agent-centric design principles (workflows over endpoints)
2. Research target API documentation exhaustively
3. Load framework documentation (Python SDK or TypeScript SDK)
4. Plan tool selection, shared utilities, input/output design, error handling

**Phase 2: Implementation**
1. Set up project structure (single file for Python, full structure for TypeScript)
2. Implement core infrastructure (API clients, error handlers, formatters)
3. Register tools with proper schemas and annotations
4. Follow language-specific best practices

**Phase 3: Testing & Quality**
1. Code quality review (DRY, composability, consistency)
2. Run builds and syntax checks
3. Use quality checklists

**Phase 4: Evaluation**
1. Create 10 complex, realistic evaluation questions
2. Questions must be read-only, independent, and verifiable
3. Test LLM's ability to use your server effectively

**Reference**: `references/building-servers.md` - Load for complete development guide with:
- Agent-centric design principles
- Python (FastMCP) implementation guide with Pydantic models
- TypeScript (MCP SDK) implementation guide with Zod schemas
- Tool naming conventions, response formats, pagination patterns
- Character limits, error handling, security best practices
- Complete working examples and quality checklists
- Evaluation creation and testing methodology

### Key Best Practices

**Tool Design**:
- Use service-prefixed names (`slack_send_message`, not `send_message`)
- Support both JSON and Markdown response formats
- Implement pagination with `limit`, `offset`, `has_more`
- Set CHARACTER_LIMIT constant (typically 25,000)
- Provide actionable error messages that guide agents

**Code Quality**:
- Extract common functionality into reusable functions
- Use async/await for all I/O operations
- Type hints (Python) or strict TypeScript throughout
- Comprehensive docstrings with explicit schemas

**Reference**: `references/best-practices.md` - Load for comprehensive guidelines

---

## Part 2: Using MCP Tools

Execute and manage tools from configured MCP servers efficiently.

### Configuration

MCP servers configured in `.claude/.mcp.json`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {"API_KEY": "${ENV_VAR}"}
    }
  }
}
```

**Gemini CLI Integration**: Create symlink for shared config:
```bash
mkdir -p .gemini && ln -sf .claude/.mcp.json .gemini/settings.json
```

**Reference**: `references/using-tools.md` - Load for complete configuration and usage guide

### Execution Methods (Priority Order)

**1. Gemini CLI (Primary)**

Automatic tool discovery and execution via natural language.

```bash
# CRITICAL: Use stdin piping, NOT -p flag (deprecated, skips MCP init)
echo "Take a screenshot of https://example.com" | gemini -y -m gemini-2.5-flash
```

**Benefits**:
- Automatic tool discovery and selection
- Structured JSON responses (if `GEMINI.md` configured)
- Fastest execution
- No manual tool specification needed

**GEMINI.md Response Format**: Place in project root to enforce JSON-only responses:
```markdown
# Gemini CLI Instructions
Always respond in this exact JSON format:
{"server":"name","tool":"name","success":true,"result":<data>,"error":null}
Maximum 500 characters. No markdown, no explanations.
```

**2. Direct CLI Scripts (Secondary)**

Manual tool specification when you know exact server/tool needed:

```bash
npx tsx scripts/cli.ts call-tool memory create_entities '{"entities":[...]}'
```

**3. mcp-manager Subagent (Fallback)**

Delegate to subagent when Gemini unavailable or for complex multi-tool workflows.

**Reference**: `references/using-tools.md` - Load for:
- Complete Gemini CLI guide with examples
- Direct script usage and options
- Subagent delegation patterns
- Tool discovery and filtering strategies
- Multi-server orchestration
- Troubleshooting and debugging

### Tool Discovery

List available tools to understand capabilities:

```bash
# Saves to assets/tools.json for offline reference
npx tsx scripts/cli.ts list-tools

# List prompts and resources
npx tsx scripts/cli.ts list-prompts
npx tsx scripts/cli.ts list-resources
```

**Intelligent Selection**: LLM reads `assets/tools.json` directly for context-aware tool filtering (better than keyword matching).

---

## Quick Start Examples

### Building a Server

**Python**:
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP("github_mcp")

class SearchInput(BaseModel):
    query: str = Field(..., min_length=2, max_length=200)
    limit: int = Field(default=20, ge=1, le=100)

@mcp.tool(name="github_search_repos", annotations={"readOnlyHint": True})
async def search_repos(params: SearchInput) -> str:
    # Implementation
    pass

if __name__ == "__main__":
    mcp.run()
```

**TypeScript**:
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({name: "github-mcp-server", version: "1.0.0"});

const SearchSchema = z.object({
  query: z.string().min(2).max(200),
  limit: z.number().int().min(1).max(100).default(20)
}).strict();

server.registerTool("github_search_repos", {
  description: "Search GitHub repositories",
  inputSchema: SearchSchema,
  annotations: {readOnlyHint: true}
}, async (params) => {
  // Implementation
});
```

**Load** `references/building-servers.md` for complete implementation guides.

### Using Tools

**Gemini CLI**:
```bash
# IMPORTANT: Use stdin piping, NOT -p flag
echo "Search GitHub for MCP servers and summarize top 3" | gemini -y -m gemini-2.5-flash
```

**Direct Script**:
```bash
npx tsx scripts/cli.ts call-tool github search_repos '{"query":"mcp","limit":3}'
```

**Load** `references/using-tools.md` for complete usage patterns.

---

## Reference Files

Load these as needed during your work:

### Core References
- **`references/building-servers.md`** - Complete MCP server development guide
  - Agent-centric design principles
  - Python (FastMCP) and TypeScript (MCP SDK) implementation
  - Tool patterns, response formats, pagination, error handling
  - Complete examples and quality checklists
  - Evaluation creation methodology

- **`references/using-tools.md`** - Complete MCP tool execution guide
  - Gemini CLI integration and configuration
  - Direct script execution patterns
  - Subagent delegation strategies
  - Tool discovery and filtering
  - Multi-server orchestration

- **`references/best-practices.md`** - Universal MCP guidelines
  - Server and tool naming conventions
  - Response format standards (JSON vs Markdown)
  - Pagination, character limits, truncation
  - Security and privacy considerations
  - Testing and compliance requirements

### Supporting References
- **`references/protocol-basics.md`** - JSON-RPC protocol details
- **`references/python-guide.md`** - Python/FastMCP specifics (Pydantic models, async patterns)
- **`references/typescript-guide.md`** - TypeScript/Zod specifics (strict types, project structure)
- **`references/evaluation-guide.md`** - Creating effective MCP server evaluations

---

## Progressive Disclosure

This SKILL.md provides high-level overview. Load reference files when:

**Building Servers**:
- Starting implementation → Load `references/building-servers.md`
- Need language-specific details → Load `references/python-guide.md` or `references/typescript-guide.md`
- Creating evaluations → Load `references/evaluation-guide.md`

**Using Tools**:
- Setting up Gemini CLI → Load `references/using-tools.md`
- Debugging tool execution → Load `references/using-tools.md`
- Multi-server configuration → Load `references/using-tools.md`

**Best Practices**:
- Reviewing standards → Load `references/best-practices.md`
- Security considerations → Load `references/best-practices.md`

---

## Integration Patterns

**Build + Use**: Create MCP server, then test with Gemini CLI
**Multi-Server**: Configure multiple servers, orchestrate via Gemini CLI
**Evaluation-Driven**: Build server, create evaluations, iterate based on LLM feedback

---

## Boundaries

**Will**:
- Guide MCP server development in Python or TypeScript
- Provide tool execution strategies via Gemini CLI or scripts
- Ensure best practices for agent-centric design
- Help create effective evaluations
- Configure multi-server setups

**Will Not**:
- Run long-running server processes in main thread (use tmux or evaluation harness)
- Skip input validation or error handling
- Create tools without comprehensive documentation
- Build servers without considering agent context limits
