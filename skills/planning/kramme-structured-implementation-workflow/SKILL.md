---
name: kramme:structured-implementation-workflow
description: Use a structured workflow with three interconnected documents (main specification, open issues, and log) to plan, track, and document complex implementations, ensuring clarity and continuity. Use when you detect the presence of LOG.md and OPEN_ISSUES_OVERVIEW.md files.
---

# Structured Implementation Workflow

## When to Use

- Complex features requiring planning and decision tracking
- Comprehensive documentation or detailed technical content
- Multi-day projects with investigation and research phases
- Technical designs, API documentation, or system architecture

**NOT for:** Small bug fixes (<1 day), trivial updates, simple refactoring, quick documentation fixes.

## Three-Document System

| Document | Purpose | Persistence |
|----------|---------|-------------|
| **[YOUR_SPEC].md** | Main specification (single source of truth) | **PERMANENT** |
| **OPEN_ISSUES_OVERVIEW.md** + **issues/*.md** | Active blockers and investigations | Temporary |
| **LOG.md** | Session progress + decision rationale | Temporary |

**Document name:** Choose spec name in Phase 1 (FEATURE_SPECIFICATION.md, API_DESIGN.md, PROJECT_PLAN.md, etc.)

**Issues:** Overview table + individual issue files for progressive disclosure.

## Critical Rules

- **[YOUR_SPEC].md NEVER references** OPEN_ISSUES.md or LOG.md (it's self-contained and permanent)
- **NEVER reference temp docs** in deliverables (code comments, docs, error messages, logs)
- **Information flows one-way:** Issues → LOG (progress + decisions) → [YOUR_SPEC].md
- **After completing tasks:** ALWAYS ask user to review unless they've opted out

## Document Flow

```
┌──────────────────────────────────┐
│  OPEN_ISSUES_OVERVIEW.md         │  ⏳ Temporary
│  + issues/ISSUE-XXX-*.md         │     Track blockers (overview + details)
└──────────────┬───────────────────┘
               │ Investigation & resolution
               ↓
┌──────────────────────────────────┐
│      LOG.md                      │  ⏳ Temporary - progress + WHY
└──────────────┬───────────────────┘
               │ Final details incorporated
               ↓
┌──────────────────────────────────┐
│ [YOUR_SPEC].md                   │  ⚠️ PERMANENT - single source of truth
└──────────────────────────────────┘
```

---

## Getting Started

**First, check for existing workflow files:**

```bash
ls LOG.md OPEN_ISSUES_OVERVIEW.md *SPEC*.md *SPECIFICATION*.md 2>/dev/null
```

### Entry Point Decision

| State | Action |
|-------|--------|
| **No files exist** | Starting fresh → Read `resources/phase-1-planning.md` |
| **LOG.md exists** | Resuming work → Read `resources/phase-0-resuming.md` |
| **Blocked/need decision** | Investigation → Read `resources/phase-2-investigation.md` |
| **Executing tasks** | Execution → Read `resources/phase-3-execution.md` |
| **All tasks complete** | Completion → Read `resources/phase-4-completion.md` |

### When Creating Documents

| Document | Template to Read |
|----------|------------------|
| [YOUR_SPEC].md | `resources/templates/spec-guidance.md` |
| LOG.md | `resources/templates/log-template.md` |
| Issues (overview + files) | `resources/templates/issues-template.md` |

---

## Resource Reference

All resources are in this skill's directory: `skills/kramme:structured-implementation-workflow/resources/`

**Phase Resources:**
- `phase-0-resuming.md` - Entry point for existing projects
- `phase-1-planning.md` - Creating documents from scratch
- `phase-2-investigation.md` - Handling blockers and decisions
- `phase-3-execution.md` - Working through tasks
- `phase-4-completion.md` - Review and completion checklist

**Templates:**
- `templates/spec-guidance.md` - [YOUR_SPEC].md guidance
- `templates/log-template.md` - LOG.md structure and examples
- `templates/issues-template.md` - Issues structure (overview + individual files)

---

## Guideline Keywords

- **ALWAYS/NEVER** — Mandatory (exceptions require explicit approval)
- **PREFER** — Strong recommendation (exceptions allowed)
- **CAN** — Optional, developer's discretion
- **NOTE** — Context or clarification

---

## File Locations

Place all workflow files in your project/work directory root:

```
/
├── [YOUR_SPEC].md              ⚠️ PERMANENT (name based on project type)
├── OPEN_ISSUES_OVERVIEW.md     ⏳ Temporary (deleted after completion)
├── issues/                     ⏳ Temporary directory
│   ├── ISSUE-001-*.md
│   └── ISSUE-002-*.md
├── LOG.md                      ⏳ Temporary (deleted after completion)
├── AGENTS.md                   (optional - project-wide guidelines)
└── CLAUDE.md                   (optional - AI-specific instructions)
```

**Integration:** If your project has AGENTS.md, check it for implementation best practices.
