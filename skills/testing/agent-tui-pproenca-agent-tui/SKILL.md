---
name: agent-tui
description: >
  Drive terminal UI (TUI) applications programmatically for testing, automation, and inspection.
  Use when: automating CLI/TUI interactions, regression testing terminal apps, verifying interactive behavior, extracting structured data from terminal UIs.
  Also use when: user asks "what is agent-tui", "what does agent-tui do", "demo agent-tui", "show me agent-tui", "how does agent-tui work", or wants to see it in action.
  Do NOT use for: web browsers, GUI apps, or non-terminal interfaces—those need different tools.
---

# Terminal Automation Mastery

## Prerequisites

- **Supported OS**: macOS or Linux (Windows not supported yet).
- **Verify install**:

```bash
agent-tui --version
```

If not installed, use one of:

```bash
# Recommended: one-line install (macOS/Linux)
curl -fsSL https://raw.githubusercontent.com/pproenca/agent-tui/master/install.sh | sh
```

```bash
# Package manager
npm i -g agent-tui
pnpm add -g agent-tui
bun add -g agent-tui
```

```bash
# Build from source
cargo install --git https://github.com/pproenca/agent-tui.git --path cli/crates/agent-tui
```

If you used the install script, ensure `~/.local/bin` is on your PATH.

## Philosophy: Why Terminal Automation Is Different

Terminal UIs are **stateless from the observer's perspective**. Unlike web browsers with a persistent DOM, terminal automation works with a constantly-refreshed character grid. This fundamental difference shapes everything:

| Web Automation | Terminal Automation |
|----------------|---------------------|
| DOM persists across interactions | Screen buffer is redrawn constantly |
| Element references are stable | Element refs expire after ANY change |
| Query once, act many times | Must re-query before EVERY action |
| Network events signal completion | Must detect visual stability |

**The Core Insight**: agent-tui gives you vision without memory. Each screenshot is a fresh observation. Previous element refs mean nothing after the UI changes. This isn't a limitation—it's the nature of terminal interaction.

## Mental Model: The Feedback Loop

Think of terminal automation as a **closed-loop control system**:

```
    ┌──────────────────────────────────────────────┐
    │                                              │
    ▼                                              │
OBSERVE ──► DECIDE ──► ACT ──► WAIT ──► VERIFY ───┘
   │                                        │
   │                                        │
   └─────── NEVER skip ◄────────────────────┘
```

**Each phase is mandatory.** Skipping verification is the #1 cause of flaky automation.

### The "Fresh Eyes" Principle

Every time you need to interact with the UI:

1. **Take a fresh screenshot** — your previous one is now stale
2. **Find your target again** — element refs from before are invalid
3. **Verify the state** — the UI may have changed unexpectedly
4. **Act only when stable** — animations and loading states cause failures

This feels slower, but it's the only reliable approach. Optimistic reuse of stale state causes intermittent failures that are painful to debug.

## Critical Rules (Non-Negotiable)

> **RULE 1: Re-snapshot after EVERY action**
> Element refs (`@e1`, `@btn2`) are invalidated by any UI change. Always take a fresh screenshot before acting again.

> **RULE 2: Never act on unstable UI**
> If the UI is animating, loading, or transitioning, `wait --stable` first. Acting during transitions causes race conditions.

> **RULE 3: Verify before claiming success**
> Use `wait "expected text" --assert` to confirm outcomes. Don't assume an action worked—prove it.

> **RULE 4: Clean up sessions**
> Always end with `agent-tui kill`. Orphaned sessions consume resources and can interfere with future runs.

## Decision Framework

### Which Screenshot Mode?

```
Need to interact with specific UI elements?
├─► YES: Use `screenshot -e --json` (get element refs)
│
└─► NO: Just checking text content?
    ├─► YES: Use `screenshot` (plain text, faster)
    │
    └─► NO: Need accessibility/focus info?
        └─► YES: Use `screenshot -a --interactive-only`
```

