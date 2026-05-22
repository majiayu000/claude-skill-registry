---
name: adynato-aimake
description: Integrate with aimake's AI-powered delivery pipeline via MCP. Covers connecting to aimake, using code/docs/kanban tools, understanding the card-based system, and leveraging AI capabilities. Use when building integrations with aimake or using its MCP tools.
---

# aimake Skill

Use this skill when integrating with aimake via MCP or leveraging its AI-powered delivery tools.

## What is aimake?

aimake is an AI-powered delivery pipeline platform where **cards are the deliverables**, not tickets about work happening elsewhere. The AI drives work forward while humans bring taste and decision-making.

**Key Concepts:**
- **Cards** are atomic, independently deliverable work units
- **Boards** organize cards by type (Product, Engineering, Bugs, Docs)
- **Stages** are quality gates that enforce professional standards
- **Card AI** co-authors deliverables through conversation

## Connecting via MCP

aimake exposes its functionality through MCP (Model Context Protocol).

### Endpoints

```
GET  /mcp/manifest      # Returns available tool definitions
POST /mcp/tools/:name   # Executes a specific tool
```

### Example Connection

```typescript
// Fetch available tools
const manifest = await fetch('https://your-aimake-instance/mcp/manifest');
const tools = await manifest.json();

// Execute a tool
const result = await fetch('https://your-aimake-instance/mcp/tools/search_code_text', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_API_KEY'
  },
  body: JSON.stringify({
    query: 'authentication',
    project_id: 'proj_123'
  })
});
```

## Available MCP Tools

### Code Tools

Search and analyze code in connected repositories.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `search_code_semantic` | AI embeddings for conceptual matching | `query`, `project_id` |
| `search_code_text` | Ripgrep-based pattern matching | `query`, `project_id`, `file_pattern` |
| `read_file` | Get file content with line numbers | `path`, `project_id` |
| `list_directory` | Browse repository structure | `path`, `project_id` |
| `get_file_tree` | Complete code structure overview | `project_id` |

**Example: Semantic Code Search**
```json
{
  "tool": "search_code_semantic",
  "input": {
    "query": "how is user authentication handled",
    "project_id": "proj_123"
  }
}
```

### Documentation Tools

Access and search project documentation.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `search_docs` | Full-text search across docs | `query`, `project_id` |
| `get_doc_page` | Retrieve specific page | `page_id`, `project_id` |
| `list_docs` | List all documentation pages | `project_id` |

**Example: Search Documentation**
```json
{
  "tool": "search_docs",
  "input": {
    "query": "API rate limits",
    "project_id": "proj_123"
  }
}
```

### Kanban Tools

Manage cards and projects in the delivery pipeline.

| Tool | Description | Key Parameters |
|------|-------------|----------------|
| `query_cards` | Search and filter cards | `project_id`, `board`, `stage`, `search` |
| `get_card` | Get card details | `card_id` |
| `update_card_field` | Update a card field | `card_id`, `field`, `value` |
| `move_card_to_stage` | Move card to different stage | `card_id`, `stage` |
| `spawn_cards` | Create new cards | `project_id`, `board`, `cards[]` |
| `get_project` | Get project details | `project_id` |

**Example: Query Cards**
```json
{
  "tool": "query_cards",
  "input": {
    "project_id": "proj_123",
    "board": "engineering",
    "stage": "in_progress",
    "search": "authentication"
  }
}
```

**Example: Create Cards**
```json
{
  "tool": "spawn_cards",
  "input": {
    "project_id": "proj_123",
    "board": "engineering",
    "cards": [
      { "title": "Add OAuth2 support", "stage": "backlog" },
      { "title": "Implement refresh tokens", "stage": "backlog" }
    ]
  }
}
```

## Understanding Boards and Stages

### Board Types

| Board | Purpose | Use For |
|-------|---------|---------|
| **Product** | Specs and requirements | Feature definitions, user stories |
| **Engineering** | Implementation tasks | Code work, technical tasks |
| **Bugs** | Issue tracking | Bug reports, fixes |
| **Docs** | Documentation | Project docs, guides |

### Stage Progression

Cards move through stages as work progresses:

**Product Board:**
```
problemStatement → acceptanceCriteria → technicalReview → ready
```

**Engineering Board:**
```
backlog → in_progress → review → done
```

### Atomicity Rules

Each card should be atomic and independently deliverable:

| Board | What's Atomic |
|-------|---------------|
| Product | One shippable experience ("Welcome screen" not "Onboarding") |
| Engineering | One independently shippable component |
| Bugs | One specific, reproducible problem |

## Working with Card AI

Each card has an AI assistant that helps co-author the deliverable.

### What Card AI Can Do

- Fill in card fields based on conversation
- Detect scope creep and suggest splitting cards
- Validate readiness before stage transitions
- Search code and docs for context
- Break down large work into atomic cards

### Integration Pattern

When building tools that interact with aimake cards:

```typescript
// 1. Get card context
const card = await mcpTool('get_card', { card_id: 'card_123' });

// 2. Search for relevant code
const codeContext = await mcpTool('search_code_semantic', {
  query: card.title,
  project_id: card.project_id
});

// 3. Update card with findings
await mcpTool('update_card_field', {
  card_id: 'card_123',
  field: 'technicalNotes',
  value: `Relevant files:\n${codeContext.results.map(r => r.path).join('\n')}`
});
```

## Common Integration Patterns

### Triage Agent

Use aimake to analyze and route incoming requests:

```typescript
// 1. Search docs for relevant context
const docs = await mcpTool('search_docs', { query: userRequest, project_id });

// 2. Search code for implementation details
const code = await mcpTool('search_code_semantic', { query: userRequest, project_id });

// 3. Create appropriate card
await mcpTool('spawn_cards', {
  project_id,
  board: isFeature ? 'product' : 'bugs',
  cards: [{ title: summarize(userRequest), stage: 'backlog' }]
});
```

### Context Retrieval

Pull relevant context from aimake for AI conversations:

```typescript
// Get project overview
const project = await mcpTool('get_project', { project_id });
const fileTree = await mcpTool('get_file_tree', { project_id });
const docs = await mcpTool('list_docs', { project_id });

// Search for specific context
const relevantCode = await mcpTool('search_code_text', {
  query: 'class UserAuth',
  project_id
});
```

### Progress Tracking

Query cards to understand project state:

```typescript
// Get all in-progress work
const activeWork = await mcpTool('query_cards', {
  project_id,
  stage: 'in_progress'
});

// Get cards related to a feature
const featureCards = await mcpTool('query_cards', {
  project_id,
  search: 'authentication',
  boards: ['product', 'engineering', 'bugs']
});
```

## Tool Response Format

All MCP tools return JSON responses:

```typescript
// Success
{
  "success": true,
  "data": { /* tool-specific response */ }
}

// Error
{
  "success": false,
  "error": "Error message"
}
```

### Code Search Response

```typescript
{
  "results": [
    {
      "path": "src/auth/login.ts",
      "lines": "45-67",
      "content": "...",
      "score": 0.92
    }
  ]
}
```

### Card Response

```typescript
{
  "id": "card_123",
  "title": "Add OAuth2 support",
  "board": "engineering",
  "stage": "in_progress",
  "data": {
    "problemStatement": "...",
    "acceptanceCriteria": "...",
    "technicalNotes": "..."
  }
}
```
