---
name: bmad-planner
version: 5.1.0
description: |
  Interactive callable tool that creates BMAD planning documents (requirements,
  architecture, epics) in main repository on contrib branch. Three-persona Q&A
  system generates comprehensive planning before feature development.

  Use when: On contrib branch, planning phase, need requirements/architecture

  Triggers: plan feature, requirements, architecture, BMAD
---

# BMAD Planner

## Purpose

Business Model, Architecture, and Design documentation created in main
repository before feature development begins.

**Now available as an interactive callable Python script** - saves ~2,000-2,700 tokens per feature compared to manual reproduction.

## When to Use

- Current directory: main repository (not worktree)
- Current branch: `contrib/<gh-user>`
- Phase: Planning (Phase 1)

## Interactive Callable Tool

BMAD is now an **interactive callable tool** that runs as a Python script in the main repository.

### Invocation

**Command:**
```bash
python .claude/skills/bmad-planner/scripts/create_planning.py \
  <slug> <gh_user>
```

**Arguments:**
- `slug`: Feature slug (e.g., my-feature)
- `gh_user`: GitHub username
- `--no-commit`: Optional flag to skip git commit (for testing)

**Example:**
```bash
# In main repo on contrib branch
python .claude/skills/bmad-planner/scripts/create_planning.py \
  my-feature stharrold
```

### Interactive Session Flow

**Session output:**
```
Working in main repository...
Branch: contrib/stharrold

======================================================================
BMAD Interactive Planning Tool
======================================================================

Creating planning documents for: my-feature
GitHub user: stharrold
Output directory: planning/my-feature

======================================================================
🧠 BMAD Analyst Persona - Requirements Gathering
======================================================================

I'll help create the requirements document through interactive Q&A.
----------------------------------------------------------------------

What problem does this feature solve?
> Add German vocabulary search by part of speech

Who are the primary users of this feature?
> German language learners

[... continues with 5-10 questions ...]

✓ Requirements gathering complete!

======================================================================
🏗️ BMAD Architect Persona - Technical Architecture Design
======================================================================

Based on the requirements, I'll design the technical architecture.
----------------------------------------------------------------------

Technology Stack:

Web framework (if applicable)?
  1) FastAPI
  2) Flask
  3) Django
  4) None
  [default: None]
> 4

[... continues with 5-8 questions ...]

✓ Architecture design complete!

======================================================================
📋 BMAD PM Persona - Epic Breakdown
======================================================================

Analyzing requirements and architecture to create epic breakdown...
----------------------------------------------------------------------

✓ Identified 3 epics:
  - E-001: Data Layer Foundation (Priority: P0, Medium complexity)
  - E-002: Core Business Logic (Priority: P0, High complexity)
  - E-003: Testing & Quality Assurance (Priority: P1, Medium complexity)

✓ Epic breakdown complete!

======================================================================
Generating Planning Documents
======================================================================
  ✓ Created planning/my-feature/CLAUDE.md
  ✓ Created planning/my-feature/README.md
  ✓ Created planning/my-feature/ARCHIVED/CLAUDE.md
  ✓ Created planning/my-feature/ARCHIVED/README.md
  ✓ Created planning/my-feature/requirements.md
  ✓ Created planning/my-feature/architecture.md
  ✓ Created planning/my-feature/epics.md

Committing planning documents...
✓ Committed planning documents for my-feature

======================================================================
✓ BMAD Planning Documents Created Successfully!
======================================================================

Files created in planning/my-feature:
  - requirements.md (Business requirements and acceptance criteria)
  - architecture.md (Technical architecture and design)
  - epics.md (Epic breakdown and planning)
  - CLAUDE.md (Context for Claude Code)
  - README.md (Human-readable overview)
  - ARCHIVED/ (Directory for deprecated planning docs)

Next steps:
  1. Review planning documents in planning/my-feature
  2. Create feature worktree
  3. SpecKit will auto-detect and use these planning documents
  4. Token savings: ~1,700-2,700 tokens by reusing planning context
```

**What happens:**
1. Script validates location (main repo, contrib branch)
2. Conducts 🧠 Analyst Q&A (5-10 questions)
3. Generates requirements.md from template + Q&A responses
4. Conducts 🏗️ Architect Q&A (5-8 questions)
5. Generates architecture.md from template + Q&A responses
6. Automatically analyzes requirements + architecture (📋 PM)
7. Generates epics.md with epic breakdown
8. Creates compliant planning/<slug>/ directory structure
9. Commits changes to contrib branch

**Token Efficiency:**

| Approach | Token Usage | Savings |
|----------|-------------|---------|
| **Before (manual):** Claude Code reproduces BMAD each time | ~2,500 tokens | - |
| **After (callable tool):** Claude Code calls script | ~200 tokens | ~2,300 tokens (92%) |

