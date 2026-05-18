# Official best practices for skills

Source: [Claude Code skills docs](https://code.claude.com/docs/en/skills), [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview), [Anthropic skills repo](https://github.com/anthropics/skills)

---

## Core principle: Claude is already smart

> "Default assumption: Claude is already very smart. Only add context Claude doesn't already have."

**Challenge each piece of information:**
- Does Claude really need this explanation?
- Can I assume Claude knows this?
- Does this paragraph justify its token cost?

**What NOT to include**: basic programming concepts, common tool usage (git, npm), standard library docs, well-known patterns.

**What TO include**: project-specific conventions, custom workflows, non-obvious requirements, domain knowledge Claude wouldn't have.

## Progressive disclosure

Skills use a three-level loading system:

1. **Metadata** (name + description) - always in context (~100 words per skill)
2. **SKILL.md body** - when skill triggers (<5k words recommended)
3. **Bundled resources** - as needed (scripts execute without loading; references load on demand)

### Context budget

Skill descriptions share a budget that scales at 2% of the context window, with a fallback of 16,000 characters. Override with `SLASH_COMMAND_TOOL_CHAR_BUDGET` env var.

### Splitting patterns

When SKILL.md approaches 500 lines, split content into separate files:

- **Pattern 1: High-level guide with references** - Keep workflow in SKILL.md, move detailed docs to references/
- **Pattern 2: Domain-specific organization** - One reference per domain area (e.g., `references/api_docs.md`, `references/schemas.md`)
- **Pattern 3: Conditional details** - Keep decision logic in SKILL.md, move variant-specific details to references/

**Guidelines:**
- Avoid deeply nested references - keep one level deep from SKILL.md
- For files over 100 lines, include a table of contents at the top
- For very large references (>10k words), include grep search patterns in SKILL.md
- Information should live in either SKILL.md OR references, not both

## Frontmatter validation rules

| Field | Constraint |
|-------|-----------|
| `name` | Max 64 chars, lowercase + numbers + hyphens only, no XML tags, no reserved words ("anthropic", "claude") |
| `description` | Max 1024 chars, non-empty if provided, no XML tags |
| Allowed properties | `name`, `description`, `license`, `allowed-tools`, `metadata`, `compatibility`, `argument-hint`, `disable-model-invocation`, `user-invocable`, `model`, `context`, `agent`, `hooks` |

## Skills and commands unification

Custom slash commands (`.claude/commands/*.md`) and skills (`.claude/skills/*/SKILL.md`) are now unified. Both create `/name` invocations and support the same frontmatter. Existing commands files continue to work. If a skill and a command share the same name, the skill takes precedence.

## Discovery hierarchy

Skills are discovered from multiple locations (higher priority wins):

1. **Enterprise** (managed settings)
2. **Personal** (`~/.claude/skills/`)
3. **Project** (`.claude/skills/`)
4. **Plugin** (namespaced as `plugin-name:skill-name`)

Additional directories via `--add-dir` are also supported with live change detection.

## User confirmation patterns

**ALWAYS confirm before:**
- Modifying user files
- Running destructive commands
- Creating external resources (PRs, issues, deployments)
- Irreversible operations

**Don't over-confirm:**
- Read-only operations
- Reversible actions
- Intermediate steps in an approved workflow

## Anti-patterns

| Pattern | Problem | Instead |
|---------|---------|---------|
| Wrapper scripts | No value added | Inline commands |
| Verbose explanations | Token waste | Trust Claude's knowledge |
| Multiple paths | Confusing | One clear workflow |
| Custom systems | Non-standard | Use official patterns |
| Over-confirmation | Friction | Confirm only critical actions |
| Deeply nested references | Hard to discover | Keep one level deep |
| Duplicated info | Drift risk, token waste | Single source of truth |
| Extraneous files | Clutter | Only SKILL.md + resources |

## Quality checklist

Before finalizing a skill:

- [ ] **Frontmatter**: description present, clear, under 1024 chars
- [ ] **Description**: includes WHAT + WHEN triggers + capabilities
- [ ] **Naming**: lowercase, hyphens, max 64 chars
- [ ] **Body**: under 500 lines, no duplication with references
- [ ] **Resources**: referenced from SKILL.md, one level deep
- [ ] **Scripts**: only value-add, not wrappers
- [ ] **Rules**: critical constraints marked with **ALWAYS**/**NEVER**
- [ ] **Test**: skill triggers on expected phrases

## Testing

### Trigger testing
Verify skill activates on expected user phrases. Test with multiple phrasings.

### Model testing
Test with all models you plan to support (Haiku, Sonnet, Opus have different capabilities). Build evaluations before writing extensive documentation.

### Edge cases
- Missing prerequisites
- Invalid input
- Partial completion

## What NOT to include in a skill

A skill should only contain files that directly support its functionality:

- No README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md
- No user-facing documentation (the skill IS the documentation for Claude)
- No setup/testing procedures
- No auxiliary context about the creation process
