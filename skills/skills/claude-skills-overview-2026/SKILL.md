---
name: claude-skills-overview-2026
description: Reference guide for Claude Code skills system (January 2026). Use when creating, modifying, or understanding skills, SKILL.md format, frontmatter fields, hooks, context fork, or skill best practices.
user-invocable: true
---

# Claude Code Skills System - Complete Reference (January 2026)

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`.

**Skills and slash commands are now unified** - they are the same system. A file at `.claude/commands/review.md` and a skill at `.claude/skills/review/SKILL.md` both create `/review` and work identically. Skills are the recommended approach as they support additional features like supporting files and advanced frontmatter options.

---

## SKILL.md Complete Format

```yaml
---
name: skill-identifier
description: What this Skill does and when to use it
argument-hint: "[optional-arg]"
allowed-tools: Read, Grep, Glob
model: claude-sonnet-4-20250514
context: fork
agent: general-purpose
user-invocable: true
disable-model-invocation: false
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate.sh"
          once: true
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
  Stop:
    - hooks:
        - type: command
          command: "./scripts/cleanup.sh"
---

# Skill Title

Your instructions here...
```

**Validation**: Use `claude plugin validate` to validate plugin structure. For skills bundled in plugins, see [./claude-plugins-reference-2026/SKILL.md](../claude-plugins-reference-2026/SKILL.md) for plugin.json schema requirements.

---

## All Frontmatter Fields

All fields are optional. Only `description` is recommended so Claude knows when to use the skill.

| Field                      | Required    | Type    | Max Length | Description                                                                                                                                           |
| -------------------------- | ----------- | ------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | No          | string  | 64 chars   | Display name for the skill. If omitted, uses the directory name. Lowercase letters, numbers, and hyphens only.                                        |
| `description`              | Recommended | string  | 1024 chars | What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. |
| `argument-hint`            | No          | string  | —          | Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`.                                    |
| `allowed-tools`            | No          | string  | —          | Tools Claude can use without asking permission when this skill is active (comma-separated). Example: `Read, Grep, Glob, Bash(npm run:*)`              |
| `model`                    | No          | string  | —          | Model to use when this skill is active. Example: `claude-opus-4-5-20251101`, `claude-sonnet-4-20250514`, `opus`, `sonnet`, `haiku`                    |
| `context`                  | No          | string  | —          | Set to `fork` to run in a forked subagent context. See [Context Fork Behavior](#context-fork-behavior) for tool restrictions.                         |
| `agent`                    | No          | string  | —          | Which subagent type to use when `context: fork` is set. Options: `Explore`, `Plan`, `general-purpose`, or custom agent. Default: `general-purpose`    |
| `user-invocable`           | No          | boolean | —          | Set to `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`.                              |
| `disable-model-invocation` | No          | boolean | —          | Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with `/name`. Default: `false`. |
| `hooks`                    | No          | object  | —          | Hooks scoped to this skill's lifecycle. See [Hooks](/en/hooks) for configuration format. Events: `PreToolUse`, `PostToolUse`, `Stop`                  |

> [!IMPORTANT]
>
> When an `allowed-tools` field is not specified, the skill inherits the tool capabilities of the parent agent. This is a common pattern for skills that need to use tools from the parent agent. Such as when a skill is used by the orchestrator agent for knowledge or task information, no `allowed-tools` field is needed.
>
> The `allowed-tools` field is a capability scoping mechanism.
> The `allowed-tools` field is not an automatic approval mechanism.
> Making a tool available does not imply permission to use it; approval and availability are distinct concerns handled by the runtime.
>
> The `allowed-tools` field exists primarily to scope the tool surface exposed to the skill, reducing prompt and context size by including only the tool definitions the skill may need.

---

## Skill Tokenomics

Skills use progressive disclosure - only frontmatter loads initially (~100 tokens), full content loads on activation.

### Budget Constraints

| Resource                   | Limit         | Notes                               |
| -------------------------- | ------------- | ----------------------------------- |
| `name` field               | 64 chars      | Lowercase, numbers, hyphens only    |
| `description` field        | 1024 chars    | Critical for skill selection        |
| `<available_skills>` block | ~15,000 chars | Separate from global context window |
| Skills before truncation   | ~34-36        | Varies by description complexity    |

### YAML Multiline Bug

**Do NOT use YAML multiline indicators** (`>-`, `|`, `|-`) for descriptions. Claude Code's skill indexer does not parse them correctly - the description appears as ">-" instead of actual content.

```yaml
# WRONG - will show ">-" as description
description: 'This is a multiline description that breaks.  # WRONG - same problem'
description: 'This breaks too.  # CORRECT - single quoted string'
description: 'This works correctly. Use single quotes for descriptions with special characters or keep on one line.'
```

### Truncation Behavior

When total skill metadata exceeds ~15,000 characters:

1. Skills are truncated from the `<available_skills>` block
2. Truncated skills cannot be auto-invoked by Claude
3. User can still invoke truncated skills explicitly with `/skill-name`
4. Run `/context` to check for a warning about excluded skills

To increase the limit, set the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable.

**Source**: Official documentation at <https://code.claude.com/docs/en/skills.md> (section: "Troubleshooting")

### Fallback Strategy

If you have many skills, embed pointers in CLAUDE.md as a safeguard:

```markdown
## Skills Available
- For debugging: use `/scientific-thinking` skill
- For delegation: use `/delegate` skill
```

This ensures Claude can find skills even if truncated from `<available_skills>`.

---

## String Substitutions

Skills support string substitution for dynamic values in the skill content:

| Variable               | Description                                                                                                                                  |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | All arguments passed when invoking the skill. If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]`        | Access a specific argument by 0-based index, such as `$ARGUMENTS[0]` for the first argument.                                                 |
| `$N`                   | Shorthand for `$ARGUMENTS[N]`, such as `$0` for the first argument or `$1` for the second.                                                   |
| `${CLAUDE_SESSION_ID}` | The current session ID. Useful for logging, creating session-specific files, or correlating skill output with sessions.                      |

**Example with positional arguments:**

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

Running `/migrate-component SearchBar React Vue` replaces `$0` with `SearchBar`, `$1` with `React`, and `$2` with `Vue`.

---

## Dynamic Context Injection

The exclamation then backtick syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself.

**Example**: This skill summarizes a pull request by fetching live PR data with the GitHub CLI: @resources/pr-summary-example.md

**How it works**:

1. Each \`\!\`command\`\` executes immediately (before Claude sees anything)
2. The output replaces the placeholder in the skill content
3. Claude receives the fully-rendered prompt with actual PR data

**This is preprocessing**, not something Claude executes. Claude only sees the final result.

**Extended Thinking**: To enable [extended thinking mode](/en/common-workflows#use-extended-thinking-thinking-mode) in a skill, include the word "ultrathink" anywhere in your skill content.

**Source**: Official documentation at <https://code.claude.com/docs/en/skills.md> (sections: "Inject dynamic context", "Advanced patterns")

---

## Directory Structure

```
skill-name/
├── SKILL.md              # Required
├── references/           # Optional: docs loaded on demand
├── scripts/              # Optional: executed, not loaded into context
└── templates/            # Optional: reusable content
```

### Location Priority (Highest to Lowest)

1. **Managed/Enterprise** - System-level (see [managed settings](/en/iam#managed-settings))
2. **Personal** - `~/.claude/skills/`
3. **Project** - `.claude/skills/`
4. **Plugin** - Bundled with plugins (see [./claude-plugins-reference-2026/SKILL.md](../claude-plugins-reference-2026/SKILL.md))

When skills share the same name across levels, higher-priority locations win: enterprise > personal > project. Plugin skills use a `plugin-name:skill-name` namespace, so they cannot conflict with other levels.

#### Automatic Discovery from Nested Directories

When you work with files in subdirectories, Claude Code automatically discovers skills from nested `.claude/skills/` directories. For example, if you're editing a file in `packages/frontend/`, Claude Code also looks for skills in `packages/frontend/.claude/skills/`. This supports monorepo setups where packages have their own skills.

**Source**: Official documentation at <https://code.claude.com/docs/en/skills.md> (section: "Where skills live")

---

## Hooks in Skills

Skills can define hooks in frontmatter to respond to events during the skill's lifecycle. See [./claude-hooks-reference-2026/SKILL.md](../claude-hooks-reference-2026/SKILL.md) for complete hook documentation.

### Hook Events

- `PreToolUse`: Before tool executes
- `PostToolUse`: After successful execution
- `Stop`: When Skill finishes

### Hook Structure

```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"           # Regex pattern
      hooks:
        - type: command
          command: "./scripts/check.sh"
          once: true            # Run only once per session
