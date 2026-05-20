---
name: sc-test
description: Execute tests with coverage analysis and automated quality reporting. Use when running unit tests, integration tests, e2e tests, analyzing coverage, or debugging test failures.
---

# Testing & QA Skill

Test execution with coverage analysis and quality reporting.

## Quick Start

```bash
# Run all tests
/sc:test

# Unit tests with coverage
/sc:test src/components --type unit --coverage

# Watch mode with auto-fix
/sc:test --watch --fix

# Web search for testing guidance (uses Rube MCP's LINKUP_SEARCH)
/sc:test --linkup --query "pytest asyncio best practices"
```

## Behavioral Flow

1. **Discover** - Categorize tests using runner patterns
2. **Configure** - Set up test environment and parameters
3. **Execute** - Run tests with real-time progress tracking
4. **Analyze** - Generate coverage reports and diagnostics
5. **Report** - Provide recommendations and quality metrics

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | all | unit, integration, e2e, all |
| `--coverage` | bool | false | Generate coverage report |
| `--watch` | bool | false | Continuous watch mode |
| `--fix` | bool | false | Auto-fix simple failures |
| `--linkup` | bool | false | Web search for guidance (via Rube MCP) |
| `--query` | string | - | Search query for LINKUP_SEARCH |

## Personas Activated

- **qa-specialist** - Test analysis and quality assessment

## MCP Integration

### PAL MCP (Quality & Debugging)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__debug` | Test failures | Root cause analysis for failing tests |
| `mcp__pal__codereview` | Test quality | Review test coverage and quality |
| `mcp__pal__thinkdeep` | Complex failures | Multi-stage investigation of flaky tests |
| `mcp__pal__consensus` | Test strategy | Multi-model validation of testing approach |
| `mcp__pal__apilookup` | Framework docs | Get current testing framework documentation |

### PAL Usage Patterns

```bash
# Debug failing test
mcp__pal__debug(
    step="Investigating intermittent test failure",
    hypothesis="Race condition in async setup",
    confidence="medium",
    relevant_files=["/tests/test_api.py"]
)

# Review test quality
mcp__pal__codereview(
    review_type="full",
    findings="Test coverage, assertion quality, edge cases",
    focus_on="test isolation and mocking patterns"
)

# Validate testing strategy
mcp__pal__consensus(
    models=[{"model": "gpt-5.2", "stance": "neutral"}, {"model": "gemini-3-pro", "stance": "neutral"}],
    step="Evaluate: Is integration testing sufficient for this feature?"
)
```

### Rube MCP (Automation & Research)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | CI/CD integration | Find test reporting tools |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Notifications | Post results to Slack, update tickets |
| `mcp__rube__RUBE_REMOTE_WORKBENCH` | Bulk processing | Analyze large test result sets |

### Rube Usage Patterns

```bash
# Search for testing best practices (--linkup flag uses LINKUP_SEARCH)
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "LINKUP_SEARCH", "arguments": {
        "query": "pytest fixtures best practices",
        "depth": "deep",
        "output_type": "sourcedAnswer"
    }}
])

# Post test results to Slack
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#ci-results",
        "text": "Test run complete: 95% pass rate, 87% coverage"
    }}
])

# Update Jira with test status
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "JIRA_ADD_COMMENT", "arguments": {
        "issue_key": "PROJ-123",
        "body": "All tests passing. Ready for review."
    }}
])

## Evidence Requirements

This skill requires evidence. You MUST:
- Show test execution output and pass/fail counts
- Reference coverage metrics when `--coverage` used
- Provide actual error messages for failures

## Test Types

### Unit Tests (`--type unit`)
- Isolated component testing
- Mock dependencies
- Fast execution

### Integration Tests (`--type integration`)
- Component interaction testing
- Database/API integration
- Service dependencies

### E2E Tests (`--type e2e`)
- Full user flow testing
- Browser automation guidance
- Cross-platform validation

## Coverage Analysis

When `--coverage` is enabled:
- Line coverage metrics
- Branch coverage metrics
- Uncovered code identification
- Coverage trend comparison

## Examples

### Targeted Unit Tests
```
/sc:test src/utils --type unit --coverage
```

### Continuous Development
```
/sc:test --watch --fix
# Real-time feedback during development
```

### Integration Suite
```
/sc:test --type integration --coverage
```

### Web Research
```
/sc:test --linkup --query "vitest react testing library patterns"
```

## Tool Coordination

- **Bash** - Test runner execution
- **Glob** - Test file discovery
- **Grep** - Result parsing, failure analysis
- **Write** - Coverage reports, test summaries
