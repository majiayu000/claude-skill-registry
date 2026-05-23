---
name: speckit-author
version: 5.0.0
description: |
  Creates SpecKit specifications (spec.md, plan.md) in feature/release/hotfix
  worktrees. Detailed implementation guidance.

  Use when: In worktree, need specifications, implementation planning

  Triggers: write spec, create plan, feature specification
---

# SpecKit Author

## Purpose

Creates detailed specifications and implementation plans for features,
releases, and hotfixes within worktree directories.

## When to Use

- Current directory: worktree (feature/release/hotfix)
- Phase: Specification (Phase 2)

## Document Templates

Templates are located in `templates/`:
- `spec.md.template` - Detailed technical specification (297 lines)
- `plan.md.template` - Task breakdown and implementation plan (367 lines)

## Interactive Callable Tool

SpecKit is now an **interactive callable tool** that runs as a Python script in feature worktrees.

### Invocation

**Command:**
```bash
python .claude/skills/speckit-author/scripts/create_specifications.py \
  <workflow_type> <slug> <gh_user> [--todo-file <path>]
```

**Arguments:**
- `workflow_type`: feature, release, or hotfix
- `slug`: Feature slug (e.g., my-feature)
- `gh_user`: GitHub username
- `--todo-file`: Optional path to TODO file (default: auto-detect)
- `--no-commit`: Skip git commit (for testing)

**Example:**
```bash
# In feature worktree
cd /Users/user/german_feature_my-feature

python .claude/skills/speckit-author/scripts/create_specifications.py \
  feature my-feature stharrold \
  --todo-file ../TODO_feature_20251024T143000Z_my-feature.md
```

### Interactive Session Flow

#### With BMAD Planning (Recommended)

**Session output:**
```
Working in worktree: /Users/user/german_feature_my-feature
Branch: feature/20251024T143000Z_my-feature
✓ Auto-detected TODO file: ../TODO_feature_20251024T143000Z_my-feature.md

======================================================================
SpecKit Interactive Specification Tool
======================================================================

✓ Detected BMAD planning context: ../planning/my-feature/

BMAD Summary:
  - Requirements: 15 functional requirements, 5 user stories
  - Architecture: Technology stack defined
  - Epics: 3 epics defined

Implementation Questions:
----------------------------------------------------------------------

Database migrations strategy?
  1) Alembic (recommended)
  2) Manual SQL migrations
  3) None needed
  [default: Alembic (recommended)]
> 1

Include end-to-end (E2E) tests? (Y/n) > n

Include performance/load tests? (Y/n) > n

Include security tests (OWASP checks)? (Y/n) > n

Task granularity preference?
  1) Small tasks (1-2 hours each)
  2) Medium tasks (half-day each)
  3) Large tasks (full-day each)
  [default: Small tasks (1-2 hours each)]
> 1

Follow epic priority order from epics.md? (Y/n) > Y

Any additional implementation notes or constraints? (optional)
> Use type hints throughout

======================================================================
Generating specifications...
======================================================================
✓ Created specs/my-feature/spec.md (1247 chars)
✓ Created specs/my-feature/plan.md (1583 chars)
✓ Created specs/my-feature/CLAUDE.md
✓ Created specs/my-feature/README.md
✓ Updated TODO file: ../TODO_feature_20251024T143000Z_my-feature.md
  Added 0 tasks across 0 categories

✓ Committed changes to branch

======================================================================
SpecKit Specifications Created Successfully!
======================================================================

Files created:
  - specs/my-feature/spec.md
  - specs/my-feature/plan.md
  - specs/my-feature/CLAUDE.md
  - specs/my-feature/README.md

Next steps:
  1. Review spec.md and plan.md
  2. Implement tasks from plan.md
  3. Update TODO task status as you complete each task
  4. Refer to ../planning/my-feature/ for BMAD context
```

**What happens:**
1. Script detects ../planning/my-feature/ directory
2. Reads requirements.md, architecture.md, epics.md
3. Displays BMAD summary
4. Asks 5-8 implementation-specific questions
5. Generates spec.md + plan.md aligned with BMAD
6. Creates compliant specs/<slug>/ directory structure
7. Updates TODO_*.md with tasks parsed from plan.md
8. Commits changes

