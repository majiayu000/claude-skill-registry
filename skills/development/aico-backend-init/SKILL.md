---
name: aico-backend-init
description: |
  Initialize backend environment by creating constraints document from template.

  Use this skill when:
  - Running /backend.init command
  - User asks to "initialize backend", "setup backend environment"
  - Starting backend work and need to establish tech stack and conventions
  - Need to create docs/reference/backend/constraints.md
---

# Backend Init

Initialize backend development environment by creating the constraints file.

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

1. **Check existing**: Look for `docs/reference/backend/constraints.md`
2. **If exists**: Ask user if they want to overwrite or skip
3. **Create directory structure**:
   ```
   docs/reference/backend/
   ├── constraints.md
   └── tasks/
   ```
4. **Generate constraints file**:
   - Read template from `references/constraints.template.md`
   - Guide user through key decisions
5. **Save output**: Write to `docs/reference/backend/constraints.md`

## Document Header Format

All generated documents MUST use this unified header format:

```markdown
# [Document Title]

> Project: [project-name]
> Created: YYYY-MM-DD
> Last Updated: YYYY-MM-DD
```

## Guided Questions

| Category         | Questions                          |
| ---------------- | ---------------------------------- |
| Language/Runtime | Node.js, Python, Go, Rust?         |
| Framework        | Express, Fastify, FastAPI, Gin?    |
| Database         | PostgreSQL, MySQL, MongoDB?        |
| ORM/Query        | Prisma, Drizzle, SQLAlchemy, GORM? |
| Testing          | Vitest, Jest, Pytest, Go test?     |
| API Style        | REST, GraphQL, gRPC?               |

## Template

See `references/constraints.template.md` for the full constraints template.

## Update Instructions File

After creating constraint files, update the project's AI instructions file to reference them:

1. **Check for existing instructions file**:
   - Look for `CLAUDE.md` (Claude Code) or `AGENTS.md` (Codex) in project root
   - If neither exists, create `CLAUDE.md`

2. **Add reference section** at the end of the file:

   ```markdown
   ## Reference Documents

   The following constraint documents should be read before starting work:

   - `docs/reference/backend/constraints.md` - Tech stack and coding conventions
   ```

3. **If file already has Reference Documents section**: Append the new reference if not already present

## Output

```
✓ Created docs/reference/backend/constraints.md
✓ Created docs/reference/backend/tasks/
✓ Updated CLAUDE.md with reference to constraint files
✓ Backend environment initialized
```

## Key Rules

- ALWAYS use the unified header format
- MUST guide user through tech stack questions
- ALWAYS create tasks/ directory
- ALWAYS save to `docs/reference/backend/constraints.md`
- MUST update CLAUDE.md or AGENTS.md with reference to constraint files
