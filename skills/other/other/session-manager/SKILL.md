---
name: session-manager
description: Manage current Claude Code session metadata — set project, task_tag, tags, and summary on session.md via Obsidian CLI. Use this skill whenever the user wants to tag, categorize, name, label, summarize, or organize the current session. Triggers on phrases like "tag this session", "this was about X", "mark this as", "set task to", "session summary", "what task is this session", "call this session", "categorize this as", "set project to", or any mention of session metadata, task grouping, or session organization. Even if the user just casually mentions what the session was about ("we were working on the auth refactor"), use this skill to offer to set the task_tag.
---

# Session Manager

Manage metadata for the current active session's `session.md` file via Obsidian CLI.

## Deriving the Session Path

The session docs path is injected into your system prompt by the SessionStart hook. It looks like:

```
Session docs path: {KB_PATH}/_sessions/2026-03-04/abc123-def456/docs/
```

To get the `session.md` vault-relative path for Obsidian CLI:

1. Take the injected docs path
2. Find `_sessions/` in it — everything from `_sessions/` onward is vault-relative
3. Remove the trailing `docs/` and append `session.md`

**Example:**
- Injected: `.../knowledge-bank/_sessions/2026-03-04/abc123-def456/docs/`
- Vault-relative session.md: `_sessions/2026-03-04/abc123-def456/session.md`

If the session docs path is not in your system prompt, ask the user for the session folder path.

## Properties You Can Update

| Property | Type | Purpose |
|----------|------|---------|
| `project` | text | Project name (auto-set from cwd at session start, customizable) |
| `task_tag` | text | Groups sessions working on the same task (queried by Dataview) |
| `tags` | list | Freeform categorization (e.g., brainstorming, debugging, architecture) |
| `summary` | text | One-line description of what the session accomplished |

Do NOT modify other frontmatter properties (session_id, date, cwd, etc.) — those are managed by hooks.

## Commands

**Set a property:**
```bash
obsidian vault="knowledge-bank" property:set name="<property>" value="<value>" [type="list"] path="<vault-relative-path>"
```

**Read current metadata:**
```bash
obsidian vault="knowledge-bank" read path="<vault-relative-path>"
```

## Examples

User: "set project to sundayhao-plugins"
```bash
obsidian vault="knowledge-bank" property:set name="project" value="sundayhao-plugins" path="_sessions/2026-03-04/abc123/session.md"
```

User: "tag this session as refactor-bidrequest"
```bash
obsidian vault="knowledge-bank" property:set name="task_tag" value="refactor-bidrequest" path="_sessions/2026-03-04/abc123/session.md"
```

User: "add tags brainstorming and architecture"
```bash
obsidian vault="knowledge-bank" property:set name="tags" value="brainstorming, architecture" type="list" path="_sessions/2026-03-04/abc123/session.md"
```

User: "summarize: designed centralized session management"
```bash
obsidian vault="knowledge-bank" property:set name="summary" value="Designed centralized session management for second-brain plugin" path="_sessions/2026-03-04/abc123/session.md"
```

User: "what's this session tagged as?"
```bash
obsidian vault="knowledge-bank" read path="_sessions/2026-03-04/abc123/session.md"
```
Then extract and report the `task_tag`, `tags`, and `summary` from the frontmatter.

## On Invocation

Every time this skill is invoked, **always start by reading the current session.md** and displaying a status summary before taking any action:

1. Read the session note using the "Read current metadata" command
2. Display current values in this format:
   ```
   **Current Session**
   - project: <value or empty>
   - task_tag: <value or empty>
   - tags: <value or empty>
   - summary: <value or empty>
   ```
3. Then proceed with the user's request (set properties, or ask what they'd like to update)

If the user invoked the skill without a specific request, show the status and list what can be set.

## Constraints

- ONLY operates on the **current active session** — do NOT modify other sessions
- ONLY updates `project`, `task_tag`, `tags`, and `summary`
- Always confirm the update to the user after running the command
