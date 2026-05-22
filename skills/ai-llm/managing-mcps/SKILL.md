---
name: managing-mcps
description: Creates, analyzes, updates, and evaluates Model Context Protocol (MCP) servers including architecture assessment, security validation, and connection configuration. Use when user asks if current context or logic should be MCP, requests MCP creation/improvement/update, mentions MCP is outdated, or asks how MCPs work, what MCPs are, explaining MCP concepts, understanding MCP architecture, protocol specification, server implementation, client integration, or connecting MCP servers to Claude Code.
---

# Managing MCPs

Enables comprehensive management of Model Context Protocol (MCP) servers including creation, analysis, improvement, and configuration.

## When to Use This Skill

Activate when:
- User asks if current conversation logic should become an MCP
- User asks if existing MCP can be improved or is outdated
- User requests creation of new MCP server
- User wants to analyze MCP architecture or implementation
- User asks about MCP concepts, protocol, or how MCPs work
- User wants to connect or configure MCP servers
- You identify repeated tool patterns that would benefit from MCP extraction

## Core Workflows

### Workflow 1: Evaluating if Logic Should Be MCP

When assessing whether current context or logic should become an MCP server:

#### Decision Criteria
Evaluate as checklist. Convert to MCP if 4+ criteria met:

- [ ] Logic provides reusable tools/resources across conversations
- [ ] Requires external system integration (APIs, databases, file systems)
- [ ] Needs persistent state or connection management
- [ ] Benefits multiple AI applications (not Claude-Code-specific)
- [ ] Requires specialized runtime environment (Node.js, Python, Docker)
- [ ] Implements security-sensitive operations requiring isolation
- [ ] Provides domain-specific data sources or knowledge bases

**Decision Rule:**
- If 4+ checked → Create MCP (proceed to Workflow 2)
- If 0-3 checked → Keep as inline logic or consider skill/command

Alternative patterns when MCP not appropriate:
- Simple utilities → Inline logic
- Claude-Code-specific workflows → Agent skill
- User shortcuts → Slash command
- Git operations → Hook

#### Recommendation Process
1. Identify tool patterns in conversation
2. Assess external integration needs
3. Evaluate reusability across AI clients
4. Explain MCP benefits vs alternatives
5. Outline proposed MCP structure
6. Offer to create if user agrees

### Workflow 2: Creating New MCP Server

When building new MCP server:

#### Step 1: Requirements Analysis
- Identify primary capabilities (tools, resources, prompts)
- Determine transport mechanism:
  - **HTTP**: Recommended for remote servers (cloud services, APIs)
  - **stdio**: For local processes and direct system access
  - **SSE**: Deprecated, avoid for new implementations
- Assess security requirements
- Choose runtime (Node.js TypeScript, Python, other)
- Plan authentication if needed

**Transport Priority:** HTTP is the recommended transport for remote servers (better cloud support, more reliable, widely supported). SSE is deprecated. For migration details, load deprecation-notes.md.

#### Step 2: Architecture Design
Load architecture-overview.md for protocol structure. Design:
- Server capabilities to expose
- Tool schemas and implementations
- Resource providers if applicable
- Prompt templates if applicable
- Lifecycle management
- Error handling strategy

#### Step 3: Implementation Planning
Load creation-guide.md for detailed steps. Plan:
- Project structure
- SDK integration (@modelcontextprotocol/sdk)
- Transport setup
- Capability registration
- Security implementation
- Testing strategy

#### Step 4: Development
Follow creation-guide.md systematic implementation:
- Initialize project with appropriate SDK
- Implement transport layer
- Register capabilities (tools/resources/prompts)
- Add request handlers
- Implement security measures per security-best-practices.md
- Add error handling and logging

#### Step 5: Configuration
Load configuration-guide.md for setup. Create:
- Server configuration for Claude Code
- Connection parameters
- Environment variables
- Security settings

#### Step 6: Testing
- Test with MCP Inspector tool
- Verify all tools/resources work
- Test error conditions
- Validate security measures
- Test Claude Code integration

#### Step 7: Documentation
Document:
- Installation instructions
- Configuration requirements
- Available capabilities
- Usage examples
- Security considerations

### Workflow 3: Analyzing Existing MCP

When evaluating existing MCP for improvements:

#### Step 1: MCP Discovery
- Use Glob to find MCP server files (package.json, pyproject.toml, *.ts, *.py)
- Use Read to load server implementation
- Use Grep to search for capability registrations
- Identify transport type and SDK usage

#### Step 2: Capability Inventory
Document:
- Tools provided (names, schemas, implementations)
- Resources provided (URIs, schemas, providers)
- Prompts provided (names, templates)
- Transport mechanism used
- Security features implemented

