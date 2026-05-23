---
name: session-manager
description: Manage current Claude Code session metadata — set project, tags, and summary on session.md via Obsidian CLI. Use this skill whenever the user wants to tag, categorize, name, label, summarize, or organize the current session. Triggers on phrases like "tag this session", "this was about X", "mark this as", "session summary", "call this session", "categorize this as", "set project to", or any mention of session metadata or session organization. Even if the user just casually mentions what the session was about ("we were working on the auth refactor"), use this skill to offer to set tags.
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
| `session_name` | text | Session name (auto-synced from `/rename` customTitle on invocation) |
| `project` | text | Project name (auto-set from cwd at session start, customizable) |
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

## Tag Suggestion Workflow

When the user wants to set tags, **do NOT set them directly**. Instead, suggest existing tags to promote consistency.

### Step 1: Load existing tags

Read from ccfind's cache (field 5, comma-separated):
```bash
CACHE="${XDG_CACHE_HOME:-$HOME/.cache}/ccfind/sessions.tsv"
cut -f5 "$CACHE" 2>/dev/null | tr ',' '\n' | sed 's/^ *//;s/ *$//' | grep -v '^-$' | grep -v '^$' | sort -u
```

If the cache doesn't exist, fall back to listing tags from the current session's tags property.

### Step 2: Match user-provided tags against existing ones

For each tag the user provides, check for:
- **Exact match** — existing tag matches exactly → use it
- **Similar match** — differs only by hyphenation (`rule-forge` vs `ruleforge`), casing (`A2X` vs `a2x`), or minor spelling → suggest the existing one
- **No match** — genuinely new tag → mark as new

### Step 3: Present suggestion table

```
| Your Tag       | Suggestion          | Reason              |
|----------------|---------------------|---------------------|
| rule-forge     | → ruleforge (6×)    | existing, no hyphen |
| debugging      | ✓ debugging (6×)    | exact match         |
| new-feature    | new                 | no similar existing |
```

The `(N×)` shows how many sessions already use that tag — higher = more reason to reuse.

### Step 4: Confirm before setting

Use the **AskUserQuestion** tool to confirm. Only set tags after the user approves:
```
AskUserQuestion({ question: "Suggested tags: [table]. Confirm or adjust?" })
```

## Examples

User: "set project to sundayhao-plugins"
```bash
obsidian vault="knowledge-bank" property:set name="project" value="sundayhao-plugins" path="_sessions/2026-03-04/abc123/session.md"
```

User: "add tags brainstorming and architecture"

**Do NOT run the command directly.** Instead:
1. Load existing tags (Step 1)
2. Both `brainstorming` and `architecture` exist — show confirmation table
3. After user confirms, then set:
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
Then extract and report the `tags` and `summary` from the frontmatter.

## On Invocation

Every time this skill is invoked, **always** perform steps 1-4 before handling the user's request. These steps run on **every invocation regardless** of what the user asked (tags, summary, or anything else):

1. Read the session note using the "Read current metadata" command
2. Check if the session has been renamed via `/rename` by reading the customTitle from the transcript:
   ```bash
   source skills/common/obsidian_helpers.sh
   read_custom_title "<cwd>" "<session_id>"
   ```
   Where `<cwd>` is from session.md's `cwd` property and `<session_id>` is from `session_id` property.
3. If customTitle exists but `session_name` in session.md is empty or different, **automatically set it**:
   ```bash
   obsidian vault="knowledge-bank" property:set name="session_name" value="<customTitle>" path="<vault-relative-path>"
   ```
4. **Always rename the tmux window** to the current session_name (whether from customTitle or already in session.md). This MUST run on every invocation:
   ```bash
   tmux set-window-option -t "$TMUX_PANE" automatic-rename off 2>/dev/null
   tmux rename-window -t "$TMUX_PANE" "<session_name>" 2>/dev/null
   ```
   Run these as actual Bash tool calls. `$TMUX_PANE` is available in Claude's shell environment when launched from tmux. Skip only if session_name is empty.
5. Display current values in this format:
   ```
   **Current Session**
   - session_name: <value or empty>
   - project: <value or empty>
   - tags: <value or empty>
   - summary: <value or empty>
   ```
6. Then proceed with the user's request. If the request is ambiguous or the skill was invoked without a specific request, use the **AskUserQuestion** tool:
   ```
   AskUserQuestion({ question: "What would you like to update?\n- tags\n- summary\n- project" })
   ```

## Constraints

- ONLY operates on the **current active session** — do NOT modify other sessions
- ONLY updates `session_name`, `project`, `tags`, and `summary`
- **Use AskUserQuestion tool** for all confirmations and prompts (not plain text questions). This ensures the user gets a proper input prompt.
- Always confirm the update to the user after running the command
