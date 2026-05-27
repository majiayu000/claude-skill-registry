---
name: command-authoring
description: "Create single-file commands with dynamic content injection (@path and !command). Use when building commands that need filesystem access, git state, runtime context, or argument handling with $1 placeholders. Includes @file injection, !shell execution, <injected_content> wrappers, and single-file structure patterns. Not for skills (use skill-development) or audit workflows."
---

<mission_control>
<objective>Create single-file commands with @path and !command injection for dynamic content and runtime state</objective>
<success_criteria>Command has valid frontmatter, proper @/! injection patterns, and graceful error handling</success_criteria>
</mission_control>

## Quick Start

**If you need to inject file content:** Use `@path` pattern at invocation time.

**If you need to execute shell commands:** Use `` !`command` `` for dynamic state.

**If you need graceful file handling:** Wrap `@path` in `<injected_content>` with fallback text.

**If you need argument handling:** Use `$1` for unique identifiers (IDs, hashes, slugs) only.

## Navigation

| If you need...    | Read this section...             |
| :---------------- | :------------------------------- |
| File injection    | ## PATTERN: @ Path Injection     |
| Command execution | ## PATTERN: ! Command Injection  |
| Structure         | ## PATTERN: Command Structure    |
| Namespacing       | ## PATTERN: Namespacing          |
| Thin interface    | ## PATTERN: Thin Interface       |
| Engine separation | ## PATTERN: Engine Separation    |
| Argument handling | ## PATTERN: Argument Patterns    |
| Anti-patterns     | ## ANTI-PATTERN: Common Mistakes |

## PATTERN: @ Path Injection

### Basic @ Syntax

```markdown
<injected_content>
@.claude/workspace/handoffs/diagnostic.yaml
</injected_content>
```

Or inline:

```markdown
Current handoff: @.claude/workspace/handoffs/latest.yaml
```

### What @ Does

At invocation time, the file content replaces the `@path` pattern. This captures the **current state** of files that change between sessions.

### @ Rules

| Rule                           | Example                            |
| :----------------------------- | :--------------------------------- |
| Wrap in `<injected_content>`   | Semantic grouping                  |
| Use absolute or relative paths | `@/path/file` or `@./path/file`    |
| Content replaces pattern       | File content inlines at invocation |

### @ Use Cases

| Use Case         | Example                              |
| :--------------- | :----------------------------------- |
| Handoff files    | `@.claude/workspace/handoffs/*.yaml` |
| Configuration    | `@.claude/settings.json`             |
| Diagnostic files | `@.claude/workspace/diagnostic.yaml` |

### Error Handling

| Scenario     | Behavior                                  |
| :----------- | :---------------------------------------- |
| File exists  | Injects content                           |
| File missing | Empty result (command handles gracefully) |

### Graceful File Handling

```markdown
<injected_content>
@.claude/workspace/handoffs/diagnostic.yaml
</injected_content>

If file doesn't exist: Create new diagnostic
```

### Multiple File Injection

```markdown
<injected_content>
@.claude/workspace/handoffs/diagnostic.yaml
@.claude/workspace/handoffs/handoff.yaml
</injected_content>
```

---

## PATTERN: ! Command Injection

### Basic ! Syntax

```markdown
Current branch: !`git branch --show-current`
Git status: !`git status --short`
```

### What ! Does

At invocation time, the bash command executes and its output replaces the `` !`command` `` pattern. This captures **runtime state** that changes between invocations.

### ! Rules

| Rule                         | Example                 |
| :--------------------------- | :---------------------- |
| Use backticks                | `` !`command` ``        |
| Standard bash syntax         | `git`, `gh`, `ls`, etc. |
| Output inlines at invocation | stdout replaces pattern |

### ! Use Cases

| Use Case   | Example                                        |
| :--------- | :--------------------------------------------- |
| Git state  | `` !`git branch --show-current``               |
| CI status  | `` !`gh run list --limit 1 --json conclusion`` |
| File stats | `` !`wc -l file.ts``                           |

### Error Handling

| Scenario         | Behavior                                  |
| :--------------- | :---------------------------------------- |
| Command succeeds | Injects stdout                            |
| Command fails    | Empty result (command handles gracefully) |

### Safe Commands

```markdown
✅ Safe:
!`git branch --show-current`
!`gh run list --limit 1 --json conclusion`
!`pwd`
!`ls *.md`

