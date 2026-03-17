---
name: Execution Workflow
description: This skill should be used when the user asks to "execute task", "implement feature", "delegate work", "run workflow", "review code", "code quality check", or needs task orchestration and code review guidance. Provides execution, delegation, and code review patterns.
---

# Task Execution and Code Review Patterns

## Delegation Principles

### Parallel vs Sequential
- **Parallel**: Independent tasks (quality + security, test + docs when independent)
- **Sequential**: Tasks with data dependencies; verify outputs before dependent tasks start

### Delegation Context
Sub-agents need:
- Specific scope and expected deliverables
- Target file paths
- MCP tool usage instructions
- Reference implementations
- Memory patterns from Serena

## Code Review Phases

### Phase 1: Initial Scan
- Syntax errors and typos
- Missing imports/dependencies
- Obvious logic errors
- Code style violations

### Phase 2: Deep Analysis
- Algorithm correctness
- Edge case handling
- Error handling completeness
- Resource management

### Phase 3: Context Evaluation
- Breaking changes to public APIs
- Side effects on existing functionality
- Dependency compatibility

### Phase 4: Standards Compliance
- Naming conventions
- Documentation requirements
- Test coverage

## Feedback Categories

| Priority | Category | Examples |
|----------|----------|----------|
| Critical | Must fix | Security vulnerabilities, data corruption, breaking changes |
| Important | Should fix | Logic errors, missing error handling, performance issues |
| Suggestion | Nice to have | Code style, refactoring, documentation |
| Positive | Done well | Good patterns, clever solutions, thorough testing |

## Review Output Format
```
Summary: [overall assessment]
Critical Issues: [must-fix with file:line refs]
Important Issues: [should-fix items]
Suggestions: [optional improvements]
Positive Feedback: [good practices observed]
```

## Critical Rules
- Execute independent tasks in parallel
- Never parallelize tasks with data dependencies
- Verify sub-agent outputs before integration
- Balance critical feedback with positive observations
- Provide file:line references for all issues
