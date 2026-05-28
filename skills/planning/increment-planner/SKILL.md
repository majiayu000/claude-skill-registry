---
name: increment-planner
description: Creates comprehensive implementation plans for ANY type of SpecWeave increment (feature, hotfix, bug, change-request, refactor, experiment). Supports all work types from features to bug investigations to POCs. Activates for: increment planning, feature planning, hotfix, bug investigation, root cause analysis, SRE investigation, change request, refactor, POC, prototype, spike work, experiment, implementation plan, create increment, organize work, break down work, new product, build project, MVP, SaaS, app development, tech stack planning, production issue, critical bug, stakeholder request.
visibility: internal
invocableBy:
  - sw:increment
---

# Increment Planner Skill

**⚠️ INTERNAL SKILL - Only invoked by `/sw:increment` command**

**Self-contained increment planning that works in ANY user project after `specweave init`.**

**Do not call this skill directly**. Use `/sw:increment` command instead, which invokes this skill automatically.

---

## Purpose

Automates creation of increment structure for ANY type of work:
- ✅ Auto-numbered directories (`0001-9999`)
- ✅ Duplicate detection (prevents conflicts)
- ✅ Complete file templates (spec.md, plan.md, tasks.md, metadata.json)
- ✅ Proper YAML frontmatter
- ✅ Works in all user projects (self-contained)

---

## Increment Types

| Type | Description | Use When | WIP Limit |
|------|-------------|----------|-----------|
| **feature** | New functionality | Adding features | Max 2 active |
| **hotfix** | Critical production fixes | Production broken | Unlimited |
| **bug** | Bug investigation with RCA | Needs root cause analysis | Unlimited |
| **change-request** | Stakeholder requests | Business changes | Max 2 active |
| **refactor** | Code improvement | Technical debt | Max 1 active |
| **experiment** | POC/spike work | Exploring options | Unlimited |

---

## When to Use

✅ **USE** when:
- Creating features, hotfixes, bug investigations, refactors, POCs
- Planning structured work in user projects
- Need complete increment scaffold with templates

❌ **DON'T USE** when:
- User asking general questions
- Another skill already handling request
- Already in active increment planning

---

## Critical Rules

### 0. **Project**: Field is MANDATORY (v0.35.0+ - HIGHEST PRIORITY!)

**⛔ EVERY User Story MUST have `**Project**:` field - NO EXCEPTIONS!**

This applies to BOTH single-project AND multi-project modes:
- **Single-project**: Use `config.project.name` value (e.g., `**Project**: my-app`)
- **Multi-project**: Use one of `multiProject.projects` keys (e.g., `**Project**: frontend-app`)

**HOW TO GET THE PROJECT VALUE:**
1. Run `specweave context projects`
2. Use project ID from output

**Single-project output:**
```json
{ "level": 1, "projects": [{"id": "my-app"}] }
→ Use: **Project**: my-app
```

**Multi-project output:**
```json
{ "level": 1, "projects": [{"id": "frontend"}, {"id": "backend"}] }
→ Pick appropriate project per US
```

**2-level output (ADO/JIRA):**
```json
{ "level": 2, "projects": [...], "boardsByProject": {"corp": [{"id": "digital-ops"}]} }
→ ALSO add: **Board**: digital-ops
```

**EXAMPLE (v0.35.0+):**
```markdown
### US-001: Show Last 2 Git Commits
**Project**: aac              # ← MANDATORY! Value from config
**As a** developer, I want to see the last 2 git commits...
```

**⛔ NEVER GENERATE:**
```markdown
### US-001: Feature Name
**As a** user, I want...      # ← MISSING **Project**: = INVALID!
```

**EDGE CASES:**
- **Empty config.project.name**: Run `specweave init` to configure
- **Empty multiProject.projects**: Invalid config - ask user to configure projects
- **Project name with special chars**: Only `a-z`, `0-9`, `-` allowed

### 1. Increment Naming (MANDATORY)

**Format**: `####-descriptive-kebab-case-name`

✅ **CORRECT**:
```
0001-user-authentication
0002-payment-processing
0003-email-notifications
```

❌ **WRONG**:
```
0001              ← No description
0002-feature      ← Too generic
my-feature        ← No number
```

### 2. NO Agent Spawning from Skills (CRITICAL)

**Skills MUST NOT spawn content-generating agents via Task() tool.**

**Why**: Context explosion causes Claude Code crashes:
- Skill (1500 lines) loads into context
- Agent (600 lines) spawned
- Agent output (2000+ lines) generated
- **Total: 4000+ lines = CRASH** 💥

**✅ SAFE Workflow**:
```
1. Skill creates basic templates (50 lines each)
2. Skill outputs: "Tell Claude: 'Complete spec for increment 0005'"
3. Agent activates in MAIN context (NOT nested) = SAFE
```

### 3. metadata.json is MANDATORY

Every increment MUST have `metadata.json` or:
- ❌ Status tracking broken
- ❌ WIP limits don't work
- ❌ External sync fails (GitHub/Jira/ADO)
- ❌ All increment commands fail

**Complete template** (values from `.specweave/config.json`):
```json
{
  "id": "0001-feature-name",
  "status": "planned",
  "type": "feature",
  "priority": "P1",
  "created": "2025-11-24T12:00:00Z",
  "lastActivity": "2025-11-24T12:00:00Z",
  "testMode": "<FROM config.testing.defaultTestMode OR 'test-after'>",
  "coverageTarget": <FROM config.testing.defaultCoverageTarget OR 80>,
  "feature_id": null,
  "epic_id": null,
  "externalLinks": {}
}
```

**NOTE**: Always read `testMode` and `coverageTarget` from config, don't hardcode!

**Testing Mode Configuration**:
- **User Projects**: Default `testMode: "test-after"` (init wizard default, fast iteration)
- **SpecWeave Core**: `testMode: "TDD"` required (mission-critical framework)
- **Override per-increment**: Can be changed in metadata.json for specific needs
- **Quality Gates**: `/sw:done` validates test coverage meets targets
- **Coverage Targets**: Unit (>85%), Integration (>80%), E2E (>90%) - see config.testing.coverageTargets

### 4. Increment Structure

**Directory structure**:
```
.specweave/increments/0001-feature-name/
├── spec.md          # WHAT & WHY (user stories, acceptance criteria) - REQUIRED
├── plan.md          # HOW (technical design, architecture) - OPTIONAL
├── tasks.md         # STEPS (implementation tasks with embedded tests) - REQUIRED
└── metadata.json    # Metadata - REQUIRED
```

