---
name: writing-skills
description: Use when creating, improving, or reviewing Claude Code skills. Covers frontmatter, tool use patterns, file structure, hooks, and CC platform limitations. Also invoke superpowers:writing-skills for CSO and testing workflow.
---

# Writing Skills

## Facts

* The frontmatter `name` is what appears in autocomplete list when typing `/` in session. So `name: foo` would allow user to submit `/foo` to trigger that skill.
* The skill directory name appears printed in session when skill is activated by the agent. E.g. dir `/foobar` would yield e.g.
  ```
  ⏺ Skill(foobar)
  ⎿  Initializing…
  ```
* `Skill(foobar)` is also the syntax for granting permission to the skill in config
* Development Related
  * Skills created or modified in ~/.claude/skills or .claude/skills are immediately available without restarting the session (added in v2.1.0)

## Overview

This skill covers __Claude Code platform specifics__. For skill design methodology (CSO, TDD, testing), also invoke `superpowers:writing-skills`.

## Key Rules (from [Anthropic guide](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices))

__Frontmatter:__

* `name`: Max 64 chars, lowercase letters/numbers/hyphens only, no reserved words ("anthropic", "claude")
* `description`: Max 1024 chars, non-empty, third person, critical for discovery
  * Good: "Processes Excel files and generates reports"
  * Avoid: "I can help you process Excel files"
* Use gerund form (verb + -ing) for names: `processing-pdfs`, `analyzing-spreadsheets`

__Body:__

* Keep SKILL.md under 500 lines
* "Claude is already very smart. Only add context Claude doesn't already have."

## File Structure

```
my-skill/
├── SKILL.md          # Main (<500 lines)
├── reference/        # Detailed docs (loaded on demand)
├── scripts/          # Executable (zero-token)
└── assets/           # Static files (banners, templates)
```

## Tools for Skills

| Tool            | Purpose                              | Reference                                                                        |
| --------------- | ------------------------------------ | -------------------------------------------------------------------------------- |
| AskUserQuestion | Interactive prompts (max 4 options)  | [tool-ask-user-question.md](reference/tool-ask-user-question.md)                 |
| TodoWrite       | Task checkboxes                      | [tool-todo-write.md](reference/tool-todo-write.md)                               |
| Bash            | Execute bundled scripts (zero-token) | [pattern-script-bundling.md](reference/pattern-script-bundling.md)               |
| Read            | Load reference files on demand       | [pattern-progressive-disclosure.md](reference/pattern-progressive-disclosure.md) |

## Frontmatter Options

| Field                      | Purpose                     | Reference                                                    |
| -------------------------- | --------------------------- | ------------------------------------------------------------ |
| `name`, `description`      | Identity and discovery      | [config-frontmatter.md](reference/config-frontmatter.md)     |
| `allowed-tools`            | Skip permission prompts     | [config-allowed-tools.md](reference/config-allowed-tools.md) |
| `context: fork`            | Run in isolated subagent    | [config-context-fork.md](reference/config-context-fork.md)   |
| `hooks`                    | PreToolUse/PostToolUse/Stop | [config-hooks.md](reference/config-hooks.md)                 |
| `user-invocable`           | Show in slash menu          | [config-frontmatter.md](reference/config-frontmatter.md)     |
| `disable-model-invocation` | User-triggered only         | [config-frontmatter.md](reference/config-frontmatter.md)     |

## Platform Limitations

__Cannot control:__

* Collapsed/expanded state of tool output - see [limitation-output-collapse.md](reference/limitation-output-collapse.md)
* Terminal theme/colors
* Streaming behavior
* Custom UI widgets
* Status line refresh from skills - see [feature-status-line.md](reference/feature-status-line.md)

## Patterns

| Pattern                | Reference                                                                        |
| ---------------------- | -------------------------------------------------------------------------------- |
| Code examples          | [pattern-code-examples.md](reference/pattern-code-examples.md)                   |
| Progressive disclosure | [pattern-progressive-disclosure.md](reference/pattern-progressive-disclosure.md) |
| Script bundling        | [pattern-script-bundling.md](reference/pattern-script-bundling.md)               |

## When Reviewing Skills

Apply criteria from both this skill (CC platform) and `superpowers:writing-skills` (methodology).

__Platform checklist:__

* [ ] Frontmatter valid? (name format, description length, third person)
* [ ] SKILL.md under 500 lines?
* [ ] Reference files used for detailed content?
* [ ] Code examples have language tags?
* [ ] Known limitations acknowledged? (output collapse, status line)
* [ ] Hooks correctly structured if used?
* [ ] `allowed-tools` syntax correct if used?

__Methodology checklist__ (from `superpowers:writing-skills`):

* [ ] CSO applied? (Claude-Specific Optimization)
* [ ] Token-efficient structure?
* [ ] Clear trigger conditions in description?
