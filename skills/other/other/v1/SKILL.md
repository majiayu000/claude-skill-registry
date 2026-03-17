---
name: start
description: "Session initialization and lifecycle management: bootstraps session context, organizes files, generates CLAUDE.md, manages soul purpose lifecycle with completion protocol and active context harvesting. Use when user says /start, /init, bootstrap session, initialize session, or organize project."
user-invocable: true
---

# Session Init & Lifecycle Skill

> Single entry point for project initialization and soul purpose lifecycle management. Two modes, auto-detected. User runs `/start` — that is all.

## Overview

This skill has two operational modes:

1. **Init Mode** — Triggered when `session-context/` does NOT exist. First-run bootstrap: captures soul purpose, organizes files, generates CLAUDE.md, integrates Claude `/init`, onboards Ralph Loop.
2. **Reconcile Mode** — Triggered when `session-context/` DOES exist. Lifecycle management: refreshes CLAUDE.md via Claude `/init`, assesses soul purpose status, optionally verifies with doubt agent, harvests active context on closure.

Mode is auto-detected from directory state. No flags, no arguments. User just runs `/start`.

---

## Hard Invariants

These hold at all times, in both modes:

1. **User authority is absolute** — AI NEVER closes a soul purpose. Only suggests; user decides.
2. **Zero unsolicited behavior** — Skill ONLY runs when user types `/start`. No hooks, no proactive triggers.
3. **Human-visible memory only** — All state lives in files. Nothing hidden in chat memory.
4. **Idempotent** — Safe to run multiple times. Re-running does not corrupt state.
5. **Templates are immutable** — NEVER edit files in `~/claude-session-init-templates/`. Copy only.
6. **Reconcile mode is audit, not rewrite** — Targeted changes only. Do not regenerate what already exists.

---

## Rules

- Act as pure bootstrap + organizer in Init Mode, pure auditor in Reconcile Mode
- All persistent state lives in files, not chat memory
- If `session-context/` files exist, do NOT overwrite unless explicitly instructed
- If project is already organized (few files at root), skip file organization steps
- **NEVER** edit template files in `~/claude-session-init-templates/` — they are immutable
- Confirm nothing except the organization map (Init Step 5) and harvest promotions (Reconcile Step 5). Execute deterministically otherwise.
- **NEVER** auto-invoke doubt agent. Only suggest it. User accepts or skips.
- **NEVER** auto-close a soul purpose. Present options; user chooses.
- All heavy file operations MUST be delegated to Task agents (see Agent-Driven Execution below)

---

## Mode Detection

```
if session-context/ does NOT exist:
    → Init Mode
else:
    → Reconcile Mode
```

Run this check silently at the start:

```bash
[ -d session-context ] && echo "MODE=reconcile" || echo "MODE=init"
```

No flags, no arguments. The directory state is the only signal.

---

### Session Context Validation

If Reconcile Mode was detected, validate `session-context/` integrity before proceeding:

```bash
# Count expected files in session-context/
for f in CLAUDE-activeContext.md CLAUDE-decisions.md CLAUDE-patterns.md CLAUDE-soul-purpose.md CLAUDE-troubleshooting.md; do
  [ -f "session-context/$f" ] && [ -s "session-context/$f" ] && echo "OK: $f" || echo "MISSING: $f"
done
```

If any files are MISSING or zero-length:
1. Check if `~/claude-session-init-templates/` exists
2. Copy missing files from templates (do NOT overwrite existing files)
3. Report to user: "Repaired X missing session-context files from templates."

This ensures Reconcile Mode always has valid files to work with, even if a previous Init was interrupted.

---

## Agent-Driven Execution (MANDATORY)

All skill operations MUST be delegated to Task agents. The main conversation thread acts as a **thin orchestrator only**.

### Why

Reading and writing large files (session-context files, CLAUDE.md, source code) directly in the main conversation causes context death spirals — compact, re-read files to restore context, fills context, compact, repeat forever. Task agents have their own context windows and do not pollute the main thread.

### Rules