**plan.md is OPTIONAL** - create only for complex features with architecture decisions. Skip for bug fixes, migrations, hotfixes.

**NO separate tests.md** - tests embedded in tasks.md (v0.7.0+)

---

## Workflow (Safe, Self-Contained)

### STEP 0-Prime: Self-Awareness Check (v1.0.102+)

**🚨 CRITICAL: Detect if running in SpecWeave repository itself!**

**Purpose**: Prevent pollution of SpecWeave's own increment history with test examples or confusion between framework development vs user project work.

**Implementation**:

```typescript
import { detectSpecWeaveRepository, logRepositoryWarnings } from './src/utils/repository-detector.js';

// Detect if this is SpecWeave's own repository
const repoInfo = detectSpecWeaveRepository(process.cwd());

// Log warnings if SpecWeave repo detected
logRepositoryWarnings(repoInfo);

// If SpecWeave repo detected, prompt user
if (repoInfo.isSpecWeaveRepo) {
  console.log('⚠️  You are running in the SpecWeave framework repository itself!');
  console.log('');
  console.log('   This increment will be created in SpecWeave\'s own .specweave/ folder.');
  console.log('');
  console.log('   Please confirm your intent:');
  console.log('');
  console.log('   1️⃣  SpecWeave Development - Working on the framework itself');
  console.log('      Example: "Add new skill routing validator"');
  console.log('');
  console.log('   2️⃣  Testing/Example - Creating test increment for examples');
  console.log('      💡 Consider using examples/ folder instead');
  console.log('');
  console.log('   3️⃣  Cancel - Not what I intended');
  console.log('');

  // In interactive Claude session, ASK user to choose
  // In CI/automation, check for --force-specweave-dev flag

  const choice = await promptUser('Your choice (1, 2, or 3): ');

  if (choice === '3') {
    throw new Error('Increment creation cancelled by user.');
  }

  if (choice === '2') {
    console.log('');
    console.log('💡 Recommendation: Create test examples in separate directory:');
    console.log('   mkdir -p examples/0001-todo-api');
    console.log('   cd examples/0001-todo-api');
    console.log('   specweave init .');
    console.log('');
    const proceed = await promptUser('Proceed anyway in SpecWeave repo? (y/N): ');
    if (proceed.toLowerCase() !== 'y') {
      throw new Error('Increment creation cancelled. Please use examples/ folder for tests.');
    }
  }

  // If choice === '1', continue with SpecWeave development
  console.log('✅ Proceeding with SpecWeave framework development');
  console.log('');
}
```

**When to Skip**:
- `--force-specweave-dev` flag provided (CI/automation)
- Not running in SpecWeave repo (normal user project)

**Why This Matters**:
The triggering bug (0001-todo-api test example created in SpecWeave repo) happened because there was NO distinction between:
- Testing SpecWeave with an example → Should use examples/ folder
- Developing SpecWeave features → Should use .specweave/ folder

This guard makes the distinction explicit and prevents confusion.

---

### STEP 0: Detect Multi-Project Mode (MANDATORY FIRST!)

**⚠️ CRITICAL: Before creating ANY user stories, detect if this is a multi-project (umbrella) setup!**

**Automated Detection**: `src/utils/multi-project-detector.ts` provides `detectMultiProjectMode(projectRoot)` which checks ALL config formats and returns `{ isMultiProject, projects, detectionReason }`.

**Manual check (for agents)**: Read `.specweave/config.json` and check:
- `umbrella.enabled: true` with `childRepos[]`
- `multiProject.enabled: true` with `projects{}`
- `sync.profiles[].config.boardMapping` exists
- Multiple folders in `.specweave/docs/internal/specs/`

**If multi-project detected (`umbrella.enabled: true` OR multiple project folders exist):**
- ✅ **MUST** generate project-scoped user stories: `US-FE-001`, `US-BE-001`, `US-SHARED-001`
- ✅ **MUST** use project-scoped AC-IDs: `AC-FE-US1-01`, `AC-BE-US1-01`
- ✅ **MUST** group user stories by project in spec.md
- ✅ **MUST** infer project from repo name if available (e.g., `sw-app-fe` → FE, `sw-app-be` → BE)

**Project Prefix Detection from Repo Names:**
```
sw-thumbnail-ab-fe     → prefix: FE (frontend)
sw-thumbnail-ab-be     → prefix: BE (backend)
sw-thumbnail-ab-shared → prefix: SHARED (shared library)
my-app-mobile          → prefix: MOBILE (mobile app)
infra-terraform        → prefix: INFRA (infrastructure)
```

**Store this for use in STEP 4 (spec.md generation)!**

---

### STEP 0A: Read Config Values (MANDATORY)

```bash
# Read testMode (default: "test-after" for user projects)
testMode=$(cat .specweave/config.json | jq -r '.testing.defaultTestMode // "test-after"')

# Read coverageTarget (default: 80)
coverageTarget=$(cat .specweave/config.json | jq -r '.testing.defaultCoverageTarget // 80')

# NEW (v1.0.111+): Select template based on testMode
if [ "$testMode" = "TDD" ]; then
  TASK_TEMPLATE="tasks-tdd-single-project.md"
  INCLUDE_TDD_CONTRACT=true
  echo "🔴 TDD MODE: Using TDD task template with RED-GREEN-REFACTOR triplets"
else
  TASK_TEMPLATE="tasks-single-project.md"
  INCLUDE_TDD_CONTRACT=false
fi

echo "Using testMode: $testMode"
echo "Using coverageTarget: $coverageTarget"
echo "Using task template: $TASK_TEMPLATE"
```

**Store these values for use in STEP 4 and STEP 7!**

**TDD Template Selection (v1.0.111+)**:
- When `testMode: "TDD"` → Use `tasks-tdd-single-project.md` with TDD triplet structure
- When `testMode: "test-after"` (default) → Use standard `tasks-single-project.md`
- TDD mode also injects `## TDD Contract` section into spec.md

### STEP 0B: Get Project Context (MANDATORY - BLOCKING!)

**⛔ THIS IS A HARD BLOCK - YOU CANNOT PROCEED WITHOUT PROJECT CONTEXT!**

**🚨 FAILURE TO COMPLETE THIS STEP = spec.md WILL BE BLOCKED BY VALIDATION HOOK!**

**🧠 ULTRATHINK REQUIRED - ANALYZE ALL AVAILABLE CONTEXT FIRST!**

Before generating ANY spec.md content, you MUST:

