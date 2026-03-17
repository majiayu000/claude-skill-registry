---
name: personality
description: Manage voice assistant personalities. List, create, switch, edit, delete, export, or import personalities.
disable-model-invocation: true
argument-hint: "[list|switch <name>|create|edit [name]|delete <name>|export [name]|import]"
---

# Personality Management

Manage multiple voice assistant personalities for claude-talk.

## Storage

- `~/.claude-talk/personalities/<name>.md` — saved personalities
- `~/.claude-talk/personality.md` — active personality (backward compat)
- `~/.claude-talk/active-personality` — name of active personality
- Personality names are lowercase with hyphens (e.g., `witty-jarvis`)

## Route by $ARGUMENTS

Parse the first word of `$ARGUMENTS` as the subcommand. The rest are arguments to that subcommand.

---

### No arguments (or "list"): List Personalities

1. Check if `~/.claude-talk/personalities/` exists. If not, run the **Migration** step below first.
2. List all `.md` files in `~/.claude-talk/personalities/`.
3. Read `~/.claude-talk/active-personality` to get the active name.
4. Display a table:

| Personality | Style | Voice | Active |
|---|---|---|---|
| default | Witty & playful | Daniel | |
| pirate-claude | Casual & warm | Moira | ✓ |

Read the `## Conversational Style` and `## Voice` sections from each file to populate Style and Voice columns.

If no personalities exist, say: "No personalities found. Run `/claude-talk:personality create` to make one, or `/claude-talk:install` to set up from scratch."

---

### "switch \<name>": Switch Active Personality

1. Check that `~/.claude-talk/personalities/<name>.md` exists. If not, list available personalities and abort.
2. Read the personality file.
3. Extract the voice from the `## Voice` section (the line `- Voice: <voice>`).
4. Copy the personality file to `~/.claude-talk/personality.md`.
5. Write the name to `~/.claude-talk/active-personality`.
6. Update the `VOICE=` line in `~/.claude-talk/config.env` with the extracted voice. Quote voices with spaces (e.g., `VOICE="Daniel (Enhanced)"`).
7. Confirm: "Switched to **<name>**. Voice set to <voice>."
8. If a voice session is active (check `~/.claude-talk/state` for `SESSION=active`), update the voice on the running audio server and speak:
   ```bash
   source ~/.claude-talk/venvs/wlk/bin/activate
   claude-talk server set-voice "<voice>"
   claude-talk server speak "Switching to <name>. How do I sound?"
   ```

---

### "create": Create New Personality

Walk the user through creating a personality using AskUserQuestion. Reuse the same interactive flow as the install skill (Questions 1-6).

#### Step 1: Voice

Check which Enhanced/Premium voices are installed (use Bash):
```bash
claude-talk voices --enhanced
```

Play voice previews and use AskUserQuestion with header "Voice" to let the user pick. Follow the same voice selection logic as install SKILL.md Question 1 (recommend Enhanced voices, play samples, etc.).

#### Step 2: Name

Play name options in the chosen voice and use AskUserQuestion with header "Name". Same options as install: Claude, Jarvis, Friday, Nova, or custom.

#### Step 3: Personality Style

Play style samples in the chosen voice and use AskUserQuestion with header "Style". Same options as install: Casual & warm, Professional & concise, Witty & playful, Calm & thoughtful.

#### Step 4: What should I call you?

Use AskUserQuestion with header "Your name". Same options as install: First name, Boss, Nothing specific.

#### Step 5: Response Length

Use AskUserQuestion with header "Verbosity". Same options as install: Short & punchy, Balanced, Thorough.

#### Step 6: Custom Instructions

Ask in plain text: "Any special instructions? For example: 'always start with a fun fact', 'be a bit sarcastic', 'speak like a ship captain', or just leave blank."

#### Step 7: Save

Generate a personality filename from the chosen name (lowercase, spaces to hyphens, e.g., "Pirate Claude" → `pirate-claude`).

If a personality with that name already exists, ask the user if they want to overwrite or pick a different name.

Write the personality file to `~/.claude-talk/personalities/<name>.md` using the same format as install Part 5, but with an added `## Voice` section after `## Identity`:

```markdown
## Voice
- Voice: <chosen voice>
```

Then ask: "Activate this personality now?"

If yes, run the same steps as the **switch** subcommand.

If no, confirm: "Saved **<name>**. Switch to it anytime with `/claude-talk:personality switch <name>`."

---

### "edit [name]": Edit a Personality

1. If no name given, use the active personality (from `~/.claude-talk/active-personality`).
2. Read `~/.claude-talk/personalities/<name>.md`.
3. Display current values: Name, Voice, Style, Verbosity, User address, Custom instructions.
4. Use AskUserQuestion with header "Edit" and options:
   - **Name** - "Change the assistant's name"
   - **Voice** - "Change the TTS voice"
   - **Style** - "Change personality style"
   - **Verbosity** - "Change response length"

   Allow multiSelect so the user can change multiple fields at once.

5. For each selected field, use the same AskUserQuestion flows as the create subcommand.
6. Write the updated personality file.
7. If this is the active personality, also update `~/.claude-talk/personality.md` and `~/.claude-talk/config.env` (VOICE).
8. Confirm changes.

---

### "delete \<name>": Delete a Personality

1. Read `~/.claude-talk/active-personality`.
2. If `<name>` is the active personality, refuse: "Can't delete the active personality. Switch to a different one first with `/claude-talk:personality switch <other>`."
3. If `<name>` is "default", warn: "Are you sure you want to delete the default personality?" and confirm.
4. Check that `~/.claude-talk/personalities/<name>.md` exists. If not, list available and abort.
5. Delete `~/.claude-talk/personalities/<name>.md`.
6. Confirm: "Deleted **<name>**."

---

### "export [name]": Export a Personality

1. If no name given, use the active personality.
2. Read `~/.claude-talk/personalities/<name>.md`.
3. Print the full contents of the file.

---

### "import": Import a Personality

Ask the user: "Paste the personality markdown below, or provide a file path:"

Wait for the user's response.

- If it looks like a file path (starts with `/` or `~` or `./`), read the file.
- Otherwise, treat the response as raw markdown content.

Extract the name from the `## Identity` section (`- Name: <name>`).
Generate a filename (lowercase, hyphens).

If a personality with that name already exists, ask if they want to overwrite.

Write to `~/.claude-talk/personalities/<name>.md`.

Ask if they want to activate it.

---

## Migration

If `~/.claude-talk/personality.md` exists but `~/.claude-talk/personalities/` does not:

1. Create `~/.claude-talk/personalities/`.
2. Read `~/.claude-talk/personality.md`.
3. Extract the name from `## Identity` → `- Name: <name>`.
4. Generate a filename from the name.
5. Check if the personality file has a `## Voice` section. If not, read VOICE from `~/.claude-talk/config.env` and add a `## Voice` section after `## Identity`:
   ```markdown
   ## Voice
   - Voice: <voice from config>
   ```
6. Write to `~/.claude-talk/personalities/<name>.md`.
7. Write the name to `~/.claude-talk/active-personality`.
Find the plugin directory the same way as the install skill: check current working directory for the file, or read `CLAUDE_TALK_DIR` from config.env.

---

## If no personality directory and no personality.md

Tell the user: "No personality configured yet. Run `/claude-talk:install` to set one up, or `/claude-talk:personality create` to create one."
