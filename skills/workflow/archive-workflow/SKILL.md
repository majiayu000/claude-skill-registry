---
name: archive-workflow
description: Use when organizing projects - detecting clutter, enforcing naming conventions, structuring directories, managing gitignore, or assessing project expandability. Triggers on project organization requests, file naming audits, or gitignore maintenance needs.
---

# archive-workflow

A comprehensive project organization skill with 1 PM orchestrator (library-pm) and 5 specialist agents, using a 4-wave workflow to manage clutter, naming, structure, and expandability across any project type.

## Overview

This skill coordinates multiple specialized agents to analyze and reorganize projects. The library-pm orchestrator dispatches 4 READ-ONLY analyst agents across three waves, then hands off to a single WRITE executor agent for synthesis and execution.

**Architecture**: Hub-and-spoke multi-agent coordination
**Pattern**: CQRS (Command Query Responsibility Segregation) - analysts READ, integrator WRITES

## When to Use

- Organizing a new project with proper structure
- Cleaning up an existing project with accumulated clutter
- Enforcing consistent naming conventions
- Reviewing gitignore for missing patterns
- Assessing project scalability and modularity
- Major project reorganization before release

## When NOT to Use

- Code refactoring (organizing structure is in scope; rewriting code is not)
- Content creation (where documentation goes is in scope; writing it is not)
- CI/CD pipeline configuration
- Database schema design
- Secret management beyond gitignore context

## Architecture Diagram

```
                        archive-workflow
                           (SKILL.md)
                               |
                               v
                          library-pm
                      (Orchestrator Agent)
                               |
        +----------------------+----------------------+
        |                      |                      |
        v                      v                      v
   [Wave 1]              [Wave 2]               [Wave 3]
        |              (parallel)                    |
        v                  |                         v
+----------------+    +----+----+         +------------------+
| clutter-       |    |         |         | expandability-   |
| analyst        |    v         v         | reviewer         |
| (READ-ONLY)    | +--------+ +--------+  | (READ-ONLY)      |
+----------------+ |nomencl-| |struct- |  +------------------+
        |          |ature-  | |ure-    |          |
        |          |enforcer| |organiz-|          |
        v          |(READ)  | |er(READ)|          v
clutter-report.md  +---+----+ +---+----+  expandability-
                       |          |       assessment.md
                       v          v
              naming-      structure-
              violations.md proposal.md
                       |          |
                       +----+-----+
                            |
                            v
                       [Wave 4]
                            |
                            v
               +------------------------+
               | decision-integrator    |
               | (READ + WRITE)         |
               +------------------------+
                            |
                            v
               execution-log.md + final-organization-report.md
```

## Pre-flight Checks (Phase 0)

Before ANY analysis or file operations:

### 1. Git Status Check
```bash
git status --porcelain
```
- If empty: PROCEED
- If non-empty: STOP and prompt user (stash, commit, or abort)

### 2. Detached HEAD Check
- If detached: STOP ("Cannot run archive-workflow in detached HEAD state")

### 3. Permissions Check
- Verify write permissions on project directory

### 4. Disk Space Check
- Warn if <100MB available in /tmp

## The 4-Wave Pipeline

### Wave 1: Clutter Analysis (Sequential)
**Agent**: archive-clutter-analyst (READ-ONLY)
**Timeout**: 10 minutes

Detects:
- Generated files (node_modules/, __pycache__, build/, dist/, .venv)
- Stale content (old branches, abandoned experiments, deprecated code)
- Organizational mess (duplicates, misplaced files, temp files)

**Output**: clutter-report.md

**Quality Gate 2**: Clutter report complete with Summary section

### Wave 2: Parallel Organization (Parallel)
**Agents**: archive-nomenclature-enforcer + archive-structure-organizer (both READ-ONLY)
**Timeout**: 10-15 minutes per agent

**nomenclature-enforcer**:
- Audits file/directory naming against project-type conventions
- Detects existing patterns (adaptive mode)
- Output: naming-violations.md

**structure-organizer**:
- Analyzes current structure vs project-type template
- Prescriptive for new projects, adaptive for existing
- Output: structure-proposal.md

**Quality Gate 3**: Both reports complete

