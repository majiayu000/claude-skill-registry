---
name: deep-analysis
description: Deep exploration and synthesis workflow using Agent Teams with dynamic planning and hub-and-spoke coordination. Use when asked for "deep analysis", "deep understanding", "analyze codebase", "explore and analyze", or "investigate codebase".
argument-hint: <analysis-context or focus-area>
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, Task, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage, AskUserQuestion
---

# Deep Analysis Workflow

Execute a structured exploration + synthesis workflow using Agent Teams with hub-and-spoke coordination. The lead performs rapid reconnaissance to generate dynamic focus areas, composes a team plan for review, workers explore independently, and a synthesizer merges findings with Bash-powered investigation.

This skill can be invoked standalone or loaded by other skills as a reusable building block. Approval behavior is configurable via `.claude/agent-alchemy.local.md`.

## Settings Check

**Goal:** Determine whether the team plan requires user approval before execution.

1. **Read settings file:**
   - Check if `.claude/agent-alchemy.local.md` exists
   - If it exists, read it and look for a `deep-analysis` section with nested settings:
     ```markdown
     - **deep-analysis**:
       - **direct-invocation-approval**: true
       - **invocation-by-skill-approval**: false
     ```
   - If the file does not exist or is malformed, use defaults (see step 4)

2. **Determine invocation mode:**
   - **Direct invocation:** The user invoked `/deep-analysis` directly, or you are running this skill standalone
   - **Skill-invoked:** Another skill (e.g., codebase-analysis, feature-dev, docs-manager) loaded and is executing this workflow

3. **Resolve settings:**
   - If settings were found, use them as-is
   - If the file is missing or the `deep-analysis` section is absent, use defaults:
     - `direct-invocation-approval`: `true`
     - `invocation-by-skill-approval`: `false`
   - If the file exists but is malformed (unparseable), warn the user and use defaults

4. **Set `REQUIRE_APPROVAL`:**
   - If direct invocation → use `direct-invocation-approval` value (default: `true`)
   - If skill-invoked → use `invocation-by-skill-approval` value (default: `false`)

5. **Parse session settings** (also under the `deep-analysis` section):
   ```markdown
   - **deep-analysis**:
     - **cache-ttl-hours**: 24
     - **enable-checkpointing**: true
     - **enable-progress-indicators**: true
   ```
   - `cache-ttl-hours`: Number of hours before exploration cache expires. Default: `24`. Set to `0` to disable caching entirely.
   - `enable-checkpointing`: Whether to write session checkpoints at phase boundaries. Default: `true`.
   - `enable-progress-indicators`: Whether to display `[Phase N/6]` progress messages. Default: `true`.

6. **Set behavioral flags:**
   - `CACHE_TTL` = value of `cache-ttl-hours` (default: `24`)
   - `ENABLE_CHECKPOINTING` = value of `enable-checkpointing` (default: `true`)
   - `ENABLE_PROGRESS` = value of `enable-progress-indicators` (default: `true`)

---

## Phase 0: Session Setup

**Goal:** Check for cached exploration results, detect interrupted sessions, and initialize the session directory.

> Skip this phase entirely if `CACHE_TTL = 0` AND `ENABLE_CHECKPOINTING = false`.

### Step 1: Exploration Cache Check

If `CACHE_TTL > 0`:

1. Check if `.claude/sessions/exploration-cache/manifest.md` exists
2. If found, read the manifest and verify:
   - `analysis_context` matches the current analysis context (or is a superset)
   - `codebase_path` matches the current working directory
   - `timestamp` is within `CACHE_TTL` hours of now
   - Config files referenced in `config_checksum` haven't been modified since the cache was written (check mod-times of `package.json`, `tsconfig.json`, `pyproject.toml`, etc.)
3. **If cache is valid:**
   - **Skill-invoked mode:** Auto-accept the cache. Set `CACHE_HIT = true`. Read cached `synthesis.md` and `recon_summary.md`. Skip to Phase 6 step 2 (present/return results).
   - **Direct invocation:** Use `AskUserQuestion` to offer:
     - **"Use cached results"** — Set `CACHE_HIT = true`, skip to Phase 6 step 2
     - **"Refresh analysis"** — Set `CACHE_HIT = false`, proceed normally