```

### Hook I/O

- Receives JSON via stdin (session info, tool name, parameters)
- Exit 0: Success
- Exit 2: Blocking error (prevents tool, shows stderr)
- Other: Non-blocking error

For complete hook configuration including all events, matchers, JSON output control, and examples, see [./claude-hooks-reference-2026/SKILL.md](../claude-hooks-reference-2026/SKILL.md).

---

## Context Fork Behavior

Add `context: fork` to your frontmatter when you want a skill to run in isolation. The skill content becomes the prompt that drives the subagent. It won't have access to your conversation history.

**WARNING**: `context: fork` only makes sense for skills with explicit instructions. If your skill contains guidelines like "use these API conventions" without a task, the subagent receives the guidelines but no actionable prompt, and returns without meaningful output.

### Agent Types

```yaml
context: fork
agent: Explore
```

| Agent             | Model    | Tools                      | Use Case                     |
| ----------------- | -------- | -------------------------- | ---------------------------- |
| `Explore`         | Haiku    | File/web/MCP (read-only)   | Fast codebase analysis       |
| `Plan`            | Inherits | File/web/MCP (read-only)   | Research before planning     |
| `general-purpose` | Inherits | File/web/MCP + Bash/system | Complex operations (default) |
| Custom            | Custom   | Custom                     | Project-specific work        |

### Tool Restrictions in Forked Contexts

**VERIFIED BEHAVIOR** (experimentally confirmed 2026-01-22):

When `context: fork` is set, the forked subagent has access to:

- File operations: Read, Write, Edit, Grep, Glob
- Web operations: WebSearch, WebFetch
- MCP tools (if configured)
- Bash and other system tools (depending on agent type)

**The Task tool is NOT available in forked contexts.** This means forked skills cannot delegate to other subagents. If you need hierarchical delegation (subagent delegates to another subagent), the parent must run in the main context (no `context: fork`), not in a forked context.

**Source**: Experimental verification on 2026-01-22. Official documentation at <https://code.claude.com/docs/en/skills.md> does not explicitly document this restriction.

### Skills vs Subagents

Skills and subagents work together in two directions:

| Approach                     | System prompt                             | Task                        | Also loads                   |
| ---------------------------- | ----------------------------------------- | --------------------------- | ---------------------------- |
| Skill with `context: fork`   | From agent type (`Explore`, `Plan`, etc.) | SKILL.md content            | CLAUDE.md                    |
| Subagent with `skills` field | Subagent's markdown body                  | Claude's delegation message | Preloaded skills + CLAUDE.md |

With `context: fork`, you write the task in your skill and pick an agent type to execute it. For the inverse (defining a custom subagent that uses skills as reference material), see the Sub-Agents documentation.

---

## Invocation Control

### Control who invokes a skill

By default, both you and Claude can invoke any skill. You can type `/skill-name` to invoke it directly, and Claude can load it automatically when relevant to your conversation. Two frontmatter fields let you restrict this:

- **`disable-model-invocation: true`**: Only you can invoke the skill. Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy`, or `/send-slack-message`. You don't want Claude deciding to deploy because your code looks ready. This field also removes the skill description from Claude's context entirely.

