---
name: tmux-init
description: Set up tmux notification system for Claude Code sessions
argument-hint: "[--uninstall] [--status]"
allowed-tools: Bash, Read, Write, Edit
---

# tmux-init

Set up a notification system for Claude Code that sends native macOS notifications when sessions need attention, with click-to-navigate support for tmux panes.

## Usage

```bash
/tmux-init              # Install notification system
/tmux-init --status     # Check installation status
/tmux-init --uninstall  # Remove notification system
```

## What Gets Installed

1. **Scripts** in `~/bin/`:
   - `notify-claude.sh` - Generates macOS notifications
   - `go-tmux.sh` - Navigates to tmux pane on notification click

2. **Webhook service** (LaunchAgent):
   - Listens on port 9000 for notification requests
   - Auto-starts on login

3. **Shell environment** (added to ~/.zshrc):
   - `WS_TMUX_LOCATION` - Current tmux session:window.pane
   - `WS_TMUX_SESSION_NAME` - Current session name
   - `WS_TMUX_WINDOW_NAME` - Current window name

4. **Claude hooks** (added to ~/.claude/settings.json):
   - `Stop` hook - Notifies when Claude finishes
   - `Notification` hook - Notifies when Claude needs input

## Prerequisites

- macOS
- tmux
- Homebrew (for installing dependencies)

## Execution Instructions

### Parse Arguments

```bash
UNINSTALL=false
STATUS=false

for arg in "$@"; do
    case "$arg" in
        --uninstall) UNINSTALL=true ;;
        --status) STATUS=true ;;
    esac
done
```

### If --status: Check Installation Status

```bash
echo "=== Claude tmux Notification System Status ==="
echo ""

# Check dependencies
echo "Dependencies:"
command -v terminal-notifier &>/dev/null && echo "  ✅ terminal-notifier" || echo "  ❌ terminal-notifier (missing)"
command -v webhook &>/dev/null && echo "  ✅ webhook" || echo "  ❌ webhook (missing)"
command -v jq &>/dev/null && echo "  ✅ jq" || echo "  ❌ jq (missing)"
command -v tmux &>/dev/null && echo "  ✅ tmux" || echo "  ❌ tmux (missing)"
echo ""

# Check scripts
echo "Scripts:"
[ -x "$HOME/bin/notify-claude.sh" ] && echo "  ✅ ~/bin/notify-claude.sh" || echo "  ❌ ~/bin/notify-claude.sh (missing)"
[ -x "$HOME/bin/go-tmux.sh" ] && echo "  ✅ ~/bin/go-tmux.sh" || echo "  ❌ ~/bin/go-tmux.sh (missing)"
[ -f "$HOME/bin/hooks.json" ] && echo "  ✅ ~/bin/hooks.json" || echo "  ❌ ~/bin/hooks.json (missing)"
echo ""

# Check LaunchAgent
echo "Webhook Service:"
PLIST="$HOME/Library/LaunchAgents/com.claude.webhook.plist"
if [ -f "$PLIST" ]; then
    if launchctl list | grep -q "com.claude.webhook"; then
        echo "  ✅ LaunchAgent installed and running"
    else
        echo "  ⚠️  LaunchAgent installed but not running"
    fi
else
    echo "  ❌ LaunchAgent not installed"
fi
echo ""

# Check webhook port
echo "Webhook Port:"
if curl -s http://localhost:9000/hooks/claude-notify -o /dev/null -w "%{http_code}" | grep -q "200\|405"; then
    echo "  ✅ Port 9000 responding"
else
    echo "  ❌ Port 9000 not responding"
fi
echo ""

# Check shell environment
echo "Shell Environment:"
if grep -q "WS_TMUX_LOCATION" "$HOME/.zshrc" 2>/dev/null; then
    echo "  ✅ tmux env vars in ~/.zshrc"
else
    echo "  ❌ tmux env vars not in ~/.zshrc"
fi
echo ""

# Check Claude hooks via webhook log
echo "Claude Hooks (check log for activity):"
LOG_FILE="$HOME/Library/Logs/claude-webhook/webhook.log"
if [ -f "$LOG_FILE" ]; then
    RECENT_LINES=$(tail -5 "$LOG_FILE" 2>/dev/null)
    if [ -n "$RECENT_LINES" ]; then
        echo "  Recent webhook log entries:"
        echo "$RECENT_LINES" | sed 's/^/    /'
    else
        echo "  ⚠️  Log file exists but is empty"
    fi
    echo ""
    echo "  To verify hooks are working, trigger a Claude stop event"
    echo "  and check: tail -f ~/Library/Logs/claude-webhook/webhook.log"
else
    echo "  ⚠️  No log file yet at ~/Library/Logs/claude-webhook/webhook.log"
    echo "  Log will be created when first notification is received"
fi
```

