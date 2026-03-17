---
name: ln-220-story-coordinator
description: CREATE/REPLAN Stories for Epic (5-10 Stories). Delegates ln-001-standards-researcher for standards research. Decompose-First Pattern. Auto-discovers team/Epic.
---

# Story Coordinator

Universal Story management coordinator that delegates CREATE/REPLAN operations to specialized workers after building IDEAL Story plan.

## When to Use This Skill

Use when:
- Decompose Epic to User Stories (5-10 Stories covering Epic scope)
- Update existing Stories when Epic requirements change
- Rebalance Story scopes within Epic
- Add new Stories to existing Epic structure

## Core Pattern: Decompose-First

**Key principle:** Build IDEAL Story plan FIRST, THEN check existing Stories to determine mode:
- **No existing Stories** → CREATE MODE (delegate to ln-221-story-creator)
- **Has existing Stories** → REPLAN MODE (delegate to ln-222-story-replanner)

**Rationale:** Ensures consistent Story decomposition based on current Epic requirements, independent of existing Story structure (may be outdated).

## Story Numbering Convention

**MANDATORY READ:** Load `shared/references/numbering_conventions.md` for Story numbering rules (US001 sequential across Epics, no Story 0).

## Quality Criteria

**MANDATORY READ:** Load `shared/references/creation_quality_checklist.md` §Story Creation Checklist for validation criteria that ln-310 will enforce.

## How It Works

### Phase 1: Context Assembly

**Objective:** Gather context for Story planning (Epic details, planning questions, frontend context, fallback docs, user input)

**Step 1: Discovery (Automated)**

Auto-discovers from `docs/tasks/kanban_board.md`:

1. **Team ID:** Reads Linear Configuration table
2. **Epic:** Parses Epic number from request → Validates in Linear → Loads Epic description
   - **User format:** "Epic N" (Linear Project number, e.g., "Epic 7: OAuth Authentication")
   - **Query:** `get_project(query="Epic N")` → Fetch full Epic document
   - **Extract:** Goal, Scope In/Out, Success Criteria, Technical Notes (Standards Research if Epic created by ln-210 v7.0.0+)
   - **Note:** Epic N = Linear Project number (global), NOT initiative-internal index (Epic 0-N)
3. **Next Story Number:** Reads Epic Story Counters table → Gets next sequential number

**Step 2: Extract Planning Information (Automated)**

Parses Epic structure for Story planning questions:

| Question | Extraction Source |
|----------|-------------------|
| **Q1 - User/Persona** | Epic Goal ("Enable [persona]...") + Scope In (user roles) |
| **Q2 - What they want** | Epic Scope In (capabilities) + functional requirements |
| **Q3 - Why it matters** | Epic Success Criteria (metrics) + Goal (business value) |
| **Q4 - Which Epic** | Already from Step 1 |
| **Q5 - Main AC** | Derive from Epic Scope In features → testable scenarios |
| **Q6 - Application type** | Epic Technical Notes (UI/API mentioned) → Default: API |

**Step 3: Frontend Research (Optional)**

**Trigger:** If Q2 (capabilities) OR Q5 (AC) missing after Step 2

**Process:**
1. Scan HTML files: `Glob` `**/*.html`, `src/**/*.html`
2. Extract:
   - Forms → AC scenarios (e.g., `<form id="login">` → "Given valid credentials, When submit, Then login success")
   - Buttons/Actions → capabilities (e.g., `<button id="register">` → "User registration")
   - Validation rules → edge case AC (e.g., `minlength="8"` → "Given password <8 chars, Then error")
3. Combine with Epic context, deduplicate, prioritize Epic AC if conflict

**Fallback:** If no HTML → Skip to Step 4

**Step 4: Fallback Search Chain**

**Objective:** Fill missing Q1-Q6 BEFORE asking user.

For each question with no answer from Step 2-3:

| Question | Fallback Search |
|----------|-----------------|
| **Q1 (User/Persona)** | Search `requirements.md` for "User personas", "Actors" → Default "User" if not found |
| **Q3 (Why it matters)** | Search `requirements.md` for "Business objectives", "Goals" → Infer from Epic Success Criteria |
| **Q6 (Application type)** | Search `tech_stack.md` for "Frontend", "Backend", "API" → Default "API" |

**Skip:** Q2, Q5 (Epic + HTML are sources of truth), Q4 (already known)

**Step 5: User Input (Only if Missing)**

**If still missing after Step 2 + 3 + 4:**
- Show extracted: "From Epic: [Epic info]. From HTML: [HTML info]. From fallback: [fallback info]"
- Ask user to confirm or provide remaining missing details

**If all questions answered from Epic OR HTML OR fallback:** Skip user prompts, proceed to Phase 2

