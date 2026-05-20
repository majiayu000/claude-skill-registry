---
name: name
description: Name or rename the current session — saves to statusline and session notes
argument-hint: <session name>
allowed-tools: Bash(mkdir:*), Bash(ls:*), Bash(echo:*), Bash(cat:*), Bash(tee:*)
---

## Your task

Name the current session so it appears in the statusline and is saved for future reference.

The argument provided is: `{{ args }}`

### Steps

1. **Get the session name** — use the argument if provided, otherwise ask the user with AskUserQuestion: "What name do you want to give this session?"

2. **Find the current session ID** — run:
   ```bash
   ls -t ~/.claude/projects/*/*.jsonl 2>/dev/null | head -1 | xargs basename | sed 's/\.jsonl$//'
   ```

3. **Save the session name**:
   ```bash
   mkdir -p ~/.claude/session_notes
   echo "<name>" | tee ~/.claude/session_notes/<session_id>
   ```

4. **Confirm** — tell the user the session is named and will appear in the statusline (📌 <name>) after the next response.

### Note

This is separate from Claude Code's built-in `/rename` command which renames the session in the UI sidebar.
Use `/name` to tag the session so the statusline always reminds you what you're working on.
You can use both: `/rename` for the sidebar, `/name` for the statusline.
