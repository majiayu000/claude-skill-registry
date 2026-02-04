---
name: dev-standards-majo
description: |
  Apply Mark's core development standards to ensure consistent, maintainable code across all
  projects. Use when starting work on any codebase, generating new code, refactoring, or when
  unsure about documentation requirements, error handling, British English spellings, or
  AGENTS.md maintenance. Covers universal principles that apply before language-specific skills.
license: Unlicense
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# Mark's Development Standards

Core development standards that apply across all languages and projects.

## Goal

Ensure all generated code is maintainable, readable, and consistent with established
patterns. Enforce British English, proper error handling, and AGENTS.md maintenance
across every project and language.

## When to Use This Skill

**Use this skill when:**
- Starting work on any codebase
- Generating new code in any language
- Refactoring existing code
- Unsure about documentation requirements
- Need to maintain AGENTS.md
- Writing error messages or handling failures
- Unsure about spelling (British vs American English)

**Do NOT use this skill when:**
- You need language-specific guidance (use `python-majo`, `js-bun-majo`, etc.)
- You're only reading code without making changes
- The task is purely exploratory with no code generation

## Process

### Step 1: Check for AGENTS.md

Always check for AGENTS.md first:

```bash
# Check if AGENTS.md exists
ls AGENTS.md AGENTS.PLAN.md 2>/dev/null || echo "No AGENTS.md found"

# Read it if it exists
cat AGENTS.md
```

### Step 2: Apply Universal Principles

For every code generation task:

1. **Maintainability First** - Code should be readable and modular
2. **Self-Documenting** - Clear variable names, no excessive comments
3. **Diagnostic Cleanliness** - No errors or warnings (suppress only when reasonable)
4. **British English** - colour, behaviour, licence (noun), initialise, etc.

### Step 3: Follow Error Handling Standards

Use consistent error format:
```
program: level: message
```

**Print to stderr and use specific exit codes** (grouped by category):
- `0` - Success
- `1-29` - Usage errors
- `30-49` - Input errors  
- `50-69` - File/IO errors
- `70-89` - Processing errors
- `255` - Runtime error

### Step 4: Update AGENTS.md

After any significant work:
- Update knowledge of codebase
- Note code style and structure
- Record practices and methodologies
- Update current task status

## Constraints

- **Always use British English** - colour, behaviour, licence (noun), initialise, organised, centre (physical location)
- **Never exceed 800 tokens in AGENTS.md root** - Use progressive disclosure for larger docs
- **Always include SPDX identifiers** in new source files
- **Never commit without checking AGENTS.md first**
- **Always quote variables** in shell scripts to prevent word splitting
- **Never use vague guidance** - Be specific: "Never commit secrets" not "Be careful with secrets"

## British English (Strict Requirement)

**Always use British English spellings throughout all code and documentation.**

Common documentation words:
- **colour** (not color)
- **licence** (noun) / **license** (verb)
- **behaviour** (not behavior)
- **favourite** (not favorite)
- **organised** (not organized)
- **initialise** (not initialize)
- **center** (technical/abstract, e.g. image center) / **centre** (a physical location, e.g. town centre)
- **recognised** (not recognized)
- **genericised** (not genericized)

**Exception**: Standard file names like `LICENSE` and `LICENSE-0BSD` use American spelling for compatibility with tooling and conventions.

## Universal Code Principles

### Code Quality

**Maintainability First**
- Generated code should be maintainable through readability and/or modularity
- No undue pre-optimization beyond existing complexity in the codebase
- Follow conventions of previous or attached files

**Self-Documenting Code**
- Code should not require extensive comments
- Variable names and expressions should visibly describe the logic
- Naming should be apt yet visible in describing implemented logic

**Diagnostic Cleanliness**
- Generated code should not have diagnostic errors or warnings
- Suppress diagnostics only when reasonable (e.g., external package missing type stubs)

### Code Organization

**Section Comments**
Use clear section comments to group related code:
```python
# constants
VERSION: Final[str] = "1.0.0"
DEBUG: Final[bool] = False

# configuration
config = load_config()

# main logic
result = process(config)
```

**Defensive Programming**
- Check preconditions before operations
- Validate inputs early
- Provide descriptive error messages
- Use specific exit codes for different error types

**Logical Grouping**
- Group related constants together
- Keep functions/methods focused on single responsibility
- Separate I/O from business logic where possible

## Error Handling

### Message Format

Use a consistent format across all languages:

```
program: level: message
```