### How to Wait?

```
What are you waiting for?
│
├─► Specific text to appear
│   └─► `wait "text" --assert` (fails if not found)
│
├─► Specific element to appear/disappear
│   ├─► Appear: `wait -e @ref --assert`
│   └─► Disappear: `wait -e @ref --gone`
│
├─► UI to stop changing (animations, loading)
│   └─► `wait --stable`
│
└─► Multiple conditions
    └─► Chain waits sequentially
```

### How to Act?

```
What do you need to do?
│
├─► Click/interact with a visible element
│   └─► `action @ref click` (or fill, select, toggle)
│
├─► Type text into focused input
│   └─► `input "text"` (or `action @ref fill "text"`)
│
├─► Send keyboard shortcuts/navigation
│   └─► `press Ctrl+C` or `press ArrowDown Enter`
│
└─► Element is off-screen
    └─► `scroll-into-view @ref` first, then re-snapshot
```

## Core Workflow

The canonical automation loop:

```bash
# 1. START: Launch the TUI app
agent-tui run <command> [-- args...]

# 2. OBSERVE: Get current UI state with element refs
agent-tui screenshot -e --format json

# 3. DECIDE: Based on elements/text, determine next action
# (This happens in your head/code)

# 4. ACT: Execute the action
agent-tui action @e1 click    # or press/input

# 5. WAIT: Synchronize with UI changes
agent-tui wait "Expected" --assert    # or wait --stable

# 6. VERIFY: Confirm the outcome (often combined with step 5)
# If verification fails, handle the error

# 7. REPEAT: Go back to step 2 until done

# 8. CLEANUP: Always clean up
agent-tui kill
```

## Anti-Patterns (What NOT to Do)

### ❌ Reusing Stale Element Refs

```bash
# WRONG: Reusing @e1 after the UI changed
agent-tui screenshot -e --json        # @e1 is "Submit" button
agent-tui action @e1 click            # Click submit
agent-tui action @e1 click            # ❌ @e1 might not exist anymore!

# RIGHT: Re-snapshot before acting again
agent-tui screenshot -e --json        # @e1 is "Submit" button
agent-tui action @e1 click            # Click submit
agent-tui wait --stable               # Wait for UI to settle
agent-tui screenshot -e --json        # Get fresh refs
agent-tui action @e2 click            # Now act on new ref
```

### ❌ Acting During Animation/Loading

```bash
# WRONG: Acting immediately on dynamic UI
agent-tui run my-app
agent-tui screenshot -e --json        # UI might still be loading!
agent-tui action @e1 click            # ❌ Might miss or hit wrong element

# RIGHT: Wait for stability first
agent-tui run my-app
agent-tui wait --stable               # Let UI settle
agent-tui screenshot -e --json        # Now it's reliable
agent-tui action @e1 click
```

### ❌ Assuming Success Without Verification

```bash
# WRONG: Assuming the click worked
agent-tui action @btn1 click
# ...proceed as if success...       # ❌ What if it failed silently?

# RIGHT: Verify the outcome
agent-tui action @btn1 click
agent-tui wait "Success" --assert    # ✓ Proves the action worked
```

### ❌ Skipping Cleanup

```bash
# WRONG: Forgetting to kill the session
agent-tui run my-app
# ...do stuff...
# script ends                        # ❌ Session left running!

# RIGHT: Always clean up
agent-tui run my-app
# ...do stuff...
agent-tui kill                       # ✓ Clean exit
```

## Before You Start: Clarify Requirements

Before automating any TUI, gather this information:

1. **Command**: What exactly to run? (`my-app --flag` or `npm start`?)
2. **Success criteria**: What text/state indicates success?
3. **Input sequence**: What keystrokes/data to enter, in what order?
4. **Safety**: Is it safe to submit forms, delete data, etc.?
5. **Auth**: Does it need login? Test credentials?
6. **Live preview**: Does the user want to watch? (`agent-tui live start --open`)

