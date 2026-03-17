---
name: sc-design
description: Design system architecture, APIs, and component interfaces with comprehensive specifications. Use when planning architecture, designing APIs, creating component interfaces, or modeling databases.
---

# System & Component Design Skill

Architecture planning and interface design with industry best practices.

## Quick Start

```bash
# Architecture design
/sc:design [target] --type architecture

# API specification
/sc:design payment-api --type api --format spec

# Database schema
/sc:design e-commerce --type database --format diagram
```

## Behavioral Flow

1. **Analyze** - Examine requirements and existing system context
2. **Plan** - Define design approach based on type and format
3. **Design** - Create specifications with best practices
4. **Validate** - Ensure maintainability and scalability
5. **Document** - Generate diagrams and specifications

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | architecture | architecture, api, component, database |
| `--format` | string | spec | diagram, spec, code |

## Evidence Requirements

This skill does NOT require hard evidence. Deliverables are:
- Design specifications and diagrams
- Interface definitions
- Schema documentation

## Design Types

### Architecture (`--type architecture`)
- System structure and component relationships
- Scalability and reliability patterns
- Service boundaries and communication

### API (`--type api`)
- RESTful/GraphQL endpoint design
- Request/response schemas
- Authentication and versioning

### Component (`--type component`)
- Interface contracts and dependencies
- State management patterns
- Integration points

### Database (`--type database`)
- Entity relationships and constraints
- Normalization and indexing
- Performance considerations

## Output Formats

### Diagram (`--format diagram`)
- ASCII or Mermaid diagrams
- Component relationship visualization
- Data flow representation

### Specification (`--format spec`)
- OpenAPI/Swagger for APIs
- Detailed interface documentation
- Technical requirements

### Code (`--format code`)
- Interface definitions
- Type declarations
- Skeleton implementations

## Examples

### System Architecture
```
/sc:design user-management --type architecture --format diagram
# Component relationships, data flow, scalability patterns
```

### API Design
```
/sc:design payment-api --type api --format spec
# OpenAPI spec with endpoints, schemas, auth patterns
```

### Component Interface
```
/sc:design notification-service --type component --format code
# TypeScript/Python interfaces with clear contracts
```

### Database Schema
```
/sc:design inventory-db --type database --format diagram
# ER diagrams with relationships and constraints
```

## MCP Integration

### PAL MCP (Design Validation)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__planner` | Architecture planning | Sequential planning with branching for design decisions |
| `mcp__pal__consensus` | Design decisions | Multi-model validation of architectural choices |
| `mcp__pal__thinkdeep` | Complex systems | Deep analysis of system requirements |
| `mcp__pal__chat` | Brainstorming | Collaborative design exploration |
| `mcp__pal__apilookup` | API standards | Get current API design best practices |

### PAL Usage Patterns

```bash
# Architecture planning
mcp__pal__planner(
    step="Designing microservices architecture for e-commerce platform",
    step_number=1,
    total_steps=4,
    more_steps_needed=True
)

# Validate design with consensus
mcp__pal__consensus(
    models=[
        {"model": "gpt-5.2", "stance": "for"},
        {"model": "gemini-3-pro", "stance": "against"},
        {"model": "deepseek", "stance": "neutral"}
    ],
    step="Evaluate: Should we use event sourcing for the order management system?"
)

# Deep system analysis
mcp__pal__thinkdeep(
    step="Analyzing scalability requirements for real-time notification system",
    hypothesis="WebSocket with Redis pub/sub will handle 100k concurrent users",
    confidence="medium",
    focus_areas=["scalability", "reliability", "performance"]
)
```

### Rube MCP (Documentation & Collaboration)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | External tools | Find diagramming, documentation tools |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Share designs | Post to Notion, Confluence, Slack |
| `mcp__rube__RUBE_CREATE_UPDATE_RECIPE` | Design workflows | Save reusable design processes |

### Rube Usage Patterns

```bash
# Create design document in Notion
mcp__rube__RUBE_SEARCH_TOOLS(queries=[
    {"use_case": "create notion page", "known_fields": "database:Architecture"}
])

mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "NOTION_CREATE_PAGE", "arguments": {
        "title": "Payment API Design v2",
        "content": "## Overview\n..."
    }}
])

# Share design for review
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#architecture",
        "text": "New design ready for review: Payment API v2"
    }},
    {"tool_slug": "JIRA_CREATE_ISSUE", "arguments": {
        "project": "ARCH",
        "summary": "Review: Payment API Design",
        "issue_type": "Task"
    }}
])
```

## Flags (Extended)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pal-plan` | bool | false | Use PAL planner for systematic design |
| `--consensus` | bool | false | Validate design with multi-model consensus |
| `--share` | string | - | Share via Rube (notion, confluence, slack) |
| `--create-ticket` | bool | false | Create review ticket via Rube |

## Tool Coordination

- **Read** - Requirements analysis
- **Grep/Glob** - Pattern analysis
- **Write** - Design documentation
- **Bash** - External tool integration
- **PAL MCP** - Design planning, consensus validation, deep analysis
- **Rube MCP** - Documentation sharing, collaboration, review workflows
