---
name: sc-mcp
description: Comprehensive MCP orchestration skill integrating PAL MCP (reasoning, consensus, debugging) and Rube MCP (500+ app automations). Central hub for all MCP-powered workflows.
---

# MCP Orchestration Skill

Central orchestration hub for PAL MCP and Rube MCP capabilities. Use this skill for complex workflows requiring multi-model reasoning, external service integration, or both.

## Quick Start

```bash
# PAL-powered analysis
/sc:mcp analyze --pal consensus --question "Should we use microservices?"

# Rube-powered automation
/sc:mcp automate --rube --apps slack,github --workflow "notify on PR"

# Combined orchestration
/sc:mcp orchestrate --pal thinkdeep --rube --full-validation
```

## PAL MCP Integration

### Available Tools

| Tool | Invocation | Purpose |
|------|------------|---------|
| `chat` | `mcp__pal__chat` | Collaborative thinking, brainstorming |
| `thinkdeep` | `mcp__pal__thinkdeep` | Multi-stage investigation, complex analysis |
| `planner` | `mcp__pal__planner` | Sequential planning with branching |
| `consensus` | `mcp__pal__consensus` | Multi-model voting on decisions |
| `codereview` | `mcp__pal__codereview` | Systematic code quality analysis |
| `precommit` | `mcp__pal__precommit` | Git change validation |
| `debug` | `mcp__pal__debug` | Root cause analysis |
| `challenge` | `mcp__pal__challenge` | Force critical thinking |
| `apilookup` | `mcp__pal__apilookup` | Current API/SDK documentation |
| `listmodels` | `mcp__pal__listmodels` | Available AI models |
| `clink` | `mcp__pal__clink` | External CLI integration |

### PAL Workflows

#### Consensus Decision Making

```
Use consensus for:
- Architectural decisions (2-3 models)
- Security validations (security-focused models)
- Technology choices (diverse perspectives)
- Complex trade-off analysis
```

Recommended model combinations:
- **Architectural**: gpt-5.2 (for), gemini-3-pro (against), deepseek (neutral)
- **Security**: gpt-5.2 (security focus), gemini-3-pro (attack surface)
- **Performance**: gpt-5.2 (optimization), deepseek (efficiency)

#### Debug Investigation

```
Use debug for:
- Complex bugs with unclear causes
- Performance issues
- Race conditions
- Memory leaks
- Integration problems
```

Debug confidence levels: exploring -> low -> medium -> high -> very_high -> almost_certain -> certain

#### Code Review

```
Use codereview for:
- Pre-merge validation
- Security audits
- Performance reviews
- Architecture compliance
```

Review types: full, security, performance, quick

## Rube MCP Integration

### Available Tools

| Tool | Invocation | Purpose |
|------|------------|---------|
| `SEARCH_TOOLS` | `mcp__rube__RUBE_SEARCH_TOOLS` | Discover available integrations |
| `CREATE_PLAN` | `mcp__rube__RUBE_CREATE_PLAN` | Generate execution plans |
| `MULTI_EXECUTE` | `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Parallel tool execution |
| `REMOTE_BASH` | `mcp__rube__RUBE_REMOTE_BASH_TOOL` | Remote shell commands |
| `REMOTE_WORKBENCH` | `mcp__rube__RUBE_REMOTE_WORKBENCH` | Python sandbox execution |
| `CREATE_RECIPE` | `mcp__rube__RUBE_CREATE_UPDATE_RECIPE` | Save reusable workflows |
| `EXECUTE_RECIPE` | `mcp__rube__RUBE_EXECUTE_RECIPE` | Run saved recipes |
| `FIND_RECIPE` | `mcp__rube__RUBE_FIND_RECIPE` | Search existing recipes |
| `MANAGE_CONNECTIONS` | `mcp__rube__RUBE_MANAGE_CONNECTIONS` | App authentication |
| `GET_SCHEMAS` | `mcp__rube__RUBE_GET_TOOL_SCHEMAS` | Tool input schemas |
| `MANAGE_SCHEDULE` | `mcp__rube__RUBE_MANAGE_RECIPE_SCHEDULE` | Recipe scheduling |

### Rube Workflows

#### External Integration Flow

```
1. SEARCH_TOOLS - Find relevant tools for use case
2. GET_SCHEMAS - Get input requirements (if schemaRef returned)
3. MANAGE_CONNECTIONS - Verify/create auth
4. MULTI_EXECUTE - Execute tools
5. CREATE_RECIPE - Save for reuse (optional)
```

#### Bulk Processing Flow

```
1. SEARCH_TOOLS - Find data source/destination tools
2. REMOTE_WORKBENCH - Process with Python helpers:
   - run_composio_tool() - Execute Composio tools
   - invoke_llm() - AI processing
   - upload_local_file() - Export results
   - proxy_execute() - Direct API calls
