---
description: Deep exploration and synthesis workflow using parallel task agents with dynamic planning and hub-and-spoke coordination. Use when asked for "deep analysis", "deep understanding", "analyze codebase", "explore and analyze", or "investigate codebase".
user-invocable: true
---

# Deep Analysis Workflow

Execute a structured exploration + synthesis workflow using parallel task agents with hub-and-spoke coordination. The lead performs rapid reconnaissance to generate dynamic focus areas, composes a team plan for review, spawns explorer agents in parallel via the `task` tool, and a synthesizer agent merges findings with bash-powered investigation.

This skill can be invoked standalone or loaded by other skills as a reusable building block. Approval behavior is configurable via `.claude/agent-alchemy.local.md`.

Arguments: $ARGUMENTS (optional — analysis context or focus area)

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
   - **Direct invocation:** Use `question` to offer:
     - **"Use cached results"** — Set `CACHE_HIT = true`, skip to Phase 6 step 2
     - **"Refresh analysis"** — Set `CACHE_HIT = false`, proceed normally
4. **If cache is invalid or absent:** Set `CACHE_HIT = false`

### Step 2: Interrupted Session Check

If `ENABLE_CHECKPOINTING = true`:

1. Check if `.claude/sessions/__da_live__/checkpoint.md` exists
2. If found, read the checkpoint to determine `last_completed_phase`
3. Use `question` to offer:
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

**Goal:** Perform codebase reconnaissance, generate dynamic focus areas, and compose a task plan.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 1/6] Reconnaissance & Planning** — Mapping codebase structure..."

1. **Determine analysis context:**
   - If `$ARGUMENTS` is provided, use it as the analysis context (feature area, question, or general exploration goal)
   - If no arguments and this skill was loaded by another skill, use the calling skill's context
   - If no arguments and standalone invocation, set context to "general codebase understanding"
   - Set `PATH = current working directory`
   - Inform the user: "Exploring codebase at: `PATH`" with the analysis context

