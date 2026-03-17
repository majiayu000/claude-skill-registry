---
name: agents-md-pro
description: Create, optimize, update, and validate AGENTS.md files with maximum token efficiency. Use when the user asks to (1) create new AGENTS.md files for any repository, (2) optimize/condense existing AGENTS.md to reduce token count, (3) update/refresh AGENTS.md to sync with codebase changes, (4) validate AGENTS.md quality and completeness, or (5) improve AGENTS.md files to be more effective for AI agents. Always generates token-efficient, condensed output focused on actionable commands and patterns while maintaining model-agnostic language.
---

# AGENTS.md Pro

Create token-efficient AGENTS.md files that maximize clarity with minimal tokens.

## Core Principles

1. **Token efficiency** - Every word justifies its cost
2. **Commands over explanations** - Show, don't tell
3. **Reference configs** - Point to `.eslintrc`, never duplicate
4. **Model-agnostic** - Universal terminology only
5. **Condensed default** - Always minimal output

## Input

**Required:** Project directory path
**If missing:** Request from user

## Workflow Router

Map user request to workflow:
- Create → [workflows.md](references/workflows.md#create-workflow)
- Optimize/condense → [workflows.md](references/workflows.md#optimize-workflow)
- Update/refresh → [workflows.md](references/workflows.md#update-workflow)
- Validate → [workflows.md](references/workflows.md#validate-workflow)

## Quick Reference

**Output template** - Standard repo:
```markdown
# [Project] | [Tech Stack]
## COMMANDS
- Dev: `cmd` | Build: `cmd` | Test: `cmd` | Lint: `cmd --fix`
## STRUCTURE
- `dir/` - purpose
## PATTERNS
[1-2 key patterns with minimal code]
## CODE STYLE
See `.eslintrc`, `.prettierrc`
## DOMAIN
| Term | Definition |
## SECURITY
[Auth/validation only]
## GIT
Format: `convention`
```

**Line limits:**
- Standard: ≤150 lines
- Monorepo root: ≤50 lines
- Sub-project: ≤100 lines

**Target tokens:**
- Standard: 500-800
- Monorepo root: 300-400
- Sub-project: 400-600

## Resources

Load as needed:
- **Workflows**: [workflows.md](references/workflows.md) - All 4 workflows with step-by-step procedures
- **Optimization**: [optimization-patterns.md](references/optimization-patterns.md) - Token reduction techniques
- **Validation**: [validation-rules.md](references/validation-rules.md) - Quality checklist and scoring
- **Anti-patterns**: [anti-patterns.md](references/anti-patterns.md) - Common bloat patterns to avoid
