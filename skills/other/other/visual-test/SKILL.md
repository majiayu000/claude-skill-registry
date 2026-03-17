---
name: visual-test
description: Visual iteration workflow for Script Kit GPUI. Use when making UI changes that need visual verification — focus indicators, colors, layout, shadows, spacing. Covers the named-pipe test pattern, captureWindow screenshots, and the build-capture-verify loop.
---

# Visual Test Workflow

Iterating on visual UI changes requires a tight feedback loop: change code, build, capture screenshots, read the PNGs to verify, adjust, repeat. This skill documents the proven pattern using named pipes and stdin JSON commands.

## Core Loop

1. Edit the Rust UI code
2. `cargo build`
3. Run a shell test script that drives the app via stdin JSON
4. Read the resulting PNG screenshots to visually verify
5. Adjust and repeat from step 1

## Named Pipe Pattern

The app reads JSON commands from stdin. To send multiple commands over time, use a **named pipe with a persistent file descriptor**. This is the critical technique — without it the pipe closes after the first write and the app exits.

```bash
# Create named pipe
PIPE=$(mktemp -u)
mkfifo "$PIPE"

# Start app reading from pipe, log output to file
./target/debug/script-kit-gpui < "$PIPE" > /tmp/sk-test-stdout.log 2>&1 &
APP_PID=$!

# Keep pipe open with a persistent file descriptor
exec 3>"$PIPE"

# Now send commands via fd 3
echo '{"type":"show"}' >&3
sleep 1
echo '{"type":"setFilter","text":"hello"}' >&3
sleep 1

# Clean up
exec 3>&-          # Close fd
rm -f "$PIPE"
kill $APP_PID 2>/dev/null || true
wait $APP_PID 2>/dev/null || true
```

**Why `exec 3>"$PIPE"`?** Each `echo > "$PIPE"` opens and closes the pipe, sending EOF to the reader. Using `exec 3>"$PIPE"` keeps the write end open so the app continues reading.

## Capturing Screenshots

Use the `captureWindow` stdin command. The `path` must be an **absolute path**.

```bash
SCREENSHOT_DIR="test-screenshots"
mkdir -p "$SCREENSHOT_DIR"

echo '{"type":"captureWindow","title":"","path":"'"$(pwd)/$SCREENSHOT_DIR"'/my-screenshot.png"}' >&3
sleep 1
```

- `title` is a substring match on the window title. Use `""` to match any window.
- The capture skips windows smaller than 100x100 (filters out tray icons).
- Always `sleep 1` after capture to let the file write complete.

**After capturing, read the PNG file** to visually verify the result. Never assume the screenshot looks correct without checking.

## SimulateKey for Keyboard Testing

```bash
# Tab
echo '{"type":"simulateKey","key":"tab","modifiers":[]}' >&3

# Shift+Tab
echo '{"type":"simulateKey","key":"tab","modifiers":["shift"]}' >&3

# Arrow keys
echo '{"type":"simulateKey","key":"down","modifiers":[]}' >&3
echo '{"type":"simulateKey","key":"up","modifiers":[]}' >&3

# Enter
echo '{"type":"simulateKey","key":"enter","modifiers":[]}' >&3

# Escape
echo '{"type":"simulateKey","key":"escape","modifiers":[]}' >&3

# Cmd+K
echo '{"type":"simulateKey","key":"k","modifiers":["cmd"]}' >&3
```

Allow `sleep 0.5` between key simulation and screenshot capture so the UI updates.

## Environment Setup

```bash
# Unset API keys to force setup card to appear
unset VERCEL_AI_GATEWAY_API_KEY
unset ANTHROPIC_API_KEY
unset OPENAI_API_KEY

# Enable compact logging
export SCRIPT_KIT_AI_LOG=1
```

## Complete Test Script Template

```bash
#!/bin/bash
# Visual test: [description]
# Usage: ./tests/smoke/test-[name].sh
# Screenshots: test-screenshots/[prefix]-*.png

set -e
cd "$(dirname "$0")/../.."

SCREENSHOT_DIR="test-screenshots"
mkdir -p "$SCREENSHOT_DIR"
rm -f "$SCREENSHOT_DIR"/[prefix]-*.png

echo "[TEST] Building app..."
cargo build 2>&1 | tail -3

PIPE=$(mktemp -u)
mkfifo "$PIPE"

# Environment for the test
unset VERCEL_AI_GATEWAY_API_KEY
unset ANTHROPIC_API_KEY
unset OPENAI_API_KEY
export SCRIPT_KIT_AI_LOG=1

./target/debug/script-kit-gpui < "$PIPE" > /tmp/sk-test-stdout.log 2>&1 &
APP_PID=$!
exec 3>"$PIPE"

sleep 3  # App startup

echo '{"type":"show"}' >&3
sleep 1

# --- Test steps: interact then capture ---

echo "[TEST] Step 1: [action]..."
echo '{"type":"simulateKey","key":"tab","modifiers":[]}' >&3
sleep 0.5

echo "[TEST] Capturing step 1..."
echo '{"type":"captureWindow","title":"","path":"'"$(pwd)/$SCREENSHOT_DIR"'/[prefix]-1.png"}' >&3
sleep 1

# --- Cleanup ---

exec 3>&-
rm -f "$PIPE"
kill $APP_PID 2>/dev/null || true
wait $APP_PID 2>/dev/null || true

echo "[TEST] Screenshots saved to $SCREENSHOT_DIR/:"
ls -la "$SCREENSHOT_DIR"/[prefix]-*.png 2>/dev/null || echo "  (none)"
```

## Timing Guidelines

| Action | Sleep after |
|--------|------------|
| App startup | 3s |
| `show` window | 1s |
| `setFilter` | 1s |
| `simulateKey` (Tab opens new view) | 1.5s |
| `simulateKey` (focus change) | 0.5s |
| `captureWindow` | 1s |

## Gotchas

- **App starts hidden.** Always send `{"type":"show"}` first.
- **`setFilter` + Tab triggers inline AI chat.** The filter must be non-empty for Tab to transition from ScriptList to ChatPrompt.
- **SimulateKey does NOT go through GPUI's event system.** It dispatches directly via `handle_setup_key` / view update logic in `main.rs`. If a new key isn't handled, check the `SimulateKey` dispatch in `main.rs`.
- **captureWindow matches by window title substring.** An empty `""` matches any window. Windows under 100x100 are automatically filtered.
- **Log output goes to file, not terminal.** Check `/tmp/sk-test-stdout.log` if the app fails silently.
- **Tab interception.** GPUI's built-in Tab focus traversal must be intercepted in `cx.intercept_keystrokes()` (in `app_impl.rs`) to prevent it from consuming Tab before custom handlers fire.

## Existing Tests

| Test | What it covers |
|------|---------------|
| `tests/smoke/test-setup-card-focus.sh` | Setup card focus indicators, Tab/Shift+Tab/Arrow navigation between buttons |

## Anti-Patterns

- **Not reading the PNG after capture** — Always visually verify by reading the screenshot file
- **Using `echo > "$PIPE"` without `exec 3>`** — Pipe closes after one write, app exits
- **Forgetting `{"type":"show"}`** — App window stays hidden, screenshots are blank or missing
- **Hardcoding relative paths in `captureWindow`** — Path must be absolute; use `$(pwd)/` prefix
- **Not unsetting API keys** — Setup card won't appear if any provider key is set
- **Using system screenshot tools** — `screencapture`, `scrot`, etc. are blocked; use `captureWindow`
