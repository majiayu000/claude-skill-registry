---
name: sc-implement
description: Feature implementation with intelligent persona activation, task orchestration, and MCP integration. Use when implementing features, APIs, components, services, or coordinating multi-agent development. Triggers on requests for code implementation, feature development, or complex task orchestration.
---

# Implementation Skill

Comprehensive feature implementation with coordinated expertise and systematic development.

## Quick Start

```bash
# Basic implementation
/sc:implement [feature-description] --type component|api|service|feature

# With framework
/sc:implement dashboard widget --framework react|vue|express

# Complex orchestration
/sc:implement [task] --orchestrate --strategy systematic|agile|enterprise
```

## Behavioral Flow

1. **Analyze** - Examine requirements, detect technology context
2. **Plan** - Choose approach, activate relevant personas
3. **Generate** - Create implementation with framework best practices
4. **Validate** - Apply security, quality, and principles validation
   - Run KISS validation: `python .claude/skills/sc-principles/scripts/validate_kiss.py --scope-root . --json`
   - Run Purity validation: `python .claude/skills/sc-principles/scripts/validate_purity.py --scope-root . --json`
   - **If blocked**: Refactor code to comply before proceeding
5. **Integrate** - Update docs, provide testing recommendations

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | feature | component, api, service, feature |
| `--framework` | string | auto | react, vue, express, etc. |
| `--safe` | bool | false | Enable safety constraints |
| `--with-tests` | bool | false | Generate tests alongside code |
| `--fast-codex` | bool | false | Streamlined path, skip multi-persona |
| `--orchestrate` | bool | false | Enable hierarchical task breakdown |
| `--strategy` | string | systematic | systematic, agile, enterprise, parallel, adaptive |
| `--delegate` | bool | false | Enable intelligent delegation |
| `--principles` | bool | true | Enable KISS/Purity validation |
| `--strict-principles` | bool | false | Treat principles warnings as errors |

## Personas Activated

- **architect** - System design, architectural decisions
- **frontend** - UI/component implementation
- **backend** - API/service implementation
- **security** - Security validation, auth concerns
- **qa-specialist** - Testing, quality assurance
- **devops** - Infrastructure, deployment
- **project-manager** - Task coordination (with --orchestrate)
- **code-warden** - Principles enforcement (KISS, Purity)

## MCP Integration

### PAL MCP (Always Use for Quality)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__consensus` | Architectural decisions | Multi-model validation before major changes |
| `mcp__pal__codereview` | Code quality | Review implementation quality, security, performance |
| `mcp__pal__precommit` | Before commit | Validate all changes before git commit |
| `mcp__pal__debug` | Implementation issues | Root cause analysis for bugs encountered |
| `mcp__pal__thinkdeep` | Complex features | Multi-stage analysis for complex implementations |
| `mcp__pal__planner` | Large features | Sequential planning for multi-step implementations |
| `mcp__pal__apilookup` | Dependencies | Get current API/SDK documentation |
| `mcp__pal__challenge` | Code review feedback | Critically evaluate review suggestions |

### PAL Usage Patterns

```bash
# Consensus for architectural decision
mcp__pal__consensus(
    models=[
        {"model": "gpt-5.2", "stance": "for"},
        {"model": "gemini-3-pro", "stance": "against"},
        {"model": "deepseek", "stance": "neutral"}
    ],
    step="Evaluate: Should we use Redux or Context API for state management?"
)

# Pre-commit validation
mcp__pal__precommit(
    path="/path/to/repo",
    step="Validating implementation changes",
    findings="Security, performance, completeness checks",
    confidence="high"
)

# Code review after implementation
mcp__pal__codereview(
    review_type="full",
    step="Reviewing new authentication implementation",
    findings="Quality, security, performance, architecture",
    relevant_files=["/src/auth/login.ts", "/src/auth/middleware.ts"]
)

# Debug implementation issue
mcp__pal__debug(
    step="Investigating why API returns 500 on edge case",
    hypothesis="Null check missing for optional field",
    confidence="medium"
)
```

