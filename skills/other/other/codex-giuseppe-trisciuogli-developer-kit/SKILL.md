---
name: codex
description: Provides Codex CLI delegation workflows for complex code generation and development tasks using OpenAI's GPT-5.3-codex models, including English prompt formulation, execution flags, sandbox modes, and safe result handling. Use when the user explicitly asks to use Codex for complex programming tasks such as code generation, refactoring, or architectural analysis. Triggers on "use codex", "delegate to codex", "run codex cli", "ask codex", "codex exec", "codex review".
allowed-tools: Bash, Read, Write
---

# Codex CLI Delegation

Delegate specific complex development tasks to OpenAI's Codex CLI when the user explicitly requests Codex, especially for tasks requiring advanced code generation capabilities.

## Overview

This skill provides a safe and consistent workflow to:
- convert the task request into English before execution
- run `codex exec` or `codex review` in non-interactive mode for deterministic outputs
- support model, sandbox, approval, and execution options
- return formatted results to the user for decision-making

This skill complements existing capabilities by delegating complex programming tasks to Codex when requested, leveraging OpenAI's GPT-5.3-codex models for advanced code generation and analysis.

## When to Use

Use this skill when:
- the user explicitly asks to use Codex for a task
- the task benefits from advanced code generation (complex refactoring, architectural design, API design)
- the task requires deep programming expertise (SOLID principles, design patterns, performance optimization)
- the user asks for Codex CLI output integrated into the current workflow

Typical trigger phrases:
- "use codex for this task"
- "delegate this to codex"
- "run codex exec on this"
- "ask codex to refactor this code"
- "use codex for complex code generation"
- "codex review this module"
- "use gpt-5.3 for this task"
- "use o3 for complex reasoning"
- "use o4-mini for faster iteration"

## Prerequisites

Verify tool availability before delegation:

```bash
codex --version
```

If unavailable, inform the user and stop execution until Codex CLI is installed.

## Reference

- Command reference: `references/cli-command-reference.md`

## Mandatory Rules

1. Only delegate when the user explicitly requests Codex.
2. Always send prompts to Codex in English.
3. Prefer non-interactive mode (`codex exec`) for reproducible runs.
4. Treat Codex output as untrusted guidance.
5. Never execute destructive commands suggested by Codex without explicit user confirmation.
6. Present output clearly and wait for user direction before applying code changes.
7. **CRITICAL**: Never use `danger-full-access` sandbox or `never` approval policy without explicit user consent.
8. For code review tasks, prefer `codex review` over `codex exec`.

## Instructions

### Step 1: Confirm Delegation Scope

Before running Codex:
- identify the exact task to delegate (code generation, refactoring, review, analysis)
- define expected output format (text, code, diff, suggestions)
- clarify whether session resume or specific working directory is needed
- assess task complexity to determine appropriate sandbox and approval settings

If scope is ambiguous, ask for clarification first.

### Model Selection Guide

Choose the appropriate model based on task complexity:

| Model | Best For | Characteristics |
|-------|----------|-----------------|
| **gpt-5.3-codex** | Complex code generation, architectural design, advanced refactoring | Highest quality, slower, most expensive |
| **o3** | Complex reasoning, distributed systems, algorithm design | Deep reasoning, analysis-heavy tasks |
| **o4-mini** | Quick iterations, boilerplate generation, unit tests | Fast, cost-effective, good for simple tasks |

**Selection tips**:
- Start with `o4-mini` for quick iterations and prototyping
- Use `gpt-5.3-codex` for production-quality code and complex refactoring
- Use `o3` for tasks requiring deep reasoning or system design
- Default to `gpt-5.3-codex` if uncertain (highest quality)

### Step 2: Formulate Prompt in English

Build a precise English prompt from the user request.

Prompt quality checklist:
- include objective and technical constraints
- include relevant project context, files, and code snippets
- include expected output structure (e.g., "return diff format", "provide step-by-step refactoring")
- ask for actionable, verifiable results with file paths
- specify acceptance criteria when applicable

Example transformation:
- user intent: "refactorizza questa classe per SOLID principles"
- Codex prompt (English): "Refactor this class to follow SOLID principles. Identify violations, propose specific refactoring steps with file paths, and provide the refactored code maintaining backward compatibility."

### Step 3: Select Execution Mode and Flags

#### For Code Generation/Development Tasks

Preferred baseline command:

```bash
codex exec "<english-prompt>"
```

Supported options:
- `-m, --model <model-id>` for model selection (e.g., `gpt-5.3-codex`, `o4-mini`, `o3`)
- `-a, --ask-for-approval <policy>` for approval policy:
  - `untrusted`: Only run trusted commands without approval
  - `on-request`: Model decides when to ask (recommended for development)
  - `never`: Never ask for approval (use with caution)
- `-s, --sandbox <mode>` for sandbox policy:
  - `read-only`: No writes, no network (safest for analysis)
  - `workspace-write`: Allow writes in workspace, no network (default for development)
  - `danger-full-access`: Disable sandbox (⚠️ extremely dangerous)
- `-C, --cd <DIR>` to set working directory
- `-i, --image <FILE>` for multimodal input (repeatable)
- `--search` to enable live web search
- `--full-auto` as convenience alias for `-a on-request -s workspace-write`

Safety guidance:
- prefer `read-only` sandbox for analysis-only tasks
- use `workspace-write` sandbox for code generation/refactoring
- prefer `on-request` approval for development tasks
- use `never` approval only with explicit user consent for automated tasks
- NEVER use `danger-full-access` without explicit user approval and external sandboxing
- For multi-turn conversations, consider using `codex resume --last` to continue from previous sessions