1. **NEVER read files >150 lines directly in the main skill flow**
2. **Delegate ALL file reading, analysis, and editing to Task agents**
3. **Main conversation holds the plan, dispatches agents, tracks progress**
4. **Each agent gets**: specific instructions, file paths, clear edit requirements
5. **Agents return**: short summary of what changed (file, what was done)
6. **Parallel agents where dependencies allow** — e.g. populating active context and generating CLAUDE.md can run simultaneously

### Agent Dispatch Pattern — Init Mode

- **Wave 1**: Bootstrap session-context (single agent — sequential file copies)
- **Wave 2** (parallel): Populate active context + Generate CLAUDE.md
- **Wave 3**: Run Claude `/init` (must wait for CLAUDE.md to exist)
- **Wave 4**: Ralph Loop onboarding (interactive, main thread)

### Agent Dispatch Pattern — Reconcile Mode

- **Wave 1**: Run Claude `/init`
- **Wave 2**: Read soul purpose + active context (single agent)
- **Wave 3**: Self-assessment (main thread — lightweight reasoning only)
- **Wave 4** (if needed): Doubt agent verification
- **Wave 5** (if closing): Harvest agent (reads active context, proposes promotions)

### Marking Delegated Steps

Steps marked **[DELEGATE TO AGENT]** below MUST be executed via Task agents. Steps marked **[MAIN THREAD]** run directly in the orchestrator conversation.

---

## Templates

**Source**: `~/claude-session-init-templates/`

These are IMMUTABLE template files. Copy them, never edit them:
- `CLAUDE-activeContext.md` — Session state tracker
- `CLAUDE-decisions.md` — Architecture decision log
- `CLAUDE-patterns.md` — Code patterns and conventions
- `CLAUDE-soul-purpose.md` — Soul purpose placeholder
- `CLAUDE-troubleshooting.md` — Issue resolution guide
- `CLAUDE-mdReference.md` — CLAUDE.md template (rename to CLAUDE.md on copy)

---

# INIT MODE — Execution

> Triggered when `session-context/` does NOT exist.

---

### INIT STEP 1 — SOUL PURPOSE [MAIN THREAD]

Use the AskUserQuestion tool to ask:

```yaml
question: "What is the soul purpose of this project?"
header: "Purpose"
options: []
multiSelect: false
```

Store the response verbatim as `SOUL_PURPOSE`.

---

### INIT STEP 2 — DETECT ENVIRONMENT [MAIN THREAD]

Run these checks silently (do NOT report to user):

```bash
# Is this a git repo?
git rev-parse --git-dir 2>/dev/null && echo "GIT=true" || echo "GIT=false"

# Does session-context/ already exist?
[ -d session-context ] && echo "SESSION_CTX=exists" || echo "SESSION_CTX=missing"

# Does CLAUDE.md already exist?
[ -f CLAUDE.md ] && echo "CLAUDE_MD=exists" || echo "CLAUDE_MD=missing"

# Count root-level files (excluding directories, hidden files, CLAUDE.md)
ls -1p | grep -v / | grep -v "^CLAUDE" | wc -l
```

Set internal flags:
- `IS_GIT`: true/false (determines `git mv` vs `mv`)
- `HAS_SESSION_CTX`: true/false (skip bootstrap if exists)
- `HAS_CLAUDE_MD`: true/false (generate vs update)
- `ROOT_FILE_COUNT`: number (skip organization if <= 10)

---

### INIT STEP 3 — BOOTSTRAP SESSION CONTEXT [DELEGATE TO AGENT]

**Pre-flight: Validate template directory**

```bash
# Verify templates exist before copying
ls ~/claude-session-init-templates/CLAUDE-activeContext.md \
   ~/claude-session-init-templates/CLAUDE-decisions.md \
   ~/claude-session-init-templates/CLAUDE-patterns.md \
   ~/claude-session-init-templates/CLAUDE-soul-purpose.md \
   ~/claude-session-init-templates/CLAUDE-troubleshooting.md \
   ~/claude-session-init-templates/CLAUDE-mdReference.md 2>/dev/null | wc -l
```

If count is not 6, STOP and tell the user:
> "Template directory ~/claude-session-init-templates/ is missing or incomplete. Expected 6 template files. Please ensure templates are installed before running /start."

