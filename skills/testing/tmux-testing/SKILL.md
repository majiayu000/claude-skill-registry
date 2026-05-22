---
name: tmux-testing
description: tmux-based TUI testing for autonomous text and ANSI verification
disable-model-invocation: false
---

# tmux-Based TUI Testing

Use this skill when:
- Testing TUI components with text/ANSI verification (not pixel-level visual)
- Running CI-friendly automated TUI tests
- Fast iteration during development without rendering overhead
- Deterministic testing of keyboard navigation and state transitions
- Analyzing TUI output programmatically via ANSI escape codes

---

## Workflow Overview

This skill enables a **text-based TUI testing workflow**:

```
1. Create tmux session     →  tmux new-session -d -s test
         ↓
2. Send commands           →  tmux send-keys -t test "cmd" Enter
         ↓
3. Wait for output         →  sleep or poll for specific content
         ↓
4. Capture pane            →  tmux capture-pane -t test -p -e
         ↓
5. Analyze output          →  Parse text + ANSI codes for verification
         ↓
6. Iterate or cleanup      →  tmux kill-session -t test
```

### Key Advantages Over VHS

| Aspect | VHS (visual) | tmux (text) |
|--------|-------------|-------------|
| **Output** | PNG screenshots | Text + ANSI escape codes |
| **Visual verification** | True pixel-level | Inferred from ANSI codes |
| **Speed** | Slow (rendering) | Fast |
| **Determinism** | Medium (timing) | High |
| **CI integration** | Manual only | Fully automatable |
| **Dependencies** | vhs, ffmpeg, ttyd | tmux only |

---

## tmux Command Reference

### Session Management

```bash
# Create detached session with specific size
tmux new-session -d -s test -x 80 -y 24

# Create session and set environment variables
tmux new-session -d -s test -x 80 -y 24 \; \
    set-environment -t test MY_VAR "value"

# Kill session
tmux kill-session -t test

# List sessions (useful for debugging)
tmux list-sessions
```

### Sending Input

```bash
# Send text (without pressing Enter)
tmux send-keys -t test "invowk tui choose"

# Send text and press Enter
tmux send-keys -t test "invowk tui choose 'A' 'B' 'C'" Enter

# Send special keys
tmux send-keys -t test Down      # Arrow down
tmux send-keys -t test Up        # Arrow up
tmux send-keys -t test Left      # Arrow left
tmux send-keys -t test Right     # Arrow right
tmux send-keys -t test Enter     # Enter key
tmux send-keys -t test Space     # Space bar
tmux send-keys -t test Escape    # Escape key
tmux send-keys -t test Tab       # Tab key
tmux send-keys -t test BSpace    # Backspace

# Send control sequences
tmux send-keys -t test C-c       # Ctrl+C
tmux send-keys -t test C-d       # Ctrl+D
tmux send-keys -t test C-u       # Ctrl+U (clear line)
tmux send-keys -t test C-l       # Ctrl+L (clear screen)
```

### Capturing Output

```bash
# Capture with ANSI codes (for color/style analysis)
tmux capture-pane -t test -p -e

# Capture plain text (stripped of ANSI codes)
tmux capture-pane -t test -p

# Capture entire scrollback history
tmux capture-pane -t test -p -S -

# Capture to file
tmux capture-pane -t test -p -e > output.txt
```

### Advanced: Control Mode

For complex automation, use control mode:

```bash
# Start control mode session
tmux -C new-session -d -s test

# In control mode, responses are machine-parseable
# Useful for building test harnesses
```

---

## Shell Helper Functions

Copy these functions into your test scripts for streamlined TUI testing:

