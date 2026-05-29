# Skill Creation Plan: Discipline-Based Refactor (General Use)

**Version**: 1.0.0
**Module**: discipline-refactor-skill
**Session ID**: parsed-rolling-starlight
**Session Agent**: Claude Opus 4.5
**Review**: Pending

---

## Summary

Create a **portable, reusable skill** for reorganizing any repository by discipline (domain expertise area). The skill orchestrates other skills and subagents following the orchestrator pattern.

---

## Skill Definition

### Metadata

```yaml
---
name: discipline-refactor
description: Reorganize any repository by discipline/domain. Converts flat
  or functional organization to discipline-based hierarchy. Works standalone.
version: 1.0.0
category: refactoring
triggers:
  - "refactor by discipline"
  - "organize by domain"
  - "restructure repository"
  - "domain-based organization"
prerequisites: none
standalone: true
calls_skills:
  - skill-creator        # For creating new discipline-specific skills
  - git-sync-manager     # For backup and rollback
  - parallel-batch-executor  # For batch file operations
calls_subagents:
  - Explore              # For analysis phase
  - Plan                 # For migration planning
  - general-purpose      # For execution
  - Bash                 # For file operations
---
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
│               │   │               │   │               │
│ Subagent:     │   │ Subagent:     │   │ Subagent:     │
│ Explore       │   │ Plan          │   │ general-purpose│
│               │   │               │   │               │
│ Skills:       │   │ Skills:       │   │ Skills:       │
│ (none)        │   │ skill-creator │   │ git-sync-mgr  │
│               │   │               │   │ parallel-batch│
└───────────────┘   └───────────────┘   └───────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │ Phase 4               │
                │ VALIDATION            │
                │                       │
                │ Subagent: Bash        │
                │ (run tests, verify)   │
                └───────────────────────┘
```

---

## Phase 1: Analysis (Explore Subagent)

**Delegate to**: `Task` with `subagent_type=Explore`

**Prompt template**:
```
Analyze the repository structure for discipline-based refactoring:

1. Scan directory structure and identify:
   - Current organization pattern (flat, functional, domain, mixed)
   - Top-level directories and their purposes
   - File distribution by type and location
   - Existing README files indicating module purposes

2. Identify potential disciplines:
   - What domain expertise areas exist?
   - What are the main "nouns" (entities) in the codebase?
   - What teams/skills would own each part?

3. Detect existing patterns:
   - Check for pyproject.toml, package.json (dependencies)
   - Check for .claude/ directory (existing skills/agents)
   - Check for tests/ structure
   - Check for docs/ structure

4. Output a discipline mapping recommendation:
   - Suggested disciplines with descriptions
   - Which current directories map to which discipline
   - Files/directories that need decisions

Report findings in structured format for Phase 2.
```

**Expected output**: Discipline mapping recommendations

---

## Phase 2: Planning (Plan Subagent + skill-creator)

**Delegate to**: `Task` with `subagent_type=Plan`

**Prompt template**:
```
Based on the analysis from Phase 1, create a migration plan:

Context from Phase 1:
{analysis_results}

Create detailed migration plan including:

1. Final discipline taxonomy:
   - Confirm or adjust recommended disciplines
   - Define _core (shared utilities)
   - Define domain disciplines
   - Define _internal (repo-specific)

2. Directory structure mapping:
   - Before/after for each top-level directory
   - Specific file moves required
   - New directories to create

3. Dependency changes:
   - Import path updates required
   - Config file updates
   - Test path updates

4. New skills to create (delegate to skill-creator):
   - One skill per discipline for domain expertise
   - Skill metadata and trigger descriptions

5. Execution order:
   - Safe order of operations
   - Checkpoints for validation
   - Rollback points

Output as executable task list for Phase 3.
```

**Skills called**:
- `@skill-creator` - To define new discipline-specific skills

**Expected output**: Detailed migration task list

---

## Phase 3: Execution (general-purpose Subagent)

**Delegate to**: `Task` with `subagent_type=general-purpose`

**Prompt template**:
```
Execute the discipline-based refactoring plan:

Migration Plan:
{migration_plan}

Execute in this order:

1. BACKUP (call git-sync-manager skill):
   - Create git tag: pre-refactor-{date}
   - Document current state

2. CREATE STRUCTURE:
   - Create new discipline directories
   - Add README.md to each with purpose description
   - Keep original structure intact (parallel existence)

3. MOVE CONTENT (call parallel-batch-executor skill):
   - Move files to new locations in batches
   - Update imports after each batch
   - Run quick validation after each move

4. UPDATE CONFIGS:
   - Update pyproject.toml / package.json paths
   - Update CI/CD workflows if present
   - Update documentation references

5. CREATE SKILLS:
   - Create .claude/skills/<discipline>/ directories
   - Create SKILL.md for each discipline
   - Update skills-index.yaml if present

Report progress after each step. Stop if any step fails.
```

**Skills called**:
- `@git-sync-manager` - For backup and version control
- `@parallel-batch-executor` - For batch file operations

**Expected output**: Execution report with changes made

---

## Phase 4: Validation (Bash Subagent)

**Delegate to**: `Task` with `subagent_type=Bash`

**Prompt template**:
```
Validate the discipline-based refactoring:

1. Structure validation:
   - Verify all expected directories exist
   - Verify no orphaned files in old locations
   - Verify README.md in each discipline

2. Code validation:
   - Run: {test_command} (e.g., pytest, npm test)
   - Verify all imports resolve
   - Run linter if configured

3. Documentation validation:
   - Check internal links work
   - Verify updated README reflects new structure

4. Generate validation report:
   - Pass/fail for each check
   - Any warnings or issues found
   - Recommendations for follow-up

If validation fails:
- Report which checks failed
- Suggest rollback command: git checkout pre-refactor-{date}
```

