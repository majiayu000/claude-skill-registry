---
name: claude-md-template
description: Generate CLAUDE.md template for current project
user-invocable: true
---

# CLAUDE.md Template Generator

Generate a customized CLAUDE.md template based on detected project type.

---

## Detection

1. **Language**: package.json, requirements.txt, Cargo.toml, go.mod
2. **Framework**: Parse dependencies
3. **Package Manager**: npm, pnpm, yarn, pip, cargo
4. **Test Framework**: jest, pytest, cargo test
5. **Existing Patterns**: .eslintrc, .prettierrc, tsconfig.json

---

## Template Structure

```markdown
# [Project Name] - Project Instructions

## Overview
[Auto-detected description]

## Tech Stack
| Category | Technology |
|----------|------------|
| Language | [detected] |
| Framework | [detected] |

## Development Commands
- Install: [detected]
- Dev: [detected]
- Test: [detected]
- Build: [detected]

## Project Structure
[Auto-generated tree]

## Coding Conventions
[Inferred from configs]

## Key Files
| File | Purpose |
|------|---------|
| [entry] | Main entry |

## Director Mode Commands
- /workflow - Start development
- /auto-loop - Autonomous TDD
```

---

## After Generation

1. Show generated CLAUDE.md
2. Highlight [TODO] sections
3. Offer to run `/claude-md-check`
