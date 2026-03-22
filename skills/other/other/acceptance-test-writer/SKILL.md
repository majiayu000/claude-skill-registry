---
name: acceptance-test-writer
description: >
  This skill should be used when the user asks to "generate acceptance tests",
  "create acceptance criteria tests", "write E2E test scripts from PRD",
  "set up acceptance testing for PRD-XXX", "convert PRD to testable criteria",
  or when starting implementation of a new PRD and acceptance tests don't exist.
  Generates executable YAML test scripts from PRD documents.
title: "Acceptance Test Writer"
status: active
---

# Acceptance Test Writer

Generate executable YAML acceptance test scripts from PRD documents, enabling automated validation that implementations meet business requirements.

## Purpose

Transform PRD acceptance criteria into structured, executable test definitions that:
- Define clear PASS/FAIL conditions linked to PRD requirements
- Specify exact validation steps (browser actions, API calls)
- Capture evidence requirements (screenshots, response bodies)
- Enable the `acceptance-test-runner` skill to validate implementations

## When to Use

Invoke this skill:
- After finalizing a PRD document
- Before starting implementation of a new feature
- When acceptance tests don't exist for a PRD (`acceptance-tests/PRD-XXX/` missing)

## Service Prerequisites (MANDATORY Before Test Execution)

Before writing or executing ANY test scenarios, verify the full service stack is running
on the **feature branch**. Test results from the default branch are not valid.

### Required Stack

| Service | How to Start | Verify |
|---------|-------------|--------|
| Backend API server | Docker container updated to feature branch, OR `uvicorn main:app --reload` | `curl http://localhost:8000/health` → 200 |
| Database | Local PostgreSQL with **all migrations applied** for the feature branch | `psql $DATABASE_URL -c "\dt"` lists expected tables |
| Frontend | `npm run dev` from the feature branch checkout | Browser opens at `http://localhost:3000` |

### Migration Check (Critical)

Before any DB-layer test step, confirm feature branch migrations are applied:

```bash
# Check tables exist (adapt to actual migration contents)
psql $DATABASE_URL -c "\dt" | grep -E "check_types|background_check_sequence|background_tasks"

# If tables missing — apply migrations:
# alembic upgrade head   (or project-specific migration command)
```

**A missing migration is a FAIL, not a SKIP.** If the tables don't exist, the test fails at the DB layer even if unit tests pass.

### Browser Test Tool: Claude in Chrome (NOT Jest or Playwright)

For all `@browser` / `@claude-in-chrome` steps, use **Claude in Chrome** (`mcp__claude-in-chrome__*`):
- `mcp__claude-in-chrome__navigate` — navigate to a URL
- `mcp__claude-in-chrome__find` — find elements on the page
- `mcp__claude-in-chrome__form_input` — fill forms
- `mcp__claude-in-chrome__javascript_tool` — execute JS assertions
- `mcp__claude-in-chrome__get_page_text` — read page content
- `mcp__claude-in-chrome__read_page` — get full DOM state

Jest and Playwright specs that already exist are supplementary and may be run, but they do NOT
substitute for Claude in Chrome browser validation. Claude in Chrome runs against the **live**
`npm run dev` frontend — it cannot run if the frontend is not started.

In Gherkin scenarios, annotate browser steps like this:
```gherkin
# TOOL: Claude in Chrome
When Claude in Chrome navigates to http://localhost:3000/some-page
And Claude in Chrome clicks the "Submit" button
```

### Pre-Execution Checklist

Before running any scenarios:
- [ ] Feature branch checked out in impl repo
- [ ] Docker container rebuilt/updated to feature branch (or server started directly)
- [ ] Database migrations applied (`alembic upgrade head` or equivalent)
- [ ] Feature branch tables exist in local PostgreSQL
- [ ] Frontend running: `npm run dev` accessible at `http://localhost:3000`
- [ ] Backend running: `GET /health` returns 200
- [ ] Auth tokens available for test accounts