Do NOT proceed with bootstrap if templates are missing.

Dispatch a Task agent with these instructions:

**Agent task**: Create `session-context/` directory and populate with templates.

**If `session-context/` does NOT exist**:

```bash
mkdir -p session-context
```

Copy templates into `session-context/`:
```bash
cp ~/claude-session-init-templates/CLAUDE-activeContext.md session-context/
cp ~/claude-session-init-templates/CLAUDE-decisions.md session-context/
cp ~/claude-session-init-templates/CLAUDE-patterns.md session-context/
cp ~/claude-session-init-templates/CLAUDE-troubleshooting.md session-context/
cp ~/claude-session-init-templates/CLAUDE-soul-purpose.md session-context/
```

**If old CLAUDE-* files exist at root** (from previous /start runs):
Migrate them into `session-context/` instead of overwriting:
```bash
# Only move if they exist at root AND session-context/ versions don't exist
for f in CLAUDE-activeContext.md CLAUDE-decisions.md CLAUDE-patterns.md CLAUDE-troubleshooting.md CLAUDE-soul-purpose.md; do
  [ -f "$f" ] && [ ! -f "session-context/$f" ] && mv "$f" session-context/
  [ -f "$f" ] && [ -f "session-context/$f" ] && rm "$f"  # remove root copy if session-context version exists
done
```

**Write soul purpose** to `session-context/CLAUDE-soul-purpose.md`:

Open `session-context/CLAUDE-soul-purpose.md` and replace its contents with:
```markdown
# Soul Purpose

{{SOUL_PURPOSE}}
```

Ensure `SOUL_PURPOSE` is fully resolved to the user's actual text.

**VERIFY**: Run `ls session-context/` — should see 5 files.

**Agent returns**: Confirmation that 5 files exist in session-context/ and soul purpose was written.

---

### INIT STEP 4 — SCAN & CATEGORIZE [DELEGATE TO AGENT]

**Skip this step entirely if `ROOT_FILE_COUNT` <= 10** (project is already clean).

Dispatch a Task agent with these instructions:

**Agent task**: Scan all files at root level. Auto-detect categories by extension and naming. Build a proposed move map.

**Category Map**:
| Pattern | Target Directory | Subcategory Logic |
|---------|-----------------|-------------------|
| `.sh`, `.bash` | `scripts/` | By purpose: ssh/, setup/, diagnostics/, fixes/ |
| `.ps1` | `scripts/` | By purpose: ssh/, setup/, diagnostics/, network/, fixes/ |
| `.py`, `.js`, `.ts` | `scripts/` | By purpose or `src/` if app code |
| `.md` (README-*, GUIDE-*, HOW-*) | `docs/guides/` | |
| `.md` (REPORT-*, AUDIT-*, SUMMARY-*) | `docs/reports/` | |
| `.md` (QUICK-START*, SETUP-*) | `docs/quickstart/` | |
| `.md` (CONTRACT-*, FULFILLMENT-*) | `docs/contract/` | |
| `.md` (HANDOVER-*, HANDOFF-*, CLIENT-*) | `docs/handover/` | |
| `.txt` (quick-start, setup) | `docs/quickstart/` | |
| `.txt` (diagnostic, report) | `docs/reports/` | |
| `.json`, `.yaml`, `.toml` | `config/` | Unless framework-required at root |
| `.log` | `logs/` | |

**Files that ALWAYS stay at root**:
- `CLAUDE.md` (Claude Code requirement)
- `README.md` (convention)
- `LICENSE`, `LICENSE.md`
- `contract.md` (or primary SOW/spec file)
- `package.json`, `package-lock.json`, `pnpm-lock.yaml` (Node.js convention)
- `.gitignore`, `.env`, `.env.example`
- `Makefile`, `Dockerfile`, `docker-compose.yml`
- `tsconfig.json`, `vite.config.*`, `next.config.*`
- Any file the user explicitly marks as "keep at root"

