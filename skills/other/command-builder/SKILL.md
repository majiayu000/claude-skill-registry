---
name: command-builder
type: standard
depth: base
description: >-
    Generates slash commands with YAML frontmatter, $ARGUMENTS/positional params, and tool permissions. Use when creating .claude/commands/*.md files or fixing command routing.
---

# [H1][COMMAND-BUILDER]
>**Dictum:** *Reusable prompt templates reduce repetition and enforce consistency.*

<br>

Load commands from `.claude/commands/` (project) or `~/.claude/commands/` (user). Filename becomes command name.

**Tasks:**
1. Read [index.md](./index.md) — Reference file listing for navigation
2. Read [workflow.md](./references/workflow.md) — 5-phase creation process
3. Read [variables.md](./references/variables.md) — Argument capture, file references, skill loading
4. Read [hints.md](./references/hints.md) — Argument-hint syntax, enum patterns
5. (prose) Load `style-standards` skill — Voice, formatting, constraints
6. Execute per workflow — UNDERSTAND, ACQUIRE, RESEARCH, AUTHOR, VALIDATE
7. Validate — Quality gate; see §VALIDATION

[REFERENCE]: [index.md](./index.md) — Complete reference file listing

---
## [1][FRONTMATTER]
>**Dictum:** *Declarative constraints gate command execution.*

<br>

```yaml
---
description: Brief description shown in /help menu
argument-hint: [required-arg] [optional-arg?]
allowed-tools: Read, Write, Edit, Glob, Grep, Task, Bash, TaskCreate
model: opus
---
```

| [INDEX] | [FIELD]             | [TYPE] | [PURPOSE]               | [SYNTAX]                                |
| :-----: | ------------------- | ------ | ----------------------- | --------------------------------------- |
|   [1]   | **`description`**   | string | `/help` menu text       | Verb-first. <80 chars. Outcome-focused. |
|   [2]   | **`argument-hint`** | string | Autocomplete guidance   | `[required]` `[optional?]` `[--flag]`.  |
|   [3]   | **`allowed-tools`** | list   | Scoped tool permissions | Comma-separated tool names.             |
|   [4]   | **`model`**         | string | Override default model  | Full model ID or alias.                 |

[IMPORTANT]:
- [ALWAYS] Use `---` delimiters (three dashes, no spaces).
- [ALWAYS] Quote strings containing `:`, `#`, `[`, `]`, `{`, `}`.
- [NEVER] Use tabs; YAML requires spaces.

[CRITICAL]:
- [ALWAYS] Declare `Read` for every `@path` reference.
- [ALWAYS] Declare `Bash` for every `!command` reference.
- [NEVER] Omit required tools—command fails without output.

---
## [2][MODELS]
>**Dictum:** *Model selection balances capability against cost and latency.*

<br>

[CRITICAL] Session inherits default model. Override for specific capability requirements.

| [INDEX] | [ALIAS]  | [STRENGTH]           | [LATENCY] | [COST] |
| :-----: | -------- | -------------------- | :-------: | :----: |
|   [1]   | `opus`   | Complex reasoning    |   High    |  High  |
|   [2]   | `sonnet` | Balanced performance |  Medium   | Medium |
|   [3]   | `haiku`  | Fast, simple tasks   |    Low    |  Low   |

| [INDEX] | [CHARACTERISTIC]         | [OPUS] | [SONNET] | [HAIKU] |
| :-----: | ------------------------ | :----: | :------: | :-----: |
|   [1]   | **Multi-file scope**     |   X    |          |         |
|   [2]   | **Architectural impact** |   X    |          |         |
|   [3]   | **Standard development** |        |    X     |         |
|   [4]   | **Speed priority**       |        |          |    X    |
|   [5]   | **Deep analysis**        |   X    |    X     |         |

---
## [3][VARIABLES]
>**Dictum:** *Dynamic substitution enables reusable commands.*

<br>

| [INDEX] | [SYNTAX]                   | [CAPTURES]                              | [REQUIRED_TOOL] | [USE_WHEN]           |
| :-----: | -------------------------- | --------------------------------------- | --------------- | -------------------- |
|   [1]   | **`$ARGUMENTS`**           | All args as string                      | None            | Free-form input      |
|   [2]   | **`$1`, `$2`...**          | Positional (1-based)                    | None            | Structured multi-arg |
|   [3]   | **`$ARGUMENTS[N]`**        | Positional (0-based)                    | None            | Indexed access       |
|   [4]   | **`$N`**                   | Shorthand for `$ARGUMENTS[N]` (0-based) | None            | Indexed shorthand    |
|   [5]   | **`${1:-val}`**            | Default if missing                      | None            | Optional parameters  |
|   [6]   | **`${CLAUDE_SESSION_ID}`** | Current session ID                      | None            | Session-specific     |
|   [7]   | **`@path`**                | Include file contents                   | `Read`          | File analysis        |
|   [8]   | **`` !`command` ``**       | Shell preprocessing                     | `Bash`          | Dynamic context      |

[CRITICAL]:
- [NEVER] Mix `$ARGUMENTS` and positional `$1-$N` in same command.
- [ALWAYS] Declare required tools for `@path` and `!command`.

[→references/variables.md](./references/variables.md): Complete reference—examples, skill loading, anti-patterns.

---
## [4][PATTERNS]
>**Dictum:** *Canonical patterns accelerate development.*

<br>

### [4.1][FILE_ANALYSIS]

```markdown
---
description: Analyze file for issues
argument-hint: [file-path]
allowed-tools: Read
---
## Target
@$1
## Task
Identify security, performance, and code quality issues.
```

---
### [4.2][MULTI_FILE_OPERATION]

```markdown
---
description: Process files matching pattern
argument-hint: [glob-pattern]
allowed-tools: Read, Edit, Glob, TaskCreate
---
## Task
Match files via $1. Analyze content. Apply fixes. Track progress via TaskCreate.
```

---
### [4.3][AGENT_WORKFLOW]

```markdown
---
description: Multi-agent analysis
argument-hint: [target-folder]
allowed-tools: Task, Read, Glob, TaskCreate
---
## Task
1. Match files in $1 via Glob
2. Spawn analysis agents via Task
3. Synthesize findings, track via TaskCreate
```

---
### [4.4][SKILL_CONTEXT]

```markdown
---
description: Validate target against skill standards
argument-hint: [target] [focus?]
allowed-tools: Read, Task, Glob, Edit, TaskCreate
---
## Skill Context
@.claude/skills/[skill-name]/SKILL.md
@.claude/skills/[skill-name]/references/[domain]/*.md
## Task
Load context above. Spawn Task agents. Verify findings against loaded context. Apply corrections.
```

[→templates/command-template.md](./templates/command-template.md) — canonical template.

---
## [5][ORGANIZATION]
>**Dictum:** *Namespaces prevent command collision.*

<br>

| [INDEX] | [SCOPE]      | [LOCATION]            | [USE_CASE]            |
| :-----: | ------------ | --------------------- | --------------------- |
|   [1]   | **Personal** | `~/.claude/commands/` | Individual workflows  |
|   [2]   | **Project**  | `.claude/commands/`   | Shared team workflows |

| [INDEX] | [CONVENTION]         | [PATTERN]       | [EXAMPLE]          |
| :-----: | -------------------- | --------------- | ------------------ |
|   [1]   | **Verb-first**       | `action-target` | `create-component` |
|   [2]   | **Lowercase**        | No capitals     | `review-pr`        |
|   [3]   | **Hyphen-separated** | No underscores  | `run-tests`        |
|   [4]   | **Descriptive**      | Clear purpose   | `analyze-coverage` |

```text
.claude/commands/
├── git/
│   ├── commit.md  -> /git:commit
│   └── pr.md      -> /git:pr
└── test/
    └── unit.md    -> /test:unit
```

---
## [6][VALIDATION]
>**Dictum:** *Validation gates prevent incomplete artifacts.*

<br>

[VERIFY] Completion:
- [ ] Workflow: All 5 phases executed (UNDERSTAND → VALIDATE).
- [ ] Frontmatter: Valid YAML, description present, tools declared.
- [ ] Variables: No `$ARGUMENTS` + positional mixing.
- [ ] Tools: All `@path` have `Read`, all `!command` have `Bash`.
- [ ] Quality: LOC < 125, verb-first naming.

[REFERENCE] Operational checklist: [→validation.md](./references/validation.md)