```

### Supported Apps (500+)

**Communication**: Slack, Discord, Teams, Gmail, Outlook, WhatsApp, Telegram
**Development**: GitHub, GitLab, Jira, Linear, Asana, Vercel
**Productivity**: Google Workspace, Notion, Airtable, Trello
**Data**: Snowflake, BigQuery, Datadog, Amplitude
**AI**: OpenAI, Anthropic, Replicate

## Combined Orchestration Patterns

### Pattern 1: Research + Decide + Execute

```
1. PAL thinkdeep - Investigate problem deeply
2. PAL consensus - Get multi-model decision
3. Rube SEARCH_TOOLS - Find execution tools
4. Rube MULTI_EXECUTE - Implement decision
```

### Pattern 2: Review + Validate + Notify

```
1. PAL codereview - Review code changes
2. PAL precommit - Validate git changes
3. Rube MULTI_EXECUTE - Send notifications (Slack, email)
4. Rube CREATE_RECIPE - Save for CI/CD
```

### Pattern 3: Debug + Fix + Verify

```
1. PAL debug - Root cause analysis
2. Implement fix locally
3. PAL codereview - Validate fix
4. Rube MULTI_EXECUTE - Update tickets, notify team
```

### Pattern 4: Plan + Consensus + Automate

```
1. PAL planner - Create implementation plan
2. PAL consensus - Validate approach with multiple models
3. Rube CREATE_PLAN - Generate execution plan
4. Rube MULTI_EXECUTE - Execute across apps
5. Rube CREATE_RECIPE - Save as reusable workflow
```

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pal` | string | - | PAL tool: chat, thinkdeep, planner, consensus, codereview, precommit, debug |
| `--rube` | bool | false | Enable Rube MCP integration |
| `--apps` | string | - | Comma-separated apps for Rube |
| `--models` | string | auto | Models for consensus (comma-separated) |
| `--full-validation` | bool | false | Run all PAL validators |
| `--save-recipe` | bool | false | Save workflow as Rube recipe |
| `--schedule` | string | - | Cron expression for recipe scheduling |

## Behavioral Flow

1. **Analyze** - Understand what MCP capabilities are needed
2. **Discover** - Use RUBE_SEARCH_TOOLS for external needs, listmodels for PAL
3. **Plan** - Create execution plan (PAL planner or RUBE_CREATE_PLAN)
4. **Validate** - Use consensus for critical decisions
5. **Execute** - Run PAL analysis and/or Rube tools
6. **Persist** - Save recipes, store memory for continuity
7. **Report** - Present findings with tool attribution

## Memory & State Management

### PAL Continuation

Use `continuation_id` to maintain context across PAL tool calls:

```python
# First call returns continuation_id
result = mcp__pal__thinkdeep(...)
continuation_id = result["continuation_id"]

# Subsequent calls reuse it
result = mcp__pal__thinkdeep(..., continuation_id=continuation_id)
```

### Rube Session & Memory

Use `session_id` and `memory` for Rube continuity:

```python
# First search generates session_id
result = mcp__rube__RUBE_SEARCH_TOOLS(..., session={"generate_id": True})
session_id = result["session_id"]

# Subsequent calls reuse session and build memory
result = mcp__rube__RUBE_MULTI_EXECUTE_TOOL(
    ...,
    session_id=session_id,
    memory={"slack": ["Channel general is C123"]}
)
```

## Examples

### Multi-Model Architecture Review

```bash
/sc:mcp analyze --pal consensus --models "gpt-5.2,gemini-3-pro,deepseek" \
  --question "Is event sourcing appropriate for this use case?"
```

### Automated PR Workflow

```bash
/sc:mcp automate --rube --apps github,slack \
  --workflow "On PR merge, post summary to #releases"
  --save-recipe --schedule "0 9 * * 1-5"
```

### Full Investigation Pipeline

```bash
/sc:mcp orchestrate --pal debug --rube \
  --issue "Memory leak in production" \
  --notify slack,jira --full-validation
```

## Guardrails

- Always search tools before executing unknown integrations
- Use consensus for decisions with >$1000 impact
- Validate schemas before multi-execute
- Store memory for frequently used IDs
- Check connection status before automation
- Use thinking_mode=high for complex PAL analysis

## Error Handling

| Error | Recovery |
|-------|----------|
| PAL model unavailable | Fall back to different model |
| Rube connection missing | Prompt MANAGE_CONNECTIONS |
| Tool schema unknown | Call GET_SCHEMAS first |
| Rate limited | Use backoff in REMOTE_WORKBENCH |
| Recipe not found | Search or create new |

## Resources

- PAL MCP: codereview, debug, consensus, thinkdeep, precommit, planner, chat, challenge, apilookup
- Rube MCP: 500+ app integrations via Composio
- Trait: `mcp-pal-enabled` - Apply PAL to any agent
- Trait: `mcp-rube-enabled` - Apply Rube to any agent
