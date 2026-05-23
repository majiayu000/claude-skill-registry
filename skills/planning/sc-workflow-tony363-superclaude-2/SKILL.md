---
name: sc-workflow
description: Generate structured implementation workflows from PRDs and feature requirements. Use when planning implementations, decomposing features, or coordinating multi-domain development.
---

# Implementation Workflow Generator Skill

Transform PRDs and requirements into structured implementation plans.

## Quick Start

```bash
# PRD-based workflow
/sc:workflow feature-spec.md --strategy systematic --depth deep

# Feature workflow
/sc:workflow "user auth system" --strategy agile --parallel

# Enterprise planning
/sc:workflow enterprise-prd.md --strategy enterprise --validate
```

## Behavioral Flow

1. **Analyze** - Parse PRD and feature specifications
2. **Plan** - Generate workflow structure with dependencies
3. **Coordinate** - Activate personas for domain expertise
4. **Execute** - Create step-by-step workflows
5. **Validate** - Apply quality gates and completeness checks

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--strategy` | string | systematic | systematic, agile, enterprise |
| `--depth` | string | normal | shallow, normal, deep |
| `--parallel` | bool | false | Enable parallel task generation |
| `--validate` | bool | false | Include quality gates |

## Personas Activated

- **architect** - System design and technical planning
- **analyzer** - Requirements analysis
- **frontend** - UI/UX implementation planning
- **backend** - API and data layer planning
- **security** - Security requirements integration
- **devops** - Infrastructure and deployment planning
- **project-manager** - Timeline and resource coordination

## MCP Integration

### PAL MCP (Planning & Validation)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__planner` | Complex workflows | Sequential planning with branching |
| `mcp__pal__consensus` | High-risk decisions | Multi-model validation of approach |
| `mcp__pal__thinkdeep` | Architecture planning | Deep analysis of system design |
| `mcp__pal__chat` | Clarification | Get second opinion on workflow structure |

### PAL Usage Patterns

```bash
# Plan complex workflow
mcp__pal__planner(
    step="Planning authentication system implementation workflow",
    step_number=1,
    total_steps=5,
    is_branch_point=True,
    branch_id="auth-approach-oauth"
)

# Validate architectural decisions
mcp__pal__consensus(
    models=[
        {"model": "gpt-5.2", "stance": "for"},
        {"model": "gemini-3-pro", "stance": "against"},
        {"model": "deepseek", "stance": "neutral"}
    ],
    step="Evaluate: Should auth be microservice or monolith module?"
)

# Deep analysis for enterprise planning
mcp__pal__thinkdeep(
    step="Analyzing compliance requirements for enterprise auth",
    hypothesis="SOC2 requires audit logging at every auth event",
    confidence="medium",
    focus_areas=["compliance", "security", "scalability"]
)
```

### Rube MCP (Project Management)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | Project tools | Find Jira, Asana, Linear, Notion |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Backlog creation | Create tasks, epics, stories |
| `mcp__rube__RUBE_CREATE_PLAN` | Complex workflows | Generate execution plans |
| `mcp__rube__RUBE_CREATE_UPDATE_RECIPE` | Reusable workflows | Save workflow templates |

### Rube Usage Patterns

```bash
# Create backlog items from workflow
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "JIRA_CREATE_ISSUE", "arguments": {
        "project": "AUTH",
        "summary": "Implement OAuth2 provider integration",
        "issue_type": "Epic",
        "description": "## Scope\n- Google OAuth\n- GitHub OAuth\n- SAML support"
    }},
    {"tool_slug": "JIRA_CREATE_ISSUE", "arguments": {
        "project": "AUTH",
        "summary": "Set up JWT token generation",
        "issue_type": "Story",
        "description": "Implement JWT with refresh tokens"
    }},
    {"tool_slug": "JIRA_CREATE_ISSUE", "arguments": {
        "project": "AUTH",
        "summary": "Add rate limiting to auth endpoints",
        "issue_type": "Task"
    }}
])

# Notify team of new workflow
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#project-planning",
        "text": "New implementation workflow created: Authentication System\nEpic: AUTH-123\n5 stories, 12 tasks"
    }},
    {"tool_slug": "NOTION_CREATE_PAGE", "arguments": {
        "title": "Auth System Implementation Plan",
        "content": "## Phases\n1. OAuth Integration\n2. JWT Implementation\n3. Rate Limiting\n\n## Timeline\nSprint 1-3"
    }}
])

# Save workflow as reusable template
mcp__rube__RUBE_CREATE_UPDATE_RECIPE(
    name="Auth System Workflow Template",
    description="Standard workflow for implementing authentication systems",
    workflow_code="..."
)
```

## Flags (Extended)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pal-plan` | bool | false | Use PAL planner for complex workflows |
| `--consensus` | bool | false | Validate approach with multi-model consensus |
| `--create-backlog` | bool | false | Create backlog items via Rube |
| `--notify` | string | - | Notify via Rube (slack, teams, email) |
| `--save-template` | bool | false | Save as reusable Rube recipe |

## Evidence Requirements

This skill does NOT require hard evidence. Deliverables are:
- Structured workflow documentation
- Task dependency maps
- Implementation phases

## Workflow Strategies

### Systematic (`--strategy systematic`)
- Comprehensive task decomposition
- Full dependency mapping
- Documentation-heavy approach

### Agile (`--strategy agile`)
- Sprint-oriented planning
- User story focused
- Iterative milestones

### Enterprise (`--strategy enterprise`)
- Compliance integration
- Stakeholder alignment
- Risk assessment included

## Workflow Components

### Task Decomposition
- Feature breakdown into implementable units
- Clear acceptance criteria
- Effort estimation

### Dependency Mapping
- Task prerequisites
- Blocking relationships
- Parallel execution opportunities

### Quality Gates
- Testing requirements
- Review checkpoints
- Deployment criteria

## Examples

### PRD Analysis
```
/sc:workflow docs/PRD/feature.md --strategy systematic --depth deep
# Full PRD parsing with comprehensive workflow
# Multi-persona coordination for complete plan
```

### Feature Implementation
```
/sc:workflow "payment integration" --strategy agile --parallel
# Sprint-ready task breakdown
# Parallel frontend/backend tracks
```

### Enterprise Planning
```
/sc:workflow enterprise-spec.md --strategy enterprise --validate
# Compliance-aware workflow
# Security and devops integration
```

### Quick Planning
```
/sc:workflow "add search feature" --depth shallow
# Rapid task list generation
# High-level milestone planning
```

## Output Structure

Workflows include:
1. **Overview** - Feature summary and scope
2. **Phases** - Implementation stages
3. **Tasks** - Detailed work items
4. **Dependencies** - Task relationships
5. **Milestones** - Key checkpoints
6. **Risks** - Identified concerns

## Tool Coordination

- **Read/Write** - PRD analysis and documentation
- **TodoWrite** - Progress tracking
- **Task** - Parallel workflow generation
- **WebSearch** - Technology research
