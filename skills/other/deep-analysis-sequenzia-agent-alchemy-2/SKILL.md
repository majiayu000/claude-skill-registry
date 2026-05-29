---
name: deep-analysis
description: Deep exploration and synthesis workflow with dynamic planning and hub-and-spoke coordination. Use for deep analysis, codebase understanding, or thorough investigation of a focus area.
dependencies: []
---

# Deep Analysis Workflow

Execute a structured exploration + synthesis workflow using hub-and-spoke coordination. The lead performs rapid reconnaissance to generate dynamic focus areas, composes a team plan for review, workers explore independently, and a synthesizer merges findings with deep investigation.

This skill can be invoked standalone or loaded by other skills as a reusable building block. Approval behavior is configurable.

## Settings Check

**Goal:** Determine whether the team plan requires user approval before execution.

1. **Read settings file:**
   - Check if `.agents/agent-alchemy.local.md` exists
   - If it exists, read it and look for a `deep-analysis` section with nested settings
   - If the file does not exist or is malformed, use defaults (see step 4)

2. **Determine invocation mode:**
   - **Direct invocation:** The user invoked this skill directly
   - **Skill-invoked:** Another skill loaded and is executing this workflow

3. **Resolve settings:**
   - If settings were found, use them as-is
   - If the file is missing or the `deep-analysis` section is absent, use defaults:
     - `direct-invocation-approval`: `true`
     - `invocation-by-skill-approval`: `false`

4. **Set `REQUIRE_APPROVAL`:**
   - If direct invocation → use `direct-invocation-approval` value (default: `true`)
   - If skill-invoked → use `invocation-by-skill-approval` value (default: `false`)

5. **Parse session settings** (also under the `deep-analysis` section):
   - `cache-ttl-hours`: Number of hours before exploration cache expires. Default: `24`. Set to `0` to disable caching entirely.
   - `enable-checkpointing`: Whether to write session checkpoints at phase boundaries. Default: `true`.
   - `enable-progress-indicators`: Whether to display `[Phase N/6]` progress messages. Default: `true`.

---

## Phase 0: Session Setup

**Goal:** Check for cached exploration results, detect interrupted sessions, and initialize the session directory.

> Skip this phase entirely if cache TTL is 0 AND checkpointing is disabled.

### Step 1: Exploration Cache Check

If cache TTL > 0:

1. Check if `.agents/sessions/exploration-cache/manifest.md` exists
2. If found, read the manifest and verify:
   - `analysis_context` matches the current analysis context (or is a superset)
   - `codebase_path` matches the current working directory
   - `timestamp` is within the configured TTL hours of now
   - Config files referenced in `config_checksum` haven't been modified since the cache was written
3. **If cache is valid:**
   - **Skill-invoked mode:** Auto-accept the cache. Read cached `synthesis.md` and `recon_summary.md`. Skip to Phase 6 step 2 (present/return results).
   - **Direct invocation:** Prompt the user to choose:
     - **Use cached results** — Skip to Phase 6 step 2
     - **Refresh analysis** — Proceed normally
4. **If cache is invalid or absent:** Proceed normally

### Step 2: Interrupted Session Check

If checkpointing is enabled:

1. Check if `.agents/sessions/__da_live__/checkpoint.md` exists
2. If found, read the checkpoint to determine `last_completed_phase`
3. Prompt the user to choose:
   - **Resume from Phase [N+1]** — Load checkpoint state, proceed from the interrupted phase
   - **Start fresh** — Archive the interrupted session and proceed normally
4. If not found: proceed normally

### Step 3: Initialize Session Directory

If checkpointing is enabled and no cache hit:

1. Create `.agents/sessions/__da_live__/` directory
2. Write a `checkpoint.md` with session metadata (analysis context, codebase path, start timestamp, current phase)
3. Write a `progress.md` to track phase completions

---

## Phase 1: Reconnaissance & Planning

**Goal:** Perform codebase reconnaissance, generate dynamic focus areas, and compose a team plan.