**0. ULTRATHINK - Gather context BEFORE running API:**
```bash
# 1. Check existing project folders in living docs
ls .specweave/docs/internal/specs/

# 2. Check how recent increments assigned projects
grep -r "^\*\*Project\*\*:" .specweave/increments/*/spec.md | tail -10

# 3. Read config.json for project.name or multiProject.projects
cat .specweave/config.json | jq '.project.name, .multiProject'
```

**1. RUN THE CONTEXT API (via Bash tool):**
```bash
specweave context projects
```

**2. CAPTURE AND STORE THE OUTPUT:**

For 1-level structures:
```json
{
  "level": 1,
  "projects": [{"id": "my-app", "name": "My App"}],
  "detectionReason": "multiProject configuration"
}
```

For 2-level structures (ADO/JIRA boards):
```json
{
  "level": 2,
  "projects": [{"id": "acme-corp", "name": "ACME Corporation"}],
  "boardsByProject": {
    "acme-corp": [
      {"id": "digital-ops", "name": "Digital Operations"},
      {"id": "mobile-team", "name": "Mobile Team"}
    ]
  }
}
```

**3. 🧠 ULTRATHINK - SMART PROJECT RESOLUTION (v0.35.0+ CRITICAL!):**

**RESOLUTION PRIORITY (MUST FOLLOW THIS ORDER!):**
```
1. ✅ EXACT MATCH: config.project.name or multiProject.projects key → USE IT
2. ✅ LIVING DOCS: Existing folder in specs/ → USE THAT PROJECT ID
3. ✅ RECENT PATTERNS: Same feature type in past increments → USE SAME PROJECT
4. ⚠️  UNCERTAIN: Multiple valid options OR no clear match → ASK USER!
5. 🔄 FALLBACK: If all else fails → USE "default" (NEVER "specweave"!)
```

**⚠️ CRITICAL: IF UNCERTAIN - YOU MUST ASK THE USER!**
```
I found multiple potential projects for this feature:
- frontend-app (keywords: UI, form, React)
- backend-api (keywords: API, endpoint)

Which project should I assign to this feature?
```

**❌ NEVER DO THIS:**
- Silently assign to "specweave" (that's the framework name, not user's project!)
- Guess without analyzing context
- Skip asking when genuinely uncertain

**✅ CORRECT FALLBACK (when no projects configured):**
```
**Project**: default
```

**4. RESOLVE PROJECT/BOARD FOR EACH USER STORY:**

```
CONTEXT_OUTPUT = <output from specweave context projects>

For each US you will generate:
  IF CONTEXT_OUTPUT.level == 1:
    US.project = select from CONTEXT_OUTPUT.projects[].id

  IF CONTEXT_OUTPUT.level == 2:
    US.project = select from CONTEXT_OUTPUT.projects[].id
    US.board = select from CONTEXT_OUTPUT.boardsByProject[project][].id
```

**5. NOW PROCEED TO STEP 1 (with resolved values stored)**

---

**VALIDATION RULES (ENFORCED BY HOOK):**

```
✅ REQUIRED: Actually RUN "specweave context projects" command
✅ REQUIRED: Parse the JSON and extract project IDs
✅ REQUIRED: project field MUST match one of projects[].id from output
✅ REQUIRED: board field (2-level) MUST match one of boardsByProject[project][].id
✅ REQUIRED: Each US has **Project**: and **Board**: (2-level) with RESOLVED values
✅ REQUIRED: ASK USER when uncertain (multiple valid options or no clear match)

❌ FORBIDDEN: Skipping this step and generating spec.md directly
❌ FORBIDDEN: Inventing project names not in the API output
❌ FORBIDDEN: Using "specweave" as project name (it's the framework, not user's project!)
❌ FORBIDDEN: Using folder names as project (e.g., "my-project-folder")
❌ FORBIDDEN: Using {{PROJECT_ID}} or {{BOARD_ID}} placeholders
❌ FORBIDDEN: Creating spec.md for 2-level without board: field
❌ FORBIDDEN: Generating spec.md without running context API first
❌ FORBIDDEN: Silently guessing project without analyzing context
```

**WHY THIS IS BLOCKING:**
- Hook `spec-project-validator.sh` BLOCKS spec.md with placeholders or invalid projects
- Without resolved project/board, living docs sync FAILS
- Without resolved project/board, external tool sync (GitHub/JIRA/ADO) FAILS
- User gets blocked error and must manually fix - BAD UX!

**Structure Levels:**
- **1-Level**: `internal/specs/{project}/FS-XXX/` - requires `project` per US
- **2-Level**: `internal/specs/{project}/{board}/FS-XXX/` - requires `project` AND `board` per US

**Alternative: Interactive Selection:**
```bash
specweave context select
# Returns auto-selected or prompts for selection
```

**Get boards for a specific project (2-level):**
```bash
specweave context boards --project=acme-corp
```

**Project/Board Selection - ULTRA-SMART LOGIC (MANDATORY BEFORE STEP 4!):**

**⚠️ CORE PRINCIPLE: Each User Story belongs to exactly ONE project (1-level) or ONE project+board (2-level). An increment can contain USs spanning MULTIPLE projects/boards.**

---

### RULE 0: LEVERAGE ALL AVAILABLE CONTEXT (v0.33.0+ CRITICAL!)

**🧠 YOU ARE AN LLM WITH FULL CONTEXT ACCESS - USE IT!**

Before asking the user ANYTHING about project/board, you MUST analyze:

**1. Living Docs Structure** (`.specweave/docs/internal/specs/`):
```bash
# List existing project folders
ls -la .specweave/docs/internal/specs/
# Example output: frontend-app/, backend-api/, mobile-app/, shared-lib/
```
→ These ARE the actual project IDs! Use them directly.

**2. Existing Increment Patterns** (`.specweave/increments/`):
```bash
# Read recent increments to see project assignments
grep -r "^\*\*Project\*\*:" .specweave/increments/*/spec.md | tail -20
```
→ Learn from how past USs were assigned to projects.

**3. Config projectMappings** (`.specweave/config.json`):
```bash
cat .specweave/config.json | jq '.projectMappings'
```
→ Use ACTUAL project IDs from config, not generic keywords.

**4. Git Remotes** (for repo-based projects):
```bash
git remote -v | head -2
```
→ If repo is `myorg/frontend-app`, that's likely the project.

**5. Feature Description + US Content**:
- Analyze the feature user is describing
- Match against project patterns from above sources
- Map generic terms to actual project IDs