**Output:** Complete context (Epic details, next Story number, Q1-Q6 answers)

---

### Phase 2: Standards Research (Delegated)

**Objective:** Research industry standards/patterns BEFORE Story generation to ensure implementation follows best practices.

**Why:** Prevents outdated patterns or RFC violations (e.g., OAuth without PKCE).

**Process:**

1. **Parse Epic for domain keywords:** Extract domain from Epic goal/Scope In (authentication, rate limiting, payments)
2. **Delegate to ln-001-standards-researcher:**
   - Call `Skill(skill: "ln-001-standards-researcher", epic_description="[Epic full description]", story_domain="[domain]")`
   - Wait for Standards Research (Markdown string)
3. **Store:** Cache for Phase 5a/5b (workers insert in Story Technical Notes)

**Output:** Standards Research stored for ALL Stories in Epic

**Skip conditions:**
- Epic has NO standards in Technical Notes
- Story domain is trivial CRUD
- Epic says "research not needed"

**Time-box:** 15-20 minutes (handled by ln-001)

**Note:** Research done ONCE per Epic, results reused for all Stories (5-10 Stories benefit from single research)

---

### Phase 3: Planning

**Objective:** Build IDEAL Story plan, determine execution mode

**Story Grouping Guidelines:**

Each Story = ONE vertical slice of user capability (end-to-end: UI → API → Service → DB).

**✅ GOOD Story Grouping (1 Story = 1 user journey):**
- ✅ "User registration" (form → validation → API → database → email)
- ✅ "Password reset" (request link → verify token → set password → update DB)
- ✅ "Product search" (input → filter/sort → API → DB query → display)

**❌ BAD Story Grouping (horizontal slices):**
- ❌ "Create user table" (database only, no user value → Task, not Story)
- ❌ "User registration API endpoint" (API layer only, not vertical)
- ❌ "Registration UI form" (frontend only, not vertical)

