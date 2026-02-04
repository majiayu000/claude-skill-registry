---
name: pi
description: Route tasks to Pi for comparison testing. Toggle Pi mode or run specific commands through Pi.
beta_required: pi
---

# Pi Integration

Run tasks through Pi (Mario Zechner's self-extending coding agent) to compare with Claude Code.

## Usage

| Command | Effect |
|---------|--------|
| `/pi` | Open Pi in a new terminal (no preset task) |
| `/pi on` | Enable Pi mode - prefer Pi for building tasks |
| `/pi off` | Disable Pi mode - back to Claude Code |
| `/pi /daily-plan` | Run a specific skill through Pi with full context |
| `/pi "build me a tool that..."` | Run a custom task through Pi |

---

## How It Works

When you run `/pi <command>`:

1. **Skill Detection:** If the command is a skill (starts with `/`), read its SKILL.md
2. **Context Gathering:** Collect user profile, pillars, today's date, vault path
3. **Terminal Launch:** Open a new Terminal.app window with Pi
4. **Context Injection:** Pi receives the full skill instructions + context

This ensures a **fair comparison** - Pi gets the same instructions Claude Code would get.

---

## Implementation

### `/pi` (No Arguments)

Open Pi in a new terminal window in the vault directory.

**macOS (default):**
```bash
osascript -e 'tell application "Terminal"
    do script "cd \"'$VAULT_PATH'\" && pi"
    activate
end tell'
```

**If in tmux:**
```bash
tmux split-window -h "cd \"$VAULT_PATH\" && pi"
```

**Output to user:**
```
✓ Pi opened in new Terminal window

  You can now interact with Pi directly.
  When done, Cmd+Tab back here.
```

---

### `/pi on`

Enable Pi mode for the session.

**Steps:**

1. Read `System/user-profile.yaml`
2. Set or update `pi_mode: true` under a `beta` section:
   ```yaml
   beta:
     pi_mode: true
   ```
3. Confirm to user:
   ```
   ✓ Pi mode enabled

   Tasks will prefer Pi. To run something in Claude Code instead,
   just say "use Claude Code for this" or run `/pi off`.
   ```

**Behavior when Pi mode is on:**

When the user asks to build something (e.g., "build me a tool that tracks relationships"):
- Suggest running it through Pi: "Pi mode is on. I'll open Pi with this task."
- Automatically invoke `/pi "build me a tool that tracks relationships"`

---

### `/pi off`

Disable Pi mode.

**Steps:**

1. Read `System/user-profile.yaml`
2. Set `pi_mode: false` under `beta` section
3. Confirm:
   ```
   ✓ Pi mode disabled

   Back to Claude Code for all tasks.
   ```

---

### `/pi <skill>` (e.g., `/pi /daily-plan`)

Run a Dex skill through Pi with full context.

**Steps:**

1. **Parse the skill name:**
   - Extract skill name from command (e.g., `daily-plan` from `/daily-plan`)
   - Handle with or without leading `/`

2. **Locate skill file:**
   - Check `.claude/skills/<skill-name>/SKILL.md`
   - Also check `.claude/skills/<skill-name>-dave/SKILL.md` (user variants)
   - If not found, report error

3. **Read skill instructions:**
   - Read full SKILL.md content
   - This is what Claude Code would use

4. **Gather context:**
   ```
   VAULT_PATH: /path/to/vault
   DATE: 2026-02-03
   DAY: Monday
   USER_NAME: [from user-profile.yaml]
   PILLARS: [from pillars.yaml]
   ```

5. **Build Pi prompt:**
   Combine skill instructions + context into a single prompt:

   ```markdown
   # Task: [Skill Name]

   You are helping a user with their personal knowledge system (Dex).
   Execute the following skill instructions.

   ## Context

   - **Vault Path:** /Users/dave/Claudesidian
   - **Date:** Monday, February 3, 2026
   - **User:** Dave Killeen
   - **Pillars:** [list from pillars.yaml]

   ## Skill Instructions

   [Full SKILL.md content here]

   ---

   Execute this skill now. You have access to the vault at the path above.
   Read files as needed to gather context.
   ```

6. **Launch Pi with prompt:**

   Write prompt to a temp file, then launch Pi:

   ```bash
   # Write prompt to temp file (handles special characters)
   PROMPT_FILE=$(mktemp)
   cat > "$PROMPT_FILE" << 'PROMPT_EOF'
   [Full prompt content]
   PROMPT_EOF

   # Launch Pi in new Terminal
   osascript -e 'tell application "Terminal"
       do script "cd \"'$VAULT_PATH'\" && pi -p \"$(cat '$PROMPT_FILE')\" && rm '$PROMPT_FILE'"
       activate
   end tell'
   ```

7. **Confirm to user:**
   ```
   ✓ Pi launched with /daily-plan

   Pi has received the full skill instructions and context.
   A new Terminal window should now be active.

   When done, compare the results:
   - Pi's output: See Terminal window
   - Claude Code: Run /daily-plan here
   ```

---

### `/pi "custom task"` (Quoted String)

Run a custom task (not a skill) through Pi.

**Steps:**

1. Extract the task description from quotes
2. Gather basic context (vault path, date, user)
3. Build prompt:
   ```markdown
   # Task

   [User's task description]

   ## Context

   - **Vault Path:** /Users/dave/Claudesidian
   - **Date:** Monday, February 3, 2026

   Execute this task. You have access to the vault.
   ```

4. Launch Pi with prompt (same as above)

---

## Error Handling

### Pi Not Installed

If `pi` command not found:

```
❌ Pi is not installed

Install it with:
  npm install -g @mariozechner/pi-coding-agent

Then try again.
```

### Skill Not Found

If skill doesn't exist:

```
❌ Skill not found: /unknown-skill

Available skills:
  /daily-plan, /daily-review, /week-plan, ...

Or run a custom task:
  /pi "build me a tool that..."
```

### Beta Not Activated

If Pi beta not activated:

```
❌ Pi integration requires beta activation

Run: /beta-activate PILAUNCH2026
```

---

## Environment Detection

Detect the user's environment to choose the best terminal launch method:

```bash
# Check if in tmux
if [ -n "$TMUX" ]; then
    # Use tmux split
    tmux split-window -h "cd \"$VAULT_PATH\" && pi"
else
    # Check OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS - use Terminal.app or iTerm2
        if [ -d "/Applications/iTerm.app" ]; then
            osascript -e 'tell application "iTerm"
                create window with default profile
                tell current session of current window
                    write text "cd \"'$VAULT_PATH'\" && pi"
                end tell
            end tell'
        else
            osascript -e 'tell application "Terminal"
                do script "cd \"'$VAULT_PATH'\" && pi"
                activate
            end tell'
        fi
    else
        # Linux - try common terminals
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd \"$VAULT_PATH\" && pi; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd \"$VAULT_PATH\" && pi" &
        else
            echo "Please open a terminal and run: cd \"$VAULT_PATH\" && pi"
        fi
    fi
fi
```

---

## Comparison Workflow

After running a task through Pi:

1. **Review Pi's output** in the Terminal window
2. **Run the same task** in Claude Code (e.g., `/daily-plan`)
3. **Compare:**
   - Quality of output
   - Time taken (subjective)
   - Ease of iteration
   - Integration with Dex

4. **Capture learnings** (optional):
   ```
   /pi capture
   ```
   Logs the comparison to `System/Pi_Comparisons/YYYY-MM-DD.md`

---

## Notes

- Pi runs as a **separate process** in its own terminal
- Pi has access to your vault files but **not** Dex MCP servers
- For MCP access, Pi uses the MCP bridge (if configured in `.pi/`)
- Results may differ because Pi's approach is more minimal

---

## Related

- `/pi-tools` - View synced Pi extensions
- `/beta-status` - Check Pi beta activation
- `System/Beta/pi/README.md` - Pi setup documentation