#### Step 3: Apply Analysis Framework
Load analysis-framework.md and evaluate:
- **Protocol Compliance**: Follows MCP specification 2025-06-18
- **Architecture Quality**: Transport, lifecycle, error handling
- **Tool Design**: Schema validity, input validation, error responses
- **Resource Design**: URI patterns, subscription support
- **Security Posture**: Authorization, input sanitization, rate limiting
- **Code Quality**: SDK usage, error handling, logging
- **Configuration**: Connection settings, environment variables
- **Documentation**: Installation, usage, examples

#### Step 4: Identify Issues
Categorize findings:
- **Critical**: Security vulnerabilities, protocol violations, broken functionality
- **Major**: Poor error handling, missing validation, unclear schemas
- **Minor**: Documentation gaps, code style, optimization opportunities

#### Step 5: Recommendations
Provide specific improvements:
- What to change
- Why it matters for MCP usage
- How to implement
- Priority level (critical/major/minor)

### Workflow 4: Updating Outdated MCP

When updating MCP for new specifications or improvements:

#### Step 1: Identify Outdated Elements
Check against current MCP specification:
- Protocol version compliance (current: 2025-06-18)
- Deprecated SDK methods
- Security best practice gaps
- Missing features now available
- Old transport patterns

#### Step 2: Plan Updates
- Preserve working functionality
- Upgrade SDK to latest version
- Update protocol compliance
- Add security improvements
- Enhance error handling
- Update documentation

#### Step 3: Implement Changes
- Edit server implementation files
- Update SDK imports and usage
- Modify capability registrations
- Update schemas to current spec
- Test all changes thoroughly

#### Step 4: Update Configuration
- Modify Claude Code config if needed
- Update environment variables
- Adjust security settings
- Update documentation

#### Step 5: Validation
- Test with MCP Inspector
- Verify Claude Code integration
- Confirm security measures
- Validate against specification

### Workflow 5: Configuring MCP Connection

When connecting MCP server to Claude Code:

#### Step 1: Choose Configuration Scope
Identify scope level (priority: Local > Project > User):
- **Local**: Temporary, session-specific (highest priority)
- **Project**: `.mcp.json` in project root (team-shared, requires approval)
- **User**: Cross-project personal settings (lowest priority)

**Security:** Project-scoped servers require user approval before first use. Claude Code prompts for approval when detecting `.mcp.json` servers. Use `claude mcp reset-project-choices` to clear previous approvals.

#### Step 2: Use CLI Commands (Primary Method)
Execute:

**Add server:**
```bash
claude mcp add --transport [stdio|http|sse] [--scope local|project|user] [--env KEY=VALUE] [--header "Name: Value"] [name] [command/url]
```

**Common flags:**
- `--scope local` (default) - Session-specific, not persisted
- `--scope project` - Team-shared via .mcp.json
- `--scope user` - Cross-project personal
- `--env KEY=VALUE` - Pass environment variables (repeatable)
- `--header "Name: Value"` - HTTP headers for http/sse (repeatable)

Examples:
```bash
# Local stdio server (default scope)
claude mcp add --transport stdio my-server -- node /path/to/server.js

# Project-scope server (team-shared)
claude mcp add --transport stdio --scope project github -- npx -y @modelcontextprotocol/server-github

# Remote HTTP server with auth header
claude mcp add --transport http api-server --header "Authorization: Bearer token" https://api.example.com/mcp

# With environment variables
claude mcp add --transport stdio github --env API_KEY=secret -- npx -y @modelcontextprotocol/server-github
```

**Manage servers:**
```bash
claude mcp list
claude mcp get [name]
claude mcp remove [name]
claude mcp add-json [json-string]
claude mcp reset-project-choices
```

**Windows-specific:** Native Windows (not WSL) requires `cmd /c` wrapper for npx servers:
```bash
claude mcp add --transport stdio server -- cmd /c npx -y @package/name
```
Without this wrapper, connection fails with "Connection closed" error.

#### Step 3: Alternative - Direct File Manipulation
When CLI unavailable or batch operations needed:
- Use Read to load `.mcp.json` from project root
- Use Edit to modify configuration
- Structure: `{"mcpServers": {"name": {"command": "...", "args": [...], "env": {...}}}}`
- User must restart Claude Code (cannot automate)

For team sharing with machine-specific values, load environment-variable-expansion.md for parameterization patterns.

#### Step 4: Authenticate (If Required)
For OAuth-protected servers:
- User types `/mcp` in conversation
- Follow OAuth prompts
- Tokens stored securely, auto-refresh

For detailed OAuth flow and troubleshooting, load oauth-authentication-flow.md.

#### Step 5: Plugin-Provided MCPs
Plugins can bundle MCP servers automatically. For plugin MCP details, see managing-plugins skill (handles plugin bundling, distribution, mcpServers configuration in plugin.json/.mcp.json).

