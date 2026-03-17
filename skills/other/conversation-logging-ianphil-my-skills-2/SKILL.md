---
name: conversation-logging
description: Global hooks for logging Claude Code conversation events to markdown files. Tracks prompts, tool usage, and responses across all sessions. Useful for debugging, auditing, and providing conversation context to Claude.
---

# Conversation Logging Skill

Automatically log all Claude Code interactions to structured markdown files using global hooks. Enables conversation replay, debugging, and context sharing between sessions.

## What Gets Logged

- **User prompts**: Every prompt submitted to Claude
- **Tool executions with context**: Tool name plus specific details:
  - **Read/Write/Edit**: File paths and content previews
  - **Bash**: Commands and output (first 10 lines)
  - **Glob/Grep**: Search patterns
  - **TodoWrite**: Task lists with status indicators
  - **Task**: Subagent type and prompt preview
  - **WebSearch/WebFetch**: Queries and URLs
  - **AskUserQuestion**: Questions asked
- **Session metadata**: Working directory, timestamps, session IDs
- **Claude responses**: Excerpts from Claude's actual responses (last 500 chars)

Each Claude instance gets its own log file to prevent conflicts when running multiple sessions simultaneously.

## Installation

### Step 1: Copy Hook Script

The logging script is provided in this skill's `scripts/` directory. Copy it to your hooks directory:

```bash
# Create hooks directory if it doesn't exist
mkdir -p ~/.claude/hooks

# Copy the script from this skill
cp /path/to/my-skills/skills/conversation-logging/scripts/log-conversation.sh ~/.claude/hooks/

# Make it executable
chmod +x ~/.claude/hooks/log-conversation.sh
```

Or create it manually at `~/.claude/hooks/log-conversation.sh`:

```bash
#!/bin/bash
# Global hook to log Claude Code conversation events
# Handles multiple concurrent Claude instances by using unique session IDs

LOG_DIR="$HOME/.claude/conversation-logs"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DATE=$(date '+%Y-%m-%d')

mkdir -p "$LOG_DIR"

# Read JSON input from stdin
INPUT=$(cat)

# Extract key fields using jq if available
if command -v jq &> /dev/null; then
    EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // "unknown"')
    CWD=$(echo "$INPUT" | jq -r '.cwd // "unknown"')
    TOOL=$(echo "$INPUT" | jq -r '.tool_name // ""')
    PROMPT=$(echo "$INPUT" | jq -r '.prompt // ""')
    SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')
else
    EVENT="unknown"
    CWD=$(pwd)
    SESSION_ID=""
fi

# Create unique log file per session
# Format: YYYY-MM-DD-session-XXXXX.md
if [ -n "$SESSION_ID" ]; then
    # Extract first 8 chars of session ID for readability
    SHORT_SESSION="${SESSION_ID:0:8}"
    LOG_FILE="$LOG_DIR/${DATE}-session-${SHORT_SESSION}.md"
else
    # Fallback: use PID if session_id not available
    LOG_FILE="$LOG_DIR/${DATE}-pid-$$.md"
fi

# Initialize log file with header if it doesn't exist
if [ ! -f "$LOG_FILE" ]; then
    cat > "$LOG_FILE" <<EOF
# Claude Code Conversation Log
**Date:** $DATE
**Session ID:** ${SESSION_ID:-unknown}
**Started:** $TIMESTAMP

---

EOF
fi

# Log based on event type
case "$EVENT" in
    UserPromptSubmit)
        cat >> "$LOG_FILE" <<EOF

## [$TIMESTAMP] User Prompt
**Working Directory:** \`$CWD\`

\`\`\`
$PROMPT
\`\`\`

EOF
        ;;

    PostToolUse)
        if [ -n "$TOOL" ]; then
            echo "### [$TIMESTAMP] Tool: \`$TOOL\`" >> "$LOG_FILE"
            echo "" >> "$LOG_FILE"
        fi
        ;;

    Stop)
        echo "### [$TIMESTAMP] Response Complete" >> "$LOG_FILE"
        echo "" >> "$LOG_FILE"
        ;;
esac

exit 0
```

Then make it executable:
```bash
chmod +x ~/.claude/hooks/log-conversation.sh
```

### Step 2: Configure Global Hooks

Add hooks to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/log-conversation.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/log-conversation.sh"
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/log-conversation.sh"
          }
        ]
      }
    ]
  }
}
```

If you already have other settings in your `settings.json`, merge the `hooks` section carefully.

### Step 3: Verify Installation

Run any Claude Code command and check the logs:

```bash
# List all conversation logs
ls -lh ~/.claude/conversation-logs/

