---
name: manage-smithery-deployment
description: Quick reference for Smithery and Cloudflare deployment operations. Use for deploying Canvas MCP server, managing workers on ariff.dev, and testing OAuth endpoints.
allowed-tools: [Bash, Read]
---

# Skill: Manage Smithery Deployment

## Quick Commands

### Smithery Operations
```bash
# Search for servers
smithery search canvas
smithery list @a-ariff

# Validate config
cd packages/remote-mcp-server-authless
smithery validate

# Publish server
smithery publish

# Check version
smithery --version
```

### Cloudflare/Wrangler Operations
```bash
# Check auth
wrangler whoami

# Deploy workers
cd packages/remote-mcp-server-authless && npm run deploy
cd packages/cloudflare-canvas-api && npm run deploy

# Check logs
wrangler tail canvas-mcp-sse
wrangler tail canvas-mcp

# List KV namespaces
wrangler kv:namespace list
```

### Git Operations (Natural Style)
```bash
# Create feature branch
git checkout -b feat/smithery-fresh-deployment

# Stage changes
git add -A

# Commit with natural messages
git commit -m "chore: remove deprecated smithery configuration"
git commit -m "feat: add fresh smithery deployment with oauth"
git commit -m "docs: update deployment instructions for smithery"

# Push and create PR
git push origin feat/smithery-fresh-deployment
```

### Testing Endpoints
```bash
# Test MCP server health
curl https://canvas-mcp-sse.ariff.dev/health

# Test API proxy
curl https://canvas-mcp.ariff.dev/

# Test OAuth discovery
curl https://canvas-mcp-sse.ariff.dev/.well-known/oauth-authorization-server
```

## Configuration Templates

### smithery.yaml (OAuth Version)
```yaml
name: canvas-student-mcp
description: Canvas LMS integration MCP server with OAuth 2.1 authentication
version: "3.0.0"
author: a-ariff
homepage: https://github.com/a-ariff/canvas-student-mcp-server

remote:
  transport:
    type: sse
    url: https://canvas-mcp-sse.ariff.dev/sse
  authentication:
    type: oauth2
    discovery_url: https://canvas-mcp-sse.ariff.dev/.well-known/oauth-authorization-server
```

### Environment Variables
```bash
# For local testing
export CANVAS_API_KEY="your-test-key"
export CANVAS_BASE_URL="https://canvas.instructure.com"
export CLIENT_ID="canvas-mcp-client"
export CLIENT_SECRET="development-secret"
```

## Current Status Checklist
- ✅ Smithery CLI v1.6.3 installed
- ⏳ Old server needs removal
- ⏳ Fresh smithery.yaml needs creation
- ✅ Cloudflare workers deployed
- ✅ Domain routing configured
- ⚠️ Multi-user fix needed

## Repository Paths
- **Main repo**: `/Users/ariff/canvas-student-mcp-server/canvas-student-mcp-server`
- **MCP server**: `packages/remote-mcp-server-authless/`
- **API proxy**: `packages/cloudflare-canvas-api/`
- **Smithery config**: `packages/remote-mcp-server-authless/smithery.yaml`

## Important IDs
- **ChatGPT Client**: HqSTFXhPtTRy2nCUgI0ewhlResFPckU8
- **OAUTH_KV**: 274766504e584434b6d32de34357de8a
- **API_KEYS_KV**: c297508f4ae54d72827eb17dc2ceffac
- **CACHE_KV**: 5d8e432d63fe4a7eb2dcdbe9914ed4c6
- **RATE_LIMIT_KV**: 2750d79db84441d3a8fd7431ed85344b