**Subcategory detection for scripts**:
- Name contains `connect`, `ssh`, `remote` → `scripts/ssh/`
- Name contains `setup`, `install`, `create`, `init` → `scripts/setup/`
- Name contains `diagnose`, `analyze`, `scan`, `audit` → `scripts/diagnostics/`
- Name contains `network`, `process`, `close` → `scripts/network/`
- Name contains `fix`, `repair`, `permission` → `scripts/fixes/`
- Default → `scripts/misc/`

**Agent returns**: A move map as a data structure:
```
{
  "source_file": "target_directory",
  ...
}
```

---

### INIT STEP 5 — PROPOSE ORGANIZATION MAP [MAIN THREAD]

Present the proposed moves to the user using AskUserQuestion:

```yaml
question: "Here's the proposed file organization. [SHOW MAP AS TABLE]. Approve or edit?"
header: "Organize"
options:
  - label: "Approve"
    description: "Move all files as proposed"
  - label: "Edit"
    description: "I want to change some placements before moving"
  - label: "Skip"
    description: "Don't reorganize, just bootstrap session context"
multiSelect: false
```

**If "Edit"**: Ask which files to change, update the map, re-present.
**If "Skip"**: Jump to Init Step 7.
**If "Approve"**: Continue to Init Step 6.

---

### INIT STEP 6 — EXECUTE MOVES [DELEGATE TO AGENT]

Dispatch a Task agent with the approved move map and the `IS_GIT` flag.

**Agent task**: Create all target directories, then move files.

Create all target directories first:
```bash
# Extract unique directories from the move map and create them
mkdir -p [all unique target directories]
```

Move files using appropriate command:
- **If `IS_GIT=true` AND file is tracked**: Use `git mv source target`
- **If `IS_GIT=false` OR file is untracked**: Use `mv source target`

Execute all moves. Do NOT ask for confirmation (user already approved in Step 5).

**VERIFY**: `ls` each target directory to confirm files landed correctly.

**Agent returns**: Summary of moves executed and verification results.

---

### INIT STEP 7 — GENERATE/UPDATE CLAUDE.md [DELEGATE TO AGENT]

Dispatch a Task agent with `HAS_CLAUDE_MD` flag, `SOUL_PURPOSE`, and current directory structure.

**If `CLAUDE.md` does NOT exist**:

Copy from template and populate:
```bash
cp ~/claude-session-init-templates/CLAUDE-mdReference.md ./CLAUDE.md
```

Then fill in the `[placeholder]` sections:
- `[Project Name]` → Infer from directory name or ask user
- `[Primary objective]` → Use `SOUL_PURPOSE`
- Project Structure section → Generate from actual directory contents
- Ralph Loop Variables → Set `--completion-promise` from soul purpose context

**If `CLAUDE.md` already exists**:

Ask user (via main thread) which update approach they prefer:

```yaml
question: "CLAUDE.md exists. How should I update the path references?"
header: "Update mode"
options:
  - label: "Patch paths (Recommended)"
    description: "Find-and-replace old file paths with new locations. Preserves all content."
  - label: "Rebuild structure section"
    description: "Regenerate the Project Structure section from actual directory state. Preserves everything else."
  - label: "Skip"
    description: "Don't touch CLAUDE.md"
multiSelect: false
```

**For either update mode**, the agent MUST ensure these governance sections exist in CLAUDE.md:

**1. Project Structure** — Reflects actual directory layout

**2. Structure Maintenance Rules** — The following block MUST be present:

```markdown
## Structure Maintenance Rules

> These rules ensure the project stays organized across sessions.

- **CLAUDE.md** stays at root (Claude Code requirement)
- **Session context** files live in `session-context/` - NEVER at root
- **Scripts** (.sh, .ps1, .py, .js, .ts) go in `scripts/<category>/`
- **Documentation** (.md, .txt guides/reports) go in `docs/<category>/`
- **Config** files (.json, .yaml, .toml) go in `config/` unless framework-required at root
- **Logs** go in `logs/`
- When creating new files, place them in the correct category directory
- Do NOT dump new files at root unless they are actively being worked on
- Periodically review root for stale files and move to correct category
```