**Rule:** 1 Story = 1 user capability (size limits per `creation_quality_checklist.md` #9)

**Database Creation Principle (Incremental Schema Evolution):**

Each Story creates ONLY the tables it needs (not all tables upfront).

**✅ GOOD (Incremental):**
- ✅ "User registration" → Creates Users table
- ✅ "Product search" → Creates Products table
- ✅ "Order checkout" → Creates Orders, Payments tables

**❌ BAD (Big-Bang):**
- ❌ "Setup database" → Creates all 50 tables (no user value, violates vertical slicing)
- ❌ "Database schema" → Creates Users, Products, Orders, Payments upfront

**Rationale:** Big-bang database setup violates incremental delivery. Each Story should deliver user value, not technical infrastructure.

**Build IDEAL Plan (Automated):**

1. **Analyze Epic Scope:** Review features in Epic Scope In, identify user capabilities
2. **Determine Story Count:**
   - Simple Epic (1-3 features): 3-5 Stories
   - Medium Epic (4-7 features): 6-8 Stories
   - Complex Epic (8+ features): 8-10 Stories
   - **Max 10 Stories per Epic**

3. **Story Size:** Limits per `creation_quality_checklist.md` #9. Outside range → split or merge.

**Over-decomposition indicators:**
- ❌ Purely technical (no user value)
- ❌ Title starts with "Add", "Create", "Update" (likely Task)
- ❌ Crosses only 1-2 layers (not vertical)

4. **Build IDEAL Plan "in mind":**
   - Each Story: persona + capability + business value
   - Each Story: testable AC per checklist #4
   - Stories ordered by dependency (no forward deps per checklist #18)
   - Each Story: Test Strategy section exists but is **empty** (tests planned later by test planner)
   - Each Story: Technical Notes (architecture, integrations, **Standards Research from Phase 2**, guide links)

5. **AC Quality Validation:** Rules per `creation_quality_checklist.md` #4. Workers (ln-221, ln-222) must validate.

**Examples:**
- ❌ BAD: "User can login" (only happy path, no error/edge cases)
- ✅ GOOD: AC1: login success + AC2: 401 invalid password + AC3: 403 locked
- ❌ BAD: "Login should be fast" (vague, not measurable)
- ✅ GOOD: "Then receive token <200ms" (specific, measurable)

**INVEST Checklist:**

| Criterion | Check | ✅ GOOD | ❌ BAD |
|-----------|-------|---------|--------|
| **Independent** | Can develop/deploy without blocking others + NO forward dependencies | "Request OAuth token" (Story N uses only N-1) | "Validate token depends on Story N+2 refresh flow" (forward dependency!) |
| **Negotiable** | AC focus on WHAT, not HOW | "User gets valid token" (what) | "Use authlib 1.3.0, store in Redis" (how) |
| **Valuable** | Clear business value | "User refreshes expired token to maintain session" | "Add token_refresh table" (no user value) |
| **Estimable** | Size within checklist #9 range | Clear scope, known patterns, researched standards | "Implement authentication" (too vague) |
| **Small** | AC/hours/tests per checklist #9 | Within limits | Exceeds limits → split |
| **Testable** | AC measurable | "Given valid refresh token, Then receive token <200ms" | "Token refresh should be fast" (not measurable) |

**Output:** IDEAL Story plan (5-10 Stories) with titles, statements, core AC, ordering

---

### Phase 4: Check Existing & Detect Mode

**Objective:** Determine execution mode based on existing Stories AND user intent

**Process:**

Query Linear for existing Stories in Epic:

```
list_issues(project=Epic.id, label="user-story")
```

**Mode Detection:**

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

**Output:** Execution mode determined + existingCount for workers

---

### Phase 5a: Delegate CREATE (No Existing Stories)

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
- Generate Story documents (8 sections, insert Standards Research)
- Validate INVEST criteria
- Show preview
- User confirmation (if autoApprove=false)
- Create in Linear (project=Epic, labels=user-story, state=Backlog)
- Update kanban_board.md (Epic Grouping Algorithm)

**Output:** Created Story URLs + summary from worker

---

### Phase 5b: Delegate REPLAN (Existing Stories Found)

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

### Phase 5c: Delegate ADD (Append to Existing Stories)

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

**Key differences from CREATE MODE:**
- `appendMode: true` → Skip full IDEAL plan, create only requested Story
- `newStoryDescription` → User's specific request (e.g., "add authorization Story")
- Does NOT require Phase 3 IDEAL plan for all Stories
- Preserves existing Stories without comparison

**Worker handles:**
- Research standards for NEW Story only
- Generate Story document (8 sections)
- Validate INVEST criteria
- Create in Linear (append to existing)
- Update kanban_board.md

**Output:** Created Story URL + summary from worker

**TodoWrite format (mandatory):**
Add phases to todos before starting:
```
- Phase 1: Context Assembly (in_progress)
- Phase 2: Standards Research via ln-221 (pending)
- Phase 3: Build IDEAL Story Plan (pending)
- Phase 4: Check Existing Stories (pending)
- Phase 5: Delegate to ln-222/ln-223 (pending)
- Wait for worker result (pending)
```
Mark each as in_progress when starting, completed when done.

---

---

## Integration with Ecosystem

**Calls:**
- **ln-001-standards-researcher** (Phase 2) - research standards/patterns for Epic
- **ln-221-story-creator** (Phase 5a, 5c) - CREATE and ADD worker
- **ln-222-story-replanner** (Phase 5b) - REPLAN worker

**Called by:**
- **ln-200-scope-decomposer** (Phase 3) - automated full decomposition (scope → Epics → Stories)
- **Manual** - user invokes for Epic Story creation/replanning

**Upstream:**
- **ln-210-epic-coordinator** - creates Epics (prerequisite for Story creation)

**Downstream:**
- **ln-300-task-coordinator** - creates implementation tasks for each Story
- **ln-310-story-validator** - validates Story structure/content
- **ln-400-story-executor** - orchestrates task execution for Story

---

## Definition of Done

**✅ Phase 1: Context Assembly Complete:**
- [ ] Team ID, Epic number, Next Story Number loaded from kanban_board.md
- [ ] Q1-Q6 extracted from Epic (Step 2)
- [ ] Frontend Research attempted if Q2/Q5 missing (Step 3)
- [ ] Fallback Search attempted for missing info (Step 4)
- [ ] User input requested if still missing (Step 5)
- [ ] Complete Story planning context assembled

**✅ Phase 2: Standards Research Complete:**
- [ ] Epic parsed for domain keywords
- [ ] ln-001-standards-researcher invoked with Epic description + Story domain
- [ ] Standards Research cached for workers
- [ ] OR Phase 2 skipped (trivial CRUD, no standards, explicit skip)

**✅ Phase 3: Planning Complete:**
- [ ] Epic Scope analyzed
- [ ] Optimal Story count determined (5-10 Stories)
- [ ] IDEAL Story plan created (titles, statements, core AC, ordering)
- [ ] Story Grouping Guidelines validated (vertical slicing)
- [ ] INVEST checklist validated for all Stories

**✅ Phase 4: Check Existing Complete:**
- [ ] Queried Linear for existing Stories (count only)
- [ ] Execution mode determined (CREATE or REPLAN)

**✅ Phase 5: Delegation Complete:**
- [ ] Called ln-221-story-creator (Phase 5a) OR ln-222-story-replanner (Phase 5b) via Skill tool
- [ ] Passed epicData, idealPlan, standardsResearch, teamId, autoApprove
- [ ] Received output from worker (Story URLs + summary + next steps)

---

## Example Usage

**CREATE MODE (First Time):**
```
"Create stories for Epic 7: OAuth Authentication"
```

**Process:**
1. Phase 1: Context Assembly → Discovery (Team "API", Epic 7, US004), Extract (Persona: API client, Value: secure API access), Frontend Research (HTML login/register forms → AC), Fallback Search (requirements.md for personas)
2. Phase 2: Standards Research → Epic mentions "OAuth 2.0", delegate ln-001 → Standards Research with RFC 6749, patterns
3. Phase 3: Planning → Build IDEAL (5 Stories: "Register client", "Request token", "Validate token", "Refresh token", "Revoke token")
4. Phase 4: Check Existing → Count = 0 → CREATE MODE
5. Phase 5a: Delegate CREATE → Call ln-221-story-creator → US004-US008 created with Standards Research

**REPLAN MODE (Requirements Changed):**
```
"Replan stories for Epic 7 - removed custom token formats, added scope management"
```

**Process:**
1. Phase 1: Context Assembly → Discovery (Team "API", Epic 7, has US004-US008), Extract (Removed custom formats, added scopes)
2. Phase 2: Standards Research → Epic mentions "OAuth 2.0 scopes", delegate ln-001 → Updated Standards Research with RFC 6749 Section 3.3
3. Phase 3: Planning → Build IDEAL (5 Stories: "Register client", "Request token", "Validate token", "Refresh token", "Manage scopes")
4. Phase 4: Check Existing → Count = 5 → REPLAN MODE
5. Phase 5b: Delegate REPLAN → Call ln-222-story-replanner → KEEP 4, UPDATE Technical Notes (scope research), OBSOLETE US008, CREATE US009

---

## Reference Files

- **[MANDATORY] Problem-solving approach:** `shared/references/problem_solving.md`
- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`
- **Decompose-first pattern:** `shared/references/decompose_first_pattern.md`
- **Numbering conventions:** `shared/references/numbering_conventions.md` (Story sequential across Epics)

---

## Best Practices

**Story Content:**
- **Research-First:** Always perform Phase 2 research (standards/patterns) before Story generation
  - **Story level:** STANDARDS/PATTERNS (OAuth RFC 6749, middleware pattern)
  - **Task level:** LIBRARIES (authlib vs oauthlib) - delegated by ln-300
- **Business-oriented Stories:** Each Story = USER JOURNEY (what user does, what they get), NOT technical tasks
  - ✅ GOOD: "As API client, I want to refresh expired token, so that I maintain session without re-authentication"
  - ❌ BAD: "Create token refresh endpoint in API" (Task, not Story)
- **Vertical Slicing:** Each Story delivers end-to-end functionality (UI → API → Service → DB)
- **One capability per Story:** Clear, focused persona + capability + value
- **Testable AC:** Given-When-Then, 3-5 AC, specific criteria ("<200ms" not "fast")
- **Test Strategy:** Section exists but is **empty** at Story creation (tests planned later by test planner)
- **Standards Research:** Include Phase 2 research in ALL Story Technical Notes

**Story Decomposition:**
- **Decompose-First:** Build IDEAL plan before checking existing - prevents anchoring to suboptimal structure
- **INVEST validation:** Validate every Story against INVEST criteria
- **Size enforcement:** 3-5 AC, 6-20 hours
- **Avoid over-decomposition:** <3 AC, <6 hours → Merge Stories

**User Interaction:**
- **Epic extraction:** Try to extract all planning info from Epic in Phase 1 Step 2 before asking user
- **Frontend Research:** HTML forms/validation → AC scenarios (Phase 1 Step 3)
- **Fallback search:** requirements.md, tech_stack.md if Epic incomplete (Phase 1 Step 4)
- **Only ask user for missing info** after Epic extraction AND frontend AND fallback search fail

**Delegation:**
- **Orchestrator loads metadata only:** ID, title, status (~50 tokens per Story)
- **Workers load full descriptions:** 8 sections (~5,000 tokens per Story)
- **Token efficiency:** 10 Stories × 50 tokens = 500 tokens (orchestrator) vs 10 Stories × 5,000 tokens = 50,000 tokens (workers load when needed)

---

**Version:** 5.0.0 (BREAKING: Added AC Quality Validation in Phase 3 (completeness: happy path + errors + edge cases; specificity: HTTP codes + timing). Updated INVEST Independent criterion with forward dependency check. Added Database Creation Principle to Story Grouping Guidelines per BMAD Method best practices.)
**Last Updated:** 2026-02-03
