---
name: ln-210-epic-coordinator
description: "Creates or replans 3-7 Epics from scope using Decompose-First pattern. Use when initiative needs Epic-level breakdown or Epic scope changed."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Epic Coordinator

**Type:** L2 Domain Coordinator
**Category:** 2XX Planning

Universal Epic management coordinator that handles both creation and replanning through scope decomposition.

## Purpose

Coordinates Epic creation (CREATE) and replanning (REPLAN) from scope decomposition, producing 3-7 Linear Projects with batch preview, auto-extraction from docs/HTML, and Decompose-First Pattern.

## When to Use This Skill

This skill should be used when:
- Start new scope/initiative requiring decomposition into multiple logical domains (CREATE mode)
- Break down large architectural requirement into Epics
- Update existing Epics when scope/requirements change (REPLAN mode)
- Rebalance Epic scopes within an initiative
- Add new Epics to existing initiative structure
- First step in project planning (scope → Epics → Stories → Tasks)
- Define clear scope boundaries and success criteria for each domain

**Output:** 3-7 Linear Projects (logical domains/modules)

## Runtime Contract

**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/epic_planning_runtime_contract.md`, `shared/references/epic_plan_summary_contract.md`

Runtime family: `epic-planning-runtime`

Identifier:
- scope identifier

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_DISCOVERY`
3. `PHASE_2_RESEARCH`
4. `PHASE_3_PLAN`
5. `PHASE_4_MODE_DETECTION`
6. `PHASE_5_PREVIEW`
7. `PHASE_6_DELEGATE`
8. `PHASE_7_FINALIZE`
9. `PHASE_8_SELF_CHECK`

Decision handling:
- preview/confirmation is runtime `PAUSED + pending_decision`
- ln-210 writes final `epic-plan` summary for ln-200 when used as downstream coordinator

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 6 | None | CREATE/REPLAN execution is inline inside ln-210; no downstream Skill worker is delegated |

**Downstream contract:** ln-210 is itself a worker for `ln-200` and writes `epic-plan` machine-readable output after inline Epic create/replan execution completes.

## TodoWrite format (mandatory)

```text
- Phase 1: Discover scope and project context (pending)
- Phase 2: Research only what changes Epic boundaries (pending)
- Phase 3: Build ideal Epic plan (pending)
- Phase 4: Detect mode and validate Infra Epic need (pending)
- Phase 5: Preview and confirm plan (pending)
- Phase 6: Execute create/replan flow (pending)
- Phase 7: Finalize epic-plan summary (pending)
- Phase 8: Self-check (pending)
```

## Core Concepts

### Decompose-First Pattern

**Key principle:** ALWAYS analyze scope and build IDEAL Epic plan FIRST, THEN check existing Epics to determine mode:
- **No existing Epics** → CREATE MODE (generate and create all Epics)
- **Has existing Epics** → REPLAN MODE (compare, determine operations: KEEP/UPDATE/OBSOLETE/CREATE)

**Rationale:** Ensures consistent Epic decomposition based on current scope requirements, independent of existing Epic structure (which may be outdated or suboptimal).

### Epic 0 Reserved for Infrastructure

**MANDATORY READ:** Load `shared/references/numbering_conventions.md` for Epic 0 rules, when to use it, and Linear numbering.

---

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `scopeDoc` | Yes | args, project docs, user | Scope document for Epic decomposition |

**Resolution:** Epic Resolution Chain (adapted: scope doc discovery).
**Fallback:** IF no scope doc found → AskUserQuestion: "What should be decomposed into Epics?"

## Workflow

### Phase 0: Tools Config

**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider

### Phase 1: Discovery & Research

**Objective:** Gather all necessary context before Epic decomposition.

**Step 0: Resolve scopeDoc** (per input_resolution_pattern.md, adapted for scope):
- IF args provided (scope description or doc path) → use args
- ELSE IF `docs/project/requirements.md` exists → use as scope source
- ELSE IF `docs/requirements.md` exists → use as scope source
- ELSE → AskUserQuestion: "What should be decomposed into Epics?"

**Step 1: Load Configuration**