**Generated spec.md includes:**
- Reference to BMAD planning documents
- Implementation context from Q&A responses
- Technology stack from architecture.md
- Functional requirements from requirements.md
- Detailed component specifications

**Generated plan.md includes:**
- Tasks organized by epics from epics.md
- Task IDs (impl_001, impl_002, test_001, etc.)
- Dependencies based on epic order
- Acceptance criteria
- Verification commands

#### Without BMAD Planning

**Session output:**
```
======================================================================
SpecKit Interactive Specification Tool
======================================================================

⚠ No BMAD planning found for 'my-feature'
I'll gather requirements through comprehensive Q&A.

Recommendation: Use BMAD planning for future features
======================================================================

What is the main purpose of this feature?
> Add vocabulary search functionality

Who are the primary users of this feature?
> German language learners

How will success be measured? (metrics, goals)
> Users can search vocabulary by German word, English translation, or POS

Technology Stack:

Web framework (if applicable)?
  1) FastAPI
  2) Flask
  3) Django
  4) None
  [default: None]
> 4

Database?
  1) SQLite (dev)
  2) PostgreSQL
  3) MySQL
  4) None
  [default: None]
> 1

Database migration strategy?
  1) Alembic
  2) Manual SQL
  3) None
  [default: Alembic]
> 1

Testing framework?
  1) pytest (recommended)
  2) unittest
  3) other
  [default: pytest (recommended)]
> 1

Performance target? (e.g., '<200ms response time', 'not critical')
> < 100ms query time

Security requirements? (e.g., 'authentication', 'encryption', 'none')
> none

Test coverage target? [80%]
> 85

Include E2E tests? (y/N) > n

Include performance tests? (y/N) > n

Task size preference?
  1) Small (1-2 hours)
  2) Medium (half-day)
  3) Large (full-day)
  [default: Small (1-2 hours)]
> 1

[... generates spec.md and plan.md ...]
```

**What happens:**
1. Script finds no planning context
2. Conducts comprehensive Q&A (10-15 questions)
3. Gathers requirements, tech stack, testing preferences
4. Generates spec.md + plan.md from scratch
5. Creates compliant specs/<slug>/ directory structure
6. Updates TODO_*.md with tasks
7. Commits changes
8. Recommends creating BMAD planning for next feature

## Script Architecture

### create_specifications.py

**Location:** `.claude/skills/speckit-author/scripts/create_specifications.py`

**Implements:**
1. **Context Detection**
   - Verifies running in worktree (not main repo)
   - Auto-detects or accepts TODO file path
   - Checks for BMAD planning in ../planning/<slug>/

2. **Interactive Q&A**
   - Adapts questions based on BMAD availability
   - With BMAD: 5-8 implementation-specific questions
   - Without BMAD: 10-15 comprehensive requirements questions

3. **Template Processing**
   - Loads spec.md.template and plan.md.template
   - Replaces placeholders ({{TITLE}}, {{SLUG}}, {{DATE}}, etc.)
   - Injects Q&A context as implementation notes

4. **Directory Creation**
   - Creates specs/<slug>/ with compliant structure
   - Generates CLAUDE.md and README.md
   - Creates ARCHIVED/ subdirectory

5. **TODO Update**
   - Parses task IDs from plan.md
   - Updates TODO_*.md YAML frontmatter
   - Groups tasks by category (impl, test, doc, etc.)

6. **Git Commit**
   - Stages specs/<slug>/ and TODO file
   - Creates descriptive commit message
   - References TODO file in commit

## Directory Structure

Specification documents are created in:

```
specs/
└── <feature-slug>/
    ├── spec.md           # Technical specification
    ├── plan.md          # Implementation plan
    ├── CLAUDE.md        # Context for this spec
    ├── README.md        # Human-readable overview
    └── ARCHIVED/        # Deprecated specs
```

### update_asbuilt.py

**Location:** `.claude/skills/speckit-author/scripts/update_asbuilt.py`

**Used in:** Phase 4 (Integration + Feedback) after PR merge

**Implements:**
1. **Read As-Built Specs**
   - Reads specs/<slug>/spec.md and plan.md
   - Reads TODO_*.md for effort/timeline data

2. **Compare with Planning**
   - Auto-detects deviations (technology changes)
   - Interactive Q&A for manual deviation identification

3. **Gather Metrics**
   - Epic completion (estimated vs actual effort)
   - Quality metrics (coverage, performance)
   - Lessons learned

