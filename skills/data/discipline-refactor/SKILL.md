---
name: discipline-refactor
description: Reorganize any repository by discipline/domain with module-based
  structure. Code in src/<pkg>/modules/, documents in <folder>/modules/.
  Orchestrates Explore, Plan, and general-purpose subagents. Works standalone.
version: 2.0.0
category: refactoring
triggers:
  - "refactor by discipline"
  - "organize by domain"
  - "restructure repository"
  - "module-based organization"
  - "discipline-based organization"
prerequisites: none
standalone: true
calls_skills:
  - skill-creator
  - git-sync-manager
  - parallel-batch-executor
calls_subagents:
  - Explore
  - Plan
  - general-purpose
  - Bash
---

# Discipline-Based Refactor (v2.0)

Reorganize any repository to **module-based, discipline-aligned structure**.

## Core Principles

1. **All folders are module-based** - Every directory uses `modules/<discipline>/` pattern
2. **Code lives in modules** - `src/<package>/modules/<discipline>/`
3. **Documents mirror code** - `docs/modules/<discipline>/`, `specs/modules/<discipline>/`
4. **Disciplines are consistent** - Same discipline names across all folders

---

## Target Repository Structure

```
<repo>/
├── src/<package_name>/
│   └── modules/
│       ├── _core/              # Shared utilities
│       ├── <discipline-1>/     # Domain module
│       │   ├── __init__.py
│       │   ├── models.py
│       │   ├── services.py
│       │   └── utils.py
│       └── <discipline-2>/
│
├── tests/
│   └── modules/
│       ├── _core/
│       ├── <discipline-1>/
│       └── <discipline-2>/
│
├── docs/
│   └── modules/
│       ├── _core/
│       ├── <discipline-1>/
│       └── <discipline-2>/
│
├── specs/
│   └── modules/
│       ├── _core/
│       ├── <discipline-1>/
│       └── <discipline-2>/
│
├── data/
│   └── modules/
│       ├── <discipline-1>/
│       └── <discipline-2>/
│
├── logs/
│   └── modules/
│       ├── <discipline-1>/
│       └── <discipline-2>/
│
├── .claude/
│   ├── skills/
│   │   ├── _core/
│   │   ├── <discipline-1>/
│   │   └── <discipline-2>/
│   └── CLAUDE.md
│
└── pyproject.toml / package.json
```

---

## Orchestration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  ORCHESTRATOR: discipline-refactor skill                    │
│  (Stays lean, delegates all execution)                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ Phase 1       │   │ Phase 2       │   │ Phase 3       │
│ ANALYSIS      │   │ PLANNING      │   │ EXECUTION     │
│ Explore       │   │ Plan          │   │ general-purpose│
│               │   │ + skill-creator│  │ + git-sync-mgr│
└───────────────┘   └───────────────┘   └───────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Phase 4: VALIDATION   │
                │ Bash (run tests)      │
                └───────────────────────┘
```

---

## Phase 1: Analysis

**Spawn**: `Task` with `subagent_type=Explore`

**Prompt**:
```
Analyze the repository for discipline-based, module-based refactoring:

1. Identify package name:
   - Check pyproject.toml [project.name] or [tool.poetry.name]
   - Check package.json name
   - Check existing src/<name>/ structure
   - Derive from repo name if not found

2. Scan ALL top-level directories:
   - src/ - code structure
   - tests/ - test organization
   - docs/ - documentation structure
   - specs/ - specifications
   - data/ - data files
   - logs/ - log files
   - .claude/skills/ - skill organization

3. Identify disciplines from existing code:
   - What domain modules exist?
   - What functional areas are present?
   - Map existing directories to discipline names

4. Check for existing modules/ patterns:
   - Already have src/<pkg>/modules/?
   - Already have tests/modules/?
   - What's the current organization level?

5. Output discipline mapping:
   - Suggested disciplines (use consistent names)
   - Current path → new module path for each folder
   - Package name to use

Report in structured format for Phase 2.
```

---

## Phase 2: Planning

**Spawn**: `Task` with `subagent_type=Plan`

**Call**: `@skill-creator` for new discipline skills

**Prompt**:
```
Create module-based migration plan based on Phase 1 analysis.

Context: {analysis_results}

Create plan for ALL directories:

1. Package identification:
   - Confirm package name: <package_name>
   - Confirm disciplines: [_core, discipline-1, discipline-2, ...]

2. Code structure (src/):
   BEFORE: src/<package>/feature1/, src/<package>/feature2/
   AFTER:  src/<package>/modules/_core/, src/<package>/modules/<discipline>/

3. Test structure:
   BEFORE: tests/test_feature1.py, tests/integration/
   AFTER:  tests/modules/_core/, tests/modules/<discipline>/

4. Documentation structure:
   BEFORE: docs/api/, docs/guides/
   AFTER:  docs/modules/_core/, docs/modules/<discipline>/

5. Specs structure:
   BEFORE: specs/feature-spec.md, specs/plan.md
   AFTER:  specs/modules/<discipline>/, specs/templates/

6. Data structure (if exists):
   BEFORE: data/raw/, data/processed/
   AFTER:  data/modules/<discipline>/

7. Skills structure:
   BEFORE: .claude/skills/category/
   AFTER:  .claude/skills/<discipline>/

8. Import updates:
   - from <package>.feature → from <package>.modules.<discipline>
   - Update __init__.py files
   - Update relative imports

9. Create README.md for each module with:
   - Module purpose
   - Key files
   - Dependencies on other modules

Output executable task list for Phase 3.
```

---

## Phase 3: Execution

**Spawn**: `Task` with `subagent_type=general-purpose`

**Call**: `@git-sync-manager`, `@parallel-batch-executor`

**Prompt**:
```
Execute module-based refactoring:

