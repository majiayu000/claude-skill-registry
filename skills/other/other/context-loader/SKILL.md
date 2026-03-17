---
name: context-loader
description: Load project context from .claude/ directory at the start of every task. This ensures Gemini CLI has the same coding rules, design decisions, and library constraints as Claude Code.
---

# Context Loader Skill for Gemini

## Purpose

Load shared project context from `.claude/` directory to ensure Gemini CLI operates with the same knowledge as Claude Code and Codex CLI.

## When to Activate

**ALWAYS** - This skill should run at the beginning of research or analysis tasks.

## Workflow

### Step 1: Load Coding Rules

Read relevant files from `.claude/rules/`:

```
.claude/rules/
├── coding-principles.md   # Simplicity, single responsibility, early return
├── dev-environment.md     # uv, ruff, ty, pytest requirements
├── language.md            # Think in English, respond in Japanese
├── security.md            # Secrets, validation, SQLi/XSS prevention
└── testing.md             # TDD, AAA pattern, 80% coverage
```

### Step 2: Load Design Documentation

Read `.claude/docs/DESIGN.md` for:
- Architecture decisions
- Implementation patterns
- Library choices and constraints

### Step 3: Check Library Documentation

If the task involves specific libraries, read relevant files from:
```
.claude/docs/libraries/
```

### Step 4: Execute Research Task

With the loaded context, execute the requested research/analysis following:
- Project coding principles
- Existing design decisions
- Library constraints

## Key Rules to Remember

1. **Simplicity first** - Recommend readable solutions over complex
2. **Type hints required** - Suggest typed code
3. **Use uv** - Reference uv for package management
4. **Security** - Highlight security considerations

## Language Protocol

- **Thinking/Reasoning**: English
- **Code examples**: English (variables, functions, comments)
- **Output**: Structured markdown, suitable for documentation

## Output Guidelines

When providing research results:
- Structure with clear headings
- Include code examples when relevant
- Cite sources from web search
- Note constraints relevant to this project
- Save comprehensive findings to `.claude/docs/research/`