❌ Unsafe:
!`rm file.ts`
!`git push --force`
!`chmod -R 777 .`
```

### Graceful Patterns

```markdown
<injected_content>
@.claude/workspace/handoff.yaml
</injected_content>

If no handoff exists: Create new session

Current branch: !`git branch --show-current 2>/dev/null || echo "detached"`
```

---

## PATTERN: Command Structure

### Single-File Structure

Commands are single markdown files:

```
.claude/commands/folder-name.md
```

Or flat structure:

```
.claude/commands/command-name.md
```

### Flat Structure

```
.claude/commands/analyze.md
.claude/commands/create.md
.claude/commands/verify.md
```

### Nested Structure

```
.claude/commands/analysis/
├── diagnose.md
├── explore.md
└── reason.md
```

### Command Scope

| Scope | Location | Description |
| :---- | :------- | :---------- |
| Project | `.claude/commands/` | Command available in this project only |
| Personal | `~/.claude/commands/` | Command available in all projects |

### Command Components

| Component             | Required? | Notes                       |
| :-------------------- | :-------- | :-------------------------- |
| Frontmatter           | Yes       | YAML with description       |
| ## Quick Start        | Yes       | Scenario-based              |
| Content               | Yes       | With @/! injection          |
| <critical_constraint> | Yes       | At bottom                   |

### What Commands Contain

| Content               | Type     | Notes                  |
| :-------------------- | :------- | :--------------------- |
| Frontmatter           | Required | First content          |
| Quick Start           | Required | Scenario-based         |
| @ injection           | Optional | Dynamic file content   |
| ! injection           | Optional | Dynamic command output |
| <critical_constraint> | Required | At file bottom         |

### What Commands Don't Contain

| Excluded               | Reason                     |
| :--------------------- | :------------------------- |
| references/ folder     | Commands are single-file   |
| SKILL.md               | Skills use this format     |
| Progressive disclosure | Commands load full content |

### Frontmatter Fields

Commands use minimal frontmatter - no `name` field (auto-derived from path):

```yaml
---
description: "Brief description, non spoiling of the content. Use when {trigger condition + keywords + key sentences user might say that should lead the command to be triggered}. Not for {exclusions}."
argument-hint: "<identifier>"  # Optional: hint for positional args
context: fork  # Optional: for orchestration, see ## PATTERN: Thin Interface
---
```

### All Frontmatter Fields

| Field | Required? | Purpose |
| :---- | :-------- | :------- |
| `description` | Yes | Auto-discovery, shown in slash menu |
| `argument-hint` | No | Placeholder for `$1` arguments |
| `context` | No | `fork` for orchestration with result return |
| `hooks` | No | Event hooks configuration |
| `disable-model-invocation` | No | `true` for liaison commands (requires AskUserQuestion) |

### Example Frontmatter

```yaml
---
description: "Refine skill content for quality and portability. Use when improving existing skills, fixing quality issues, or updating documentation. Includes pattern validation and anti-pattern detection. Not for creating new skills from scratch."
argument-hint: "<skill-name>"
hooks:
  PreToolUse:
    - matcher: "tool == \"Bash\" && tool_input.command matches \"rm\""
      type: prompt
      prompt: "About to run rm - confirm this is intentional."
---
```

### Argument Handling

| Syntax | Description | Example |
| :----- | :---------- | :------ |
| `$ARGUMENTS` | Everything after command | `/test auth` → `Run tests matching: auth` |
| `$1`, `$2` | Positional arguments | `/fix 123 high` → Issue #123, priority high |

### String Substitutions

| Variable | Replaces With |
| :------- | :------------ |
| `$ARGUMENTS` | All passed args (appended if missing) |
| `$ARGUMENTS[N]` | Nth arg (0-based) |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |

### Best Practices

1. **Discovery**: Commands available via slash command menu
2. **Security**: Limit `allowed-tools` to essentials when needed
3. **Organization**: Use subdirectories for namespacing complex projects

### Command Frontmatter

```yaml
---
description: "Verb + object. Use when [condition]. Includes [features]. Not for [exclusions]."
---
```

### Command Body

```markdown
## Quick Start

**If you need X:** Do Y

## Core Content