**3. Session Context Files** — References use `session-context/` prefix:
```markdown
## Session Context Files (MUST maintain)

After every session, update these files in `session-context/` with timestamp and reasoning:

- `session-context/CLAUDE-activeContext.md` - Current session state, goals, progress
- `session-context/CLAUDE-decisions.md` - Architecture decisions and rationale
- `session-context/CLAUDE-patterns.md` - Established code patterns and conventions
- `session-context/CLAUDE-troubleshooting.md` - Common issues and proven solutions
```

**4. Immutable Template Rules** — Append at bottom if not present:
```markdown
## IMMUTABLE TEMPLATE RULES

> **DO NOT** edit the template files in `~/claude-session-init-templates/`
> Templates are immutable source-of-truth. Only edit the copies in your project.
```

**5. Ralph Loop** — Add section (will be populated in Step 9):
```markdown
## Ralph Loop

**Mode**: pending
```

**Agent returns**: Confirmation that CLAUDE.md exists with all 5 governance sections.

---

### INIT STEP 8 — RUN CLAUDE'S BUILT-IN /init [MAIN THREAD]

Now that project structure exists and CLAUDE.md is in place, run Claude's built-in `/init` command.

**Why this ordering**: Claude's `/init` analyzes the codebase and enriches CLAUDE.md. Our bootstrap (Steps 1-7) creates the structure that `/init` needs to analyze. Running `/init` after bootstrap means it has meaningful content to work with.

**Before running /init**: [DELEGATE TO AGENT] Cache the current governance sections from CLAUDE.md:
- Read and store the content of: `## Structure Maintenance Rules`, `## Session Context Files`, `## IMMUTABLE TEMPLATE RULES`, `## Ralph Loop`
- This cached content is the restore source if /init removes these sections.

Execute:
```
/init
```

**After /init completes**: [DELEGATE TO AGENT] Verify governance sections are still present AND correct:
1. Check CLAUDE.md for each governance section heading
2. If any heading is missing OR its content differs from the cached version, restore from cache
3. If CLAUDE.md was completely regenerated, append all cached governance sections at the end
4. Report: "Restored X governance sections after /init refresh."

---

### INIT STEP 9 — RALPH LOOP ONBOARDING [MAIN THREAD]

This replaces the old auto-launch behavior. Explain Ralph Loop to the user, then let them choose.

**Show this explanation**:

> "Ralph Loop is an iterative execution loop that works toward your soul purpose autonomously, checking its own work with doubt agents. It's useful for complex multi-step projects where you want Claude to keep pushing forward without constant prompting."
>
> Reference: https://github.com/snarktank/ralph

Then present options using AskUserQuestion:

```yaml
question: "How would you like to configure Ralph Loop for this project?"
header: "Ralph Loop"
options:
  - label: "Automatic"
    description: "Ralph Loop launches every time /start runs"
  - label: "Manual"
    description: "Installed but only runs when you invoke it yourself"
  - label: "Skip"
    description: "Not installed. Can be added later by editing CLAUDE.md"
multiSelect: false
```

**After user chooses**: Update the `## Ralph Loop` section in CLAUDE.md:

```markdown
## Ralph Loop

**Mode**: automatic | manual | skip
```

Use the exact value the user chose (lowercase). This is done via a Task agent editing CLAUDE.md.

---

### INIT STEP 10 — LAUNCH RALPH LOOP (CONDITIONAL) [MAIN THREAD]

**If Ralph Loop mode = "automatic"**:

Extract Ralph Loop variables from CLAUDE.md:
- Goal or Mission
- Constraints
- Loop limits or stopping conditions
- Required tools or modes

If variables present, bind automatically.
If variables missing, use safe defaults inferred from `SOUL_PURPOSE`.

Immediately invoke:
```
/ralph-wiggum:ralph-loop
```

Run using:
- Extracted variables from CLAUDE.md
- `SOUL_PURPOSE` value as part of mission context
- All loaded session-context files as persistent memory

Do not explain what you are doing. Do not restate configuration. Proceed directly into Ralph Loop execution.

**If Ralph Loop mode = "manual" or "skip"**:

Report completion:

> "Session initialized. Soul purpose set. Project organized. Run `/start` again any time to check progress or manage lifecycle."

