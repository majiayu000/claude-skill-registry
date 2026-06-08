---
name: docs-anthropic
description: Index of official Claude Code / Anthropic docs — fetches the right page on demand
disable-model-invocation: true
user-invocable: true
allowed-tools: WebFetch(domain:code.claude.com)
argument-hint: "[topic] e.g. hooks · skills · channels · commands (blank = list all)"
---

# Anthropic / Claude Code documentation index

The curated set of official Claude Code docs to reach for, with what each one covers. All live
under `https://code.claude.com/docs/en/`.

| Topic | URL | What it covers |
| :-- | :-- | :-- |
| **skills** | https://code.claude.com/docs/en/skills | Authoring Agent Skills: `SKILL.md` format and frontmatter, progressive disclosure (description always in context, body on invoke), `disable-model-invocation` / `user-invocable`, supporting files, `context: fork`, packaging. |
| **hooks** | https://code.claude.com/docs/en/hooks | Lifecycle hooks — `PreToolUse`, `PostToolUse`, `UserPromptSubmit`, `PreCompact`, `SessionStart`, `Stop`, `SubagentStop`, `Notification` — their JSON stdin/stdout contract, exit codes, and `settings.json` wiring. **(`PreCompact` = the compact-hook event.)** |
| **tools-reference** | https://code.claude.com/docs/en/tools-reference | Reference for the built-in tools (Bash, Read, Edit, Write, Glob, Grep, WebFetch, …) and how permissions gate them. |
| **plugins-reference** | https://code.claude.com/docs/en/plugins-reference | Plugin structure: `plugin.json`, bundling commands / agents / skills / hooks / MCP servers, marketplace layout, skills-dir plugins. |
| **channels-reference** | https://code.claude.com/docs/en/channels-reference | Building an MCP **channel** server that pushes webhooks, alerts, and chat into a session: capability declaration, notification events, reply tools, sender gating, permission relay. (Research preview.) |
| **commands** | https://code.claude.com/docs/en/commands | Slash commands — built-ins plus custom commands in `.claude/commands/` (now merged into skills), frontmatter, `$ARGUMENTS`/`$N`, and `:`-namespacing (plugin-only). |
| **interactive-mode** | https://code.claude.com/docs/en/interactive-mode | The interactive REPL: keyboard shortcuts, vim mode, multiline input, and session controls. |

**Master index:** `https://code.claude.com/docs/en/llms.txt` — the full list of every docs page, for
discovering anything not in the table above.

## How to use this skill

Argument passed: **$ARGUMENTS**

- **If a topic was given** (a keyword above, or something one of these docs would answer — e.g.
  `hooks`, `precompact`, `skill frontmatter`, `channels`, `slash command args`): pick the single
  best-matching URL, `WebFetch` it, and answer the question from the live page. Cite the URL. If
  nothing matches the seven, fetch the master `llms.txt` index, find the closest page, then fetch it.
- **If the argument is blank:** present the table above as the index — no fetching. Offer to pull
  any specific page on request.

Keep the verdict-open, no-overclaim floor: report what the docs actually say, and if a page has
moved or 404s, say so plainly rather than reconstructing it from memory.
