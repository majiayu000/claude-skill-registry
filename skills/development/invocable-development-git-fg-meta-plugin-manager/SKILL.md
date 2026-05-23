---
name: invocable-development
description: "Create, validate, and audit portable invocable components (commands and skills) for reusable capabilities. Use when building, auditing, or reviewing component quality. Not for agents, hooks, or MCP servers."
---

# Invocable Development

<mission_control>
<objective>Create portable, self-contained invocable components that work in isolation without external dependencies</objective>
<success_criteria>Component created with valid frontmatter, clear description, and appropriate organization for complexity level</success_criteria>
<standards_gate>
MANDATORY: Read skills documentation BEFORE creating components:

- Frontmatter fields → https://code.claude.com/docs/en/skills.md
- Frontmatter patterns → references/frontmatter-reference.md
- Progressive disclosure → references/progressive-disclosure.md
- Quality framework → references/quality-framework.md
  </standards_gate>
  </mission_control>

<trigger>When creating commands or skills. Not for: agents, hooks, or MCP servers (use agent-development, hook-development, mcp-development).</trigger>

## The Fundamental Truth

**Commands and Skills are the same system.**

Both use:

- Same frontmatter format
- Same invocation mechanism
- Same auto-invoke behavior
- Same portability requirements
- Same quality standards

**The only difference is organizational choice.**

---

## Command vs Skill: Organizational Choice

Both commands and skills are **auto-invocable tools** - AI and users can invoke either based on description and context.

The difference is **structural and organizational**:

| Aspect         | Commands                                                                   | Skills                                                         |
| -------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **Structure**  | Single `.md` file                                                          | Folder with `SKILL.md` + optional `workflows/` + `references/` |
| **Naming**     | Folder nesting creates `/category:command` or `/category:subgroup:command` | Flat: `skills/engineering-lifecycle/SKILL.md`                  |
| **File count** | One file                                                                   | Multiple files (main + optional workflows/references)          |
| **Use case**   | Simple operations, categorization, or router patterns                      | Domain knowledge, progressive disclosure, complex workflows    |

### Choose Command When

- Single file is sufficient
- Folder nesting provides useful categorization
- Content fits in one file (~500-1500 words)
- Quick access via `/category:command` naming is valuable
- **Router pattern**: Grouping related operations under a namespace

### Choose Skill When

- Content benefits from multiple files
- SKILL.md contains full philosophy (~500 lines flexible for context)
- Ultra-situational content needs references/ (API specs, code snippets, troubleshooting)
- Multiple workflow files provide better organization
- Examples or scripts should be bundled
- Domain expertise that warrants structured documentation

---

## Command Structure

Commands are single `.md` files. Folder depth determines the invocation name:

### Standard Category Pattern (2 levels)

```
commands/
├── build/
│   └── fix.md         → /build:fix
├── analysis/
│   └── diagnose.md    → /analysis:diagnose
└── planning/
    └── create.md      → /planning:create
```

### Router Pattern (3 levels)

**Use deeper nesting when you need a namespace that groups related operations:**

```
commands/
└── toolkit/
    ├── build/
    │   ├── command.md    → /toolkit:build:command
    │   ├── skill.md      → /toolkit:build:skill
    │   └── package.md    → /toolkit:build:package
    ├── audit/
    │   ├── command.md    → /toolkit:audit:command
    │   └── skill.md      → /toolkit:audit:skill
    └── critique/
        ├── command.md    → /toolkit:critique:command
        └── skill.md      → /toolkit:critique:skill
```

**Router Pattern Characteristics:**

- **3-level structure**: `commands/namespace/action/component.md`
- **Invokes as**: `/namespace:action:component`
- **Purpose**: Group related operations by action type
- **Each command**: Still a single file with self-contained logic
- **Not a skill**: No `SKILL.md`, `workflows/`, or `references/` folders

**When to use Router Pattern:**

- Multiple related operations that share a common namespace
- Toolkit-style organization (e.g., `/toolkit:build:*`, `/toolkit:audit:*`)
- Action-based categorization provides value
- You want to group operations without creating a skill

**Key distinction**: Router commands are still single-file commands. The folder structure is purely organizational - no "router skill" coordinates them.

---

## Skill Structure

```
skill-name/
├── SKILL.md           # Full philosophy, patterns, workflows (~400-600 lines)
├── workflows/         # Optional: separate workflow files
│   ├── workflow-1.md
│   └── workflow-2.md
├── references/        # Optional: ultra-situational lookup (2-3 files)
│   ├── api-spec.md    # API endpoints, field definitions
│   ├── examples.md     # Ready-to-copy code snippets
│   └── troubleshooting.md  # Edge cases, debugging
├── templates/         # Optional: reusable output structures
│   └── template.md
├── scripts/           # Optional: executable automation scripts
│   └── script.sh
└── examples/          # Optional: working demonstrations
    └── example.md
```

