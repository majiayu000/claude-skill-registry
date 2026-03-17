---
name: aico-frontend-init
description: |
  Initialize frontend environment by creating design system and constraints documents from templates.

  Use this skill when:
  - Running /frontend.init command
  - User asks to "initialize frontend", "setup frontend environment"
  - Starting frontend work and need to establish design system and constraints
  - Need to create docs/reference/frontend/design-system.md or constraints.md
---

# Frontend Init

Initialize frontend engineer configuration files: design system and constraints.

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Check existing**: Look for `docs/reference/frontend/design-system.md` and `constraints.md`
2. **Create directory structure**:
   ```
   docs/reference/frontend/
   ├── design-system.md
   ├── constraints.md
   ├── designs/
   └── tasks/
   ```
3. **Design System Setup**:
   - Option A: Extract from reference website using `aico-frontend-style-extraction` skill
   - Option B: Use template from `references/design-system.template.md`
4. **Constraints Setup**:
   - Guide user through tech stack questions
   - Use template from `references/constraints.template.md`
5. **Save output**: Write to `docs/reference/frontend/`

## Document Header Format

All generated documents MUST use this unified header format:

```markdown
# [Document Title]

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
```

## Design System Options

### Option A: Extract from Reference Website

If user provides a reference URL:

1. Check if Playwright MCP is available
2. Navigate to URL → take screenshot → analyze
3. Extract design tokens using `aico-frontend-style-extraction` skill

### Option B: Fill Template

If no reference:

1. Read template from `references/design-system.template.md`
2. Ask about color preferences (light/dark, accent color)
3. Ask about typography (serif/sans-serif)
4. Fill in reasonable defaults

## Constraints Questions

| Question          | Options                                      |
| ----------------- | -------------------------------------------- |
| Framework         | React, Vue, Next.js, Svelte                  |
| TypeScript        | Yes (recommended), No                        |
| Component Library | shadcn/ui, Ant Design, MUI, None             |
| Styling           | Tailwind CSS, CSS Modules, styled-components |
| Testing           | Vitest, Jest, None                           |
| Directory Pattern | Feature-based, Type-based                    |

## Templates

- `references/design-system.template.md` - Design tokens template
- `references/constraints.template.md` - Tech stack and conventions template

## Update Instructions File

After creating constraint files, update the project's AI instructions file to reference them:

1. **Check for existing instructions file**:
   - Look for `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex) in project root
   - If neither exists, create `CLAUDE.md`

2. **Add reference section** at the end of the file:

   ```markdown
   ## Reference Documents

   The following constraint documents should be read before starting work:

   - `docs/reference/frontend/design-system.md` - Design tokens and visual guidelines
   - `docs/reference/frontend/constraints.md` - Tech stack and coding conventions
   ```

3. **If file already has Reference Documents section**: Append the new references if not already present

## Output

```
✓ Created docs/reference/frontend/design-system.md
✓ Created docs/reference/frontend/constraints.md
✓ Created docs/reference/frontend/designs/
✓ Created docs/reference/frontend/tasks/
✓ Updated CLAUDE.md with reference to constraint files
✓ Frontend environment initialized
```

## Key Rules

- ALWAYS use the unified header format
- MUST create both design-system.md and constraints.md
- ALWAYS create designs/ and tasks/ directories
- MUST update CLAUDE.md or AGENTS.md with reference to constraint files
