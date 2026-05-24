---
name: mcp-converter
description: Converts MCP servers to Claude Skills with 90%+ context savings using progressive disclosure pattern. Supports automatic detection and on-demand conversion.
context:fork: true
allowed-tools: read, write, bash, grep, glob
version: 1.0
best_practices:
  - Convert MCP servers with 10+ tools
  - Keep critical tools (1-5) as MCP
  - Use automatic detection for new MCP servers
  - Validate generated Skills before installation
error_handling: graceful
streaming: supported
---

# MCP-to-Skill Converter Skill

## Identity

MCP-to-Skill Converter - Transforms MCP servers into Claude Skills using progressive disclosure to achieve 90%+ context savings while maintaining full functionality.

## Capabilities

- **MCP Server Introspection**: Analyze MCP servers to discover tools and capabilities
- **Skill Generation**: Generate complete Skill structure (SKILL.md, executor.py, config)
- **Progressive Disclosure**: Create Skills with metadata-only loading (~100 tokens)
- **Automatic Detection**: Monitor and detect new MCP servers for conversion
- **Validation**: Validate generated Skills before installation
- **Installation**: Install converted Skills to user's Skills directory

## The Problem

MCP servers load all tool definitions into context at startup:

- 20+ tools = 30-50k tokens consumed immediately
- Context fills before Claude does any work
- Hard to scale beyond ~100 tools
- Most tools unused in each conversation

## The Solution

Convert MCP servers to Skills with progressive disclosure:

- **Startup**: ~100 tokens (metadata only)
- **When used**: ~5k tokens (full instructions)
- **Executing**: 0 tokens (runs externally)
- **Savings**: 90%+ context reduction

## How It Works

1. **Introspection**: Connect to MCP server and discover all tools
2. **Analysis**: Calculate token usage and conversion eligibility
3. **Generation**: Create Skill structure with progressive disclosure
4. **Validation**: Verify Skill structure and functionality
5. **Installation**: Install to `~/.claude/skills/`

## Usage Patterns

### On-Demand Conversion

**When to Use**:

- You have an MCP server with 10+ tools
- Context space is critical
- Most tools aren't used in every conversation
- You want maximum context efficiency

**How to Invoke**:

```
"Convert the github MCP server to a Skill"
"Convert all MCP servers with more than 10 tools"
"Convert the custom-server MCP to a Skill"
```

**What It Does**:

- Reads MCP server configuration
- Introspects server to discover tools
- Generates Skill structure
- Validates and installs Skill

### Automatic Detection

**When Enabled**:

- Monitor `.claude/.mcp.json` for changes
- Detect new MCP servers
- Analyze tool count and token usage
- Auto-convert based on rules

**Configuration**:

```yaml
auto_convert:
  enabled: true
  threshold:
    tool_count: 10
    estimated_tokens: 5000
  exceptions:
    - github # Keep as MCP
    - memory # Keep as MCP
```

## Skill Structure

Generated Skills follow this structure:

```
skill-name/
├── SKILL.md          # Metadata and instructions (~100 tokens)
├── executor.py       # Dynamic MCP tool execution
└── config.json       # MCP server configuration
```

### SKILL.md (Progressive Disclosure)

**Metadata Only** (~100 tokens):

- Skill name and description
- Tool categories
- When to use guidance
- Quick reference

**Full Instructions** (~5k tokens, loaded when used):

- Complete tool documentation
- Usage examples
- Error handling
- Best practices

### executor.py

Handles MCP tool calls dynamically:

- Connects to MCP server
- Executes tool calls
- Returns results
- Handles errors

## Integration

### With Tool Search

Skills work alongside Tool Search:

- **Tool Search**: Semantic discovery of tools
- **Skills**: On-demand tool loading with minimal context
- **Combined**: Optimal context usage for large tool libraries

### With Skill Builder

Uses Skill Builder plugin for:

- Validation of generated Skills
- Template-based generation
- Testing and verification
- Installation management

### With Marketplace

Integrates with superpowers-marketplace:

- Install marketplace plugins
- Auto-detect MCP servers in plugins
- Convert plugin MCP servers to Skills
- Manage plugin ecosystem

## Best Practices

### When to Convert

**Convert to Skill When**:

- MCP server has 10+ tools
- Most tools unused in each conversation
- Context space is critical
- Tools are independent

