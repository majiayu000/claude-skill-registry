---
name: command-development
description: "Create and refine single-file commands with @/! injection. Use when authoring new commands or improving existing ones. Includes namespacing rules, thin interface patterns, and delegation best practices. Not for skills or agents."
---

<mission_control>
<objective>Create and audit commands that follow toolkit standards: proper namespacing, thin interface, and skill delegation</objective>
<success_criteria>Command has valid namespacing, provides reality source, and delegates to appropriate Knowledge Skill</success_criteria>
</mission_control>

## Quick Start

**If you need to create a command:** Place in folder matching hierarchy (e.g., `.claude/commands/meta/refine/rules.md`).

**If you need to audit a command:** Invoke this skill directly to validate structure and patterns.

**If you need to refine a command:** Compare against patterns and apply fixes.

## Navigation

| If you need... | Read this section... |
| :------------- | :------------------- |
| Namespacing rules | ## PATTERN: Namespacing |
| Thin interface pattern | ## PATTERN: Thin Interface |
| Frontmatter format | ## PATTERN: Frontmatter |
| Perfect command examples | ## PATTERN: Perfect Command |
| Common failures | ## ANTI-PATTERN: Common Failures |
| Validation checklist | ## Validation Checklist |

## Philosophy

Commands are stateless interfaces that bind Reality to logic. Unlike skills (which are self-contained knowledge), commands exist at the boundary between Claude and the filesystem, injecting dynamic content at invocation time.

**Key insight:** Commands are "Skin" - thin wrappers that gather context and delegate to Knowledge Skills ("Brain"). They should contain minimal logic.

**Why this matters:**
- Commands are auto-named from file paths (no `name` field in frontmatter)
- Commands use `@` and `!` for dynamic content injection
- Commands are single-file (no `references/` folder)
- Commands delegate to Skills for complex logic

## PATTERN: Namespacing

Commands use folder hierarchy for namespacing. Path maps to colon syntax:

| Folder Path | Command Invocation |
|-------------|-------------------|
| `.claude/commands/meta/refine/rules.md` | `/meta:refine:rules` |
| `.claude/commands/strategy/architect.md` | `/strategy:architect` |
| `.claude/commands/meta/audit/all.md` | `/meta:audit:all` |

### Namespacing Rules

| Rule | Example |
| :--- | :------- |
| No `name` field in frontmatter | Auto-derived from path |
| Only `description` is mandatory | Frontmatter is minimal |
| `argument-hint` optional | `"<skill-name>"` |
| Folders create namespace hierarchy | `meta/refine/` → `/meta:refine:` |

### Flat vs Namespaced

| Type | Use When | Example |
| :--- | :-------- | :------- |
| Flat | Core, high-frequency commands | `/continue`, `/handoff` |
| Namespaced | Related commands, complex domains | `/meta:refine:rules` |

### Namespace Categories

| Namespace | Purpose | Example Commands |
| :--------- | :------ | :---------------- |
| `meta/*` | Toolkit self-improvement | refine, audit, reflect, capture |
| `strategy/*` | Planning and execution | architect, execute |
| `handoff/*` | Session continuity | resume, diagnostic |
| `learning/*` | Knowledge capture | archive, refine-rules |

## PATTERN: Thin Interface

Commands are "Skin" - thin interfaces that bind Reality to Knowledge Skills ("Brain").

### Three Command Use-Cases

| Use-Case | Pattern | Example |
| :-------- | :------- | :------- |
| Context Gathering | `@` and `!` injection | Gather git state, file content |
| Liaison Work | `AskUserQuestion` | Clarify ambiguous intent |
| Delegation | `Skill(tool)` invocation | Call Knowledge Skill for logic |

### Thin Interface Rules

1. Commands MUST provide at least one "Reality" source (`@` or `!`)
2. Commands SHOULD NOT contain complex logic - delegate to Skills
3. Commands MUST NOT delegate to other commands (only to Skills)
4. Skill chaining requires `context: forked` in frontmatter for result return
5. Without `context: forked`, subprocess results don't reliably return

### Context Forking (Orchestration)

When a command/skill must orchestrate subprocesses and receive their results:

**Without `context:forked`:**
```markdown
---
description: "Call skill B."
---
1. Invoke `skill-b` skill.
2. [Skill A ends here - unreliable return]
```

Skill B runs but results don't reliably return to Skill A.