## Input Requirements

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--prd` | **Auto-detected** | PRD identifier - extracted from YAML frontmatter if present |
| `--source` | Yes | Path to PRD markdown file |

**PRD ID Detection Priority:**
1. **YAML frontmatter** (preferred) - Look for `prd_id:` in the source document
2. **`--prd` argument** - Explicit override if frontmatter missing
3. **Error** - If neither is found, fail with clear message

Example invocations:
```bash
# Auto-detect from frontmatter (PREFERRED)
Skill("acceptance-test-writer", args="--source=.taskmaster/docs/PRD-AUTH-001-auth-system.md")

# Explicit override (when frontmatter missing or for legacy PRDs)
Skill("acceptance-test-writer", args="--prd=PRD-AUTH-001 --source=.taskmaster/docs/PRD-AUTH-001-auth-system.md")
```

### PRD Frontmatter Format

The PRD source document should have YAML frontmatter with `prd_id`:

```yaml
prd_id: PRD-AUTH-001
title: "User Authentication System"
product: "AgenCheck"
version: "1.0"
status: active
created: "2026-01-15"
author: "Product Team"
```

**Parsing Logic:**
1. Read source file
2. Look for YAML block (between triple backticks with `yaml` or fenced with `---`)
3. Extract `prd_id` field
4. If `--prd` argument provided, use it as override
5. If no `prd_id` found and no `--prd` argument, fail with:
   ```
   ERROR: No PRD ID found. Either:
   - Add prd_id to document frontmatter, or
   - Provide --prd=PRD-XXX argument
   ```

## Output Structure

```
acceptance-tests/
└── PRD-{identifier}/
    ├── manifest.yaml           # PRD metadata, feature list
    ├── AC-{criterion-1}.yaml   # One file per acceptance criterion
    ├── AC-{criterion-2}.yaml
    └── ...
```

## Workflow

### Step 0: Extract PRD ID (MANDATORY)

**Before anything else, determine the canonical PRD ID.**

```python
# Pseudocode for PRD ID extraction
def extract_prd_id(source_path, prd_override=None):
    content = read_file(source_path)

    # Look for YAML frontmatter (```yaml ... ``` or --- ... ---)
    yaml_match = regex_search(r'```yaml\n(.*?)\n```', content, DOTALL)
    if not yaml_match:
        yaml_match = regex_search(r'^---\n(.*?)\n---', content, DOTALL)

    if yaml_match:
        frontmatter = parse_yaml(yaml_match.group(1))
        prd_id = frontmatter.get('prd_id')
        if prd_id:
            return prd_override or prd_id  # Override wins if provided

    if prd_override:
        return prd_override

    raise Error("No PRD ID found. Add prd_id to frontmatter or provide --prd argument")
