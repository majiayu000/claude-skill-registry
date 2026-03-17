---
name: sc-document
description: Generate focused documentation for components, functions, APIs, and features. Use when creating inline docs, API references, user guides, or technical documentation.
---

# Documentation Generation Skill

Focused documentation for code, APIs, and features.

## Quick Start

```bash
# Inline documentation
/sc:document src/auth/login.js --type inline

# API reference
/sc:document src/api --type api --style detailed

# User guide
/sc:document payment-module --type guide
```

## Behavioral Flow

1. **Analyze** - Examine component structure and functionality
2. **Identify** - Determine documentation requirements and audience
3. **Generate** - Create appropriate documentation content
4. **Format** - Apply consistent structure and patterns
5. **Integrate** - Ensure compatibility with existing docs

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | inline | inline, external, api, guide |
| `--style` | string | detailed | brief, detailed |

## Evidence Requirements

This skill does NOT require hard evidence. Deliverables are:
- Generated documentation files
- Inline code comments
- API reference materials

## Documentation Types

### Inline (`--type inline`)
- JSDoc/docstring generation
- Parameter and return descriptions
- Function-level comments

### External (`--type external`)
- Standalone documentation files
- Component overviews
- Integration guides

### API (`--type api`)
- Endpoint documentation
- Request/response schemas
- Usage examples

### Guide (`--type guide`)
- User-focused tutorials
- Implementation patterns
- Common use cases

## Style Options

### Brief (`--style brief`)
- Concise descriptions
- Essential information only
- Quick reference format

### Detailed (`--style detailed`)
- Comprehensive explanations
- Extended examples
- Edge case coverage

## Examples

### Inline Code Docs
```
/sc:document src/auth/login.js --type inline
# JSDoc with @param, @returns, @throws
```

### API Reference
```
/sc:document src/api --type api --style detailed
# Full endpoint docs with examples
```

### User Guide
```
/sc:document payment-module --type guide --style brief
# Quick-start tutorial with common patterns
```

### Component Docs
```
/sc:document components/ --type external
# README.md for component library
```

## MCP Integration

### PAL MCP (Quality & Research)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__codereview` | API docs | Review documentation accuracy |
| `mcp__pal__apilookup` | External APIs | Get current API documentation |
| `mcp__pal__chat` | Writing assistance | Get help with complex explanations |
| `mcp__pal__consensus` | Style decisions | Multi-model validation of doc approach |

### PAL Usage Patterns

```bash
# Verify documentation accuracy
mcp__pal__codereview(
    review_type="quick",
    step="Reviewing API documentation for accuracy",
    findings="Parameter descriptions, return types, examples",
    relevant_files=["/docs/api/auth.md"]
)

# Get current API docs for external integration
mcp__pal__apilookup(
    prompt="Get current Stripe API documentation for payment intents"
)

# Writing assistance for complex topics
mcp__pal__chat(
    prompt="Help me explain the OAuth2 authorization code flow clearly for developers",
    model="gpt-5.2"
)
```

### Rube MCP (Publishing & Collaboration)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | Doc platforms | Find Notion, Confluence, GitBook |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Publishing | Push docs to platforms |
| `mcp__rube__RUBE_REMOTE_WORKBENCH` | Bulk docs | Generate docs for large codebases |

### Rube Usage Patterns

```bash
# Publish documentation
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "NOTION_CREATE_PAGE", "arguments": {
        "title": "API Reference: Authentication",
        "content": "## Endpoints\n### POST /auth/login\n..."
    }},
    {"tool_slug": "CONFLUENCE_CREATE_PAGE", "arguments": {
        "space": "DEV",
        "title": "Auth API Documentation",
        "content": "..."
    }}
])

# Notify team of new docs
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#documentation",
        "text": "New API docs published: Authentication endpoints"
    }}
])

# Bulk generate docs
mcp__rube__RUBE_REMOTE_WORKBENCH(
    thought="Generate JSDoc for all exported functions",
    code_to_execute='''
import os
# Process all JS files and generate documentation
# Use invoke_llm for each function
'''
)
```

## Flags (Extended)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pal-review` | bool | false | Use PAL to review doc accuracy |
| `--publish` | string | - | Publish via Rube (notion, confluence, gitbook) |
| `--notify` | string | - | Notify via Rube (slack, teams, email) |

## Tool Coordination

- **Read** - Component analysis
- **Grep** - Reference extraction
- **Write** - Documentation creation
- **Glob** - Multi-file documentation
- **PAL MCP** - Accuracy review, API lookup, writing assistance
- **Rube MCP** - Publishing, notifications, bulk generation
