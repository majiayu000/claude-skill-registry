---
name: deepwiki-api
description: This skill enables GitHub repository documentation exploration using DeepWiki API directly via curl. Use when researching repository structure, understanding library APIs, or asking questions about open-source projects. MCP server not required.
---

# DeepWiki API (Direct)

## Overview

DeepWiki provides AI-powered documentation exploration for GitHub repositories. This skill uses the API directly via curl - no MCP server required.

## Base URL
```
https://api.deepwiki.com
```

## Read Wiki Structure

Get a list of documentation topics for a repository.

### Endpoint
```
GET https://api.deepwiki.com/wiki/{owner}/{repo}/structure
```

### Usage
```bash
curl -s "https://api.deepwiki.com/wiki/microsoft/vscode/structure" \
  -H "Accept: application/json" | jq '.'
```

## Read Wiki Contents

Get full documentation content for a repository.

### Endpoint
```
GET https://api.deepwiki.com/wiki/{owner}/{repo}/contents
```

### Usage
```bash
curl -s "https://api.deepwiki.com/wiki/xtermjs/xterm.js/contents" \
  -H "Accept: application/json" | jq '.'
```

## Ask Question

Ask a question about a repository and get AI-generated answers.

### Endpoint
```
POST https://api.deepwiki.com/wiki/{owner}/{repo}/ask
```

### Usage
```bash
curl -s -X POST "https://api.deepwiki.com/wiki/microsoft/vscode/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How does the terminal handle PTY integration?"}'
```

## Common Workflows

### Research a Library
```bash
# Get structure first
curl -s "https://api.deepwiki.com/wiki/xtermjs/xterm.js/structure" | jq '.topics[]'

# Then ask specific questions
curl -s -X POST "https://api.deepwiki.com/wiki/xtermjs/xterm.js/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How to implement custom key handling?"}'
```

### Understand VS Code Patterns
```bash
curl -s -X POST "https://api.deepwiki.com/wiki/microsoft/vscode/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "How are WebView panels implemented?"}'
```

### Explore Repository Architecture
```bash
curl -s -X POST "https://api.deepwiki.com/wiki/anthropics/claude-code/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the overall architecture?"}'
```

## Response Processing

```bash
# Extract answer only
| jq '.answer'

# Get with sources
| jq '{answer, sources}'
```

## Notes

- No API key required for public repositories
- Rate limits may apply
- Responses are AI-generated based on repository content