Auto-discovers Team ID and Next Epic Number from `docs/tasks/kanban_board.md`:
- **Team ID:** Reads Linear Configuration table → Fallback: Ask user directly
- **Next Epic Number:** Reads Next Epic Number field → Fallback: Ask user directly

**MANDATORY READ:** Load `CLAUDE.md` — sections "Configuration Auto-Discovery" and "Linear Integration".

**Step 2: Project Research**

**Objective:** Research project documentation AND frontend code to understand context BEFORE asking user questions.

**Process:**

1. **Document Scan:**
   - Use `Glob` to find: `docs/requirements.md`, `docs/architecture.md`, `docs/tech_stack.md`
   - Use `Read` to load found documents

2. **Frontend Code Scan (if applicable):**
   - Use `Glob` to find: `**/*.html`, `src/**/*.html`, `public/**/*.html`, `templates/**/*.html`
   - Use `Read` to load HTML files
   - Extract functional domains from:
     - **Navigation menus:** `<nav>`, `<a href>` links reveal feature areas
     - **Forms:** Input fields reveal data models (user registration, login, checkout)
     - **Page titles:** `<h1>`, `<title>` tags reveal feature names
     - **Route patterns:** URL structures reveal domain boundaries

   **Example HTML extraction:**
   ```html
   <nav>
     <a href="/products">Products</a>
     <a href="/cart">Shopping Cart</a>
     <a href="/checkout">Checkout</a>
   </nav>
   <!-- Reveals domains: Product Catalog, Shopping Cart, Payment -->
   ```

3. **Extract key information from docs + HTML:**
   - **Business objectives:** What is the project trying to achieve? (from requirements.md)
   - **User personas:** Who will use the system? (from requirements.md)
   - **Major functional domains:** What are the main modules/areas? (from requirements.md, architecture.md, HTML navigation)
   - **Technical stack:** What technologies mentioned? (from tech_stack.md, architecture.md, HTML meta/script tags)
   - **Infrastructure requirements:** Any mention of logging, monitoring, deployment, CI/CD, security, performance optimization?

4. **Combine findings:**
   - Merge domains from docs + HTML (deduplicate, consolidate similar)
   - Example: "User Auth" (from docs) + "Login" (from HTML) → "User Management"

**Fallback:** If docs AND HTML missing → Skip to Phase 2, will ask user basic questions

**Step 3: Infrastructure Epic Decision**

**Objective:** Determine if Infrastructure Epic (Epic 0) should be proposed.

**Criteria for Infrastructure Epic:**

✅ **PROPOSE Infrastructure Epic (Epic 0)** if ANY of:
1. **New project** (no `docs/infrastructure.md` found, no Epic "Infrastructure" in kanban_board.md Epic Story Counters)
2. **Multi-stack** (requirements.md or tech_stack.md mentions frontend AND backend on different stacks - e.g., React + Python)
3. **Infrastructure requirements mentioned** in requirements.md, architecture.md:
   - Logging, Error Handling
   - Monitoring, Alerting
   - Hosting, Deployment, CI/CD
   - Security (authentication, authorization, encryption, secrets management)
   - Performance optimization (caching, rate limiting, database optimization)

❌ **DO NOT propose** if:
1. Existing project (found `docs/infrastructure.md`)
2. Epic Story Counters shows existing Epic with "Infrastructure" in title
3. User explicitly declined in previous interaction

**Decision:** Store YES/NO decision for use in Phase 2

**Output from Phase 1:**
- Team ID, Next Epic Number
- Project context (business goals, domains from docs + HTML, tech stack, infrastructure needs) - if found
- Infrastructure Epic decision (YES/NO)

---

### Phase 2: Scope Analysis & Epic Planning

**Objective:** Identify logical domains and build Epic structure inline.

**Process:**

**Step 1: Auto-identify Domains**

Use research context from Phase 1 Step 2:
- If project docs found → Extract domains from requirements.md, architecture.md (module names, feature areas)
- If HTML found → Extract domains from navigation, forms, page structures
- Combine and deduplicate domains
- Example: "User Auth" + "Profile Management" → "User Management"

**Fallback:** If no docs/HTML → Ask user basic questions (scope, objectives, functional areas)

