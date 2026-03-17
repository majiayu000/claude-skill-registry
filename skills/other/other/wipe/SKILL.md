---
context: fork
---

# /wipe

Generate a context handoff summary, clear the session, and resume in a fresh conversation. Detects environment and provides automated (tmux) or manual workflow.

## Usage

```
/wipe
/wipe quick           # Minimal handoff, just essentials
/wipe detailed        # Comprehensive handoff with full context
```

## Instructions

When the user invokes `/wipe`:

### Phase 1: Detect Environment

First, check the terminal environment:

```bash
echo "Environment Detection:"
echo "TMUX: ${TMUX:-not set}"
echo "TERM_PROGRAM: ${TERM_PROGRAM:-not set}"
echo "TERM: $TERM"

if [ -n "$TMUX" ]; then
    echo "MODE: tmux (automated wipe available)"
    tmux display-message -p 'Session: #{session_name}:#{window_index}.#{pane_index}'
else
    echo "MODE: manual (clipboard workflow)"
fi
```

### Phase 2: Generate Handoff Summary

Create a structured summary of the current session. Use this format:

```markdown
## What we're working on

- [Primary task or topic from this session]

## Current state

- [Where we left off - be specific]
- [Any pending questions or decisions]

## Key decisions made

- [Important choices, conclusions, or agreements]
- [Technical decisions with rationale]

## Recent changes

- [Files modified with brief description]
- [Commands run or actions taken]

## Important context

- [Technical constraints or requirements]
- [User preferences discovered]
- [Project-specific facts needed to continue]

## Next steps

- [Immediate next action to take]
- [Any blocked items or dependencies]
```

**Guidelines for generating the handoff:**

- Be concise but complete - this will be the only context in the new session
- Include file paths for any files that were being edited
- Mention any errors encountered and their status (fixed/pending)
- Note any user preferences expressed during the session
- Skip sections that don't apply (empty sections waste tokens)

### Phase 3: Execute Wipe

Based on the detected environment:

#### If tmux is detected (automated):

Present the handoff summary to the user, then provide this script:

```bash
# Save handoff to temp file
HANDOFF_FILE="/tmp/claude-handoff-$$.txt"
cat > "$HANDOFF_FILE" << 'HANDOFF_EOF'
Here's the context from my previous session:

[PASTE THE GENERATED HANDOFF HERE]

---
Please acknowledge you've received this context, then continue from where we left off.
HANDOFF_EOF

# Copy to clipboard as backup
if command -v pbcopy &> /dev/null; then
    cat "$HANDOFF_FILE" | pbcopy
    echo "Backup copied to clipboard (macOS)"
elif command -v clip.exe &> /dev/null; then
    cat "$HANDOFF_FILE" | clip.exe
    echo "Backup copied to clipboard (WSL)"
elif command -v xclip &> /dev/null; then
    cat "$HANDOFF_FILE" | xclip -selection clipboard -i &>/dev/null &
    sleep 0.2
    echo "Backup copied to clipboard (xclip)"
elif command -v wl-copy &> /dev/null; then
    cat "$HANDOFF_FILE" | wl-copy
    echo "Backup copied to clipboard (Wayland)"
fi

# Get tmux session info
TMUX_SOCKET=$(echo "$TMUX" | cut -d',' -f1)
TARGET_PANE=$(tmux display-message -p '#{session_name}:#{window_index}.#{pane_index}')

echo "Target pane: $TARGET_PANE"

# Schedule automated wipe sequence
(
    sleep 2
    # Clear terminal scrollback to prevent lag
    tmux -S "$TMUX_SOCKET" clear-history -t "$TARGET_PANE"
    tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" C-l
    sleep 1
    # Send /clear command
    tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" Escape
    sleep 0.3
    tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" '/clear'
    sleep 0.5
    tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" Enter
    # Wait for /clear to process
    sleep 8
    # Load and paste handoff
    tmux -S "$TMUX_SOCKET" load-buffer "$HANDOFF_FILE"
    tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" ""
    sleep 0.3
    tmux -S "$TMUX_SOCKET" paste-buffer -t "$TARGET_PANE"
    sleep 0.3
    tmux -S "$TMUX_SOCKET" send-keys -t "$TARGET_PANE" C-m
    sleep 1
    rm -f "$HANDOFF_FILE"
) &
disown

echo ""
echo "========================================"
echo "WIPE SCHEDULED"
echo "========================================"
echo "  - Scrollback clears in 2 seconds"
echo "  - /clear runs after 1 second"
echo "  - Handoff arrives after 8 seconds"
echo "  - Total time: ~12 seconds"
echo ""
echo "  Backup saved to clipboard"
echo "========================================"
```