**Keep as MCP When**:

- 1-5 tools (minimal context impact)
- Complex OAuth flows required
- Persistent connections needed
- Cross-platform compatibility critical

### Critical Tools to Keep as MCP

Keep these as MCP (always loaded):

- Core file operations: `read_file`, `write_file`, `search_code`
- Essential integrations: `create_pull_request`, `get_issue`
- Frequently used: `take_screenshot`, `navigate_page`

### Hybrid Approach

**Best Strategy**: Use both MCP and Skills

- **MCP**: Core tools (1-5 tools, always loaded)
- **Skills**: Extended toolset (10+ tools, on-demand)
- **Tool Search**: Discovery and semantic matching

## Examples

### Example 1: Convert GitHub MCP

```bash
# On-demand conversion
"Convert the github MCP server to a Skill"

# Result: Creates ~/.claude/skills/github/
# - SKILL.md (100 tokens metadata)
# - executor.py (dynamic tool calls)
# - config.json (MCP configuration)
```

### Example 2: Batch Conversion

```bash
# Convert multiple MCP servers
"Convert all MCP servers with more than 10 tools to Skills"

# Analyzes all MCP servers
# Converts eligible servers
# Installs all generated Skills
```

### Example 3: Automatic Detection

```yaml
# .claude/skills/mcp-converter/conversion_rules.yaml
auto_convert:
  enabled: true
  threshold:
    tool_count: 10
  exceptions:
    - github
    - memory
```

## Error Handling

**Common Issues**:

- MCP server not responding: Check configuration and environment variables
- Tool introspection fails: Verify MCP server is accessible
- Skill generation errors: Check templates and validation
- Installation fails: Verify Skills directory permissions

**Recovery**:

- Retry with verbose logging
- Validate MCP configuration
- Check Skill Builder integration
- Review conversion rules

## Context Savings

**Before (MCP)**:

```
20 tools = 30k tokens always loaded
Context available: 170k / 200k = 85%
```

**After (Skills)**:

```
20 skills = 2k tokens metadata
When 1 skill active: 7k tokens
Context available: 193k / 200k = 96.5%
```

## Dependencies

- `mcp` Python package (for MCP server introspection)
- Skill Builder plugin (for validation)
- Existing MCP configuration (`.claude/.mcp.json`)

## Batch Conversion

**Convert Multiple MCP Servers at Once**:

```bash
"Convert all MCP servers from the catalog"
"Convert all MCP servers with more than 15 tools"
"Convert MCP servers: postgres, aws, docker"
```

**Catalog-Based Conversion**:

The skill uses `mcp-catalog.yaml` to identify popular MCP servers for conversion:

- **Automatic Detection**: Servers in catalog are automatically considered
- **Priority-Based**: High priority servers converted first
- **Batch Processing**: Convert multiple servers concurrently (max 3 at a time)
- **Validation**: All converted skills validated before installation

**Catalog Features**:

- 25+ popular MCP servers pre-configured
- Tool count and token estimates
- Conversion priority levels
- Category tagging
- Keep-as-MCP exceptions (github, filesystem, memory)

**Batch Conversion Process**:

1. Load `mcp-catalog.yaml` to get server list
2. Filter by conversion criteria (tool count, tokens, priority)
3. Convert servers in parallel (max 3 concurrent)
4. Validate all generated skills
5. Install to `~/.claude/skills/`
6. Generate conversion report

## Catalog Support

**Using the MCP Catalog**:

The catalog (`mcp-catalog.yaml`) provides:

- **Server Metadata**: Name, description, tool count, token estimates
- **Conversion Rules**: Auto-convert thresholds and exceptions
- **Batch Settings**: Concurrent conversion limits and timeouts
- **Statistics**: Total servers, conversion recommendations

**Catalog Integration**:

- Catalog automatically loaded when skill is invoked
- Servers filtered by conversion criteria
- Exceptions (keep-as-MCP) respected
- Priority-based conversion order

**Example Catalog Entry**:

```yaml
- name: postgres
  description: PostgreSQL database operations
  tool_count: 20
  estimated_tokens: 35000
  conversion_priority: high
  keep_as_mcp: false
  categories:
    - database
    - data
```

## Related Skills

- **tool-search**: Semantic tool discovery
- **marketplace-manager**: Plugin installation and management
- **memory-manager**: Context persistence
