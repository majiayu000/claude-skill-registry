---
name: sc-explain
description: Provide clear explanations of code, concepts, and system behavior with educational clarity. Use when understanding code, learning concepts, or knowledge transfer.
---

# Code & Concept Explanation Skill

Educational explanations with adaptive depth and format.

## Quick Start

```bash
# Basic code explanation
/sc:explain authentication.js --level basic

# Framework concept
/sc:explain react-hooks --level intermediate --context react

# System architecture
/sc:explain microservices-system --level advanced --format interactive
```

## Behavioral Flow

1. **Analyze** - Examine target code or concept
2. **Assess** - Determine audience level and depth
3. **Structure** - Plan explanation with progressive complexity
4. **Generate** - Create clear explanations with examples
5. **Validate** - Verify accuracy and educational effectiveness

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--level` | string | intermediate | basic, intermediate, advanced |
| `--format` | string | text | text, examples, interactive |
| `--context` | string | - | Domain context (react, security, etc.) |

## Personas Activated

- **educator** - Learning-optimized explanations
- **architect** - System design context
- **security** - Security practice explanations

## MCP Integration

### PAL MCP (Multi-Perspective Explanations)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__consensus` | Complex topics | Cross-perspective validation |
| `mcp__pal__chat` | Clarification | Get alternative explanations |
| `mcp__pal__thinkdeep` | Deep concepts | Multi-stage exploration |
| `mcp__pal__apilookup` | Current APIs | Get up-to-date documentation |
| `mcp__pal__challenge` | Verify accuracy | Challenge explanation correctness |

### PAL Usage Patterns

```bash
# Multi-perspective explanation for complex topic
mcp__pal__consensus(
    models=[
        {"model": "gpt-5.2", "stance": "neutral"},
        {"model": "gemini-3-pro", "stance": "neutral"}
    ],
    step="Explain: How does React's reconciliation algorithm work?"
)

# Get alternative explanation approach
mcp__pal__chat(
    prompt="Explain React hooks to someone familiar with Vue composition API",
    model="gpt-5.2",
    thinking_mode="medium"
)

# Deep dive into complex concept
mcp__pal__thinkdeep(
    step="Understanding Kubernetes pod scheduling algorithm",
    hypothesis="Priority-based scheduling with resource constraints",
    confidence="medium",
    focus_areas=["scheduling", "resource_management", "affinity"]
)

# Verify explanation accuracy
mcp__pal__challenge(
    prompt="Is my explanation of OAuth2 refresh tokens technically accurate?"
)

# Get current API/framework documentation
mcp__pal__apilookup(
    prompt="Get current React 19 documentation for use hook"
)
```

### Rube MCP (Research & Sharing)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | Web research | Find tutorials, docs, examples |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Share explanations | Post to Notion, Slack, etc. |

### Rube Usage Patterns

```bash
# Research current best practices
mcp__rube__RUBE_SEARCH_TOOLS(queries=[
    {"use_case": "web search", "known_fields": "query:React 19 new features explained"}
])

# Share explanation with team
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "NOTION_CREATE_PAGE", "arguments": {
        "title": "Understanding: React Concurrent Mode",
        "content": "## Overview\n..."
    }},
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#learning",
        "text": "New explainer: React Concurrent Mode fundamentals"
    }}
])
```

## Flags (Extended)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pal-consensus` | bool | false | Use PAL for multi-perspective validation |
| `--pal-deep` | bool | false | Use PAL thinkdeep for complex topics |
| `--research` | bool | false | Use Rube for web research |
| `--share` | string | - | Share via Rube (notion, slack, confluence) |

## Evidence Requirements

This skill does NOT require hard evidence. Focus on:
- Clear, accurate explanations
- Appropriate examples
- Progressive complexity

## Explanation Levels

### Basic (`--level basic`)
- Foundational concepts
- Simple examples
- Beginner-friendly language

### Intermediate (`--level intermediate`)
- Implementation details
- Common patterns
- Best practices

### Advanced (`--level advanced`)
- Deep technical details
- Edge cases and trade-offs
- Performance implications

## Format Options

### Text (`--format text`)
- Written explanations
- Step-by-step breakdowns
- Conceptual overviews

### Examples (`--format examples`)
- Code samples
- Before/after comparisons
- Real-world applications

### Interactive (`--format interactive`)
- Progressive disclosure
- Follow-up suggestions
- Exploration paths

## Examples

### Code Explanation
```
/sc:explain src/auth/jwt.js --level basic
# What the code does, how it works, why it's structured this way
```

### Framework Concept
```
/sc:explain useEffect --level intermediate --context react
# Hook lifecycle, dependency arrays, cleanup patterns
```

### Architecture Explanation
```
/sc:explain event-driven-architecture --level advanced
# Patterns, trade-offs, implementation strategies
```

### Security Concept
```
/sc:explain oauth2-flow --level basic --context security
# Authorization flow, tokens, security considerations
```

## Tool Coordination

- **Read/Grep/Glob** - Code analysis
- **TodoWrite** - Multi-part explanation tracking
- **Task** - Complex explanation delegation