4. **If cache is invalid or absent:** Set `CACHE_HIT = false`

### Step 2: Interrupted Session Check

If `ENABLE_CHECKPOINTING = true`:

1. Check if `.claude/sessions/__da_live__/checkpoint.md` exists
2. If found, read the checkpoint to determine `last_completed_phase`
3. Use `AskUserQuestion` to offer:
   - **"Resume from Phase [N+1]"** — Load checkpoint state, proceed from the interrupted phase (see Session Recovery in Error Handling)
   - **"Start fresh"** — Archive the interrupted session to `.claude/sessions/da-interrupted-{timestamp}/` and proceed normally
4. If not found: proceed normally

### Step 3: Initialize Session Directory

If `ENABLE_CHECKPOINTING = true` AND `CACHE_HIT = false`:

1. Create `.claude/sessions/__da_live__/` directory
2. Write `checkpoint.md`:
   ```markdown
   ## Deep Analysis Session
   - **analysis_context**: [context from arguments or caller]
   - **codebase_path**: [current working directory]
   - **started**: [ISO timestamp]
   - **current_phase**: 0
   - **status**: initialized
   ```
3. Write `progress.md`:
   ```markdown
   ## Deep Analysis Progress
   - **Phase**: 0 of 6
   - **Status**: Session initialized

   ### Phase Log
   - [timestamp] Phase 0: Session initialized
   ```

---

## Phase 1: Reconnaissance & Planning

**Goal:** Perform codebase reconnaissance, generate dynamic focus areas, and compose a team plan.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 1/6] Reconnaissance & Planning** — Mapping codebase structure..."

1. **Determine analysis context:**
   - If `$ARGUMENTS` is provided, use it as the analysis context (feature area, question, or general exploration goal)
   - If no arguments and this skill was loaded by another skill, use the calling skill's context
   - If no arguments and standalone invocation, set context to "general codebase understanding"
   - Set `PATH = current working directory`
   - Inform the user: "Exploring codebase at: `PATH`" with the analysis context

