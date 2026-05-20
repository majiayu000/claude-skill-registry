---
name: peekaboo
description: |
  Native macOS GUI automation via peekaboo 3.0+. AX-first hybrid with VLM fallback,
  FSM-based workflows with bug-specific transitions. Safari web automation, native app
  control, social media operations, system dialogs, cross-app workflows.
triggers:
  - native macOS app automation, system dialogs, file pickers
  - Safari web automation, form filling, JavaScript injection
  - cross-app workflows, menu navigation, clipboard operations
  - web scraping via Safari, social media operations
tools_required:
  - peekaboo CLI (brew install)
  - peekaboo-safe.sh wrapper (./scripts/)
env_optional:
  - PEEKABOO_RETINA_SCALE (default 2.0)
---

# Peekaboo

Native macOS GUI automation via peekaboo, using an AX-first hybrid approach that prioritizes accessibility-tree interaction when reliable and switches to screenshot, coordinate, JavaScript, or vision-based fallbacks when AX coverage breaks down in real apps.

Terminology used in this file:
- **AX (Accessibility tree):** The macOS accessibility hierarchy used for deterministic element discovery and interaction (`B1`, `T2`, etc.).
- **peekaboo:** The macOS automation CLI used for discovery (`see`, `image`), interaction (`click`, `type`, `hotkey`), and app/window/dialog control.
- **UI-TARS:** Vision model server used when AX discovery fails or times out on complex UIs.
- **FSM:** Finite State Machine controlling retries, transitions, and recovery paths.
- **Retina scale:** Display pixel ratio (typically `2.0`) used to map screenshot coordinates correctly on Retina displays.
- **snapshot ID:** The `snapshot_id` returned by `see`; required for stable element resolution and invalidated by UI changes.

## Setup

```bash
brew install jq
brew install --cask peekaboo
mkdir -p ./scripts
chmod +x ./scripts/peekaboo-safe.sh ./scripts/health-check.sh
./scripts/health-check.sh
```

- Grant **Accessibility** and **Screen Recording** permissions for your terminal agent host (for example, Terminal, iTerm2, Claude Code).
- Use `./scripts/peekaboo-safe.sh` as the only invocation entrypoint for peekaboo commands.
- For full setup details and troubleshooting, see `references/installation-guide.md` if present in your local skill copy.

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the peekaboo skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

---

## Quick Start

Run a 3-step baseline flow: health check, discover, interact.

```bash
# 1) Health check
./scripts/health-check.sh

# 2) Discover UI state
./scripts/peekaboo-safe.sh see --app Safari --json --path /tmp/peekaboo/

# 3) Interact
./scripts/peekaboo-safe.sh click --on B1 --app Safari
```

## Hard Rules (MUST FOLLOW)

1. **All peekaboo calls MUST use `./scripts/peekaboo-safe.sh` wrapper** - never direct `peekaboo` calls
2. **Sequential execution only** - no parallel GUI operations (causes race conditions)
3. **NEVER run `tccutil reset`** - resets ALL app permissions, not just one
4. **Always `--mode screen`** - window mode returns 698B stubs (beta3 bug)
5. **Health check required** - run `./scripts/health-check.sh` before automation
6. **Fresh snapshots mandatory** - re-run `see` before each click sequence (IDs expire)
7. **Use see --analyze for Q&A** - 50x more token-efficient than full screenshots

## Navigation Strategy: Navigate Programmatically, Interact Visually

**Core principle:** Never waste turns clicking through UI to reach a target. Get there programmatically, then use peekaboo for the last-mile interaction.

| Method | When | Example |
|--------|------|---------|
| URL scheme | System Settings, Safari pages | `open "x-apple.systempreferences:com.apple.Desktop-Settings.extension"` |
| AppleScript | Apps with scripting dictionary | `osascript -e 'tell app "Finder" to open folder "Desktop"'` |
| CLI/flags | Apps with CLI args | `open -a TextEdit /path/to/file` |
| Menu command | Navigate within already-open app | `./scripts/peekaboo-safe.sh menu click --path "View > Show Sidebar"` |
| AX sidebar click | **Last resort** - only if above fail | Unreliable for tightly-packed items (System Settings proven broken) |