Exit after showing status.

### If --uninstall: Remove Installation

```bash
echo "=== Uninstalling Claude tmux Notification System ==="
echo ""

# Stop and remove LaunchAgent
PLIST="$HOME/Library/LaunchAgents/com.claude.webhook.plist"
if [ -f "$PLIST" ]; then
    echo "Stopping webhook service..."
    launchctl unload "$PLIST" 2>/dev/null || true
    rm -f "$PLIST"
    echo "  ✅ LaunchAgent removed"
fi

# Remove scripts
echo "Removing scripts..."
rm -f "$HOME/bin/notify-claude.sh"
rm -f "$HOME/bin/go-tmux.sh"
rm -f "$HOME/bin/hooks.json"
echo "  ✅ Scripts removed"

# Note: Don't remove shell env or Claude hooks automatically
echo ""
echo "Manual cleanup (optional):"
echo "  - Remove WS_TMUX_* lines from ~/.zshrc"
echo "  - Remove Stop/Notification hooks from ~/.claude/settings.json"
echo ""
echo "✅ Uninstallation complete"
```

Exit after uninstalling.

### Install: Full Setup

#### Step 1: Check and Install Dependencies

```bash
echo "=== Installing Claude tmux Notification System ==="
echo ""
echo "Step 1: Checking dependencies..."

MISSING_DEPS=()

if ! command -v terminal-notifier &>/dev/null; then
    MISSING_DEPS+=("terminal-notifier")
fi

if ! command -v webhook &>/dev/null; then
    MISSING_DEPS+=("webhook")
fi

if ! command -v jq &>/dev/null; then
    MISSING_DEPS+=("jq")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "Installing missing dependencies: ${MISSING_DEPS[*]}"
    brew install "${MISSING_DEPS[@]}"
fi

echo "  ✅ Dependencies installed"
```

#### Step 2: Create ~/bin and Copy Scripts

```bash
echo ""
echo "Step 2: Installing scripts to ~/bin..."

mkdir -p "$HOME/bin"

# Find the source scripts directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
NOTIFICATION_DIR="$SCRIPT_DIR/../../../scripts/notifications"

# If running from plugin context, find the repo root
if [ ! -d "$NOTIFICATION_DIR" ]; then
    # Try to find via git
    REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
    if [ -n "$REPO_ROOT" ]; then
        NOTIFICATION_DIR="$REPO_ROOT/scripts/notifications"
    fi
fi

# Copy scripts
cp "$NOTIFICATION_DIR/notify-claude.sh" "$HOME/bin/"
cp "$NOTIFICATION_DIR/go-tmux.sh" "$HOME/bin/"
chmod +x "$HOME/bin/notify-claude.sh"
chmod +x "$HOME/bin/go-tmux.sh"

# Process hooks.json - replace placeholder with actual path
sed "s|__BIN_DIR__|$HOME/bin|g" "$NOTIFICATION_DIR/hooks.json" > "$HOME/bin/hooks.json"

echo "  ✅ Scripts installed"
```

#### Step 3: Set Up LaunchAgent

```bash
echo ""
echo "Step 3: Setting up webhook LaunchAgent..."

PLIST_DIR="$HOME/Library/LaunchAgents"
PLIST_FILE="$PLIST_DIR/com.claude.webhook.plist"
LOG_DIR="$HOME/Library/Logs/claude-webhook"

mkdir -p "$PLIST_DIR"
mkdir -p "$LOG_DIR"

# Find webhook binary
WEBHOOK_BIN=$(which webhook)

# Process plist template
sed -e "s|__WEBHOOK_BIN__|$WEBHOOK_BIN|g" \
    -e "s|__HOOKS_JSON__|$HOME/bin/hooks.json|g" \
    -e "s|__LOG_DIR__|$LOG_DIR|g" \
    "$NOTIFICATION_DIR/com.claude.webhook.plist" > "$PLIST_FILE"

# Load the LaunchAgent
launchctl unload "$PLIST_FILE" 2>/dev/null || true
launchctl load "$PLIST_FILE"

echo "  ✅ Webhook service started"
```

#### Step 4: Add Shell Environment

