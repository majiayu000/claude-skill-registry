---
name: ttt
description: Send messages to other tmux sessions for multi-agent coordination. Use when user types 'ttt' or needs to communicate with other Claude/Gemini instances running in different tmux sessions.
model: haiku
---

# TTT - Tmux Talk To

## Purpose
Send messages to other tmux sessions for multi-agent coordination and automation. Enables communication between multiple Claude/Gemini instances.

## When to Use
- User explicitly types `ttt`
- Need to send tasks to different Claude instances
- Parallel execution across multiple agents
- Workflow automation across sessions
- Coordinating multi-agent work

## Usage Syntax

### Basic Communication (Claude Code)
```bash
tmux send-keys -t [session_name] "[message]" C-d
```

### Basic Communication (Terminal/Shell)
```bash
tmux send-keys -t [session_name] "[message]" C-m
```

### Handle Stuck Sessions
```bash
tmux send-keys -t [session_name] C-[ "[message]" C-d
```

### List Available Sessions
```bash
tmux list-sessions
```

## Steps

### 1. Use TTT Script (No LLM needed - pure bash)

This skill now uses `scripts/ttt_tmux.sh` which handles all tmux operations without requiring LLM processing. This saves 100% of LLM costs for this skill.

### 2. Understand User Request

User will provide:
- `ttt --list` - List all sessions
- `ttt [session] "[message]"` - Send message to session
- `ttt [session] --esc "[message]"` - Send ESC then message (if stuck)

### 3. Execute Script

**List sessions:**
```bash
./scripts/ttt_tmux.sh --list
```

**Send normal message:**
```bash
./scripts/ttt_tmux.sh [session_name] "[message]"
```

**Send with ESC (clear input first):**
```bash
./scripts/ttt_tmux.sh --esc [session_name] "[message]"
```

The script will:
- Validate session exists
- Send tmux commands with correct key bindings (C-d for Claude Code)
- Report success with timestamp (GMT+7)
- Show helpful errors if session not found

## Examples

### Example 1: Basic Message (Claude Code)
```bash
# User: ttt claude1 "สวัสดี"

# Validate session
tmux has-session -t claude1

# Send message (Claude Code uses C-d)
tmux send-keys -t claude1 "สวัสดี" C-d

# Report
✅ Message sent to 'claude1'
Message: "สวัสดี"
Mode: normal (C-d for Claude Code)
```

### Example 2: Handle Stuck Session
```bash
# User: ttt claude1 --esc "create retrospective"

# Validate session
tmux has-session -t claude1

# Send ESC then message (Claude Code uses C-d)
tmux send-keys -t claude1 C-[ "create retrospective" C-d

# Report
✅ Message sent to 'claude1'
Message: "create retrospective"
Mode: esc (cleared input first)
```

### Example 3: List Sessions
```bash
# User: ttt --list

# List all sessions
tmux list-sessions

# Format output
Available tmux sessions:

1. claude1: 1 windows (created 2 hours ago)
2. gemini1: 2 windows (created 30 minutes ago)
3. dev: 3 windows (created 1 day ago)

Use 'ttt [session_name] "[message]"' to send messages.
```

### Example 4: Multi-Agent Coordination
```bash
# User: ttt claude1 "analyze auth.ts for security issues"
# User: ttt claude2 "write unit tests for auth.ts"
# User: ttt claude3 "review both outputs and create summary"

# Send to each session (Claude Code uses C-d)
tmux send-keys -t claude1 "analyze auth.ts for security issues" C-d
tmux send-keys -t claude2 "write unit tests for auth.ts" C-d
tmux send-keys -t claude3 "review both outputs and create summary" C-d

# Report
✅ Sent 3 messages to parallel agents:
- claude1: Security analysis
- claude2: Unit tests
- claude3: Review & summary

Check each session for results.
```

## Use Cases

### 1. Multi-Agent Coordination
Send different tasks to different Claude instances:
```bash
ttt gemini1 "research approach A"
ttt gemini2 "research approach B"
ttt claude1 "compare both approaches and recommend"
```

### 2. Parallel Execution
Run tasks concurrently across sessions:
```bash
ttt dev1 "run tests"
ttt dev2 "build project"
ttt dev3 "lint codebase"
```

### 3. Workflow Automation
Chain commands across multiple agents:
```bash
ttt gemini1 "analyze codebase"
# Wait for completion
ttt claude1 "create plan based on gemini1's analysis"
# Wait for completion
ttt dev1 "execute the plan with gogogo"
```

## Important Notes

### Tmux Key Bindings
- **C-d**: Submit (sends message in Claude Code) ✅ DEFAULT
- **C-m**: Enter/Newline (sends in terminal, but only newline in Claude Code)
- **C-[**: ESC key (clears input, use when stuck)

### Session Validation
- **Always check** if session exists before sending
- **Provide helpful errors** with available sessions
- **Suggest corrections** if session name is close match

### Message Formatting
- **Escape quotes** in messages properly
- **Use double quotes** for messages with spaces
- **Preserve special characters** (don't escape unnecessarily)

### Error Handling
- **Session not found**: List available sessions
- **Tmux not running**: Guide user to start tmux
- **Permission denied**: Check tmux socket permissions

## Advanced Usage

### Send to Multiple Sessions
```bash
# Send same message to multiple sessions
for session in gemini1 gemini2 claude1; do
  tmux send-keys -t $session "[message]" C-m
done
```

### Session Info
```bash
# Get detailed session info
tmux display-message -p -t [session_name] "#{session_name}: #{window_index} windows, created #{session_created}"
```

### Window Management
```bash
# Send to specific window in session
tmux send-keys -t [session_name]:[window_index] "[message]" C-m

# Example: Send to window 2 of gemini1
tmux send-keys -t gemini1:2 "hello" C-m
```

## Troubleshooting

**"no server running on /tmp/tmux-*":**
```
❌ Tmux server not running. Start with:
  tmux new -s my-session
```

**"can't find session [name]":**
```
❌ Session '[name]' not found.

Available sessions:
[list sessions]

Did you mean: [closest match]?
```

**"input stuck, message not processing":**
```
Use --esc flag to clear input first:
  ttt [session] --esc "[message]"
```

## Success Criteria
- ✅ Tmux session validated before sending
- ✅ Message sent successfully
- ✅ User informed of result
- ✅ Error messages helpful and actionable
- ✅ Time recorded (GMT+7)
- ✅ Mode indicated (normal/esc)

## Performance Notes
- **Fast**: Haiku model for quick execution (~10x cost savings)
- **Instant**: tmux send-keys is near-instant
- **Parallel**: Can send to multiple sessions simultaneously
- **Reliable**: Session validation prevents errors

## Related Skills
- `lll` - Check project status before coordinating
- `nnn` - Create plan, then distribute tasks via ttt
- `rrr` - Collect results from multiple sessions for retrospective
