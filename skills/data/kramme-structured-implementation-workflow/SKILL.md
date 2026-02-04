---
name: kramme:structured-implementation-workflow
description: Structured Implementation Workflow (SIW) - Use a structured workflow with three interconnected documents (main specification, open issues, and log) to plan, track, and implement work items. Triggers on "SIW", "structured workflow", or when siw/LOG.md and siw/OPEN_ISSUES_OVERVIEW.md files are detected.
---

# Structured Implementation Workflow (SIW)

A local issue tracking system using markdown files to plan, track, and document implementations without requiring external services.

## When to Use

- Complex features requiring planning and decision tracking
- Multi-issue projects with multiple work items
- Projects without Linear or when you want local-only tracking
- Technical designs, API documentation, or system architecture

**NOT for:** Small bug fixes (<1 day), trivial updates, simple refactoring.

## Quick Start

```
/kramme:siw:init                    # Initialize workflow documents
/kramme:siw:define-issue "feature"  # Create a work item
/kramme:siw:implement-issue 001     # Start implementing
/kramme:siw:restart-issues          # Remove DONE issues, renumber from 001
/kramme:siw:reset                   # Reset for next iteration (keeps spec)
/kramme:siw:remove                  # Clean up when done
```

## Three-Document System

| Document | Purpose | Persistence |
|----------|---------|-------------|
| **siw/[YOUR_SPEC].md** | Main specification (single source of truth) | **PERMANENT** |
| **siw/supporting-specs/*.md** | Detailed specifications by domain | **PERMANENT** |
| **siw/OPEN_ISSUES_OVERVIEW.md** + **siw/issues/*.md** | Work items to implement | Temporary |
| **siw/LOG.md** | Session progress + decision rationale | Temporary |

### What Each Document Contains

**Specification (PERMANENT):**
- Project overview and objectives
- Scope (in/out)
- Design decisions (migrated from siw/LOG.md)
- Success criteria

**Supporting Specs (PERMANENT, optional):**
- Detailed specifications organized by domain
- Examples: data model, API design, UI specs, user stories
- Named with ordering prefix: `00-overview.md`, `01-data-model.md`, etc.
- Main spec references these via TOC

**Issues (TEMPORARY):**
- Individual work items (features, bugs, improvements)
- Each issue has: problem, context, scope, acceptance criteria
- Deleted when implemented

**siw/LOG.md (TEMPORARY):**
- Current progress and status
- Decision log with rationale
- Session continuity between conversations

## Document Flow

```
┌──────────────────────────────────┐
│  /kramme:siw:define-issue        │  Create work items
│  → siw/issues/ISSUE-XXX-*.md     │
└──────────────┬───────────────────┘
               │ Implementation
               ↓
┌──────────────────────────────────┐
│  /kramme:siw:implement-issue     │  Work on issues
│  → siw/LOG.md (progress + decisions) │
└──────────────┬───────────────────┘
               │ Decisions migrated
               ↓
┌──────────────────────────────────┐
│  siw/[YOUR_SPEC].md              │  ⚠️ PERMANENT - single source of truth
│  (updated via sync step)         │
└──────────────────────────────────┘
```

## Critical Rules

1. **Spec NEVER references temp docs** - It's self-contained and permanent
2. **NEVER reference temp docs in code** - Comments, docs, error messages must not mention siw/LOG.md or siw/issues
3. **Decisions flow one-way:** Issues → siw/LOG.md → siw/[YOUR_SPEC].md
4. **Sync before completion:** Always run Step 10 (Spec Sync) in implement-issue

---

## Commands Reference

| Command | Purpose |
|---------|---------|
| `/kramme:siw:init` | Initialize SIW documents (spec, siw/LOG.md, siw/issues) |
| `/kramme:siw:define-issue` | Define a new work item with guided interview |
| `/kramme:siw:implement-issue` | Start implementing a defined issue |
| `/kramme:siw:restart-issues` | Remove DONE issues and renumber remaining from 001 |
| `/kramme:siw:reset` | Reset workflow state (migrate log to spec, clear issues) |
| `/kramme:siw:remove` | Clean up all SIW files after completion |

---

## Working With Existing Files

When SIW files already exist, check the current state:

```bash
ls siw/LOG.md siw/OPEN_ISSUES_OVERVIEW.md siw/*SPEC*.md siw/*SPECIFICATION*.md siw/issues/ 2>/dev/null
```

### Entry Point Decision

| State | Action |
|-------|--------|
| **No files exist** | Run `/kramme:siw:init` to set up |
| **Files exist, resuming** | Read siw/LOG.md "Current Progress" section first |
| **Need new work item** | Run `/kramme:siw:define-issue` |
| **Ready to implement** | Run `/kramme:siw:implement-issue {number}` |
| **Iteration complete** | Run `/kramme:siw:reset` to start fresh |
| **Project complete** | Run `/kramme:siw:remove` to clean up |

### Resuming Work

When resuming a session with existing SIW files:

1. **Read siw/LOG.md first** - Check "Current Progress" section for:
   - What was last completed
   - What's next
   - Any blockers

2. **Check siw/OPEN_ISSUES_OVERVIEW.md** - See which issues are:
   - READY (not started)
   - IN PROGRESS (being worked on)
   - IN REVIEW (awaiting review/approval)
   - DONE (completed)

3. **Continue or start new** - Either:
   - Continue the in-progress issue
   - Pick up the next ready issue with `/kramme:siw:implement-issue`

---

## Issue Lifecycle

```
Created              In Progress           Review              Completed
   │                      │                   │                    │
   ▼                      ▼                   ▼                    ▼
┌─────────┐          ┌─────────┐        ┌─────────┐          ┌─────────┐
│  READY  │ ───────► │IN PROG  │ ─────► │IN REVIEW│ ───────► │  DONE   │
└─────────┘          └─────────┘        └─────────┘          └─────────┘
```

**Issue States:**
- **READY** - Defined, waiting to be picked up
- **IN PROGRESS** - Currently being implemented
- **IN REVIEW** - Work complete, awaiting review/approval
- **DONE** - Finalized (issue file deleted or marked complete)

When an issue is completed:
1. Decisions are logged in siw/LOG.md
2. Key decisions are synced to spec (Step 10)
3. Issue file is deleted
4. Row removed from siw/OPEN_ISSUES_OVERVIEW.md

---

## File Locations

All workflow files live in the `siw/` folder in the project root:

```
/
├── siw/
│   ├── [YOUR_SPEC].md              ⚠️ PERMANENT (name chosen at init)
│   ├── supporting-specs/           ⚠️ PERMANENT (optional, for large projects)
│   │   ├── 00-overview.md
│   │   ├── 01-data-model.md
│   │   ├── 02-api-specification.md
│   │   └── 03-ui-specification.md
│   ├── OPEN_ISSUES_OVERVIEW.md     ⏳ Temporary
│   ├── issues/                     ⏳ Temporary directory
│   │   ├── ISSUE-001-feature-a.md
│   │   └── ISSUE-002-bug-fix.md
│   └── LOG.md                      ⏳ Temporary
├── AGENTS.md                       (optional)
└── CLAUDE.md                       (optional)
```

### When to Use Supporting Specs

Use `siw/supporting-specs/` when:
- Main spec exceeds ~500 lines
- Multiple distinct domains (data model, API, UI, user stories)
- Different team members own different sections
- You want targeted reading during execution

**Naming convention:** `NN-descriptor.md` (e.g., `01-data-model.md`, `02a-cms-ui.md`)

---

## Templates Reference

When manually creating documents, use these templates from:
`skills/kramme:structured-implementation-workflow/resources/templates/`

| Document | Template |
|----------|----------|
| siw/[YOUR_SPEC].md | `templates/spec-guidance.md` |
| siw/LOG.md | `templates/log-template.md` |
| siw/issues | `templates/issues-template.md` |

**Tip:** Using `/kramme:siw:init` and `/kramme:siw:define-issue` is preferred over manual creation.

---

## Phase Resources

For detailed guidance on specific phases, read:

| Phase | Resource |
|-------|----------|
| Resuming existing work | `resources/phase-0-resuming.md` |
| Planning from scratch | `resources/phase-1-planning.md` |
| Handling blockers | `resources/phase-2-investigation.md` |
| Executing tasks | `resources/phase-3-execution.md` |
| Completing work | `resources/phase-4-completion.md` |

---

## Guideline Keywords

- **ALWAYS/NEVER** — Mandatory (exceptions require explicit approval)
- **PREFER** — Strong recommendation (exceptions allowed)
- **CAN** — Optional, developer's discretion
- **NOTE** — Context or clarification
