---
name: tmux-manage
description: General-purpose tmux session management for containers. Use this for listing sessions, creating/attaching/killing sessions, managing windows and panes, viewing session info, and general tmux operations across all containers.
---

# Tmux Management Skill

通用 tmux 会话管理工具，适用于所有开发和运营容器。

## Capabilities

### 1. Session Management
- List all tmux sessions
- Create new sessions with custom names
- Attach to existing sessions
- Kill sessions (single or multiple)
- Rename sessions
- Check if session exists

### 2. Window Management
- List windows in a session
- Create new windows
- Switch between windows
- Rename windows
- Kill windows

### 3. Pane Management
- Split panes (horizontal/vertical)
- Navigate between panes
- Resize panes
- Kill panes
- Synchronize panes

### 4. Session Information
- View session details
- Check active sessions
- Show session tree structure
- Display window and pane count

### 5. Quick Operations
- Quick attach to last session
- Create workspace sessions
- Clone session layout
- Session cleanup

## Common Commands

### List Sessions
```bash
# List all sessions
tmux list-sessions
tmux ls

# Show detailed session info
tmux list-sessions -F "#{session_name}: #{session_windows} windows (created #{session_created_string})"
```

### Create Sessions
```bash
# Create new session
tmux new-session -s <session-name>

# Create detached session
tmux new-session -d -s <session-name>

# Create session in specific directory
tmux new-session -s <session-name> -c /path/to/dir
```

### Attach to Sessions
```bash
# Attach to session
tmux attach-session -t <session-name>
tmux attach -t <session-name>
tmux a -t <session-name>

# Attach to last session
tmux attach

# Create or attach
tmux new-session -A -s <session-name>
```

### Kill Sessions
```bash
# Kill specific session
tmux kill-session -t <session-name>

# Kill all sessions except current
tmux kill-session -a

# Kill all sessions
tmux kill-server
```

### Window Operations
```bash
# Create new window
tmux new-window -t <session-name> -n <window-name>

# List windows
tmux list-windows -t <session-name>

# Kill window
tmux kill-window -t <session-name>:<window-index>
```

### Pane Operations
```bash
# Split pane horizontally
tmux split-window -h -t <session-name>

# Split pane vertically
tmux split-window -v -t <session-name>

# List panes
tmux list-panes -t <session-name>

# Send commands to pane
tmux send-keys -t <session-name>:<window>.<pane> "command" C-m
```

## Tmux Key Bindings

Default prefix: `Ctrl+B`

### Session Commands
- `Ctrl+B d` - Detach from session
- `Ctrl+B s` - List sessions
- `Ctrl+B $` - Rename session
- `Ctrl+B (` - Previous session
- `Ctrl+B )` - Next session

### Window Commands
- `Ctrl+B c` - Create new window
- `Ctrl+B ,` - Rename window
- `Ctrl+B w` - List windows
- `Ctrl+B n` - Next window
- `Ctrl+B p` - Previous window
- `Ctrl+B &` - Kill window
- `Ctrl+B 0-9` - Switch to window by number

### Pane Commands
- `Ctrl+B %` - Split horizontally
- `Ctrl+B "` - Split vertically
- `Ctrl+B o` - Next pane
- `Ctrl+B ;` - Last pane
- `Ctrl+B x` - Kill pane
- `Ctrl+B ←↑→↓` - Navigate panes
- `Ctrl+B {` - Move pane left
- `Ctrl+B }` - Move pane right
- `Ctrl+B z` - Toggle pane zoom
- `Ctrl+B !` - Break pane to new window

### Other Commands
- `Ctrl+B ?` - List all key bindings
- `Ctrl+B [` - Enter copy mode (scroll)
- `Ctrl+B ]` - Paste buffer
- `Ctrl+B :` - Enter command mode

## Useful Workflows

### Create Development Workspace
```bash
# Create session with multiple windows
tmux new-session -d -s workspace -n editor
tmux new-window -t workspace -n server
tmux new-window -t workspace -n logs
tmux new-window -t workspace -n shell
tmux attach -t workspace
```

### Monitor Multiple Services
```bash
# Create session with split panes
tmux new-session -d -s monitor
tmux split-window -h -t monitor
tmux split-window -v -t monitor:0.0
tmux split-window -v -t monitor:0.1
tmux attach -t monitor
```