If any of these are unclear, ask before running.

## Demo Mode: Showing What agent-tui Can Do

When a user asks what agent-tui is, wants a demo, or asks "show me how it works":

1. **Don't explain—demonstrate.** Actions speak louder than words.
2. **Use the live preview** so they can watch in real-time.
3. **Run `top`**—it's universal and shows dynamic real-time updates.

For the complete demo script, see `references/demo.md`.

**Quick demo trigger phrases:**
- "What is agent-tui?" / "What does agent-tui do?"
- "Demo agent-tui" / "Show me agent-tui"
- "How does agent-tui work?" / "See it in action"

## Failure Recovery

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| "Element not found" | Stale ref or element moved | Re-snapshot, find element again |
| "Element exists but can't interact" | Element off-screen | `scroll-into-view @ref`, then re-snapshot |
| Wait times out | UI didn't reach expected state | Check screenshot, verify expectations |
| "Daemon not running" | Daemon crashed or not started | `agent-tui daemon start` |
| Unexpected layout | Wrong terminal size | `agent-tui resize --cols 120 --rows 40` |
| Session unresponsive | App crashed or hung | `agent-tui kill`, then re-run |
| Repeated failures | Something fundamentally wrong | Stop after 3-5 attempts, ask user |

## Element Selectors

Three ways to reference elements:

| Syntax | Matches | Example |
|--------|---------|---------|
| `@e1`, `@btn2` | Element ref from screenshot | `action @e1 click` |
| `@Submit`, `@"Submit Button"` | Exact text match | `action @Submit click` |
| `:Submit` | Contains text | `action :Submit click` |

**Always prefer element refs** (`@e1`) from `screenshot -e`—they're unambiguous. Use text matching only when refs aren't available.

## Self-Discovery: Use --help

You don't need to memorize every flag. The CLI is self-documenting:

```bash
agent-tui --help                     # List all commands
agent-tui run --help                 # Options for 'run'
agent-tui screenshot --help          # Options for 'screenshot'
agent-tui wait --help                # Options for 'wait'
agent-tui action --help              # Options for 'action'
```

**When in doubt, ask the CLI.** This skill teaches *when* and *why* to use commands. For exact flags and syntax, `--help` is authoritative.

## Quick Reference

```bash
# Start app
agent-tui run <cmd> [-- args]        # Launch TUI under control

# Observe
agent-tui screenshot                  # Plain text view
agent-tui screenshot -e --json        # With element refs (for actions)
agent-tui screenshot -a               # Accessibility tree

# Act
agent-tui action @e1 click            # Click element
agent-tui action @e1 fill "value"     # Fill input
agent-tui press Enter                 # Press key(s)
agent-tui press Ctrl+C                # Keyboard shortcuts
agent-tui input "text"                # Type text

# Wait/Verify
agent-tui wait "text" --assert        # Wait for text, fail if not found
agent-tui wait -e @e1 --gone          # Wait for element to disappear
agent-tui wait --stable               # Wait for UI to stop changing

# Manage
agent-tui sessions                    # List active sessions
agent-tui live start --open           # Start live preview
agent-tui kill                        # End current session
```

## Progressive Disclosure

For deeper reference material:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Demo/introduction | `references/demo.md` | User asks what agent-tui is or wants a demo |
| Full command syntax | `references/command-atlas.md` | Need specific flags/options |
| Decision flowcharts | `references/decision-tree.md` | Unsure which approach |
| Session management | `references/session-lifecycle.md` | Multiple sessions, concurrency |
| Assertion patterns | `references/assertions.md` | Complex verification needs |
| Recovery strategies | `references/recovery.md` | Debugging failures |
| JSON output schemas | `references/output-contract.md` | Parsing automation output |
| Example flows | `references/flows.md` | Need full workflow examples |
| Prompt templates | `references/prompt-templates.md` | User communication |
