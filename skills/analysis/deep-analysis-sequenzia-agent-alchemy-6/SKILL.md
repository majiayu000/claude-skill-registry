---
name: deep-analysis
description: Deep exploration and synthesis workflow using agent teams with dynamic planning and hub-and-spoke coordination. Use when asked for "deep analysis", "deep understanding", "analyze codebase", "explore and analyze", or "investigate codebase".
dependencies: []
---

# Deep Analysis Workflow

Execute a structured exploration + synthesis workflow using agent teams with hub-and-spoke coordination. The lead performs rapid reconnaissance to generate dynamic focus areas, composes a team plan for review, workers explore independently, and a synthesizer merges findings with deep investigation.

This skill can be invoked standalone or loaded by other skills as a reusable building block. Approval behavior is configurable.

## Settings Check

**Goal:** Determine whether the team plan requires user approval before execution.

1. **Read settings file:**
   - Check if a configuration file exists for the project
   - If it exists, look for a `deep-analysis` section with these settings:
     - `direct-invocation-approval`: Whether to require approval when invoked directly (default: `true`)
     - `invocation-by-skill-approval`: Whether to require approval when loaded by another skill (default: `false`)
     - `cache-ttl-hours`: Hours before exploration cache expires; 0 disables caching (default: `24`)
     - `enable-checkpointing`: Write session checkpoints at phase boundaries (default: `true`)
     - `enable-progress-indicators`: Display phase progress messages (default: `true`)

2. **Determine invocation mode:**
   - **Direct invocation:** The user invoked deep-analysis directly or standalone
   - **Skill-invoked:** Another skill (e.g., codebase-analysis, feature-dev, docs-manager) loaded and is executing this workflow

3. **Resolve settings:**
   - Use found settings, or defaults if absent
   - If the file is malformed, warn the user and use defaults

4. **Set behavioral flags:**
   - `REQUIRE_APPROVAL` = direct-invocation-approval (if direct) or invocation-by-skill-approval (if skill-invoked)
   - `CACHE_TTL` = cache-ttl-hours value
   - `ENABLE_CHECKPOINTING` = enable-checkpointing value
   - `ENABLE_PROGRESS` = enable-progress-indicators value

---

## Phase 0: Session Setup

**Goal:** Check for cached exploration results, detect interrupted sessions, and initialize the session directory.

Skip this phase entirely if `CACHE_TTL = 0` AND `ENABLE_CHECKPOINTING = false`.

### Step 1: Exploration Cache Check

If `CACHE_TTL > 0`:

1. Check if `.agents/sessions/exploration-cache/manifest.md` exists
2. If found, read the manifest and verify:
   - `analysis_context` matches the current analysis context (or is a superset)
   - `codebase_path` matches the current working directory
   - `timestamp` is within `CACHE_TTL` hours of now
   - Config files referenced in `config_checksum` have not been modified since the cache was written (check mod-times of `package.json`, `tsconfig.json`, `pyproject.toml`, etc.)
3. **If cache is valid:**
   - **Skill-invoked mode:** Auto-accept the cache. Set `CACHE_HIT = true`. Read cached `synthesis.md` and `recon_summary.md`. Skip to Phase 6 step 2 (present/return results).
   - **Direct invocation:** Prompt the user to choose:
     - **Use cached results** — Set `CACHE_HIT = true`, skip to Phase 6 step 2
     - **Refresh analysis** — Set `CACHE_HIT = false`, proceed normally
4. **If cache is invalid or absent:** Set `CACHE_HIT = false`

### Step 2: Interrupted Session Check

If `ENABLE_CHECKPOINTING = true`:

1. Check if `.agents/sessions/__da_live__/checkpoint.md` exists
2. If found, read the checkpoint to determine `last_completed_phase`
3. Prompt the user to choose:
   - **Resume from Phase [N+1]** — Load checkpoint state, proceed from the interrupted phase (see Session Recovery in Error Handling)
   - **Start fresh** — Archive the interrupted session to `.agents/sessions/da-interrupted-{timestamp}/` and proceed normally
4. If not found: proceed normally

### Step 3: Initialize Session Directory

If `ENABLE_CHECKPOINTING = true` AND `CACHE_HIT = false`:

1. Create `.agents/sessions/__da_live__/` directory
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

