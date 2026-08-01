---
name: dipeo-backend
description: 'Router skill for DiPeO backend ecosystem (server/ and cli/): FastAPI
  server, CLI tools, database, MCP integration. Use when task mentions CLI commands,
  server endpoints, database queries, or MCP tools'
---

---
name: dipeo-backend
description: Router skill for DiPeO backend ecosystem (server/ and cli/): FastAPI server, CLI tools, database, MCP integration. Use when task mentions CLI commands, server endpoints, database queries, or MCP tools. For simple tasks, handle directly; for complex work, escalate to dipeo-backend agent.
allowed-tools: Read, Grep, Glob, Bash, Skill
---

# DiPeO Backend Router

**Domain**: Backend ecosystem including FastAPI server (`server/`), CLI tools (`cli/`), message store, and MCP integration. Database schema initialization is in `/dipeo/infrastructure/execution/state/persistence_manager.py` (package-maintainer domain).

## Quick Decision: Skill or Agent?

### ✅ Handle Directly (This Skill)
- **Simple changes**: <20 lines, 1-2 files
- **Read-only tasks**: Understanding code, reviewing configs, debugging logs
- **Documentation lookup**: CLI help, API signatures, database schema
- **Small config tweaks**: Environment variables, command flags

### ❌ Escalate to Agent
- **Complex features**: Multi-file changes, new CLI commands, database migrations
- **Architecture changes**: New API endpoints, MCP tool implementation
- **Cross-cutting concerns**: Affects CLI + database + execution engine
- **Uncertain scope**: Not sure how many files will change

**Agent**: `Task(dipeo-backend, "your detailed task description")`

## Documentation Sections (Load On-Demand)

Use `Skill(doc-lookup)` with these anchors when you need detailed context:

**Core Responsibilities**:
- `docs/agents/backend-development.md#core-responsibilities` - CLI, FastAPI server, database, MCP server

**Implementation Patterns**:
- `docs/agents/backend-development.md#common-patterns` - CLI, background execution, database, MCP patterns

**Troubleshooting**:
- `docs/agents/backend-development.md#troubleshooting` - Server, CLI, database, MCP issues

**MCP Integration**:
- `docs/features/mcp-server-integration.md#quick-start` - Setup and usage guide
- `docs/features/chatgpt-mcp-integration.md#quick-start` - ChatGPT connection

**Example doc-lookup call**:
```bash
python .claude/skills/doc-lookup/scripts/section_search.py \
  --query "cli-commands" \
  --paths docs/agents/backend-development.md \
  --top 1
```

## Escalation to Other Agents

**To dipeo-package-maintainer**: Execution handlers, service architecture, domain models, LLM infrastructure
**To dipeo-codegen-pipeline**: GraphQL schema changes, generated type issues, TypeScript specs

## Typical Workflow

1. **Assess task complexity**: Simple (handle) vs. complex (escalate)
2. **If simple**: Load relevant section via `Skill(doc-lookup)`
3. **Execute**: Make changes or provide answer
4. **If complex**: Escalate with `Task(dipeo-backend, "task details")`