2. **Rapid codebase reconnaissance:**
   Use Glob, Grep, and Read to quickly map the codebase structure. This should take 1-2 minutes, not deep investigation.

   - **Directory structure:** List top-level directories with `Glob` (e.g., `*/` pattern) to understand the project layout
   - **Language and framework detection:** Read config files (`package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) to identify primary language(s) and framework(s)
   - **File distribution:** Use `Glob` with patterns like `src/**/*.ts`, `**/*.py` to gauge the size and shape of different areas
   - **Key documentation:** Read `README.md`, `CLAUDE.md`, or similar docs if they exist for project context
   - **For feature-focused analysis:** Use `Grep` to search for feature-related terms (function names, component names, route paths) to find hotspot directories
   - **For general analysis:** Identify the 3-5 largest or most architecturally significant directories

   **Fallback:** If reconnaissance fails (empty project, unusual structure, errors), use the static focus area templates from Step 3b.

3. **Generate dynamic focus areas:**

   Based on reconnaissance findings, create focus areas tailored to the actual codebase. Default to 3 focus areas, but adjust based on codebase size and complexity (2 for small projects, up to 4 for large ones).

   **a) Dynamic focus areas (default):**

   Each focus area should include:
   - **Label:** Short description (e.g., "API layer in src/api/")
   - **Directories:** Specific directories to explore
   - **Starting files:** 2-3 key files to read first
   - **Search terms:** Grep patterns to find related code
   - **Complexity estimate:** Low/Medium/High based on file count and apparent structure

   For feature-focused analysis, focus areas should track the feature's actual footprint:
   ```
   Example:
   Focus 1: "API routes and middleware in src/api/ and src/middleware/" (auth-related endpoints, request handling)
   Focus 2: "React components in src/pages/profile/ and src/components/user/" (UI layer for user profiles)
   Focus 3: "Data models and services in src/db/ and src/services/" (persistence and business logic)
   ```

   For general analysis, focus areas should map to the codebase's actual structure:
   ```
   Example:
   Focus 1: "Next.js app layer in apps/web/src/" (pages, components, app router)
   Focus 2: "Shared library in packages/core/src/" (utilities, types, shared logic)
   Focus 3: "CLI and tooling in packages/cli/" (commands, configuration, build)
   ```

   **b) Static fallback focus areas** (only if recon failed):

   For feature-focused analysis:
   ```
   Focus 1: Explore entry points and user-facing code related to the context
   Focus 2: Explore data models, schemas, and storage related to the context
   Focus 3: Explore utilities, helpers, and shared infrastructure
   ```

   For general codebase understanding:
   ```
   Focus 1: Explore application structure, entry points, and core logic
   Focus 2: Explore configuration, infrastructure, and shared utilities
   Focus 3: Explore shared utilities, patterns, and cross-cutting concerns
   ```

4. **Compose the team plan:**

   Assemble a structured plan document from the reconnaissance and focus area findings:

   ```markdown
   ## Team Plan: Deep Analysis

   ### Analysis Context
   [context from Step 1]

   ### Reconnaissance Summary
   - **Project:** [name/type]
   - **Primary language/framework:** [detected]
   - **Codebase size:** [file counts, key directories]
   - **Key observations:** [2-3 bullets]

   ### Focus Areas

   #### Focus Area 1: [Label]
   - **Directories:** [list]
   - **Starting files:** [2-3 files]
   - **Search patterns:** [Grep patterns]
   - **Complexity:** [Low/Medium/High]
   - **Assigned to:** explorer-1 (sonnet)

   #### Focus Area 2: [Label]
   - **Directories:** [list]
   - **Starting files:** [2-3 files]
   - **Search patterns:** [Grep patterns]
   - **Complexity:** [Low/Medium/High]
   - **Assigned to:** explorer-2 (sonnet)

   [... repeated for each focus area]

   ### Agent Composition
   | Role | Count | Model | Purpose |
   |------|-------|-------|---------|
   | Explorer | [N] | sonnet | Independent focus area exploration |
   | Synthesizer | 1 | opus | Merge findings, deep investigation |

   ### Task Dependencies
   - Exploration Tasks 1-[N]: parallel (no dependencies)
   - Synthesis Task: blocked by all exploration tasks
   ```

5. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 1`
   - Write `.claude/sessions/__da_live__/team_plan.md` with the full team plan from Step 4
   - Write `.claude/sessions/__da_live__/recon_summary.md` with reconnaissance findings from Step 2
   - Append to `progress.md`: `[timestamp] Phase 1: Reconnaissance complete — [N] focus areas identified`

---

## Phase 2: Review & Approval

**Goal:** Present the team plan for user review and approval before allocating resources.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 2/6] Review & Approval** — Presenting team plan..."

### If `REQUIRE_APPROVAL = false`

Skip to Phase 3 with a brief note: "Auto-approving team plan (skill-invoked mode). Proceeding with [N] explorers and 1 synthesizer."

### If `REQUIRE_APPROVAL = true`

1. **Present the team plan** to the user (output the plan from Phase 1 Step 4), then use `AskUserQuestion`:
   - **"Approve"** — Proceed to Phase 3 as-is
   - **"Modify"** — User describes changes (adjust focus areas, add/remove explorers, change scope)
   - **"Regenerate"** — Re-run reconnaissance with user feedback

2. **If "Modify"** (up to 3 cycles):
   - Ask what to change using `AskUserQuestion`
   - Apply modifications to the team plan (adjust focus areas, agent count, scope)
   - Re-present the updated plan for approval
   - If 3 modification cycles are exhausted, offer "Approve current plan" or "Abort analysis"

3. **If "Regenerate"** (up to 2 cycles):
   - Ask for feedback/new direction using `AskUserQuestion`
   - Return to Phase 1 Step 2 with the user's feedback incorporated
   - Re-compose and re-present the team plan
   - If 2 regeneration cycles are exhausted, offer "Approve current plan" or "Abort analysis"

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 2`, record `approval_mode` (approved/auto-approved)
   - Append to `progress.md`: `[timestamp] Phase 2: Plan approved (mode: [approval_mode])`

---

## Phase 3: Team Assembly

**Goal:** Create the team, spawn agents, create tasks, and assign work using the approved plan.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 3/6] Team Assembly** — Creating team and spawning agents..."

1. **Create the team:**
   - Use `TeamCreate` with name `deep-analysis-{timestamp}` (e.g., `deep-analysis-1707300000`)
   - Description: "Deep analysis of [analysis context]"

2. **Spawn teammates:**
   Use the Task tool with the `team_name` parameter to spawn teammates based on the approved plan:

   - **N explorers** (one per focus area) — `subagent_type: "code-explorer"`, model: sonnet
     - Named: `explorer-1`, `explorer-2`, ... `explorer-N`
     - Prompt each with: "You are part of a deep analysis team. Wait for your task assignment. The codebase is at: [PATH]. Analysis context: [context]"

   - **1 synthesizer** — `subagent_type: "code-synthesizer"`
     - Named: `synthesizer`
     - Prompt with: "You are the synthesizer for a deep analysis team. You have Bash access for git history, dependency analysis, and static analysis. Wait for your task assignment. The codebase is at: [PATH]. Analysis context: [context]"

3. **Create tasks:**
   Use `TaskCreate` for each task based on the approved plan's focus areas:

   - **Exploration Task per focus area:** Subject: "Explore: [Focus area label]", Description: detailed exploration instructions including directories, starting files, search terms, and complexity estimate
   - **Synthesis Task:** Subject: "Synthesize and evaluate exploration findings", Description: "Merge and synthesize findings from all exploration tasks into a unified analysis. Investigate gaps using Bash (git history, dependency trees). Evaluate completeness before finalizing."
     - Use `TaskUpdate` to set `addBlockedBy` pointing to all exploration task IDs

4. **Assign exploration tasks (with status guard):**

   For each exploration task, apply the following status-guarded assignment:

   1. Use `TaskGet` to check the task's current status and owner
   2. **Only assign if** status is `pending` AND owner is empty
   3. If already assigned or completed: log "Task [ID] already [status], skipping" and move on
   4. Use `TaskUpdate` to set the owner to the corresponding explorer
   5. Send the explorer a message with the task details via `SendMessage`:
      ```
      SendMessage type: "message", recipient: "[explorer-N]",
      content: "Your exploration task [ID] is assigned. Focus area: [label]. Directories: [list]. Starting files: [list]. Search patterns: [list]. Begin exploration now.",
      summary: "Exploration task assigned"
      ```

   **Never re-assign a completed or in-progress task.**

5. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 3`, record `team_name`, `explorer_names` (list), `task_ids` (map of explorer → task ID), `synthesis_task_id`
   - Append to `progress.md`: `[timestamp] Phase 3: Team assembled — [N] explorers, 1 synthesizer`

---

## Phase 4: Focused Exploration

**Goal:** Workers explore their assigned areas independently.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 4/6] Focused Exploration** — 0/[N] explorers complete"

### Monitoring Loop

After assigning exploration tasks, monitor progress with status-aware tracking:

1. When an explorer goes idle or sends a message, use `TaskGet` to check their task status
2. **If task is `completed`**: Record the explorer's findings. If `ENABLE_CHECKPOINTING = true`, write `explorer-{N}-findings.md` to `.claude/sessions/__da_live__/` and update checkpoint.
3. **If task is `in_progress`**: The explorer is still working — do NOT re-send the assignment
4. **If task is `pending` and owner is set**: The explorer received the assignment but hasn't started yet — wait, do NOT re-send
5. **If task is `pending` and owner is empty**: Assignment may have been lost — re-assign using the status guard from Phase 3 step 4

**Never re-assign a completed or in-progress task.** This is the primary duplicate prevention mechanism.

If `ENABLE_PROGRESS = true`: Update the progress display as explorers complete: "**[Phase 4/6] Focused Exploration** — [completed]/[N] explorers complete"

- Workers explore their assigned focus areas independently — no cross-worker messaging
- Workers can respond to follow-up questions from the synthesizer
- Each worker marks its task as completed when done
- You (the lead) receive idle notifications as workers finish
- **Wait for all exploration tasks to be marked complete** before proceeding to Phase 5

---

## Phase 5: Evaluation and Synthesis

**Goal:** Verify exploration completeness, launch synthesis with deep investigation.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 5/6] Synthesis** — Merging findings and investigating gaps..."

### Step 1: Structural Completeness Check

This is a structural check, not a quality assessment:

1. Use `TaskList` to verify all exploration tasks are completed
2. Check that each worker produced a report with content (review the messages/reports received)
3. **If a worker failed completely** (empty or error output):
   - Create a follow-up exploration task targeting the gap
   - Assign it to an idle worker
   - Add the new task to the synthesis task's `blockedBy` list
   - Wait for the follow-up task to complete
4. **If all produced content**: proceed immediately to Step 2

### Step 2: Launch Synthesis

1. Use `TaskUpdate` to assign the synthesis task: `owner: "synthesizer"`
2. Send the synthesizer a message with exploration context and recon findings:
   ```
   SendMessage type: "message", recipient: "synthesizer",
   content: "All exploration tasks are complete. Your synthesis task is now assigned.

   Analysis context: [analysis context]
   Codebase path: [PATH]

   Recon findings from planning phase:
   - Project structure: [brief summary of directory layout]
   - Primary language/framework: [what was detected]
   - Key areas identified: [the focus areas and why they were chosen]

   The workers are: [list of explorer names from the approved plan]. You can message them with follow-up questions if you find conflicts or gaps in their findings.

   You have Bash access for deep investigation — use it for git history analysis, dependency trees, static analysis, or any investigation that Read/Glob/Grep can't handle.

   Read the completed exploration tasks via TaskGet to access their reports, then synthesize into a unified analysis. Evaluate completeness before finalizing.",
   summary: "Synthesis task assigned, begin work"
   ```
3. Wait for the synthesizer to mark the synthesis task as completed

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 5`
   - Write `.claude/sessions/__da_live__/synthesis.md` with the synthesis results
   - Append to `progress.md`: `[timestamp] Phase 5: Synthesis complete`

---

## Phase 6: Completion + Cleanup

**Goal:** Collect results, present to user, and tear down the team.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 6/6] Completion** — Collecting results and cleaning up..."

1. **Collect synthesis output:**
   - The synthesizer's findings are in the messages it sent and/or the task completion output
   - Read the synthesis results

2. **Write exploration cache** (if `CACHE_TTL > 0`):
   - Create `.claude/sessions/exploration-cache/` directory (overwrite if exists)
   - Write `manifest.md`:
     ```markdown
     ## Exploration Cache Manifest
     - **analysis_context**: [the analysis context used]
     - **codebase_path**: [current working directory]
     - **timestamp**: [ISO timestamp]
     - **config_checksum**: [comma-separated list of config files and their mod-times]
     - **ttl_hours**: [CACHE_TTL value]
     - **explorer_count**: [N]
     ```
   - Write `synthesis.md` with the full synthesis output
   - Write `recon_summary.md` with the Phase 1 reconnaissance findings
   - Write `explorer-{N}-findings.md` for each explorer's findings (if not already persisted from Phase 4 checkpoints)

3. **Present or return results:**
   - **Standalone invocation:** Present the synthesized analysis to the user. The results remain in conversation memory for follow-up questions.
   - **Loaded by another skill:** The synthesis is complete. Control returns to the calling workflow — do not present a standalone summary.

4. **Shutdown teammates:**
   Send shutdown requests to all spawned teammates (iterate over the actual agents from the approved plan):
   ```
   SendMessage type: "shutdown_request", recipient: "explorer-1", content: "Analysis complete"
   SendMessage type: "shutdown_request", recipient: "explorer-2", content: "Analysis complete"
   [... for each explorer spawned]
   SendMessage type: "shutdown_request", recipient: "synthesizer", content: "Analysis complete"
   ```

5. **Archive session and cleanup team:**
   - If `ENABLE_CHECKPOINTING = true`: Move `.claude/sessions/__da_live__/` to `.claude/sessions/da-{timestamp}/`
   - Use `TeamDelete` to remove the team and its task list

---

## Error Handling

### Settings Check Failure
- If `.claude/agent-alchemy.local.md` exists but is malformed or the `deep-analysis` section is unparseable: warn the user ("Settings file found but could not parse deep-analysis settings — using defaults") and proceed with default approval values.

### Planning Phase Failure
- If reconnaissance fails (errors, empty results, unusual structure): fall back to static focus area templates (Step 3b)
- If the codebase appears empty: inform the user and ask how to proceed

### Approval Phase Failure
- If maximum modification cycles (3) or regeneration cycles (2) are reached without approval: use `AskUserQuestion` with options:
  - **"Approve current plan"** — Proceed with the latest version of the plan
  - **"Abort analysis"** — Cancel the analysis entirely

### Partial Worker Failure
- If one worker fails: create a follow-up task targeting the missed focus area, assign to an idle worker, add to synthesis `blockedBy`
- If two workers fail: attempt follow-ups, but if they also fail, instruct the synthesizer to work with partial results
- If all workers fail: inform the user and offer to retry or abort

### Synthesizer Failure
- If the synthesizer fails: present the raw exploration results to the user directly
- Offer to retry synthesis or let the user work with partial results

### General Failures
If any phase fails:
1. Explain what went wrong
2. Ask the user how to proceed:
   - Retry the phase
   - Continue with partial results
   - Abort the analysis

### Session Recovery

When resuming from an interrupted session (detected in Phase 0 Step 2), use the following per-phase strategy:

| Interrupted At | Recovery Strategy |
|----------------|-------------------|
| **Phase 1** | Restart from Phase 1 (reconnaissance is fast, ~1-2 min) |
| **Phase 2** | Load saved `team_plan.md` from session dir, re-present for approval |
| **Phase 3** | Load approved plan from checkpoint, restart team assembly |
| **Phase 4** | Read completed `explorer-{N}-findings.md` files from session dir. Only spawn and assign explorers whose findings files are missing. Add existing findings to synthesizer context. |
| **Phase 5** | Load all explorer findings from session dir. Spawn a fresh synthesizer and launch synthesis with the persisted findings. |
| **Phase 6** | Load `synthesis.md` from session dir. Proceed directly to present/return results and cleanup. |

**Recovery procedure:**
1. Read `checkpoint.md` to determine `last_completed_phase` and session state (team_name, explorer_names, task_ids)
2. Load any persisted artifacts from the session directory (team_plan, explorer findings, synthesis)
3. Resume from Phase `last_completed_phase + 1` using the loaded state
4. For Phase 4 recovery: compare persisted `explorer-{N}-findings.md` files against expected explorer list to determine which explorers still need to run

---

## Agent Coordination

- The lead (you) acts as the planner: performs recon, composes the team plan, handles approval, assigns work
- Workers explore independently — no cross-worker messaging (hub-and-spoke topology)
- The synthesizer can ask workers follow-up questions to resolve conflicts and fill gaps
- The synthesizer has Bash access for deep investigation (git history, dependency trees, static analysis)
- Wait for task dependencies to resolve before proceeding
- Handle agent failures gracefully — continue with partial results
- Agent count and focus area details come from the approved plan, not hardcoded values

When calling Task tool for teammates:
- Use `model: "opus"` for the synthesizer
- Use `model: "sonnet"` for workers
- Always include `team_name` parameter to join the team