```bash
#!/bin/bash

# Configuration
TUI_SESSION_PREFIX="invowk-tui-test"
TUI_DEFAULT_WIDTH=80
TUI_DEFAULT_HEIGHT=24

# ─────────────────────────────────────────────────────────────────────────────
# tui_session_start - Create a new tmux session for TUI testing
#
# Usage: tui_session_start [session_suffix] [width] [height]
# Example: tui_session_start "choose" 100 30
# ─────────────────────────────────────────────────────────────────────────────
tui_session_start() {
    local suffix="${1:-$$}"
    local width="${2:-$TUI_DEFAULT_WIDTH}"
    local height="${3:-$TUI_DEFAULT_HEIGHT}"

    TUI_SESSION="${TUI_SESSION_PREFIX}-${suffix}"

    # Kill any existing session with this name
    tmux kill-session -t "$TUI_SESSION" 2>/dev/null || true

    # Create new detached session with specified size
    tmux new-session -d -s "$TUI_SESSION" -x "$width" -y "$height"

    # Small delay to ensure session is ready
    sleep 0.1

    echo "$TUI_SESSION"
}

# ─────────────────────────────────────────────────────────────────────────────
# tui_send - Send keys to the TUI session
#
# Usage: tui_send "text or key" [wait_ms]
# Example: tui_send "invowk tui choose 'A' 'B'"
# Example: tui_send Enter 100
# Example: tui_send Down 50
# ─────────────────────────────────────────────────────────────────────────────
tui_send() {
    local keys="$1"
    local wait_ms="${2:-0}"

    tmux send-keys -t "$TUI_SESSION" "$keys"

    if [[ "$wait_ms" -gt 0 ]]; then
        sleep "$(echo "scale=3; $wait_ms / 1000" | bc)"
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# tui_capture - Capture pane content with ANSI codes
#
# Usage: output=$(tui_capture)
# ─────────────────────────────────────────────────────────────────────────────
tui_capture() {
    tmux capture-pane -t "$TUI_SESSION" -p -e
}

# ─────────────────────────────────────────────────────────────────────────────
# tui_capture_plain - Capture pane content without ANSI codes
#
# Usage: output=$(tui_capture_plain)
# ─────────────────────────────────────────────────────────────────────────────
tui_capture_plain() {
    tmux capture-pane -t "$TUI_SESSION" -p
}

# ─────────────────────────────────────────────────────────────────────────────
# tui_wait_for - Wait until pattern appears in pane (with timeout)
#
# Usage: tui_wait_for "pattern" [timeout_seconds]
# Example: tui_wait_for ">" 5
# Returns: 0 if found, 1 if timeout
# ─────────────────────────────────────────────────────────────────────────────
tui_wait_for() {
    local pattern="$1"
    local timeout="${2:-10}"
    local elapsed=0
    local interval=0.1

    while [[ $elapsed -lt $timeout ]]; do
        if tui_capture_plain | grep -q "$pattern"; then
            return 0
        fi
        sleep "$interval"
        elapsed=$(echo "$elapsed + $interval" | bc)
    done

    echo "Timeout waiting for pattern: $pattern" >&2
    return 1
}

# ─────────────────────────────────────────────────────────────────────────────
# tui_session_end - Cleanup the TUI session
#
# Usage: tui_session_end
# ─────────────────────────────────────────────────────────────────────────────
tui_session_end() {
    if [[ -n "$TUI_SESSION" ]]; then
        tmux kill-session -t "$TUI_SESSION" 2>/dev/null || true
        unset TUI_SESSION
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# tui_assert_contains - Assert that output contains pattern
#
# Usage: tui_assert_contains "pattern" ["error message"]
# ─────────────────────────────────────────────────────────────────────────────
tui_assert_contains() {
    local pattern="$1"
    local msg="${2:-Output should contain: $pattern}"

    if ! tui_capture_plain | grep -q "$pattern"; then
        echo "FAIL: $msg" >&2
        echo "--- Captured output ---" >&2
        tui_capture_plain >&2
        echo "--- End captured output ---" >&2
        return 1
    fi
}

# ─────────────────────────────────────────────────────────────────────────────
# tui_assert_selected - Assert that an item is selected (has > indicator)
#
# Usage: tui_assert_selected "Item text"
# ─────────────────────────────────────────────────────────────────────────────
tui_assert_selected() {
    local item="$1"
    local output
    output=$(tui_capture_plain)

    # Look for "> Item" or ">Item" patterns indicating selection
    if ! echo "$output" | grep -E "^[[:space:]]*>[[:space:]]*${item}" > /dev/null; then
        echo "FAIL: Expected '$item' to be selected" >&2
        echo "--- Captured output ---" >&2
        echo "$output" >&2
        return 1
    fi
}
```

