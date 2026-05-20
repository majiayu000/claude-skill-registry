---
name: implement
description: "Execute plan phases, writing code in spaces/ while tracking in ideas/. Use after creating a plan with /plan to implement work."
model: claude-sonnet-4-20250514
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# /implement

Execute implementation phases from PLAN.md, writing code in `spaces/` while tracking progress in `ideas/`.

## Usage

```bash
/implement yourbench YB-2 1.1      # Execute phase 1.1 of issue YB-2
/implement yourbench YB-2 --next   # Auto-find next uncompleted phase
/implement yourbench --next        # Auto-detect issue + next phase
/implement coordinatr 003 --full   # Execute all remaining phases
```

## The Bridge Pattern

```
ideas/yourbench/issues/YB-2-auth/     spaces/yourbench/
├── TASK.md (requirements)            ├── src/
├── PLAN.md (phases)          ←→      │   └── auth/  ← CODE WRITTEN HERE
└── worklog/                          └── tests/
    ├── _state.json (current state)
    └── 001-phase-*.json (entries)
```

## Prerequisites

**REQUIRED:**
- `issues/###-name/PLAN.md` must exist
- Active issue context (issue number specified or inferable)
- `spaces/{project}/` exists (code repository)

**If PLAN.md missing:** Run `/plan` first to create implementation plan

## Execution Flow

### 1. Parse & Validate
- Locate issue in `ideas/[project]/issues/###-*/`
- Verify `spaces/[project]/` exists
- Check git branch (warn if on main/develop)
- Check dependencies (warn if incomplete)

### 2. Load Worklog Context
Read `worklog/_state.json` for:
- Current phase progress
- Key decisions made
- Previous agent context
- Blockers

### 3. Branch & Status Management
On first phase:
- Create feature branch: `feature/###-slug` or `bugfix/###-slug`
- Update issue status to `in_progress`
- Initialize worklog directory

### 4. Execute Phase
1. Load context:
   - PLAN.md (phases and checkboxes)
   - Spec section from `implements:` field in TASK.md
   - ADRs and research docs
2. Select agent based on phase domain
3. Write code to `spaces/[project]/`
4. Run tests and quality gates
5. Create worklog entry
6. Update PLAN.md checkboxes
7. Update `_state.json`

### 5. Agent Coordination

| Phase Type | Primary Agent |
|------------|---------------|
| Frontend UI | frontend-specialist |
| Backend API | backend-specialist |
| Database | database-specialist |
| Tests (RED) | test-engineer |
| Refactor | code-reviewer |

### 6. Per-Phase Security Checks (Conditional)

Trigger security-auditor after phase if touching:
- Authentication/Authorization
- Secrets/API keys
- Database operations
- File operations
- External APIs
- Deployment config

### 7. Worklog Entries (MANDATORY)

After each phase, create JSON entry:
- Filename: `{sequence:03d}-phase-{slug}.json`
- Required: `type`, `phase`, `author`, `summary`, `work`, `learnings`, `next_steps`, `blockers`

### 8. Final Review (--full mode)

When all phases complete:
1. Launch code-reviewer agent
2. Launch security-auditor agent
3. Process combined results
4. Block if CRITICAL issues

## Modes

### Specific Phase
```bash
/implement yourbench YB-2 1.1  # Execute only phase 1.1
```

### Next Phase
```bash
/implement yourbench YB-2 --next  # Find first uncompleted checkbox
```

### Full Run
```bash
/implement yourbench YB-2 --full  # All remaining phases + final review
```

## Flags

| Flag | Purpose |
|------|---------|
| `--full` | Execute all remaining phases |
| `--next` | Auto-detect next phase |
| `--skip-branch-check` | Skip branch warnings |
| `--skip-security-checks` | Skip per-phase security |
| `--skip-reviews` | Skip final reviews |
| `--force` | Skip dependency warnings |

## Workflow

```
/spec → /issue → /plan → /implement → /commit → /complete
           ↓                 ↓
    implements:        Load spec section
    spec section       for requirements
                             ↓
                   worklog/ entries created
                             ↓
                   spaces/[project]/ code written
```

## Spec Compliance

When implementing, the code should fulfill the requirements from the spec section referenced in the issue's `implements:` field. The `/complete` command will validate that all spec requirements are met.
