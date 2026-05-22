---
name: tui-testing
description: VHS-based TUI testing workflow using .tape files for visual analysis. Use when testing invowk tui commands, verifying visual layout/colors, or debugging TUI with screenshots.
disable-model-invocation: false
---

# VHS-Based TUI Testing

Use this skill when:
- Testing interactive TUI components (`invowk tui choose`, `invowk tui filter`, etc.)
- Verifying visual layout, colors, alignment, or cursor positioning
- Testing keyboard navigation flows and multi-step interactions
- Debugging TUI issues that require visual inspection
- Creating reproducible test cases for TUI bugs

---

## Workflow Overview

This skill enables a **closed-loop TUI testing workflow**:

```
1. Write .tape file     →  Define interaction sequence + Screenshot commands
         ↓
2. Run `vhs <tape>`     →  Execute in virtual terminal, capture screenshots
         ↓
3. Read PNG files       →  Use Read tool to visually analyze TUI state
         ↓
4. Analyze & verify     →  Check layout, colors, content, cursor position
         ↓
5. Iterate if needed    →  Modify tape or fix code, repeat
```

### When to Use Each Testing Approach

| Approach | Use When | Example |
|----------|----------|---------|
| **VHS + Screenshot** | Visual verification needed (layout, colors, alignment) | Testing that filter highlights match correctly |
| **testscript (txtar)** | Text output verification | Testing that `invowk cmd hello` prints "Hello" |
| **Unit tests** | Model state transitions | Testing Bubble Tea model `Update()` logic |

## Prerequisites

VHS must be installed and available in PATH:

```bash
# Check VHS is available
vhs --version

# Install if needed (see vhs/README.md for full instructions)
go install github.com/charmbracelet/vhs@latest
```

For screenshot capture, VHS also requires `ffmpeg` and `ttyd`.

## VHS Tape Syntax Reference

### Configuration Commands

```tape
# Output settings
Output output.gif              # Primary output (GIF, MP4, or WebM)
Output output.txt              # Text capture (optional)

# Terminal settings
Set Shell "bash"               # Shell to use
Set FontSize 14                # Font size in pixels
Set Width 1280                 # Terminal width in pixels
Set Height 720                 # Terminal height in pixels
Set TypingSpeed 50ms           # Delay between keystrokes

# Window settings
Set Theme "Dracula"            # Color theme
Set Padding 20                 # Padding around terminal
```

### Input Commands

```tape
# Typing
Type "invowk tui choose"       # Type text character by character
Type@100ms "fast typing"       # Override typing speed

# Keys
Enter                          # Press Enter
Tab                            # Press Tab
Space                          # Press Space
Backspace                      # Press Backspace
Delete                         # Press Delete
Escape                         # Press Escape

# Arrow keys
Up                             # Arrow up
Down                           # Arrow down
Left                           # Arrow left
Right                          # Arrow right

# Control sequences
Ctrl+C                         # Control+C (interrupt)
Ctrl+D                         # Control+D (EOF)
Ctrl+L                         # Control+L (clear)
Ctrl+U                         # Control+U (clear line)
```

### Flow Control

```tape
# Timing
Sleep 500ms                    # Wait for specified duration
Sleep 1s                       # Supports various time units

# Screenshot capture (key for TUI testing!)
Screenshot screenshots/initial.png    # Capture current terminal state

# Hide/Show recording
Hide                           # Stop recording output
Show                           # Resume recording output
```

### Environment Setup

```tape
# Environment variables
Env MY_VAR "value"             # Set environment variable
Env HOME "/tmp/test-home"      # Override HOME for isolated testing

# Requirements
Require invowk                 # Fail if command not available
```

## Screenshot Analysis Patterns

### Placement Strategy

Place `Screenshot` commands at key points in the interaction:

```tape
Output test_output.gif
Set Shell "bash"
Set Width 800
Set Height 400

# Initial state
Type "./bin/invowk tui choose 'Option A' 'Option B' 'Option C'"
Enter
Sleep 300ms
Screenshot screenshots/initialselection01.png

# After navigation
Down
Sleep 100ms
Screenshot screenshots/afterdown02.png

# After another navigation
Down
Sleep 100ms
Screenshot screenshots/afterseconddown03.png

# Final selection
Enter
Sleep 200ms
Screenshot screenshots/finalresult04.png
```

### Naming Conventions

**Critical VHS parser limitation:** VHS tokenizes Screenshot paths at numbers followed by non-alphanumeric characters. Use **number suffixes** instead of prefixes for sequential ordering:

```
screenshots/
├── initial01.png
├── navigation02.png
├── inputentered03.png
├── filterapplied04.png
└── selectionmade05.png
```

Alternative: Use simple descriptive names without numbers:
```
screenshots/
├── initial.png
├── afterdown.png
├── filtered.png
├── selected.png
└── final.png
```

### What to Look For in Screenshots

When analyzing screenshots with the Read tool:

1. **Layout verification**
   - Are items properly aligned?
   - Is the cursor/highlight on the expected item?
   - Are borders and boxes rendering correctly?

