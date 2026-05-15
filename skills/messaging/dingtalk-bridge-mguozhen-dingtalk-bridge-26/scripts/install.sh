#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
echo "=== DingTalk Bridge Installer ==="
echo "Skill dir: $SKILL_DIR"
echo

# --- 1. Python deps ---
echo "[1/4] Installing Python dependencies..."
pip3 install --user dingtalk_stream websockets 2>/dev/null || pip3 install dingtalk_stream websockets
echo "  Done."
echo

# --- 2. Credentials ---
echo "[2/4] Configuring credentials..."
CONFIG_FILE="$SKILL_DIR/config.json"

if [ -f "$CONFIG_FILE" ]; then
    echo "  config.json already exists, skipping."
else
    APP_KEY="${DINGTALK_APP_KEY:-}"
    APP_SECRET="${DINGTALK_APP_SECRET:-}"

    if [ -z "$APP_KEY" ]; then
        read -rp "  DingTalk App Key: " APP_KEY
    else
        echo "  Using DINGTALK_APP_KEY from env."
    fi

    if [ -z "$APP_SECRET" ]; then
        read -rsp "  DingTalk App Secret: " APP_SECRET
        echo
    else
        echo "  Using DINGTALK_APP_SECRET from env."
    fi

    WORKDIR="${DINGTALK_WORKDIR:-$(pwd)}"
    read -rp "  Working directory for claude CLI [$WORKDIR]: " INPUT_WORKDIR
    WORKDIR="${INPUT_WORKDIR:-$WORKDIR}"

    cat > "$CONFIG_FILE" <<EOCFG
{
  "app_key": "$APP_KEY",
  "app_secret": "$APP_SECRET",
  "workdir": "$WORKDIR"
}
EOCFG
    chmod 600 "$CONFIG_FILE"
    echo "  Saved to $CONFIG_FILE (chmod 600)"
fi
echo

# --- 3. Data directory ---
echo "[3/4] Creating data directory..."
mkdir -p "$SKILL_DIR/data"
echo "  Done."
echo

# --- 4. Optional LaunchAgent ---
echo "[4/4] LaunchAgent setup (macOS only, optional)..."
if [[ "$(uname)" == "Darwin" ]]; then
    read -rp "  Create LaunchAgent for 24/7 bot? (y/N): " CREATE_AGENT
    if [[ "$CREATE_AGENT" =~ ^[Yy] ]]; then
        PLIST_NAME="com.dingtalk-bridge.bot"
        PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_NAME}.plist"
        PYTHON3="$(which python3)"
        BOT_SCRIPT="$SKILL_DIR/src/stream_bot.py"
        LOG_FILE="$SKILL_DIR/data/bot.log"

        cat > "$PLIST_PATH" <<EOPLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON3}</string>
        <string>-u</string>
        <string>${BOT_SCRIPT}</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${WORKDIR:-$(pwd)}</string>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${LOG_FILE}</string>
    <key>StandardErrorPath</key>
    <string>${LOG_FILE}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>
</dict>
</plist>
EOPLIST
        launchctl load "$PLIST_PATH" 2>/dev/null || true
        echo "  Created: $PLIST_PATH"
        echo "  Bot will start automatically. Log: $LOG_FILE"
        echo "  Control: launchctl start/stop $PLIST_NAME"
    else
        echo "  Skipped."
    fi
else
    echo "  Not macOS, skipped."
fi

echo
echo "=== Setup complete ==="
echo
echo "Next steps:"
echo "  1. Add the bot to a DingTalk group"
echo "  2. Start the bot:  python3 $SKILL_DIR/src/stream_bot.py"
echo "  3. @mention the bot in the group to auto-save conversation ID"
echo "  4. Send messages: python3 $SKILL_DIR/src/send.py 'Hello from Claude!'"
echo
echo "Run tests: python3 $SKILL_DIR/tests/test_dingtalk.py"