---

### STEP 11 — SEED ACTIVE CONTEXT `[DELEGATE TO AGENT]`

Write initial state to `session-context/CLAUDE-activeContext.md`:

```markdown
# Active Context

**Last Updated**: {{TODAY_DATE}}
**Current Goal**: {{SOUL_PURPOSE}}

## Current Session
- **Started**: {{TODAY_DATE}}
- **Focus**: {{SOUL_PURPOSE}}
- **Status**: Initialized

## Progress
- [x] Session initialized via /start (Init Mode)
- [ ] Begin working on soul purpose

## Notes
- Soul purpose established: {{TODAY_DATE}}
- Ralph Loop preference: {{RALPH_MODE}}
```

This ensures the first Reconcile run finds meaningful content instead of an empty template.

---

# RECONCILE MODE — Execution

> Triggered when `session-context/` already exists.

---

### RECONCILE STEP 1 — RUN CLAUDE'S BUILT-IN /init [MAIN THREAD]

Run Claude's `/init` first to refresh CLAUDE.md from the current codebase state.

**Why this ordering**: In Reconcile Mode, the codebase already exists with structure. Let `/init` refresh CLAUDE.md before we layer our governance and lifecycle checks on top.

**Before running /init**: [DELEGATE TO AGENT] Cache the current governance sections from CLAUDE.md:
- Read and store the content of: `## Structure Maintenance Rules`, `## Session Context Files`, `## IMMUTABLE TEMPLATE RULES`, `## Ralph Loop`
- This cached content is the restore source if /init removes these sections.

Execute:
```
/init
```

**After /init completes**: [DELEGATE TO AGENT] Verify governance sections are still present AND correct:
1. Check CLAUDE.md for each governance section heading
2. If any heading is missing OR its content differs from the cached version, restore from cache
3. If CLAUDE.md was completely regenerated, append all cached governance sections at the end
4. Report: "Restored X governance sections after /init refresh."

---

### RECONCILE STEP 2 — READ SOUL PURPOSE + ACTIVE CONTEXT [DELEGATE TO AGENT]

Dispatch a Task agent to read and summarize:

**Agent task**: Read the following files and return a structured summary:
- `session-context/CLAUDE-soul-purpose.md` — Extract the current soul purpose text, any [CLOSED] markers, and the active purpose
- `session-context/CLAUDE-activeContext.md` — Extract current state, open tasks, blockers, recent progress

**Agent returns**: A concise summary (no more than 30 lines) containing:
- Current soul purpose (verbatim)
- Whether any previous purposes are archived with [CLOSED]
- Open tasks / active blockers from active context
- Recent progress indicators
- Any success criteria mentioned

---

### RECONCILE STEP 3 — SELF-ASSESSMENT [MAIN THREAD]

Using ONLY the summary returned by the agent in Step 2, classify the soul purpose status. This is pure reasoning — no file reads, no agents, no extra cost.

Classify as one of:

| Classification | Criteria |
|---------------|----------|
| `clearly_incomplete` | Open tasks remain, active blockers present, success criteria not met |
| `probably_complete` | Success criteria appear met, no open TODOs, artifacts exist |
| `uncertain` | Mixed signals — some done, some unclear |

- If `clearly_incomplete` → Skip to Step 7 (Ralph Loop check). Soul purpose is clearly not done — no need to ask.
- If `probably_complete` or `uncertain` → Continue to Step 4 (doubt agent suggestion).

---

### RECONCILE STEP 4 — SUGGEST DOUBT AGENT (CONDITIONAL) [MAIN THREAD]

**This step ONLY runs for `probably_complete` or `uncertain` assessments.**

Present to the user:

> "Soul purpose appears potentially complete. Want me to run a doubt verification before we decide?"

```yaml
question: "Would you like to run a doubt agent to verify completion before deciding?"
header: "Verification"
options:
  - label: "Yes, verify"
    description: "Run doubt agent with soul purpose and current artifacts"
  - label: "No, skip"
    description: "I'll decide without verification"
multiSelect: false
```

**If "Yes, verify"**: See Doubt Agent Escalation section below for execution details.
**If "No, skip"**: Continue to Reconcile Step 5.

