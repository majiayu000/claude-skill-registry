---
name: ln-220-story-coordinator
description: "Creates, replans, or appends 5-10 Stories per Epic with standards research and multi-epic routing. Use when Epic needs Story decomposition."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# Story Coordinator

## Purpose

Coordinates Story creation (CREATE), replanning (REPLAN), and appending (ADD) for one or more Epics, producing 5-10 User Stories per Epic with standards research, Decompose-First Pattern, multi-epic routing, and delegation to ln-221/ln-222 workers.

## When to Use This Skill

Use when:
- Decompose Epic to User Stories (5-10 Stories covering Epic scope)
- Update existing Stories when Epic requirements change
- Rebalance Story scopes within Epic
- Add new Stories to existing Epic structure
- Request spans multiple Epics (routing auto-groups Stories by correct Epic)
- Story doesn't fit any existing Epic (creates stub Epic inline)

## Core Pattern: Decompose-First

**Key principle:** Build IDEAL Story plan FIRST, THEN check existing Stories to determine mode:
- **No existing Stories** → CREATE MODE (delegate to ln-221-story-creator)
- **Has existing Stories** → REPLAN MODE (delegate to ln-222-story-replanner)

**Rationale:** Ensures consistent Story decomposition based on current Epic requirements, independent of existing Story structure (may be outdated).

## Story Numbering Convention

**MANDATORY READ:** Load `shared/references/numbering_conventions.md` for Story numbering rules (US001 sequential across Epics, no Story 0).

## Quality Criteria

**MANDATORY READ:** Load `shared/references/creation_quality_checklist.md` §Story Creation Checklist for validation criteria that ln-310 will enforce.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `epicId` | Yes | args, kanban, user | Primary Epic to process |

**Resolution:** Epic Resolution Chain.
**Status filter:** Active (planned/started)
**Multi-epic:** If IDEAL plan (Phase 3) produces Stories that don't fit resolved Epic, Phase 3 Step 8 auto-routes them to correct Epics (or creates stub Epics inline).

## Workflow

### Phase 0: Tools Config

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider

### Phase 1: Context Assembly

**Objective:** Gather context for Story planning (Epic details, planning questions, frontend context, fallback docs, user input)

**Step 1: Discovery (Automated)**

Auto-discovers from `docs/tasks/kanban_board.md`:

1. **Resolve epicId:** Run Epic Resolution Chain per guide.
2. **Team ID:** Reads Linear Configuration table
3. **Load Epic description:**
   - **IF task_provider == "linear":** `get_project(query="Epic N")` → Fetch full Epic document
   - **ELSE:** `Read("docs/tasks/epics/epic-{N}-*/epic.md")` → Load file-based Epic
   - **Extract:** Goal, Scope In/Out, Success Criteria, Technical Notes
   - **Note:** Epic N = Linear Project number (global), NOT initiative-internal index (Epic 0-N)
4. **Next Story Number:** Reads Epic Story Counters table → Gets next sequential number

**Step 2: Load Active Epics Metadata**

Load ALL active Epics from `docs/tasks/kanban_board.md` → Epics Overview section:
- Extract: Epic number, title for each active Epic
- Store as `allEpics[]` for Phase 3 Epic Routing (Step 8)
- Lightweight: titles from kanban only, NOT full Epic documents

**Step 3: Extract Planning Information (Automated)**

Parses Epic structure for Story planning questions:

| Question | Extraction Source |
|----------|-------------------|
| **Q1 - User/Persona** | Epic Goal ("Enable [persona]...") + Scope In (user roles) |
| **Q2 - What they want** | Epic Scope In (capabilities) + functional requirements |
| **Q3 - Why it matters** | Epic Success Criteria (metrics) + Goal (business value) |
| **Q4 - Which Epic** | Already from Step 1 |
| **Q5 - Main AC** | Derive from Epic Scope In features → testable scenarios |
| **Q6 - Application type** | Epic Technical Notes (UI/API mentioned) → Default: API |