4. **Update Planning Docs**
   - Appends "## As-Built Notes" to requirements.md
   - Appends "## As-Built Architecture" to architecture.md
   - Appends "## Epic Completion Status" to epics.md

5. **Git Commit**
   - Commits updated planning documents
   - Creates feedback loop for future planning

**Invocation:**
```bash
# From main repo on contrib branch after PR merge
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/my-feature specs/my-feature
```

## Integration with Workflow

The workflow-orchestrator calls SpecKit scripts during workflow phases.

### Phase 2: Create Specifications (Step 2.3)

**Workflow orchestrator code:**
```python
# In workflow orchestrator - Phase 2.3
if current_phase == 2 and current_step == '2.3':
    import subprocess

    # Call SpecKit interactive tool
    result = subprocess.run([
        'python',
        '.claude/skills/speckit-author/scripts/create_specifications.py',
        workflow_type,  # feature, release, hotfix
        slug,           # my-feature
        gh_user,        # stharrold
        '--todo-file', f'../TODO_{workflow_type}_{timestamp}_{slug}.md'
    ], check=True)

    # SpecKit handles:
    # - Interactive Q&A with user
    # - BMAD context detection
    # - spec.md and plan.md generation
    # - TODO_*.md update
    # - Git commit

    print("✓ SpecKit specifications created")
    print(f"  Next: Implement tasks from specs/{slug}/plan.md")
```

### Phase 4: Update As-Built (Step 4.4)

**After PR merge to contrib branch:**
```python
# In workflow orchestrator - Phase 4.4
if current_phase == 4 and current_step == '4.4':
    import subprocess

    # Call as-built update tool
    result = subprocess.run([
        'python',
        '.claude/skills/speckit-author/scripts/update_asbuilt.py',
        f'planning/{slug}',
        f'specs/{slug}'
    ], check=True)

    # update_asbuilt.py handles:
    # - Deviation analysis
    # - Interactive metrics gathering
    # - Planning document updates
    # - Git commit

    print("✓ BMAD planning updated with as-built details")
    print(f"  Feedback loop completed for {slug}")
```

## Template Placeholders

Both templates use these placeholders:
- `{{TITLE}}` - Feature name (title case)
- `{{WORKFLOW_TYPE}}` - feature, release, or hotfix
- `{{SLUG}}` - Feature slug (kebab-case)
- `{{DATE}}` - Creation date (YYYY-MM-DD)
- `{{GH_USER}}` - GitHub username

## Using BMAD Planning Context

When BMAD planning documents exist in `../planning/<feature>/`:

### SpecKit Should:

**1. Read planning context:**
```python
# Read BMAD planning docs from main repo
requirements = Path('../planning/<feature>/requirements.md').read_text()
architecture = Path('../planning/<feature>/architecture.md').read_text()
epics = Path('../planning/<feature>/epics.md').read_text()
```

**2. Extract key information:**
- **From requirements.md:**
  - Functional requirements (FR-001, FR-002...)
  - Non-functional requirements (performance, security, scalability)
  - User stories and acceptance criteria
  - Success criteria and constraints

- **From architecture.md:**
  - Technology stack and framework choices
  - Data models and database schema
  - API endpoint definitions
  - Container configuration
  - Security and error handling strategies

- **From epics.md:**
  - Epic breakdown (E-001, E-002...)
  - Epic priorities (P0, P1, P2)
  - Epic dependencies
  - Implementation timeline

**3. Generate spec.md informed by planning:**
```markdown
# spec.md sections should reference BMAD docs

## Functional Requirements
FR-001 from requirements.md: [Requirement description]
  - Acceptance Criteria (from requirements.md):
    - [ ] AC 1...
    - [ ] AC 2...

## Technology Stack
Stack defined in architecture.md:
  - Language: Python 3.11+
  - Framework: FastAPI (chosen in architecture.md)
  - Database: PostgreSQL (from architecture.md)

## Security Requirements
From architecture.md Section "Security Considerations":
  - Authentication: JWT tokens
  - Authorization: RBAC
  - Input validation: JSON schema
```