### Quick Session Switch
```bash
# Detach and switch to another session
# In tmux: Ctrl+B d
tmux attach -t <another-session>

# Or use Ctrl+B s to select from list
```

### Session Cleanup
```bash
# Kill all dead sessions
for session in $(tmux ls | grep -v attached | cut -d: -f1); do
    tmux kill-session -t "$session"
done

# Kill sessions matching pattern
tmux ls | grep "pattern" | cut -d: -f1 | xargs -I {} tmux kill-session -t {}
```

## Configuration Tips

### Essential .tmux.conf Settings
```bash
# Mouse support
set -g mouse on

# Increase history limit
set -g history-limit 10000

# Start window numbering at 1
set -g base-index 1
set -g pane-base-index 1

# Renumber windows on close
set -g renumber-windows on

# Enable focus events
set -g focus-events on

# Status bar
set -g status-position bottom
set -g status-style 'bg=colour234 fg=colour137'
```

## Helper Scripts

The `scripts/` directory contains helper tools:

- `tmux-list.sh` - Enhanced session listing
- `tmux-quick-attach.sh` - Quick session selection
- `tmux-workspace.sh` - Create workspace layouts
- `tmux-cleanup.sh` - Clean up old sessions

## Best Practices

1. **Use Descriptive Names**: Name sessions after their purpose
   ```bash
   tmux new -s api-server
   tmux new -s log-monitor
   tmux new -s debug-session
   ```

2. **Detach, Don't Kill**: Use `Ctrl+B d` to detach instead of killing
   - Sessions persist after detaching
   - Easy to reattach later

3. **Check Existing Sessions**: Before creating new session
   ```bash
   tmux ls
   tmux has-session -t <name> 2>/dev/null
   ```

4. **Use Session Create-or-Attach**:
   ```bash
   tmux new-session -A -s <session-name>
   ```

5. **Clean Up Regularly**: Remove unused sessions
   ```bash
   tmux kill-session -t <unused-session>
   ```

6. **Keep Sessions Organized**:
   - One session per major task/project
   - Multiple windows within session for related subtasks
   - Split panes for side-by-side viewing

## Troubleshooting

### Session Already Exists
```bash
# Error: duplicate session
# Solution: Attach instead
tmux attach -t <session-name>

# Or kill and recreate
tmux kill-session -t <session-name>
tmux new -s <session-name>
```

### Cannot Connect to Server
```bash
# Check tmux is running
ps aux | grep tmux

# Check socket permissions
ls -la /tmp/tmux-*/

# Restart tmux server
tmux kill-server
tmux new-session
```

### Lost Session
```bash
# List all sessions
tmux ls

# Check for detached sessions
tmux ls | grep -v attached

# Attach to last session
tmux attach
```

### Pane Synchronization Issues
```bash
# Enable pane synchronization
tmux setw synchronize-panes on

# Disable pane synchronization
tmux setw synchronize-panes off

# Or use Ctrl+B : then type
:setw synchronize-panes on
```

## Integration with Container Workflows

### Development Container
```bash
# Create dev session on container startup
tmux new-session -d -s dev -n editor
tmux new-window -t dev -n terminal
tmux new-window -t dev -n logs

# Attach when needed
tmux attach -t dev
```

### Operations Container
```bash
# Monitor session for production
tmux new-session -d -s ops -n metrics
tmux new-window -t ops -n alerts
tmux new-window -t ops -n logs

# Multiple monitors
tmux split-window -h -t ops:metrics
tmux split-window -v -t ops:metrics.0
```

### CI/CD Container
```bash
# Temporary build session
tmux new-session -d -s "build-${BUILD_ID}"
tmux send-keys -t "build-${BUILD_ID}" "make build" C-m

# Capture output
tmux pipe-pane -t "build-${BUILD_ID}" 'cat > build.log'

# Kill after completion
tmux kill-session -t "build-${BUILD_ID}"
```

## Managed Sessions

This skill provides pre-configured session management scripts for common workflows.

### System Monitor Session

**univers-monitor** - System monitoring dashboard (4-pane layout)