### Script Architecture

**Location:** `.claude/skills/bmad-planner/scripts/create_planning.py`

**Key functions:**
- `detect_context()` - Verify main repo, contrib branch
- `interactive_qa_analyst()` - 🧠 Requirements Q&A
- `interactive_qa_architect()` - 🏗️ Architecture Q&A
- `generate_epic_breakdown()` - 📋 Auto-generate epics
- `process_*_template()` - Replace placeholders, inject Q&A responses
- `create_directory_structure()` - CLAUDE.md, README.md, ARCHIVED/
- `commit_planning_docs()` - Git commit

## Document Templates

Templates are located in `templates/`:
- `requirements.md.template` - Business requirements and acceptance criteria (170 lines)
- `architecture.md.template` - System architecture and design decisions (418 lines)
- `epics.md.template` - Epic breakdown with priorities and dependencies (245 lines)

## Interactive Planning Approach

BMAD uses a three-persona method to gather comprehensive planning information through interactive Q&A sessions with the user.

### 🧠 Persona 1: BMAD Analyst (Requirements)

**Role:** Business Analyst creating Product Requirements Document

**Process:**
1. Ask user about problem statement and business context
2. Identify target users and stakeholders
3. Define success criteria and measurable outcomes
4. Gather functional and non-functional requirements
5. Document user stories with scenarios
6. Identify risks and constraints

**Interactive Q&A Example:**
```
I'll help create the requirements document using the BMAD Analyst persona.

What problem does this feature solve?
> [User describes the problem]

Who are the primary users of this feature?
> [User identifies user types]

How will we measure success for this feature?
> [User defines success metrics]

What are the must-have capabilities? (functional requirements)
> [User lists key capabilities]

Any performance, security, or scalability requirements? (non-functional)
> [User specifies NFRs]
```

**Generates:** `planning/<feature>/requirements.md` using comprehensive template

### 🏗️ Persona 2: BMAD Architect (Architecture)

**Role:** Technical Architect designing system architecture

**Process:**
1. Read requirements.md for business context
2. Ask user about technology preferences and constraints
3. Design system components and data models
4. Define API contracts and integration points
5. Specify security, error handling, testing strategies
6. Document deployment and observability approach

**Interactive Q&A Example:**
```
Based on the requirements, I'll design the technical architecture.

Technology preferences?
- Web framework: FastAPI / Flask / Django?
> [User chooses framework]

Database requirements?
- Development: SQLite
- Production: PostgreSQL / MySQL?
> [User chooses database]

Performance targets?
- Response time: < 200ms?
- Concurrent users: How many?
> [User specifies targets]

Container strategy?
- Using Podman (default for this project)
- Multi-container setup needed?
> [User confirms approach]
```

**Generates:** `planning/<feature>/architecture.md` using comprehensive template

### 📋 Persona 3: BMAD PM (Epic Breakdown)

**Role:** Project Manager breaking down work into epics

**Process:**
1. Read requirements.md + architecture.md for full context
2. Identify major work streams (epics)
3. Define scope, complexity, and dependencies for each epic
4. Prioritize epics (P0/P1/P2)
5. Create implementation timeline
6. Estimate effort and identify risks

**Analysis:**
```
Analyzing requirements and architecture to create epic breakdown...

Identified 3 major epics:
1. E-001: Data Layer (Foundation) - P0, High complexity
2. E-002: API Layer (Core functionality) - P0, Medium complexity
3. E-003: Testing & Quality - P1, Medium complexity

Dependencies detected:
  E-001 → E-002 (API needs data layer)
  E-002 → E-003 (tests need API)

Creating epic breakdown document...
```

**Generates:** `planning/<feature>/epics.md` with epic definitions, priorities, timeline

## How to Invoke BMAD

When workflow-orchestrator loads bmad-planner during Phase 1, it calls the create_planning.py script.

**Workflow Orchestrator Code:**
```python
# In workflow orchestrator - Phase 1.1
if current_phase == 1 and current_step == '1.1':
    import subprocess

    result = subprocess.run([
        'python',
        '.claude/skills/bmad-planner/scripts/create_planning.py',
        slug,       # my-feature
        gh_user,    # stharrold
    ], check=True)

    # Script handles:
    # - 🧠 Analyst Q&A with user
    # - 🏗️ Architect Q&A with user
    # - 📋 PM epic breakdown (automatic)
    # - requirements.md, architecture.md, epics.md generation
    # - Directory structure creation
    # - Git commit

    print(f"✓ BMAD planning created in planning/{slug}/")
    print("  Next: Create feature worktree (Phase 2)")
```

