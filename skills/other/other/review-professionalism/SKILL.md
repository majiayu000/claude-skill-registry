---
name: review-professionalism
description: Review app polish — native feel, user-facing text, UX quality, and professional presentation
user-invocable: true
disable-model-invocation: true
---
Enter planning mode. Deep-review all user-facing aspects of the app for professionalism and polish. Use maximum parallelism — spawn explore agents for independent areas.

## Context

Making an AHK app feel native and professional on Windows is hard. Past reviews have surfaced valuable improvements — consistent theming, proper DPI handling, polished message boxes, etc. This review checks whether the app still feels professional as features have been added.

## What to Look For

### Visual polish
- Inconsistent fonts, sizes, or spacing across different windows/dialogs
- Controls that don't align properly or have uneven margins
- Windows that don't respect system DPI scaling
- Dark/light mode inconsistencies (see `theme.ahk` — the theme system exists, but is it applied everywhere?)
- Flash or flicker when showing/hiding windows (see `gui_antiflash.ahk`)
- Tray icon and menu looking native and consistent with Windows conventions

### User-facing text
- Typos, grammatical errors, or awkward phrasing in any user-visible string
- Inconsistent capitalization (Title Case vs Sentence case across dialogs)
- Technical jargon exposed to end users who won't understand it
- Error messages that don't tell the user what to do next
- Tooltip text that's too vague or too verbose

### UX quality of life
- Operations that block the UI without feedback (no progress indication)
- Dialogs that appear in unexpected positions (not centered on parent/monitor)
- Missing keyboard navigation (Tab order, Enter to confirm, Escape to cancel)
- Actions that can't be undone but have no confirmation prompt
- Config changes that require restart but don't tell the user

### Native Windows behavior
- Message boxes that don't use `ThemeMsgBox()` (the project's themed replacement)
- Windows that don't appear in taskbar when they should (or appear when they shouldn't)
- Improper window ownership (child dialogs that can go behind parent)
- Missing or wrong window icons
- Context menus that don't follow Windows conventions

### Installer/update experience
- Wizard steps that are confusing or have unclear choices
- Update notifications that are intrusive or poorly timed
- Elevation prompts without explanation of why admin is needed
- Error recovery that leaves the user stranded

### Config editor
- Settings descriptions that are unclear to non-technical users
- Missing validation feedback (user enters invalid value, nothing happens)
- Settings that interact but don't communicate this to the user

## Explore Strategy

Split by user-facing surface:

- **Overlay / Alt-Tab UI** — `src/gui/gui_paint.ahk`, `gui_overlay.ahk` — the main interaction surface
- **Tray menu / launcher** — `src/alt_tabby.ahk`, launcher files — first impression and daily interaction point
- **Config editor** — `src/editors/` — where users spend time customizing
- **Wizard / installation** — wizard files, setup utilities — first-run experience
- **Dialogs / message boxes** — grep for `MsgBox`, `ThemeMsgBox`, `Gui()` across all files
- **User-facing strings** — all strings shown to users (error messages, tooltips, menu items, descriptions)

## Validation

After explore agents report back, **validate every finding yourself**. "Professionalism" is subjective — what one person calls polish, another calls unnecessary complexity.

For each candidate:

1. **Cite evidence**: "I verified by reading `file.ahk` lines X–Y" with the actual user-facing text or UI code quoted.
2. **User impact**: Who sees this and when? A rough edge in the first-run wizard matters more than one in a diagnostic dialog.
3. **Counter-argument**: "What would make this fix unnecessary or counterproductive?" — Is the current behavior actually fine and the "improvement" just taste? Would the fix add complexity for minimal visual gain?
4. **Observed vs inferred**: Did you see the issue in the code, or infer it from the absence of something (e.g., "no DPI handling" — but did you check if AHK handles it automatically)?

## Plan Format

Group by user-facing area:

| Area | File | Lines | Issue | User Impact | Fix |
|------|------|-------|-------|------------|-----|
| Wizard | `launcher_wizard.ahk` | 88 | "Click OK to continue" — no explanation of what happens next | Confusing first-run | Rewrite to "This will install Alt-Tabby to Program Files and create a startup task." |
| Tray menu | `launcher_tray.ahk` | 42 | Menu item "Debug Viewer" — technical jargon | Intimidating to non-technical users | Rename to "Window Inspector" or similar |
| Config editor | `config_editor.ahk` | 200 | Setting description uses ms units without explanation | User doesn't know what 150ms means | Add "(lower = faster response)" hint |

Order by user exposure: high-traffic surfaces first (overlay, tray, config editor), rarely-seen surfaces last (wizard, error dialogs).

Ignore any existing plans — create a fresh one.