```

**Output**: Canonical `prd_id` string (e.g., `PRD-AUTH-001`)

### Step 1: Read and Parse PRD

Read the source PRD document. Extract:
- PRD title and identifier (use `prd_id` from Step 0)
- Features/epics with descriptions
- Acceptance criteria (look for sections titled "Acceptance Criteria", "Definition of Done", "Success Criteria", or numbered requirements)
- User flows and scenarios
- API contracts (if specified)
- UI requirements (if specified)

### Step 2: Identify Acceptance Criteria

For each feature, identify testable acceptance criteria. Common patterns in PRDs:

| PRD Pattern | Maps To |
|-------------|---------|
| "User can..." | Browser test with user flow |
| "System shall..." | API or integration test |
| "When X, then Y" | Conditional behavior test |
| "API returns..." | API response validation |
| "Page displays..." | UI element assertion |

### Step 3: Determine Validation Type

For each criterion, classify:

| Type | When to Use | Tools |
|------|-------------|-------|
| `browser` | UI interactions, visual verification | chrome-devtools MCP |
| `api` | Backend endpoints, data validation | curl, httpx |
| `hybrid` | UI triggers API, verify both | Both |

### Step 4: Generate Test Steps

Convert acceptance criteria into executable steps. Map natural language to actions:

| PRD Language | Action | Example |
|--------------|--------|---------|
| "navigate to", "go to" | `navigate` | `target: "/login"` |
| "enter", "fill in", "type" | `fill` | `selector: "[data-testid='email']"` |
| "click", "press", "submit" | `click` | `selector: "[data-testid='submit']"` |
| "should see", "displays" | `assert_visible` | `selector: ".success-message"` |
| "redirected to" | `assert_url` | `pattern: "/dashboard"` |
| "returns", "responds with" | `assert_status` | `expected: 200` |
| "contains", "shows" | `assert_text` | `contains: "Welcome"` |

### Step 5: Define Evidence Requirements

Each criterion should specify evidence to capture:
- **Browser tests**: Screenshots at key steps and on completion
- **API tests**: Full response capture (headers + body)
- **Hybrid tests**: Both screenshots and API responses

### Step 6: Create Manifest

Generate `manifest.yaml` linking all criteria to features and PRD source.

### Step 7: Write YAML Files

Create all files in `acceptance-tests/PRD-XXX/`:
1. Write `manifest.yaml` first
2. Write one `AC-{name}.yaml` per criterion
3. Verify all files are valid YAML

## Guardian Mode (--mode=guardian)

Generates per-epic Gherkin acceptance test scenarios with confidence scoring guides, for use by
the cobuilder-guardian skill. Output goes in `acceptance-tests/PRD-{ID}/` (same as standard mode but
Gherkin `.feature` format instead of YAML).

### When to Use
- Invoked by cobuilder-guardian in Phase 1 to create the blind acceptance rubric
- Replaces the guardian's manual Steps 1-4 (read PRD, extract features, write Gherkin, create manifest)

### Invocation
```
Skill("acceptance-test-writer", args="--source=/path/to/impl-repo/.taskmaster/docs/SD-{ID}.md --mode=guardian")
```

### Workflow

### Step G0: Verify Service Prerequisites

Before generating scenarios, note the service requirements in the manifest so the executor
knows exactly what must be running. During test execution (Phase 4), verify these
prerequisites before scoring any scenario.

The executor (tdd-test-engineer or guardian Phase 4) MUST confirm before running scenarios:
- [ ] Feature branch is deployed/running (not main/default branch)
- [ ] Migrations applied — expected tables exist in local PostgreSQL
- [ ] Frontend running on `http://localhost:3000` via `npm run dev` (feature branch)
- [ ] Backend running on `http://localhost:8000`

A missing service or unapplied migration is a **FAIL**, not a SKIP. Surface the gap explicitly.

**Step G1: Read PRD and Extract Weighted Features**
Read the PRD. Identify every testable feature. Assign weights based on business criticality:

| Weight | Meaning | Example |
|--------|---------|---------|
| 0.30+ | Core feature — initiative fails without it | Pipeline execution engine |
| 0.15-0.29 | Important feature — degrades experience | Error handling, retry logic |
| 0.05-0.14 | Supporting feature — nice to have | Logging, configuration |
| < 0.05 | Polish, documentation | README, inline comments |

Weights across all features MUST sum to 1.0.

**Step G1b: Classify Validation Method Per Feature**

For each feature extracted in G1, classify the `validation_method` based on PRD language signals:

| PRD Signal | Maps To |
|------------|---------|
| "page renders", "UI shows", "user clicks", "frontend", "navigate to", "dashboard displays", "form submits", "button", "modal", "toast" | `browser-required` |
| "API returns", "endpoint responds", "HTTP status", "POST /api", "GET /api", "webhook fires", "REST" | `api-required` |
| "database schema", "migration", "code structure", "config file", "import graph", "type definitions" | `code-analysis` |
| Mixed signals or unclear | `hybrid` |