# View the most recent log
cat $(ls -t ~/.claude/conversation-logs/*.md | head -1)
```

**Note:** Each Claude session creates a unique log file with format `YYYY-MM-DD-session-XXXXX.md` to prevent conflicts between concurrent instances.

## Usage

### Viewing Conversation Logs

**Most recent session:**
```bash
cat $(ls -t ~/.claude/conversation-logs/*.md | head -1)
```

**All sessions from today:**
```bash
ls -1 ~/.claude/conversation-logs/$(date +%Y-%m-%d)-*.md
```

**View specific session:**
```bash
# List today's sessions to find the one you want
ls ~/.claude/conversation-logs/$(date +%Y-%m-%d)-*.md

# Then view it
cat ~/.claude/conversation-logs/2026-01-05-session-a1b2c3d4.md
```

**Recent logs (last 5 sessions):**
```bash
ls -lt ~/.claude/conversation-logs/ | head -6
```

**Search across all logs:**
```bash
grep -r "search term" ~/.claude/conversation-logs/
```

### Providing Context to Claude

When you want Claude to understand a previous conversation:

**Option 1: Reference most recent session**
```
Read my last conversation log:
@$(ls -t ~/.claude/conversation-logs/*.md | head -1)

What were we working on?
```

**Option 2: Reference specific session**
```
Read my conversation from this morning:
@~/.claude/conversation-logs/2026-01-04-session-a1b2c3d4.md

Continue where we left off.
```

**Option 3: Copy relevant sections**
```
Here's what happened in my last session:

[paste relevant log sections]

Continue from where we left off.
```

**Option 4: Search and reference**
```bash
# Find the conversation about a topic
grep -l "GitHub Issues" ~/.claude/conversation-logs/*.md
```

Then reference that file with `@` in Claude Code.

### Debugging Failed Sessions

When Claude encounters errors or you need to replay a session:

```bash
# Find failed tool executions in most recent session
grep -A 5 "Tool: Bash" $(ls -t ~/.claude/conversation-logs/*.md | head -1)

# See what prompts led to errors across all today's sessions
grep -B 10 "error" ~/.claude/conversation-logs/$(date +%Y-%m-%d)-*.md

# Find specific session with errors
grep -l "error" ~/.claude/conversation-logs/*.md
```

### Resuming Work Across Sessions

Use conversation logs to pick up where you left off:

```bash
# View most recent session
cat $(ls -t ~/.claude/conversation-logs/*.md | head -1)

# View yesterday's sessions
ls ~/.claude/conversation-logs/$(date -d yesterday +%Y-%m-%d)-*.md

# Share with Claude
claude -p "Read @$(ls -t ~/.claude/conversation-logs/*.md | head -1) and summarize what we were working on"
```

### Pruning Old Logs

Keep your logs directory clean by removing old logs:

**Interactive prune (with confirmation):**
```bash
# Delete logs older than 14 days (default)
~/.claude/hooks/prune-logs.sh

# Delete logs older than 30 days
~/.claude/hooks/prune-logs.sh 30

# Delete logs older than 7 days
~/.claude/hooks/prune-logs.sh 7
```

**Dry run (preview without deleting):**
```bash
~/.claude/hooks/prune-logs.sh 14 --dry-run
```

**What it does:**
- Shows list of logs to be deleted with dates
- Displays total size to be freed
- Asks for confirmation before deleting
- Supports dry-run mode to preview

**Setup the prune script:**
```bash
# Copy from skill
cp /path/to/my-skills/skills/conversation-logging/scripts/prune-logs.sh ~/.claude/hooks/

# Make executable
chmod +x ~/.claude/hooks/prune-logs.sh

# Create an alias (optional)
echo "alias prune-claude-logs='~/.claude/hooks/prune-logs.sh'" >> ~/.bashrc
source ~/.bashrc

# Now you can just run:
prune-claude-logs
```

**Automated cleanup with cron:**
```bash
# Add to crontab to run monthly
crontab -e

# Add this line to delete logs older than 30 days on the 1st of each month
0 0 1 * * $HOME/.claude/hooks/prune-logs.sh 30 <<< "y"
```

## Log Format

Each log file has a unique name per session: `YYYY-MM-DD-session-XXXXXXXX.md`

Log contents are organized chronologically with rich context:

```markdown
# Claude Code Conversation Log
**Date:** 2026-01-05
**Session ID:** a1b2c3d4-5678-90ab-cdef-1234567890ab
**Started:** 2026-01-05 14:23:10

---

## [2026-01-05 14:23:15] User Prompt
**Working Directory:** `/home/user/project`

```
Implement the login feature
```

### [2026-01-05 14:23:16] Tool: `Read` - `/home/user/project/src/auth.js`

### [2026-01-05 14:23:17] Tool: `Bash`
```bash
git status
```
<details><summary>Output</summary>

```
On branch main
Changes not staged for commit:
  modified:   src/auth.js
```
</details>

### [2026-01-05 14:23:18] Tool: `Write` - `/home/user/project/src/login.js`
<details><summary>Preview</summary>

```
import { authenticate } from './auth.js';

export async function login(username, password) {
  ret...
```
</details>

### [2026-01-05 14:23:20] Tool: `TodoWrite` - 3 tasks
<details><summary>Tasks</summary>

- [x] Create login function
- [>] Add error handling
- [ ] Write tests
</details>

### [2026-01-05 14:23:25] Claude Response
<details><summary>Response excerpt</summary>

I've implemented the login feature with proper authentication. The new
login.js file handles user authentication and includes error handling...
</details>

## [2026-01-05 14:25:30] User Prompt
...
```

**File naming:**
- Session-based: `2026-01-05-session-a1b2c3d4.md` (first 8 chars of session ID)
- Fallback (if no session ID): `2026-01-05-pid-12345.md` (process ID)

## Customization

### Change Log Location

Edit the script's `LOG_DIR` variable:

```bash
LOG_DIR="$HOME/my-custom-logs"
```

### Add More Details

Extend the script to log additional fields from the hook input:

```bash
# Log model info
MODEL=$(echo "$INPUT" | jq -r '.model // "unknown"')

# Log session ID
SESSION=$(echo "$INPUT" | jq -r '.session_id // "unknown"')
```

### Filter Specific Tools

Only log certain tools:

```bash
PostToolUse)
    # Only log Read, Write, Edit tools
    if [[ "$TOOL" =~ ^(Read|Write|Edit)$ ]]; then
        echo "### [$TIMESTAMP] Tool: $TOOL" >> "$DATE_FILE"
    fi
    ;;
```

### JSON Logs Instead of Markdown

Replace the logging logic to output JSON:

```bash
echo "$INPUT" | jq '.' >> "$LOG_DIR/$(date +%Y-%m-%d).jsonl"
```

## Troubleshooting

**Logs not being created?**
- Check hook script is executable: `ls -l ~/.claude/hooks/log-conversation.sh`
- Verify settings.json syntax: `cat ~/.claude/settings.json | jq .`
- Check for hook errors: Hook failures are silent by default

**Logs are empty or incomplete?**
- Install `jq` for better parsing: `sudo apt install jq` (Linux) or `brew install jq` (macOS)
- Check script permissions on log directory: `ls -ld ~/.claude/conversation-logs`

**Want to disable logging temporarily?**
- Comment out hooks in `~/.claude/settings.json`
- Or rename the hook script: `mv ~/.claude/hooks/log-conversation.sh{,.disabled}`

## Privacy & Security

**Important considerations:**

- Logs contain **all prompts** you send to Claude, including potentially sensitive info
- Logs are stored **unencrypted** in your home directory
- Logs persist **indefinitely** unless manually cleaned up

**Recommendations:**

1. **Regular cleanup**: Use the prune script to delete old logs
   ```bash
   # Interactive deletion of logs older than 14 days
   ~/.claude/hooks/prune-logs.sh

   # Or use find directly
   find ~/.claude/conversation-logs -name "*.md" -mtime +30 -delete
   ```

2. **Exclude from backups**: Add to `.gitignore` or backup exclusions
   ```bash
   echo "conversation-logs/" >> ~/.gitignore_global
   ```

3. **Encrypt sensitive logs**:
   ```bash
   gpg -c ~/.claude/conversation-logs/2026-01-05.md
   rm ~/.claude/conversation-logs/2026-01-05.md
   ```

## Advanced: Per-Project Logs

To log per-project instead of globally, use project-specific hooks in `.claude/settings.json` within each project:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'cat >> .claude/conversation.md'"
          }
        ]
      }
    ]
  }
}
```

Add `.claude/conversation.md` to your `.gitignore`.

## Quick Reference

| Task | Command |
|------|---------|
| View most recent session | `cat $(ls -t ~/.claude/conversation-logs/*.md \| head -1)` |
| List today's sessions | `ls ~/.claude/conversation-logs/$(date +%Y-%m-%d)-*.md` |
| List all logs | `ls -lh ~/.claude/conversation-logs/` |
| Search logs | `grep -r "search term" ~/.claude/conversation-logs/` |
| Prune old logs | `~/.claude/hooks/prune-logs.sh` (default: 14 days) |
| Prune with custom days | `~/.claude/hooks/prune-logs.sh 30` |
| Dry run prune | `~/.claude/hooks/prune-logs.sh 14 --dry-run` |
| Share with Claude | `@~/.claude/conversation-logs/YYYY-MM-DD-session-XXXXX.md` |
| Disable logging | Rename hook script to `.disabled` |

## See Also

- [Claude Code Hooks Documentation](https://docs.anthropic.com/claude-code/hooks) - Full hooks reference
- [MCP Logging](https://modelcontextprotocol.io) - Alternative logging via MCP servers