### Wave 3: Expandability Review (Sequential)
**Agent**: archive-expandability-reviewer (READ-ONLY)
**Input**: structure-proposal.md from Wave 2
**Timeout**: 10 minutes

Assesses:
- Scalability (can structure handle 10x files? 5x contributors?)
- Modularity (components decoupled? extension points?)
- Coupling issues

**Output**: expandability-assessment.md

**Quality Gate 4**: Expandability assessment complete

### Wave 4: Synthesis & Execution (Sequential, User Approval Required)
**Agent**: archive-decision-integrator (READ + WRITE)
**Timeout**: 30 minutes

**Inputs**: All 4 analyst reports
**Process**:
1. Merge outputs, apply conflict resolution rules
2. Generate execution-plan.md for user review
3. Get user approval (APPROVE ALL / APPROVE WITH EXCLUSIONS / REJECT)
4. Execute file operations
5. Generate documentation via editor skill
6. Produce execution-log.md and final-organization-report.md

**Quality Gate 5**: All operations successful, no ERROR entries in log

## Timeout Configuration

| Phase/Wave | Agent | Timeout | Exceeded Action |
|------------|-------|---------|-----------------|
| Phase 0 | Pre-flight checks | 5 min | Abort |
| Phase 1 | library-pm (Project Analysis) | 10 min | Escalate to user |
| Wave 1 | clutter-analyst | 10 min | Retry once, then proceed without |
| Wave 2 | nomenclature-enforcer | 10 min | Retry once, then proceed without |
| Wave 2 | structure-organizer | 15 min | Retry once, then escalate |
| Wave 3 | expandability-reviewer | 10 min | Proceed with advisory flag |
| Wave 4 | decision-integrator | 30 min | Escalate to user |
| Global | All | 2 hours | Save state, escalate to user |

## Quality Gate Specifications

| Gate | Phase | Checks | Pass Threshold | On Failure |
|------|-------|--------|----------------|------------|
| QG1 | Phase 1 | Project type detected, session initialized | All pass | Escalate |
| QG2 | Wave 1 | clutter-report.md exists, has Summary section | 2/2 | Retry once |
| QG3 | Wave 2 | Both Wave 2 reports exist | 2/2 | Proceed with available |
| QG4 | Wave 3 | expandability-assessment.md exists | 1/1 | Proceed with advisory |
| QG5 | Wave 4 | execution-log.md exists, no ERROR entries | 2/2 | Rollback + escalate |

## Execution Plan Approval

Before Wave 4 executes file operations, present to user:

**Category A** (Non-destructive): Renames, moves
- Execute unless user explicitly excludes

**Category B** (Clutter cleanup): Gitignore additions
- Execute unless user explicitly excludes

**Category C** (Deletions): File removals
- REQUIRES EXPLICIT APPROVAL per file

User options:
- APPROVE ALL
- APPROVE WITH EXCLUSIONS (specify files to skip)
- REJECT (abort workflow)

## Conflict Resolution Rules

Apply in order:

1. **Rename + Move**: Combined operation
   - `git mv old_path new_dir/new_name`

2. **Naming vs Structure Directory Name**: Nomenclature wins on naming questions
   - If structure proposes `/Data/`, but naming says kebab-case, use `/data/`

3. **Placement vs Naming**: Structure wins on file placement
   - File goes to best-fit location even if name doesn't perfectly match

4. **Expandability Concerns**: Adjust if critical issue flagged
   - Modify proposal before executing, log reasoning

5. **Clutter Priority**: Process clutter first
   - Add to .gitignore before organizing remaining files

6. **Unresolvable Naming Conflict**: ESCALATE to user
   - When nomenclature and structure propose different names for same file
   - Present both options, document decision

7. **Multi-Analyst Existence Conflict**: ESCALATE to user
   - When clutter says delete, but other analyst needs the file
   - NEVER auto-delete; require explicit user confirmation

## Rollback Procedure

### Case 1: Failure During Wave 4 Execution (Pre-Commit)

If failure occurs BEFORE final commit (during file operations):

**Step 1**: Stop execution immediately

**Step 2**: Check git status:
```bash
git status --porcelain
```

**Step 3**: Revert all unstaged changes:
```bash
git restore .
```

**Step 4**: Unstage all staged changes:
```bash
git restore --staged .
```