**MAPPING EXAMPLE:**
```
User says: "Add login form to the frontend"
You detect: "frontend" keyword

WRONG: Assign project = "frontend" (generic, may not exist!)
RIGHT: Check living docs → find "frontend-app" folder → Assign project = "frontend-app"
```

**RESOLUTION PRIORITY:**
```
1. Exact match in projectMappings keys → USE IT
2. Exact match in living docs folders → USE IT
3. Pattern match in recent increment specs → USE SAME PROJECT
4. Keyword → Map to closest projectMappings/folder
5. ONLY IF ALL ABOVE FAIL → Ask user with dropdown of valid options
```

**FORBIDDEN:**
- ❌ Inventing project names not in config/folders
- ❌ Using generic keywords ("frontend") when actual ID exists ("frontend-app")
- ❌ Asking user when context provides clear answer
- ❌ Assigning `{{PROJECT_ID}}` placeholder

---

### SMART SELECTION DECISION TREE

**RULE 1: NO QUESTION IF ONLY 1 OPTION**
```
IF 1-level AND only 1 project → AUTO-SELECT silently
IF 2-level AND only 1 project AND only 1 board → AUTO-SELECT silently
```

**RULE 2: KEYWORD-BASED AUTO-DETECTION (v0.33.0+)**

Use `CrossCuttingDetector` utility for programmatic detection:

```typescript
import { detectCrossCutting } from 'src/utils/cross-cutting-detector.js';

const result = detectCrossCutting("OAuth with React frontend and Node backend");
// result.isCrossCutting = true
// result.suggestedProjects = ["frontend", "backend"]
// result.confidence = "high"
```

Or analyze feature description and US content for keywords:

**Project-Level Keywords (1-level and 2-level):**
```
Frontend (FE) keywords:
  UI, form, button, page, component, React, Vue, Angular, Next.js,
  CSS, style, responsive, chart, dashboard, view, modal, widget,
  Tailwind, Material-UI, Recharts

Backend (BE) keywords:
  API, endpoint, REST, GraphQL, database, query, migration, service,
  controller, authentication, JWT, session, middleware, CRUD,
  Redis, PostgreSQL, MongoDB, microservice

Mobile keywords:
  mobile, iOS, Android, React Native, Flutter, Expo, app, native,
  push notification, offline, AsyncStorage, screen, touch, gesture

Infrastructure (INFRA) keywords:
  deploy, CI/CD, Docker, Kubernetes, terraform, monitoring,
  logging, pipeline, AWS, Azure, GCP, nginx, Helm, ArgoCD

Shared (SHARED) keywords:
  types, interfaces, utilities, validators, shared, common, library,
  SDK, models, constants, helpers
```

**Board-Level Keywords (2-level structures only):**
```
When project has multiple boards, also match board-specific keywords:

analytics/reporting: analytics, metrics, KPI, dashboard, report, chart, graph
user-management: user, auth, login, registration, profile, permissions, roles
integrations: integration, webhook, API, third-party, sync, import, export
payments: payment, billing, subscription, invoice, stripe, checkout
notifications: notification, alert, email, SMS, push, messaging
devops/platform: deploy, infrastructure, monitoring, CI/CD, pipeline
```

**RULE 3: CONFIDENCE CALCULATION FORMULA**
```
confidence = (matched_keywords / total_feature_keywords) × 100

Example: "Add React login form with JWT authentication"
  Keywords found: React (FE), login (FE), form (FE), JWT (BE), authentication (BE)
  FE matches: 3, BE matches: 2
  FE confidence: 3/5 = 60%
  BE confidence: 2/5 = 40%
  → Primary: FE (60%), Secondary: BE (40%)
  → SUGGEST: "Frontend (60%), but also touches Backend (40%)"

If multiple projects have similar confidence (within 15%):
  → Treat as MULTI-PROJECT feature
  → Auto-split USs by detected keywords
```

**RULE 4: CONFIDENCE-BASED DECISION**
```
>80% single project → AUTO-SELECT with notification (no question)
50-80% single project → SUGGEST with quick confirm option
Multiple projects within 15% → AUTO-SPLIT across projects
<50% OR ambiguous → ASK user with all options
```

**RULE 5: FALLBACK TO DEFAULTS**
```
IF US has explicit **Project**: field → USE IT
ELSE IF frontmatter has default_project → USE default_project
ELSE → ASK user (should not happen if flow followed correctly)

Same logic applies to **Board**: and default_board for 2-level
```

---

### DECISION FLOWCHART

```
START
  │
  ▼
┌─────────────────────────────────────┐
│ 1. Detect structure level (1 or 2) │
│ 2. Count available projects/boards │
└─────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────┐
│ ONLY 1 PROJECT?                     │
│ (1-level: 1 project)                │
│ (2-level: 1 project + 1 board)      │
└─────────────────────────────────────┘
  │
  ├── YES ──► AUTO-SELECT SILENTLY
  │           Output: "✅ Project: {name} (auto-selected)"
  │           NO QUESTION ASKED
  │
  ▼ NO
┌─────────────────────────────────────┐
│ ANALYZE KEYWORDS in feature desc   │
│ Calculate confidence per project   │
└─────────────────────────────────────┘
  │
  ├── HIGH CONFIDENCE (>80% single) ──► AUTO-SELECT + NOTIFY
  │   Output: "✅ Detected: {project} (keywords: form, React)"
  │
  ├── MULTI-PROJECT (within 15%) ──► AUTO-SPLIT USs
  │   Output: "🔀 Multi-project detected:
  │            • US-001 (Login UI) → web-app (60%)
  │            • US-002 (Auth API) → api-service (55%)
  │            Proceed? (Y/n)"
  │
  ├── MEDIUM CONFIDENCE (50-80%) ──► SUGGEST + CONFIRM
  │   Output: "📍 Suggested: {project}. Confirm? (Y/n)"
  │
  ▼ LOW CONFIDENCE (<50%)
┌─────────────────────────────────────┐
│ ASK USER with ALL options listed   │
│ multiSelect: true                  │
│ Show complete list (never truncate)│
└─────────────────────────────────────┘
```

---

### PER-USER-STORY ASSIGNMENT MODEL

**CRITICAL: Assignment is at USER STORY level, not increment level!**

Each US in spec.md has its own project (and board for 2-level):

