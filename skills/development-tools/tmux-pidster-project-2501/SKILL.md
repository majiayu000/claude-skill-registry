---
name: tmux
description: Manage tmux sessions. Use when needing to create, list, attach to, or manage terminal multiplexer sessions. Triggers on "tmux", "create session", "list sessions", "terminal session".
allowed-tools: Bash
---

# Skill: tmux Session Management

Manage tmux sessions for terminal multiplexing.

## When to Use

Use this skill when:
- Creating new tmux sessions for background work
- Listing existing sessions
- Attaching to or detaching from sessions
- Killing sessions that are no longer needed

**Trigger phrases:** "tmux", "create session", "list sessions", "terminal session", "background terminal", "attach session", "detach session"

## Prerequisites

tmux must be installed. Check with:

```bash
which tmux && tmux -V
```

## If tmux Is Not Found

If `which tmux` returns nothing, alert the user that tmux is not installed and suggest installation based on the operating system.

### Detect Operating System

```bash
case "$(uname -s)" in
    Darwin)  echo "macOS" ;;
    Linux)
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            echo "Linux ($ID)"
        else
            echo "Linux"
        fi
        ;;
    *)       echo "Unknown OS: $(uname -s)" ;;
esac
```

### Installation Commands by OS

| OS | Package Manager | Installation Command |
|----|-----------------|---------------------|
| **macOS** | Homebrew | `brew install tmux` |
| **macOS** | MacPorts | `sudo port install tmux` |
| **Ubuntu/Debian** | apt | `sudo apt update && sudo apt install tmux` |
| **Fedora** | dnf | `sudo dnf install tmux` |
| **CentOS/RHEL** | yum | `sudo yum install tmux` |
| **Arch Linux** | pacman | `sudo pacman -S tmux` |
| **Alpine** | apk | `sudo apk add tmux` |
| **openSUSE** | zypper | `sudo zypper install tmux` |

### User Notification Template

When tmux is not found, inform the user:

```
tmux is not installed on this system.

To install tmux on [detected OS]:
  [appropriate installation command]

After installation, you can verify with:
  tmux -V
```

**Do not attempt to install software automatically.** Always present the installation command to the user and let them decide whether to proceed.

## Session Management Commands

### List Sessions

```bash
tmux list-sessions 2>/dev/null || echo "No tmux sessions running"
```

Or with more detail:

```bash
tmux list-sessions -F "#{session_name}: #{session_windows} windows (created #{session_created_string})" 2>/dev/null || echo "No tmux sessions running"
```

### Create Session

Create a new detached session:

```bash
tmux new-session -d -s <session-name>
```

Create with a specific starting directory:

```bash
tmux new-session -d -s <session-name> -c /path/to/directory
```

Create and run a command:

```bash
tmux new-session -d -s <session-name> '<command>'
```

### Attach to Session

**Note:** Attaching is interactive and will take over the terminal. Only suggest this to users; do not execute directly.

```bash
tmux attach-session -t <session-name>
```

### Detach from Session

From within tmux: `Ctrl-b d`

Or programmatically detach all clients:

```bash
tmux detach-client -s <session-name>
```

### Kill Session

```bash
tmux kill-session -t <session-name>
```

Kill all sessions:

```bash
tmux kill-server
```

### Check if Session Exists

```bash
tmux has-session -t <session-name> 2>/dev/null && echo "exists" || echo "not found"
```

## Session Naming Conventions

Sessions are **local to each machine** (not shared across team members), so we use a naming convention rather than a registry file.

### Pattern

```
<project-slug>-<purpose>
```

Where:
- `<project-slug>` identifies the project (derived from directory name or configured)
- `<purpose>` links to a task ID, process instance, or descriptive slug

### Deriving Project Slug

```bash
# From directory name (simple)
PROJECT_SLUG=$(basename "$CLAUDE_PROJECT_DIR" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

# Or use a configured value if available
PROJECT_SLUG="${DIALOGUE_PROJECT_SLUG:-$(basename "$CLAUDE_PROJECT_DIR")}"
```

### Purpose Patterns

| Purpose Type | Pattern | Example Session Name |
|--------------|---------|---------------------|
| Task-linked | `<project>-<task-id>` | `project-2501-FW-033` |
| Process instance | `<project>-<process-id>` | `project-2501-PI-001` |
| Build process | `<project>-build` | `project-2501-build` |
| File watcher | `<project>-watch` | `project-2501-watch` |
| Server | `<project>-serve` | `project-2501-serve` |

### Listing Project Sessions

Filter sessions belonging to the current project:

```bash
PROJECT_SLUG=$(basename "$CLAUDE_PROJECT_DIR" | tr '[:upper:]' '[:lower:]')
tmux list-sessions -F "#{session_name}" 2>/dev/null | grep "^${PROJECT_SLUG}-" || echo "No project sessions"
```

### Framework Discovery

The framework orchestrator can discover running sessions and correlate them:

```bash
# List project sessions with details
PROJECT_SLUG=$(basename "$CLAUDE_PROJECT_DIR" | tr '[:upper:]' '[:lower:]')
tmux list-sessions -F "#{session_name}|#{session_created}|#{session_windows}" 2>/dev/null | \
    grep "^${PROJECT_SLUG}-" | \
    while IFS='|' read -r name created windows; do
        # Extract purpose (everything after project slug)
        purpose="${name#${PROJECT_SLUG}-}"
        echo "Session: $name | Purpose: $purpose | Windows: $windows"
    done
```

This allows the framework to:
1. Discover all sessions for the current project
2. Parse the purpose suffix to identify linked tasks or processes
3. Correlate with `.dialogue/tasks/` or process instance state

## Common Patterns

### Run Long Process in Background

```bash
# Create session and run command
tmux new-session -d -s my-build 'npm run build:watch'

# Check it's running
tmux list-sessions | grep my-build
```

### Check Session Output

Send keys to capture recent output (session must exist):

```bash
tmux capture-pane -t <session-name> -p | tail -20
```

### Send Command to Running Session

```bash
tmux send-keys -t <session-name> 'echo hello' Enter
```

## Safety Notes

- Always use `-d` (detached) when creating sessions from scripts
- Check if a session exists before creating to avoid duplicates
- Clean up sessions when work is complete
- Do not attach interactively without user intent
