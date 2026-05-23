---
name: teams-deep-analysis
description: Team-based deep exploration and synthesis workflow using Agent Teams with dynamic planning and hub-and-spoke coordination. Use when asked for "teams deep analysis", "team-based analysis", "collaborative analysis", or "teams-deep-analysis".
argument-hint: <analysis-context or focus-area>
model: inherit
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Bash, Task, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage, AskUserQuestion
---

# Teams Deep Analysis Workflow

Execute a structured exploration + synthesis workflow using Agent Teams with hub-and-spoke coordination. The lead performs rapid reconnaissance to generate dynamic focus areas, workers explore independently, and a deep synthesizer merges findings with Bash-powered investigation.

This skill can be invoked standalone or loaded by other skills as a reusable building block.

## Phase 1: Planning

**Goal:** Perform codebase reconnaissance, generate dynamic focus areas, create the team, and assign tasks.

1. **Determine analysis context:**
   - If `$ARGUMENTS` is provided, use it as the analysis context (feature area, question, or general exploration goal)
   - If no arguments and this skill was loaded by another skill, use the calling skill's context
   - If no arguments and standalone invocation, set context to "general codebase understanding"
   - Set `PATH = current working directory`
   - Inform the user: "Exploring codebase at: `PATH`" with the analysis context

2. **Load skills for this phase** (standalone or within tools plugin only):
   - If invoked standalone or from within the tools plugin:
     - Read `${CLAUDE_PLUGIN_ROOT}/skills/project-conventions/SKILL.md` and apply its guidance
     - Read `${CLAUDE_PLUGIN_ROOT}/skills/language-patterns/SKILL.md` and apply its guidance
   - If loaded cross-plugin (`${CLAUDE_PLUGIN_ROOT}` does not contain these skills): Skip this step — the explorer agents load project-conventions and language-patterns automatically via their agent definitions