**Step 2: Build Epic List (inline)**

**IF Infrastructure needed (from Phase 1 Step 3):**
- **Epic 0: Infrastructure & Operations** — per `numbering_conventions.md` §Epic 0 Content Template
- **Epic 1-N:** Business domains (from Step 1)

**ELSE:**
- **Epic 1-N:** Business domains only

**Step 3: Determine Epic Count**

- Infrastructure Epic (if applicable): +1 Epic
- Simple Initiative (1-3 domains): 3-4 Epics total
- Medium Initiative (4-6 domains): 5-7 Epics total
- Complex Initiative (7+ domains): 7-10 Epics total (rare)
- **Max 10 Epics per Initiative** (enforced)

**Step 4: Show Proposed Epic Structure (USER CONTROL POINT 1)**

Display identified Epics with initiative-internal indexes:

```
📋 Proposed Epic Structure:

Epic 0: Infrastructure & Operations
Epic 1: User Management
Epic 2: Product Catalog
Epic 3: Shopping Cart
Epic 4: Payment Processing
Epic 5: Order Management

Total: 6 Epics
Type "confirm" to proceed, or modify the list
```

**Step 5: User Confirmation**

- User types "confirm" → Proceed to Phase 3
- User modifies → Update domain list, show again

**Output:** Approved Epic list (Epic 0-N or Epic 1-N) ready for next phase

### Epic Quality Gate

**Context:** Structured quality check before creating Epics ensures scope clarity and prevents rework during Story decomposition.

For each proposed Epic, validate 5 criteria:

| # | Criterion | PASS | FAIL |
|---|-----------|------|------|
| 1 | **Scope clarity** | Clear In/Out boundaries | Vague or overlapping with other Epics |
| 2 | **Success criteria** | Measurable ("<200ms", ">98%") | Vague ("fast", "reliable") |
| 3 | **Risk documentation** | Dependencies/blockers identified | Risks section empty or generic |
| 4 | **Balance** | Similar scope size across Epics (±30%) | One Epic has 80% of work |
| 5 | **Independence** | No circular Epic dependencies | Epics block each other |

**Quality Score = count of PASS criteria (0-5)**
- 5/5: Proceed to creation
- 3-4/5: Show warnings, user decides
- <3/5: Rework Epic structure before creation

---

### Phase 3: Check Existing Epics

**Objective:** Determine CREATE vs REPLAN mode.

Query kanban_board.md and task provider for existing Epics:

1. **Read Epic Story Counters** table in kanban_board.md
2. **IF task_provider == "linear":** `list_projects(team=teamId)` to cross-check
   **ELSE IF task_provider == "github":** `gh issue list -R {REPO} --label epic --state all --json number,title` to cross-check
   **ELSE:** `Glob("docs/tasks/epics/*/epic.md")` to list file-based Epics
3. **Count existing Epic rows** (excludes header row)

**Decision Point:**
- **Count = 0** → No existing Epics → **Proceed to Phase 4+5a (CREATE MODE)**
- **Count ≥ 1** → Existing Epics found → **Proceed to Phase 5b (REPLAN MODE)**

---

### Phase 4: Epic Preparation (CREATE mode only)

**Trigger:** Phase 3 determined Count = 0 (CREATE MODE)

**Objective:** Prepare all Epic documents before batch preview.

**Step 1: Auto-extract Information for ALL Domains**

For EACH domain (from Phase 2), extract answers to 5 key questions from project documentation:

1. **Q1: Business goal** - Why this Epic/domain matters
   - **Source:** requirements.md (domain objectives section)
   - **Extraction:** "The [domain] module aims to..." or "Goal: [objective]"
   - **Fallback:** architecture.md (module purpose)

2. **Q2: Key features in scope** - 3-5 bullet points of capabilities
   - **Source:** requirements.md (functional requirements for this domain)
   - **Extraction:** Bulleted lists under domain heading, feature descriptions
   - **Fallback:** architecture.md (component responsibilities)

3. **Q3: Out of scope** - Prevent scope creep
   - **Source:** requirements.md (explicitly excluded features section)
   - **Extraction:** "Not in scope:", "Future versions:", "Out of scope for [domain]:"
   - **Fallback:** Infer from requirements.md (features NOT mentioned in domain)