```bash
# Start monitor session
tmux-monitor start

# Attach to monitor
tmux-monitor attach

# Check status
tmux-monitor status

# Stop monitor
tmux-monitor stop
```

**Features:**
- Real-time system resource monitoring
- 4-pane split layout for comprehensive overview
- Auto-refresh monitoring data
- 50,000 line history buffer

**Layout:**

```
┌──────────────┬──────────────┐
│   系统资源    │   进程监控    │
│   (htop)     │   (top CPU)   │
├──────────────┼──────────────┤
│   磁盘监控    │   网络监控    │
│   (df/du)    │   (ss/ip)     │
└──────────────┴──────────────┘
```

**Panes:**
- **Pane 0 (Top-Left)**: System resources (htop/top)
- **Pane 1 (Top-Right)**: Top CPU processes (watch ps)
- **Pane 2 (Bottom-Left)**: Disk usage (watch df/du)
- **Pane 3 (Bottom-Right)**: Network connections (watch ss/ip)

**Navigation:**
- `Ctrl+B ←↑→↓` to navigate between panes
- `Ctrl+B Z` to zoom/unzoom current pane

### Container Manager Session

**univers-manager** - Container management terminal

```bash
# Start manager session
tmux-manager start

# Attach to manager
tmux-manager attach

# Check status
tmux-manager status

# Stop manager
tmux-manager stop
```

**Features:**
- Opens in univers-container directory
- Shows available container management commands
- Persistent session for Claude Code and skill management
- 50,000 line history buffer

### Desktop View Session

**univers-desktop-view** - Split-pane aggregated view (for desktop monitors)

```bash
# Start desktop view
tmux-desktop-view start

# Attach to view
tmux-desktop-view attach

# Check status
tmux-desktop-view status
```

**Layout:**

Window 1: **workbench** (4 panes)
```
┌──────────────┬──────────────┐
│              │  server      │
│  developer   ├──────────────┤
│              │  ui          │
│              ├──────────────┤
│              │  web         │
└──────────────┴──────────────┘
```

Window 2: **operation** (1 pane)
- univers-operator

Window 3: **manager** (1 pane)
- univers-manager

**Dependencies:**
- univers-developer (hvac-workbench)
- univers-server (hvac-workbench)
- univers-ui (hvac-workbench)
- univers-web (hvac-workbench)
- univers-operator (hvac-operation)
- univers-manager (univers-container)

### Mobile View Session

**univers-mobile-view** - Multi-window view (for smaller screens/mobile workflows)

```bash
# Start mobile view
tmux-mobile-view start

# Attach to view
tmux-mobile-view attach

# Check status
tmux-mobile-view status
```

**Layout:**

Window 1: **dev** - univers-developer

Window 2: **service** (3 panes, vertical stack)
```
┌──────────────┐
│  server      │
├──────────────┤
│  ui          │
├──────────────┤
│  web         │
└──────────────┘
```

Window 3: **ops** - univers-operator

Window 4: **manager** - univers-manager

**Navigation:**
- `Ctrl+B 1-4` to switch between windows
- `Ctrl+B ←↑→↓` to navigate panes in service window

**Dependencies:** Same as desktop view

### Installation

Install all tmux-manage commands globally:

```bash
cd .claude/skills/tmux-manage
./install.sh
```

This creates global commands:
- `tmux-manager` - Manager session control
- `tmux-desktop-view` - Desktop view control
- `tmux-mobile-view` - Mobile view control
- `tmux-monitor` - System monitor control

### Complete Workflow Example

```bash
# 1. Start all base sessions
univers-dev developer start      # Developer terminal
univers-dev server start socket  # Backend server
univers-dev ui start             # UI development
univers-dev web start            # Web development
univers-ops operator start       # Operations console
tmux-manager start               # Container manager

# 2. Start aggregated view
tmux-desktop-view start          # Or tmux-mobile-view start

# 3. Attach to view
tmux-desktop-view attach

# 4. Work with unified interface
# - All services visible in one view
# - Switch windows/panes as needed
# - Detach without stopping services (Ctrl+B D)
```

## Version History

- v1.2 (2025-10-24): Add system-monitor session with 4-pane layout
- v1.1 (2025-10-24): Add manager, desktop-view, mobile-view sessions
- v1.0 (2025-10-24): Initial tmux management skill