```markdown
## User Stories

### US-001: Login Form UI
**Project**: web-app
**Board**: frontend  <!-- 2-level only -->
**As a** user...

### US-002: Auth API Endpoints
**Project**: api-service
**Board**: backend  <!-- 2-level only -->
**As a** developer...

### US-003: Mobile Login Screen
**Project**: mobile-app
**Board**: mobile-team  <!-- 2-level only -->
**As a** mobile user...
```

**User can manually change project/board per US at any time by editing spec.md!**

---

### EXAMPLE SCENARIOS

**Scenario 1: Single Project (NO QUESTION)**
```
Config: 1 project (my-app)
Feature: "Add user authentication"

→ AUTO-SELECT: my-app
→ Output: "✅ Project: my-app (single project - auto-selected)"
→ NO question asked
```

**Scenario 2: Multiple Projects, Clear Keywords (AUTO-DETECT)**
```
Config: 3 projects (web-app, api-service, mobile-app)
Feature: "Add React dashboard with charts"

→ Keyword analysis: "React" (FE), "dashboard" (FE), "charts" (FE)
→ Confidence: 95% → web-app
→ Output: "✅ Detected project: web-app (keywords: React, dashboard, charts)"
→ NO question asked (high confidence)
```

**Scenario 3: Multiple Projects, Multi-Area Feature (SMART SPLIT)**
```
Config: 3 projects (web-app, api-service, shared-lib)
Feature: "User authentication with JWT"

→ Analyze: This spans FE (login form) + BE (auth API) + possibly shared (types)
→ Output:
  "🔍 This feature likely spans multiple projects:

   Based on 'user authentication with JWT', I'll create:
   • US-001: Login/Register UI → web-app (keywords: UI, form)
   • US-002: Auth API endpoints → api-service (keywords: API, JWT)
   • US-003: Auth types/validators → shared-lib (keywords: types, shared)

   ✅ Proceed with this assignment? (Y/n)
   💡 You can modify project per US in spec.md anytime"
```

**Scenario 4: 2-Level, Single Project, Auto-Detect Board**
```
Config: 1 project (enterprise-corp), 5 boards (analytics, frontend, backend, mobile, devops)
Feature: "Add reporting dashboard"

→ Project: AUTO-SELECT enterprise-corp (only option)
→ Board keywords: "reporting" → analytics, "dashboard" → frontend
→ Confidence: 70% analytics, 60% frontend
→ Output:
  "✅ Project: enterprise-corp (auto-selected)
   📍 Suggested board: analytics (keyword: reporting)

   Confirm or select different board:
   1. analytics (suggested)
   2. frontend
   3. backend
   4. mobile
   5. devops"
```

**Scenario 5: Completely Ambiguous (ASK WITH ALL OPTIONS)**
```
Config: 4 projects (proj-a, proj-b, proj-c, proj-d)
Feature: "Improve system performance"

→ Keyword analysis: No clear project match
→ Output:
  "❓ Which project(s) should this increment target?

   Available projects:
   • proj-a - E-commerce frontend
   • proj-b - Order processing API
   • proj-c - Mobile shopping app
   • proj-d - Infrastructure/DevOps

   Select one or more (comma-separated, e.g., '1,2' or 'proj-a,proj-b'):"
```

---

### VALIDATION RULES

```
❌ FORBIDDEN: Asking project question when only 1 project exists
❌ FORBIDDEN: Asking board question when only 1 board exists in project
❌ FORBIDDEN: Hiding options behind "Let me see all" - ALWAYS show complete list
❌ FORBIDDEN: Truncating project/board lists
❌ FORBIDDEN: Assigning ALL USs to same project when content clearly differs
✅ REQUIRED: Auto-select when only 1 option available
✅ REQUIRED: Use keyword matching before asking user
✅ REQUIRED: Each US has explicit project (and board for 2-level) assignment
✅ REQUIRED: Allow user to modify assignments per-US in spec.md
✅ REQUIRED: When asking, show ALL options with descriptions
```

---

### SPEC.MD YAML FORMAT

**1-Level Structure:**
```yaml
---
increment: 0045-user-auth
title: "User Authentication"
# Optional default (used if US doesn't specify)
default_project: web-app
---
```

**2-Level Structure:**
```yaml
---
increment: 0045-user-auth
title: "User Authentication"
# Optional defaults (used if US doesn't specify)
default_project: enterprise-corp
default_board: backend
---
```

**Store detected/selected values for use in STEP 4!**

---

### STEP 1: Get Next Increment Number

Use helper script:
```bash
node plugins/specweave/skills/increment-planner/scripts/feature-utils.js next
# Returns: "0021"
```

Or manually scan:
```bash
ls -1 .specweave/increments/ | grep -E '^[0-9]{4}-' | sort | tail -1
# Get highest number, add 1
```

### STEP 1.5: Validate Increment Number (v1.0.102+)

**Warn if non-sequential number is requested.**

```typescript
import { validateIncrementNumber, logValidationResult } from './src/core/increment-validator.js';

// Get all existing increments (including archived/paused)
const existingIncrements = [
  ...fs.readdirSync('.specweave/increments/'),
  ...fs.readdirSync('.specweave/increments/_archive/').map(f => `_archive/${f}`),
  ...fs.readdirSync('.specweave/increments/_paused/').map(f => `_paused/${f}`)
].filter(f => /^\d{4}-/.test(f));

// Validate requested number
const result = validateIncrementNumber(requestedNumber, existingIncrements);

// Log warnings and suggestions
logValidationResult(result);

// If invalid, STOP
if (!result.isValid) {
  throw new Error('Invalid increment number. See warnings above.');
}

// If valid but has warnings, prompt user to confirm
if (result.warnings.length > 0) {
  const proceed = await promptUser(`Continue with ${requestedNumber}? (Y/n)`);
  if (!proceed) {
    throw new Error('Increment creation cancelled by user.');
  }
}
```

**Example output for non-sequential number:**
```
⚠️  Increment Number Warning
   ⚠️  Skipping 2 number(s): 0158 to 0159
   💡 Consider using 0158 for sequential tracking.
   💡 Non-sequential numbers can make it harder to track increment history.

Continue with 0160? (Y/n)
```

### STEP 2: Check for Duplicates

```bash
node plugins/specweave/skills/increment-planner/scripts/feature-utils.js check-increment 0021
# If exists: STOP and inform user
```

### STEP 3: Create Directory Structure

```bash
mkdir -p .specweave/increments/0021-feature-name
```

**⚠️ CRITICAL: Increment Folder Structure Rules**

**ONLY these files allowed at increment ROOT:**
- `metadata.json` - Increment state (auto-managed)
- `spec.md` - Specification
- `plan.md` - Implementation plan
- `tasks.md` - Task list

