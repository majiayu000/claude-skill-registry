---
name: kit-skill-development
description: (ePost) This skill should be used when the user wants to "create a skill", "add a skill to plugin", "write a new skill", "improve skill description", "organize skill content", or needs guidance on skill structure, progressive disclosure, or skill development best practices for Claude Code plugins.
disable-model-invocation: true
metadata:
  keywords:
    - skill
    - create-skill
    - optimize-skill
    - frontmatter
    - progressive-disclosure
  agent-affinity:
    - epost-fullstack-developer
    - epost-planner
  platforms:
    - all
  connections:
    enhances: [kit-agents]
---

# Skill Development for Claude Code Plugins

Skills are modular packages that extend Claude's capabilities with specialized knowledge, workflows, and tools. Each skill has a required `SKILL.md` and optional bundled resources in `scripts/`, `references/`, and `assets/`.

## Progressive Disclosure (3 levels)

| Level | What | When loaded |
|-------|------|-------------|
| Frontmatter `name` + `description` | ~100 tokens | Always in context |
| `SKILL.md` body | < 5k tokens | When skill triggers |
| `references/`, `scripts/`, `assets/` | Unlimited | On demand by Claude |

**Target SKILL.md body: 150–200 lines (~1,500–2,000 words). Hard max: 500 lines. Move everything else to `references/`.**

## Skill Creation Process (Summary)

1. **Understand use cases** — gather concrete examples from user
2. **Plan resources** — identify what scripts/references/assets are needed
3. **Create structure** — `mkdir -p skills/skill-name/{references,scripts,assets}`
4. **Write SKILL.md** — lean body (imperative form) + third-person description with trigger phrases
5. **Add resources** — populate `references/`, `examples/`, `scripts/` as needed
6. **Validate & iterate** — check structure, triggers, writing style, progressive disclosure

See `references/skill-authoring-guide.md` for detailed steps, examples, and common mistakes.

## SKILL.md Frontmatter

**Required fields:**
```yaml
name: skill-name         # lowercase, hyphens only, matches directory
description: This skill should be used when the user asks to "phrase 1", "phrase 2"...
```

**Valid epost-kit extensions:**
`user-invocable`, `disable-model-invocation`, `context`, `agent`, `keywords`, `platforms`, `triggers`, `agent-affinity`

**Invalid:** `version:` — not a Claude Code frontmatter field.

## Skill Connections

Declare relationships between skills using `metadata.connections`. Extracted into `skill-index.json` during init.

```yaml
metadata:
  connections:
    extends: [parent-skill]        # inherits from; parent loaded before this
    requires: [dependency-skill]   # must be co-loaded for this skill to work
    conflicts: [incompatible-skill] # cannot coexist in same agent
    enhances: [enhanced-skill]     # optional complement; not required
```

**Rules:**
- Only declare direct relationships (not transitive)
- `extends` implies the parent is loaded first — use for specializations (e.g., `ios-a11y` extends `a11y`)
- `requires` means this skill is broken without the dependency — use sparingly
- `conflicts` is bidirectional — if A conflicts B, B should conflict A
- `enhances` is advisory — hints at useful pairings without hard dependency

## Writing Style

- **Description (frontmatter):** Third person — "This skill should be used when the user asks to..."
- **Body:** Imperative/infinitive form — "Configure X", "Validate Y" (not "You should...")

## Skill Directory Structures

**Minimal:**
```
skill-name/
└── SKILL.md
```

**Standard (recommended):**
```
skill-name/
├── SKILL.md
└── references/
    └── detailed-guide.md
```

**Complete:**
```
skill-name/
├── SKILL.md
├── references/
│   ├── patterns.md
│   └── advanced.md
├── assets/
│   └── template.json
└── scripts/
    └── validate.sh
```

## Extended Thinking (`ultrathink`)

Anthropic supports the `ultrathink` keyword to trigger extended thinking in Claude models.

- **When to use**: complex multi-step orchestration, deep architecture decisions, root cause analysis with many unknowns
- **When NOT to use**: simple workflows, lookup tasks, CRUD operations, anything with a clear single answer
- **How**: include the word `ultrathink` naturally in the skill body where deep reasoning is needed — Claude detects it and activates extended thinking mode
- Extended thinking increases token usage; use only where depth outweighs speed

## CSO: Cognitive Skill Optimization

Skills only work if models follow the body, not just the description. CSO prevents the "Description Trap" — where a description that summarizes workflow causes the model to skip the skill body entirely.

**Key rules:**
- Description = triggering conditions ONLY (when/who/situation), never workflow steps
- Discipline skills MUST include: Iron Law block, Anti-Rationalization table, Red Flags list
- Close every loophole explicitly — models find workarounds to vague instructions
- Add foundational principle: "Violating the letter of the rules IS violating the spirit"

See `references/cso-principles.md` for the full guide with examples, bad/good descriptions, token budgets, and anti-rationalization table format.

## agentskills.io Compliance Rules

- `SKILL.md` MUST be in skill root (only `.md` in root)
- Reference docs → `references/`, data files → `assets/`, scripts → `scripts/`
- `name:` MUST be lowercase with hyphens only — **no `/`, spaces, or underscores** per spec
  (Note: epost-kit uses `/` as a namespace extension, e.g. `ios-a11y` — intentional divergence)

## Sub-Skill Routing

When this skill is active and user intent matches a sub-skill, delegate:

| Intent | Sub-Skill | When |
|--------|-----------|------|
| Add new skill | `kit-add-skill` | `/kit-add-skill`, create skill |
| Optimize skill | `kit-optimize-skill` | `/kit-optimize-skill`, improve existing |
| Add new agent | `kit-add-agent` | `/kit-add-agent`, create agent |
| Add new hook | `kit-add-hook` | `/kit-add-hook`, create hook |

## Reference Files

- **`references/skill-authoring-guide.md`** — Step-by-step creation, writing style details, common mistakes, examples from plugin-dev
- **`references/skill-structure.md`** — Full anatomy, bundled resource types, string substitutions, progressive disclosure deep-dive, validation checklist
- **`references/description-validation-checklist.md`** — Checklist for validating skill description quality (form, length, keywords, anti-patterns)