**Step 4: Frontend Research (Optional)**

**Trigger:** If Q2 (capabilities) OR Q5 (AC) missing after Step 3

**Process:**
1. Scan HTML files: `Glob` `**/*.html`, `src/**/*.html`
2. Extract: forms → AC scenarios, buttons → capabilities, validation rules → edge case AC
3. Combine with Epic context, deduplicate, prioritize Epic AC if conflict

**Fallback:** If no HTML → Skip to Step 5

**Step 5: Fallback Search Chain**

**Objective:** Fill missing Q1-Q6 BEFORE asking user.

For each question with no answer from Step 3-4:

| Question | Fallback Search |
|----------|-----------------|
| **Q1 (User/Persona)** | Search `requirements.md` for "User personas", "Actors" → Default "User" if not found |
| **Q3 (Why it matters)** | Search `requirements.md` for "Business objectives", "Goals" → Infer from Epic Success Criteria |
| **Q6 (Application type)** | Search `tech_stack.md` for "Frontend", "Backend", "API" → Default "API" |

**Skip:** Q2, Q5 (Epic + HTML are sources of truth), Q4 (already known)

**Step 6: User Input (Only if Missing)**

**If still missing after Step 3 + 4 + 5:**
- Show extracted: "From Epic: [Epic info]. From HTML: [HTML info]. From fallback: [fallback info]"
- Ask user to confirm or provide remaining missing details

**If all questions answered from Epic OR HTML OR fallback:** Skip user prompts, proceed to Phase 2

**Output:** Complete context (Epic details, next Story number, Q1-Q6 answers)

---

### Phase 2: Standards Research (Inline)

**MANDATORY READ:** Load `shared/references/research_methodology.md`, `shared/references/research_tool_fallback.md`, `shared/references/documentation_creation.md`

**Objective:** Research industry standards/patterns BEFORE Story generation.

**Process:**
1. **Stack Detection:** per `shared/references/documentation_creation.md` stack table
2. **Domain extraction:** Parse Epic goal/Scope In for domain keywords
3. **MCP Ref Research:**
   - Standards: `ref_search_documentation(query="[prefix] [domain] RFC standard specification")`
   - Patterns: `ref_search_documentation(query="[prefix] [domain] architectural patterns best practices")`
4. **Scan existing guides:** `Glob("docs/guides/*.md")` → match by domain
5. **Generate Standards Research** — per research_methodology.md Summary Template (tables, no code)
6. **Save:** `docs/research/rsh-{NNN}-{slug}.md` per `shared/references/documentation_creation.md` naming
7. **Store** for Phase 5a/5b workers (Technical Notes only, never ACs)

**Output contract:** Phase 2 MUST return `{ standards_research: string, file_path: string }` — cached for all Stories in Epic.

**Skip conditions:** No standards in Technical Notes, trivial CRUD, explicit skip
**Time-box:** 10-15 minutes

---

### Phase 3: Planning

**Objective:** Build IDEAL Story plan, determine execution mode

**Story Grouping Guidelines:**

Each Story = ONE vertical slice of user capability (end-to-end: UI → API → Service → DB). Size limits per `creation_quality_checklist.md` #9.

| Pattern | Example | Verdict |
|---------|---------|---------|
| Vertical slice (1 user journey) | "User registration" (form→API→DB→email) | GOOD Story |
| Horizontal slice (1 layer) | "Create user table", "Registration API endpoint" | BAD → Task, not Story |
| Incremental DB (per Story) | "Product search" → creates Products table | GOOD |
| Big-bang DB (all upfront) | "Setup database" → creates 50 tables | BAD → no user value |

**Build IDEAL Plan (Automated):**

