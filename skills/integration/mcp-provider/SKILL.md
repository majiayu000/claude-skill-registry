---
name: mcp-provider
description: Discovers, validates, and integrates Model Context Protocol (MCP) tools into Claude Code skills. Searches MCP catalogs, scores candidates, generates tool configurations, and optionally sets up Docker runtimes. Use when creating skills that need external MCP tool integration.
allowed-tools: Read, Write, Bash, Grep
---

# MCP Provider - MCP Tool Integration for Skills

Automatically discovers and integrates Model Context Protocol (MCP) tools into your Claude Code skills.

## What This Skill Does

The MCP Provider helps you add external MCP tools to your skills by:

1. **Discovering MCP tools** from approved catalogs
2. **Scoring and validating** candidates based on your requirements
3. **Generating tool artifacts** (configs, manifests) in skill directories
4. **Preparing runtimes** (optional Docker sandboxing)

## When to Use This Skill

- Creating a new skill that needs MCP tool integration
- Adding external capabilities to existing skills
- Validating MCP tool compatibility
- Setting up secure MCP tool execution environments

## Quick Start

### 1. Discover Available MCP Tools

```python
# Run from project root
python3 .claude/skills/mcp-provider/scripts/discover_mcp.py --search "database tools"
```

This searches approved MCP catalogs and displays matching tools.

### 2. Attach MCP Tool to a Skill

```python
# Attach a specific MCP tool to a skill
python3 .claude/skills/mcp-provider/scripts/attach_mcp.py \
  --skill-path .claude/skills/my-skill \
  --mcp-id "sql-query-executor" \
  --tool-name "db-tools"
```

This generates:
- Tool manifest in `.claude/skills/my-skill/mcp_tools/`
- Configuration files
- Optional Docker runtime setup

### 3. Validate MCP Tool

```python
# Test that the MCP tool works correctly
python3 .claude/skills/mcp-provider/scripts/test_mcp.py \
  --skill-path .claude/skills/my-skill \
  --tool-name "db-tools"
```

## Security Features

### Sandbox Isolation
- Docker containers with read-only filesystem
- Dropped capabilities for security
- Network isolation by default
- No access to host filesystem

### Source Validation
- Only approved MCP catalogs are processed
- Tools are scored against security policies
- Secrets never logged or exposed

### Runtime Controls
- Configurable resource limits
- Audit logging of all operations
- Health checks before activation

## Configuration

MCP Provider uses a simple config file:

```python
# .claude/skills/mcp-provider/config.json
{
  "approved_sources": [
    "https://github.com/modelcontextprotocol/servers"
  ],
  "docker_enabled": true,
  "sandbox_profile": "strict",
  "max_candidates": 10
}
```

## Common Workflows

### Add Database Tools to a Skill

```bash
# 1. Search for database MCP tools
python3 .claude/skills/mcp-provider/scripts/discover_mcp.py --search "database"

# 2. Attach the best match
python3 .claude/skills/mcp-provider/scripts/attach_mcp.py \
  --skill-path .claude/skills/data-processor \
  --mcp-id "postgresql-mcp" \
  --tool-name "postgres-tools"

# 3. Test it works
python3 .claude/skills/mcp-provider/scripts/test_mcp.py \
  --skill-path .claude/skills/data-processor \
  --tool-name "postgres-tools"
```

### Create Secure API Integration

```bash
# Discover API-related MCP tools
python3 .claude/skills/mcp-provider/scripts/discover_mcp.py --search "REST API"

# Attach with strict sandbox
python3 .claude/skills/mcp-provider/scripts/attach_mcp.py \
  --skill-path .claude/skills/api-client \
  --mcp-id "rest-api-client" \
  --sandbox strict \
  --network-isolation
```

## Advanced Features

### Custom Scoring

You can customize how MCP tools are scored:

```python
# In .claude/skills/mcp-provider/scripts/attach_mcp.py
# Add --score-config option with custom weights
python3 attach_mcp.py \
  --skill-path .claude/skills/my-skill \
  --mcp-id "tool-id" \
  --score-config '{"security": 0.6, "performance": 0.4}'
```

### Runtime Policies

Configure Docker execution policies:

```python
# .claude/skills/mcp-provider/runtime_policy.json
{
  "read_only_root": true,
  "drop_capabilities": ["ALL"],
  "add_capabilities": [],
  "network_mode": "none",
  "memory_limit": "512m",
  "cpu_quota": 50000
}
```

## Resources

See [references/MCP_INTEGRATION.md](references/MCP_INTEGRATION.md) for:
- Complete API documentation
- MCP catalog structure
- Security best practices
- Troubleshooting guide

## Limitations

- Only works with MCP tools that follow the standard protocol
- Docker required for sandboxed execution
- Approved sources only (security requirement)
- No automatic updates of MCP tools (manual refresh needed)

## Troubleshooting

**MCP tool not found:**
- Check the tool ID is correct
- Verify the catalog source is approved
- Try refreshing the catalog cache

**Docker runtime fails:**
- Ensure Docker is installed and running
- Check Docker permissions
- Verify the image is accessible

**Permission denied:**
- MCP tools run in strict sandbox by default
- Adjust runtime policy if needed (with caution)

---

*MCP Provider simplifies integration of external tools while maintaining security and isolation.*