[Content with @ and ! injection patterns]

<injected_content>
@path/to/file.yaml
</injected_content>
```

### Commands vs Skills

| Aspect      | Commands             | Skills                 |
| :---------- | :------------------- | :--------------------- |
| Structure   | Single file          | SKILL.md + references/ |
| Injection   | @, ! supported       | Not supported          |
| Frontmatter | Required             | Required               |
| References  | Optional references/ | Extensive references/  |

## PATTERN: Engine Separation

Commands **SHOULD NOT contain complex logic**. They should:

1. **Gather context** (via @/!)
2. **Ask clarifying questions** (if Liaison)
3. **Invoke the appropriate Skill**

### Anti-Pattern: Command with Logic

```markdown
❌ Wrong: A 200-line "how-to" guide in a command
✅ Correct: 5-line context gatherer → invoke Skill
```

### Command Responsibilities

| Responsibility | Description |
| :------------- | :---------- |
| Context Injection | Use @/! to capture current state |
| Human Negotiation | Use AskUserQuestion to clarify intent |
| Skill Invocation | Delegate to Engine with compiled context |

### When to Move to Skill

Use a Skill instead of a Command when:
- You need `references/` for documentation
- Logic exceeds 50 lines of content
- Multiple patterns and anti-patterns needed
- Complex decision trees required

**Rule: If you need references/, you are building a Skill, not a Command.**

---

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

---

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
4. Skill chaining IS allowed when using `context:forked` in frontmatter

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

### Delegation Pattern

```markdown
## Execution
1. Read the provided skill content.
2. Invoke `skill-development` skill.
3. Compare content against standards.
4. Apply refinements autonomously.
```

### Reality Source Requirement

| Do | Don't |
| :-- | :----- |
| Use `@` for current file state | Assume static content |
| Use `!` for runtime state | Hardcode git status, etc. |
| Provide at least one injection | Create pure logic commands |

---



## PATTERN: Argument Patterns

### Dual-Mode Pattern

Commands can operate in two modes:

| Mode         | Behavior              | Example                                      |
| :----------- | :-------------------- | :------------------------------------------- |
| **Implicit** | Infer from context    | `/handoff:resume` → scans handoffs           |
| **Explicit** | Use provided argument | `/handoff:resume session-x` → loads specific |

### Argument Rules

| Rule                             | Example                    |
| :------------------------------- | :------------------------- |
| `$1` for unique identifiers only | `session-x`, `abc123`      |
| Not for flags/options            | `$1` cannot be `--verbose` |
| Positional only                  | No `--flag value` syntax   |

### Example

```markdown
$IF($1, Use the provided argument, Scan conversation for context and infer intent)
```

### Argument Use Cases

| Use Case     | Example                       |
| :----------- | :---------------------------- |
| Session ID   | `/handoff:resume session-x`   |
| File hash    | `/ops:extract abc123`         |
| Project slug | `/strategy:create my-project` |

### Valid Arguments

```markdown
✅ Valid (identifiers only):
session-abc123  # session ID
hash-xyz789     # file hash
my-project      # project slug
```

### Invalid Arguments

```markdown
❌ Invalid (flags not allowed):
--verbose               # flag
output-format json      # flag with value
--max-results 10        # flag with value
```

---

## PATTERN: Error Handling

### @ Error Behavior

| Scenario     | Result           |
| :----------- | :--------------- |
| File exists  | Content injected |
| File missing | Empty string     |

### ! Error Behavior

| Scenario         | Result          |
| :--------------- | :-------------- |
| Command succeeds | stdout injected |
| Command fails    | Empty string    |

---

## ANTI-PATTERN: Common Mistakes

### Anti-Pattern: Using @ in Skills

```markdown
❌ Wrong (skill):
@injected_content>
@.claude/workspace/file.yaml
</injected_content>

✅ Correct (skill):
Read `references/configuration.md` to understand the schema.
```

**Fix:** Skills use semantic instructions, not @ injection.

### Anti-Pattern: @ for Static Content

```markdown
❌ Wrong:
@.claude/commands/static-template.md

✅ Correct:
[inline the template directly]
```

**Fix:** Use @ for dynamic content (changes between invocations), not static templates.

### Anti-Pattern: No Error Handling

```markdown
❌ Wrong:
Current branch: !`git branch --show-current`
[no fallback]