**Expected output**: Validation report (pass/fail with details)

---

## Skill Composition Details

### Skills This Skill Calls

| Skill | Phase | Purpose |
|-------|-------|---------|
| `skill-creator` | Phase 2 | Create new discipline-specific skills |
| `git-sync-manager` | Phase 3 | Backup, versioning, rollback |
| `parallel-batch-executor` | Phase 3 | Batch file moves efficiently |

### Subagents Spawned

| Subagent | Phase | Purpose |
|----------|-------|---------|
| `Explore` | Phase 1 | Analyze repo structure |
| `Plan` | Phase 2 | Design migration plan |
| `general-purpose` | Phase 3 | Execute migration |
| `Bash` | Phase 4 | Run tests and validation |

---

## Skill Location (Portable)

```
<any-repo>/.claude/skills/refactoring/discipline-refactor/
├── SKILL.md           # Main skill (this content)
└── README.md          # Quick reference
```

Or centrally:
```
workspace-hub/.claude/skills/meta/discipline-refactor/
├── SKILL.md
├── README.md
└── examples/
```

---

## SKILL.md Template

```markdown
---
name: discipline-refactor
description: Reorganize repository by discipline/domain. Orchestrates
  Explore, Plan, and general-purpose subagents with skill-creator,
  git-sync-manager, and parallel-batch-executor skills.
version: 1.0.0
category: refactoring
standalone: true
---

# Discipline-Based Refactor

Reorganize any repository from flat/functional to discipline-based structure.

## Usage

Invoke with: "refactor by discipline" or "organize by domain"

## Orchestration

This skill orchestrates 4 phases:

### Phase 1: Analysis
Spawns **Explore** subagent to analyze current structure and recommend disciplines.

### Phase 2: Planning
Spawns **Plan** subagent to create migration plan.
Calls **skill-creator** to define new discipline skills.

### Phase 3: Execution
Spawns **general-purpose** subagent to execute migration.
Calls **git-sync-manager** for backup/rollback.
Calls **parallel-batch-executor** for batch operations.

### Phase 4: Validation
Spawns **Bash** subagent to run tests and verify.

## Discipline Taxonomy

Customize these for your repo:

| Discipline | When to Use |
|------------|-------------|
| `_core` | Universal utilities, shared code |
| `<domain>` | Primary business domain |
| `data` | Data handling, ETL |
| `automation` | CI/CD, scripts |
| `_internal` | Repo-specific coordination |

## How to Identify Disciplines

1. What are the main "nouns" in this repo?
2. What expertise areas does the code serve?
3. What would you call the team that owns each part?

## Migration Workflow

```
Step 1: Backup (git tag)
Step 2: Create discipline directories (empty)
Step 3: Move content (update imports)
Step 4: Update configs
Step 5: Create discipline skills
Step 6: Validate (run tests)
```

## Rollback

If any phase fails:
```bash
git checkout pre-refactor-{date}
```

## Verification Checklist

- [ ] All files in discipline directories
- [ ] No orphaned files
- [ ] README.md in each discipline
- [ ] All imports resolve
- [ ] Tests pass
- [ ] Documentation updated
```

---

## Implementation Tasks

### Task 1: Create Skill Directory
```bash
mkdir -p .claude/skills/meta/discipline-refactor
```

### Task 2: Write SKILL.md
Create SKILL.md with:
- Orchestration documentation
- Subagent spawn templates
- Skill call references
- Discipline taxonomy
- Verification checklist

### Task 3: Write README.md
Quick reference with:
- One-page summary
- Common discipline patterns
- Example invocations

### Task 4: Update Skill Index
Add to `.claude/skills-index.yaml`

### Task 5: Test Orchestration
- Verify Explore subagent spawns correctly
- Verify Plan subagent spawns correctly
- Verify skill-creator is called
- Verify git-sync-manager is called
- Verify Bash validation runs

---

## Critical Files

| File | Action |
|------|--------|
| `.claude/skills/meta/discipline-refactor/SKILL.md` | Create |
| `.claude/skills/meta/discipline-refactor/README.md` | Create |
| `.claude/skills-index.yaml` | Update |

---

## Success Criteria

- [ ] SKILL.md documents all 4 phases
- [ ] SKILL.md specifies which subagents to spawn per phase
- [ ] SKILL.md specifies which skills to call per phase
- [ ] Works standalone (can be copied to any repo)
- [ ] Orchestrator pattern followed (delegates, doesn't execute)
- [ ] Skill-creator called for new discipline skills
- [ ] git-sync-manager called for backup
- [ ] parallel-batch-executor called for file moves
- [ ] Verification phase runs tests

---

## Example Discipline Mappings

### Engineering Repo
```
disciplines:
  - _core: Base utilities, logging, config
  - simulation: OrcaFlex, AQWA, FEM
  - analysis: Structural, fatigue, risk
  - data: Input processing, results export
```

### Business App
```
disciplines:
  - _core: Auth, base models, utils
  - invoicing: Invoice generation, payments
  - reporting: Dashboards, exports
  - integrations: External APIs
```

### Data Platform
```
disciplines:
  - _core: Connectors, base transforms
  - ingestion: Data sources, extractors
  - processing: ETL, validation
  - serving: APIs, exports, viz
```