2. **Color verification**
   - Is the selected item highlighted?
   - Are error states shown in red/warning colors?
   - Is text contrast sufficient?

3. **Content verification**
   - Are all expected options visible?
   - Is truncation happening correctly for long text?
   - Are counts/status indicators correct?

4. **State verification**
   - Does the selection indicator show the right item?
   - Are checkboxes checked/unchecked as expected?
   - Is the input prompt showing expected placeholder?

### Example Analysis Workflow

```python
# Pseudocode for the analysis loop
1. Create tape file with screenshots at key points
2. Run: vhs test.tape
3. For each screenshot:
   - Read PNG with Read tool
   - Verify expected visual state
   - Note any issues
4. If issues found:
   - Identify root cause in TUI code
   - Fix the code
   - Re-run tape to verify
```

## TUI Component Testing Recipes

### Testing `invowk tui choose`

```tape
# test-choose.tape - Test single-selection component
Output test-output/choose-test.gif

Set Shell "bash"
Set Width 800
Set Height 400
Set TypingSpeed 50ms

# Start choose component
Type "./bin/invowk tui choose 'Apple' 'Banana' 'Cherry' 'Date'"
Enter
Sleep 300ms
Screenshot screenshots/chooseinitial01.png

# Navigate down twice
Down
Sleep 100ms
Screenshot screenshots/choosefirstdown02.png

Down
Sleep 100ms
Screenshot screenshots/chooseseconddown03.png

# Select (should output "Cherry")
Enter
Sleep 200ms
Screenshot screenshots/chooseselected04.png
```

**What to verify:**
- Initial state shows "Apple" highlighted
- After each `Down`, highlight moves to next item
- Final screenshot shows "Cherry" was output

### Testing `invowk tui filter`

```tape
# test-filter.tape - Test filterable list
Output test-output/filter-test.gif

Set Shell "bash"
Set Width 800
Set Height 400

# Start filter with many options
Type "./bin/invowk tui filter 'apple' 'apricot' 'banana' 'blackberry' 'cherry'"
Enter
Sleep 300ms
Screenshot screenshots/filterinitial01.png

# Type filter text
Type "ap"
Sleep 200ms
Screenshot screenshots/filterfiltered02.png

# Clear and try different filter
Ctrl+U
Sleep 100ms
Type "berry"
Sleep 200ms
Screenshot screenshots/filterberry03.png

# Select filtered item
Enter
Sleep 200ms
Screenshot screenshots/filterselected04.png
```

**What to verify:**
- Initial state shows all 5 options
- After typing "ap", only "apple" and "apricot" visible
- After typing "berry", only "blackberry" visible
- Selection outputs correct filtered value

### Testing `invowk tui confirm`

```tape
# test-confirm.tape - Test yes/no confirmation
Output test-output/confirm-test.gif

Set Shell "bash"
Set Width 800
Set Height 300

# Default is "No" - test accepting default
Type "./bin/invowk tui confirm 'Proceed with operation?'"
Enter
Sleep 300ms
Screenshot screenshots/confirmprompt01.png

# Press Enter to accept default (No)
Enter
Sleep 200ms
Screenshot screenshots/confirmdefaultno02.png

# Now test selecting Yes
Type "./bin/invowk tui confirm 'Delete all files?'"
Enter
Sleep 300ms
Screenshot screenshots/confirmnewprompt03.png

# Navigate to Yes
Left
Sleep 100ms
Screenshot screenshots/confirmyesselected04.png

# Confirm
Enter
Sleep 200ms
Screenshot screenshots/confirmconfirmed05.png
```

### Testing Interactive Execution (`-i` flag)

```tape
# test-interactive.tape - Test interactive command execution
Output test-output/interactive-test.gif

Set Shell "bash"
Set Width 1000
Set Height 600

# Run interactive mode
Type "./bin/invowk cmd -i"
Enter
Sleep 500ms
Screenshot screenshots/interactivecmdlist01.png

# Filter commands
Type "hello"
Sleep 300ms
Screenshot screenshots/interactivefiltered02.png

# Select a command
Enter
Sleep 500ms
Screenshot screenshots/interactiveexec03.png
```

### Testing Multi-Select Mode

```tape
# test-multiselect.tape - Test checkbox selection
Output test-output/multiselect-test.gif

Set Shell "bash"
Set Width 800
Set Height 400

# Start multi-select choose
Type "./bin/invowk tui choose --multi 'Red' 'Green' 'Blue' 'Yellow'"
Enter
Sleep 300ms
Screenshot screenshots/multiinitial01.png

# Toggle first item
Space
Sleep 100ms
Screenshot screenshots/multifirst02.png

# Navigate and toggle another
Down
Down
Space
Sleep 100ms
Screenshot screenshots/multithird03.png

# Confirm selection
Enter
Sleep 200ms
Screenshot screenshots/multiresult04.png
```

## Integration with Existing Patterns

### Relationship to testscript CLI Tests