**Folder structure** enables progressive disclosure - SKILL.md contains full philosophy and patterns, references/ contains ultra-situational lookup material only.

---

## Both Are Auto-Invocable

**Commands and skills work the same way:**

- AI invokes based on description keywords
- Users invoke via `/name` or `/category:name`
- Same frontmatter format
- Same portability requirements
- Same quality standards

**The choice is about organization, not capability.**

---

## Universal Frontmatter

Both commands and skills use the same frontmatter:

```yaml
---
name: component-name
description: "What it does. Use when [trigger condition]."
argument-hint: "[arg1] [arg2]"
---
```

### Field Reference

| Field           | Required    | Description                                                         |
| --------------- | ----------- | ------------------------------------------------------------------- |
| `name`          | Yes         | Unique identifier (max 64 chars, lowercase letters/numbers/hyphens) |
| `description`   | Recommended | What the component does and when to use it (What-When-Not format)   |
| `argument-hint` | No          | Hint shown during autocomplete indicating expected arguments        |

### Description Guidelines

- Third person (never "I can" or "You can")
- What-When-Not format
- No references to other commands/skills by name
- Clear and actionable

### Argument Hint Guidelines

**Purpose**: Show users what arguments are expected during autocomplete `/` invocation.

**Format**: Use bracket notation for placeholders: `[arg1] [arg2]`

**Examples**:

```yaml
# Single required argument
argument-hint: "[issue-number]"

# Multiple arguments
argument-hint: "[filename] [format]"

# Optional arguments (use ? suffix)
argument-hint: "[filename] [format?]"

# Variadic arguments (use ...)
argument-hint: "[files...]"

# Combined patterns
argument-hint: "[pattern] [path?]"
```

**Best Practices**:

- Keep hints concise (use short, descriptive placeholder names)
- Use `?` suffix for optional arguments
- Use `...` suffix for variadic arguments (accepts multiple values)
- Align hint with actual `$ARGUMENTS` usage in skill body
- Order hints to match argument position: `$0`, `$1`, `$2`...

**When to Use**:

- Skills/commands that accept specific arguments
- Workflow components with clear expected inputs
- When argument structure isn't obvious from description alone
- Skip for simple boolean flags or context-only operations

### Name Validation Rules

- Maximum 64 characters
- Lowercase letters, numbers, hyphens only
- No XML tags
- Reserved words: "anthropic", "claude" are forbidden
- Must match directory name exactly

### Naming Conventions

Use verb-noun convention:

| Pattern     | Purpose                    | Examples                               |
| ----------- | -------------------------- | -------------------------------------- |
| `create-*`  | Building/authoring tools   | `create-agent-skills`, `create-hooks`  |
| `manage-*`  | Managing external services | `manage-facebook-ads`, `manage-stripe` |
| `setup-*`   | Configuration/integration  | `setup-stripe-payments`, `setup-meta`  |
| `analyze-*` | Analysis and inspection    | `analyze-diagnose`, `analyze-security` |

**Avoid**: Vague names (`helper`, `utils`), generic (`documents`, `data`), reserved words (`anthropic-helper`, `claude-tools`).

---

## Universal UHP Structure

For complex components (especially skills), use UHP structure:

### Header (MANDATORY for skills, recommended for complex commands)

```markdown
# Component Name

<mission_control>
<objective>[What this achieves]</objective>
<success_criteria>[How to verify success]</success_criteria>
</mission_control>

<trigger>When [specific condition]. Not for: [exclusion cases].</trigger>

<interaction_schema>
[State flow for reasoning tasks]
</interaction_schema>
```

### Footer (MANDATORY for skills, recommended for commands)

```markdown
---

<trigger>When [specific condition]</trigger>

<critical_constraint>
MANDATORY: [Non-negotiable rule 1]
MANDATORY: [Non-negotiable rule 2]
No exceptions.
</critical_constraint>
```

---

## Universal Best Practices

### Portability

- Self-contained (no external dependencies)
- Work in isolation
- Carry own philosophy

### Autonomy

- 80-95% autonomy (0-5 AskUserQuestion rounds per session)
- Clear triggering conditions
- Concrete patterns and examples

### Quality

- Imperative form (no "you/your")
- Clear examples (working, not pseudo-code)
- Single source of truth

### Templates Folder

Templates are reusable output structures in `templates/` that Claude copies and fills:

```
skill-name/
└── templates/
    ├── plan-template.md
    ├── spec-template.md
    └── report-template.md
```