✅ Correct:
Current branch: !`git branch --show-current` (or detached HEAD)
```

**Fix:** Consider edge cases and provide context.

### Anti-Pattern: $1 for Options

```markdown
❌ Wrong:
--verbose               # using flags
output-format           # option names

✅ Correct:
session-abc123          # identifier only
```

**Fix:** `$1` is for IDs, slugs, hashes only—not flags or options.

### Anti-Pattern: Command with References/

```
❌ Wrong:
.claude/commands/example/
├── command.md
└── references/
    └── detail.md

✅ Correct:
.claude/commands/example.md  # Single file

Or if needed:
.claude/skills/example/
├── SKILL.md
└── references/
```

### Anti-Pattern: Wrong Extension

```
❌ Wrong:
.claude/commands/command.txt
.claude/commands/command

✅ Correct:
.claude/commands/command.md
```

### Anti-Pattern: Inconsistent Naming

```
❌ Wrong:
.claude/commands/create-prompt.md
.claude/commands/run_prompt.md
.claude/commands/runprompt.md

✅ Correct:
.claude/commands/create-prompt.md
.claude/commands/run-prompt.md
.claude/commands/run-prompt.md  # Consistent kebab-case
```

### Anti-Pattern: Complex Logic in !

```
❌ Wrong:
!`for f in *.ts; do echo $f; done`

✅ Correct:
Use bash with proper escaping or inline differently
```

---

## EDGE: Special Cases

### Edge Case: No @ or !

Commands that don't need dynamic content:

```
✅ Valid:
.claude/commands/simple.md
[no @ or ! injection]

Content is static, no dynamic state needed.
```

### Edge Case: Multiple Injections

Commands with complex injection:

```markdown
<injected_content>
@.claude/workspace/handoff.yaml
</injected_content>

Current branch: !`git branch --show-current`
Modified files: !`git status --porcelain`
```

### Edge Case: Nested Wrappers

```markdown
<injected_content>
@main-file.yaml

<details>

<injected_content>
@supporting.yaml
</injected_content>

</details>
</injected_content>
```

### Edge Case: Conditional Injection

```markdown
$IF($1, Use explicit: $1, Infer from context)
```

### Edge Case: Command Grouping

Related commands in folder:

```
.claude/commands/handoff/
├── create.md
├── diagnostic.md
├── resume.md
└── create-full.md
```

### Edge Case: Single Command

No folder needed for single command:

```
.claude/commands/simple.md
```

### Edge Case: Many Commands

Use folders for organization:

```
.claude/commands/
├── analysis/
├── build/
├── handoff/
├── learning/
├── ops/
├── planning/
├── qa/
├── strategy/
└── sync/
```

### Edge Case: Optional Injection

Commands with optional @/!:

```
✅ Valid:
!`git branch --show-current` (or detached)

<injected_content>
@optional-file.yaml
</injected_content>
(if exists)
```

### Edge Case: Multiple Commands

Commands with multiple ! patterns:

```markdown
Branch: !`git branch --show-current`
Status: !`git status --short`
Last commit: !`git log -1 --oneline`
```

### Edge Case: Conditional Arguments

```markdown
$IF($1, Use: $1, Infer from context)
```

---

## Validation Checklist

Before claiming command authoring complete:

**Structure:**
- [ ] Single markdown file in `.claude/commands/`
- [ ] File has `.md` extension
- [ ] Valid YAML frontmatter with description

**Injection Patterns:**
- [ ] @path for dynamic file content (not in skills)
- [ ] !command for runtime state capture
- [ ] Wrapped in `<injected_content>` for semantic grouping
- [ ] Paths are absolute or relative to workspace root

**Error Handling:**
- [ ] Missing files handled gracefully (empty result)
- [ ] Command failures handled gracefully

**Argument Handling:**
- [ ] $1 used only for identifiers (IDs, slugs, hashes)
- [ ] No flags or modes as $1 arguments

**Content:**
- [ ] Follows What-When-Not-Includes format in description
- [ ] Imperative/infinitive voice throughout
- [ ] No references/ folder (commands are single-file)

---

## Common Mistakes to Avoid

### Mistake 1: Using @ or ! in Skills

❌ **Wrong:**
```markdown
# My Skill
Current branch: !`git branch --show-current`
```

✅ **Correct:**
Skills use semantic instructions:
```markdown
# My Skill
Determine the current Git branch using standard git commands.
```

### Mistake 2: Using $1 for Flags

❌ **Wrong:**
```yaml
$1: --verbose
```

✅ **Correct:**
```yaml
$1: session-id  # Only for identifiers
```

### Mistake 3: Missing Frontmatter

❌ **Wrong:**
```markdown
# My Command
description: Does something useful
```

✅ **Correct:**
```yaml
---
name: my-command
description: "Verb + object. Use when [condition]. Includes [features]. Not for [exclusions]."
---
```

### Mistake 4: Complex Bash in !

❌ **Wrong:**
```markdown
!`for f in $(ls *.json); do cat $f | jq '.name'; done`
```

✅ **Correct:**
```markdown
!`find . -name "*.json" -exec jq -r '.name' {} \;`
```

### Mistake 5: Missing Error Handling

❌ **Wrong:**
```markdown
@/path/to/mandatory/file.yaml
```
(If file doesn't exist, command fails)

✅ **Correct:**
```markdown
@/path/to/file.yaml
```
(gracefully handles missing files)
```