#### Step 6: Verification
- User restarts Claude Code (config loaded on startup)
- Type `/mcp` in conversation to check server status
- Verify tools appear in available tools
- Test tool invocation

#### Step 7: Troubleshooting
Use Bash for diagnostics:
```bash
# Verify command exists
which node

# Test server standalone
node /path/to/server.js

# Test with Inspector
npx @modelcontextprotocol/inspector node /path/to/server.js

# Check configuration
claude mcp get server-name
```

### Workflow 6: Using MCPs via Messages API

When integrating MCPs into applications via the Anthropic Messages API (not Claude Code):

#### When to Use Messages API Integration
- Building applications that use Claude with MCP tools
- Remote server integration without Claude Code CLI
- Programmatic MCP server access
- API-based workflows requiring MCP capabilities

#### Quick Start
Load mcp-connector-api-integration.md for complete workflow including:
- MCP server configuration in API requests
- MCPToolset configuration patterns
- Beta headers and response handling
- Multiple server management
- Code examples in Python/TypeScript

**Note:** This workflow is for API users. Claude Code users should use Workflows 5 and 7 instead.

### Workflow 7: Using MCPs in Conversations

When referencing or invoking MCP capabilities during Claude Code conversations:

#### Step 1: Check Server Status
User command:
```
/mcp
```

Shows:
- Connected servers
- Connection status
- Available tools/resources/prompts
- Authentication status

#### Step 2: Reference MCP Resources
Syntax: `@server:protocol://resource/path`

**Examples:**
```
@github:issue://owner/repo/123
@database:schema://users
@filesystem:file:///path/to/file
```

**When user requests resource:**
"Analyze @github:issue://anthropics/claude-code/456" → Claude Code fetches issue content

For detailed resource reference patterns and troubleshooting, load mcp-resources-and-prompts.md.

#### Step 3: Invoke MCP Prompts
MCP prompts become slash commands: `/mcp__servername__promptname`

**Examples:**
```
/mcp__github__list_prs
/mcp__github__pr_review 123
/mcp__jira__create_issue "Bug title" high
```

**When user requests prompt:**
"Execute /mcp__github__pr_review 456" → Claude Code invokes GitHub MCP prompt with arg 456

For prompt discovery, argument patterns, and examples, load mcp-resources-and-prompts.md.

#### Step 4: Monitor Output Limits
**Limits:**
- Warning: 10,000 tokens
- Maximum: 25,000 tokens (configurable)

**Configure limits:**
```bash
MAX_MCP_OUTPUT_TOKENS=50000 claude  # Increase output limit
```

**When approaching limits:**
- Suggest filtering/pagination if tool supports it
- Break large queries into smaller requests
- Increase limit only if legitimate need

#### Step 5: Handle Authentication
**When MCP requires authentication:**
- User types `/mcp` in conversation
- Follow OAuth flow prompts
- Tokens stored securely, auto-refresh

No manual token management needed. For detailed OAuth setup and troubleshooting, load oauth-authentication-flow.md.

## Progressive Disclosure References

Load these files when specific detail needed for current workflow step:

**Core Guidance:**
- **architecture-overview.md**: MCP protocol structure, concepts, lifecycle, capabilities
- **creation-guide.md**: Step-by-step server implementation with SDK patterns
- **analysis-framework.md**: Comprehensive evaluation criteria for existing MCPs
- **configuration-guide.md**: Connection setup, transport config basics
- **security-best-practices.md**: Security validation, authorization, input sanitization

**Advanced Topics:**
- **mcp-connector-api-integration.md**: Complete Messages API integration workflow (Workflow 6)
- **enterprise-mcp-configuration.md**: Organization-wide MCP policies and restrictions
- **environment-variable-expansion.md**: Team-shared .mcp.json with variable parameterization
- **mcp-resources-and-prompts.md**: Using resources (@mentions) and prompts (/commands) in conversations
- **oauth-authentication-flow.md**: OAuth setup, token management, troubleshooting

**Cross-Skill References:**
- **managing-plugins skill**: Plugin bundling with MCP servers, distribution patterns
- **managing-prompts skill**: MCP prompts as specialized prompt templates

**Reference:**
- **deprecation-notes.md**: Old patterns, migration guides (SSE, old API versions)
- **examples.md**: Reference implementations from AWS, Microsoft, community

## Key Principles

1. **Protocol Compliance**: Always follow MCP specification 2025-06-18
2. **Security First**: Validate inputs, sanitize outputs, implement authorization
3. **SDK Usage**: Prefer official SDKs (@modelcontextprotocol/sdk) over custom implementations
4. **Transport Isolation**: Understand stdio vs SSE tradeoffs
5. **Schema Rigor**: JSON Schema validation for all tools and resources
6. **Error Transparency**: Clear error messages, proper logging
7. **Reusability**: Design for multiple AI client applications