**With `context:forked`:**
```yaml
---
description: "Call skill B with result return."
context: forked
---
```

```markdown
1. Invoke `skill-b` skill.
2. [Skill B completes, result returns to Skill A]
3. Process skill B results...
```

**How it works:**
- `context: forked` in frontmatter makes the component behave like a subagent
- Results reliably return to the parent for analysis
- Essential for: multi-step workflows, result aggregation, orchestration

### Reality Source Requirement

| Do | Don't |
| :-- | :----- |
| Use `@` for current file state | Assume static content |
| Use `!` for runtime state | Hardcode git status, etc. |
| Provide at least one injection | Create pure logic commands |

### Delegation Pattern

```markdown
## Execution
1. Read the provided skill content.
2. Invoke `skill-development` skill.
3. Compare content against standards.
4. Apply refinements autonomously.
```

## PATTERN: Frontmatter

Commands use minimal frontmatter:

```yaml
---
description: "Brief description, non spoiling of the content. Use when {trigger condition + keywords + key sentences user might say that should lead the command to be triggered}. Not for {exclusions}."
argument-hint: "<identifier>"  # Optional
context: fork  # Optional: for orchestration, see ## PATTERN: Thin Interface
---
```

### Frontmatter Fields

| Field | Required? | Purpose |
| :---- | :-------- | :------- |
| `description` | Yes | Auto-discovery, shown in slash menu |
| `argument-hint` | No | Placeholder for `$1` arguments |
| `context` | No | `fork` for orchestration with result return |
| `hooks` | No | Event hooks configuration |
| `disable-model-invocation` | No | `true` for liaison commands |

### Description Format

| Element | Purpose | Required? |
| :------ | :------- | :-------- |
| Brief description | Action summary (non-spoiling) | Yes |
| "Use when" | Activation conditions | Yes |
| Keywords/triggers | User phrases that activate | Yes |
| "Not for" | Exclusions | Yes |

### Description Examples

**Basic:**
```yaml
description: "Create portable skills with SKILL.md. Use when building new skills or documenting reusable patterns."
```

**Intermediate:**
```yaml
description: "Refine skill content for quality. Use when improving existing skills, fixing quality issues, or updating documentation. Not for creating new skills from scratch."
```

**Gold Standard:**
```yaml
description: "Autonomously correct project rules when negative feedback occurs. Use PROACTIVELY when user says 'no', 'wrong', 'wait', 'not that', or 'actually'. Identifies root cause and rewrites offending instruction. Not for new feature requests or unrelated changes."
```

## PATTERN: Perfect Command

### Simple Command (Context Gathering)

```markdown
---
description: "Show current git state. Use when needing branch and status information. Includes branch name, status, and modified files."
---

<mission_control>
<objective>Display current git state for context</objective>
<success_criteria>Git branch and status displayed</success_criteria>
</mission_control>

## Quick Start
Current git state shown below.

## Git State

<injected_content>
!`git branch --show-current`
!`git status --short`
</injected_content>
```

### Medium Command (With Delegation)

```markdown
---
description: "Refine skill content for quality. Use when improving existing skills. Includes pattern validation. Not for creating new skills."
argument-hint: "<skill-name>"
---

<mission_control>
<objective>Refine skill to meet quality standards</objective>
<success_criteria>Skill passes all validation checks</success_criteria>
</mission_control>

## Quick Start
Refining skill: $1

## Context

Current Skill: @.claude/skills/$1/SKILL.md
Project State: !`ls .claude/skills`

## Execution
1. Read the provided skill content.
2. Invoke `skill-development` skill.
3. Compare content against standards.
4. Apply refinements autonomously.
```

### Complex Command (Liaison + Delegation)

```markdown
---
description: "Clarify intent and delegate to appropriate engine. Use when user intent is ambiguous. Includes clarification questions. Not for clear intents."
disable-model-invocation: true
---

<mission_control>
<objective>Clarify ambiguous intent and route to appropriate handler</objective>
<success_criteria>User intent clarified and routed to correct engine</success_criteria>
</mission_control>

## Clarification
[AskUserQuestion to determine user intent]

## Execution
[Based on answer, invoke appropriate Knowledge Skill]
```

## ANTI-PATTERN: Common Failures

### Anti-Pattern: No Reality Source

```markdown
❌ Wrong:
---
description: "Validate skill structure."
---
## Execution
1. Read skill content.
2. Check frontmatter.
3. Validate structure.
```