**Classification rules:**
1. If ANY scenario in the feature requires browser interaction, the entire feature is `browser-required`
2. If the feature is purely backend/API but requires live requests (not just reading router code), it is `api-required`
3. Only use `code-analysis` when the feature can be fully validated by reading source files
4. When in doubt, default to `hybrid`

**Step G2: Write Gherkin Scenarios with Confidence Scoring Guides**
For each feature, write one or more Gherkin scenarios. Each scenario MUST include:
- `Given` / `When` / `Then` clauses
- A confidence scoring guide (what 0.0 vs 0.5 vs 1.0 looks like for that scenario)
- Evidence to check (specific files, functions, tests to examine)
- Red flags (indicators of incomplete or falsely-claimed implementation)

Example scenario format:
```gherkin
@feature-F001 @weight-0.30
Feature: Pipeline Execution Engine

  Scenario: Pipeline executes all stages in sequence
    Given a valid pipeline configuration exists
    When the pipeline runner is invoked
    Then stages are executed in topological order
    And each stage produces expected output artifacts

    # Confidence scoring guide:
    # 1.0 — All 4 stages run, artifacts verified in tests
    # 0.5 — Stages run but no artifact verification
    # 0.0 — Pipeline fails or only 1-2 stages execute

    # Evidence to check:
    # - pipeline_runner.py execute() method
    # - tests/test_pipeline_runner.py stage_sequence tests
    # - .beads/ notes for any skipped stages

    # Red flags:
    # - TODO comments in execute()
    # - Tests that mock stage execution (hollow tests)
    # - Missing artifact assertions
```

**Browser step annotation**: For `@browser` or `@claude-in-chrome` steps, prefix each step with
`# TOOL: Claude in Chrome` and write steps as "Claude in Chrome navigates to...", "Claude in Chrome
clicks...", etc. This makes the tooling explicit. Do NOT write browser steps as abstract "the user
does X" — name the tool.

**Step G3: Generate Manifest**
Create `manifest.yaml` with:
- PRD metadata (id, title, source)
- Feature list with weights and `validation_method` (from Step G1b)
- Decision thresholds (default: accept=0.60, investigate=0.40)
- Links to each scenario file

Each feature entry in the manifest MUST include the `validation_method` field:
```yaml
features:
  - name: "Epic A4 — Frontend UI"
    weight: 0.25
    validation_method: browser-required   # From Step G1b classification
    scenarios:
      - "frontend_rendering"
      - "user_interaction"
```

**Step G4: Write Files**
Output to `acceptance-tests/PRD-{ID}/`:
- `manifest.yaml` — metadata, weights, thresholds
- `scenarios.feature` — all Gherkin scenarios in one file (or one per feature)

### Guardian Mode Output Checklist
- [ ] All PRD features represented with weights summing to 1.0
- [ ] Each scenario has a confidence scoring guide
- [ ] Evidence references are specific (file names, function names, test names)
- [ ] Red flags call out hollow test patterns explicitly
- [ ] manifest.yaml is valid YAML with correct threshold structure

## Journey Mode (--mode=journey)

Generates Gherkin journey scenarios from the PRD's **Goals / Business Objectives** section
(not the feature list). Output goes in `acceptance-tests/PRD-{ID}/journeys/`.

### When to Use
- After generating per-epic tests (run `--mode=guardian` first)
- Invoked by cobuilder-guardian in Phase 1 to create blind journey tests
- Invoked by cobuilder's post-completion smoke gate

### Invocation
```
Skill("acceptance-test-writer", args="--source=.taskmaster/docs/PRD-{ID}.md --mode=journey")
```

### Workflow

**Step J1: Extract Business Objectives**
Read the PRD's Goals, Success Criteria, or "Business Objectives" sections (not the feature list).
Each distinct objective maps to one journey scenario J1, J2, J3...