---

## Comprehensive ANSI Escape Code Reference

Claude can parse ANSI escape sequences to understand terminal styling. All sequences start with `\033[` (or `\e[` or `\x1b[`).

### Text Attributes (SGR - Select Graphic Rendition)

| Code | Meaning | Reset Code |
|------|---------|------------|
| `0` | Reset all attributes | - |
| `1` | Bold / Increased intensity | `22` |
| `2` | Dim / Decreased intensity | `22` |
| `3` | Italic | `23` |
| `4` | Underline | `24` |
| `5` | Slow blink | `25` |
| `6` | Rapid blink | `25` |
| `7` | Reverse video (swap fg/bg) | `27` |
| `8` | Hidden / Conceal | `28` |
| `9` | Strikethrough | `29` |

**Example:** `\033[1;4m` = Bold + Underline

### Standard Foreground Colors (30-37)

| Code | Color |
|------|-------|
| `30` | Black |
| `31` | Red |
| `32` | Green |
| `33` | Yellow |
| `34` | Blue |
| `35` | Magenta |
| `36` | Cyan |
| `37` | White |
| `39` | Default foreground |

### Standard Background Colors (40-47)

| Code | Color |
|------|-------|
| `40` | Black |
| `41` | Red |
| `42` | Green |
| `43` | Yellow |
| `44` | Blue |
| `45` | Magenta |
| `46` | Cyan |
| `47` | White |
| `49` | Default background |

### Bright/High-Intensity Colors

| Foreground (90-97) | Background (100-107) | Color |
|--------------------|---------------------|-------|
| `90` | `100` | Bright Black (Gray) |
| `91` | `101` | Bright Red |
| `92` | `102` | Bright Green |
| `93` | `103` | Bright Yellow |
| `94` | `104` | Bright Blue |
| `95` | `105` | Bright Magenta |
| `96` | `106` | Bright Cyan |
| `97` | `107` | Bright White |

### 256-Color Mode (8-bit)

```
Foreground: \033[38;5;Nm    (N = 0-255)
Background: \033[48;5;Nm    (N = 0-255)

Color ranges:
  0-7:     Standard colors (same as 30-37)
  8-15:    High-intensity colors (same as 90-97)
  16-231:  216 colors (6×6×6 color cube)
  232-255: Grayscale (24 shades, black to white)
```

### True Color (24-bit RGB)

```
Foreground: \033[38;2;R;G;Bm    (R, G, B = 0-255)
Background: \033[48;2;R;G;Bm    (R, G, B = 0-255)
```

**Example from invowk TUI:** `\033[38;2;97;97;97m` = Gray foreground (R=97, G=97, B=97)

### Cursor Positioning

| Code | Meaning |
|------|---------|
| `\033[H` | Move cursor to home (1,1) |
| `\033[<row>;<col>H` | Move cursor to row, col |
| `\033[<n>A` | Move cursor up n lines |
| `\033[<n>B` | Move cursor down n lines |
| `\033[<n>C` | Move cursor forward n columns |
| `\033[<n>D` | Move cursor backward n columns |
| `\033[s` | Save cursor position |
| `\033[u` | Restore cursor position |

### Screen Control

| Code | Meaning |
|------|---------|
| `\033[2J` | Clear entire screen |
| `\033[J` | Clear from cursor to end of screen |
| `\033[1J` | Clear from cursor to beginning of screen |
| `\033[2K` | Clear entire line |
| `\033[K` | Clear from cursor to end of line |
| `\033[1K` | Clear from cursor to beginning of line |

