---
name: discover-mcp
description: Automatically discover MCP (Model Context Protocol) skills when building MCP servers, designing tools, implementing resources/prompts, or testing MCP integrations. Activates for MCP server development tasks.
license: MIT
metadata:
  author: rand
  version: "3.1"
compatibility: Designed for Claude Code. Compatible with any agent supporting the Agent Skills format.
---

# MCP Skills Discovery

Provides automatic access to comprehensive MCP server development, tool design, and testing skills.

## When This Skill Activates

This skill auto-activates when you're working with:
- Building MCP servers (TypeScript or Python)
- Designing MCP tools, resources, or prompts
- Choosing MCP transports (stdio, SSE, Streamable HTTP)
- Implementing JSON-RPC 2.0 over MCP
- Testing MCP servers with Inspector or automated tests
- Debugging MCP protocol or transport issues
- Publishing or deploying MCP servers

## Available Skills

### Quick Reference

The MCP category contains 3 specialized skills:

1. **mcp-server-fundamentals** - Architecture, transports, tools/resources/prompts primitives, SDK setup
2. **mcp-tool-design** - Tool naming, schemas, error handling, annotations, progressive disclosure
3. **mcp-testing** - Inspector, unit tests, integration tests, transport debugging, CI/CD

### Load Full Category Details

For complete descriptions and workflows:

Read <cc-polymath-root>/skills/mcp/INDEX.md


This loads the full MCP category index with:
- Detailed skill descriptions
- Usage triggers for each skill
- Common workflow combinations
- Cross-references to related skills

### Load Specific Skills

Load individual skills as needed:

# Server architecture and setup
Read <cc-polymath-root>/skills/mcp/mcp-server-fundamentals.md

# Tool design and best practices
Read <cc-polymath-root>/skills/mcp/mcp-tool-design.md

# Testing and debugging
Read <cc-polymath-root>/skills/mcp/mcp-testing.md


## Common Workflows

### New MCP Server
**Sequence**: Fundamentals -> Tool Design -> Testing

Read <cc-polymath-root>/skills/mcp/mcp-server-fundamentals.md   # Architecture, transport, SDK
Read <cc-polymath-root>/skills/mcp/mcp-tool-design.md           # Design tool interfaces
Read <cc-polymath-root>/skills/mcp/mcp-testing.md               # Test with Inspector, CI


### Adding Tools to Existing Server
**Sequence**: Tool Design -> Testing

Read <cc-polymath-root>/skills/mcp/mcp-tool-design.md           # Naming, schemas, errors
Read <cc-polymath-root>/skills/mcp/mcp-testing.md               # Test new tools


### Debugging MCP Issues
**Sequence**: Testing -> Fundamentals

Read <cc-polymath-root>/skills/mcp/mcp-testing.md               # Inspector, transport debugging
Read <cc-polymath-root>/skills/mcp/mcp-server-fundamentals.md   # Lifecycle, capabilities


## Integration with Other Skills

MCP skills commonly combine with:

**API skills** (`discover-api`):
- MCP servers wrapping REST or GraphQL APIs
- Authentication for MCP tool backends

**Testing skills** (`discover-testing`):
- Comprehensive test strategies
- Contract testing patterns

**Infrastructure skills** (`discover-infra`, `discover-cloud`):
- Deploying MCP servers
- Scaling HTTP transports

## Progressive Loading

This gateway skill (~170 lines, ~1.5K tokens) enables progressive loading:
- **Level 1**: Gateway loads automatically (you're here now)
- **Level 2**: Load category INDEX.md (~2.5K tokens) for full overview
- **Level 3**: Load specific skills (~2-3K tokens each) as needed

Total context: 1.5K + 2.5K + skill(s) = 4-8K tokens vs 12K+ for everything.

## Quick Start Examples

**"Build an MCP server"**:
Read <cc-polymath-root>/skills/mcp/mcp-server-fundamentals.md


**"Design MCP tools for my API"**:
Read <cc-polymath-root>/skills/mcp/mcp-tool-design.md


**"Test my MCP server"**:
Read <cc-polymath-root>/skills/mcp/mcp-testing.md


**"Debug why my MCP tool isn't showing up"**:
Read <cc-polymath-root>/skills/mcp/mcp-testing.md



**Next Steps**: Run `Read <cc-polymath-root>/skills/mcp/INDEX.md` to see full category details, or load specific skills using the commands above.
