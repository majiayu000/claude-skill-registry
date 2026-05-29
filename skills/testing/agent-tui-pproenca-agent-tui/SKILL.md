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
| DOM persists across interactions | Screen buffer redraws constantly |
| Stable UI IDs | No stable IDs; re-snapshot frequently |
| Query once, act many times | Re-snapshot before each decision |
| Network events signal completion | Detect visual stability or text |

**The Core Insight**: agent-tui gives you vision without memory. Each screenshot is a fresh observation. Previous screenshots can become stale after any UI change.

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

1. **Take a fresh screenshot** — your previous one can be stale
2. **Re-read your target** — the screen may have shifted
3. **Verify the state** — the UI may have changed unexpectedly
4. **Act only when stable** — animations and loading states cause failures

This feels slower, but it's the only reliable approach. Optimistic reuse of stale state causes intermittent failures that are painful to debug.

## Critical Rules (Non-Negotiable)

> **RULE 1: Re-snapshot after EVERY action**
> Screens can change after any interaction. Always take a fresh screenshot before deciding again.

> **RULE 2: Never act on unstable UI**
> If the UI is animating, loading, or transitioning, `wait --stable` first. Acting during transitions causes race conditions.

> **RULE 3: Verify before claiming success**
> Use `wait "expected text" --assert` to confirm outcomes. Don't assume an action worked—prove it.

> **RULE 4: Clean up sessions**
> Always end with `agent-tui kill`. Orphaned sessions consume resources and can interfere with future runs.

## Decision Framework

### Which Screenshot Mode?

```
Need only raw text?
├─► YES: Use `screenshot` (plain text, faster)
│
└─► NO: Need machine-readable output?
    └─► Use `screenshot --json`
```

### How to Wait?

```
What are you waiting for?
│
├─► Specific text to appear
│   └─► `wait "text" --assert`
│
├─► Specific text to disappear
│   └─► `wait "text" --gone`
│
└─► UI to stop changing (animations, loading)
    └─► `wait --stable`
```

### How to Act?

```
What do you need to do?
│
├─► Type text into focused input
│   └─► `input "text"` (or `type "text"`)
│
├─► Send keyboard shortcuts/navigation
│   └─► `press Ctrl+C` or `press ArrowDown Enter`
│
└─► Scroll the viewport
    └─► `scroll down 5`
```

## Core Workflow

The canonical automation loop:

```bash
# 1. START: Launch the TUI app
agent-tui run <command> [-- args...]

# 2. OBSERVE: Get current UI state
agent-tui screenshot --format json

# 3. DECIDE: Based on text/tree, determine next action
# (This happens in your head/code)

# 4. ACT: Execute the action
agent-tui press Enter    # or input/scroll

# 5. WAIT: Synchronize with UI changes
agent-tui wait "Expected" --assert    # or wait --stable

# 6. VERIFY: Confirm the outcome (often combined with step 5)

# 7. REPEAT: Go back to step 2 until done

# 8. CLEANUP: Always clean up
agent-tui kill
```

## Anti-Patterns (What NOT to Do)

### ❌ Acting on Stale Screens

```bash
# WRONG: Acting based on old information
agent-tui screenshot --json
# ...some time passes and UI updates...
agent-tui press Enter            # ❌ Might be the wrong action now

# RIGHT: Re-snapshot before acting
agent-tui screenshot --json
agent-tui press Enter            # Now based on fresh state
```

### ❌ Acting During Animation/Loading

```bash
# WRONG: Acting immediately on dynamic UI
agent-tui run my-app
agent-tui press Enter            # ❌ Might miss or hit wrong state

# RIGHT: Wait for stability first
agent-tui run my-app
agent-tui wait --stable           # Let UI settle
agent-tui press Enter
```

### ❌ Assuming Success Without Verification

```bash
# WRONG: Assuming the action worked
agent-tui press Enter
# ...proceed as if success...     # ❌ What if it failed silently?

# RIGHT: Verify the outcome
agent-tui press Enter
agent-tui wait "Success" --assert    # ✓ Proves the action worked
```