| Aspect | testscript | VHS |
|--------|------------|-----|
| **Output verification** | Text stdout/stderr | Visual terminal state |
| **CI integration** | Yes (`make test-cli`) | Manual only |
| **Speed** | Fast | Slower (renders terminal) |
| **Determinism** | High | Medium (timing-dependent) |

**Use testscript for:** Verifying command output text, exit codes, error messages.

**Use VHS for:** Visual layout bugs, interactive flow verification, debugging rendering issues.

### Relationship to Unit Tests

Unit tests verify Bubble Tea model logic without terminal rendering:

```go
// Unit test (in *_test.go)
func TestChooseModel_Navigation(t *testing.T) {
    model := NewChooseModel([]string{"a", "b", "c"})
    model, _ = model.Update(tea.KeyMsg{Type: tea.KeyDown})
    if model.cursor != 1 {
        t.Errorf("expected cursor=1, got %d", model.cursor)
    }
}
```

**Use unit tests for:** State machine logic, edge cases, error handling.

**Use VHS for:** Verifying that state changes translate to correct visual output.

### Recommended Testing Strategy

1. **First**: Write unit tests for model logic
2. **Second**: Write testscript tests for CLI output
3. **Third**: Use VHS for visual verification when needed

## Common Pitfalls

### Timing Issues

**Problem:** Screenshots capture intermediate states.

```tape
# BAD: May capture before TUI renders
Type "./bin/invowk tui choose 'A' 'B'"
Enter
Screenshot early.png  # May be blank or partial

# GOOD: Wait for render
Type "./bin/invowk tui choose 'A' 'B'"
Enter
Sleep 300ms          # Wait for full render
Screenshot good.png
```

**General timing guidelines:**
- `Sleep 300ms` after starting a TUI component
- `Sleep 100ms` after navigation (Up/Down/Left/Right)
- `Sleep 200ms` after selection/confirmation
- `Sleep 500ms` for commands that spawn processes

### Screenshot Organization

**Problem:** Screenshots scattered or overwritten.

```tape
# BAD: Overwrites same file
Screenshot output.png
Down
Screenshot output.png  # Overwrites previous!

# GOOD: Sequential naming
Screenshot screenshots/initial.png
Down
Screenshot screenshots/afterdown.png
```

**Best practice:** Create a dedicated directory for each test's screenshots.

### Environment Setup

**Problem:** Tape assumes built binary exists.

```tape
# BAD: Assumes binary location
Type "invowk tui choose ..."

# GOOD: Use explicit path and check
Require ./bin/invowk
Type "./bin/invowk tui choose ..."
```

**Before running tapes:**
```bash
make build  # Ensure binary is built
```

### Terminal Size Considerations

**Problem:** TUI truncates or wraps unexpectedly.

```tape
# BAD: Default size may truncate long items
Set Width 400
Type "./bin/invowk tui choose 'Very long option that will be truncated'"

# GOOD: Size terminal appropriately
Set Width 1000
Set Height 600
Type "./bin/invowk tui choose 'Very long option that will be truncated'"
```

**Recommended sizes:**
- Simple TUIs: 800x400
- Complex TUIs (tables, pagers): 1200x800
- Full-screen TUIs: 1920x1080

### Non-Deterministic Timing

**Problem:** Tests pass locally but fail with different timing.

**Mitigation strategies:**
1. Use generous `Sleep` values (err on the side of waiting longer)
2. For CI, consider using VHS only for demo generation, not automated testing
3. Use `Wait` command if available in newer VHS versions

## Directory Structure

When creating VHS-based TUI tests, organize files as:

```
vhs/
├── demos/           # Demo recordings for docs/website
│   └── *.tape
├── tui-tests/       # TUI testing tapes (optional)
│   ├── choose/
│   │   ├── test-basic.tape
│   │   └── screenshots/
│   ├── filter/
│   │   ├── test-filter.tape
│   │   └── screenshots/
│   └── ...
└── output/          # Generated output (gitignored)
```

## Quick Reference

### Minimal Test Tape Template

```tape
# test-<component>.tape - Brief description
Output test-output.gif

Set Shell "bash"
Set Width 800
Set Height 400
Set TypingSpeed 50ms

Require ./bin/invowk

# Test sequence
Type "./bin/invowk tui <component> <args>"
Enter
Sleep 300ms
Screenshot screenshots/initial.png

# Interaction
<navigation/input commands>
Sleep 100ms
Screenshot screenshots/afteraction.png

# Final state
Enter
Sleep 200ms
Screenshot screenshots/result.png
```

### Running Tests

```bash
# Build invowk first
make build

# Run a single tape
vhs vhs/tui-tests/choose/test-basic.tape

# Validate tape syntax without running
vhs validate vhs/tui-tests/*.tape
```

### Analyzing Screenshots

```python
# In Claude conversation:
1. Ask to read the screenshot: "Read screenshots/initial.png"
2. Describe what you see and verify against expectations
3. Note any visual issues (alignment, colors, content)
```