### Rube MCP (Automation & Integration)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | External services | Find APIs, SDKs, integrations |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | CI/CD, notifications | Trigger builds, notify team, update tickets |
| `mcp__rube__RUBE_REMOTE_WORKBENCH` | Code generation | Bulk code operations, transformations |
| `mcp__rube__RUBE_CREATE_UPDATE_RECIPE` | Reusable workflows | Save implementation patterns as recipes |
| `mcp__rube__RUBE_MANAGE_CONNECTIONS` | Verify integrations | Ensure external service connections |

### Rube Usage Patterns

```bash
# Search for integration tools
mcp__rube__RUBE_SEARCH_TOOLS(queries=[
    {"use_case": "send slack message", "known_fields": "channel_name:dev-updates"},
    {"use_case": "create github pull request", "known_fields": "repo:myapp"}
])

# Notify team and update ticket on completion
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#dev-updates",
        "text": "Feature implemented: User authentication flow"
    }},
    {"tool_slug": "JIRA_UPDATE_ISSUE", "arguments": {
        "issue_key": "PROJ-123",
        "status": "In Review"
    }},
    {"tool_slug": "GITHUB_CREATE_PULL_REQUEST", "arguments": {
        "repo": "myapp",
        "title": "feat: Add user authentication",
        "base": "main",
        "head": "feature/auth"
    }}
])

# Save implementation workflow as recipe
mcp__rube__RUBE_CREATE_UPDATE_RECIPE(
    name="Feature Implementation Workflow",
    description="Standard flow for implementing features with notifications",
    workflow_code="..."
)
```

### MCP-Powered Loop Mode

When `--loop` is enabled, MCP tools are used between iterations:

1. **Iteration N** - Implement feature
2. **PAL codereview** - Assess quality (target: 70+ score)
3. **PAL debug** - Investigate any issues found
4. **Iteration N+1** - Apply improvements
5. **PAL precommit** - Final validation before marking complete

## Guardrails

- Start in analysis mode; produce scoped plan before touching files
- Only mark complete when referencing concrete repo changes (filenames + diff hunks)
- Return plan + next actions if tooling unavailable
- Prefer minimal viable change; skip speculative scaffolding
- Escalate to security persona before modifying auth/secrets/permissions

## Evidence Requirements

This skill requires evidence. You MUST:
- Show actual file diffs or code changes
- Reference test results or lint output
- Never claim code exists without proof

## Examples

### React Component
```
/sc:implement user profile component --type component --framework react
```

### API with Tests
```
/sc:implement user auth API --type api --safe --with-tests
```

### Complex Orchestration
```
/sc:implement "enterprise auth system" --orchestrate --strategy systematic --delegate
```

## Loop Mode & Learning

When using `--loop`, this skill integrates with the skill persistence layer for cross-session learning:

### How Learning Works

1. **Feedback Recording** - Each iteration's quality scores and improvements are persisted
2. **Skill Extraction** - Successful patterns are extracted when quality threshold is met
3. **Skill Retrieval** - Relevant learned skills are injected into subsequent tasks
4. **Effectiveness Tracking** - Applied skills are tracked for success rate

### Loop Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--loop` | int | 3 | Enable iterative improvement (max 5) |
| `--learn` | bool | true | Enable learning from this session |
| `--auto-promote` | bool | false | Auto-promote high-quality skills |

### Example with Learning

```bash
# Iterative implementation with learning
/sc:implement auth flow --loop 3 --learn

# View learned skills
python scripts/skill_learn.py '{"command": "stats"}'

# Retrieve relevant skills
python scripts/skill_learn.py '{"command": "retrieve", "task": "auth"}'
```

### Learned Skills Location

Promoted skills are stored in:
```
.claude/skills/learned/
├── SKILL.md                    # Index
├── learned-backend-auth/       # Example promoted skill
│   ├── SKILL.md
│   └── metadata.json
```

## Resources

- [PERSONAS.md](PERSONAS.md) - Available persona definitions
- [scripts/select_agent.py](scripts/select_agent.py) - Agent selection logic
- [scripts/evidence_gate.py](scripts/evidence_gate.py) - Evidence validation
- [scripts/skill_learn.py](scripts/skill_learn.py) - Skill learning management