**Fix:** Add `@` or `!` to provide reality source:
```markdown
✅ Correct:
---
description: "Validate skill structure."
---
## Context
Skill: @.claude/skills/$1/SKILL.md
```

### Anti-Pattern: Command Contains Complex Logic

```markdown
❌ Wrong:
---
description: "Create perfect skill."
---
## Execution
1. Write frontmatter.
2. Add Quick Start section.
3. Add Navigation table.
4. Add Philosophy section.
5. Add PATTERN sections.
6. Add ANTI-PATTERN sections.
7. Add Validation Checklist.
8. Add critical_constraint.
```

**Fix:** Delegate to Knowledge Skill:
```markdown
✅ Correct:
---
description: "Create perfect skill."
---
## Execution
1. Read `skill-development` skill.
2. Invoke `skill-development` skill with context.
3. Apply refinements.
```

### Anti-Pattern: References Folder

```
❌ Wrong:
.claude/commands/example/
├── command.md
└── references/
    └── detail.md

✅ Correct:
.claude/skills/example/
├── SKILL.md
└── references/
    └── detail.md
```

**Fix:** Commands are single-file. If you need `references/`, build a Skill.

### Anti-Pattern: Slash Command Reference

```markdown
❌ Wrong:
---
description: "Run meta refinement. See /meta:refine:all for details."
---
```

**Fix:** Never reference slash commands:
```markdown
✅ Correct:
---
description: "Run meta refinement. Use when improving multiple components. Orchestrates all refine operations."
---
```

### Anti-Pattern: Missing Frontmatter Description

```markdown
❌ Wrong:
---
# My Command
## Quick Start
Do something.
---
```

**Fix:** Add proper frontmatter:
```markdown
✅ Correct:
---
description: "Do something. Use when [condition]. Includes [features]."
---
## Quick Start
Do something.
```

## Validation Checklist

Before claiming command authoring complete:

**Structure:**
- [ ] Single markdown file in `.claude/commands/`
- [ ] File has `.md` extension
- [ ] No `name` field in frontmatter (auto-derived)
- [ ] Valid frontmatter with description

**Namespacing:**
- [ ] File path matches intended command invocation
- [ ] Folders used for namespacing if applicable

**Injection:**
- [ ] At least one `@` or `!` injection present
- [ ] Injections wrapped in `<injected_content>` if grouping
- [ ] Missing files handled gracefully

**Thin Interface:**
- [ ] Command delegates to Knowledge Skill for logic
- [ ] Command does not contain complex logic
- [ ] Command does not reference slash commands

**Frontmatter:**
- [ ] Description uses "Use when" format
- [ ] `argument-hint` present if command uses `$1`

---

## Recognition Questions

| Question | Recognition |
| :------- | :---------- |
| Command uses namespacing? | Path maps to colon syntax (/path/to/cmd → /path:to:cmd) |
| Command has reality source? | At least one @ or ! injection |
| Command delegates to Skill? | Yes, for complex logic |
| Command references /meta? | No, never references slash commands |
| Command uses single-file? | Yes, no references/ folder |
| Frontmatter has description? | With "Use when" clause and "Not for" exclusions |

---

## Validation Checklist

Before claiming command complete:

- [ ] Namespacing follows path-to-colon syntax
- [ ] At least one @ or ! injection provides reality source
- [ ] Complex logic delegated to skills (not commands)
- [ ] No references to slash commands
- [ ] Single-file format, no references/ folder
- [ ] Description follows What-When-Not format
- [ ] Argument hints for positional parameters if applicable
- [ ] context: fork for orchestration with result return

---

<critical_constraint>
**Portability:**

1. This skill MUST NEVER reference a slash command (e.g., /meta)
2. Skills never know about commands that trigger them
3. All validation logic MUST reside in this skill
4. Never use relative paths pointing outside the skill itself. When referencing other components, use: "invoke `skill-name`" or "invoke `skill-name` and read its file"

**Self-Contained:**

1. Command validation patterns MUST be documented here
2. No external dependencies for validation
3. Fork isolation (works in vacuum)

**Thin Interface:**

1. Commands MUST provide at least one reality source (@ or !)
2. Commands MUST NOT delegate to other commands
3. Skill chaining requires `context: forked` in frontmatter for result return
4. Without `context: forked`, subprocess results don't reliably return
</critical_constraint>
