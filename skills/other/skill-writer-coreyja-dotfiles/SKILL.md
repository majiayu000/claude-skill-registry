---
name: skill-writer
description: Create and improve Claude Code skills. Use when drafting new skills, writing SKILL.md files, improving skill descriptions, or structuring skill directories. Triggers on requests to create skills, write skills, draft skills, improve skill triggering, or fix skills that aren't activating.
---

# Writing Claude Code Skills

Skills are directories that teach Claude how to perform specialized tasks. Claude discovers them automatically based on description matching—no manual invocation needed.

## File Structure

```
~/.claude/skills/skill-name/
├── SKILL.md          # Required - frontmatter + instructions
├── reference.md      # Optional - detailed docs loaded on-demand
├── examples.md       # Optional - usage examples
└── scripts/          # Optional - executable utilities
```

**Location determines scope:**
- `~/.claude/skills/` - Personal, works across all projects
- `.claude/skills/` - Project-specific, committed to repo

## SKILL.md Format

```yaml
---
name: lowercase-with-hyphens
description: What this does and when Claude should use it. Max 1024 chars.
allowed-tools: [Read, Grep, Glob]  # Optional - restrict available tools
model: haiku                        # Optional - specify model
---

# Skill Title

Instructions in markdown...
```

### Required Fields

| Field | Rules |
|-------|-------|
| `name` | Lowercase, hyphens only, max 64 chars |
| `description` | Max 1024 chars, this is how Claude decides to trigger |

### Optional Fields

| Field | Purpose |
|-------|---------|
| `allowed-tools` | Restrict what Claude can do (e.g., read-only skills) |
| `model` | Force a specific model for this skill |

## The Description is Everything

Claude triggers skills via semantic matching against descriptions. A vague description means the skill won't fire.

**Bad:** "Helps with documents"
**Good:** "Extract text and tables from PDFs, fill PDF forms, merge PDF files. Use when working with PDF documents, document extraction, or form filling."

A strong description answers:
1. **What specific actions does this skill enable?** (use concrete verbs: extract, create, validate, deploy)
2. **What words would naturally appear in a request?** (domain terms, file types, tool names)
3. **What are the boundaries?** (what this skill does NOT do, if ambiguous)

### Description Patterns That Work

```yaml
# Action-focused
description: Generate database migrations for PostgreSQL. Use when creating tables, adding columns, or modifying schemas.

# Tool-focused
description: Work with Axum web framework in Rust. Handles routing, extractors, state management, and middleware configuration.

# Workflow-focused
description: Deploy to production. Runs tests, builds assets, pushes to registry, and updates infrastructure.
```

## Progressive Disclosure

Keep `SKILL.md` under 500 lines. Put detailed reference material in separate files:

```markdown
# Main Skill Content

Core instructions here...

For API reference, see [reference.md](reference.md).
For examples, see [examples.md](examples.md).
```

Claude loads supporting files only when the task requires them—keeps context focused.

**Rules:**
- Keep references one level deep (A links to B, not B links to C)
- Scripts in `scripts/` are executed, not loaded into context
- Link supporting files explicitly so Claude knows they exist

## Writing Good Instructions

**Assume Claude is smart.** Don't over-explain. Only add context Claude genuinely needs.

**Use appropriate freedom levels:**
- **High freedom** (text instructions): When multiple approaches are valid
- **Medium freedom** (pseudocode): When preferred patterns exist
- **Low freedom** (exact scripts): When operations are fragile or must be consistent

**Structure instructions with:**
- Clear headers for different concerns
- Bullet points for steps/rules
- Code blocks for exact commands or patterns
- Examples showing expected input/output

## Testing Skills

Before relying on a skill, test three scenarios:

1. **Normal case** - Typical request that should trigger it
2. **Edge case** - Unusual or incomplete input
3. **Out-of-scope** - Related request that should NOT trigger it

If the skill isn't triggering:
- Description is too vague—add specific verbs and domain terms
- Conflicting with another skill—differentiate trigger terms

If the skill triggers when it shouldn't:
- Description is too broad—add boundaries
- Add "Do NOT use for..." statements

## Skills vs Other Customization

| Approach | Trigger | Use Case |
|----------|---------|----------|
| **Skills** | Auto (Claude chooses) | Specialized workflows with supporting files |
| **Slash commands** | Manual (`/command`) | Guaranteed execution, simple prompts |
| **CLAUDE.md** | Always loaded | Project-wide rules, always-on context |
| **Subagents** | Delegated | Isolated context for research-heavy tasks |

**Choose skills when:**
- The workflow benefits from supporting files (docs, scripts, templates)
- Claude should recognize when to apply it automatically
- The task is domain-specific but recurs across projects

**Choose slash commands when:**
- You need guaranteed execution (skills might not trigger)
- It's a simple prompt without supporting files
- Terminal discoverability matters (`/` autocomplete)

## Common Patterns

### Read-Only Skills

```yaml
allowed-tools: [Read, Grep, Glob, WebFetch]
```

Prevents accidental writes when skill is for analysis/research.

### Domain Expert Skills

```yaml
---
name: sqlx-expert
description: Work with SQLx in Rust. Handles queries, migrations, compile-time checking, and connection pooling. Use for database code in Rust projects using SQLx.
---

# SQLx Patterns

[Core patterns and gotchas]

For migration guide, see [migrations.md](migrations.md).
For query patterns, see [queries.md](queries.md).
```

### Workflow Skills

```yaml
---
name: deploy-production
description: Deploy to production environment. Runs full test suite, builds release artifacts, and deploys to infrastructure. Use when shipping to prod.
allowed-tools: [Read, Bash, Grep, Glob]
---

# Production Deploy

## Pre-flight Checks
- [ ] All tests pass
- [ ] No uncommitted changes
- [ ] On main branch

## Steps
1. Run test suite: `cargo test --release`
2. Build: `cargo build --release`
3. Deploy: `./scripts/deploy.sh`
```

## Checklist for New Skills

- [ ] Directory created in `~/.claude/skills/skill-name/`
- [ ] `SKILL.md` has valid YAML frontmatter
- [ ] `name` is lowercase-with-hyphens, max 64 chars
- [ ] `description` is specific with action verbs and domain terms
- [ ] Instructions are concise (Claude is smart)
- [ ] Supporting files linked if over 500 lines
- [ ] Tested with normal, edge, and out-of-scope requests
