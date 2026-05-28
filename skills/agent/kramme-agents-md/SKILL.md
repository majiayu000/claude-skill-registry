---
name: kramme:agents-md
description: This skill should be used when the user asks to "update AGENTS.md", "add to AGENTS.md", "maintain agent docs", or needs to add guidelines to agent instructions. Guides discovery of local skills and enforces structured, keyword-based documentation style.
---

# Adding to AGENTS.md

AGENTS.md is the canonical agent-facing documentation. Each rule should be minimal, but many rules are OK.

## Before Writing

Discover local skills to reference:

```bash
find .claude/skills -name "SKILL.md" 2>/dev/null
ls plugins/*/skills/*/SKILL.md 2>/dev/null
```

Read each skill's frontmatter to understand when to reference it.

## Guideline Keywords

Use these keywords to indicate requirement strength:

- **ALWAYS** — Mandatory requirement
- **NEVER** — Strong prohibition
- **PREFER** — Strong recommendation, exceptions allowed
- **CAN** — Optional, developer's discretion
- **NOTE** — Context or clarification
- **EXAMPLE** — Illustrative example

Strictness hierarchy: ALWAYS/NEVER > PREFER > CAN > NOTE/EXAMPLE

## Writing Rules

- **Existing sections first** - Only propose new sections if no appropriate existing section exists
- **One rule per bullet** - Keep each guideline minimal and atomic
- **Start with keyword** - Every rule begins with ALWAYS/NEVER/PREFER/CAN/NOTE
- **Headers + bullets** - No paragraphs
- **Code blocks** - For commands and templates
- **Reference, don't duplicate** - Point to skills: "See `.claude/skills/db-migrate/SKILL.md`"
- **No filler** - No intros, conclusions, or pleasantries

## Common Sections

Add sections as needed for the project:

### When Stuck
```markdown
## When Stuck
- **ALWAYS** ask a clarifying question or propose alternatives
- **NEVER** initiate large speculative changes without confirmation
```

### Git Commits
```markdown
## Git Commits
- **ALWAYS** write succinct commit messages in imperative mood
- **ALWAYS** keep the first line short
- **NEVER** mention that you are an AI
```

### Issue Management
```markdown
## Linear Issues
- **NEVER** change issue status without explicit instruction
- **NEVER** create issues without explicit instruction
```

### Package Manager
```markdown
## Package Manager
Use **pnpm**: `pnpm install`, `pnpm dev`, `pnpm test`
```

### Local Skills
Reference each discovered skill:
```markdown
## Database
Use `db-migrate` skill. See `.claude/skills/db-migrate/SKILL.md`
```

### Domain-Specific Sections
Add sections for each tech stack (Frontend, Backend, etc.) with domain-specific guidelines.

## Anti-Patterns

Omit these:
- "Welcome to..." or "This document explains..."
- Obvious instructions ("run tests", "write clean code")
- Explanations of why (just say what)
- Long prose paragraphs
- Content duplicated from skills (reference instead)