Examples of business objectives in PRDs:
  - "Employer contact submission triggers validation workflow"
  - "User signs up via OAuth and lands on correct dashboard"
  - "Failed check triggers retry sequence in Prefect"

**Step J2: Identify the Causal Chain**
For each objective, trace which layers are crossed:
  - @browser — scenario starts with a user action in the UI
  - @api    — scenario involves direct API assertion
  - @db     — scenario requires checking DB state
  - @async  — scenario has downstream async effects (Prefect, Celery, queue job)

A journey scenario typically crosses 3-5 layers. If it only crosses one layer, it belongs in
per-epic Gherkin tests, not a journey.

**Layer execution rules for journey runners:**
- `@browser` / `@claude-in-chrome` steps → **Claude in Chrome** (`mcp__claude-in-chrome__*`) against `http://localhost:3000`
  - Frontend MUST be running via `npm run dev` on the feature branch
  - Annotate each step with `# TOOL: Claude in Chrome` prefix and write as "Claude in Chrome navigates/clicks/fills..."
  - Do NOT use Jest or Playwright as a substitute for these steps
- `@api` steps → direct HTTP calls (`curl` or `httpx`) against `http://localhost:8000` — annotate `# TOOL: curl`
- `@db` steps → `psql $DATABASE_URL` queries directly — annotate `# TOOL: direct psql query`
- `@async` + "eventually" steps → poll with `sleep` + repeated query, per `runner_config.yaml` intervals
- `@smoke` steps → can run without browser (API + DB only)

**Step J3: Write Gherkin Scenarios**
Naming: `J{N}-{slug}.feature`, e.g. `J1-contact-validation-chain.feature`
Tags: `@journey @prd-{ID} @J{N}` plus any of `@browser @async @db @api @smoke`

Standard journey Gherkin pattern:
```gherkin
@journey @prd-UEA-001 @J1 @browser @async @db
Scenario J1: Employer contact submission triggers full validation chain
  # Browser layer
  Given I am logged in as an employer
  When I submit a university contact via the UI (or API)
  # API layer
  Then the API returns HTTP 201
  And the response contains a contact_id
  # DB layer (immediate)
  And the contacts table has a row with that contact_id and status="queued"
  # Async layer (Prefect / downstream)
  And eventually a Prefect flow run for that contact_id reaches state "Completed"
  # Final business outcome
  And the contacts table row has status="validated"
  And the employer dashboard shows the contact as "Verified"
```

"Eventually" steps imply polling: use `runner_config.yaml` for intervals/timeout.

### Canonical Work History /verify E2E Pattern

For projects with a `/verify` endpoint, the primary E2E journey MUST include submitting
a real check request and verifying the full downstream chain:

```gherkin
@journey @prd-{ID} @J1 @api @db @async @smoke
Scenario J1: Work history check submitted via /verify triggers full verification chain
  # Submit the check (TOOL: curl or httpx)
  Given I have a valid API key for the test employer account
  When I POST to /api/v1/verify with a valid work history payload
  Then the API returns HTTP 200 or 202
  And the response body contains a check_id (or task_id)
  # Immediate DB state (TOOL: direct psql query)
  And the background_tasks table has a row with that check_id and status in ("pending", "queued")
  # Async processing (TOOL: poll psql every 5s, max 120s)
  And eventually the background_tasks row has status="completed" or "verified"
  # Business outcome (TOOL: curl GET)
  And GET /api/v1/verify/{check_id} returns 200 with structured employment data
```

This journey is `@smoke` — it runs without the frontend. Run it first: if it fails, browser journeys will also fail.

**Step J4: Write runner_config.yaml**
```yaml
services:
  frontend_url: "http://localhost:3000"
  api_url: "http://localhost:8000"
  db_dsn: "${DATABASE_URL}"
  prefect_api: "http://localhost:4200/api"
polling:
  interval_seconds: 5
  max_wait_seconds: 120
auth:
  test_employer_email: "${TEST_EMPLOYER_EMAIL}"
  test_employer_password: "${TEST_EMPLOYER_PASSWORD}"
```

