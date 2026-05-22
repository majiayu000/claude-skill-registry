---
name: agents-md
description: Create and optimize AGENTS.md files for AI coding agents. Use when setting up agent instructions for a new project, improving existing AGENTS.md, or diagnosing why agents aren't following project conventions.
---

# AGENTS.md Authoring Skill

## What This Skill Does

This skill guides the creation of effective AGENTS.md files - configuration files that provide persistent instructions to AI coding agents. A well-crafted AGENTS.md encodes project-specific knowledge that agents need to work effectively in your codebase.

### What AGENTS.md Solves

1. **Memory persistence** - LLMs don't retain context between sessions; AGENTS.md is loaded at session start
2. **Team standardization** - Shared via version control, ensures consistent AI behavior across team
3. **Reduced exploration overhead** - Agents immediately know build commands, conventions, gotchas
4. **Mistake prevention** - Explicit rules prevent common errors before they happen

---

## Quick Start

For a simple project:

```markdown
# Project Name

## Quick Reference
| Task | Command |
|------|---------|
| Build | `npm run build` |
| Test | `npm test` |
| Lint | `npm run lint` |

## Code Style
- TypeScript strict mode
- 2-space indentation
- Single quotes, no semicolons

## Gotchas
- Use `httpx` not `requests` for HTTP calls
- Database migrations are in `db/migrations/`, not project root
```

For complex projects, follow the phases below.

---

## Phase 1: Assessment

Before writing, understand what the project needs.

### Questions to Answer

1. **Tech stack**: What languages, frameworks, build tools?
2. **Common commands**: What does the team run daily?
3. **Conventions**: What style rules aren't enforced by linters?
4. **Gotchas**: What trips up newcomers (human or AI)?
5. **Architecture**: What's the directory structure and data flow?

### Scope Determination

| Project Type | Recommended Structure |
|--------------|----------------------|
| Single-language, simple | One root AGENTS.md (~50-80 lines) |
| Monorepo or multi-component | Root + component-level AGENTS.md files |
| Large team with varied workflows | Root + `.agents/rules/*.md` modular rules |

### Check Existing Documentation

```bash
# Find existing docs that might inform AGENTS.md
ls -la README.md CONTRIBUTING.md STYLE*.md .cursor* .claude* 2>/dev/null
```

---

## Phase 2: Structure Selection

### File Hierarchy

```
~/.config/opencode/AGENTS.md    # User-level (all your projects)
./AGENTS.md                      # Project-level (team-shared via git)
./AGENTS.local.md                # Personal overrides (gitignored)
./component/AGENTS.md            # Component-specific rules
```

**Lookup behavior**: Agents read the nearest AGENTS.md in the directory tree, plus any nested in subdirectories when working there.

### Recommended Sections

| Section | Include When | Content |
|---------|--------------|---------|
| Quick Reference | Always | Table of common commands |
| Architecture | Multi-component projects | Directory structure, data flow |
| Code Style | Conventions beyond linter | Naming, patterns, preferences |
| Database | Has database | Migration commands, patterns |
| Testing | Non-trivial test setup | How to run, what to verify |
| Gotchas | Project has quirks | Things that cause mistakes |
| See Also | Has related docs | Links to other AGENTS.md or docs |

### Length Guidelines

| Guideline | Rationale |
|-----------|-----------|
| Root: 50-100 lines | Sweet spot for coverage without dilution |
| Component: 30-50 lines | Focused on component-specific rules |
| Total: Under 500 lines | Empirically validated maximum effectiveness |
| Under 2 pages per file | GitHub Copilot recommendation |

---

## Phase 3: Writing Effective Instructions

### Instruction Types That Work

**1. Imperative Commands**
```markdown
# GOOD - Imperative
Run `npm test` before committing.

# WEAK - Passive
Tests should be run before committing.
```

**2. Exact Commands (Copy-Paste Ready)**
```markdown
# GOOD - Exact
Run migrations: `cd server/database && uv run --directory .. alembic upgrade head`

# WEAK - Vague
Run the database migrations using alembic.
```

**3. Always/Never Rules (Strong Constraints)**
```markdown
# GOOD - Clear constraint
- Always use `httpx` for HTTP calls, never `requests`
- Never commit directly to `main` branch

# WEAK - Wishy-washy
- Prefer httpx over requests when possible
```

**4. Concrete Examples**
```markdown
# GOOD - Shows exact format
Error format: `{ "error": true, "code": "E001", "message": "Description" }`

# WEAK - Abstract
Use our standard error format.
```

**5. Tables for Quick Reference**
```markdown
| Task | Command |
|------|---------|
| Server dev | `cd server && uv run uvicorn app:main --reload` |
| Server test | `cd server && uv run pytest` |
| Mobile dev | `cd mobile && flutter run` |
```

### Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Vague instructions | "Write clean code" | Specific rules: "Use 2-space indent" |
| Contradictions | "Be thorough" + "Keep changes minimal" | Remove conflict |
| Restating defaults | "Handle errors appropriately" | Agent already does this |
| Too verbose | Paragraph per rule | Bullet points, tables |
| Duplicating linters | "Follow ESLint rules" | Linter already enforces |

### Writing Checklist

- [ ] Commands are copy-paste ready
- [ ] Used imperative mood ("Run X" not "X should be run")
- [ ] Constraints use "Always" or "Never"
- [ ] Examples show exact format expected
- [ ] No vague guidance ("write good code")
- [ ] No contradictory rules
- [ ] Under 100 lines for root file

---

## Phase 4: Gotchas Section

The Gotchas section is often the most valuable. It prevents AI mistakes proactively.

### What to Include

1. **Naming collisions**: "API keys use `myapp_sk_` prefix - don't confuse with OpenAI keys"
2. **Framework choices**: "Uses Riverpod (not Provider) for state management"
3. **Library preferences**: "Use `httpx` for HTTP calls, not `requests`"
4. **Directory quirks**: "The `database/` directory is inside `server/`, not at project root"
5. **Tool versions**: "Requires Node 18+ (uses native fetch)"
6. **Generated files**: "Files in `dist/` are generated - never edit directly"

### Pattern: Iterative Gotcha Collection

When an AI makes a mistake that could have been prevented:
1. Note the mistake
2. Add a gotcha rule to prevent it
3. Periodically review and prune rules that aren't triggered

---

## Phase 5: Multi-Component Projects

For monorepos or multi-component projects:

### Root AGENTS.md

```markdown
# Project Name

Brief description.

## Quick Reference
[Commands for all components]

## Architecture
[High-level structure and data flow]

## See Also
- Server: See server/AGENTS.md
- Mobile: See mobile/AGENTS.md
- Git workflow: See global AGENTS.md
```

### Component AGENTS.md

```markdown
# Component Name

## Commands
[Component-specific commands]

## Code Style
[Component-specific conventions]

## Gotchas
[Component-specific pitfalls]
```

### When to Split

Split into component-level files when:
- Components use different languages/frameworks
- Components have different build systems
- Different team members own different components
- Component-specific rules would clutter root file

---

## Phase 6: Maintenance

### Gitignore Setup

```bash
# Add to .gitignore
echo "AGENTS.local.md" >> .gitignore
echo "**/AGENTS.local.md" >> .gitignore
```

### Review Cadence

| Trigger | Action |
|---------|--------|
| AI makes preventable mistake | Add gotcha rule |
| Rule never triggers | Consider removing |
| Team onboards new member | Review for clarity |
| Major refactor | Update architecture, commands |
| Quarterly | Prune outdated rules |

### Version Control

- Commit AGENTS.md changes with the code they relate to
- Use descriptive commit messages: `docs: add database migration gotcha to AGENTS.md`

---

## Templates

### Minimal Template (~30 lines)

```markdown
# Project Name

## Quick Reference
| Task | Command |
|------|---------|
| Build | `<command>` |
| Test | `<command>` |
| Lint | `<command>` |

## Code Style
- <key rule 1>
- <key rule 2>

## Gotchas
- <common mistake to avoid>
```

### Standard Template (~80 lines)

```markdown
# Project Name

Brief description of the project.

## Quick Reference

| Task | Command |
|------|---------|
| Install | `<command>` |
| Dev server | `<command>` |
| Test | `<command>` |
| Lint | `<command>` |
| Build | `<command>` |

## Architecture

```
dir1/     Description
dir2/     Description
  sub/    Description
```

- Key architectural point 1
- Key architectural point 2

## Code Style

- <convention 1>
- <convention 2>
- <convention 3>

## Database

- Migration command: `<command>`
- Rollback: `<command>`
- Never modify migrations after they've been applied

## Testing

- Run `<command>` before committing
- Add tests for new functionality
- Mock external services in tests

## Gotchas

- <gotcha 1>
- <gotcha 2>
- <gotcha 3>

## See Also

- Related doc 1: See path/to/doc
- Related doc 2: See path/to/doc
```

### Monorepo Template

```markdown
# Project Name

Multi-component project description.

## Quick Reference

| Component | Dev | Test |
|-----------|-----|------|
| Server | `cd server && <cmd>` | `cd server && <cmd>` |
| Web | `cd web && <cmd>` | `cd web && <cmd>` |
| Mobile | `cd mobile && <cmd>` | `cd mobile && <cmd>` |

## Architecture

```
server/     Backend API
web/        Web frontend
mobile/     Mobile app
shared/     Shared types/utilities
```

## Cross-Component Rules

- Shared types live in `shared/` - import from there
- API contract defined in `shared/api-types.ts`
- All components use the same linting rules

## See Also

- Server: See server/AGENTS.md
- Web: See web/AGENTS.md
- Mobile: See mobile/AGENTS.md
```

