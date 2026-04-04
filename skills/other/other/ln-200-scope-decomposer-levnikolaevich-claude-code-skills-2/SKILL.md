---
name: ln-200-scope-decomposer
description: "Decomposes scope into Epics, Stories, and RICE priorities. Use when user has project scope and wants full Agile breakdown."
disable-model-invocation: true
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Scope Decomposer (Top Orchestrator)

**Type:** L1 Top Orchestrator
**Category:** 2XX Planning

Top-level orchestrator for complete initiative decomposition from scope to User Stories through Epic and Story coordinators.

## Purpose

### What This Skill Does

Coordinates the complete decomposition pipeline for new initiatives:
- Auto-discovers Team ID from kanban_board.md
- **Phase 1:** Discovery (Team ID)
- **Phase 2:** Epic Decomposition (delegates to ln-210-epic-coordinator)
- **Phase 3:** Story Decomposition Loop (delegates to ln-220-story-coordinator per Epic, sequential)
- **Phase 4:** RICE Prioritization Loop (optional, delegates to ln-230-story-prioritizer per Epic, sequential)
- **Phase 5:** Summary (total counts + next steps)

## Runtime Contract

**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/scope_decomposition_runtime_contract.md`, `shared/references/scope_decomposition_summary_contract.md`, `shared/references/epic_plan_summary_contract.md`, `shared/references/coordinator_summary_contract.md`

Runtime family: `scope-decomposition-runtime`

Identifier:
- scope identifier

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_EPIC_DECOMPOSITION`
4. `PHASE_3_STORY_LOOP`
5. `PHASE_4_PRIORITIZATION_LOOP`
6. `PHASE_5_FINALIZE`
7. `PHASE_6_SELF_CHECK`

Coordinator summary contract:
- consume `epic-plan` from `ln-210`
- consume `story-plan` from `ln-220`
- keep prioritization loop progress as machine-readable checkpoints

## Worker Invocation (MANDATORY)

```text
Skill(skill: "ln-210-epic-coordinator", args: "{scopeDoc}")
Skill(skill: "ln-220-story-coordinator", args: "{epicId}")
Skill(skill: "ln-230-story-prioritizer", args: "{epicId}")
```

## TodoWrite format (mandatory)

```text
- Phase 1: Discover top-level scope context (pending)
- Phase 2: Run Epic decomposition (pending)
- Phase 3: Run sequential Story loop (pending)
- Phase 4: Run optional prioritization loop (pending)
- Phase 5: Finalize scope summary (pending)
- Phase 6: Self-check (pending)
```

### When to Use This Skill

This skill should be used when:
- Start new initiative requiring full decomposition (scope → Epics → Stories)
- Automate Epic + Story creation in single workflow
- Prefer full pipeline over manual step-by-step invocation
- Time-efficient approach for new projects (2-3 hours end-to-end)

**Alternative:** For granular control, invoke coordinators manually:
1. [ln-210-epic-coordinator](../ln-210-epic-coordinator/SKILL.md) - CREATE/REPLAN Epics
2. [ln-220-story-coordinator](../ln-220-story-coordinator/SKILL.md) - CREATE/REPLAN Stories (once per Epic)
3. [ln-230-story-prioritizer](../ln-230-story-prioritizer/SKILL.md) - RICE prioritization (once per Epic)

### When NOT to Use

Do NOT use if:
- Initiative already has Epics → Use ln-210-epic-coordinator REPLAN mode instead
- Need to replan existing Stories → Use ln-220-story-coordinator REPLAN mode per Epic
- Only need Epic creation → Use ln-210-epic-coordinator directly
- Only need Story creation for specific Epic → Use ln-220-story-coordinator directly

---

## Core Concepts

### Orchestrator Pattern

**ln-200-scope-decomposer is a pure coordinator** - it does NOT execute work directly:
- ✅ Discovers context (Team ID)
- ✅ Makes routing decisions (which coordinator to invoke)
- ✅ Delegates all work via Skill tool (ln-210, ln-220, ln-230)
- ✅ Manages workflow state (Epic creation → Story loop)
- ❌ Does NOT research project docs (ln-210 does this)
- ❌ Does NOT generate Epic/Story documents (ln-210/ln-220 do this)
- ❌ Does NOT create Linear issues (coordinators do this)
- ❌ Does NOT prompt user (coordinators handle all user interaction)

**Coordinators:**
- **ln-210-epic-coordinator:** Creates 3-7 Epics (Epic 0 for Infrastructure if applicable, Epic 1-N for business domains)
- **ln-220-story-coordinator:** Creates 5-10 Stories per Epic (with inline standards research)

