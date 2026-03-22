---
# ═══════════════════════════════════════════════════════════════════════════════
# CLAUDE OFFICE SKILL - Enhanced Metadata v2.0
# ═══════════════════════════════════════════════════════════════════════════════

# Basic Information
name: mcp-hub
description: "Access 1200+ AI Agent tools via Model Context Protocol (MCP)"
version: "1.0"
author: claude-office-skills
license: MIT

# Categorization
category: workflow
tags:
  - mcp
  - hub
  - tools
  - integration
department: All

# AI Model Compatibility
models:
  recommended:
    - claude-sonnet-4
    - claude-opus-4
  compatible:
    - claude-3-5-sonnet
    - gpt-4
    - gpt-4o

# Skill Capabilities
capabilities:
  - tool_discovery
  - mcp_integration

# Language Support
languages:
  - en
  - zh
---

# Mcp Hub Skill

## Overview

This skill provides access to 1200+ MCP (Model Context Protocol) servers - standardized tools that extend AI capabilities. Connect Claude to filesystems, databases, APIs, and document processing tools.

## How to Use

1. Describe what you want to accomplish
2. Provide any required input data or files
3. I'll execute the appropriate operations

**Example prompts:**
- "Access local filesystem to read/write documents"
- "Query databases for data analysis"
- "Integrate with GitHub, Slack, Google Drive"
- "Run document processing tools"

## Domain Knowledge


### MCP Architecture

```
Claude ←→ MCP Server ←→ External Resource
        (Protocol)      (Files, APIs, DBs)
```

### Popular Document MCP Servers

| Server | Function | Stars |
|--------|----------|-------|
| **filesystem** | Read/write local files | Official |
| **google-drive** | Access Google Docs/Sheets | 5k+ |
| **puppeteer** | Browser automation, PDF gen | 10k+ |
| **sqlite** | Database queries | Official |

### Configuration Example

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/documents"
      ]
    },
    "google-drive": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-google-drive"]
    }
  }
}
```

### MCP Tool Discovery

Browse available servers:
- [mcp.run](https://mcp.run) - MCP marketplace
- [awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
- [mcp-awesome.com](https://mcp-awesome.com)

### Using MCP in Skills

```python
# MCP tools become available to Claude automatically
# Example: filesystem MCP provides these tools:

# read_file(path) - Read file contents
# write_file(path, content) - Write to file
# list_directory(path) - List directory contents
# search_files(query) - Search for files
```


## Best Practices

1. **Only enable MCP servers you need (security)**
2. **Use official servers when available**
3. **Check server permissions before enabling**
4. **Combine multiple servers for complex workflows**

## Installation

```bash
# Install required dependencies
pip install python-docx openpyxl python-pptx reportlab jinja2
```

## Resources

- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [Claude Office Skills Hub](https://github.com/claude-office-skills/skills)