1. **Articulate REAL GOAL:** **MANDATORY READ:** `shared/references/goal_articulation_gate.md` — State REAL GOAL of this Epic in one sentence (the user capability being enabled, not "create Stories"). Verify: does the decomposition serve THIS goal?
2. **Analyze Epic Scope:** Review features in Epic Scope In, identify user capabilities
3. **Scope Minimalism Gate (MANDATORY):**

   After analyzing Epic Scope, challenge the AGGREGATE design BEFORE generating Stories. Each test is pass/fail.

   | Test | Rule | FAIL action |
   |------|------|-------------|
   | **Cart Test** | State the simplest design that delivers the Epic Goal in one sentence. If you cannot — scope too wide, split Epic. | STOP. Return to Epic coordinator for split. |
   | **AC Count Test** | Projected ACs across all Stories: divide total by Story count. If average > 5 per Story — over-scoped. | Reduce: cut speculative ACs until average <= 5. |
   | **AC Purity Test** | Every AC must describe OBSERVABLE USER BEHAVIOR (Given user does X, Then user sees Y). ACs that describe system internals (lookup priority, cache layers, endpoint URLs) are Technical Notes, not ACs. | Move to Technical Notes. |
   | **Feature Bundling Test** | Epic Goal contains "and", "&", "+" joining DISTINCT capabilities? Each distinct capability = separate Story. Title "X and Y" = 2 Stories minimum. | Split into separate Stories. |
   | **Research Firewall** | Standards Research (Phase 2) informs Technical Notes ONLY. Research MUST NOT add ACs, endpoints, or features. ACs come from Epic Scope In alone. | Remove research-driven ACs. |

   **Anti-pattern (real example):**
   - Story "Translation Memory AND Response Cache" → FAIL Feature Bundling (2 distinct capabilities bundled)
   - 10 ACs with "5-level lookup priority" → FAIL AC Purity (system architecture, not user behavior)
   - Research found "industry does segment matching at 75%" → added AC for it → FAIL Research Firewall (not in Epic Scope In)

   **Pass:** All 5 tests pass → proceed to Step 4.
   **Fail ANY:** Fix before proceeding. Do NOT generate Stories from an over-scoped plan.

4. **Determine Story Count:**
   - Simple Epic (1-3 features): 3-5 Stories
   - Medium Epic (4-7 features): 6-8 Stories
   - Complex Epic (8+ features): 8-10 Stories
   - **Max 10 Stories per Epic**

5. **Story Size:** Limits per `creation_quality_checklist.md` #9. Outside range → split or merge.

