---
name: init
description: Analyze project structure and update AGENTS.md with detected tech stack, commands, and configurations.
disable-model-invocation: true
---

# Initialize Project Configuration

Analyze this project and update **only the project-specific sections** of AGENTS.md.

## Important

- Do **NOT** modify the "Extensions" section and below in existing AGENTS.md
- Only update the top project-specific sections

## Steps

### 1. Project Analysis

Find these files to identify the tech stack:

- `package.json` → Node.js/TypeScript project
- `pyproject.toml` / `setup.py` / `requirements.txt` → Python project
- `Cargo.toml` → Rust project
- `go.mod` → Go project
- `Makefile` / `Dockerfile` → Build/deploy config
- `.github/workflows/` → CI/CD config

Also detect:

- npm scripts / poe tasks / make targets → Common commands
- Major libraries/frameworks

### 2. Ask User

Use AskUserQuestion tool to ask:

1. **Project overview**: What does this project do? (1-2 sentences)
2. **Code language**: English or Japanese for comments/variable names?
3. **Additional rules**: Any other coding conventions to follow?

### 3. Partial Update of AGENTS.md

Use Edit tool to update only the top section (up to first `---`) with this format:

```markdown
# Project Overview

{User's answer}

## Language Settings

- **Thinking/Reasoning**: English
- **Code**: {Based on analysis - English or Japanese}
- **User Communication**: Japanese

## Tech Stack

- **Language**: {Detected language}
- **Package Manager**: {Detected tools}
- **Dev Tools**: {Detected tools}
- **Main Libraries**: {Detected libraries}
```

### 4. Update Common Commands

Update the `## Common Commands` section with detected commands:

```markdown
## Common Commands

```bash
# Detected commands (example)
{npm run dev / poe test / make build etc.}
```
```

### 5. Check Unnecessary Rules

Check rules in `.claude/rules/` and suggest removing unnecessary ones:

- Non-Python project → `dev-environment.md` (uv/ruff/ty) may not be needed
- No-test project → `testing.md` may not be needed

### 6. Report Completion

Report to user (in Japanese):

- Detected tech stack
- Updated sections
- Recommended rules to remove (if any)