4. **Q4: Success criteria** - Measurable outcomes
   - **Source:** requirements.md (acceptance criteria, metrics, KPIs for domain)
   - **Extraction:** Performance targets, user metrics, quality gates
   - **Fallback:** Generic criteria based on domain type (e.g., "<200ms API response" for backend)

5. **Q5: Known risks** (Optional) - Blockers, dependencies
   - **Source:** architecture.md (technical constraints, dependencies section)
   - **Extraction:** "Risks:", "Dependencies:", "Constraints:"
   - **Fallback:** User input if critical, otherwise leave as "To be determined during Story planning"

**If extraction incomplete:**
- Show extracted information to user
- Ask ONCE for ALL missing information across ALL domains (batch question, not per-domain)
- Example: "For Epic 1 (User Management), I couldn't find success criteria. For Epic 2 (Payment), I couldn't find risks. Please provide..."

**Step 2: Generate ALL Epic Documents**

For EACH domain, generate complete Epic document using epic_template_universal.md:

**Epic indexing:**
- IF Infrastructure Epic exists (from Phase 1 Step 3) → Epic 0 (Infrastructure), Epic 1-N (business domains)
- ELSE → Epic 1-N (business domains only)

**Linear Title (will be created in Phase 5a):**
- Use Next Epic Number from kanban_board.md for sequential numbering
- Format: "Epic {Next Epic Number}: {Domain Title}"
- Example: Next = 11 → "Epic 11: Infrastructure & Operations"

**Sections:** Goal, Scope In/Out, Success Criteria, Dependencies, Risks & Mitigations, Architecture Impact, Phases

**Use extracted information** from Step 1 for all sections

**Output:** All Epic documents ready (Epic 0-N), indexed within initiative

---

### Phase 5a: Epic Creation (CREATE mode)

**Trigger:** Phase 4 completed preparation

**Objective:** Show preview, get confirmation, create all Epics in Linear.

**Step 1: Show Batch Preview (USER CONTROL POINT 2)**

Display ALL generated Epics with initiative-internal indexes:

```
📋 Epic Batch Preview (6 Epics to create)

═══════════════════════════════════════════════
Epic 0: Infrastructure & Operations
═══════════════════════════════════════════════
Goal: Establish foundational infrastructure, deployment pipeline, and operational capabilities to support all business Epics

Scope In:
- Logging and error handling framework
- Monitoring and alerting system
- CI/CD pipeline (GitHub Actions)
- Security baseline (secrets management, encryption)
- Performance optimization (caching, rate limiting)

Scope Out:
- Application-specific business logic
- User-facing features
- Domain-specific integrations

Success Criteria:
- All deployments automated via CI/CD (<10 min deployment time)
- System uptime ≥99.9%
- API response time <200ms (p95)
- Security audit passed

═══════════════════════════════════════════════
Epic 1: User Management
═══════════════════════════════════════════════
Goal: Enable users to register, authenticate, and manage their accounts securely

Scope In:
- User registration with email verification
- Login/logout with JWT authentication
- Password reset flow
- Profile management

Scope Out:
- Social login (OAuth) - planned for Epic 5
- Multi-factor authentication - future version
- User roles and permissions - part of Epic 3

Success Criteria:
- User registration <2 seconds
- Login success rate >98%
- Password reset completion rate >90%

[... all other Epics ...]

───────────────────────────────────────────────
Total: 6 Epics (Epic 0: Infrastructure, Epic 1-5: Business domains)
Type "confirm" to create all Epics in Linear
```

**Step 2: User Confirmation**

- User types "confirm" → Proceed to Step 3
- User provides feedback → Adjust documents in Phase 4, regenerate preview, repeat

### Stop Conditions (Preview Loop)

| Condition | Action |
|-----------|--------|
| User confirms (types "confirm" or approves) | STOP — proceed to creation |
| User feedback cycle >= 3 | STOP — ASK: "3 revision cycles. Proceed with current, or abandon?" |
| Epic Quality Gate score < 3/5 after 2 rework attempts | STOP — ESCALATE: "Cannot achieve quality threshold. Review scope." |