2. **Rapid codebase reconnaissance:**
   Use `glob`, `grep`, and `read` to quickly map the codebase structure. This should take 1-2 minutes, not deep investigation.

   - **Directory structure:** List top-level directories with `glob` (e.g., `*/` pattern) to understand the project layout
   - **Language and framework detection:** Read config files (`package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) to identify primary language(s) and framework(s)
   - **File distribution:** Use `glob` with patterns like `src/**/*.ts`, `**/*.py` to gauge the size and shape of different areas
   - **Key documentation:** Read `README.md`, `CLAUDE.md`, or similar docs if they exist for project context
   - **For feature-focused analysis:** Use `grep` to search for feature-related terms (function names, component names, route paths) to find hotspot directories
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

4. **Compose the task plan:**

   Assemble a structured plan document from the reconnaissance and focus area findings:

   ```markdown
   ## Task Plan: Deep Analysis

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
   | Explorer | [N] | anthropic/claude-sonnet-4-6 | Independent focus area exploration |
   | Synthesizer | 1 | anthropic/claude-opus-4-6 | Merge findings, deep investigation |

   ### Execution Plan
   - Exploration Tasks 1-[N]: parallel (spawned simultaneously via task tool)
   - Synthesis Task: sequential (spawned after all explorer task returns are collected)
   ```

5. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 1`
   - Write `.claude/sessions/__da_live__/team_plan.md` with the full task plan from Step 4
   - Write `.claude/sessions/__da_live__/recon_summary.md` with reconnaissance findings from Step 2
   - Append to `progress.md`: `[timestamp] Phase 1: Reconnaissance complete — [N] focus areas identified`

---

## Phase 2: Review & Approval

**Goal:** Present the task plan for user review and approval before allocating resources.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 2/6] Review & Approval** — Presenting task plan..."

### If `REQUIRE_APPROVAL = false`

Skip to Phase 3 with a brief note: "Auto-approving task plan (skill-invoked mode). Proceeding with [N] explorers and 1 synthesizer."

### If `REQUIRE_APPROVAL = true`

1. **Present the task plan** to the user (output the plan from Phase 1 Step 4), then use `question`:
   - **"Approve"** — Proceed to Phase 3 as-is
   - **"Modify"** — User describes changes (adjust focus areas, add/remove explorers, change scope)
   - **"Regenerate"** — Re-run reconnaissance with user feedback

2. **If "Modify"** (up to 3 cycles):
   - Ask what to change using `question`
   - Apply modifications to the task plan (adjust focus areas, agent count, scope)
   - Re-present the updated plan for approval
   - If 3 modification cycles are exhausted, offer "Approve current plan" or "Abort analysis"

3. **If "Regenerate"** (up to 2 cycles):
   - Ask for feedback/new direction using `question`
   - Return to Phase 1 Step 2 with the user's feedback incorporated
   - Re-compose and re-present the task plan
   - If 2 regeneration cycles are exhausted, offer "Approve current plan" or "Abort analysis"

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 2`, record `approval_mode` (approved/auto-approved)
   - Append to `progress.md`: `[timestamp] Phase 2: Plan approved (mode: [approval_mode])`

---

## Phase 3: Agent Spawning

**Goal:** Spawn explorer agents in parallel and synthesizer agent sequentially using the `task` tool.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 3/6] Agent Spawning** — Launching explorer agents..."

**Architecture note:** OpenCode uses isolated `task` tool calls instead of persistent teams. Explorers run in parallel (all spawned before waiting for returns). The synthesizer is spawned after all explorers complete, receiving their findings concatenated in its prompt. There is no inter-agent messaging — all context is passed via the `task` prompt parameter.

1. **Spawn all explorer agents in parallel:**

   For each focus area in the approved plan, invoke the `task` tool. Spawn all N explorers before collecting any returns (true parallelism):

   ```
   task(
     description: "Explorer [N]: [Focus area label]",
     prompt: "You are a code explorer performing focused codebase analysis.

   Analysis context: [analysis context]
   Codebase path: [PATH]

   Your focus area: [Focus area label]
   Directories to explore: [list]
   Starting files to read first: [list]
   Search patterns: [grep patterns]
   Complexity estimate: [Low/Medium/High]

   Instructions:
   - Explore your assigned focus area thoroughly using read, glob, grep, and bash
   - Document all significant findings: architecture patterns, data flows, key abstractions, dependencies
   - Note any unusual patterns, technical debt, or areas of high complexity
   - Produce a structured findings report covering: overview, key files/components, patterns observed, dependencies, notable findings
   - Be thorough — the synthesizer will rely entirely on your report

   Return your complete findings report as your final response.",
     subagent_type: "build",
     command: "code-explorer"
   )
   ```

   Repeat for each focus area, using the specific directories, starting files, and search patterns for each.

2. **Collect explorer returns:**
   - Wait for all N explorer `task` calls to return
   - Each return value contains the explorer's findings report
   - Store the findings for each explorer: `explorer_1_findings`, `explorer_2_findings`, ..., `explorer_N_findings`
   - If a task fails or returns empty: record it as a partial failure (see Error Handling — Partial Worker Failure)

3. **Track progress with todowrite** (optional scratchpad):
   Use `todowrite` to note which explorers have completed if you find it helpful for session tracking. Note: `todowrite` is a simple session-scoped scratchpad — it does not support dependencies, owners, or structured statuses. Use it only for your own reference.

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 3`, record `explorer_count`
   - For each explorer that returned successfully, write `.claude/sessions/__da_live__/explorer-{N}-findings.md` with its findings
   - Append to `progress.md`: `[timestamp] Phase 3: [N] explorers spawned and returned`

---

## Phase 4: Completeness Check

**Goal:** Verify all explorers produced substantive output before proceeding to synthesis.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 4/6] Completeness Check** — Verifying explorer outputs..."

1. Review each explorer's returned findings:
   - **If content is present and substantive**: mark as complete
   - **If a return was empty or contained an error**: treat as a failed explorer (see Error Handling — Partial Worker Failure)

2. **If any explorer failed:** Spawn a replacement explorer task targeting the gap area with a more specific prompt. Wait for the replacement to return and add its findings to the collection.

3. **If all explorers produced content**: proceed immediately to Phase 5.

4. If `ENABLE_PROGRESS = true`: Display "**[Phase 4/6] Completeness Check** — [completed]/[N] explorers valid, proceeding to synthesis"

---

## Phase 5: Evaluation and Synthesis

**Goal:** Launch synthesis agent with all explorer findings, wait for synthesized output.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 5/6] Synthesis** — Merging findings and investigating gaps..."

1. **Concatenate all explorer findings** into a single context block:

   ```
   === EXPLORER FINDINGS ===

   --- Explorer 1: [Focus area label] ---
   [explorer_1_findings]

   --- Explorer 2: [Focus area label] ---
   [explorer_2_findings]

   [... for each explorer]
   ```

2. **Spawn the synthesizer agent:**

   ```
   task(
     description: "Synthesizer: Merge and analyze all exploration findings",
     prompt: "You are a code synthesizer. Your job is to produce a unified, deeply analytical report from the exploration findings below.

   Analysis context: [analysis context]
   Codebase path: [PATH]

   Recon findings from planning phase:
   - Project structure: [brief summary of directory layout]
   - Primary language/framework: [what was detected]
   - Key areas identified: [the focus areas and why they were chosen]

   [concatenated explorer findings block from step 1]

   Instructions:
   - Synthesize all findings into a unified, coherent analysis
   - Identify cross-cutting themes, patterns, and architectural principles
   - Use bash for deep investigation of gaps — git history analysis, dependency trees, static analysis, or any investigation that read/glob/grep cannot handle
   - Evaluate completeness: are there significant areas not covered by the explorers? If so, investigate with bash
   - Resolve conflicts or inconsistencies between explorer reports
   - Produce a comprehensive final report with: executive summary, architecture overview, key findings by area, cross-cutting concerns, technical debt/risk areas, and recommendations

   Return your complete synthesis report as your final response.",
     subagent_type: "build",
     command: "code-synthesizer"
   )
   ```

3. **Collect synthesizer return:**
   - Wait for the synthesizer `task` call to return
   - The return value is the full synthesis report
   - Store as `synthesis_output`

4. **Checkpoint** (if `ENABLE_CHECKPOINTING = true`):
   - Update `.claude/sessions/__da_live__/checkpoint.md`: set `current_phase: 5`
   - Write `.claude/sessions/__da_live__/synthesis.md` with the synthesis results
   - Append to `progress.md`: `[timestamp] Phase 5: Synthesis complete`

---

## Phase 6: Completion & Cleanup

**Goal:** Collect results, present to user, and archive the session.

> If `ENABLE_PROGRESS = true`: Display "**[Phase 6/6] Completion** — Collecting results and cleaning up..."

1. **Collect synthesis output:**
   - The synthesizer's findings are in the `task` tool return value stored as `synthesis_output`
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
   - Write `explorer-{N}-findings.md` for each explorer's findings (if not already persisted from Phase 3 checkpoints)

3. **Present or return results:**
   - **Standalone invocation:** Present the synthesized analysis to the user. The results remain in conversation memory for follow-up questions.
   - **Loaded by another skill:** The synthesis is complete. Control returns to the calling workflow — do not present a standalone summary.

4. **Archive session:**
   - If `ENABLE_CHECKPOINTING = true`: Move `.claude/sessions/__da_live__/` to `.claude/sessions/da-{timestamp}/`

---

## Error Handling

### Settings Check Failure
- If `.claude/agent-alchemy.local.md` exists but is malformed or the `deep-analysis` section is unparseable: warn the user ("Settings file found but could not parse deep-analysis settings — using defaults") and proceed with default approval values.

### Planning Phase Failure
- If reconnaissance fails (errors, empty results, unusual structure): fall back to static focus area templates (Step 3b)
- If the codebase appears empty: inform the user and ask how to proceed

### Approval Phase Failure
- If maximum modification cycles (3) or regeneration cycles (2) are reached without approval: use `question` with options:
  - **"Approve current plan"** — Proceed with the latest version of the plan
  - **"Abort analysis"** — Cancel the analysis entirely

### Partial Worker Failure
- If one explorer task returns empty or errors: spawn a replacement `task` call targeting the missed focus area with a more specific prompt
- If two explorers fail: attempt replacements, but if they also fail, spawn the synthesizer with partial results and note the gaps explicitly in its prompt
- If all explorers fail: inform the user and offer to retry or abort

### Synthesizer Failure
- If the synthesizer `task` call fails or returns empty: present the raw explorer findings to the user directly
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
| **Phase 3** | Load approved plan from checkpoint, re-spawn any explorers whose findings files are missing |
| **Phase 4** | Read completed `explorer-{N}-findings.md` files from session dir. Re-spawn any explorers whose findings files are missing. |
| **Phase 5** | Load all explorer findings from session dir. Spawn a fresh synthesizer with the persisted findings in its prompt. |
| **Phase 6** | Load `synthesis.md` from session dir. Proceed directly to present/return results and cleanup. |

**Recovery procedure:**
1. Read `checkpoint.md` to determine `last_completed_phase` and session state (explorer_count, focus area details)
2. Load any persisted artifacts from the session directory (team_plan, explorer findings, synthesis)
3. Resume from Phase `last_completed_phase + 1` using the loaded state
4. For Phase 3/4 recovery: compare persisted `explorer-{N}-findings.md` files against expected explorer list to determine which explorers still need to run — only re-spawn missing ones

---

## Agent Coordination

- The lead (you) acts as the planner: performs recon, composes the task plan, handles approval, spawns agents
- Explorers run independently — no cross-explorer communication (hub-and-spoke topology enforced by task isolation)
- The synthesizer receives all explorer findings in its initial prompt — it cannot message explorers directly, but can use bash to fill gaps that explorers missed
- The synthesizer has bash access for deep investigation (git history, dependency trees, static analysis)
- Explorer tasks run in parallel — spawn all before collecting returns
- Synthesis task runs after all explorer returns are collected
- Handle agent failures gracefully — continue with partial results
- Agent count and focus area details come from the approved plan, not hardcoded values

When calling the `task` tool for explorer agents:
- Use `command: "code-synthesizer"` and `subagent_type: "build"` for the synthesizer
- Use `command: "code-explorer"` and `subagent_type: "build"` for explorers
- All context (focus area, directories, search terms, recon findings) must be included in the `prompt` parameter — there is no inter-agent messaging
- Explorer findings are returned as the task tool's return value — collect and concatenate them for the synthesizer