**Step 5**: Remove any newly created files (not in git):
```bash
# List new files
git status --porcelain | grep "^??" | cut -c4-

# Manually review and delete if appropriate
```

**Step 6**: Verify clean state:
```bash
git status
# Should show: "nothing to commit, working tree clean"
```

**Step 7**: Clean session directory:
```bash
rm -rf /tmp/archive-workflow-session-{id}/
```

### Case 2: Failure After Commit (Post-Commit)

If failure occurs AFTER final commit (during testing or validation):

**Step 1**: Identify the commit before archive-workflow:
```bash
git log --oneline | head -5
# Find the commit SHA before the archive-workflow commit
```

**Step 2**: Hard reset to that commit:
```bash
git reset --hard <SHA-before-archive-workflow>
```

**Step 3**: Force push if already pushed to remote (ONLY if you're sure):
```bash
# WARNING: Destructive operation - confirm with user first
git push --force origin main
```

**Step 4**: Clean session directory:
```bash
rm -rf /tmp/archive-workflow-session-{id}/
```

### Quick Rollback Decision Tree

```
Failure occurred?
       |
       v
Has commit been made?
       |
   +---+---+
   |       |
   v       v
  YES      NO
   |       |
   v       v
Case 2:   Case 1:
Post-     Pre-
Commit    Commit
Rollback  Rollback
(git      (git
reset     restore)
--hard)
```

## Session Directory Structure

```
/tmp/archive-workflow-session-{YYYYMMDD-HHMMSS-PID}/
├── workflow-state.yaml
├── project-type.md
├── clutter-report.md          (Wave 1 output)
├── naming-violations.md       (Wave 2 output)
├── structure-proposal.md      (Wave 2 output)
├── expandability-assessment.md (Wave 3 output)
├── execution-plan.md          (Pre-Wave 4)
├── execution-log.md           (Wave 4 output)
└── final-organization-report.md (Phase 6 output)
```

## Project Type Detection Heuristics

| Signal | Code | Research | Data | Weight |
|--------|------|----------|------|--------|
| package.json, pyproject.toml, Cargo.toml | +++ | - | - | HIGH |
| .ipynb files | + | +++ | + | MEDIUM |
| Large CSV/JSON/Parquet files | - | + | +++ | MEDIUM |
| .tex files, /papers/ directory | - | +++ | - | HIGH |
| src/, tests/ directories | +++ | + | - | HIGH |
| data/, raw/, processed/ | - | + | +++ | HIGH |

**Classification Logic**:
- If max_score > 2 * second_score: Clear winner
- Elif max_score > 1.5 * second_score: Primary + secondary
- Else: Mixed (prompt user to confirm)

## User Confirmation Points

1. **Before Wave 4**: Execution plan approval
2. **Before deletions**: Explicit confirmation per file (Category C)
3. **After completion**: Final report review

## Graceful Cancellation Handling

If user sends SIGINT (Ctrl+C) or requests cancellation:

1. Complete current atomic operation (e.g., single git mv)
2. Update execution-log.md with partial progress
3. Preserve session directory for resume
4. Report cancellation status to user
5. Provide rollback instructions if needed

## Agent Dispatch

library-pm dispatches agents via Task tool:

```markdown
Use the Task tool to dispatch archive-clutter-analyst:
- Working directory: [project root]
- Task: "Analyze project for clutter following clutter-detection-rules.md"
- Output expected: clutter-report.md in session directory
- Timeout: 10 minutes
```

## Handoffs

| Condition | Hand off to |
|-----------|-------------|
| Wave 1 start | archive-clutter-analyst |
| Wave 2 start | archive-nomenclature-enforcer + archive-structure-organizer (parallel) |
| Wave 3 start | archive-expandability-reviewer |
| Wave 4 start (after approval) | archive-decision-integrator |
| Documentation needed | editor skill |
| Workflow complete | User |
| Critical failure | User (with rollback instructions) |

## References

- references/naming-conventions-code.md
- references/naming-conventions-research.md
- references/naming-conventions-data.md
- references/structure-template-code.md
- references/structure-template-research.md
- references/structure-template-data.md
- references/gitignore-patterns.md
- references/clutter-detection-rules.md

## Examples

- examples/code-project-organization.md
- examples/research-project-organization.md
- examples/mixed-project-organization.md