**Step J5: Write the files**
```
acceptance-tests/PRD-{ID}/journeys/
  J1-{slug}.feature         # one per business objective
  J2-{slug}.feature
  runner_config.yaml
```

### Journey Scenario Principles
- One scenario per business objective (not per epic or feature)
- Steps MUST cross at least 2 system layers (browser+API, API+DB, DB+queue, etc.)
- Final step asserts the *business outcome*, not just data existence:
  - BAD:  "And a row exists in the contacts table"
  - GOOD: "And the contacts table row has status='validated' AND verified_at IS NOT NULL"
- Use "eventually" for async steps — signals the runner to poll
- Keep scenarios short (5-8 steps max) — if longer, split into two journeys
- @smoke tag = can run without services up (structural checks only)

## YAML Schemas

### Manifest Schema

See `references/schemas.md` for complete manifest.yaml schema.

Key fields:
```yaml
prd_id: string          # PRD identifier
prd_title: string       # Human-readable title
prd_source: string      # Path to source PRD
generated: ISO8601      # Generation timestamp
features: []            # List of features with criteria
task_mapping: {}        # Optional: feature to task IDs
```

### Acceptance Criterion Schema

See `references/schemas.md` for complete AC-*.yaml schema.

Key fields:
```yaml
id: string              # Unique criterion ID (e.g., AC-user-login)
feature: string         # Feature ID this belongs to
title: string           # One-line description
description: string     # Detailed description
prd_reference: string   # Section/requirement in PRD
validation_type: browser|api|hybrid
priority: critical|high|medium|low
preconditions: []       # What must be true before test
steps: []               # Executable test steps
expected_outcome: string
failure_indicators: []  # How to recognize failure
evidence: []            # What to capture
```

## Best Practices

### Selector Strategy

Prefer selectors in this order:
1. `[data-testid='...']` - Most stable, designed for testing
2. `[aria-label='...']` - Accessibility-friendly
3. `#id` - Unique but may change
4. `.class` - Least stable, avoid if possible

### Step Granularity

- One action per step (don't combine fill + click)
- Include `screenshot: true` at verification points
- Add `wait_for_navigation` after clicks that trigger page loads

### Preconditions

Be explicit about test data requirements:
- User accounts that must exist
- Database state required
- Services that must be running
- Environment variables needed

### Failure Indicators

Help the runner understand what failure looks like:
- Error messages that might appear
- URLs that indicate wrong navigation
- HTTP status codes that indicate problems

## Example Workflow

Given a PRD section:
```markdown
## 3.1 User Login

Users must be able to log in with their email and password.

**Acceptance Criteria:**
1. User can log in with valid credentials and see dashboard
2. Invalid credentials show error message
3. Locked accounts show "account locked" message
```

Generate:
1. `AC-user-login-valid.yaml` - Happy path login
2. `AC-user-login-invalid.yaml` - Error handling
3. `AC-user-login-locked.yaml` - Account lock handling

## Additional Resources

### Reference Files

- **`references/schemas.md`** - Complete YAML schemas for manifest and criteria
- **`references/action-catalog.md`** - All supported test actions with parameters

### Example Files

- **`examples/manifest.yaml`** - Sample manifest file
- **`examples/AC-browser-test.yaml`** - Browser validation example
- **`examples/AC-api-test.yaml`** - API validation example
- **`examples/AC-hybrid-test.yaml`** - Hybrid validation example

## Validation Checklist

Before completing, verify:
- [ ] All PRD acceptance criteria have corresponding AC-*.yaml files
- [ ] Manifest lists all features and their criteria
- [ ] Each criterion has valid `validation_type`
- [ ] All steps use supported actions (see `references/action-catalog.md`)
- [ ] Evidence requirements specified for each criterion
- [ ] Preconditions are explicit and achievable
- [ ] YAML files are syntactically valid