**Step 3: Create All Epics**

For EACH Epic (in sequential order for numbering consistency):

1. **Get Next Epic Number:**
   - Read current Next Epic Number from kanban_board.md
   - Example: 11

2. **Create Epic (provider-dependent):**

   **IF task_provider == "linear":**
   - `save_project({name: "Epic {N}: {Title}", description: epic_markdown, team: teamId, state: "planned"})`
   - Collect returned URL

   **ELSE IF task_provider == "github":**
   - `gh issue create -R {REPO} --title "Epic {N}: {Title}" --body "{epic_markdown}" --label "epic"`
   - Add to project + set status Backlog (per provider_github.md)
   - Collect returned issue URL

   **ELSE (file mode):**
   - `mkdir -p docs/tasks/epics/epic-{N}-{slug}/stories/`
   - `Write("docs/tasks/epics/epic-{N}-{slug}/epic.md")` with Epic markdown + file headers (`**Status:** Backlog`, `**Created:** {date}`)

3. **Update kanban_board.md:**
   - Increment Next Epic Number by 1 in Linear Configuration table
   - Add new row to Epic Story Counters: `Epic {N} | - | US001 | - | EPN_01`
   - Add to "Epics Overview" → Active: `- [Epic {N}: Title](link) - Backlog`

4. **Collect URL** (Linear/GitHub mode) or file path (file mode)

**Step 4: Display Summary**

```
✅ Created 6 Epics for initiative

Epics created:
- Epic 11: Infrastructure & Operations (Epic 0 index) [link]
- Epic 12: User Management (Epic 1 index) [link]
- Epic 13: Product Catalog (Epic 2 index) [link]
- Epic 14: Shopping Cart (Epic 3 index) [link]
- Epic 15: Payment Processing (Epic 4 index) [link]
- Epic 16: Order Management (Epic 5 index) [link]

Next Epic Number updated to: 17

Next Steps:
1. Use ln-220-story-coordinator to create Stories for each Epic (run 6 times)
2. OR use ln-200-scope-decomposer to automate Epic + Story creation
```

**Output:** Created Epic URLs + summary

**TodoWrite format:** Add Phase 1-5a todos + one todo per Epic + kanban update. Mark in_progress/completed.

---

### Phase 5b: Replan Mode (Existing Epics Found)

**Trigger:** Phase 3 determined Count ≥ 1 (REPLAN MODE)

**Full workflow:** **MANDATORY READ:** Load `references/replan_workflow.md` for complete REPLAN process.

**Summary:**
1. Load existing Epics (IF task_provider == "linear": from Linear API | IF task_provider == "github": from `gh issue list --label epic` | ELSE: from `docs/tasks/epics/*/epic.md`)
2. Compare IDEAL plan vs existing → Categorize: KEEP/UPDATE/OBSOLETE/CREATE
3. Show replan summary with diffs and warnings
4. User confirmation required
5. Execute operations (per provider_*.md) + update kanban_board.md

**Constraints:** Never auto-update/archive Epics with Stories In Progress. Never delete (use archived). Always require confirmation.

---

## Critical Rules

- **Decompose-First:** Always build IDEAL Epic plan before checking existing Epics (prevents anchoring to outdated structure)
- **Epic 0 reserved for Infrastructure:** Business domains start from Epic 1; Epic 0 auto-proposed when new project, multi-stack, or infra requirements detected
- **Auto-extract before asking:** Extract Q1-Q5 from docs (requirements.md, architecture.md, tech_stack.md) + HTML; ask user only for missing info in a single batch
- **Never auto-update Epics with In Progress Stories:** REPLAN mode requires user confirmation; Epics with active Stories get warnings, not silent changes
- **Linear title format:** "Epic {Next Epic Number}: {Domain Title}" — sequential numbering from kanban_board.md

---

## Definition of Done

Before completing work, verify ALL checkpoints:

**✅ Discovery Complete (Phase 1):**
- [ ] Team ID loaded from kanban_board.md
- [ ] Next Epic Number loaded from kanban_board.md
- [ ] Documentation scanned (requirements.md, architecture.md, tech_stack.md)
- [ ] HTML files scanned (if frontend exists)
- [ ] Infrastructure Epic decision made (YES/NO based on project conditions)