### Sequential Story Decomposition

**CRITICAL CONSTRAINT:** Epic N Stories MUST complete before Epic N+1 starts (ln-220 includes user interaction — interactive dialog cannot be parallelized across Epics).

**Why sequential?**
- ln-220-story-coordinator includes user interaction (Story preview confirmation)
- Interactive dialog cannot be parallelized (user must review each Epic's Stories)
- Ensures Epic N Stories are approved and created before starting Epic N+1

**Example:** 6 Epics → ln-220 invoked 6 times sequentially (Epic 0 → Epic 1 → Epic 2 → ... → Epic 5)

### Infrastructure Epic = Epic 0

**Reserved number:** Epic 0 is reserved for Infrastructure Epic (if proposed by ln-210).

**Numbering:**
- IF Infrastructure Epic exists → Epic 0 (Infrastructure), Epic 1-N (business domains)
- ELSE → Epic 1-N (business domains only)

**Decision:** ln-210-epic-coordinator Phase 1 Step 3 automatically determines if Infrastructure Epic is needed (new project, multi-stack, security/monitoring requirements).

### Auto-Discovery

**Team ID**: Auto-discovered from `docs/tasks/kanban_board.md` Linear Configuration table (see CLAUDE.md "Configuration Auto-Discovery").

**Fallback:** If kanban_board.md missing → ln-210-epic-coordinator will ask user directly

---

## Workflow

### Phase 1: Discovery (Automated)

Auto-discovers Team ID from `docs/tasks/kanban_board.md`.

**Validation:**
- Team ID exists in kanban_board.md
- If missing → Skip (ln-210 will request from user)

**NO user confirmation at orchestrator level** - coordinators handle all user interaction.

**Output:** Team ID (or None if not found)

### Phase 2: Epic Decomposition (Delegated)

**Objective:** Create all Epics for initiative.

Delegate to ln-210-epic-coordinator:
```
🔄 [ORCHESTRATOR] Phase 2: Delegating Epic creation to ln-210-epic-coordinator

Skill(skill: "ln-210-epic-coordinator")
```

**ln-210-epic-coordinator will:**
- Phase 1: Research project docs (requirements.md, architecture.md, tech_stack.md)
- Phase 2: Auto-propose domains + Infrastructure Epic (Epic 0) → User confirms domain list
- Phase 3: Build IDEAL Epic plan (Epic 0-N)
- Phase 5a: Auto-extract Q1-Q4 from docs → Generate ALL Epic documents → Show batch preview → User confirms → Create all Epics
- Return: Epic URLs + summary

**After completion:** Epics created in Linear, kanban_board.md updated.

**Output:** 3-7 Epics created (Epic 0 for Infrastructure if applicable, Epic 1-N for business domains)

### Phase 3: Story Decomposition Loop (Sequential, Delegated)

**Objective:** Create Stories for EACH Epic (sequential processing).

**Sequential Loop Logic:**

```
FOR EACH Epic (Epic 0, Epic 1, ..., Epic N):
    1. Invoke ln-220-story-coordinator for current Epic
    2. Wait for completion
    3. Verify Stories created in kanban_board.md
    4. Move to next Epic
```

### Stop Conditions (Decomposition Loops)

| Condition | Action |
|-----------|--------|
| All Epics processed (Stories + optional RICE) | STOP — proceed to Summary |
| ln-220 fails for an Epic (coordinator error) | STOP — report partial results, list completed Epics |
| User cancels during Story confirmation | STOP — report completed Epics, skip remaining |
| Total Story count exceeds 80 | STOP — WARN: "Scope may be too large. Continue?" |

**Invocation per Epic:**
```
🔄 [ORCHESTRATOR] Phase 3: Delegating Story creation for Epic N to ln-220-story-coordinator

Skill(skill: "ln-220-story-coordinator", epic_number="Epic N")
```

**ln-220-story-coordinator will (per Epic):**
- Phase 1: Auto-extract Q1-Q6 from Epic + Fallback search (requirements.md, tech_stack.md)
- Phase 2: Research standards inline MCP Ref (auto)
- Phase 3: Build IDEAL Story plan (5-10 Stories)
- Phase 4a: Generate ALL Story documents → Show preview → User confirms → Create all Stories
- Return: Story URLs + summary

**Sequential constraint explanation:**
- ln-220 includes user interaction (Story preview confirmation)
- Cannot parallelize - user must review each Epic's Stories sequentially
- Epic N Stories approved → Epic N+1 Stories generated

**After each Epic:** Stories created in Linear, kanban_board.md updated.

**Output:** 30-60 Stories total (5-10 per Epic × 3-7 Epics)

**TodoWrite format (mandatory):**
Add phases and Epic iterations to todos before starting:
```
- Phase 1: Discovery (in_progress)
- Phase 2: Delegate to ln-210-epic-coordinator (pending)
- Phase 3: Delegate to ln-220 for Epic 0 (pending)
- Phase 3: Delegate to ln-220 for Epic 1 (pending)
- Phase 3: Delegate to ln-220 for Epic 2 (pending)
... (one todo per Epic)
- Phase 4: Delegate to ln-230 for Epic 0 (pending)
- Phase 4: Delegate to ln-230 for Epic 1 (pending)
... (one todo per Epic, optional)
- Phase 5: Summary (pending)
```
Mark each as in_progress when starting, completed when coordinator returns success.

### Phase 4: RICE Prioritization Loop (Optional, Sequential, Delegated)

**Objective:** Prioritize Stories per Epic using RICE scoring with market research.

> **OPTIONAL:** Ask user "Run RICE prioritization for all Epics?" If user declines, skip to Phase 5.

**Sequential Loop Logic:**

```
FOR EACH Epic (Epic 0, Epic 1, ..., Epic N):
    1. Invoke ln-230-story-prioritizer for current Epic
    2. Wait for completion
    3. Verify prioritization.md created in docs/market/[epic-slug]/
    4. Move to next Epic
```

**Invocation per Epic:**
```
Skill(skill: "ln-230-story-prioritizer", args: "epic=\"Epic N\"")
```

**ln-230-story-prioritizer will (per Epic):**
- Load Stories metadata from Linear
- Research market size and competition per Story
- Calculate RICE score and assign Priority (P0-P3)
- Generate docs/market/[epic-slug]/prioritization.md

**Skip condition:** If Epic contains only technical/infrastructure Stories (no business value to prioritize), skip that Epic.

**After each Epic:** Prioritization table saved to docs/market/[epic-slug]/prioritization.md.

**Output:** Prioritization tables for all applicable Epics.

### Phase 5: Summary and Next Steps

**Objective:** Provide complete decomposition overview.

```
🔄 [ORCHESTRATOR] Phase 5: Full decomposition complete

Initiative Decomposition Summary:
- Epics created: N Projects (Epic 0: Infrastructure [if exists], Epic 1-N: Business domains)
- Stories created: M Issues (breakdown per Epic)
- Location: docs/tasks/kanban_board.md

Next Steps:
1. Run ln-310-multi-agent-validator to validate all Stories
2. Use ln-400-story-executor to process each Story (tasks → execution → Done)
   OR use ln-300-task-coordinator to create tasks manually for each Story
```

**Output:** Summary message with full decomposition results

---

## Critical Rules

### 1. No User Prompts at Orchestrator Level

**Orchestrator does NOT prompt user:**
- ❌ NO "Proceed with decomposition?" confirmation (redundant - coordinators already confirm)
- ❌ NO time estimates (misleading - actual time varies)
- ❌ NO Epic/Story previews (coordinators handle this)

**All user interaction delegated to coordinators:**
- ln-210 Phase 2: Domain approval (USER CONTROL POINT 1)
- ln-210 Phase 5a: Epic batch preview (USER CONTROL POINT 2)
- ln-220 Phase 4a: Story preview per Epic (USER CONTROL POINT 3, N times)

---

## Definition of Done

Before completing work, verify ALL checkpoints:

**✅ Team ID Discovered (Phase 1):**
- [ ] Team ID loaded from kanban_board.md OR skipped (ln-210 will request)

**✅ Epic Decomposition Complete (Phase 2):**
- [ ] Delegated to ln-210-epic-coordinator
- [ ] 3-7 Epics created (Epic 0 for Infrastructure if applicable, Epic 1-N for business domains)
- [ ] Epic URLs returned
- [ ] Epics visible in kanban_board.md

**✅ Story Decomposition Complete (Phase 3):**
- [ ] Delegated to ln-220-story-coordinator for EACH Epic (sequential)
- [ ] 5-10 Stories created per Epic
- [ ] Story URLs returned for each Epic
- [ ] All Stories visible in kanban_board.md (Backlog section)

**✅ RICE Prioritization Complete (Phase 4, optional):**
- [ ] User asked about prioritization (skip if declined)
- [ ] Delegated to ln-230-story-prioritizer for each applicable Epic
- [ ] Prioritization tables saved to docs/market/[epic-slug]/

**✅ Summary Provided (Phase 5):**
- [ ] Total counts displayed (Epics, Stories, breakdown per Epic)
- [ ] kanban_board.md location shown
- [ ] Next steps provided (validation, task creation)

**Output:** Summary message with full decomposition results (Epics + Stories per Epic)

---

## Integration with Ecosystem

### Called By

Users directly: "Decompose initiative: [initiative name]" or "Create epics and stories for [project]"

### Calls (via Skill tool)

- **ln-210-epic-coordinator** (Phase 2) - CREATE mode (batch Epic creation with batch preview)
- **ln-220-story-coordinator** (Phase 3, sequential loop) - CREATE mode per Epic (Story creation with preview)
- **ln-230-story-prioritizer** (Phase 4, optional sequential loop) - RICE prioritization per Epic

### Downstream

After ln-200-scope-decomposer completes:
- **ln-310-multi-agent-validator** - validates all created Stories before task creation
- **ln-400-story-executor** - processes each Story (tasks → execution → Done)
  - OR **ln-300-task-coordinator** - creates tasks manually for each Story

---

## Best Practices

### Coordinator Trust

**Trust coordinator results:** Coordinators return summary, orchestrator doesn't re-verify.

**Error handling:** If coordinator returns error, report to user and stop pipeline.

### Time Estimates

**Realistic estimate:** 2-3 hours for full decomposition (6 Epics × 7 Stories avg = 42 Stories).

**Breakdown:**
- Phase 2 (Epic creation): 30-45 min (batch preview reduces time)
- Phase 3 (Story creation): 1.5-2 hours (6 Epics × 15-20 min per Epic)
- Phase 4 (Summary): 2 min

**Do NOT provide time estimates to user** - varies based on project complexity and user response time.

---

## Example Usage

**Request:**
```
"Decompose initiative: E-commerce Platform"
```

**Execution:**

1. **Phase 1: Discovery**
   - Team ID loaded from kanban_board.md

2. **Phase 2: Epic Decomposition**
   - Invoke ln-210-epic-coordinator
   - ln-210 creates 6 Epics:
     - Epic 11 (Infrastructure Epic 0 pattern)
     - Epic 12-16 (business domains)
   - Output: 6 Epic URLs

3. **Phase 3: Story Decomposition Loop (Sequential)**
   - **Epic 11:** Invoke ln-220 → 6 Stories (US017-US022)
   - **Epic 12:** Invoke ln-220 → 7 Stories (US023-US029)
   - **Epic 13:** Invoke ln-220 → 5 Stories (US030-US034)
   - **Epic 14:** Invoke ln-220 → 6 Stories (US035-US040)
   - **Epic 15:** Invoke ln-220 → 7 Stories (US041-US047)
   - **Epic 16:** Invoke ln-220 → 5 Stories (US048-US052)
   - Output: 36 Stories total

4. **Phase 4: Summary**
   ```
   🔄 [ORCHESTRATOR] Full decomposition complete

   Initiative: E-commerce Platform
   - Epics created: 6 Projects (Epic 11: Infrastructure, Epic 12-16: Business domains)
   - Stories created: 36 Issues
     - Epic 11: 6 Stories
     - Epic 12: 7 Stories
     - Epic 13: 5 Stories
     - Epic 14: 6 Stories
     - Epic 15: 7 Stories
     - Epic 16: 5 Stories
   - Location: docs/tasks/kanban_board.md

   Next Steps:
   1. Run ln-310-multi-agent-validator to validate all Stories
   2. Use ln-400-story-executor to process each Story (tasks → execution → Done)
   ```

**Result:** 6 Epics + 36 Stories created through full pipeline automation

---

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after all phases complete. Output to chat using the `planning-coordinator` format.

## Reference Files

- **Configuration source:** `docs/tasks/kanban_board.md` (Team ID, Next Epic Number)
- **Epic coordinator:** `ln-210-epic-coordinator/SKILL.md`
- **Story coordinator:** `ln-220-story-coordinator/SKILL.md`
- **Story prioritizer:** `ln-230-story-prioritizer/SKILL.md`
- **Numbering conventions:** `shared/references/numbering_conventions.md` (Epic 0 reserved)

---

## Chat Output Prefix

Use emoji prefix for visual differentiation:
- 🔄 [ORCHESTRATOR] - ln-200-scope-decomposer (top orchestrator)

**Purpose:** Helps users track orchestrator progress when delegating to multiple coordinators.

---

**Version:** 2.0.0
**Last Updated:** 2025-11-20
