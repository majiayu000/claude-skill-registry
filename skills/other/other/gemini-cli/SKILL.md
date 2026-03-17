---
name: gemini-cli
description: Use Gemini CLI as a complementary AI tool for tasks requiring massive context windows (1M tokens). Invoke when analyzing large codebases, requesting deep analysis with extended thinking, getting second opinions on complex problems, or when Claude's context limits are insufficient. Triggers include phrases like "use gemini", "analyze with gemini", "get second opinion", "deep analysis of codebase", or when processing files exceeding Claude's context capacity.
---

# Gemini CLI Integration

Gemini CLI provides access to Google's Gemini models with 1 million token context windows directly from the terminal. Use it as a complementary tool for tasks where extended context or alternative perspectives add value.

## Core Use Cases

1. **Large codebase analysis** - Analyze entire repositories that exceed Claude's context
2. **Deep thinking tasks** - Extended reasoning on complex architectural decisions
3. **Second opinions** - Cross-validate Claude's analysis on critical problems
4. **Bulk file processing** - Process multiple files in a single context

## Quick Reference

```bash
# Basic one-shot query
gemini "Explain this codebase architecture"

# Interactive mode (continue conversation)
gemini -i "Start analyzing this project"

# Auto-approve file operations (use carefully)
gemini --approval-mode yolo "Refactor all deprecated API calls"

# Specify model explicitly
gemini -m gemini-2.5-pro "Complex analysis task"

# Include additional directories
gemini --include-directories ./libs,./shared "Analyze dependencies"

# Resume previous session
gemini --resume latest
gemini --resume 3

# List available sessions
gemini --list-sessions

# Use EOF pattern for multi-line prompt input
gemini <<'__GEMINI_PROMPT__'
... your prompt including any EOF, code fences, rich formatting, etc ...
__GEMINI_PROMPT__
```

## Workflow Patterns

### Pattern 1: Codebase Analysis

Run `scripts/analyze_codebase.sh` for comprehensive codebase review:

```bash
./scripts/analyze_codebase.sh /path/to/project "Focus on security vulnerabilities"
```

Or manually:

```bash
cd /path/to/project
gemini "Analyze this codebase. Focus on:
1. Architecture patterns and anti-patterns
2. Code quality issues
3. Security concerns
4. Performance bottlenecks
5. Improvement recommendations"
```

### Pattern 2: Second Opinion

When Claude has provided an analysis, seek Gemini's perspective:

```bash
gemini "I received this analysis from another AI:
---
[paste Claude's analysis]
---

Review this analysis critically. Identify:
- Points you agree with and why
- Points you disagree with and alternatives
- Gaps or missing considerations
- Additional recommendations"
```

### Pattern 3: Deep Reasoning

For complex architectural decisions requiring extended thinking:

```bash
gemini -i "I need deep analysis on migrating from monolith to microservices.

Context:
- Current: Java monolith, 500k LOC, PostgreSQL
- Team: 15 developers, 3 teams
- Traffic: 10k req/sec peak

Think through:
1. Service boundary identification
2. Data decomposition strategy  
3. Migration sequence
4. Risk assessment
5. Timeline estimation"
```

### Pattern 4: Interactive Exploration

For iterative analysis requiring conversation:

```bash
gemini -i "Let's explore the design options for this system"
```

Continue with follow-up questions in the interactive session.

## Approval Modes

| Mode      | Flag                           | Behavior                                |
| --------- | ------------------------------ | --------------------------------------- |
| Default   | (none)                         | Prompts for each file operation         |
| Auto-edit | `--approval-mode auto_edit`    | Auto-approves edits, prompts for others |
| YOLO      | `--approval-mode yolo` or `-y` | Auto-approves all operations            |

**Recommendation**: Use default mode for analysis. Use `auto_edit` for refactoring tasks with review. Reserve `yolo` for well-understood, reversible operations.

## Output Formats

```bash
# Standard text (default, best for reading)
gemini -o text "query"

# JSON (for programmatic processing)
gemini -o json "query"

# Streaming JSON (for real-time integration)
gemini -o stream-json "query"
```

## Session Management

Gemini maintains conversation sessions that can be resumed:

```bash
# List available sessions
gemini --list-sessions

# Resume most recent session
gemini --resume latest

# Resume specific session by index
gemini --resume 5

# Delete a session
gemini --delete-session 3
```

## MCP Server Integration

Gemini supports Model Context Protocol (MCP) servers for extended capabilities:

```bash
# Manage MCP servers
gemini mcp

# Allow specific MCP servers
gemini --allowed-mcp-server-names server1,server2 "query"
```

## Best Practices

1. **Scope appropriately** - Don't dump entire monorepos; focus on relevant modules
2. **Provide context** - Include problem background, constraints, and goals
3. **Be specific** - Vague queries yield vague responses
4. **Use interactive mode** - For exploratory analysis requiring iteration
5. **Review before auto-approve** - Understand what `yolo` mode will execute
6. **Combine perspectives** - Use Gemini's analysis alongside Claude's for critical decisions

## When to Use Gemini vs Claude

| Scenario                           | Recommended |
| ---------------------------------- | ----------- |
| Quick code questions               | Claude      |
| Small file analysis                | Claude      |
| Interactive coding assistance      | Claude      |
| Massive codebase review            | Gemini      |
| Cross-validating critical analysis | Gemini      |
| Multi-file refactoring decisions   | Gemini      |
| Analysis exceeding 100k tokens     | Gemini      |

## Troubleshooting

**Context too large**: Split analysis into focused modules rather than entire repository.

**Session lost**: Use `--list-sessions` to find previous sessions, `--resume` to continue.

**Slow responses**: Large context requires processing time. Consider narrowing scope.

**API errors**: Verify Gemini CLI authentication with `gemini --version` and check Google Cloud credentials.
