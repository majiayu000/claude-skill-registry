---
name: deep-analysis
description: Deep exploration and synthesis workflow with dynamic planning and hub-and-spoke coordination. Use for deep analysis, deep understanding, or codebase investigation.
dependencies: []
---

# Deep Analysis Workflow

Execute a structured exploration + synthesis workflow using hub-and-spoke coordination. The lead performs rapid reconnaissance to generate dynamic focus areas, composes a team plan for review, workers explore independently, and a synthesizer merges findings with deep investigation.

This skill can be invoked standalone or loaded by other skills as a reusable building block. Approval behavior is configurable.

## Settings Check

**Goal:** Determine whether the team plan requires user approval before execution.

1. **Read settings:**
   - Check configuration for deep-analysis settings
   - Look for a `deep-analysis` section with nested settings:
     - `direct-invocation-approval`: Whether to require plan approval when invoked directly (default: true)
     - `invocation-by-skill-approval`: Whether to require approval when loaded by another skill (default: false)

2. **Determine invocation mode:**
   - **Direct invocation:** The user invoked this skill directly, or it is running standalone
   - **Skill-invoked:** Another skill (e.g., codebase-analysis, feature-dev, docs-manager) loaded and is executing this workflow

3. **Resolve settings:**
   - If settings were found, use them as-is
   - If the settings are missing, use defaults
   - If the settings are malformed (unparseable), warn the user and use defaults

4. **Set `REQUIRE_APPROVAL`:**
   - If direct invocation: use `direct-invocation-approval` value (default: `true`)
   - If skill-invoked: use `invocation-by-skill-approval` value (default: `false`)

5. **Parse session settings** (also under the `deep-analysis` section):
   - `cache-ttl-hours`: Number of hours before exploration cache expires. Default: `24`. Set to `0` to disable caching entirely.
   - `enable-checkpointing`: Whether to write session checkpoints at phase boundaries. Default: `true`.
   - `enable-progress-indicators`: Whether to display phase progress messages. Default: `true`.

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

1. Check if `.agents/sessions/exploration-cache/manifest.md` exists
2. If found, read the manifest and verify:
   - `analysis_context` matches the current analysis context (or is a superset)
   - `codebase_path` matches the current working directory
   - `timestamp` is within `CACHE_TTL` hours of now
   - Config files referenced in `config_checksum` haven't been modified since the cache was written (check mod-times of `package.json`, `tsconfig.json`, `pyproject.toml`, etc.)
3. **If cache is valid:**
   - **Skill-invoked mode:** Auto-accept the cache. Set `CACHE_HIT = true`. Read cached `synthesis.md` and `recon_summary.md`. Skip to Phase 6 step 2 (present/return results).
   - **Direct invocation:** Prompt the user to choose:
     - **Use cached results** -- Set `CACHE_HIT = true`, skip to Phase 6 step 2
     - **Refresh analysis** -- Set `CACHE_HIT = false`, proceed normally
4. **If cache is invalid or absent:** Set `CACHE_HIT = false`

### Step 2: Interrupted Session Check

If `ENABLE_CHECKPOINTING = true`:

1. Check if `.agents/sessions/__da_live__/checkpoint.md` exists
2. If found, read the checkpoint to determine `last_completed_phase`
3. Prompt the user to choose:
   - **Resume from Phase [N+1]** -- Load checkpoint state, proceed from the interrupted phase (see Session Recovery in Error Handling)
   - **Start fresh** -- Archive the interrupted session to `.agents/sessions/da-interrupted-{timestamp}/` and proceed normally
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
   - Accept the following inputs: an analysis context or focus area
   - If no inputs and this skill was loaded by another skill, use the calling skill's context
   - If no inputs and standalone invocation, set context to "general codebase understanding"
   - Set `PATH = current working directory`
   - Inform the user: "Exploring codebase at: `PATH`" with the analysis context