3. **Rapid codebase reconnaissance:**
   Use Glob, Grep, and Read to quickly map the codebase structure. This should take 1-2 minutes, not deep investigation.

   - **Directory structure:** List top-level directories with `Glob` (e.g., `*/` pattern) to understand the project layout
   - **Language and framework detection:** Read config files (`package.json`, `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.) to identify primary language(s) and framework(s)
   - **File distribution:** Use `Glob` with patterns like `src/**/*.ts`, `**/*.py` to gauge the size and shape of different areas
   - **Key documentation:** Read `README.md`, `CLAUDE.md`, or similar docs if they exist for project context
   - **For feature-focused analysis:** Use `Grep` to search for feature-related terms (function names, component names, route paths) to find hotspot directories
   - **For general analysis:** Identify the 3-5 largest or most architecturally significant directories

   **Fallback:** If reconnaissance fails (empty project, unusual structure, errors), use the static focus area templates from Step 4b.

4. **Generate dynamic focus areas:**

   Based on reconnaissance findings, create 3 focus areas tailored to the actual codebase.

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

5. **Create the team:**
   - Use `TeamCreate` with name `deep-analysis-{timestamp}` (e.g., `deep-analysis-1707300000`)
   - Description: "Deep analysis of [analysis context]"

6. **Spawn teammates:**
   Use the Task tool with the `team_name` parameter to spawn 4 teammates:

   - **3 workers** — `subagent_type: "claude-alchemy-tools:team-code-explorer"`, model: sonnet
     - Named: `explorer-1`, `explorer-2`, `explorer-3`
     - Prompt each with: "You are part of a deep analysis team. Wait for your task assignment. The codebase is at: [PATH]. Analysis context: [context]"

   - **1 deep synthesizer** — `subagent_type: "claude-alchemy-tools:team-deep-synthesizer"`, model: opus
     - Named: `synthesizer`
     - Prompt with: "You are the deep synthesizer for a deep analysis team. You have Bash access for git history, dependency analysis, and static analysis. Wait for your task assignment. The codebase is at: [PATH]. Analysis context: [context]"

7. **Create tasks:**
   Use `TaskCreate` for each task:

   - **Exploration Task 1:** Subject: "Explore: [Focus 1 label]", Description: detailed exploration instructions including directories, starting files, search terms, and complexity estimate
   - **Exploration Task 2:** Subject: "Explore: [Focus 2 label]", Description: detailed exploration instructions including directories, starting files, search terms, and complexity estimate
   - **Exploration Task 3:** Subject: "Explore: [Focus 3 label]", Description: detailed exploration instructions including directories, starting files, search terms, and complexity estimate
   - **Synthesis Task:** Subject: "Synthesize and evaluate exploration findings", Description: "Merge and synthesize findings from all 3 exploration tasks into a unified analysis. Investigate gaps using Bash (git history, dependency trees). Evaluate completeness before finalizing."
     - Use `TaskUpdate` to set `addBlockedBy` pointing to all 3 exploration task IDs

8. **Assign exploration tasks:**
   Use `TaskUpdate` to assign:
   - Exploration Task 1 → `owner: "explorer-1"`
   - Exploration Task 2 → `owner: "explorer-2"`
   - Exploration Task 3 → `owner: "explorer-3"`

---

## Phase 2: Focused Exploration

**Goal:** Workers explore their assigned areas independently.

- Workers explore their assigned focus areas independently — no cross-worker messaging
- Workers can respond to follow-up questions from the deep synthesizer
- Each worker marks its task as completed when done
- You (the lead) receive idle notifications as workers finish
- **Wait for all 3 exploration tasks to be marked complete** before proceeding to Phase 3

---

## Phase 3: Evaluation and Synthesis

**Goal:** Verify exploration completeness, launch synthesis with deep investigation.

### Step 1: Structural Completeness Check

This is a structural check, not a quality assessment:

1. Use `TaskList` to verify all 3 exploration tasks are completed
2. Check that each worker produced a report with content (review the messages/reports received)
3. **If a worker failed completely** (empty or error output):
   - Create a follow-up exploration task targeting the gap
   - Assign it to an idle worker
   - Add the new task to the synthesis task's `blockedBy` list
   - Wait for the follow-up task to complete
4. **If all 3 produced content**: proceed immediately to Step 2

### Step 2: Launch Synthesis

1. Use `TaskUpdate` to assign the synthesis task: `owner: "synthesizer"`
2. Send the deep synthesizer a message with exploration context and recon findings:
   ```
   SendMessage type: "message", recipient: "synthesizer",
   content: "All 3 exploration tasks are complete. Your synthesis task is now assigned.

   Analysis context: [analysis context]
   Codebase path: [PATH]

   Recon findings from planning phase:
   - Project structure: [brief summary of directory layout]
   - Primary language/framework: [what was detected]
   - Key areas identified: [the 3 focus areas and why they were chosen]

   The workers are: explorer-1, explorer-2, explorer-3. You can message them with follow-up questions if you find conflicts or gaps in their findings.

   You have Bash access for deep investigation — use it for git history analysis, dependency trees, static analysis, or any investigation that Read/Glob/Grep can't handle.

   Read the completed exploration tasks via TaskGet to access their reports, then synthesize into a unified analysis. Evaluate completeness before finalizing.",
   summary: "Synthesis task assigned, begin work"
   ```
3. Wait for the deep synthesizer to mark the synthesis task as completed

---

## Phase 4: Completion + Cleanup

**Goal:** Collect results, present to user, and tear down the team.

1. **Collect synthesis output:**
   - The deep synthesizer's findings are in the messages it sent and/or the task completion output
   - Read the synthesis results

2. **Present or return results:**
   - **Standalone invocation:** Present the synthesized analysis to the user. The results remain in conversation memory for follow-up questions.
   - **Loaded by another skill:** The synthesis is complete. Control returns to the calling workflow — do not present a standalone summary.

3. **Shutdown teammates:**
   Send shutdown requests to all 4 teammates:
   ```
   SendMessage type: "shutdown_request", recipient: "explorer-1", content: "Analysis complete"
   SendMessage type: "shutdown_request", recipient: "explorer-2", content: "Analysis complete"
   SendMessage type: "shutdown_request", recipient: "explorer-3", content: "Analysis complete"
   SendMessage type: "shutdown_request", recipient: "synthesizer", content: "Analysis complete"
   ```

4. **Cleanup team:**
   - Use `TeamDelete` to remove the team and its task list

---

## Error Handling

### Planning Phase Failure
- If reconnaissance fails (errors, empty results, unusual structure): fall back to static focus area templates (Step 4b)
- If the codebase appears empty: inform the user and ask how to proceed

### Partial Worker Failure
- If one worker fails: create a follow-up task targeting the missed focus area, assign to an idle worker, add to synthesis `blockedBy`
- If two workers fail: attempt follow-ups, but if they also fail, instruct the deep synthesizer to work with partial results
- If all workers fail: inform the user and offer to retry or abort

### Deep Synthesizer Failure
- If the deep synthesizer fails: present the raw exploration results to the user directly
- Offer to retry synthesis or let the user work with partial results

### General Failures
If any phase fails:
1. Explain what went wrong
2. Ask the user how to proceed:
   - Retry the phase
   - Continue with partial results
   - Abort the analysis

---

## Agent Coordination

- The lead (you) acts as the planner: performs recon, generates focus areas, assigns work
- Workers explore independently — no cross-worker messaging (hub-and-spoke topology)
- The deep synthesizer can ask workers follow-up questions to resolve conflicts and fill gaps
- The deep synthesizer has Bash access for deep investigation (git history, dependency trees, static analysis)
- Wait for task dependencies to resolve before proceeding
- Handle agent failures gracefully — continue with partial results

When calling Task tool for teammates:
- Use `model: "opus"` for the deep synthesizer
- Use default model (sonnet) for workers
- Always include `team_name` parameter to join the team