## Tool Usage Patterns

**Discovering MCP servers:**
1. Use Glob with patterns: `**/package.json`, `**/*mcp*.py`, `**/server.ts`
2. Use Grep to search for: "@modelcontextprotocol/sdk", "class Server", "stdio"
3. Use Read to examine server implementation files

**Analyzing MCP implementation:**
1. Use Read to load main server file
2. Use Grep to find capability registrations: "server.setRequestHandler", "ListToolsRequest", "CallToolRequest"
3. Use Read to examine tool/resource implementations
4. Count and catalog all capabilities

**Creating MCP server:**
1. Use Bash to initialize project: `npm init` or `python -m venv`
2. Use Bash to install SDK: `npm install @modelcontextprotocol/sdk`
3. Use Write to create server implementation
4. Use Bash to test with Inspector: `npx @modelcontextprotocol/inspector`

**Configuring MCP connection:**
1. Primary: Use Bash to run `claude mcp add --transport [stdio|http|sse] --scope [local|project|user] [name] -- [command]`
2. Alternative (project scope): Use Read to load `.mcp.json` from project root, use Edit to modify mcpServers
3. User must restart Claude Code if using file manipulation (CLI reloads automatically)

**For advanced configuration topics:**
1. Check supporting files first (environment-variable-expansion.md, plugin-mcp-servers.md, etc.)
2. Ask user for documentation if information unclear
3. Use WebFetch only if user provides documentation URLs

**Validating MCP security:**
1. Use Grep to search for security patterns: "authorization", "validate", "sanitize"
2. Use Read to examine input validation code
3. Load security-best-practices.md to check compliance

## Common Patterns

**Tool Schema Definition:**
```typescript
{
  name: "tool-name",
  description: "What it does",
  inputSchema: {
    type: "object",
    properties: {
      param: { type: "string", description: "Parameter purpose" }
    },
    required: ["param"]
  }
}
```

**Resource URI Pattern:**
```
protocol://host/path?query=value
Examples:
- file:///path/to/resource
- db://database/table/id
- api://service/endpoint
```

**Error Response:**
```typescript
{
  code: -32600, // Invalid request
  message: "Clear error description",
  data: { additional: "context" }
}
```

## Security Considerations

**Third-party MCP servers:**
- Use at own risk - Anthropic has not verified third-party server security
- Only connect to trusted sources
- **Prompt injection risk:** Servers fetching untrusted content (web pages, user input, external APIs) can expose Claude to prompt injection attacks
- Review server documentation and security practices before connecting
- Servers with authentication can access credentials for their services

**Project-scope approval:**
- `.mcp.json` servers require user approval before first use
- Protects against malicious servers in cloned repositories
- Reset approvals: `claude mcp reset-project-choices`

## Related Skills

Cross-reference these complementary skills when managing MCPs:

- **managing-plugins**: When bundling MCPs with plugins for distribution (see plugin-mcp-servers.md)
- **managing-prompts**: When working with MCP prompts (specialized prompts exposed by servers)
- **managing-agent-skills**: When designing MCPs that provide tool capabilities similar to skills

## Anti-Patterns to Avoid

- Creating MCP for Claude-Code-only functionality (use skill instead)
- Exposing security-sensitive operations without authorization
- Skipping input validation on tool parameters
- Using custom protocol instead of official SDK
- Hardcoding credentials in server code
- Missing error handling in tool implementations
- Overly generic tool names ("process", "handle", "do")
- Stateful operations without proper cleanup
- Connecting to untrusted third-party MCP servers

## Quick Validation

Before considering MCP complete:
- [ ] Follows MCP specification 2025-06-18
- [ ] Uses official SDK (@modelcontextprotocol/sdk)
- [ ] All tools have valid JSON Schema
- [ ] Input validation on all parameters
- [ ] Error handling with proper codes
- [ ] Security measures implemented (auth, sanitization, rate limiting)
- [ ] Transport configured correctly (stdio/SSE)
- [ ] Successfully connects to Claude Code
- [ ] All tools tested with MCP Inspector
- [ ] Documentation includes installation and usage
- [ ] Environment variables documented
- [ ] No hardcoded credentials

## Output Format

When completing MCP management tasks:

1. **Summary**: What was done (evaluation, creation, analysis, update)
2. **Files**: Locations of server code, config, documentation
3. **Capabilities**: Tools, resources, prompts provided
4. **Configuration**: Connection settings for Claude Code
5. **Security**: Measures implemented
6. **Testing**: Validation results
7. **Next Steps**: How to use or improve the MCP

For history, see HISTORY.md
