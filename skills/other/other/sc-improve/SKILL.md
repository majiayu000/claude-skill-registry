---
name: sc-improve
description: Apply systematic improvements to code quality, performance, maintainability, and cleanup. Use when refactoring code, optimizing performance, removing dead code, or improving project structure.
---

# Code Improvement & Cleanup Skill

Systematic improvements with multi-persona expertise and safety validation.

## Quick Start

```bash
# Quality improvement
/sc:improve src/ --type quality --safe

# Performance optimization
/sc:improve api-endpoints --type performance

# Dead code cleanup
/sc:improve src/ --cleanup --type code --safe

# Import optimization
/sc:improve --cleanup --type imports
```

## Behavioral Flow

1. **Analyze** - Examine codebase for improvement opportunities
2. **Plan** - Choose approach and activate relevant personas
3. **Execute** - Apply systematic improvements
4. **Validate** - Ensure functionality preservation
5. **Document** - Generate improvement summary

## Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--type` | string | quality | quality, performance, maintainability, style, principles, code, imports, files, all |
| `--cleanup` | bool | false | Enable cleanup mode |
| `--safe` | bool | true | Conservative with safety validation |
| `--aggressive` | bool | false | Thorough cleanup (use with caution) |
| `--preview` | bool | false | Show changes without applying |
| `--interactive` | bool | false | Guided decision mode |

## Personas Activated

- **architect** - Structure and design improvements
- **performance** - Optimization expertise
- **quality** - Code quality and maintainability
- **security** - Security pattern application
- **code-warden** - KISS and Purity enforcement (with --type principles)

## MCP Integration

### PAL MCP (Validation & Analysis)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__pal__consensus` | Complex refactors | Multi-model validation before major changes |
| `mcp__pal__codereview` | Quality assessment | Review improvement quality and safety |
| `mcp__pal__thinkdeep` | Architecture changes | Deep analysis of structural improvements |
| `mcp__pal__precommit` | Before commit | Validate all changes preserve functionality |
| `mcp__pal__debug` | Regression issues | Root cause analysis if improvements break things |
| `mcp__pal__challenge` | Aggressive mode | Critical evaluation of aggressive cleanup decisions |

### PAL Usage Patterns

```bash
# Consensus for major refactor
mcp__pal__consensus(
    models=[
        {"model": "gpt-5.2", "stance": "for"},
        {"model": "gemini-3-pro", "stance": "against"}
    ],
    step="Evaluate: Should we extract this into a separate module?"
)

# Review after improvements
mcp__pal__codereview(
    review_type="full",
    step="Reviewing code improvements",
    findings="Quality, maintainability, backwards compatibility",
    relevant_files=["/src/refactored/module.py"]
)

# Pre-commit validation
mcp__pal__precommit(
    path="/path/to/repo",
    step="Validating refactoring changes",
    confidence="high"
)
```

### Rube MCP (Automation & Tracking)

| Tool | When to Use | Purpose |
|------|-------------|---------|
| `mcp__rube__RUBE_SEARCH_TOOLS` | External tools | Find linters, formatters, analyzers |
| `mcp__rube__RUBE_MULTI_EXECUTE_TOOL` | Notifications | Update tickets, notify team |
| `mcp__rube__RUBE_CREATE_UPDATE_RECIPE` | Reusable workflows | Save improvement patterns |

### Rube Usage Patterns

```bash
# Notify team of improvements
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "SLACK_SEND_MESSAGE", "arguments": {
        "channel": "#refactoring",
        "text": "Completed: Dead code cleanup removed 500 lines"
    }},
    {"tool_slug": "JIRA_UPDATE_ISSUE", "arguments": {
        "issue_key": "TECH-456",
        "status": "Done"
    }}
])

# Create improvement report in Notion
mcp__rube__RUBE_MULTI_EXECUTE_TOOL(tools=[
    {"tool_slug": "NOTION_CREATE_PAGE", "arguments": {
        "title": "Refactoring Report - Q4 2025",
        "content": "## Summary\n- Lines removed: 500\n- Complexity reduced: 25%"
    }}
])
```

## Evidence Requirements

This skill requires evidence. You MUST:
- Show before/after code comparisons
- Run tests to verify functionality preservation
- Report metrics (lines removed, complexity reduction)

## Improvement Types

### Quality (`--type quality`)
- Technical debt reduction
- Code structure improvements
- Readability enhancements

### Performance (`--type performance`)
- Bottleneck resolution
- Algorithm optimization
- Resource efficiency

### Maintainability (`--type maintainability`)
- Complexity reduction
- Documentation improvements
- Modular restructuring

### Style (`--type style`)
- Formatting consistency
- Naming conventions
- Pattern alignment

### Principles (`--type principles`)
- KISS compliance improvements (reduce complexity, extract methods)
- Purity enforcement (separate I/O from logic)
- Guard clause refactoring (reduce nesting)
- Functional core extraction (move I/O to shell layer)

**Validators:**
```bash
# Run KISS validation
python .claude/skills/sc-principles/scripts/validate_kiss.py --scope-root . --json

# Run Purity validation
python .claude/skills/sc-principles/scripts/validate_purity.py --scope-root . --json
```

## Cleanup Mode (`--cleanup`)

### Code Cleanup (`--type code`)
- Dead code detection and removal
- Unused variable elimination
- Unreachable code removal

### Import Cleanup (`--type imports`)
- Unused import removal
- Import organization
- Dependency optimization

### File Cleanup (`--type files`)
- Empty file removal
- Orphaned file detection
- Structure optimization

### Full Cleanup (`--type all`)
- Comprehensive cleanup
- All categories combined
- Multi-persona coordination

## Safety Modes

### Safe Mode (`--safe`)
- Conservative changes only
- Automatic safety validation
- Preserves all functionality

### Aggressive Mode (`--aggressive`)
- Thorough cleanup
- Framework-aware patterns
- Requires careful review

## Examples

### Safe Quality Improvement
```
/sc:improve src/ --type quality --safe
# Technical debt reduction with safety validation
```

### Performance Optimization
```
/sc:improve api-endpoints --type performance --interactive
# Guided optimization with profiling analysis
```

### Dead Code Cleanup
```
/sc:improve src/ --cleanup --type code --safe
# Remove unused code with dependency validation
```

### Preview Changes
```
/sc:improve --cleanup --type imports --preview
# Show what would be removed without executing
```

## Tool Coordination

- **Read/Grep/Glob** - Code analysis
- **Edit/MultiEdit** - Safe modifications
- **TodoWrite** - Progress tracking
- **Task** - Large-scale improvement delegation