Use templates when output should have consistent structure. Template syntax uses `{{placeholder}}`:

```markdown
# {{PROJECT_NAME}} Implementation Plan

## Overview

{{1-2 sentence summary}}

## Goals

- {{Primary goal}}
```

### Scripts Folder

Scripts are executable code in `scripts/` that Claude runs as-is:

```
skill-name/
└── scripts/
    ├── deploy.sh
    └── validate.py
```

Well-structured scripts include:

- Clear purpose comment at top
- Input validation
- Error handling
- Idempotent operations
- `set -euo pipefail` for bash

**Security**: Never embed secrets; use environment variables.

---

## Command Orchestration Pattern (Optional)

**This is an optional orchestration archetype, not a requirement.**

One component can orchestrate another for workflow automation.

**Pattern:** Component A orchestrates → Component B

- **Component A (typically command):** Orchestrates workflow, manages interaction flow, coordinates multiple steps
- **Component B (typically skill):** Contains detailed knowledge, patterns, or procedures to execute

**Why this works:** Both are auto-invocable. A command can invoke a skill, which can invoke other components, creating flexible workflows.

**Critical constraint:** Component B MUST NOT reference Component A. This ensures portability - Component B works independently.

See `references/command-orchestration.md` for complete pattern documentation.

---

---

## Dynamic Sourcing Protocol

<fetch_protocol>
**MANDATORY FETCH**: Before creating commands or skills, fetch the content from:

- https://code.claude.com/docs/en/skills.md (frontmatter reference)
- https://agentskills.io/specification.md (Agent Skills specification)

This skill builds on these standards with Seed System-specific patterns and philosophy.
</fetch_protocol>

---

## Navigation

**Official Documentation**:

- Frontmatter reference → https://code.claude.com/docs/en/skills.md
- Agent Skills specification → https://agentskills.io/specification.md

### Toolkit Commands

| If you need...     | Command                     |
| ------------------ | --------------------------- |
| Create a command   | `/toolkit:build:command`    |
| Create a skill     | `/toolkit:build:skill`      |
| Create a package   | `/toolkit:build:package`    |
| Audit a command    | `/toolkit:audit:command`    |
| Audit a skill      | `/toolkit:audit:skill`      |
| Critique (command) | `/toolkit:critique:command` |
| Critique (skill)   | `/toolkit:critique:skill`   |

---

## Absolute Constraints

<critical_constraint>
MANDATORY: All components MUST be self-contained and work in isolation (zero .claude/rules dependency)

MANDATORY: Skills MUST include UHP header (mission_control, trigger, interaction_schema) and footer (critical_constraint)

MANDATORY: Components MUST achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)

MANDATORY: Description MUST use What-When-Not format in third person

MANDATORY: No component references another component by name in description (portability violation)

MANDATORY: If using Command Orchestration Pattern, skill MUST NOT reference invoking command

MANDATORY: Skills with `context: fork` MUST include `<philosophy_bundle>` section carrying essential behavioral rules

**Philosophy Bundle Requirement (context: fork only):**

Forked skills run in isolation and lose access to `.claude/rules/`. To maintain quality standards:

- Identify critical behavioral rules the skill needs
- Include `<philosophy_bundle>` section after main content
- Bundle only BEHAVIORAL rules (not style, not tutorials)
- Ensure skill works correctly in project with ZERO .claude/rules

See `references/advanced-execution.md` - "Philosophy Bundles" section for implementation.

---

<philosophy_bundle>
<portability_invariant>
<mandatory_rule>Every component MUST work with zero .claude/rules dependencies</mandatory_rule>
<recognition_question>Would this work in a project with no .claude/rules?</recognition_question>
</portability_invariant>

<quality_invariant>
<iron_law>NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE</iron_law>
<verification_protocol>
<claims>Mark every factual claim with VERIFIED/INFERRED/UNCERTAIN</claims>
<files>Read actual file before asserting "X exists"</files>
<logic>Trace behavior by reading code, not just grep</logic>
</verification_protocol>
</quality_invariant>

<architecture_invariant>
<uhp>XML for control, Markdown for data</uhp>
<recency_bias>Place critical constraints at bottom of files</recency_bias>
<progressive_disclosure>Tier 2 lean, Tier 3 deep</progressive_disclosure>
</architecture_invariant>

<principles_invariant>
<map_not_script>Provide boundaries and invariants; trust the Pilot</map_not_script>
<delta_standard>Good Component = Expert Knowledge − What Claude Already Knows</delta_standard>
<positive_delta>Only document knowledge Claude wouldn't already have</positive_delta>
</principles_invariant>
</philosophy_bundle>

No exceptions. Portability invariant must be maintained.
</critical_constraint>