**User Experience:**
```
Phase 1: BMAD Planning Session

Workflow calls:
  python .claude/skills/bmad-planner/scripts/create_planning.py my-feature stharrold

Script conducts interactive session:
  🧠 BMAD Analyst: Requirements gathering [5-10 questions]
  🏗️ BMAD Architect: Architecture design [5-8 questions]
  📋 BMAD PM: Epic breakdown [automatic analysis]

✓ Generated: planning/my-feature/requirements.md
✓ Generated: planning/my-feature/architecture.md
✓ Generated: planning/my-feature/epics.md
✓ Committed to contrib branch

✓ BMAD planning complete!
  Next: Create feature worktree (Phase 2 will use these docs)
  Token savings: ~2,300 tokens vs manual approach
```

## Integration with Workflow

The workflow-orchestrator calls the create_planning.py script during Phase 1:

```python
# In workflow orchestrator
if current_phase == 1 and current_step == '1.1':
    import subprocess

    result = subprocess.run([
        'python',
        '.claude/skills/bmad-planner/scripts/create_planning.py',
        slug,
        gh_user,
    ], check=True)

    print(f"✓ BMAD planning created: planning/{slug}/")
```

## Output Files

BMAD generates three planning documents that become input context for SpecKit:

```
planning/<feature-name>/
├── requirements.md    # Business requirements (170 lines from template)
│   ├─ Problem statement, stakeholders
│   ├─ Functional requirements (FR-001, FR-002...)
│   ├─ Non-functional requirements (performance, security...)
│   ├─ User stories with scenarios
│   └─ Risks, assumptions, success criteria
│
├── architecture.md    # Technical architecture (418 lines from template)
│   ├─ System overview, components
│   ├─ Technology stack with justifications
│   ├─ Data models, API endpoints
│   ├─ Container architecture (Containerfile, podman-compose.yml)
│   ├─ Security, error handling, testing strategies
│   └─ Deployment, observability, disaster recovery
│
├── epics.md          # Epic breakdown (245 lines from template)
│   ├─ Epic definitions (scope, complexity, priority)
│   ├─ Dependencies and critical path
│   ├─ Implementation timeline
│   └─ Resource requirements and risks
│
├── CLAUDE.md         # Context for this planning directory
├── README.md         # Human-readable overview
└── ARCHIVED/         # Deprecated planning documents
```

**These files become input context for SpecKit in Phase 2.**

## Integration with SpecKit

BMAD documents are used as context when creating SpecKit specifications:

### Data Flow: BMAD → SpecKit

**Phase 1 (Main Repo, contrib branch):**
```
BMAD Interactive Session
  ↓
planning/<feature>/
├── requirements.md
├── architecture.md
└── epics.md
```

**Create Worktree:**
```bash
# Worktree creation preserves link to main repo
git worktree add ../repo_feature_<slug> feature/<timestamp>_<slug>
```

**Phase 2 (Worktree):**
```
SpecKit reads from main repo:
../planning/<feature>/requirements.md → Business context
../planning/<feature>/architecture.md → Technical design
../planning/<feature>/epics.md        → Epic priorities

SpecKit generates (informed by BMAD):
specs/<feature>/spec.md  ← Detailed specification
specs/<feature>/plan.md  ← Implementation tasks
```

### Why This Connection Matters

**Consistency:**
- Technology choices in spec.md match architecture.md stack
- spec.md acceptance criteria cover requirements.md success criteria
- plan.md tasks align with epics.md breakdown

**Completeness:**
- All functional requirements from requirements.md appear in spec.md
- Non-functional requirements (performance, security) included
- Epic dependencies reflected in plan.md task ordering

**Traceability:**
- spec.md sections reference FR-001, FR-002... from requirements.md
- plan.md tasks map to E-001, E-002... from epics.md
- Architecture decisions from architecture.md justify implementation choices

**Less Rework:**
- Planning clarifies requirements before coding
- Design decisions made explicit
- Reduces ambiguity and prevents scope creep

## Integration with Workflow

The workflow-orchestrator calls this skill during Phase 1:

```python
# In workflow orchestrator
if current_phase == 1 and current_step == '1.1':
    load_skill('bmad-planner')
    create_planning_docs(feature_name, gh_user)
    commit_changes('docs: add BMAD planning for ' + feature_name)
```

## Template Placeholders

Both templates use these placeholders:
- `{{TITLE}}` - Feature name (title case)
- `{{DATE}}` - Creation date (YYYY-MM-DD)
- `{{GH_USER}}` - GitHub username

## Best Practices

- **Requirements first**: Define business needs before technical design
- **Acceptance criteria**: Make success measurable
- **Architecture clarity**: Explain design decisions and trade-offs
- **Technology justification**: Document why specific tools/frameworks chosen
- **Non-functional requirements**: Don't forget performance, security, scalability