**Hostile AX apps** (use URL scheme / AppleScript only):
- System Settings - SwiftUI toggles invisible to AX roles, sidebar clicks misfire

## Routing Algorithm (Interaction Tier)

```text
if target_is_native_macos_ui():
    use_ax_interaction()  # click --on B1, type, hotkey
elif target_is_swiftui_toggle():
    use_screenshot_coordinate_click()  # screenshot -> identify -> click --coords
elif target_is_web_form():
    use_safari_js_injection()  # osascript JavaScript
elif target_is_web_button():
    use_coordinate_click()  # click --coords X,Y --no-auto-focus
elif see_timeout_complex_app():
    start_ui_tars_server()  # vision provider required
elif dialog_or_sheet():
    add_no_auto_focus_flag()  # prevent focus conflicts
else:
    escalate_to_human()
```

## FSM State Machine

| State | Entry Condition | Actions | Exit Criteria | Retry Budget | Next State |
|-------|----------------|---------|---------------|--------------|------------|
| PREFLIGHT | Start | health-check.sh, mkdir /tmp/peekaboo | all_checks_pass | 1 | CLASSIFY_TARGET |
| CLASSIFY_TARGET | Health pass | Determine interaction tier | tier_identified | 1 | ACQUIRE_WINDOW |
| ACQUIRE_WINDOW | Target known | app switch, window focus | app_frontmost | 3 | WAIT_FOR_UI_STABLE |
| WAIT_FOR_UI_STABLE | Window focused | sleep, check spinner state | ui_elements_stable | 2 | DISCOVER |
| DISCOVER | UI stable | see --app --json --path | elements_found | 3 | INTERACT |
| INTERACT | Elements found | click/type/menu based on tier | action_completed | 5 | VERIFY |
| VERIFY | Action attempted | see/image for state change | success_confirmed | 2 | EXTRACT or CLEANUP |
| EXTRACT | Data needed | see --analyze or JS injection | data_extracted | 2 | CLEANUP |
| CLEANUP | Task complete | clean snapshots, restore clipboard | cleanup_done | 1 | DONE |
| RECOVER | Error detected | Retry from previous state | retry_limit_hit | 3 | HUMAN_HANDOFF or ABORT |
| HUMAN_HANDOFF | Auth/CAPTCHA/TCC | Log issue, preserve evidence | human_resolved | inf | CLASSIFY_TARGET |
| ABORT | Fatal error | Log failure, preserve evidence | - | - | - |
| DONE | Success | Return results | - | - | - |

### Bug-Specific Transitions

- `see` timeout -> start UI-TARS -> retry DISCOVER
- Safari AX click misfires -> force coordinate click path
- `type` targets URL bar -> force JS injection path
- daemon file-not-found -> `daemon run --mode manual &`
- Chrome window capture fail -> switch to Safari
- System Settings AX sidebar misfire -> use URL scheme: `open "x-apple.systempreferences:com.apple.PANE_ID"`
- SwiftUI toggle invisible to AX -> screenshot + coordinate click (not AX click)

## Core Commands (Canonical Forms Only)

### Discovery
- `./scripts/peekaboo-safe.sh see --app AppName --json --path /tmp/peekaboo/`
- `./scripts/peekaboo-safe.sh see --analyze "What is the current state?" --app AppName`
- `./scripts/peekaboo-safe.sh image --mode screen --path /tmp/peekaboo/screenshot.png`

### Interaction
- `./scripts/peekaboo-safe.sh click --on B1 --snapshot "$sid" --app AppName`
- `./scripts/peekaboo-safe.sh click --coords X,Y --no-auto-focus --app AppName`
- `./scripts/peekaboo-safe.sh type "text" --return --profile human --app AppName`
- `./scripts/peekaboo-safe.sh hotkey --keys "cmd,w" --app AppName`

### App Control
- `./scripts/peekaboo-safe.sh app switch --to AppName`
- `./scripts/peekaboo-safe.sh window focus --window-title "Title" --app AppName`
- `./scripts/peekaboo-safe.sh menu click --path "File > Save As..." --app AppName`