---

## Worked Example: Python/Flutter Project

### Assessment

- **Tech stack**: Python FastAPI backend, Flutter mobile app
- **Commands**: uv for Python, flutter CLI for mobile
- **Conventions**: Ruff for Python, dart analyze for Flutter
- **Gotchas**: Database migrations path is non-obvious, uses Riverpod not Provider

### Result

**Root AGENTS.md (60 lines)**:

```markdown
# Oracy

AI-powered voice transcription: Flutter mobile app + Python FastAPI server.

## Quick Reference

| Task | Command |
|------|---------|
| Server dev | `cd server && uv run uvicorn oracy.main:app --reload` |
| Server test | `cd server && uv run pytest` |
| Server lint | `cd server && uv run ruff check . && uv run ruff format .` |
| Mobile dev | `cd mobile && flutter run` |
| Mobile lint | `cd mobile && dart analyze && dart format .` |
| DB migrate | `cd server/database && uv run --directory .. alembic upgrade head` |

## Architecture

```
mobile/     Flutter app (iOS/Android) - Riverpod state, Drift local DB
server/     FastAPI + SQLAlchemy - OpenAI Whisper integration
  oracy/
    api/      REST endpoints
    core/     Config, security
    db/       SQLAlchemy models
    services/ Business logic
  database/   Alembic migrations
```

## Gotchas

- API keys use `oracy_sk_` prefix - don't confuse with OpenAI keys
- Mobile uses Riverpod (not Provider) for state management
- Server uses `httpx` for HTTP calls (not `requests`)
- The `database/` directory is inside `server/`, not at project root

## See Also

- Server details: See server/AGENTS.md
- Mobile details: See mobile/AGENTS.md
```

---

## Troubleshooting

### Agent Ignores AGENTS.md Rules

**Causes:**
1. File not in expected location
2. Rule too vague
3. Contradicted by other instructions
4. Rule buried in too much text

**Fixes:**
1. Verify file is at project root or component root
2. Make rule more specific with exact commands/examples
3. Remove contradictions
4. Move critical rules to top, use bold/headers

### AGENTS.md Too Long

**Symptoms:** Over 150 lines, rules getting ignored

**Fixes:**
1. Split into component-level files
2. Move reference material to separate docs (link with "See X")
3. Remove rules that duplicate linter behavior
4. Prune rules that haven't prevented mistakes

### Team Disagreement on Rules

**Resolution:**
1. AGENTS.md is for machine consumption, not style debates
2. If linter can enforce it, let linter handle it
3. Only include rules that prevent actual AI mistakes
4. Use AGENTS.local.md for personal preferences

---

## Cross-Tool Compatibility

| Tool | Primary File | Also Reads |
|------|--------------|------------|
| Claude Code | CLAUDE.md | - |
| OpenCode | AGENTS.md | CLAUDE.md, CONTEXT.md |
| Cursor | .cursor/rules/*.md | AGENTS.md |
| GitHub Copilot | .github/copilot-instructions.md | - |

For maximum compatibility, use AGENTS.md (OpenCode reads it, Cursor falls back to it).

---

## Power User Techniques

### Personal Overrides (AGENTS.local.md)

For settings you don't want to share with the team:

```markdown
# Personal overrides (gitignored)

## My Preferences
- I prefer verbose test output: `pytest -v --tb=long`
- My local API runs on port 3001

## Local Paths
- Test data: ~/test-fixtures/oracy/
```

### Path-Specific Rules (Advanced)

Some tools support YAML frontmatter for path scoping:

```yaml
---
paths:
  - "src/api/**/*.ts"
---

# API Development Rules
- All endpoints must validate input with Zod
- Return standard error format: { error, code, message }
```

### Import Syntax (Tool-Specific)

Some tools support imports to reduce duplication:

```markdown
# AGENTS.md
See @docs/api-conventions.md for API rules
See @docs/testing-guide.md for testing patterns
```

### Credential Hygiene Pattern

```markdown
## Credential Rules
- Never read credential values into conversation context
- Verify credentials exist without exposing: `pass show X > /dev/null && echo "exists"`
- If accidentally exposed, immediately advise rotation
```

---

## Validation Checklist

Before finalizing AGENTS.md:

- [ ] Commands are tested and work
- [ ] No vague instructions ("write good code")
- [ ] No contradictory rules
- [ ] Gotchas section covers known pitfalls
- [ ] Under 100 lines for root file
- [ ] AGENTS.local.md added to .gitignore
- [ ] Component files linked from root "See Also"
- [ ] At least one team member reviewed