1. **Determine analysis context:**
   - If arguments are provided, use them as the analysis context
   - If no arguments and this skill was loaded by another skill, use the calling skill's context
   - If no arguments and standalone invocation, set context to "general codebase understanding"

2. **Rapid codebase reconnaissance:**
   Search for files, read config files, and map the codebase structure. This should take 1-2 minutes, not deep investigation.

   - **Directory structure:** Find top-level directories to understand the project layout
   - **Language and framework detection:** Read config files (`package.json`, `tsconfig.json`, `pyproject.toml`, etc.) to identify primary language(s) and framework(s)
   - **File distribution:** Search for file patterns like `src/**/*.ts`, `**/*.py` to gauge the size and shape of different areas
   - **Key documentation:** Read `README.md`, `CLAUDE.md`, or similar docs if they exist for project context
   - **For feature-focused analysis:** Search for feature-related terms to find hotspot directories
   - **For general analysis:** Identify the 3-5 largest or most architecturally significant directories

   **Fallback:** If reconnaissance fails (empty project, unusual structure, errors), use static focus area templates from Step 3b.

3. **Generate dynamic focus areas:**

   Based on reconnaissance findings, create focus areas tailored to the actual codebase. Default to 3 focus areas, but adjust based on codebase size and complexity (2 for small projects, up to 4 for large ones).

   Each focus area should include:
   - **Label:** Short description (e.g., "API layer in src/api/")
   - **Directories:** Specific directories to explore
   - **Starting files:** 2-3 key files to read first
   - **Search terms:** Patterns to find related code
   - **Complexity estimate:** Low/Medium/High based on file count and apparent structure

4. **Compose the team plan:**

   Assemble a structured plan document:
   - Analysis context
   - Reconnaissance summary (project name, primary language/framework, codebase size, key observations)
   - Focus areas with directories, starting files, search patterns, and complexity estimates
   - Agent composition table (N explorers using a balanced model, 1 synthesizer using a high-reasoning model)
   - Task dependencies (exploration tasks are parallel, synthesis is blocked by all exploration tasks)

5. **Checkpoint** (if enabled):
   - Update session checkpoint, write team plan and recon summary, append to progress log

---

## Phase 2: Review & Approval

**Goal:** Present the team plan for user review and approval before allocating resources.

### If approval is not required

Skip to Phase 3 with a brief note: "Auto-approving team plan (skill-invoked mode). Proceeding with N explorers and 1 synthesizer."

### If approval is required

1. Present the team plan, then prompt the user to choose:
   - **Approve** — Proceed to Phase 3 as-is
   - **Modify** — User describes changes (adjust focus areas, add/remove explorers, change scope)
   - **Regenerate** — Re-run reconnaissance with user feedback

2. If "Modify" (up to 3 cycles): Apply modifications, re-present for approval
3. If "Regenerate" (up to 2 cycles): Re-run Phase 1 Step 2 with feedback, re-compose and re-present

---

## Phase 3: Team Assembly

**Goal:** Create the team, delegate to agents, create tasks, and assign work using the approved plan.

1. **Set up the team** for the analysis session

2. **Delegate exploration work:**
   - Assign **N independent explorer agents** (one per focus area), each using a balanced-reasoning model
     - Each explorer receives: the codebase path, analysis context, and their specific focus area details
   - Assign **1 synthesizer agent** using a high-reasoning model
     - The synthesizer receives: the codebase path, analysis context, and instructions to wait for exploration results

3. **Create tasks** for tracking:
   - One exploration task per focus area
   - One synthesis task blocked by all exploration tasks

4. **Assign exploration tasks** with status guards — only assign if status is pending and unowned. Never re-assign a completed or in-progress task.

---

## Phase 4: Focused Exploration

**Goal:** Workers explore their assigned areas independently.

After assigning exploration tasks, monitor progress:

1. When an explorer completes, record its findings. If checkpointing is enabled, persist findings to the session directory.
2. Workers explore independently — no cross-worker messaging (hub-and-spoke topology)
3. Workers can respond to follow-up questions from the synthesizer
4. **Wait for all exploration tasks to complete** before proceeding to Phase 5

---

## Phase 5: Evaluation and Synthesis

