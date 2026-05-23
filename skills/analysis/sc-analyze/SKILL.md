---
name: sc-analyze
description: Comprehensive code analysis, quality assessment, and issue diagnosis. Use when analyzing code quality, security vulnerabilities, performance bottlenecks, architecture reviews, or troubleshooting bugs and build failures.
---

# Analysis & Troubleshooting Skill

Multi-domain code analysis with issue diagnosis and resolution capabilities.

## Quick Start

```bash
# Quality analysis
/sc:analyze [target] --focus quality|security|performance|architecture

# Troubleshooting mode
/sc:analyze [issue] --troubleshoot --focus bug|build|performance|deployment

# With auto-fix
/sc:analyze "TypeScript errors" --troubleshoot --focus build --fix
```

## Behavioral Flow

1. **Discover** - Categorize source files, detect languages
2. **Scan** - Apply domain-specific analysis techniques
3. **Evaluate** - Generate prioritized findings with severity
4. **Recommend** - Create actionable recommendations
5. **Report** - Present comprehensive analysis with metrics

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--focus` | string | quality | quality, security, performance, architecture, bug, build, deployment |
| `--troubleshoot` | bool | false | Enable issue diagnosis mode |
| `--trace` | bool | false | Detailed trace analysis for debugging |
| `--fix` | bool | false | Auto-apply safe fixes |
| `--depth` | string | standard | quick, standard, deep |
| `--format` | string | text | text, json, report |

## Analysis Domains

### Quality Analysis
- Code smells and maintainability issues
- Pattern violations and anti-patterns
- Technical debt assessment

### Security Analysis
- Vulnerability scanning
- Compliance validation
- Authentication/authorization review

### Performance Analysis
- Bottleneck identification
- Resource utilization patterns
- Optimization opportunities

### Architecture Analysis
- Component coupling assessment
- Dependency analysis
- Design pattern evaluation

## Troubleshooting Mode

When `--troubleshoot` is enabled:

| Focus | Behavior |
|-------|----------|
| bug | Error analysis, stack traces, code inspection |
| build | Build logs, dependencies, config validation |
| performance | Metrics analysis, bottleneck identification |
| deployment | Environment analysis, service validation |

## Examples

### Security Deep Dive
```
/sc:analyze src/auth --focus security --depth deep
```

### Build Failure Fix
```
/sc:analyze "compilation errors" --troubleshoot --focus build --fix
```

### Performance Diagnosis
```
/sc:analyze "slow API response" --troubleshoot --focus performance --trace
```

## MCP Integration

### PAL MCP (Always Use)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__thinkdeep` | Complex issues | Multi-stage investigation with hypothesis testing |
| `mcp__pal__debug` | Bug troubleshooting | Systematic root cause analysis |
| `mcp__pal__codereview` | Quality analysis | Comprehensive code quality, security, performance review |
| `mcp__pal__consensus` | Critical findings | Multi-model validation of security/architecture issues |
| `mcp__pal__challenge` | Uncertain findings | Force critical thinking on ambiguous issues |
| `mcp__pal__apilookup` | Dependency issues | Get current API docs for version conflicts |

### PAL Usage Patterns

```bash
# Deep investigation (--depth deep)
mcp__pal__thinkdeep(
    step="Investigating performance bottleneck in API layer",
    hypothesis="Database queries lack proper indexing",
    confidence="medium",
    relevant_files=["/src/api/users.py"]
)

# Security analysis (--focus security)
mcp__pal__codereview(
    review_type="security",
    findings="Authentication, authorization, injection vectors",
    issues_found=[{"severity": "high", "description": "SQL injection risk"}]
)

# Critical finding validation
mcp__pal__consensus(
    models=[
        {"model": "gpt-5.2", "stance": "for"},
        {"model": "gemini-3-pro", "stance": "against"}
    ],
    step="Evaluate: Is this a critical security vulnerability?"
)
```

### Rube MCP (When Needed)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | External analysis | Find security scanners, linters |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Issue tracking | Create tickets for findings |
| `mcp__rube__RUBE_REMOTE_WORKBENCH` | Bulk analysis | Process large codebases |

### Rube Usage Patterns

```bash
# Find and create Jira tickets for findings
mcp__rube__RUBE_SEARCH_TOOLS(queries=[
    {"use_case": "create jira issue", "known_fields": "project:SECURITY"}
])

# Notify team of critical findings
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {"channel": "#security", "text": "Critical finding..."}}
])
```

## Flags (Extended)

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--pal-deep` | bool | false | Use PAL thinkdeep for multi-stage analysis |
| `--pal-review` | bool | false | Use PAL codereview for comprehensive review |
| `--consensus` | bool | false | Use PAL consensus for critical findings |
| `--notify` | string | - | Notify via Rube (slack, jira, email) |
| `--create-tickets` | bool | false | Create tickets for findings via Rube |

## Tool Coordination

- **Glob** - File discovery and structure analysis
- **Grep** - Pattern analysis and code search
- **Read** - Source inspection and config analysis
- **Bash** - External tool execution
- **Write** - Report generation
- **PAL MCP** - Multi-model analysis, debugging, code review
- **Rube MCP** - External notifications, ticket creation