**Levels** (in order of severity):
- `error:` — Fatal errors requiring exit
- `internal error:` — Bugs or unexpected failures
- `warning:` or `warn:` — Non-fatal issues
- `info:` — Status updates
- `debug:` — Verbose debugging (only when debug mode enabled)

**Examples**:
```python
print(f"surplus: error: {exc}", file=stderr)
print(f"zigbpy: internal error: {exc.__class__.__name__}", file=stderr)
print(f"warn: '{target}' does not exist, skipping", file=stderr)
```

### Follow-up Notes

Provide additional context using `... note:` prefix:

```python
print(f"zigbpy: error: unmatched brackets at depth {depth}", file=stderr)
print(f"... note: depth {depth} - program index {start} -> {end} [unmatched]", file=stderr)
```

### Exit Codes

Group exit codes by category:

- `0`: Success
- `-1` (or `255`, depending on platform): Runtime error, unexpected crash
- Usage errors
- Input errors
- File/IO errors
- Memory errors
- Processing errors

and so on, using ranges for each category,
e.g. `1-29` for usage errors, `30-49` for input errors, and so on,
depending on how many errors and categories you have and/or expect to encounter.

**Example** (document at top of CLI scripts):

```python
# exit codes:
# 0  - success
# 1  - bad command usage or missing env vars
# 2  - bad target
# 3  - could not send message
# 10 - invalid input format
# 20 - file not found
# 255 - runtime error
```

### File Operations

**Respect File Moves**
- If a file has been renamed/moved without duplicate, consider the newest structure correct
- Do not revert seemingly deliberate file moves if you did not cause them

## Documentation Policy

**NO Documentation Unless Asked**
- Do not write README files, API docs, or user-facing documentation unless explicitly requested
- Do not write code comments explaining obvious logic

**License Headers**
All source files must include the full license text at the top. See language-specific skills for exact formatting:
- `python-majo` - Python file headers
- `shell-majo` - Shell script headers
- `rust-majo` - Rust file headers (if created)
- `zig-majo` - Zig file headers (if created)

**AGENTS.md Maintenance (CRITICAL)**

Maintain an `AGENTS.md` file with:
- Knowledge of the codebase
- Understood code style and structure
- Practices and methodologies recognized
- Linguistic style of comments
- Current task at hand and/or to-do list

**Location**: Place wherever documentation is stored in the project.

**Purpose**: Enable resumption from a context-less state without requiring codebase inquiry every time a new agent-or-LLM conversation thread starts.

**Updates**: Update old knowledge in the file as you work.

## Environment Awareness

### Read-Write Environment

**Gemini CLI, Claude Code, ChatGPT Codex CLI**: Your environment is NOT read-only. You can read and write files in this workspace.

### Search Constraints

**Grok-code-fast-1**: Do NOT use regex-based or purely wildcard workspace/file content searches. Use globs or regexes that have a non-wildcard component.

## SPDX License Identifiers

When creating new source files in public domain projects, add the appropriate SPDX identifier at the top:

**For most files** (dual-licensed):
```python
# SPDX-License-Identifier: Unlicense OR 0BSD
```

**For files by contributors who cannot waive copyright**:
```python
# SPDX-License-Identifier: 0BSD
```

## Testing Skills

Before relying on this skill, test implicit invocation:

**Should trigger:**
- "Help me write a Python script"
- "Refactor this code"
- "Create a new function"

**Should NOT trigger:**
- "Read this file for me" (no code generation)
- "Explain what this code does" (exploratory only)

## Integration

This skill works alongside language-specific skills:
- `python-majo` - Python-specific standards (UV, basedpyright, MDF)
- `js-bun-majo` - JavaScript/TypeScript/Bun standards
- `shell-majo` - POSIX shell scripting standards
- `git-majo` - Git workflow and commit standards
- `writing-docs-majo` - Documentation writing standards
- `task-planning-majo` - Planning workflows
- `setting-up-public-domain-repos-majo` - Public domain repository setup
- `running-windows-commands-majo` - Windows-specific command alternatives
- `skill-authoring-majo` - Creating new Agent Skills
- `agents-md-authoring-majo` - Writing effective AGENTS.md files
- `csharp-unity-majo` - C#/Unity development standards
- `mdf-majo` - meadow Docstring Format (MDF) for Python
- `mdf-md-api-docs-majo` — Writing API refs or docs from code using the MDF

**Always load this skill first**, then the appropriate language-specific skill.
