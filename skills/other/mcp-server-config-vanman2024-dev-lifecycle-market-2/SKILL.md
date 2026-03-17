---
name: mcp-server-config
description: Manage .mcp.json MCP server configurations. Use when configuring MCP servers, adding server entries, managing MCP config files, or when user mentions .mcp.json, MCP server setup, server configuration.
allowed-tools: Bash, Read, Write, Edit
---

# MCP Server Config

This skill manages `.mcp.json` files for MCP server configuration.

## Instructions

### Adding MCP Server

1. **Add Server Entry**
   - Use script: `scripts/add-mcp-server.sh <server-name> <command> <args...>`
   - Updates `.mcp.json` with new server configuration

2. **Configure Environment Variables**
   - Use script: `scripts/set-server-env.sh <server-name> <VAR=value>`
   - Adds environment variables to server config

### Managing Configuration

1. **List Servers**
   - Use script: `scripts/list-mcp-servers.sh`
   - Shows all configured MCP servers

2. **Remove Server**
   - Use script: `scripts/remove-mcp-server.sh <server-name>`
   - Removes server from configuration

3. **Validate Config**
   - Use script: `scripts/validate-mcp-config.sh`
   - Checks `.mcp.json` structure and server definitions

## Available Scripts

- **`scripts/add-mcp-server.sh`** - Add new MCP server to config
- **`scripts/remove-mcp-server.sh`** - Remove server from config
- **`scripts/list-mcp-servers.sh`** - List all configured servers
- **`scripts/set-server-env.sh`** - Set environment variables for server
- **`scripts/validate-mcp-config.sh`** - Validate .mcp.json structure

## Available Templates

### FastMCP Configuration
- **`templates/fastmcp-config-template.json`** - fastmcp.json for FastMCP Cloud deployment

### STDIO Deployment (Local IDEs)
- **`templates/mcp-stdio-python-template.json`** - .mcp.json for Python command
- **`templates/mcp-stdio-uv-template.json`** - .mcp.json for UV runner
- **`templates/mcp-config-template.json`** - Generic .mcp.json template

### HTTP Deployment
- **`templates/mcp-http-template.json`** - .mcp.json for HTTP transport

### Cloud Deployment
- **`templates/mcp-cloud-template.json`** - .mcp.json for FastMCP Cloud

## Examples

**Example 1: Add Postman MCP Server**
```bash
# Add Postman server
./scripts/add-mcp-server.sh postman npx -y @executeautomation/postman-mcp-server

# Set API key
./scripts/set-server-env.sh postman POSTMAN_API_KEY="\${POSTMAN_API_KEY}"
```

**Example 2: Manage Servers**
```bash
# List all servers
./scripts/list-mcp-servers.sh

# Remove a server
./scripts/remove-mcp-server.sh old-server

# Validate configuration
./scripts/validate-mcp-config.sh
```

## Requirements

- jq for JSON processing
- Valid .mcp.json file (or will be created)

## Success Criteria

- ✅ .mcp.json created/updated correctly
- ✅ Server configuration valid
- ✅ Environment variables properly set
- ✅ Config validates successfully