1. **Determine analysis context:**
   - If arguments are provided, use them as the analysis context (feature area, question, or general exploration goal)
   - If no arguments and this skill was loaded by another skill, use the calling skill's context
   - If no arguments and standalone invocation, set context to "general codebase understanding"
   - Set `PATH = current working directory`
   - Inform the user: "Exploring codebase at: `PATH`" with the analysis context

2. **Rapid codebase reconnaissance:**
   Quickly map the codebase structure. This should take 1-2 minutes, not deep investigation.

   - **Directory structure:** List top-level directories to understand the project layout
   - **Language and framework detection:** Read config files (`package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) to identify primary language(s) and framework(s)
   - **File distribution:** Search for files with patterns like `src/**/*.ts`, `**/*.py` to gauge the size and shape of different areas
   - **Key documentation:** Read `README.md`, `CLAUDE.md`, or similar docs if they exist for project context
   - **For feature-focused analysis:** Search for feature-related terms (function names, component names, route paths) to find hotspot directories
   - **For general analysis:** Identify the 3-5 largest or most architecturally significant directories

   **Fallback:** If reconnaissance fails (empty project, unusual structure, errors), use the static focus area templates from Step 3b.

3. **Generate dynamic focus areas:**

   Based on reconnaissance findings, create focus areas tailored to the actual codebase. Default to 3 focus areas, but adjust based on codebase size and complexity (2 for small projects, up to 4 for large ones).

   **a) Dynamic focus areas (default):**

   Each focus area should include:
   - **Label:** Short description (e.g., "API layer in src/api/")
   - **Directories:** Specific directories to explore
   - **Starting files:** 2-3 key files to read first
   - **Search terms:** Patterns to find related code
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
   - **Search patterns:** [patterns]
   - **Complexity:** [Low/Medium/High]
   - **Assigned to:** explorer-1

   #### Focus Area 2: [Label]
   - **Directories:** [list]
   - **Starting files:** [2-3 files]
   - **Search patterns:** [patterns]
   - **Complexity:** [Low/Medium/High]
   - **Assigned to:** explorer-2

   [... repeated for each focus area]

   ### Agent Composition
   | Role | Count | Purpose |
   |------|-------|---------|
   | Explorer | [N] | Independent focus area exploration |
   | Synthesizer | 1 | Merge findings, deep investigation |

   ### Task Dependencies
   - Exploration Tasks 1-[N]: parallel (no dependencies)
   - Synthesis Task: blocked by all exploration tasks
   ```

5. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.agents/sessions/__da_live__/checkpoint.md`: set `current_phase: 1`
   - Write `.agents/sessions/__da_live__/team_plan.md` with the full team plan from Step 4
   - Write `.agents/sessions/__da_live__/recon_summary.md` with reconnaissance findings from Step 2
   - Append to `progress.md`: `[timestamp] Phase 1: Reconnaissance complete — [N] focus areas identified`

---

## Phase 2: Review & Approval

**Goal:** Present the team plan for user review and approval before allocating resources.

### If `REQUIRE_APPROVAL = false`

Skip to Phase 3 with a brief note: "Auto-approving team plan (skill-invoked mode). Proceeding with [N] explorers and 1 synthesizer."

### If `REQUIRE_APPROVAL = true`

1. **Present the team plan** to the user (output the plan from Phase 1 Step 4), then prompt the user to choose:
   - **Approve** — Proceed to Phase 3 as-is
   - **Modify** — User describes changes (adjust focus areas, add/remove explorers, change scope)
   - **Regenerate** — Re-run reconnaissance with user feedback

2. **If "Modify"** (up to 3 cycles):
   - Ask what to change
   - Apply modifications to the team plan (adjust focus areas, agent count, scope)
   - Re-present the updated plan for approval
   - If 3 modification cycles are exhausted, offer "Approve current plan" or "Abort analysis"

3. **If "Regenerate"** (up to 2 cycles):
   - Ask for feedback/new direction
   - Return to Phase 1 Step 2 with the user's feedback incorporated
   - Re-compose and re-present the team plan
   - If 2 regeneration cycles are exhausted, offer "Approve current plan" or "Abort analysis"

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.agents/sessions/__da_live__/checkpoint.md`: set `current_phase: 2`, record `approval_mode` (approved/auto-approved)
   - Append to `progress.md`: `[timestamp] Phase 2: Plan approved (mode: [approval_mode])`

---

## Phase 3: Team Assembly

**Goal:** Create the team, spawn agents, create tasks, and assign work using the approved plan.

1. **Create the team:**
   - Create an agent team named `deep-analysis-{timestamp}` (e.g., `deep-analysis-1707300000`)
   - Description: "Deep analysis of [analysis context]"

2. **Spawn teammates:**
   Spawn agents based on the approved plan:

   - **N explorers** (one per focus area) — Delegate to independent explorer agents (see `agents/code-explorer.md` for instructions)
     - Named: `explorer-1`, `explorer-2`, ... `explorer-N`
     - Prompt each with: "You are part of a deep analysis team. Wait for your task assignment. The codebase is at: [PATH]. Analysis context: [context]"

   - **1 synthesizer** — Delegate to a synthesizer agent (see `agents/code-synthesizer.md` for instructions)
     - Named: `synthesizer`
     - Prompt with: "You are the synthesizer for a deep analysis team. You have shell access for git history, dependency analysis, and static analysis. Wait for your task assignment. The codebase is at: [PATH]. Analysis context: [context]"

3. **Create tasks:**
   Create a task for each item based on the approved plan's focus areas:

   - **Exploration Task per focus area:** Subject: "Explore: [Focus area label]", Description: detailed exploration instructions including directories, starting files, search terms, and complexity estimate
   - **Synthesis Task:** Subject: "Synthesize and evaluate exploration findings", Description: "Merge and synthesize findings from all exploration tasks into a unified analysis. Investigate gaps using shell commands (git history, dependency trees). Evaluate completeness before finalizing."
     - Mark the synthesis task as blocked by all exploration task IDs

4. **Assign exploration tasks (with status guard):**

   For each exploration task, apply the following status-guarded assignment:

   1. Check the task's current status and owner
   2. Only assign if status is `pending` AND owner is empty
   3. If already assigned or completed: log "Task [ID] already [status], skipping" and move on
   4. Set the owner to the corresponding explorer
   5. Send the explorer a message with the task details:
      "Your exploration task [ID] is assigned. Focus area: [label]. Directories: [list]. Starting files: [list]. Search patterns: [list]. Begin exploration now."

   Never re-assign a completed or in-progress task.

5. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.agents/sessions/__da_live__/checkpoint.md`: set `current_phase: 3`, record `team_name`, `explorer_names` (list), `task_ids` (map of explorer to task ID), `synthesis_task_id`
   - Append to `progress.md`: `[timestamp] Phase 3: Team assembled — [N] explorers, 1 synthesizer`

---

## Phase 4: Focused Exploration

**Goal:** Workers explore their assigned areas independently.

### Monitoring Loop

After assigning exploration tasks, monitor progress with status-aware tracking:

1. When an explorer goes idle or sends a message, check their task status
2. **If task is `completed`**: Record the explorer's findings. If `ENABLE_CHECKPOINTING = true`, write `explorer-{N}-findings.md` to `.agents/sessions/__da_live__/` and update checkpoint.
3. **If task is `in_progress`**: The explorer is still working — do not re-send the assignment
4. **If task is `pending` and owner is set**: The explorer received the assignment but has not started yet — wait, do not re-send
5. **If task is `pending` and owner is empty**: Assignment may have been lost — re-assign using the status guard from Phase 3 step 4

Never re-assign a completed or in-progress task. This is the primary duplicate prevention mechanism.

Update the progress display as explorers complete.

- Workers explore their assigned focus areas independently — no cross-worker messaging
- Workers can respond to follow-up questions from the synthesizer
- Each worker marks its task as completed when done
- You (the lead) receive idle notifications as workers finish
- Wait for all exploration tasks to be marked complete before proceeding to Phase 5

---

## Phase 5: Evaluation and Synthesis

**Goal:** Verify exploration completeness, launch synthesis with deep investigation.

### Step 1: Structural Completeness Check

This is a structural check, not a quality assessment:

1. Verify all exploration tasks are completed
2. Check that each worker produced a report with content (review the messages/reports received)
3. **If a worker failed completely** (empty or error output):
   - Create a follow-up exploration task targeting the gap
   - Assign it to an idle worker
   - Add the new task to the synthesis task's blocked-by list
   - Wait for the follow-up task to complete
4. **If all produced content**: proceed immediately to Step 2

### Step 2: Launch Synthesis

1. Assign the synthesis task to the synthesizer
2. Send the synthesizer a message with exploration context and recon findings:
   "All exploration tasks are complete. Your synthesis task is now assigned.

   Analysis context: [analysis context]
   Codebase path: [PATH]

   Recon findings from planning phase:
   - Project structure: [brief summary of directory layout]
   - Primary language/framework: [what was detected]
   - Key areas identified: [the focus areas and why they were chosen]

   The workers are: [list of explorer names from the approved plan]. You can message them with follow-up questions if you find conflicts or gaps in their findings.

   You have shell access for deep investigation — use it for git history analysis, dependency trees, static analysis, or any investigation that file reading and searching cannot handle.

   Read the completed exploration tasks to access their reports, then synthesize into a unified analysis. Evaluate completeness before finalizing."
3. Wait for the synthesizer to mark the synthesis task as completed

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.agents/sessions/__da_live__/checkpoint.md`: set `current_phase: 5`
   - Write `.agents/sessions/__da_live__/synthesis.md` with the synthesis results
   - Append to `progress.md`: `[timestamp] Phase 5: Synthesis complete`

---

## Phase 6: Completion + Cleanup

**Goal:** Collect results, present to user, and tear down the team.

1. **Collect synthesis output:**
   - The synthesizer's findings are in the messages it sent and/or the task completion output
   - Read the synthesis results

2. **Write exploration cache** (if `CACHE_TTL > 0`):
   - Create `.agents/sessions/exploration-cache/` directory (overwrite if exists)
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
   Send shutdown requests to all spawned teammates (iterate over the actual agents from the approved plan).

5. **Archive session and cleanup team:**
   - If `ENABLE_CHECKPOINTING = true`: Move `.agents/sessions/__da_live__/` to `.agents/sessions/da-{timestamp}/`
   - Delete the team and its task list

---

## Error Handling

### Settings Check Failure
- If the settings file exists but is malformed or the deep-analysis section is unparseable: warn the user ("Settings file found but could not parse deep-analysis settings — using defaults") and proceed with default approval values.

### Planning Phase Failure
- If reconnaissance fails (errors, empty results, unusual structure): fall back to static focus area templates (Step 3b)
- If the codebase appears empty: inform the user and ask how to proceed

### Approval Phase Failure
- If maximum modification cycles (3) or regeneration cycles (2) are reached without approval, prompt the user to choose:
  - **Approve current plan** — Proceed with the latest version of the plan
  - **Abort analysis** — Cancel the analysis entirely

### Partial Worker Failure
- If one worker fails: create a follow-up task targeting the missed focus area, assign to an idle worker, add to synthesis blocked-by list
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
- The synthesizer has shell access for deep investigation (git history, dependency trees, static analysis)
- Wait for task dependencies to resolve before proceeding
- Handle agent failures gracefully — continue with partial results
- Agent count and focus area details come from the approved plan, not hardcoded values

---

## Nested Agents

This skill uses the following nested agents:

- **`agents/code-explorer.md`** — Independent exploration agents that investigate assigned focus areas and report structured findings. Multiple instances run in parallel, one per focus area.
- **`agents/code-synthesizer.md`** — A single synthesizer agent that merges exploration findings, investigates gaps with shell access, and produces a unified analysis.

---

## Integration Notes

### Sub-agent Capabilities

**Code Explorer agents** need:
- File reading, file search by pattern, and content search capabilities
- Shell access for basic commands
- Ability to communicate with the coordinator and respond to follow-up questions
- Read-heavy workload; suitable for faster/cheaper model tiers

**Code Synthesizer agent** needs:
- All capabilities of explorers
- Shell access for git history, dependency analysis, and static analysis
- Ability to communicate with explorer agents for follow-up questions
- Higher reasoning capability for cross-cutting synthesis; suitable for advanced model tiers

### Configurable Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `direct-invocation-approval` | `true` | Require plan approval when invoked directly |
| `invocation-by-skill-approval` | `false` | Require approval when loaded by another skill |
| `cache-ttl-hours` | `24` | Hours before exploration cache expires; 0 disables |
| `enable-checkpointing` | `true` | Write session checkpoints at phase boundaries |
| `enable-progress-indicators` | `true` | Display phase progress messages |