---

### RECONCILE STEP 5 — USER DECISION [MAIN THREAD]

**This step ONLY runs for `probably_complete` or `uncertain` assessments.** (The `clearly_incomplete` path skips directly to Step 7.)

Present the self-assessment result (and doubt agent result, if run) to the user. Then offer the decision:

```yaml
question: "Based on the assessment, what would you like to do with the current soul purpose?"
header: "Soul Purpose Lifecycle"
options:
  - label: "Close"
    description: "Mark soul purpose as complete. Harvest active context to durable files."
  - label: "Continue"
    description: "Keep working on current soul purpose. No changes."
  - label: "Redefine"
    description: "Harvest current context, then set a new soul purpose."
multiSelect: false
```

**If "Continue"**: No changes. Skip to Reconcile Step 7 (Ralph Loop check).
**If "Close"**: Run the Active Context Harvesting flow (Reconcile Step 6), then ask for optional new soul purpose.
**If "Redefine"**: Run the Active Context Harvesting flow (Reconcile Step 6), then immediately ask for new soul purpose.

---

### RECONCILE STEP 6 — HARVEST ACTIVE CONTEXT (CONDITIONAL) [DELEGATE TO AGENT]

**This step ONLY runs if user chose "Close" or "Redefine".**

See the full Active Context Harvesting section below. Dispatch a harvest agent to execute the flow.

---

### RECONCILE STEP 7 — RALPH LOOP CHECK [MAIN THREAD]

Read the `## Ralph Loop` section from CLAUDE.md (this is a small section, safe to read directly).

| Mode | Action |
|------|--------|
| `automatic` | Launch Ralph Loop immediately (same as Init Step 10) |
| `manual` | Report: "Ralph Loop is available. Invoke it manually when ready." |
| `skip` | Report: "Session reconciled. Soul purpose status checked." |
| Not found | Report: "No Ralph Loop preference set. Run `/start` on a fresh project to configure." |

---

# Self-Assessment Criteria

Used in Reconcile Step 3. The AI reads the agent's summary of `CLAUDE-soul-purpose.md` and `CLAUDE-activeContext.md` and checks:

| Signal | Assessment |
|--------|-----------|
| Open tasks remain, active blockers present | `clearly_incomplete` |
| Success criteria appear met, no open TODOs, artifacts exist | `probably_complete` |
| Mixed signals, some done / some unclear | `uncertain` |

This is pure reasoning on the agent summary. No file reads, no tool calls, no extra cost.

---

# Doubt Agent Escalation

Only triggered when user explicitly accepts verification in Reconcile Step 4.

**What to pass to the doubt agent**:
- The full soul purpose text
- Success criteria (if defined)
- Current artifacts and progress from active context summary
- The self-assessment classification and reasoning

**How to invoke**:
```
Task(subagent_type="doubt-agent", prompt="Verify whether this soul purpose is complete. Soul purpose: [text]. Success criteria: [criteria]. Current state: [summary from Step 2]. Self-assessment: [classification]. Challenge the assessment — look for gaps, untested assumptions, missing deliverables.")
```

**What to do with the result**: Present the doubt agent's findings to the user alongside the self-assessment in Reconcile Step 5. The user makes the final call.

---

# Active Context Harvesting

Triggered when user closes or redefines a soul purpose (Reconcile Step 6).

### Flow

**Early exit check**: Before dispatching the harvest agent, check if `session-context/CLAUDE-activeContext.md` is still in its template state (contains only boilerplate headings with no substantive content). If so, skip the harvest ceremony entirely:

> "No active context to harvest — working memory is empty. Proceeding with closure."

Skip directly to archiving the soul purpose and clearing active context.

Dispatch a harvest Task agent with these instructions:

**1. Read** `session-context/CLAUDE-activeContext.md` fully.

**2. Scan for durable content** in three categories:
   - **Decisions** → candidates for promotion to `session-context/CLAUDE-decisions.md`
   - **Patterns** → candidates for promotion to `session-context/CLAUDE-patterns.md`
   - **Issues solved** → candidates for promotion to `session-context/CLAUDE-troubleshooting.md`