### Common Combined Sequences

| Sequence | Meaning |
|----------|---------|
| `\033[0m` | Reset all attributes |
| `\033[1;31m` | Bold red |
| `\033[1;36m` | Bold cyan (often used for selection indicator) |
| `\033[7m` | Reverse video (selected item highlight) |
| `\033[?25l` | Hide cursor |
| `\033[?25h` | Show cursor |

---

## TUI Component Testing Recipes

### Testing `invowk tui choose`

```bash
#!/bin/bash
source tui_helpers.sh  # Include helper functions above

# Setup
tui_session_start "choose-test"
trap tui_session_end EXIT

# Start the TUI
tui_send "./bin/invowk tui choose 'Apple' 'Banana' 'Cherry'"
tui_send Enter 300

# Verify initial state
tui_wait_for ">" || exit 1
tui_assert_selected "Apple"

# Navigate down
tui_send Down 100
tui_assert_selected "Banana"

# Navigate down again
tui_send Down 100
tui_assert_selected "Cherry"

# Make selection
tui_send Enter 200

# Verify output
output=$(tui_capture_plain)
if echo "$output" | grep -q "Cherry"; then
    echo "PASS: Selected Cherry"
else
    echo "FAIL: Expected Cherry in output"
    exit 1
fi

echo "All tests passed!"
```

### Testing `invowk tui filter`

```bash
#!/bin/bash
source tui_helpers.sh

tui_session_start "filter-test" 100 30
trap tui_session_end EXIT

# Start filter with options
tui_send "./bin/invowk tui filter 'apple' 'apricot' 'banana' 'blackberry' 'cherry'"
tui_send Enter 300

# Wait for TUI to render
tui_wait_for ">" || exit 1

# Verify all options visible initially
for item in apple apricot banana blackberry cherry; do
    tui_assert_contains "$item"
done

# Type filter text
tui_send "ap" 200

# Verify only matching items visible
tui_assert_contains "apple"
tui_assert_contains "apricot"

# These should NOT be visible (but grep returns 0 if found)
if tui_capture_plain | grep -q "banana"; then
    echo "FAIL: banana should be filtered out"
    exit 1
fi

echo "PASS: Filter works correctly"
```

### Testing `invowk tui confirm`

```bash
#!/bin/bash
source tui_helpers.sh

tui_session_start "confirm-test"
trap tui_session_end EXIT

# Test default (No)
tui_send "./bin/invowk tui confirm 'Proceed with operation?'"
tui_send Enter 300
tui_wait_for "No" || tui_wait_for "Yes" || exit 1

# Accept default
tui_send Enter 200

# Check result
if tui_capture_plain | grep -q "false\|no\|No"; then
    echo "PASS: Default No confirmed"
fi

echo "Test completed"
```

### Testing Multi-Select Mode

```bash
#!/bin/bash
source tui_helpers.sh

tui_session_start "multiselect-test"
trap tui_session_end EXIT

# Start multi-select
tui_send "./bin/invowk tui choose --multi 'Red' 'Green' 'Blue' 'Yellow'"
tui_send Enter 300
tui_wait_for "Red" || exit 1

# Toggle first item (Space)
tui_send Space 100

# Capture and verify checkbox state
# Look for filled checkbox indicator (varies by theme)
output=$(tui_capture)

# Navigate and toggle Blue
tui_send Down 50
tui_send Down 50
tui_send Space 100

# Confirm selection
tui_send Enter 200

# Verify output contains both selected items
output=$(tui_capture_plain)
if echo "$output" | grep -q "Red" && echo "$output" | grep -q "Blue"; then
    echo "PASS: Multi-select works"
else
    echo "FAIL: Expected Red and Blue in output"
    exit 1
fi
```

### Verifying ANSI Colors/Styling

