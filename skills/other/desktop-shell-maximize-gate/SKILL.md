---
name: "desktop-shell-maximize-gate"
description: "How to gate maximize-state fixes in a custom desktop shell without missing restored-state regressions"
domain: "testing"
confidence: "medium"
source: "hicks-maximize-clipping-gate"
---

## Context

Use this when a desktop app owns its own chrome or hosts web UI content inside a native shell, and a bug only appears when the window is maximized.

## Pattern

1. Capture the same route in both restored and maximized states.
2. Check shell primitives first: titlebar, menu/header row, nav rail, active accent, and outer content edges.
3. Verify the maximize fix did not just hide the symptom by introducing new inset spacing or clipping elsewhere.
4. Run the state transition both ways: restored → maximized → restored.
5. End with one restored resize smoke check so edge/corner hit targets are still credible.

## Good signs

- The active navigation marker stays fully visible in maximized state.
- Shell chrome and page content sit inside the visible work area with no clipped edges.
- Restored mode looks unchanged after the maximize/restore cycle.

## Anti-patterns

- Trusting a maximized screenshot without checking the restored state afterward
- Verifying only the web content while ignoring native titlebar and resize affordances
- Approving a fix that solves clipping by adding obvious new gaps or layout drift