**3. Apply Promotion Rules** (filter strictly):
   - Only promote content that is **finalized** (not provisional or speculative)
   - Decisions must have rationale (not just "we decided X")
   - Patterns must have been reused at least once
   - Troubleshooting entries must have verified solutions
   - When in doubt, leave content unharvested (user can manually promote later)

**4. Agent returns** to main thread: A structured summary of proposed promotions, organized by target file.

**5. Present proposed promotions** to the user [MAIN THREAD]:

> "I found the following durable content in active context. Here's what I propose to promote:"
>
> **To CLAUDE-decisions.md:**
> - [Decision 1 summary]
>
> **To CLAUDE-patterns.md:**
> - [Pattern 1 summary]
>
> **To CLAUDE-troubleshooting.md:**
> - [Issue 1 summary]

```yaml
question: "Approve these promotions to durable context files?"
header: "Harvest"
options:
  - label: "Approve all"
    description: "Promote all listed content"
  - label: "Edit"
    description: "I want to change what gets promoted"
  - label: "Skip"
    description: "Don't promote anything, just clear active context"
multiSelect: false
```

**6. Execute promotions** [DELEGATE TO AGENT]:
   - Append approved content to the appropriate durable files in `session-context/`
   - Clear `session-context/CLAUDE-activeContext.md` back to its template state (copy from `~/claude-session-init-templates/CLAUDE-activeContext.md`)
   - Archive the closed soul purpose: append to `session-context/CLAUDE-soul-purpose.md` with `[CLOSED]` marker and date:

```markdown
## [CLOSED] — {{date}}

{{previous soul purpose text}}
```

**7. Handle next soul purpose**:
   - **If user chose "Close"**: Ask for optional new soul purpose, or leave blank
   - **If user chose "Redefine"**: Immediately ask for new soul purpose

If a new soul purpose is provided, write it to the top of `session-context/CLAUDE-soul-purpose.md` (above the archived entries):

```markdown
# Soul Purpose

{{NEW_SOUL_PURPOSE}}

---

## [CLOSED] — {{date}}

{{previous soul purpose text}}
```

---

# Ralph Loop Onboarding

One-time onboarding during Init Mode only (Init Step 9).

### Explanation (shown to user)

> "Ralph Loop is an iterative execution loop that works toward your soul purpose autonomously, checking its own work with doubt agents. It's useful for complex multi-step projects where you want Claude to keep pushing forward without constant prompting."
>
> Reference: https://github.com/snarktank/ralph

### Options

- **Automatic** — Ralph Loop launches every time `/start` runs
- **Manual** — Installed but only runs when you invoke it yourself
- **Skip** — Not installed. Can be added later by editing CLAUDE.md.

### Persistence

Choice saved to CLAUDE.md under a `## Ralph Loop` section:

```markdown
## Ralph Loop

**Mode**: automatic | manual | skip
```

On Reconcile Mode, the skill reads this preference and acts accordingly. No re-asking. User edits CLAUDE.md directly to change preference.

---

# Claude /init Integration

### Why

Claude's built-in `/init` command analyzes the codebase and generates/updates CLAUDE.md. Our skill layers governance (session-context, soul purpose, lifecycle rules) on top of what `/init` produces.

### Ordering Logic

| Mode | Order | Reason |
|------|-------|--------|
| Init | Our bootstrap THEN `/init` | `/init` needs structure to analyze. Our bootstrap creates that structure first. |
| Reconcile | `/init` first THEN our reconciliation | Codebase already exists. Let `/init` refresh CLAUDE.md before we layer governance. |

### Implementation Notes

- The skill invokes Claude's `/init` as a step in its flow
- The `/init` output enriches CLAUDE.md with codebase-aware content
- After `/init` runs, the skill verifies that all 5 governance sections are still present:
  1. Project Structure
  2. Structure Maintenance Rules
  3. Session Context Files
  4. Immutable Template Rules
  5. Ralph Loop
- If `/init` removed or overwrote any governance section, restore it via a Task agent
- This is a defensive check — `/init` may regenerate CLAUDE.md entirely