**✅ Scope Analysis Complete (Phase 2):**
- [ ] Domains auto-identified from docs + HTML
- [ ] Infrastructure Epic (Epic 0) included if applicable
- [ ] Epic list built (Epic 0-N or Epic 1-N)
- [ ] User confirmed Epic structure (CONTROL POINT 1)

**✅ Existing Epics Checked (Phase 3):**
- [ ] Epic Story Counters read from kanban_board.md
- [ ] Existing Epic count determined (0 → CREATE, ≥1 → REPLAN)

**✅ Epic Preparation Complete (Phase 4 - CREATE only):**
- [ ] Q1-Q5 auto-extracted for ALL domains
- [ ] User provided missing information if needed (batch question)
- [ ] ALL Epic documents generated (Epic 0-N indexes)

**✅ Epic Creation Complete (Phase 5a - CREATE only):**
- [ ] Batch preview shown with Epic 0-N indexes
- [ ] User confirmed preview (CONTROL POINT 2)
- [ ] ALL Epics created (Linear or file mode) with "Epic {N}: {Title}" format (N = Next Epic Number)
- [ ] kanban_board.md updated after EACH Epic:
  - Next Epic Number incremented by 1
  - Epic Story Counters row added
  - Epics Overview updated
- [ ] Summary displayed with all Epic URLs

**✅ Epic Replan Complete (Phase 5b - REPLAN only):**
- **MANDATORY READ:** Load `references/replan_workflow.md` for full checklist

**Output:** List of Linear Project URLs (Epic {N}: {Title}) + Next Epic Number value

---

## Example Usage

**Request:** "Create epics for e-commerce platform"

**Flow:** Phase 1 (discover Team ID=Product, Next=11, scan docs+HTML) → Phase 2 (identify 6 domains: Infrastructure, User, Products, Cart, Payment, Orders) → Phase 3 (count=0 → CREATE) → Phase 4 (auto-extract Q1-Q5, generate docs) → Phase 5a (preview, confirm, create in Linear: Epic 11-16)

**Result:** 6 Epics created (Epic 0-5 internal indexes, Epic 11-16 Linear titles)

---

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after all phases complete. Output to chat using the `planning-coordinator` format.

## Reference Files

- **MANDATORY READ:** `shared/references/environment_state_contract.md`
- **MANDATORY READ:** `shared/references/storage_mode_detection.md`
- **[MANDATORY] Problem-solving approach:** `shared/references/problem_solving.md`
- **Orchestrator lifecycle:** `shared/references/orchestrator_pattern.md`
- **Auto-discovery patterns:** `shared/references/auto_discovery_pattern.md`
- **Decompose-first pattern:** `shared/references/decompose_first_pattern.md`
- **Numbering conventions:** `shared/references/numbering_conventions.md` (Epic 0 reserved, Linear numbering)
- **Issue creation workflow:** `shared/references/issue_creation_workflow.md`
- **linear_integration.md:** Discovery patterns + Linear API reference (moved to `shared/templates/linear_integration.md`)
- **epic_template_universal.md:** Epic template structure
- **replan_workflow.md:** Complete REPLAN mode workflow (Phase 5b)

---

## Best Practices

- **Research first:** Scan docs (requirements.md, architecture.md, tech_stack.md) + HTML before asking user
- **Epic 0 for Infrastructure:** Reserved index for Infrastructure Epic; business domains start from Epic 1
- **Business Epic grouping:** 1 Epic = 5-10 Stories = 1 business capability (not technical components)
- **Auto-extraction:** Extract Q1-Q5 from docs before asking user; ask only for missing info
- **Linear Title:** "Epic {Next Epic Number}: {Domain}" format
- **Business-focused Scope:** List USER CAPABILITIES, not technical tasks
- **Measurable criteria:** "<200ms" not "fast"; ">98% login rate" not "reliable"
- **No code snippets:** High-level features and goals only

---

**Version:** 8.0.0
**Last Updated:** 2026-04-05
