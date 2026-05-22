---
name: sketch-devtools-qa
description: Chrome DevTools QA workflow for the Sketch Magic kid-first UI. Use when validating Console/Network/Performance, investigating “tap doesn’t work”, /api/convert failures, mobile touch issues, or when a proof video must be backed by DevTools evidence.
---

# Sketch DevTools QA

## Overview
Run a repeatable DevTools QA pass for the upload → prompt → convert → result flow, with explicit log review and kid-first UX checks.

## Quick Start
1. Start the dev server and open Chrome DevTools.
2. Enable **Preserve log** + **Log XMLHttpRequests** in Console.
3. Run through the full flow (upload → prompt → convert → result).
4. Record findings using the checklists in `references/`.

## Workflow (required)

### 1) DevTools setup
- Console: enable **Preserve log** and **Group similar**.
- Network: filter by `/api/convert` and check for 4xx/5xx.
- Performance: verify no frozen UI during convert.

### 2) Happy-path run
- Use a real upload or sample.
- Confirm Convert starts loading within ~300ms.
- Confirm result image renders and download works.

### 3) Log review
- Dev server logs: tail or use `pnpm dev:logs` if available.
- Confirm **no server errors** and **no console errors**.

### 4) Kid-first UX pass
- Validate tap targets, spacing, readability, and motion at 320/390 widths.
- Use the kid-first checklist from `references/ux-qa-checklist.md`.

### 5) Report outcome
- If any error exists (Console, Network, or logs), **do not claim done**.
- Create follow-up issues for any UX or stability gaps.
- Use `qa-verification` for the standard evidence format.

## References
- `references/devtools-checklist.md` — Console/Network/Performance QA list + log rubric.
- `references/ux-qa-checklist.md` — Kid-first UX checklist (tap targets, motion, copy).