**4. Generate plan.md informed by epics:**
```markdown
# plan.md tasks organized by epic

## Epic E-001: Data Layer (from epics.md)
Priority: P0 (Foundation)
Dependencies: None

Tasks:
- [ ] impl_001: Create database schema (from architecture.md data models)
- [ ] impl_002: Implement ORM entities
- [ ] test_001: Unit tests for data layer

## Epic E-002: API Layer (from epics.md)
Priority: P0 (Core functionality)
Dependencies: E-001

Tasks:
- [ ] impl_003: Create API endpoints (from architecture.md)
- [ ] impl_004: Implement request validation
- [ ] test_002: API integration tests
```

### Interactive Prompts

**When planning exists:**
```
I found BMAD planning documents:
  ✓ planning/<feature>/requirements.md (15 functional requirements)
  ✓ planning/<feature>/architecture.md (Python/FastAPI stack, PostgreSQL)
  ✓ planning/<feature>/epics.md (3 epics: Data, API, Tests)

I'll use these as context to create detailed SpecKit specifications.

Based on the requirements, I see these priority P0 epics:
  - E-001: Data Layer (Foundation)
  - E-002: API Layer (Core functionality)

The architecture specifies:
  - Framework: FastAPI
  - Database: PostgreSQL with SQLAlchemy
  - Testing: pytest with ≥80% coverage

Would you like me to expand on any areas before generating specs? (Y/n)
```

**When no planning:**
```
No BMAD planning documents found.

I'll create specifications from scratch through interactive Q&A.

What is the main purpose of this feature?
> [User describes]

What technology stack should we use?
> [User specifies or accepts defaults]

Any specific performance or security requirements?
> [User answers]

Generating specifications...
```

## Best Practices

### When BMAD Planning Exists:

- **Use planning as foundation**: Reference `../planning/<feature>/requirements.md` sections
- **Be consistent**: Technology choices must match `architecture.md`
- **Epic-driven tasks**: Break down `plan.md` tasks by epic from `epics.md`
- **Acceptance criteria alignment**: `spec.md` AC must cover `requirements.md` success criteria
- **Traceability**: spec.md references FR-001, FR-002...; plan.md references E-001, E-002...
- **Justify deviations**: If deviating from architecture.md, document why

### When BMAD Planning Doesn't Exist:

- **Gather requirements interactively**: Ask user for purpose, users, success criteria
- **Document assumptions**: State technology choices and rationale
- **Start simple**: Can always add complexity later
- **Ask clarifying questions**: Better to clarify upfront than rework later

### Always:

- **Be specific**: Include exact file names, function signatures, data structures
- **Code examples**: Show actual implementation patterns
- **API contracts**: Define exact request/response formats
- **Test cases**: Specify what to test and expected outcomes
- **Dependencies**: List what must be done first (refer to epic dependencies)

## SpecKit → BMAD Feedback (As-Built Documentation)

After implementation completes and PR is merged to contrib branch, SpecKit outputs should update BMAD planning docs with as-built details.

### When to Update BMAD Planning

**Trigger:** Phase 4, after feature PR merged to contrib/<gh-user>

**Location:** Back in main repo on contrib branch

**Process:**
```bash
# After PR merge, back in main repo
cd /Users/user/Documents/GitHub/german
git checkout contrib/stharrold
git pull origin contrib/stharrold

# Run as-built documentation update
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/<feature>/ \
  specs/<feature>/
```

### What Gets Updated

**planning/<feature>/requirements.md:**
```markdown
## As-Built Notes

**Implementation Date:** 2025-10-23
**Final Implementation:** specs/<feature>/spec.md in feature worktree

### Deviations from Original Plan

**FR-001: Original Requirement**
- Planned: Use Redis for caching
- As-Built: Used in-memory caching (LRU cache)
- Reason: Redis not needed for current scale, simpler deployment

**FR-003: Original Requirement**
- Planned: Real-time WebSocket updates
- As-Built: Polling every 30 seconds
- Reason: Simpler implementation, meets performance requirements

### Lessons Learned

- Database connection pooling: Default settings were sufficient
- Testing: Achieved 87% coverage (exceeded 80% goal)
- Performance: Response times < 100ms (better than 200ms target)
```