### Safari Workarounds
- Navigate: `./scripts/peekaboo-safe.sh open "https://url" --app Safari`
- Form fill: `osascript -e 'tell application "Safari" to do JavaScript "document.querySelector(\"input[name=field]\").value = \"value\"" in document 1'`
- Button click: `./scripts/peekaboo-safe.sh click --coords X,Y --no-auto-focus --app Safari`

### Agent Mode
- `./scripts/peekaboo-safe.sh agent "Natural language task" --model gpt-4o --max-steps 10`
- `./scripts/peekaboo-safe.sh agent --resume --max-steps 5`

## Token Budget

`see --analyze` ~100 tokens | `see --json` ~600 | `image --mode screen` ~1400. Soft limit 50 turns, hard limit 100. Prefer `see --analyze` over full AX trees. Details in `references/token-budget.md`.

## Capability Matrix

| Feature Area | Status | Last Validated | Notes |
|-------------|--------|----------------|-------|
| Native macOS UI | **validated** | 2026-02-22 | 20 tests passed, core capability |
| Agent mode | **validated** | 2026-02-22 | Multi-step automation works |
| Safari forms | **partial** | 2026-02-22 | JS injection required, see playbooks |
| System dialogs | **validated** | 2026-02-22 | Use --no-auto-focus |
| File pickers | **partial** | 2026-02-22 | Compact mode issues |
| Menu navigation | **validated** | 2026-02-22 | App menus work, Apple menu limited |
| Spaces management | **validated** | 2026-02-22 | Full virtual desktop support |
| Live capture | **validated** | 2026-02-22 | Recording and diff detection |
| Chrome automation | **unsupported** | 2026-02-22 | Issue #67, use Safari |
| Social media ops | **validated** | 2026-02-22 | Reddit shadow DOM login, Booking URL-first search, X signup, cookie extraction, CAPTCHA detection -- see playbooks |

## Playbook Index

Each playbook is a self-contained field-tested recipe. Status: validated = tested in production, experimental = untested or partially tested.

| Playbook | Use Case | Status |
|----------|----------|--------|
| `native-app-automation.md` | Any macOS app workflow | **validated** |
| `safari-login.md` | Generic web authentication | **validated** |
| `dialog-and-file-picker.md` | System dialogs, save/open | **validated** |
| `cross-app-data-transfer.md` | Clipboard transfer between apps | **validated** |
| `reddit-login.md` | Reddit auth (shadow DOM + React events) | **validated** |
| `reddit-data-extraction.md` | Post Insights extraction (author-only analytics) | **validated** |
| `booking-search.md` | Hotel search (URL-first, VLM extraction) | **validated** |
| `x-signup.md` | X/Twitter account registration + email verification | **validated** |
| `file-upload.md` | macOS file dialog from web apps (Cmd+Shift+G) | **validated** |
| `captcha-solver.md` | CAPTCHA detection and handling | **experimental** |
| `cookie-extractor.md` | Browser session cookie extraction | **experimental** |
| `instagram-monitor.md` | Instagram content monitoring | **experimental** |

## Reference Index

- `references/commands.md` - Complete command reference with all flags
- `references/safari-workarounds.md` - Web automation canonical patterns
- `references/patterns.md` - Common automation workflows and recipes
- `references/failures.md` - Error recovery procedures and symptom table
- `references/validated-tests.md` - Field validation results and capabilities
- `references/token-budget.md` - Token costs and optimization strategies
- `references/hard-tests.md` - Edge-case and stress test catalog
- `references/installation-guide.md` - Full setup from zero to working

## Pre-flight Checklist

```bash
./scripts/health-check.sh
# Must return: cli_exists=true, accessibility_granted=true, ax_test_success=true
mkdir -p /tmp/peekaboo
```

## Error Recovery

After 3 retries on same state: log state + evidence screenshot + escalate to `HUMAN_HANDOFF`. Quick recovery: `app switch` + fresh `see` + `health-check.sh`.