**ALL other files MUST go in subfolders:**
```
.specweave/increments/####-name/
├── reports/     # Validation reports, QA, completion summaries
├── logs/        # Debug logs, session traces
├── scripts/     # Helper scripts
├── docs/        # Additional documentation, domain knowledge
└── backups/     # Backup files
```

### STEP 4: Create metadata.json FIRST (MANDATORY - CRITICAL ORDER!)

**🚨 CRITICAL: metadata.json MUST be created BEFORE spec.md!**

The `metadata-json-guard.sh` hook BLOCKS spec.md creation if metadata.json doesn't exist.
This prevents broken increments that lack proper tracking.

**IMPORTANT**: Read `testMode` and `coverageTarget` from `.specweave/config.json`:

```bash
# Read config to get defaultTestMode and defaultCoverageTarget
cat .specweave/config.json | jq -r '.testing.defaultTestMode // "test-after"'
cat .specweave/config.json | jq -r '.testing.defaultCoverageTarget // 80'
```

Create `.specweave/increments/0021-feature-name/metadata.json`:

```json
{
  "id": "0021-feature-name",
  "status": "planned",
  "type": "feature",
  "priority": "P1",
  "created": "2025-11-24T12:00:00Z",
  "lastActivity": "2025-11-24T12:00:00Z",
  "testMode": "<VALUE FROM config.testing.defaultTestMode OR 'test-after'>",
  "coverageTarget": <VALUE FROM config.testing.defaultCoverageTarget OR 80>,
  "feature_id": null,
  "epic_id": null,
  "externalLinks": {}
}
```

**Use Write tool to create this file IMMEDIATELY after creating directory.**

**Example Logic**:
```javascript
// Read config
const config = JSON.parse(fs.readFileSync('.specweave/config.json', 'utf8'));
const testMode = config?.testing?.defaultTestMode || 'test-after';
const coverageTarget = config?.testing?.defaultCoverageTarget || 80;

// Create metadata with config values
const metadata = {
  id: "0021-feature-name",
  status: "planned",
  type: "feature",
  priority: "P1",
  created: new Date().toISOString(),
  lastActivity: new Date().toISOString(),
  testMode: testMode,  // ← FROM CONFIG!
  coverageTarget: coverageTarget,  // ← FROM CONFIG!
  feature_id: null,
  epic_id: null,
  externalLinks: {}
};
```

### STEP 5: Create spec.md Template

**⚠️ This step REQUIRES metadata.json to exist (created in STEP 4)!**

Create `.specweave/increments/0021-feature-name/spec.md`:

**⚠️ CRITICAL: You MUST have PROJECT_ID (and BOARD_ID for 2-level) from STEP 0B before proceeding!**

**⚠️ IMPORTANT: Use the correct template based on STEP 0 detection!**

#### 5A: 1-Level Structure (GitHub, Single Project, Multi-Repo without ADO/JIRA)

**USE THIS WHEN**: `specweave context projects` returns `level: 1`

**Examples of 1-level**:
- GitHub sync profiles (each repo = project)
- Single project mode
- Umbrella repos WITHOUT multiple teams

**Template Rules for 1-level:**
- Each User Story has `**Project**:` field
- **NO `**Board**:` field** - GitHub doesn't have boards!
- User story IDs: `US-001`, `US-002` (or `US-API-001`, `US-WEB-001` for multi-repo)
- AC-IDs: `AC-US1-01` (or `AC-API-US1-01` for multi-repo)

**Example 1-level spec.md:**
```markdown
### US-API-001: Create Auth API
**Project**: sw-content-repurposer-api

**As a** frontend, I want auth endpoints...

**Acceptance Criteria**:
- [ ] **AC-API-US1-01**: POST /auth/login returns JWT
```

**⚠️ CRITICAL: Do NOT add `**Board**:` for 1-level structures!**

#### 5B: 2-Level Structure (ADO Area Paths, JIRA Boards, Multi-Team Umbrella)

**USE THIS WHEN**: `specweave context projects` returns `level: 2`

**Examples of 2-level**:
- ADO with `areaPathMapping`
- JIRA with multiple `boardMapping.boards`
- Umbrella repos with multiple teams

**Template Rules for 2-level:**
- Each User Story has BOTH `**Project**:` AND `**Board**:` fields
- User story IDs: `US-FE-001`, `US-BE-001` (with project prefix)
- AC-IDs: `AC-FE-US1-01`, `AC-BE-US1-01` (with project prefix)

**Example 2-level spec.md:**
```markdown
### US-FE-001: Create Login Form
**Project**: acme-corp
**Board**: frontend-team

**As a** user, I want a login form...

**Acceptance Criteria**:
- [ ] **AC-FE-US1-01**: Login form displays email/password fields
```

**Key Rules for spec.md (ADR-0140: v0.35.0+):**
1. **`project:` field REMOVED from YAML frontmatter** - now resolved from per-US fields
2. **`board:` field REMOVED from YAML frontmatter** (2-level) - now in per-US fields
3. **Each User Story MUST have `**Project**:` field** - source of truth for project
4. **Each User Story (2-level ONLY) MUST have `**Board**:` field** - source of truth for board

**⚠️ VALIDATION RULES:**
```
✅ 1-level: **Project**: required, NO **Board**:
✅ 2-level: **Project**: AND **Board**: both required
❌ FORBIDDEN: **Board**: on 1-level structure → hook will BLOCK
❌ FORBIDDEN: Missing **Board**: on 2-level → sync will fail
❌ FORBIDDEN: Unresolved placeholders like {{PROJECT_ID}}
```

### STEP 6: Create plan.md Template (OPTIONAL)

Create `.specweave/increments/0021-feature-name/plan.md`:

**Template File**: `templates/plan.md`

Replace `{{FEATURE_TITLE}}` placeholder. plan.md is OPTIONAL - create only for complex features with architecture decisions.

### STEP 7: Create tasks.md Template

Create `.specweave/increments/0021-feature-name/tasks.md`:

**⚠️ IMPORTANT: Use the correct template based on STEP 0A testMode detection!**

#### 7-TDD: TDD Mode Template (testMode: "TDD") - v1.0.111+

**Template File**: `templates/tasks-tdd-single-project.md`

Use this when `$TASK_TEMPLATE = "tasks-tdd-single-project.md"` (set in STEP 0A).

This template generates tasks in RED-GREEN-REFACTOR triplets:
- T-001 [RED]: Write failing test
- T-002 [GREEN]: Implement to pass test (depends on T-001)
- T-003 [REFACTOR]: Improve code quality (depends on T-002)