```bash
#!/bin/bash
source tui_helpers.sh

tui_session_start "color-test"
trap tui_session_end EXIT

tui_send "./bin/invowk tui choose 'Apple' 'Banana' 'Cherry'"
tui_send Enter 300
tui_wait_for ">" || exit 1

# Capture WITH ANSI codes
output=$(tui_capture)

# Check for expected styling on selected item
# invowk typically uses RGB colors like [38;2;R;G;Bm
if echo "$output" | grep -E '\[38;2;[0-9]+;[0-9]+;[0-9]+m.*Apple' > /dev/null; then
    echo "PASS: Selected item has color styling"
else
    echo "INFO: No RGB color detected (may use different styling)"
fi

# Check for selection indicator styling
if echo "$output" | grep -E '\[1m.*>' > /dev/null || \
   echo "$output" | grep -E '>[[:space:]]*Apple' > /dev/null; then
    echo "PASS: Selection indicator present"
fi
```

---

## CI Integration Patterns

### Basic CI Test Script

```bash
#!/bin/bash
# ci-tui-tests.sh - Run TUI tests in CI environment

set -e

# Ensure tmux is available
if ! command -v tmux &> /dev/null; then
    echo "tmux is required for TUI tests"
    exit 1
fi

# Ensure binary is built
make build

# Run test suite
./tests/tui/test-choose.sh
./tests/tui/test-filter.sh
./tests/tui/test-confirm.sh

echo "All TUI tests passed"
```

### GitHub Actions Integration

```yaml
# In .github/workflows/ci.yml
jobs:
  tui-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.25'

      - name: Install tmux
        run: sudo apt-get install -y tmux

      - name: Build
        run: make build

      - name: Run TUI tests
        run: |
          chmod +x tests/tui/*.sh
          ./tests/tui/run-all.sh
```

### Parallel Test Execution

```bash
#!/bin/bash
# Run tests in parallel with unique session names

run_test() {
    local test_script="$1"
    local test_name=$(basename "$test_script" .sh)

    # Each test gets unique session via $$ or test name
    TUI_SESSION_PREFIX="invowk-ci-${test_name}" \
        bash "$test_script"
}

export -f run_test

# Run all tests in parallel
find tests/tui -name "test-*.sh" | parallel -j4 run_test {}
```

### Cleanup on Failure

```bash
#!/bin/bash
# Ensure cleanup even on test failure

cleanup_all_sessions() {
    tmux list-sessions -F "#{session_name}" 2>/dev/null | \
        grep "^invowk-" | \
        xargs -I{} tmux kill-session -t {} 2>/dev/null || true
}

# Run cleanup on script exit (success or failure)
trap cleanup_all_sessions EXIT

# Run tests...
```

---

## Common Pitfalls

### Timing/Synchronization Issues

**Problem:** Capture happens before TUI renders completely.

```bash
# BAD: May capture partial render
tui_send "./bin/invowk tui choose 'A' 'B'" Enter
output=$(tui_capture)  # Too early!

# GOOD: Wait for render
tui_send "./bin/invowk tui choose 'A' 'B'"
tui_send Enter 300  # Wait 300ms
tui_wait_for ">"    # Or poll for expected content
output=$(tui_capture)
```

**Best practices:**
- Use `tui_wait_for` to poll for expected content
- Add 100-300ms delay after sending commands
- Use longer delays (300-500ms) after starting TUI components

### Session Naming Conflicts

**Problem:** Parallel tests use same session name.

```bash
# BAD: Fixed session name conflicts in parallel runs
tui_session_start "test"

# GOOD: Include unique identifier
tui_session_start "test-$$"        # PID
tui_session_start "test-$(date +%s%N)"  # Timestamp with nanoseconds
tui_session_start "test-${RANDOM}"      # Random
```

### Terminal Size Considerations

**Problem:** TUI truncates content or wraps unexpectedly.