6. **Build IDEAL Plan "in mind":**
   - Each Story: persona + capability + business value
   - Each Story: testable AC per checklist #4 (3-5 ACs, user behavior only)
   - Stories ordered by dependency (no forward deps per checklist #18)
   - Each Story: Test Strategy section exists but is **empty** (tests planned later by test planner)
   - Each Story: Technical Notes (architecture, integrations, **Standards Research from Phase 2**, guide links)
   - **Research Firewall (per Step 3):** research → Technical Notes only, never ACs
   - Each Story: `orchestratorBrief` for ln-1000 pipeline lead:
     ```
     orchestratorBrief: {
       tech: "<languages, frameworks, key libraries from Epic context>",
       keyFiles: "<2-5 files/dirs most affected>",
       approach: "<1-line implementation strategy>",
       complexity: "Low|Medium|High (<reason>)"
     }
     ```

7. **AC Quality Validation:** Rules per `creation_quality_checklist.md` #4. Workers (ln-221, ln-222) must validate.

**INVEST Score (0-6 per Story):** Validate per `creation_quality_checklist.md` INVEST criteria (loaded above). Gate: Score ≥ 4 → proceed, < 4 → rework.

8. **Epic Routing**

**Objective:** Ensure each Story in IDEAL plan is assigned to the correct Epic. Handles multi-epic requests and missing Epics.

**Process:** Routing always runs (keyword matching is cheap). After tagging, if ALL Stories match `resolvedEpicId` → SINGLE-EPIC fast path (common case).

**Routing (multiple active Epics):**

```
FOR EACH Story in IDEAL plan:
  1. Compare Story domain/capability keywords vs resolved Epic Scope In
     - IF match → tag Story with resolvedEpicId
  2. ELSE compare vs allEpics[] scopes (load Epic descriptions on-demand for ambiguous matches)
     - IF matches another Epic → tag with that epicId
     - IF matches NO Epic → tag as NEEDS_NEW_EPIC

ANALYZE tags:
  - ALL resolvedEpicId → SINGLE-EPIC (proceed as before)
  - Mixed tags → MULTI-EPIC:
    a. Group: epicGroups = {epicId: Story[]}
    b. Show ROUTING PREVIEW (see format below)
    c. User confirms or reassigns Stories
    d. NEEDS_NEW_EPIC Stories → create stub Epic inline:
       1. Read kanban_board.md → Next Epic Number, teamId
       2. Create Epic (Linear: save_project, File: mkdir + Write minimal epic.md)
       3. Update kanban_board.md: increment Next Epic Number, add Epic Story Counters row, add to Epics Overview → Active
       4. Assign returned epicId to tagged Stories
```

**Routing Preview Format:**
```
EPIC ROUTING PREVIEW

Epic 7 (OAuth Authentication): 4 Stories
  - US004: Register OAuth client
  - US005: Request access token
  - US006: Validate token
  - US007: Refresh token

Epic 12 (User Management): 2 Stories
  - US008: User profile settings
  - US009: Account deletion

NEW EPIC NEEDED: 1 Story
  - US010: Payment webhook handler
    Suggested domain: Payment Processing

Confirm routing? (or reassign Stories between Epics)
```

**Output:** `epicGroups` — map of epicId to Story[] (for single-epic: one group with all Stories)

---

### Phase 4: Check Existing & Detect Mode

**Objective:** Determine execution mode based on existing Stories AND user intent, per each Epic group from Phase 3 routing.

**Process:** FOR EACH epicGroup in `epicGroups`, query task provider for existing Stories:

**IF task_provider == "linear":**
```
list_issues(project=epicGroup.epicId, label="user-story")
```

**ELSE (file mode):**
```
Glob("docs/tasks/epics/epic-{N}-*/stories/*/story.md")
```

**Mode Detection (per epicGroup):**

1. **Analyze user request** for keywords:
   - ADD keywords: "add story", "one more story", "additional story", "append"
   - REPLAN keywords: "update plan", "revise", "requirements changed", "replan stories"

2. **Decision matrix:**

| Condition | Mode | Delegate To |
|-----------|------|-------------|
| Count = 0 | **CREATE** | Phase 5a: ln-221-story-creator |
| Count ≥ 1 AND ADD keywords | **ADD** | Phase 5c: ln-221-story-creator (appendMode) |
| Count ≥ 1 AND REPLAN keywords | **REPLAN** | Phase 5b: ln-222-story-replanner |
| Count ≥ 1 AND ambiguous | **ASK USER** | "Add new Story or revise the plan?" |

**Important:** Orchestrator loads metadata ONLY (ID, title, status). Workers load FULL descriptions (token efficiency).

**Output:** `epicGroupModes` — map of epicId to {mode, existingCount, epicData} for each group

---

### Phase 5: Delegate to Workers

**Iteration:** Process each epicGroup sequentially (workers include user interaction, cannot parallelize).

```
FOR EACH epicGroup in epicGroupModes:
  IF mode == CREATE  → Phase 5a (ln-221-story-creator)
  IF mode == REPLAN  → Phase 5b (ln-222-story-replanner)
  IF mode == ADD     → Phase 5c (ln-221-story-creator, appendMode)
```

Workers receive the same interface: `epicData + idealPlan` for ONE Epic.

#### Phase 5a: Delegate CREATE (No Existing Stories)

**Trigger:** Epic has no Stories yet (first decomposition)

**Delegation:**

Call ln-221-story-creator via Skill tool:

```javascript
Skill(
  skill: "ln-221-story-creator",
  epicData: {id, title, description},
  idealPlan: [ /* 5-10 Stories from Phase 3 */ ],
  standardsResearch: "Standards Research from Phase 2",
  teamId: "team-id",
  autoApprove: false  // or true for automation
)
```

**Worker handles:**
- Generate Story documents (9 sections, insert Standards Research)
- Validate INVEST criteria
- Show preview
- User confirmation (if autoApprove=false)
- Create in Linear (project=Epic, labels=user-story, state=Backlog)
- Update kanban_board.md (Epic Grouping Algorithm)

**Output:** Created Story URLs + summary from worker

---

#### Phase 5b: Delegate REPLAN (Existing Stories Found)

**MANDATORY READ:** Load `references/replan_algorithm.md`

**Trigger:** Epic already has Stories (requirements changed)

**Delegation:**

Call ln-222-story-replanner via Skill tool:

```javascript
Skill(
  skill: "ln-222-story-replanner",
  epicData: {id, title, description},
  idealPlan: [ /* 5-10 Stories from Phase 3 */ ],
  standardsResearch: "Standards Research from Phase 2",
  existingCount: N,
  teamId: "team-id",
  autoApprove: false  // or true for automation
)
```

**Worker handles:**
- Load existing Stories (Progressive Loading: ONE BY ONE for token efficiency)
- Compare IDEAL vs existing (KEEP/UPDATE/OBSOLETE/CREATE operations)
- Show replan summary with diffs (AC, Standards Research, Technical Notes)
- User confirmation (if autoApprove=false)
- Execute operations (respecting status constraints: Backlog/Todo only, warnings for In Progress/Review/Done)
- Update kanban_board.md (add NEW Stories only via Epic Grouping Algorithm)

**Output:** Operation results + warnings + affected Story URLs from worker

---

#### Phase 5c: Delegate ADD (Append to Existing Stories)

**Trigger:** Epic has Stories, user wants to ADD more (not replan existing)

**Delegation:**

Call ln-221-story-creator via Skill tool with appendMode:

```javascript
Skill(
  skill: "ln-221-story-creator",
  appendMode: true,  // ADD to existing, don't replace
  epicData: {id, title, description},
  newStoryDescription: userRequestedStory,  // Single Story from user request
  standardsResearch: "Standards Research from Phase 2",
  teamId: "team-id",
  autoApprove: false
)
```

`appendMode: true` — creates only user-requested Story(s), skips IDEAL plan comparison.

**Worker handles:**
- Research standards for NEW Story only
- Generate Story document (9 sections)
- Validate INVEST criteria
- Create in Linear (append to existing)
- Update kanban_board.md

**Output:** Created Story URL + summary from worker

---

### Phase 6: Commit

After ALL workers complete (any mode: CREATE/REPLAN/ADD):

1. `git add docs/tasks/kanban_board.md` (updated by worker)
2. `git commit` with message:
   - **Single-epic:** `"ln-220: create Stories US{first}-US{last} for Epic {N}"`
   - **Multi-epic:** `"ln-220: create Stories for Epics {N1}, {N2}, {N3}"`
   - REPLAN: `"ln-220: replan Stories for Epic {N}"`
   - ADD: `"ln-220: add Story US{num} to Epic {N}"`

---

### Phase 7: Self-Check

**Objective:** Verify all skill phases completed and all planned Stories accounted for.

**Process:**

1. **Phase Completion:** Verify Phases 0-6 completed (or skipped with documented reason). Report any missed phase.

2. **Story Accounting:**
   - Planned Stories (from IDEAL plan): N
   - Created/updated Stories (from worker results): M
   - IF N ≠ M → WARNING: list missing Stories by title

3. **Epic Routing Verification (multi-epic only):**
   - Verify all epicGroups processed by workers
   - Verify all NEEDS_NEW_EPIC Stories resolved (assigned to created Epics)

4. **Output:**
```
SELF-CHECK RESULTS

Phases: 7/7 completed (or K/7 + skipped reasons)
Stories: M/N created
Epics: K epic(s) processed

Status: PASS / FAIL (with details)
```

IF FAIL → list which Stories were lost, recommend re-running for missed epicGroups.

---

**TodoWrite format (mandatory):**
Add phases to todos before starting:
```
- Phase 1: Context Assembly (in_progress)
- Phase 2: Standards Research — inline (pending)
- Phase 3: Build IDEAL Story Plan + Epic Routing (pending)
- Phase 4: Check Existing Stories (pending)
- Phase 5: Delegate to ln-221/ln-222 (pending)
- Wait for worker result (pending)
- Phase 6: Commit kanban changes (pending)
- Phase 7: Self-Check (pending)
```
Mark each as in_progress when starting, completed when done.

---

## Critical Rules

- **Decompose-First:** Build IDEAL Story plan before checking existing Stories (prevents anchoring to suboptimal structure)
- **Vertical slicing only:** Each Story = one user journey end-to-end (UI -> API -> Service -> DB); no horizontal/technical-only Stories
- **Scope Minimalism Gate:** Phase 3 Step 3 must pass before Story generation. >5 ACs per Story = mandatory split. ACs describe user behavior only, not system internals
- **Standards research before generation:** Phase 2 (inline research) must complete before Story documents are created; results go into all Story Technical Notes (never into ACs)
- **Orchestrator loads metadata only:** ID, title, status (~50 tokens per Story); workers load full descriptions (~5,000 tokens) when needed
- **Test Strategy section left empty:** Tests are planned later by test planner, not at Story creation time
- **Epic Routing fast path:** Routing always runs. If all Stories match resolved Epic (common case), no user confirmation needed and zero branching overhead (Phase 3 Step 8)
- **Self-Check mandatory:** Phase 7 always runs. Verifies N planned == M created, all phases completed. Never skipped

---

## Integration with Ecosystem

**Calls:**
- **ln-221-story-creator** (Phase 5a, 5c) - CREATE and ADD worker
- **ln-222-story-replanner** (Phase 5b) - REPLAN worker

**Called by:**
- **ln-200-scope-decomposer** (Phase 3) - automated full decomposition (scope → Epics → Stories)
- **Manual** - user invokes for Epic Story creation/replanning

**Upstream:**
- **ln-210-epic-coordinator** - creates Epics (prerequisite for Story creation)

**Downstream:**
- **ln-300-task-coordinator** - creates implementation tasks for each Story
- **ln-310-multi-agent-validator** - validates Story structure/content
- **ln-400-story-executor** - orchestrates task execution for Story

---

## Definition of Done

**✅ Phase 1: Context Assembly Complete:**
- [ ] Team ID, Epic number, Next Story Number loaded from kanban_board.md
- [ ] Q1-Q6 extracted from Epic (Step 3)
- [ ] Frontend Research attempted if Q2/Q5 missing (Step 4)
- [ ] Fallback Search attempted for missing info (Step 5)
- [ ] User input requested if still missing (Step 6)
- [ ] Complete Story planning context assembled

**✅ Phase 2: Standards Research Complete:**
- [ ] Epic parsed for domain keywords
- [ ] Standards research executed inline with MCP Ref
- [ ] Standards Research cached for workers
- [ ] OR Phase 2 skipped (trivial CRUD, no standards, explicit skip)

**✅ Phase 3: Planning + Routing Complete:**
- [ ] Epic Scope analyzed
- [ ] Optimal Story count determined (5-10 Stories)
- [ ] IDEAL Story plan created (titles, statements, core AC, ordering)
- [ ] Story Grouping Guidelines validated (vertical slicing)
- [ ] INVEST checklist validated for all Stories
- [ ] Epic Routing executed (Step 8): fast path OR multi-epic grouping confirmed by user
- [ ] NEEDS_NEW_EPIC resolved (if any): stub Epic(s) created inline

**✅ Phase 4: Check Existing Complete:**
- [ ] Queried task provider for existing Stories per epicGroup
- [ ] Execution mode determined per epicGroup (CREATE/REPLAN/ADD)

**✅ Phase 5: Delegation Complete:**
- [ ] Called ln-221/ln-222 per epicGroup via Skill tool
- [ ] Passed epicData, idealPlan, standardsResearch, teamId, autoApprove
- [ ] Received output from each worker (Story URLs + summary + next steps)

**✅ Phase 6: Commit Complete:**
- [ ] Kanban board changes committed with descriptive message

**✅ Phase 7: Self-Check Complete:**
- [ ] All phases verified (completed or explicitly skipped with reason)
- [ ] Story count matches: planned == created/updated
- [ ] No Stories lost in routing (multi-epic scenarios)
- [ ] Summary displayed with PASS/FAIL status

---

## Example Usage

**CREATE MODE (First Time):**
```
"Create stories for Epic 7: OAuth Authentication"
```

**Process:**
1. Phase 1: Context Assembly → Discovery (Team "API", Epic 7, US004), Extract (Persona: API client, Value: secure API access), Frontend Research (HTML login/register forms → AC), Fallback Search (requirements.md for personas)
2. Phase 2: Standards Research → Epic mentions "OAuth 2.0", inline MCP Ref research → Standards Research with RFC 6749, patterns
3. Phase 3: Planning → Build IDEAL (5 Stories: "Register client", "Request token", "Validate token", "Refresh token", "Revoke token")
4. Phase 4: Check Existing → Count = 0 → CREATE MODE
5. Phase 5a: Delegate CREATE → Call ln-221-story-creator → US004-US008 created with Standards Research

**REPLAN MODE (Requirements Changed):**
```
"Replan stories for Epic 7 - removed custom token formats, added scope management"
```

**Process:**
1. Phase 1: Context Assembly → Discovery (Team "API", Epic 7, has US004-US008), Extract (Removed custom formats, added scopes)
2. Phase 2: Standards Research → Epic mentions "OAuth 2.0 scopes", inline MCP Ref → Updated Standards Research with RFC 6749 Section 3.3
3. Phase 3: Planning → Build IDEAL (5 Stories: "Register client", "Request token", "Validate token", "Refresh token", "Manage scopes")
4. Phase 4: Check Existing → Count = 5 → REPLAN MODE
5. Phase 5b: Delegate REPLAN → Call ln-222-story-replanner → KEEP 4, UPDATE Technical Notes (scope research), OBSOLETE US008, CREATE US009

**MULTI-EPIC MODE (Stories span multiple Epics):**
```
"Create stories for user authentication and payment processing"
```

**Process:**
1. Phase 1: Context Assembly → Discovery (resolve to Epic 7: Auth), Step 2 loads allEpics [Epic 7, Epic 12, Epic 14]
2. Phase 2: Standards Research → Inline MCP Ref research for auth + payment standards
3. Phase 3: Planning → 8 Stories planned. Step 8 Routing → 5 Stories match Epic 7 (Auth), 3 Stories match Epic 12 (Payments). Routing preview shown, user confirms
4. Phase 4: Check Existing per epicGroup → Epic 7: count=0 (CREATE), Epic 12: count=3 (REPLAN)
5. Phase 5: Delegate CREATE to ln-221 for Epic 7 (5 Stories), then REPLAN to ln-222 for Epic 12 (3 Stories)
6. Phase 6: Commit → `"ln-220: create Stories for Epics 7, 12"`
7. Phase 7: Self-Check → 8/8 Stories created, 2 Epics processed, PASS

---

## Phase 8: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after all phases complete. Output to chat using the `planning-coordinator` format.

## Reference Files

- **MANDATORY READ:** `shared/references/tools_config_guide.md`
- **MANDATORY READ:** `shared/references/storage_mode_detection.md`
- **[MANDATORY] Problem-solving approach:** `shared/references/problem_solving.md`
- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`
- **Decompose-first pattern:** `shared/references/decompose_first_pattern.md`
- **Numbering conventions:** `shared/references/numbering_conventions.md` (Story sequential across Epics)

---

**Version:** 5.0.0
**Last Updated:** 2026-02-03