**Dependency markers are CRITICAL** - they enable TDD enforcement hooks.

#### 7A: Single-Project Template (Standard)

**Template File**: `templates/tasks-single-project.md`

Use this when `testMode != "TDD"` (default for most user projects).
Replace `{{FEATURE_TITLE}}` placeholder.

#### 7B: Multi-Project Template (umbrella.enabled: true) - USE THIS!

**Template File**: `templates/tasks-multi-project.md`

Replace placeholders: `{{FEATURE_TITLE}}`, `{{PROJECT_FE_ID}}`, `{{PROJECT_BE_ID}}`, `{{PROJECT_SHARED_ID}}`

**Key Rules for Multi-Project tasks.md:**
1. **Tasks MUST reference project-scoped user stories**: `US-FE-001`, `US-BE-001`
2. **Tasks MUST reference project-scoped ACs**: `AC-FE-US1-01`, `AC-BE-US1-01`
3. **Group tasks by project/phase** (Shared first, then BE, then FE)
4. **Test file paths MUST include project folder**: `sw-app-be/tests/`, `sw-app-fe/tests/`
5. **Dependencies between projects should be explicit**

### STEP 8: Guide User to Complete Planning

**Output this guidance to user**:

```
✅ Increment structure created: .specweave/increments/0021-feature-name/

📋 Basic templates created:
   • spec.md (user stories, acceptance criteria)
   • plan.md (technical design, architecture)
   • tasks.md (implementation steps with test plans)
   • metadata.json (increment metadata)

🚀 To complete planning, run these commands in sequence:

1. Complete product specification:
   Tell Claude: "Complete the spec for increment 0021-feature-name"
   (PM expertise will activate automatically in main conversation)

2. Create technical architecture:
   Tell Claude: "Design architecture for increment 0021-feature-name"
   (Architect will create detailed design in main conversation)

3. Generate implementation tasks:
   Tell Claude: "Create tasks for increment 0021-feature-name"
   (Test-aware planner will generate tasks with embedded tests)

⚠️  These commands run in MAIN conversation (NOT nested agents) to prevent crashes!
```

**DO NOT invoke Task() tool to spawn agents from this skill!**

### STEP 9: Trigger Living Docs & External Tool Sync (v0.32.2+)

**🔄 CRITICAL: After increment files are created, trigger sync to living docs AND external tools!**

This step uses the existing sync infrastructure to:
1. Create living docs (FS-XXX folder with FEATURE.md and us-*.md files)
2. Check permissions (`canUpsertInternalItems`) from `.specweave/config.json`
3. Sync to external tools (GitHub/JIRA/ADO) if configured and permitted

**Run the sync-specs command:**

```bash
/sw:sync-specs {increment-id}
```

**Expected output:**

```
🔄 Syncing increment to living docs...
✅ Living docs synced: FS-021
   Created: 4 files (FEATURE.md, us-001.md, us-002.md, us-003.md)

📡 Syncing to external tools: github
   📋 Permissions: upsert=true, update=true, status=true
   ✅ Synced to GitHub: 0 updated, 3 created
```

**Permission handling (v0.32.2+):**

If `canUpsertInternalItems: false` in config:
```
⚠️ Skipping external sync - canUpsertInternalItems is disabled
💡 Enable in .specweave/config.json: sync.settings.canUpsertInternalItems: true
```

**Error handling:**

External tool sync failures are NON-BLOCKING:
```
⚠️ External sync failed: Rate limit exceeded
💡 Run /sw:sync-specs {increment-id} to retry
```

**Output after sync:**

```
✅ Increment created and synced!

Next steps:
1. Review the increment plan and docs
2. Start implementation: /sw:do {increment-id}
3. Monitor status: /sw:status {increment-id}
```

---

## Model Selection for Tasks

When creating tasks, assign optimal models:

**⚡ Haiku** (fast, cheap):
- Clear instructions with specific file paths
- Detailed acceptance criteria (3+ points)
- Simple CRUD, configuration, setup
- Mechanical work with defined approach

**💎 Opus** (best quality, default):
- Architecture decisions
- Multiple valid approaches
- Integration between components
- Complex business logic
- Error handling strategies
- Critical system architecture
- Security-critical decisions
- Performance-critical algorithms
- Novel problem-solving

**🧠 Sonnet** (legacy, rarely needed):
- Use only for backwards compatibility
- Prefer Opus or Haiku instead

---

## TDD Task Generation (v1.0.105+)

**When `testMode: "TDD"` is set in metadata.json, tasks MUST follow RED-GREEN-REFACTOR triplet pattern!**

### TDD Task Structure

For each feature, generate tasks in triplets:

```markdown
### T-001: [RED] Write failing test for user authentication
**User Story**: US-001
**Satisfies ACs**: AC-US1-01
**Status**: [ ] pending
**Phase**: RED
**Model**: 💎 opus

**Test**: Given [invalid credentials] → When [login attempted] → Then [authentication fails]

**Guidance**:
- Write test BEFORE implementation
- Test MUST fail initially (no production code yet)
- Focus on behavior, not implementation details

---

### T-002: [GREEN] Implement user authentication
**User Story**: US-001
**Satisfies ACs**: AC-US1-01
**Status**: [ ] pending
**Phase**: GREEN
**Model**: 💎 opus
**Depends On**: T-001

**Test**: Make T-001 tests pass with minimal code

**Guidance**:
- Write MINIMAL code to make tests pass
- Don't over-engineer or optimize yet
- Keep it simple and working

---

### T-003: [REFACTOR] Improve authentication code quality
**User Story**: US-001
**Satisfies ACs**: AC-US1-01
**Status**: [ ] pending
**Phase**: REFACTOR
**Model**: 💎 opus
**Depends On**: T-002

**Test**: All tests from T-001 must still pass after refactoring

**Guidance**:
- Clean up code without changing behavior
- Extract helpers, improve naming
- Tests MUST stay green throughout
```

### TDD Phase Markers

**CRITICAL**: Use phase markers in task titles:

| Phase | Marker | Purpose |
|-------|--------|---------|
| RED | `[RED]` | Write failing test first |
| GREEN | `[GREEN]` | Make test pass with minimal code |
| REFACTOR | `[REFACTOR]` | Improve code, keep tests green |

### TDD Enforcement Hook

