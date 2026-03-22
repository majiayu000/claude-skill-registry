---
name: minimax-mcp
description: MiniMax MCP server for web search and image understanding. Use when needing: (1) Web search via MiniMax API, (2) Analyze/describe images, (3) Extract content from URLs. Requires MINIMAX_API_KEY (China: api.minimaxi.com, Global: api.minimax.io).
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["uvx"], "env": ["MINIMAX_API_KEY", "MINIMAX_API_HOST"] },
        "primaryEnv": "MINIMAX_API_KEY",
        "install":
          [
            {
              "id": "region",
              "kind": "select",
              "label": "Select Region",
              "options": ["Global (minimax.io)", "Mainland China (minimaxi.com)"],
              "default": "Mainland China (minimaxi.com)"
            },
            {
              "id": "api_key",
              "kind": "input",
              "label": "MiniMax API Key",
              "description": "Global: https://www.minimax.io/platform/user-center/basic-information/interface-key | China: https://platform.minimaxi.com/user-center/basic-information/interface-key",
              "secret": true,
              "envVar": "MINIMAX_API_KEY"
            },
            {
              "id": "uv",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uvx"],
              "label": "Install uv (required for MCP server)"
            }
          ]
      }
  }
---

# MiniMax MCP Skill

## Overview

Official MiniMax Model Context Protocol (MCP) server for coding-plan users, providing AI-powered search and vision analysis capabilities.

## Features

| Tool | Function | Supported Formats |
|------|----------|-------------------|
| **web_search** | Web search with structured results (title, link, snippet) | - |
| **understand_image** | AI image analysis and content recognition | JPEG, PNG, WebP |

## Trigger Scenarios

Use this skill when user says:
- "Search for xxx" / "Look up xxx"
- "Look at this image" / "Analyze this picture"
- "What's in this image" / "Describe this photo"
- "Extract content from URL" / "Fetch this webpage"

## Quick Start

### 1. Get API Key

| Region | API Key URL | API Host |
|--------|-------------|----------|
| 🇨🇳 China | platform.minimaxi.com | https://api.minimaxi.com |
| 🇺🇳 Global | minimax.io | https://api.minimax.io |

### 2. Configure mcporter (Recommended)

```bash
# Add MCP server
mcporter config add minimax \
  --command "uvx minimax-coding-plan-mcp -y" \
  --env MINIMAX_API_KEY="your-key" \
  --env MINIMAX_API_HOST="https://api.minimaxi.com"

# Test connection
mcporter list
```

### 3. Direct Usage

```bash
# Search
mcporter call minimax.web_search query="keywords"

# Analyze image
mcporter call minimax.understand_image prompt="Describe this image" image_source="image-url-or-path"
```

## Usage Examples

See [references/examples.md](references/examples.md)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MINIMAX_API_KEY` | ✅ | Your MiniMax API Key |
| `MINIMAX_API_HOST` | ✅ | API endpoint |

## Important Notes

⚠️ **API Key must match the host region!**

| Region | API Key Source | API Host |
|--------|---------------|----------|
| Global | minimax.io | https://api.minimax.io |
| China | minimaxi.com | https://api.minimaxi.com |

If you get "Invalid API key" error, check if your Key and Host are from the same region.

## Troubleshooting

- **"uvx not found"**: Install uv - `brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **"Invalid API key"**: Confirm API Key and Host are from the same region
- **Image download failed**: Ensure image URL is publicly accessible, supports JPEG/PNG/WebP

## Related Resources

- GitHub: https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP
- MiniMax Platform: https://platform.minimaxi.com (China) / https://www.minimax.io (Global)