Migration Plan: {migration_plan}
Package Name: {package_name}
Disciplines: {disciplines}

Execute in order:

1. BACKUP:
   git tag pre-module-refactor-$(date +%Y%m%d)

2. CREATE MODULE STRUCTURE:
   # For each discipline in [_core, discipline-1, ...]:
   mkdir -p src/<package>/modules/<discipline>
   mkdir -p tests/modules/<discipline>
   mkdir -p docs/modules/<discipline>
   mkdir -p specs/modules/<discipline>
   mkdir -p data/modules/<discipline>  # if data/ exists
   mkdir -p .claude/skills/<discipline>

3. MOVE CODE:
   # Move source files to appropriate modules
   # Update __init__.py in each module
   # Preserve git history with git mv

4. MOVE TESTS:
   # Move test files to mirror source structure
   # Update test imports

5. MOVE DOCS:
   # Move documentation to module folders
   # Update internal links

6. MOVE SPECS:
   # Move specifications to module folders
   # Keep templates/ at top level

7. UPDATE IMPORTS:
   # Search and replace import paths
   # from <pkg>.old_path → from <pkg>.modules.<discipline>
   # Update conftest.py
   # Update pyproject.toml entry points

8. UPDATE CONFIGS:
   # pyproject.toml: packages, entry points
   # Update CI/CD paths
   # Update Makefile/scripts

9. CREATE MODULE README:
   # Add README.md to each module explaining purpose

Report progress. Stop on failure.
```

---

## Phase 4: Validation

**Spawn**: `Task` with `subagent_type=Bash`

**Prompt**:
```
Validate module-based refactoring:

1. Structure validation:
   - [ ] src/<package>/modules/ exists with disciplines
   - [ ] tests/modules/ mirrors src structure
   - [ ] docs/modules/ exists
   - [ ] specs/modules/ exists
   - [ ] Each module has __init__.py (Python) or index (JS)
   - [ ] Each module has README.md

2. Import validation:
   - [ ] No old import paths remain
   - [ ] All imports resolve
   - [ ] Circular imports checked

3. Test validation:
   - [ ] pytest / npm test passes
   - [ ] Coverage maintained

4. Documentation validation:
   - [ ] Internal links work
   - [ ] Module READMEs complete

Generate report. On failure, suggest:
git checkout pre-module-refactor-{date}
```

---

## Module-Based Folder Mapping

### Standard Folders → Module Structure

| Folder | Module Pattern | Example |
|--------|----------------|---------|
| `src/<pkg>/` | `src/<pkg>/modules/<discipline>/` | `src/myapp/modules/data/` |
| `tests/` | `tests/modules/<discipline>/` | `tests/modules/data/` |
| `docs/` | `docs/modules/<discipline>/` | `docs/modules/data/` |
| `specs/` | `specs/modules/<discipline>/` | `specs/modules/data/` |
| `data/` | `data/modules/<discipline>/` | `data/modules/ingestion/` |
| `logs/` | `logs/modules/<discipline>/` | `logs/modules/api/` |
| `.claude/skills/` | `.claude/skills/<discipline>/` | `.claude/skills/data/` |

### Exceptions (Keep Flat)

| Folder | Reason |
|--------|--------|
| `specs/templates/` | Shared templates |
| `docs/assets/` | Shared images/files |
| `.claude/state/` | Runtime state |
| `scripts/` | Build/deploy scripts |
| `config/` | Configuration files |

---

## Discipline Taxonomy

Standard disciplines (customize per repo):

| Discipline | Purpose | Contains |
|------------|---------|----------|
| `_core` | Shared utilities | Base classes, logging, config, utils |
| `engineering` | Domain expertise | Simulation, analysis, calculations |
| `data` | Data handling | ETL, storage, visualization |
| `api` | External interfaces | REST, GraphQL, webhooks |
| `automation` | Workflows | CI/CD, scripts, jobs |
| `_internal` | Repo-specific | Meta tools, guidelines |

### How to Identify Disciplines

1. What are the main "nouns" in this repo?
2. What expertise areas does the code serve?
3. What would you call the team that owns each part?
4. Use consistent names across src/, tests/, docs/, specs/

---

## Example Transformations

### Python Package

**Before:**
```
mypackage/
├── src/mypackage/
│   ├── utils.py
│   ├── models.py
│   ├── api/
│   └── data/
├── tests/
│   ├── test_utils.py
│   └── test_api.py
└── docs/
    ├── api.md
    └── data.md
```

**After:**
```
mypackage/
├── src/mypackage/
│   └── modules/
│       ├── _core/
│       │   ├── __init__.py
│       │   └── utils.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py
│       └── data/
│           ├── __init__.py
│           └── models.py
├── tests/
│   └── modules/
│       ├── _core/
│       │   └── test_utils.py
│       └── api/
│           └── test_routes.py
├── docs/
│   └── modules/
│       ├── api/
│       │   └── README.md
│       └── data/
│           └── README.md
└── specs/
    └── modules/
        └── api/
            └── api-spec.md
```

### Import Changes

```python
# Before
from mypackage.utils import helper
from mypackage.api.routes import router

# After
from mypackage.modules._core.utils import helper
from mypackage.modules.api.routes import router
```

---

## Rollback

```bash
git checkout pre-module-refactor-{date}
```

---

## Verification Checklist

- [ ] All code in `src/<pkg>/modules/<discipline>/`
- [ ] All tests in `tests/modules/<discipline>/`
- [ ] All docs in `docs/modules/<discipline>/`
- [ ] All specs in `specs/modules/<discipline>/`
- [ ] Consistent discipline names across all folders
- [ ] Each module has `__init__.py` and `README.md`
- [ ] All imports updated
- [ ] Tests pass
- [ ] No orphaned files outside modules/