---

## Best Practices Summary

✅ **DO:**
- Use @path for dynamic file content that changes between sessions
- Use !command for runtime state (git status, CI results)
- Wrap injections in `<injected_content>` for semantic grouping
- Handle missing files gracefully
- Use $1 only for unique identifiers (IDs, slugs)
- Follow single-file structure (no references/ folder)
- Provide at least one "Reality" source (@ or !)
- Delegate complex logic to Skills

❌ **DON'T:**
- Use @ or ! in skills (skills use semantic instructions)
- Use $1 for flags, modes, or non-identifier values
- Create multi-file commands (use skills instead)
- Skip .md extension
- Skip frontmatter description
- Use complex bash in ! without proper escaping
- Delegate from command to another command (delegate to Skills only)

---

## Recognition Questions

| Question                                | Recognition |
| :-------------------------------------- | :---------- |
| Does @ inject dynamic file content?     | Yes, content changes between sessions |
| Does ! execute for runtime state?       | Yes, captures git status, CI, etc.    |
| Does command use single-file structure? | Yes, no references/ folder            |
| Does $1 use identifier-only pattern?    | Yes, IDs/slugs, not flags             |
| Is XML minimal?                         | Only injected_content wrapper         |
| Does command delegate to Skill?         | Yes, if logic exceeds ~50 lines       |

---

## Validation Checklist

Before claiming command authoring complete:

- [ ] @ injections provide dynamic content
- [ ] ! executions capture runtime state
- [ ] Single-file structure, no references/ folder
- [ ] $1 uses identifier-only pattern
- [ ] XML minimal (only injected_content wrapper)
- [ ] Complex logic delegated to skills

---

<critical_constraint>
**Command-Only Injection:**

1. Skills MUST NEVER use `@` or `!` syntax
2. Commands MAY use `@` and `!` freely
3. Use `<injected_content>` wrapper for semantic grouping
4. All paths MUST be absolute or relative to workspace root

**Namespacing:**

- Commands use folder hierarchy for namespacing
- Path `.claude/commands/meta/refine/rules.md` → `/meta:refine:rules`
- No `name` field in frontmatter (auto-derived from path)
- Only `description` is mandatory in frontmatter

**Thin Interface:**

- Commands are "Skin" that bind Reality to Knowledge Skills ("Brain")
- Commands MUST provide at least one "Reality" source (`@` or `!`)
- Commands MUST NOT delegate to other commands (only to Skills)
- Skill chaining requires `context: forked` in frontmatter for result return
- Without `context: forked`, subprocess results don't reliably return
- Commands SHOULD NOT contain complex logic (delegate to Skills)

**Engine vs Interface:**

- Commands are Interfaces that bind Skills to Reality
- Commands SHOULD NOT contain complex logic (delegate to Skills)
- If you need references/, you are building a Skill, not a Command

@ and ! are command-only features.

Skills MUST use semantic instructions, not injection.

Commands MUST handle missing files gracefully.

Commands MUST be single markdown files.

Commands MUST use .md extension.

Commands MUST have frontmatter with description.
</critical_constraint>