```bash
echo ""
echo "Step 4: Configuring shell environment..."

ZSHRC="$HOME/.zshrc"
MARKER="# Claude tmux notification environment"

if ! grep -q "$MARKER" "$ZSHRC" 2>/dev/null; then
    cat >> "$ZSHRC" << 'EOF'

# Claude tmux notification environment
if [ -n "$TMUX" ] && [ -z "$WS_TMUX_LOCATION" ]; then
    export WS_TMUX_LOCATION=$(tmux display-message -p '#{session_name}:#{window_index}.#{pane_index}')
    export WS_TMUX_SESSION_NAME=$(tmux display-message -p '#{session_name}')
    export WS_TMUX_WINDOW_NAME=$(tmux display-message -p '#{window_name}')
fi
EOF
    echo "  ✅ Added tmux env vars to ~/.zshrc"
else
    echo "  ⏭️  tmux env vars already in ~/.zshrc"
fi
```

#### Step 5: Configure Claude Hooks

```bash
echo ""
echo "Step 5: Configuring Claude hooks..."

CLAUDE_SETTINGS="$HOME/.claude/settings.json"

# Create settings file if it doesn't exist
if [ ! -f "$CLAUDE_SETTINGS" ]; then
    mkdir -p "$HOME/.claude"
    echo '{}' > "$CLAUDE_SETTINGS"
fi

# Check if hooks already configured
if grep -q "claude-notify" "$CLAUDE_SETTINGS" 2>/dev/null; then
    echo "  ⏭️  Claude hooks already configured"
else
    # Use jq to merge hooks into existing settings
    HOOK_CMD='jq -n --arg tmux_location "$WS_TMUX_LOCATION" --arg tmux_session_name "$WS_TMUX_SESSION_NAME" --arg tmux_window_name "$WS_TMUX_WINDOW_NAME" --arg project "$(basename \"$PWD\")" --arg cwd "$PWD" --arg hook_event_name "__EVENT__" --arg session_id "$CLAUDE_SESSION_ID" '"'"'{tmux_location: $tmux_location, tmux_session_name: $tmux_session_name, tmux_window_name: $tmux_window_name, project: $project, cwd: $cwd, hook_event_name: $hook_event_name, session_id: $session_id}'"'"' | curl -s -X POST -H '"'"'Content-Type: application/json'"'"' -d @- http://localhost:9000/hooks/claude-notify'

    STOP_CMD="${HOOK_CMD/__EVENT__/Stop}"
    NOTIFICATION_CMD="${HOOK_CMD/__EVENT__/Notification}"

    # Create the hooks JSON structure
    HOOKS_JSON=$(cat << ENDJSON
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$STOP_CMD"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$NOTIFICATION_CMD"
          }
        ]
      }
    ]
  }
}
ENDJSON
)

    # Merge with existing settings
    jq -s '.[0] * .[1]' "$CLAUDE_SETTINGS" <(echo "$HOOKS_JSON") > "$CLAUDE_SETTINGS.tmp"
    mv "$CLAUDE_SETTINGS.tmp" "$CLAUDE_SETTINGS"

    echo "  ✅ Claude hooks configured"
fi
```

#### Step 6: Verify Installation

```bash
echo ""
echo "Step 6: Verifying installation..."

sleep 1  # Give webhook time to start

if curl -s http://localhost:9000/hooks/claude-notify -o /dev/null; then
    echo "  ✅ Webhook service responding"
else
    echo "  ⚠️  Webhook service not responding yet (may need a moment)"
fi

echo ""
echo "=========================================="
echo "✅ Installation complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Restart your shell or run: source ~/.zshrc"
echo "  2. Start a new tmux session"
echo "  3. Run Claude Code - you'll get notifications!"
echo ""
echo "Test the notification:"
echo '  curl -X POST -H "Content-Type: application/json" \'
echo '    -d '"'"'{"tmux_location":"test:0.0","tmux_session_name":"test","tmux_window_name":"test","project":"test","cwd":"/tmp","hook_event_name":"Stop","session_id":"test"}'"'"' \'
echo '    http://localhost:9000/hooks/claude-notify'
echo ""
echo "Check status anytime with: /tmux-init --status"
```

## Troubleshooting

### Notifications not appearing

1. Check if webhook is running:
   ```bash
   launchctl list | grep claude.webhook
   ```

2. Check webhook logs:
   ```bash
   tail -f ~/Library/Logs/claude-webhook/webhook.log
   ```

3. Test webhook manually:
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"tmux_location":"test:0.0","hook_event_name":"Stop"}' \
     http://localhost:9000/hooks/claude-notify
   ```

### Click doesn't navigate to pane

1. Ensure tmux env vars are set:
   ```bash
   echo $WS_TMUX_LOCATION
   ```

2. Test navigation script:
   ```bash
   ~/bin/go-tmux.sh "session:0.0"
   ```

### Webhook won't start

1. Check if port 9000 is in use:
   ```bash
   lsof -i :9000
   ```

2. Try restarting:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.claude.webhook.plist
   launchctl load ~/Library/LaunchAgents/com.claude.webhook.plist
   ```