**planning/<feature>/architecture.md:**
```markdown
## As-Built Architecture

**Implemented:** 2025-10-23
**Detailed Spec:** specs/<feature>/spec.md

### Technology Stack (Final)

Matches planned architecture with these changes:
- Database: PostgreSQL (as planned)
- Caching: ~~Redis~~ → Python LRU cache
- API Framework: FastAPI (as planned)

### Actual Data Models

Final database schema implemented in src/models/:
- [Link to actual code files]
- Schema migration: migrations/versions/abc123_initial.py

### API Endpoints (Implemented)

All planned endpoints implemented:
- POST /api/endpoint (spec.md line 89)
- GET /api/endpoint/{id} (spec.md line 144)
- Additional endpoint added: GET /api/endpoint/search (user request)

### Performance Metrics (Actual)

- Response time p95: 87ms (target: 200ms) ✓
- Throughput: 1200 req/s (target: 1000 req/s) ✓
- Test coverage: 87% (target: 80%) ✓
```

**planning/<feature>/epics.md:**
```markdown
## Epic Completion Status

### E-001: Data Layer (COMPLETED)
- Status: ✓ Completed 2025-10-23
- Actual effort: 2.5 days (estimated: 3 days)
- Delivered:
  - Database models (src/models/example.py)
  - Migrations (migrations/versions/)
  - Unit tests (tests/test_models.py)
- Notes: Faster than expected, schema design was solid

### E-002: API Layer (COMPLETED)
- Status: ✓ Completed 2025-10-25
- Actual effort: 3 days (estimated: 3 days)
- Delivered:
  - FastAPI routes (src/api/routes.py)
  - Request/response models (src/api/models.py)
  - Integration tests (tests/test_api.py)
- Deviations:
  - Added search endpoint (not in original epic)
  - Used simpler caching strategy

### E-003: Testing & Quality (COMPLETED)
- Status: ✓ Completed 2025-10-26
- Actual effort: 1.5 days (estimated: 2 days)
- Delivered:
  - Test coverage: 87% (target: 80%)
  - All quality gates passing
- Notes: Exceeded coverage target

## Lessons Learned for Future Epics

1. **Estimation accuracy:** Data layer took less time due to good planning
2. **Scope changes:** Added search endpoint mid-implementation (user request)
3. **Technology choices:** Simpler caching was sufficient, saved complexity
4. **Quality gates:** Setting ≥80% coverage target was appropriate
```

### Script: `update_asbuilt.py`

**Location:** `.claude/skills/speckit-author/scripts/update_asbuilt.py`

**Purpose:** Reads specs/ from worktree, updates planning/ with as-built details

**Usage:**
```bash
python .claude/skills/speckit-author/scripts/update_asbuilt.py \
  planning/my-feature/ \
  specs/my-feature/
```

**What it does:**
1. Read spec.md and plan.md from merged feature specs/
2. Extract: deviations, actual timelines, lessons learned
3. Update planning/ files with "As-Built" sections
4. Prompt user for: deviation reasons, lessons learned, metrics
5. Commit updates to contrib branch

**Interactive prompts:**
```
Reading as-built specs from merged feature...
  ✓ Found specs/my-feature/spec.md
  ✓ Found specs/my-feature/plan.md

Analyzing deviations from BMAD planning...

Found potential deviation:
  Planned: Redis caching (architecture.md line 64)
  As-Built: LRU cache (spec.md line 142)

Why was this changed?
> [User explains: Simpler, meets requirements]

[Continue for all deviations...]

Found completed epics:
  E-001: Data Layer (3 tasks completed)
  E-002: API Layer (4 tasks completed)

E-001 estimated 3 days, how long did it actually take?
> [User: 2.5 days]

Any lessons learned for E-001?
> [User: Schema design was solid, migrations went smoothly]

[Continue for all epics...]

Updating planning documents...
  ✓ Updated planning/my-feature/requirements.md (added as-built notes)
  ✓ Updated planning/my-feature/architecture.md (added as-built architecture)
  ✓ Updated planning/my-feature/epics.md (added completion status)

Commit these updates? (Y/n)
```

### Why This Matters

**Living Documentation:**
- Planning docs evolve from "planned" to "as-built"
- Historical record of decisions and changes
- Future features can reference actual outcomes

**Improved Planning:**
- Learn from deviations (why did we change the plan?)
- Improve estimation accuracy (actual vs estimated effort)
- Identify patterns (certain epics always take longer)

**Traceability:**
```
requirements.md (planned) → spec.md (detailed) → src/ (code) → requirements.md (as-built)
```
- Complete lifecycle documented
- Easy to find why decisions were made
- Reference for similar future features