```bash
# BAD: Default 80x24 may be too small
tui_session_start "test"

# GOOD: Size appropriately for content
tui_session_start "test" 120 40  # Wider and taller

# For long option lists
tui_session_start "test" 100 50
```

**Recommended sizes:**
- Simple choosers: 80×24 (default)
- Filters with many options: 100×40
- Complex TUIs: 120×50

### ANSI Code Variations

**Problem:** Different terminals/themes produce different codes.

```bash
# BAD: Assumes specific color code
if echo "$output" | grep -q '\[31m'; then  # Exact red

# GOOD: Check for any color on the line
if echo "$output" | grep -E '\[[0-9;]+m.*Apple' > /dev/null; then
    echo "Apple has styling"
fi

# BETTER: Check for selection indicator semantically
if echo "$output" | grep -E '^[[:space:]]*>[[:space:]]*Apple' > /dev/null; then
    echo "Apple is selected"
fi
```

### Escape Code Parsing Edge Cases

**Problem:** Regex matches fail due to escape sequences.

```bash
# BAD: Pattern matching through escape sequences
if echo "$output" | grep "Apple"; then  # May fail if styled

# GOOD: Strip ANSI codes first for content matching
plain_output=$(echo "$output" | sed 's/\x1b\[[0-9;]*m//g')
if echo "$plain_output" | grep "Apple"; then
    echo "Found Apple"
fi

# OR: Use tui_capture_plain helper
if tui_capture_plain | grep "Apple"; then
    echo "Found Apple"
fi
```

### Leftover Sessions

**Problem:** Failed tests leave tmux sessions running.

```bash
# ALWAYS use trap for cleanup
tui_session_start "my-test"
trap tui_session_end EXIT  # Cleanup on any exit

# Run tests...

# Session will be cleaned up automatically
```

### Control Character Handling

**Problem:** Special characters in test input cause issues.

```bash
# BAD: Quote characters may cause problems
tui_send "'quoted text'"

# GOOD: Escape properly or use literals
tui_send "\"quoted text\""
tui_send "text with spaces"

# For complex strings, use a variable
input="Some 'complex' \"input\""
tui_send "$input"
```

---

## Quick Reference

### Minimal Test Template

```bash
#!/bin/bash
# test-component.sh - Brief description

set -e

# Include helpers (or inline them)
TUI_SESSION="invowk-test-$$"

cleanup() {
    tmux kill-session -t "$TUI_SESSION" 2>/dev/null || true
}
trap cleanup EXIT

# Setup
tmux new-session -d -s "$TUI_SESSION" -x 80 -y 24
sleep 0.1

# Test
tmux send-keys -t "$TUI_SESSION" "./bin/invowk tui choose 'A' 'B' 'C'" Enter
sleep 0.3

# Verify
output=$(tmux capture-pane -t "$TUI_SESSION" -p)
if echo "$output" | grep -q ">"; then
    echo "PASS: Selection indicator present"
else
    echo "FAIL: No selection indicator"
    exit 1
fi
```

### Key Commands Cheat Sheet

| Action | Command |
|--------|---------|
| Create session | `tmux new-session -d -s NAME -x W -y H` |
| Send text + Enter | `tmux send-keys -t NAME "text" Enter` |
| Send arrow key | `tmux send-keys -t NAME Down` |
| Send Ctrl+key | `tmux send-keys -t NAME C-c` |
| Capture with ANSI | `tmux capture-pane -t NAME -p -e` |
| Capture plain | `tmux capture-pane -t NAME -p` |
| Kill session | `tmux kill-session -t NAME` |

### ANSI Quick Reference

| Pattern | Meaning |
|---------|---------|
| `\033[0m` | Reset |
| `\033[1m` | Bold |
| `\033[31m` | Red |
| `\033[32m` | Green |
| `\033[36m` | Cyan |
| `\033[7m` | Reverse |
| `\033[38;2;R;G;Bm` | RGB foreground |
| `\033[48;2;R;G;Bm` | RGB background |