- **`user-invocable: false`**: Only Claude can invoke the skill. Use this for background knowledge that isn't actionable as a command. A `legacy-system-context` skill explains how an old system works. Claude should know this when relevant, but `/legacy-system-context` isn't a meaningful action for users to take.

**How invocation control affects context loading:**

| Frontmatter                      | You can invoke | Claude can invoke | When loaded into context                                     |
| :------------------------------- | :------------- | :---------------- | :----------------------------------------------------------- |
| (default)                        | Yes            | Yes               | Description always in context, full skill loads when invoked |
| `disable-model-invocation: true` | Yes            | No                | Description not in context, full skill loads when you invoke |
| `user-invocable: false`          | No             | Yes               | Description always in context, full skill loads when invoked |

In a regular session, skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked. [Subagents with preloaded skills](/en/sub-agents#preload-skills-into-subagents) work differently: the full skill content is injected at startup.

**Source**: Official documentation at <https://code.claude.com/docs/en/skills.md> (section: "Control who invokes a skill")

### Restrict Claude's skill access

By default, Claude can invoke any skill that doesn't have `disable-model-invocation: true` set. Skills that define `allowed-tools` grant Claude access to those tools without per-use approval when the skill is active. Your [permission settings](/en/iam) still govern baseline approval behavior for all other tools. Built-in commands like `/compact` and `/init` are not available through the Skill tool.

Three ways to control which skills Claude can invoke:

**Disable all skills** by denying the Skill tool in `/permissions`:

```
# Add to deny rules:
Skill
```

**Allow or deny specific skills** using [permission rules](/en/iam):

```
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Permission syntax: `Skill(name)` for exact match, `Skill(name *)` for prefix match with any arguments.

**Hide individual skills** by adding `disable-model-invocation: true` to their frontmatter. This removes the skill from Claude's context entirely.

**Note**: The `user-invocable` field only controls menu visibility, not Skill tool access. Use `disable-model-invocation: true` to block programmatic invocation.

**Source**: Official documentation at <https://code.claude.com/docs/en/skills.md> (section: "Restrict Claude's skill access")

---

## Description Best Practices

**Good**:

```yaml
description: Extract text and tables from PDFs, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, extraction.
```

**Bad**:

```yaml
description: Helps with documents
```

**Template**:

```
[Action 1], [Action 2], [Action 3]. Use when [situation 1], [situation 2],
or when the user mentions [keywords].
```

---

## Examples

### Simple Skill

```yaml
---
name: commit-messages
description: Generate conventional commit messages from git diffs. Use when writing commits.
---

# Commit Messages

1. Run `git diff --staged`
2. Determine type (feat, fix, docs)
3. Write message under 50 chars
4. Use imperative mood
```

### Tool-Restricted

```yaml
---
name: safe-reader
description: Read files without changes. Use for code review.
allowed-tools: Read, Grep, Glob
---

# Safe Reader

ONLY read files. Never modify.
```

### Forked Context

```yaml
---
name: deep-research
description: Thorough codebase research. Use for complex investigations.
context: fork
agent: Explore
---

# Deep Research

Runs in isolated context to avoid polluting main conversation.
```

### With Hooks

```yaml
---
name: secure-ops
description: Audit-logged file operations.
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
          once: true
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "./scripts/lint.sh"
---

# Secure Operations

All modifications logged and validated.
```

### Hidden from Users

```yaml
---
name: internal-standards
description: Auto-apply code review standards.
user-invocable: false
---

Claude invokes this, users don't see it in menu.
```

### User-Only (No Auto-Invoke)

```yaml
---
name: deploy-production
description: Deploy to production.
disable-model-invocation: true
---

Only runs when user types `/deploy-production`.
```

---

## Skills vs Other Features

**Note**: Skills and slash commands are now the same system. Files in `.claude/commands/` still work but skills are recommended.

| Feature         | Invocation            | Use Case                                     |
| --------------- | --------------------- | -------------------------------------------- |
| **Skills**      | Claude decides OR `/` | Specialized knowledge/workflows, auto-invoke |
| **CLAUDE.md**   | Always loaded         | Project-wide instructions                    |
| **Subagents**   | Claude delegates      | Isolated complex operations                  |
| **MCP Servers** | Claude calls          | External tools/data                          |
| **Hooks**       | Tool events           | Automate actions                             |

---

## Installation

**Via Plugins**: Skills can be bundled in plugins. See [./claude-plugins-reference-2026/SKILL.md](../claude-plugins-reference-2026/SKILL.md) for plugin creation and distribution.

**Marketplace**:

```bash
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
```

**Manual**: Copy to `~/.claude/skills/` or `.claude/skills/`

**Hot Reload**: Changes apply immediately without restart.

---

## Recent Updates (2.1+)

- **Unified skills and commands** - `.claude/commands/` files now work as skills, skills recommended
- **Dynamic context injection** - \!\`command\` syntax for preprocessing shell command output
- **`argument-hint` field** - Show autocomplete hints for expected arguments
- **Optional name/description** - If omitted, uses directory name and first paragraph
- **`once: true` for hooks** - Run only once per session
- **`${CLAUDE_SESSION_ID}`** - Session-scoped operations
- **15,000 character budget** for skill metadata
- **`context: fork`** with agent selection
- **Hot reload** - immediate updates without restart

---

## Sources

- **Primary**: [Claude Code Skills Documentation](https://code.claude.com/docs/en/skills.md) (accessed 2026-01-28)
- **Standards**: [Agent Skills Open Standard](https://agentskills.io)
- **Examples**: [anthropics/skills](https://github.com/anthropics/skills)
- **Blog**: [Anthropic Engineering Blog - Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- **Experimental**: Context fork tool restrictions verified 2026-01-22