When tasks.md is edited, the `tdd-enforcement-guard.sh` hook:
1. Detects if `testMode: "TDD"` in metadata.json
2. Checks task completion order
3. **WARNS** (non-blocking) if:
   - GREEN task completed before RED task
   - REFACTOR task completed before GREEN task

**Example warning:**
```
⚠️  TDD DISCIPLINE WARNING
   Your increment is configured for TDD mode (testMode: TDD)

   Potential violations detected:
   • T-002 (GREEN) completed but T-001 (RED) not found or not completed

   💡 TDD Best Practice: RED → GREEN → REFACTOR
      1. 🔴 Write failing test FIRST
      2. 🟢 Make test pass with minimal code
      3. 🔵 Refactor while keeping tests green
```

### Coverage Validation

During `/sw:done`, coverage validation checks:
1. If `coverageTarget > 0` and `testMode != "none"`
2. Searches for coverage data (Istanbul, c8, Jest, lcov, Cobertura)
3. **WARNS** if coverage below target (non-blocking)

Supported coverage file locations:
- `coverage/coverage-summary.json` (Istanbul)
- `.c8/coverage-summary.json` (c8)
- `coverage/lcov.info` (lcov)
- `coverage/cobertura-coverage.xml` (Cobertura)

---

## Validation Checklist

Before marking increment planning complete, verify:

**Increment Structure**:
- [ ] Directory exists: `.specweave/increments/####-name/`
- [ ] spec.md has valid YAML frontmatter
- [ ] plan.md has technical design
- [ ] tasks.md has embedded test plans (NO separate tests.md)
- [ ] metadata.json exists and is valid

**spec.md Content**:
- [ ] User stories with AC-IDs (AC-US1-01, etc.)
- [ ] Functional requirements
- [ ] Success criteria (measurable)
- [ ] Out of scope defined
- [ ] Dependencies identified

**plan.md Content**:
- [ ] Components identified
- [ ] Data model defined
- [ ] API contracts specified
- [ ] Technology choices explained
- [ ] Architecture decisions documented

**tasks.md Content**:
- [ ] All tasks have embedded test plans
- [ ] Test cases in BDD format (Given/When/Then)
- [ ] All AC-IDs from spec covered by tasks
- [ ] Model hints assigned (⚡🧠💎)
- [ ] Dependencies explicitly stated
- [ ] **If TDD mode**: Tasks follow RED-GREEN-REFACTOR triplets
- [ ] **If TDD mode**: Phase markers used ([RED], [GREEN], [REFACTOR])

**metadata.json Content**:
- [ ] Valid JSON syntax
- [ ] All required fields present
- [ ] Status is "planned"
- [ ] Type matches increment purpose
- [ ] Timestamps in ISO-8601 format

---

## Helper Scripts

Located in `plugins/specweave/skills/increment-planner/scripts/`:

**Get next increment number**:
```bash
node plugins/specweave/skills/increment-planner/scripts/feature-utils.js next
```

**Check for duplicates**:
```bash
node plugins/specweave/skills/increment-planner/scripts/feature-utils.js check-increment 0021
```

**Generate short name from description**:
```bash
node plugins/specweave/skills/increment-planner/scripts/generate-short-name.js "Add user authentication"
# Returns: "user-authentication"
```

---

## Common Patterns

### Pattern 1: Simple Feature

**User request**: "Add user authentication"

**Process**:
1. Get next number: `0015`
2. Generate short name: `user-authentication`
3. Create directory: `.specweave/increments/0015-user-authentication/`
4. Create **metadata.json FIRST** (required before spec.md)
5. Create spec.md (now allowed - metadata.json exists)
6. Create tasks.md (plan.md optional for simple features)
7. Guide user to complete in main conversation

### Pattern 2: Critical Hotfix

**User request**: "Fix critical security vulnerability CVE-2024-1234"

**Process**:
1. Get next number: `0016`
2. Short name: `security-fix-cve-2024-1234`
3. Type: `hotfix` (in metadata.json)
4. Priority: `P1`
5. Create templates with urgency markers
6. Guide user to complete quickly

### Pattern 3: Bug Investigation

**User request**: "Investigate memory leak in production API"

**Process**:
1. Get next number: `0017`
2. Short name: `memory-leak-investigation`
3. Type: `bug` (in metadata.json)
4. spec.md focuses on: What's broken? Expected vs actual? Impact?
5. plan.md focuses on: Investigation approach, tools, hypothesis
6. tasks.md focuses on: Investigation steps, fix implementation, verification

---

## Troubleshooting

**Issue**: spec.md Write BLOCKED by guard
**Solution**: Create metadata.json FIRST! The `metadata-json-guard.sh` hook blocks spec.md creation until metadata.json exists. Always follow the order: directory → metadata.json → spec.md → tasks.md

**Issue**: Feature number conflict
**Solution**: Always run duplicate check before creating increment

**Issue**: metadata.json missing after creation
**Solution**: Verify Write tool succeeded, check file exists with Read tool

**Issue**: Claude Code crashes during planning
**Solution**: This skill creates templates only - completion happens in main conversation (NOT via nested agent spawning)

**Issue**: User stories don't have AC-IDs
**Solution**: Ensure AC-IDs follow format: `AC-US{number}-{criteria}` (e.g., `AC-US1-01`)

**Issue**: Tasks missing test plans
**Solution**: Each testable task MUST have Test Plan section with BDD format (Given/When/Then)

---

## Integration with External Tools

**GitHub Issues**: After increment creation, optionally sync to GitHub:
```bash
/sw-github:create-issue 0021
```

**Jira Epics**: Sync to Jira:
```bash
/sw-jira:sync 0021
```

**Azure DevOps**: Sync to ADO work items:
```bash
/sw-ado:create-workitem 0021
```

---

## Best Practices

**✅ DO**:
- Always create metadata.json (MANDATORY)
- Always create spec.md and tasks.md (MANDATORY)
- Create plan.md only for complex features with architecture decisions
- Use descriptive increment names
- Include AC-IDs in all acceptance criteria
- Embed tests in tasks.md (NO separate tests.md)
- Guide user to complete in main conversation
- Check for duplicates before creating

**❌ DON'T**:
- Use bare numbers (0001) without description
- Spawn agents from this skill (causes crashes)
- Skip metadata.json creation
- Create plan.md for bug fixes, simple migrations, or hotfixes
- Create separate tests.md (deprecated v0.7.0+)
- Reference SpecWeave internal docs/ADRs (users won't have them)
- Over-plan in skill (keep templates simple)

---

**This skill is self-contained and works in ANY user project after `specweave init`.**
