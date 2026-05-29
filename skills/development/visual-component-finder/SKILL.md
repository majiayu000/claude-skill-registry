---
name: visual-component-finder
version: 1.1.0
description: '[Frontend] Auto-activated visual-to-code component finder. Matches screenshots to Angular components with >=85% confidence using BEM classes, route paths, text content, and component selectors. Also supports index refresh/sync. Triggers on: screenshot, find component, find page, where is this, fix ui, update ui, fix screen, this page, this component, which component, locate component, visual match, find code for, match screenshot, refresh component index, update component index, sync component index, rebuild index.'
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

Find the Angular component(s) matching this screenshot: `$ARGUMENTS`

## Quick Summary

**Goal:** Match screenshots to existing Angular components in the codebase for code reuse.

**Workflow:**
1. **Analyze** — Process screenshot with vision capabilities
2. **Search** — Grep/glob for matching component patterns in frontend source directories
3. **Match** — Return component paths with similarity assessment

**Key Rules:**
- Auto-activated when user provides UI screenshots
- Search shared component library, domain libraries, and app-specific components
- Report exact component file paths and usage examples

## Prerequisites

- **MUST READ** `references/anti-hallucination-protocol.md` before any output
- **MUST READ** `references/matching-algorithm.md` for the 6-step protocol

## Workflow

### Step 1: Load Component Index

Read `docs/component-index.json`. If missing or stale, regenerate:

```bash
# Full scan — rebuild entire index from all source files
python .claude/skills/visual-component-finder/scripts/build-component-index.py

# Incremental — only re-index files changed since last commit (fast)
python .claude/skills/visual-component-finder/scripts/build-component-index.py --git-changes

# Incremental — changes since a specific branch/ref
python .claude/skills/visual-component-finder/scripts/build-component-index.py --git-changes main
```

**When to use which:**

- `--git-changes` — after pulling new code or switching branches (seconds, not minutes)
- No flag (full scan) — first-time build, or when index seems corrupted/stale

### Step 2: Analyze Screenshot

Use the Read tool on the screenshot image. Extract visual fingerprint:

- Visible text (headers, labels, button text, table columns)
- Layout pattern (sidebar+content, table, form, card grid, modal)
- URL path (if browser bar visible)
- BEM class patterns (if DevTools open)
- App identification (detect from project config, URL, or port mapping)

### Step 3: Match Components

Follow the **Signal Checklist** in `references/matching-algorithm.md`:

- Check 6 boolean signals (S1-S6) against index
- Calculate confidence from signal count
- If 0-1 signals matched, run Live Grep Fallback (Step 6)

### Step 4: Generate Component Graph

Follow `references/component-graph-template.md` to output Mermaid relationship diagram.

### Step 5: Output Results

Report with: matched component(s), confidence %, evidence per signal, file paths, relationship graph.

## Disambiguation

- Intent is to **find/modify existing** code → THIS skill
- Intent is to **create new** UI from screenshot → defer to `design-screenshot`
- Intent is to **describe** a design → defer to `design-describe`

## Workflow Positioning

When attached to bugfix/feature/refactor prompts, this skill runs **before** `/scout`.

## Important Notes

- Every match MUST cite `file:line` evidence — see anti-hallucination protocol
- Show ranked candidates when confidence <85%
- Detect reusable components (in `libs/`) and trace to page consumers
- Index covers all frontend application versions

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