**Goal:** Verify exploration completeness, launch synthesis with deep investigation.

### Step 1: Structural Completeness Check

1. Verify all exploration tasks are completed
2. Check that each worker produced a report with content
3. If a worker failed completely, create a follow-up exploration task and wait for it
4. If all produced content, proceed to Step 2

### Step 2: Launch Synthesis

1. Assign the synthesis task to the synthesizer
2. Provide the synthesizer with all exploration results and recon findings
3. The synthesizer can message explorers with follow-up questions to resolve conflicts and gaps
4. The synthesizer has shell command access for git history analysis, dependency trees, and static analysis
5. Wait for synthesis to complete

---

## Phase 6: Completion + Cleanup

**Goal:** Collect results, present to user, and tear down the team.

1. **Collect synthesis output** from the synthesizer's report

2. **Write exploration cache** (if cache TTL > 0):
   - Create `.agents/sessions/exploration-cache/` directory
   - Write manifest with analysis context, codebase path, timestamp, config checksums, and TTL
   - Write synthesis and recon summary results

3. **Present or return results:**
   - **Standalone invocation:** Present the synthesized analysis to the user
   - **Loaded by another skill:** Control returns to the calling workflow — do not present a standalone summary

4. **Shut down all agents** and archive/clean up the session

---

## Error Handling

### Settings Check Failure
- If settings file exists but is malformed: warn the user and proceed with defaults

### Planning Phase Failure
- If reconnaissance fails: fall back to static focus area templates
- If the codebase appears empty: inform the user and ask how to proceed

### Partial Worker Failure
- If one worker fails: create a follow-up task for the missed focus area
- If two workers fail: attempt follow-ups, but synthesize with partial results if follow-ups also fail
- If all workers fail: inform the user and offer to retry or abort

### Synthesizer Failure
- Present the raw exploration results directly; offer to retry synthesis

### Session Recovery

When resuming from an interrupted session, use per-phase strategy:

| Interrupted At | Recovery Strategy |
|----------------|-------------------|
| Phase 1 | Restart from Phase 1 (reconnaissance is fast) |
| Phase 2 | Load saved team plan, re-present for approval |
| Phase 3 | Load approved plan, restart team assembly |
| Phase 4 | Read completed explorer findings from session dir, only assign missing explorers |
| Phase 5 | Load all explorer findings, launch fresh synthesis |
| Phase 6 | Load synthesis, proceed to present results and cleanup |

---

## Agent Coordination

- The lead acts as the planner: performs recon, composes the team plan, handles approval, assigns work
- Workers explore independently — no cross-worker messaging (hub-and-spoke topology)
- The synthesizer can ask workers follow-up questions to resolve conflicts and fill gaps
- The synthesizer has shell command access for deep investigation (git history, dependency trees, static analysis)
- Wait for task dependencies to resolve before proceeding
- Handle agent failures gracefully — continue with partial results
- Agent count and focus area details come from the approved plan, not hardcoded values

## Integration Notes

**What this component does:** Orchestrates a multi-agent codebase exploration and synthesis workflow with dynamic focus area planning, caching, and session recovery.

**Capabilities needed:**
- File reading and searching
- Shell command execution
- User interaction / prompting
- Sub-agent delegation (multiple parallel explorers + 1 synthesizer)

**Adaptation guidance:**
- The exploration step delegates to multiple agents in parallel — implement as concurrent tasks if your harness supports it, or serialize if not
- The original used a 3-tier model strategy (fast/balanced/powerful) — use your default model unless specific steps need stronger reasoning
- Session files under `.agents/sessions/` provide caching and recovery — implement if your harness supports persistent state, or skip for simpler setups

**Configurable parameters:**
- `direct-invocation-approval` (default: true) — Require plan approval when invoked directly
- `invocation-by-skill-approval` (default: false) — Require approval when loaded by another skill
- `cache-ttl-hours` (default: 24) — Hours before exploration cache expires; 0 disables caching
- `enable-checkpointing` (default: true) — Write session checkpoints at phase boundaries
- `enable-progress-indicators` (default: true) — Display phase progress messages
