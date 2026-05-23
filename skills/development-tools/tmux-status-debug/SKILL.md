---
name: tmux-status-debug
description: Debug and test tmux pane status detection for AI agents (opencode, claude, amp). Use when patterns aren't matching, status icons are wrong, or adding new detection patterns.
---

# Debugging tmux-opencode-integrated Status Detection

## When to Use

- Status icons showing wrong state (e.g., showing ERROR when agent is IDLE)
- Adding new patterns for agent detection
- Testing pattern matching against real pane content

## Quick Commands

### List all agent panes

```bash
tmux list-panes -a -F "#{session_name}:#{window_name}.#{pane_index} #{pane_current_command}" | grep -E "opencode|claude|amp"
```

### Capture pane content (raw)

```bash
tmux capture-pane -t "main:1" -p -S -30 | tail -40
```

### Capture with control chars visible

```bash
tmux capture-pane -t "main:1" -p -S -30 | cat -v | tail -40
```

### Check if pattern exists in pane

```bash
tmux capture-pane -t "main:1" -p -S -20 | grep -o "pattern"
```

## Debug Script

Create `/tmp/debug_status.py` and run with the Nix Python that has libtmux:

```python
import sys
sys.path.insert(0, "/Users/emiller/.config/dotfiles/packages/tmux-opencode-integrated/scripts")
import smart_name
import re

import libtmux
server = libtmux.Server()
for session in server.sessions:
    for window in session.windows:
        for pane in window.panes:
            program = smart_name.get_pane_program(pane)
            if program in smart_name.AGENT_PROGRAMS:
                print(f"\n=== {program} in {session.name}:{window.name} ===")
                try:
                    cmd_output = pane.cmd("capture-pane", "-p", "-S", "-20").stdout
                    if isinstance(cmd_output, list):
                        content = "\n".join(cmd_output)
                    else:
                        content = str(cmd_output)

                    cleaned = smart_name.strip_ansi_and_control(content)
                    print(f"Last 300 chars (cleaned):\n{cleaned[-300:]}")
                    print(f"\n--- Status: {smart_name.get_opencode_status(pane)} ---")
                except Exception as e:
                    print(f"Error: {e}")
```

### Find the Nix Python with libtmux

```bash
# Build the package and get the store path
nix build .#tmux-opencode-integrated --no-link --print-out-paths

# Check wrapper to find Python path
head -10 /nix/store/<hash>-tmux-opencode-integrated-*/share/tmux-plugins/tmux-opencode-integrated/scripts/smart-name.sh

# Run debug script with that Python
/nix/store/<python-hash>-python3-*-env/bin/python3 /tmp/debug_status.py
```

## Pattern Testing

Test patterns against sample content:

```python
import re

content = """ctrl+t variants  tab agents  ctrl+p commands    • OpenCode 1.1.30"""

patterns = [
    (r"OpenCode \d+\.\d+\.\d+", "IDLE - version"),
    (r"ctrl\+p commands", "IDLE - status bar"),
    (r"esc interrupt", "BUSY - can interrupt"),
    (r"Esc to cancel", "BUSY - can cancel"),
    (r"■■■", "BUSY - progress bar"),
]

for pattern, desc in patterns:
    if re.search(pattern, content, re.IGNORECASE):
        print(f"✓ {desc}: {pattern}")
```

## Status Priority

Order matters - first match wins:

1. **ERROR** - Traceback, panic, FATAL ERROR, API errors
2. **WAITING** - Allow once?, Permission required, yes/no/skip prompts
3. **BUSY** - Thinking..., spinners, Running tools, esc interrupt
4. **IDLE** - Input prompt, context display, OpenCode version, ctrl+p commands
5. **UNKNOWN** - No patterns matched (fallback)

## Adding New Patterns

1. Capture real pane content with the debug script above
2. Identify unique text that indicates the state
3. Add pattern to appropriate list in `smart_name.py`
4. Add test case in `tests/test_smart_name.py`
5. Run tests: `uvx pytest tests/test_smart_name.py -v`
6. Rebuild: `nix build .#tmux-opencode-integrated`

## Common Issues

### "No module named 'libtmux'"

Using wrong Python. Must use the Nix-wrapped Python from the package.

### Patterns not matching

Terminal control characters may be interfering. The `strip_ansi_and_control()` function should handle this, but check with `cat -v` to see raw content.

### Status showing ERROR when it shouldn't

Check if content contains error-like strings from previous output. The detection looks at last 20 lines of pane content.