2. **Rapid codebase reconnaissance:**
   Quickly map the codebase structure. This should take 1-2 minutes, not deep investigation.

   - **Directory structure:** Search for top-level directories to understand the project layout
   - **Language and framework detection:** Read config files (`package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) to identify primary language(s) and framework(s)
   - **File distribution:** Search with patterns like `src/**/*.ts`, `**/*.py` to gauge the size and shape of different areas
   - **Key documentation:** Read `README.md`, `CLAUDE.md`, or similar docs if they exist for project context
   - **For feature-focused analysis:** Search file contents for feature-related terms (function names, component names, route paths) to find hotspot directories
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

   ### Worker Composition
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
   - Append to `progress.md`: `[timestamp] Phase 1: Reconnaissance complete -- [N] focus areas identified`

---

## Phase 2: Review & Approval

**Goal:** Present the team plan for user review and approval before allocating resources.

### If `REQUIRE_APPROVAL = false`

Skip to Phase 3 with a brief note: "Auto-approving team plan (skill-invoked mode). Proceeding with [N] explorers and 1 synthesizer."

### If `REQUIRE_APPROVAL = true`

1. **Present the team plan** to the user (output the plan from Phase 1 Step 4), then prompt the user to choose:
   - **Approve** -- Proceed to Phase 3 as-is
   - **Modify** -- User describes changes (adjust focus areas, add/remove explorers, change scope)
   - **Regenerate** -- Re-run reconnaissance with user feedback

2. **If "Modify"** (up to 3 cycles):
   - Ask what to change
   - Apply modifications to the team plan (adjust focus areas, worker count, scope)
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

**Goal:** Set up workers, create tasks, and assign work using the approved plan.

1. **Prepare workers:**
   Based on the approved plan, prepare the following workers:

   - **N explorers** (one per focus area): Refer to the **code-explorer** skill for exploration behavior. Each explorer investigates their assigned focus area independently.
   - **1 synthesizer**: Refer to the **code-synthesizer** skill for synthesis behavior. The synthesizer has shell access for git history, dependency analysis, and static analysis.

2. **Create tasks:**
   For each focus area, create an exploration task with: subject ("Explore: [Focus area label]"), detailed exploration instructions including directories, starting files, search terms, and complexity estimate.

   Create a synthesis task: "Synthesize and evaluate exploration findings" -- blocked by all exploration tasks.

3. **Assign exploration tasks:**
   For each exploration task, delegate to the corresponding explorer worker with the task details: focus area label, directories, starting files, and search patterns.

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.agents/sessions/__da_live__/checkpoint.md`: set `current_phase: 3`, record worker names, task assignments
   - Append to `progress.md`: `[timestamp] Phase 3: Team assembled -- [N] explorers, 1 synthesizer`

---

## Phase 4: Focused Exploration

**Goal:** Workers explore their assigned areas independently.

### Monitoring

After assigning exploration tasks, monitor progress:

1. When an explorer completes, record their findings. If `ENABLE_CHECKPOINTING = true`, write `explorer-{N}-findings.md` to `.agents/sessions/__da_live__/` and update checkpoint.
2. Workers explore independently -- no cross-worker communication (hub-and-spoke topology)
3. Workers can respond to follow-up questions from the synthesizer
4. Each worker marks its task as completed when done
5. **Wait for all exploration tasks to complete** before proceeding to Phase 5

---

## Phase 5: Evaluation and Synthesis

**Goal:** Verify exploration completeness, launch synthesis with deep investigation.

### Step 1: Structural Completeness Check

This is a structural check, not a quality assessment:

1. Verify all exploration tasks are completed
2. Check that each worker produced a report with content
3. **If a worker failed completely** (empty or error output):
   - Create a follow-up exploration task targeting the gap
   - Assign it to an idle worker
   - Wait for the follow-up to complete
4. **If all produced content**: proceed immediately to Step 2

### Step 2: Launch Synthesis

1. Assign the synthesis task to the synthesizer worker
2. Provide the synthesizer with:
   - Analysis context and codebase path
   - Reconnaissance findings from Phase 1
   - The list of explorer workers (for follow-up questions if needed)
   - Instructions to read exploration task results, synthesize into a unified analysis, and evaluate completeness before finalizing
3. The synthesizer has shell access for deep investigation -- git history analysis, dependency trees, static analysis, or any investigation that basic file reading cannot handle
4. Wait for the synthesizer to complete

5. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.agents/sessions/__da_live__/checkpoint.md`: set `current_phase: 5`
   - Write `.agents/sessions/__da_live__/synthesis.md` with the synthesis results
   - Append to `progress.md`: `[timestamp] Phase 5: Synthesis complete`

---

## Phase 6: Completion + Cleanup

**Goal:** Collect results, present to user, and clean up.

1. **Collect synthesis output:**
   - Read the synthesis results from the synthesizer

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
   - **Loaded by another skill:** The synthesis is complete. Control returns to the calling workflow -- do not present a standalone summary.

4. **Shut down workers:**
   Signal all workers that analysis is complete and they can stop.

5. **Archive session and cleanup:**
   - If `ENABLE_CHECKPOINTING = true`: Move `.agents/sessions/__da_live__/` to `.agents/sessions/da-{timestamp}/`
   - Clean up any temporary team/task resources

---

## Error Handling

### Settings Check Failure
- If settings exist but are malformed or unparseable: warn the user ("Settings found but could not parse deep-analysis settings -- using defaults") and proceed with default approval values.

### Planning Phase Failure
- If reconnaissance fails (errors, empty results, unusual structure): fall back to static focus area templates (Step 3b)
- If the codebase appears empty: inform the user and ask how to proceed

### Approval Phase Failure
- If maximum modification cycles (3) or regeneration cycles (2) are reached without approval, prompt the user to choose:
  - **Approve current plan** -- Proceed with the latest version of the plan
  - **Abort analysis** -- Cancel the analysis entirely

### Partial Worker Failure
- If one worker fails: create a follow-up task targeting the missed focus area, assign to an idle worker
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
| **Phase 4** | Read completed `explorer-{N}-findings.md` files from session dir. Only assign explorers whose findings files are missing. Add existing findings to synthesizer context. |
| **Phase 5** | Load all explorer findings from session dir. Launch a fresh synthesizer with the persisted findings. |
| **Phase 6** | Load `synthesis.md` from session dir. Proceed directly to present/return results and cleanup. |

**Recovery procedure:**
1. Read `checkpoint.md` to determine `last_completed_phase` and session state (worker names, task assignments)
2. Load any persisted artifacts from the session directory (team_plan, explorer findings, synthesis)
3. Resume from Phase `last_completed_phase + 1` using the loaded state
4. For Phase 4 recovery: compare persisted `explorer-{N}-findings.md` files against expected explorer list to determine which explorers still need to run

---

## Coordination

- The lead (you) acts as the planner: performs recon, composes the team plan, handles approval, assigns work
- Workers explore independently -- no cross-worker communication (hub-and-spoke topology)
- The synthesizer can ask workers follow-up questions to resolve conflicts and fill gaps
- The synthesizer has shell access for deep investigation (git history, dependency trees, static analysis)
- Wait for task dependencies to resolve before proceeding
- Handle worker failures gracefully -- continue with partial results
- Worker count and focus area details come from the approved plan, not hardcoded values

## Integration Notes

**What this component does:** Orchestrates a multi-phase deep analysis workflow: reconnaissance, dynamic planning, user approval, parallel exploration via independent workers, synthesis with deep investigation, caching, and session checkpointing/recovery.

**Origin:** Skill (orchestrator, keystone)

**Capabilities needed:**
- File reading, writing, and search (for reconnaissance, caching, checkpointing)
- Shell command execution (for the synthesizer's deep investigation: git history, dependency trees, static analysis)
- User interaction/prompting (for approval flow, cache decisions, session recovery)
- Task/worker delegation (for spawning explorer and synthesizer workers)
- Background task monitoring (for tracking explorer completion)

**Adaptation guidance:**
- The hub-and-spoke coordination pattern originally used platform-specific TeamCreate/TaskCreate/SendMessage/TaskUpdate APIs. Adapt to whatever task delegation and messaging mechanism the target harness provides.
- Explorer workers were originally spawned as Sonnet-tier agents; the synthesizer as Opus-tier. If the target harness supports model selection, preserve this tiering for cost efficiency.
- Session checkpointing writes to `.agents/sessions/__da_live__/`. If the target harness has its own session/state management, adapt accordingly.
- The approval flow uses interactive prompts. If the target harness is non-interactive, default to auto-approval.
