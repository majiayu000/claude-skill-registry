---
name: aico-pm-init
description: |
  Initialize PM environment by creating constitution document from template.

  Use this skill when:
  - Running /pm.init command
  - User asks to "initialize PM", "setup product management", "create constitution"
  - Starting a new project and need to establish product constraints and domain info
  - Need to create docs/reference/pm/constitution.md for a new project
---

# PM Init

Initialize the product constitution document that provides shared constraints and domain information for all PM activities.

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Check existing**: Look for `docs/reference/pm/constitution.md`
2. **If exists**: Ask user if they want to overwrite or update specific sections
3. **If not exists**:
   - Read template from `references/constitution.template.md`
   - Guide user through questions to fill template
4. **Save output**: Write to `docs/reference/pm/constitution.md`

## Document Header Format

All generated documents MUST use this unified header format:

```markdown
# [Document Title]

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
```

## Guided Questions

Ask user about:

| Section          | Questions                                                  |
| ---------------- | ---------------------------------------------------------- |
| Product Overview | Product name? One-line description? Target users?          |
| Domain Info      | Industry/market? Key terminology? Compliance requirements? |
| Constraints      | Technical stack? Business constraints?                     |
| Standards        | Documentation language? Naming conventions?                |

## Template

See `references/constitution.template.md` for the full constitution template.

## Update Instructions File

After creating constraint files, update the project's AI instructions file to reference them:

1. **Check for existing instructions file**:
   - Look for `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex) in project root
   - If neither exists, create `CLAUDE.md`

2. **Add reference section** at the end of the file:

   ```markdown
   ## Reference Documents

   The following constraint documents should be read before starting work:

   - `docs/reference/pm/constitution.md` - Product constitution with domain info and constraints
   ```

3. **If file already has Reference Documents section**: Append the new reference if not already present

## Output

```
✓ Created docs/reference/pm/constitution.md
✓ Updated CLAUDE.md with reference to constitution
✓ PM environment initialized
```

## Key Rules

- ALWAYS use the unified header format
- MUST guide user through key questions before generating
- ALWAYS save to `docs/reference/pm/constitution.md`
- MUST update CLAUDE.md or AGENTS.md with reference to constraint files
