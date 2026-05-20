---
name: kriya
aliases: [apply-fixes, materialize, review-fixes, ship]
description: Review soul discoveries (fixes, improvements, corrections) one by one, accept or discard each, implement accepted ones, build chitta, and optionally release.
execution: direct
allowed-tools: Read, Edit, Write, Bash, Glob, Grep, AskUserQuestion, mcp__chitta__*
---

# Kriya (क्रिया) — Materialise Soul Discoveries into Code

**Kriya** means "action, practice" — the applied counterpart to jnana (knowledge). Sadhanas and dreams accumulate findings; kriya turns them into shipped code.

## Usage

```
/kriya              # Review all pending fixes and improvements
/kriya --dry-run    # Show pending findings without implementing anything
/kriya --all        # Apply all without interactive review (still asks before release)
```

## How It Works

1. **Surface** — recall `[fix]`, `[solution]`, `[improvement]`, `[correction]` memories not yet tagged `[applied]`
2. **Review** — present each finding; user accepts, skips, or stops
3. **Implement** — for accepted findings, read the relevant source and apply the change
4. **Build** — `cmake --build build --parallel`
5. **Install** — stop daemon → copy binaries → daemon auto-restarts
6. **Verify** — `health_check` confirms the daemon is live
7. **Release** — ask whether to release (patch / minor / skip)
8. **Mark** — tag all applied memories `[applied]` so they don't resurface

---

## Instructions

### Step 0 — Load tools

```
ToolSearch({ query: "chitta recall smart_recall remember" })
```

### Step 1 — Surface pending findings

Call `mcp__chitta__smart_recall` with a targeted query:

```
mcp__chitta__smart_recall({
  query: "fix solution improvement correction bug gotcha",
  limit: 20
})
```

Filter the results to memories whose `tags` or `title` contain any of:
`[fix]`, `[solution]`, `[improvement]`, `[correction]`, `[gotcha]`, `[bug]`
AND do **not** contain `[applied]`.

If `--dry-run` flag: print the findings list and stop.

If no pending findings found:
> "No pending fixes found. The soul is clean. Run a sadhana or dream to surface new discoveries."
Stop.

### Step 2 — Present findings summary

Display a numbered list of all findings:
```
Pending findings (N):

  1. [fix]    daemon: ETXTBSY when copying binary while running
               File: chitta/src/simple_cli.cpp  Confidence: 92%

  2. [correction]  build order: kill daemon BEFORE cp
               File: CLAUDE.md  Confidence: 95%

  3. [improvement]  TimeoutYantra: unbounded embedding threads
               File: chitta/include/chitta/vak_timeout.hpp  Confidence: 88%
  ...
```

### Step 3 — Ask review mode

```
AskUserQuestion({
  questions: [{
    question: "Found N pending findings. How do you want to proceed?",
    header: "Review mode",
    multiSelect: false,
    options: [
      { label: "Review individually", description: "Go through each finding one by one" },
      { label: "Apply all",           description: "Accept every finding without reviewing" },
      { label: "Cancel",              description: "Exit without making changes" }
    ]
  }]
})
```

### Step 4 — Review loop (if "Review individually")

For each finding, ask:

```
AskUserQuestion({
  questions: [{
    question: "[fix] #{title}\n\n#{content}\n\nFile: #{file_ref}",
    header: "Finding #N",
    multiSelect: false,
    options: [
      { label: "Apply",  description: "Implement this fix" },
      { label: "Skip",   description: "Leave for later" },
      { label: "Stop",   description: "Stop reviewing, apply what's accepted so far" }
    ]
  }]
})
```

Collect the list of accepted findings. If "Stop" → break loop early.

If nothing was accepted: confirm and exit.

### Step 5 — Implement each accepted finding

For each accepted finding:

1. Read the cited file(s) from the memory's citation references
2. Understand the existing code
3. Apply the fix — use Edit (targeted, precise, no extra changes)
4. Log: `✓ Applied: {title}`

If a finding is ambiguous or the file doesn't exist: skip it and log `⚠ Skipped (unclear): {title}`.

### Step 6 — Build

```bash
cd /maps/projects/fernandezguerra/apps/repos/cc-soul/chitta && cmake --build build --parallel
```

If build fails:
- Show the error
- Ask:
  ```
  AskUserQuestion({
    questions: [{
      question: "Build failed. What now?",
      header: "Build error",
      options: [
        { label: "Try to fix",    description: "Attempt to fix the build error" },
        { label: "Revert all",    description: "Git checkout the changed files and abort" },
        { label: "Abort",         description: "Stop here, leave files as-is" }
      ]
    }]
  })
  ```
  - "Try to fix": diagnose and fix the compile error, then rebuild
  - "Revert all": `git checkout -- .` and stop
  - "Abort": stop, leave changes uncommitted

### Step 7 — Install

```bash
pkill -TERM chittad 2>/dev/null; sleep 1
cp /maps/projects/fernandezguerra/apps/repos/cc-soul/chitta/bin/chitta \
   /maps/projects/fernandezguerra/apps/repos/cc-soul/chitta/bin/chittad \
   ~/.claude/bin/
```

### Step 8 — Verify

```
mcp__chitta__health_check({})
```

If the daemon responds healthy: `✓ Daemon is live`
If not: wait 2 seconds and retry once. If still failing, warn but continue.

### Step 9 — Ask about release

```
AskUserQuestion({
  questions: [{
    question: "Build and install succeeded. Release a new version?",
    header: "Release",
    options: [
      { label: "Patch (x.x.+1)",  description: "Bug fixes only" },
      { label: "Minor (x.+1.0)",  description: "New features or significant changes" },
      { label: "Skip release",    description: "Keep changes local for now" }
    ]
  }]
})
```

If patch or minor:
```bash
cd /maps/projects/fernandezguerra/apps/repos/cc-soul && ./scripts/release.sh <patch|minor> -y
```

### Step 10 — Mark applied memories

For each successfully applied finding, add `[applied]` to its tags:

```
mcp__chitta__set_memory_type({ id: <id>, ... })
```

Or use `mcp__chitta__remember` to store a brief record:
```
mcp__chitta__remember({
  content: "[applied] #{title} — applied in session #{date}, released in v#{version}",
  tags: "applied,kriya,fix"
})
```

Then connect the new "applied" memory to the original finding:
```
mcp__chitta__connect_temporal({
  from: "<applied-memory-id>",
  relation: "resolves",
  to: "<original-finding-id>"
})
```

### Step 11 — Report summary

```
Kriya complete ✓

  Applied:  3 fixes
  Skipped:  1
  Build:    ✓ successful
  Daemon:   ✓ live
  Released: v3.44.0

  Fixes applied:
    ✓ daemon: ETXTBSY build order fix
    ✓ TimeoutYantra: bounded embedding threads
    ✓ socket_is_active: EACCES treated as stale
    ↷ is_pid_alive zombie detection (skipped)
```

---

## Anti-patterns

- Never skip the build step — applying a fix that doesn't compile is worse than not applying it
- Never release without a successful health_check
- Never mark `[applied]` if the build failed
- Never apply a finding to a file that hasn't been read first — always read before editing