#### If NOT in tmux (manual workflow):

Present the handoff summary, then provide manual instructions:

```markdown
## Manual Wipe Instructions

Your terminal (**[TERMINAL_NAME]**) doesn't support automated wipe.

### Step 1: Copy the Handoff

Copy the handoff summary above to your clipboard. You can:

- Select all the text in the handoff block and copy (Cmd+C / Ctrl+C)
- Or I can copy it to your clipboard automatically

### Step 2: Clear the Session

Run this command:
```

/clear

```

### Step 3: Paste the Handoff

After the session clears, paste the handoff:
- **macOS**: Cmd+V
- **Windows/Linux**: Ctrl+V
- **Warp**: Cmd+V or use Warp's paste

### Step 4: Continue

Claude will acknowledge the context and you can continue where you left off.
```

Also offer to copy to clipboard:

```bash
# Copy handoff to clipboard
HANDOFF='[THE GENERATED HANDOFF TEXT]'

if command -v pbcopy &> /dev/null; then
    echo "$HANDOFF" | pbcopy
    echo "Copied to clipboard (macOS)"
elif command -v clip.exe &> /dev/null; then
    echo "$HANDOFF" | clip.exe
    echo "Copied to clipboard (WSL)"
elif command -v xclip &> /dev/null; then
    echo "$HANDOFF" | xclip -selection clipboard
    echo "Copied to clipboard (xclip)"
elif command -v wl-copy &> /dev/null; then
    echo "$HANDOFF" | wl-copy
    echo "Copied to clipboard (Wayland)"
else
    echo "No clipboard tool found - please copy manually"
fi
```

## Handoff Variants

### `/wipe quick`

Minimal handoff for simple sessions:

```markdown
## Task

- [One-line description]

## State

- [Current status]

## Next

- [Immediate action]
```

### `/wipe detailed`

Comprehensive handoff for complex sessions:

```markdown
## What we're working on

- [Full task description with background]

## Current state

- [Detailed status]
- [All pending items]
- [Blockers or issues]

## Key decisions made

- [All significant decisions with rationale]
- [Rejected alternatives and why]

## Recent changes

- [All files modified with line numbers if relevant]
- [All commands run]
- [All errors encountered and resolutions]

## Important context

- [Technical architecture notes]
- [User preferences and constraints]
- [External dependencies]
- [Project conventions]

## Code snippets

- [Any important code that was written/discussed]

## Next steps

- [Prioritised list of remaining work]
- [Dependencies between tasks]
```

## Examples

### Example Quick Handoff

```markdown
## Task

- Implementing BM25 search in graph-query.js

## State

- BM25Index class added and tested
- Need to update skills documentation

## Next

- Update search.md and graph-query.md skills
```

### Example Detailed Handoff

```markdown
## What we're working on

- Adding BM25 relevance ranking to the vault's graph search system
- Part of improving search quality for Claude Code integration

## Current state

- BM25Index class implemented in scripts/graph-query.js (lines 36-153)
- Tested with "kafka integration" query - returns 70 results, top score 14.65
- Skills documentation not yet updated

## Key decisions made

- Chose BM25 over semantic search (Claude already has semantic understanding)
- Parameters: k1=1.5 (saturation), b=0.75 (length normalisation)
- Pure JS implementation, no new dependencies

## Recent changes

- Modified: scripts/graph-query.js (added BM25Index class)
- Modified: .claude/skills/graph-query/SKILL.md (pending)
- Modified: .claude/skills/search/SKILL.md (pending)

## Important context

- User prefers graph-first search strategy
- Template repo (ArchitectKB) needs same updates
- Organisation-specific content must be removed from template repo

## Next steps

- Update graph-query.md skill with BM25 documentation
- Update search.md skill with relevance score examples
- Copy changes to ArchitectKB template repo
```

## Notes

- The handoff is your lifeline in the new session - be thorough
- Clipboard backup ensures you never lose context even if automation fails
- tmux users get fully automated flow; others need 3 manual steps
- Consider running `/wipe` proactively when context is getting full
- The new session will have fresh context budget for continued work

## Related Skills

- `/summarize` - Summarize notes (different purpose)
- `/daily` - Daily notes (may want to log wipe in daily note)