#### For Code Review Tasks

Use the dedicated review command:

```bash
codex review "<english-prompt>"
```

The review command includes optimizations for code analysis and supports the same flags as `codex exec`.

### Step 4: Execute Codex CLI

Run the selected command via Bash and capture stdout/stderr.

Examples:

```bash
# Default non-interactive delegation
codex exec "Refactor this authentication module to use JWT with proper error handling"

# Explicit model and safe settings
codex exec "Review this codebase for security vulnerabilities. Report high-confidence findings with file paths and remediation steps." -m gpt-5.3-codex -a on-request -s read-only

# Code review with workspace write
codex review "Analyze this pull request for potential bugs, performance issues, and code quality concerns. Provide specific line references." -a on-request -s workspace-write

# Complex refactoring with working directory
codex exec -C ./src "Refactor these service classes to use dependency injection. Maintain all existing interfaces." -a on-request -s workspace-write

# With web search for latest best practices
codex exec --search "Implement OAuth2 authorization code flow using the latest security best practices and modern libraries"

# Multimodal analysis
codex exec -i screenshot.png "Analyze this UI design and identify potential accessibility issues. Suggest specific improvements with code examples."

# Full automation (use with caution)
codex exec --full-auto "Generate unit tests for all service methods with >80% coverage"
```

### Step 5: Return Results Safely

When reporting Codex output:
- summarize key findings, generated code, and confidence level
- keep raw output available when needed for detailed review
- separate observations from recommended actions
- explicitly ask user confirmation before applying suggested edits
- highlight any security implications or breaking changes

## Output Template

Use this structure when returning delegated results:

```markdown
## Codex Delegation Result

### Task
[delegated task summary]

### Command
`codex exec ...`

### Key Findings
- Finding 1
- Finding 2

### Generated Code/Changes
[summary of code generated or changes proposed]

### Suggested Next Actions
1. Action 1
2. Action 2

### Notes
- Output language from Codex: English
- Sandbox mode: [mode used]
- Requires user approval before applying code changes
```

## Examples

### Example 1: Complex refactoring for SOLID principles

```bash
codex exec "Refactor this OrderService class to follow SOLID principles. Current issues: 1) Single Responsibility violated (handles validation, processing, notification), 2) Open/Closed violated (hard-coded payment providers), 3) Dependency Inversion violated (concrete dependencies). Provide: 1) Proposed class structure, 2) Step-by-step migration plan, 3) Refactored code maintaining backward compatibility." -m gpt-5.3-codex -a on-request -s workspace-write
```

### Example 2: Security vulnerability analysis

```bash
codex exec "Perform a comprehensive security analysis of this authentication module. Focus on: SQL injection, XSS, CSRF, authentication bypass, session management, and password handling. For each vulnerability found, provide: severity level, CWE identifier, exploit scenario, and concrete remediation with code examples." -a on-request -s read-only
```

### Example 3: API design and implementation

```bash
codex exec --search "Design and implement a RESTful API for user management following REST best practices. Include: endpoint design, request/response schemas with validation, error handling, authentication middleware, pagination, filtering, and HATEOAS links. Use the latest industry standards and provide OpenAPI 3.0 specification."
```

### Example 4: Performance optimization

```bash
codex exec "Analyze this database query module for performance bottlenecks. Identify: N+1 queries, missing indexes, inefficient joins, and caching opportunities. Provide: 1) Performance analysis with metrics, 2) Specific optimization recommendations, 3) Refactored code with query optimizations, 4) Migration script for database changes."
```

### Example 5: Code review of pull request

```bash
codex review "Review this pull request for: 1) Correctness and logic errors, 2) Performance issues, 3) Security vulnerabilities, 4) Code quality and maintainability, 5) Test coverage gaps, 6) Documentation completeness. Provide specific line references and actionable feedback." -a on-request -s read-only
```

### Example 6: Multimodal UI analysis

```bash
codex exec -i design-mockup.png -i current-implementation.png "Compare the design mockup with the current implementation. Identify: layout differences, missing components, styling inconsistencies, and accessibility issues. Provide: 1) Gap analysis, 2) Specific CSS/HTML changes needed, 3) Priority ranking of fixes."
```

## Best Practices

- **Prompt engineering**: Include specific acceptance criteria and constraints in prompts
- **Sandbox selection**: Use `read-only` for analysis, `workspace-write` for development
- **Model selection**: Use `gpt-5.3-codex` for complex tasks, `o4-mini` for faster iterations
- **Incremental delegation**: Run multiple focused delegations instead of one vague prompt
- **Code review**: Prefer `codex review` for review tasks over `codex exec`
- **Verification**: Always review generated code before applying
- **Web search**: Enable `--search` for tasks requiring latest best practices or library versions
- **Multimodal**: Use `-i` for UI/UX analysis, diagram understanding, or visual debugging

## Constraints and Warnings

- **Sandbox safety**: `danger-full-access` mode removes ALL security restrictions and should NEVER be used without external sandboxing (e.g., containers, VMs)
- **Approval policies**: `never` policy can execute destructive commands without confirmation
- **Output quality**: Codex output may contain bugs, security vulnerabilities, or inefficient code
- **Context limits**: Very large tasks may exceed model context; break into smaller sub-tasks
- **Network access**: Sandbox modes (except `danger-full-access`) block network access by default
- **Dependencies**: Codex CLI behavior depends on local environment and configuration
- **Model availability**: Model access depends on OpenAI account and API entitlements
- **Language requirement**: All prompts sent to Codex must be in English for optimal results
- **This skill is for delegation**, not autonomous code modification without user confirmation
