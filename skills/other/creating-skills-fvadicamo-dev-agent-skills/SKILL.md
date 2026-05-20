---
name: creating-skills
description: Guide for creating Claude Code skills following Anthropic's official best practices. Use when user wants to create a new skill, build a skill, write SKILL.md, update an existing skill, or needs skill creation guidelines. Provides structure, frontmatter fields, naming conventions, and new features like dynamic context injection and subagent execution.
---

# Creating skills

Guide for creating Claude Code skills following Anthropic's official best practices.

## Quick start

```bash
# 1. Create skill directory
mkdir -p ~/.claude/skills/<skill-name>

# 2. Create SKILL.md with frontmatter
cat > ~/.claude/skills/<skill-name>/SKILL.md << 'EOF'
---
name: <skill-name>
description: <What it does>. Use when <trigger phrases>. <Key capabilities>.
---

# <Skill title>

<Instructions for the skill workflow>
EOF

# 3. Add optional resources as needed
mkdir -p ~/.claude/skills/<skill-name>/{scripts,references,assets}
```

## SKILL.md structure

### Frontmatter (YAML between `---` markers)

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name. Defaults to directory name. Lowercase, hyphens, max 64 chars. |
| `description` | Recommended | What + when + capabilities. Max 1024 chars. Determines when Claude activates the skill. |
| `allowed-tools` | No | Tools Claude can use without asking permission when skill is active. |
| `argument-hint` | No | Autocomplete hint for arguments. Example: `[issue-number]` |
| `disable-model-invocation` | No | `true` to prevent auto-invocation (manual `/name` only). |
| `user-invocable` | No | `false` to hide from `/` menu (background knowledge only). |
| `model` | No | Model override when skill is active. |
| `context` | No | `fork` to run in isolated subagent context. |
| `agent` | No | Subagent type when `context: fork`. Built-in: `Explore`, `Plan`, `general-purpose`. |
| `hooks` | No | Lifecycle hooks scoped to this skill. |

### Invocation control matrix

| Configuration | User can invoke | Claude can invoke |
|---------------|-----------------|-------------------|
| (defaults) | Yes | Yes |
| `disable-model-invocation: true` | Yes | No |
| `user-invocable: false` | No | Yes |

### Description formula

```
<What it does>. Use when <trigger phrases>. <Key capabilities>.
```

Include action verbs ("create", "handle"), user intent ("wants to", "needs to"), and domain keywords users would say.

## Directory structure

```
skill-name/
├── SKILL.md              # Required: instructions (keep under 500 lines)
├── scripts/              # Optional: executable code (deterministic, token-efficient)
├── references/           # Optional: docs loaded into context on demand
└── assets/               # Optional: files used in output, NOT loaded into context
                          #   (templates, images, fonts, boilerplate)
```

### Progressive disclosure (3-level loading)

1. **Metadata** (name + description) - always in context (~100 tokens per skill)
2. **SKILL.md body** - loaded when skill triggers (keep under 5k words)
3. **Bundled resources** - loaded as needed by Claude

Reference supporting files from SKILL.md so Claude knows they exist. Keep references one level deep. For files over 100 lines, include a table of contents.

### Scripts vs references vs assets

| Type | Purpose | Loaded into context? |
|------|---------|---------------------|
| `scripts/` | Deterministic operations, complex processing | No (executed via bash) |
| `references/` | Documentation Claude reads while working | Yes, on demand |
| `assets/` | Templates, images, fonts for output | No (copied/used in output) |

Only create scripts when they add value: complex multi-step processing, repeated code generation, deterministic reliability. Not for single-command wrappers.

## Dynamic features

### Context injection

Inject shell command output into skill content before loading:

```markdown
## Recent commits
!`git log --oneline -5 2>/dev/null`
```

The output replaces the directive when the skill loads.

### String substitutions

Pass arguments to skills invoked via `/skill-name arg1 arg2`:

| Variable | Value |
|----------|-------|
| `$ARGUMENTS` | Full argument string |
| `$ARGUMENTS[0]`, `$ARGUMENTS[1]` | Individual arguments |
| `$1`, `$2` | Shorthand for `$ARGUMENTS[N]` |

### Subagent execution

Run a skill in isolated context with `context: fork`:

```yaml
---
name: deep-research
description: Research a topic thoroughly.
context: fork
agent: Explore
---
```

## Degrees of freedom

Match specificity to the task's fragility:

| Level | When to use | Example |
|-------|-------------|---------|
| **High** (text instructions) | Multiple valid approaches, context-dependent | "Analyze the code and suggest improvements" |
| **Medium** (pseudocode/scripts with params) | Preferred pattern exists, some variation OK | Script with configurable parameters |
| **Low** (specific scripts, few params) | Fragile operations, consistency critical | Exact sequence of API calls |

## Naming conventions

- Lowercase, hyphens between words, max 64 chars
- Styles: gerund (`processing-pdfs`), noun phrase (`github-pr-creation`), prefixed group (`github-pr-*`)

## Important rules

- **ALWAYS** write descriptions that include WHAT + WHEN triggers + capabilities
- **ALWAYS** keep SKILL.md under 500 lines, split to references when approaching
- **ALWAYS** reference bundled files from SKILL.md so Claude discovers them
- **NEVER** duplicate info between SKILL.md and reference files
- **NEVER** create wrapper scripts for single commands
- **NEVER** include extraneous files (README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md)
- **NEVER** explain things Claude already knows (standard libraries, common tools, basic patterns)

## References

- `references/official_best_practices.md` - Principles, anti-patterns, quality checklist, testing
- `references/skill_examples.md` - Concrete skill examples with new features
