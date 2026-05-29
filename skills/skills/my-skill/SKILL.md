---
name: my-skill
description: What this skill does and when to use it. Claude reads this to decide relevance. Include keywords users would naturally say.
---

These two fields are the only ones required. `name` must be lowercase with hyphens, max 64 characters, and match the parent directory name. `description` is what Claude reads at startup to decide when the skill is relevant (max 1024 characters).

## Optional Frontmatter Fields

Add any of these to the `---` block above to customise behaviour:

| Field | Example | Purpose |
|---|---|---|
| `argument-hint` | `[issue-number]` | Hint shown during autocomplete to indicate expected arguments |
| `disable-model-invocation` | `true` | Prevent Claude from auto-loading. User must type `/name` explicitly. Use for deploys, sends, destructive ops |
| `user-invocable` | `false` | Hide from the `/` menu. Claude can still load it automatically. Use for background knowledge |
| `allowed-tools` | `Read, Grep, Bash(npm *)` | Tools Claude can use without asking permission. Space-delimited, supports patterns |
| `model` | `claude-sonnet-4-6` | Override the model when this skill is active. Useful for cost control |
| `context` | `fork` | Run in an [isolated subagent](^A separate Claude instance with its own context. The skill content becomes the subagent's system prompt). Skill content becomes the subagent's prompt |
| `agent` | `Explore` | Which subagent runs when `context: fork`. Built-in: `Explore`, `Plan`, `general-purpose`, or custom from `.claude/agents/` |
| `license` | `Apache-2.0` | License name or reference to a bundled LICENSE file |
| `compatibility` | `Requires git, docker` | Environment requirements (max 500 chars) |
| `metadata` | key-value pairs | Arbitrary metadata (author, version, etc.) |

---

# Body Content

Everything below the frontmatter is the instruction body. Claude reads this when the skill is activated. Write whatever helps Claude perform the task. There are no format restrictions.

Good body content includes:

- Step-by-step instructions for the task
- Examples of inputs and expected outputs
- Common edge cases and how to handle them
- References to supporting files in this skill folder

## String Substitutions

[Placeholders](^Variables in your SKILL.md that get replaced with real values before Claude sees the content) are replaced with real values before Claude sees the content:

| Placeholder | Resolves To |
|---|---|
| `$ARGUMENTS` | Everything the user typed after the skill name |
| `$ARGUMENTS[N]` or `$N` | A specific argument by index (0-based) |
| `${CLAUDE_SESSION_ID}` | The current session ID |
| `${CLAUDE_SKILL_DIR}` | Path to this skill's directory |

Example: `/my-skill SearchBar React Vue` gives `$0` = "SearchBar", `$1` = "React", `$2` = "Vue".

If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`.

## Dynamic Context Injection

The `!` backtick syntax runs shell commands before the content reaches Claude. Output replaces the placeholder:

- PR diff: `` !`gh pr diff` ``
- Dependencies: `` !`cat package.json | jq .dependencies` ``
- Changed files: `` !`git diff --name-only` ``

This is [preprocessing](^The commands run at skill load time, not during conversation. Claude only sees the final output, not the commands themselves). Claude only sees the final output, not the commands.

---

# Supporting Files

Keep SKILL.md under 500 lines. Move detailed material to separate files and reference them from the body:

- [references/REFERENCE.md](references/REFERENCE.md): Detailed documentation loaded on demand
- [assets/template.md](assets/template.md): Templates and static resources
- [scripts/helper.sh](scripts/helper.sh): Executable code Claude can run

Use relative paths from SKILL.md. Keep references one level deep. Navigate into these folders to learn more about each.