---
name: prd-planner
description: Creates PRDs using persistent file-based planning. Use when user explicitly says "PRD", "product requirements document", or "产品需求文档". Combines PRD methodology with planning-with-files to avoid context switching.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, WebSearch
hooks:
  after_complete:
    - trigger: self-improving-agent
      mode: background
      reason: "Extract patterns and improve PRD quality"
    - trigger: session-logger
      mode: auto
      reason: "Save session context"
---

# PRD Planner

A PRD creation skill that uses persistent file-based planning to maintain coherent thinking and avoid "left-brain vs right-brain" context switching issues.

## When This Skill Activates

This skill activates when you:
- Explicitly say "PRD", "prd", "create a PRD", or "产品需求文档"
- Say "product requirements document" or "产品需求"
- Mention "write a PRD for..."
- Say "PRD planning" or "PRD 设计"

**If user says "design solution" or "architecture design" without mentioning PRD, use `architecting-solutions` instead.**

## The Core Philosophy

> "PRD creation should be traceable, coherent, and persistent - not scattered across context switches."

This skill combines:
- **PRD methodology** (from architecting-solutions)
- **File-based persistence** (from planning-with-files)

To create a single, coherent PRD creation workflow that doesn't lose context.

## 4-File Pattern for PRD Creation

For every PRD project, create FOUR files:

Pick a SCOPE (short, unique, kebab-case slug) and use it as a prefix for all files.

```text
docs/{scope}-prd-notes.md     → Store research, requirements, findings, options
docs/{scope}-prd-task-plan.md → Track PRD creation phases and progress
docs/{scope}-prd.md           → Product requirements (what & why)
docs/{scope}-tech.md          → Technical design (how)
```

### File Purposes

| File | Purpose | Audience | Updated When |
|------|---------|----------|--------------|
| `{scope}-prd-notes.md` | Raw research, requirements, architecture options (A/B/C) | Self + reviewers | New information gathered |
| `{scope}-prd-task-plan.md` | Track progress, phases, checkboxes, timestamps | PM + dev lead | Each phase completion |
| `{scope}-prd.md` | Product requirements (what & why), user flows | PM + stakeholders + devs | After requirements are clear |
| `{scope}-tech.md` | Technical design (API, data flow, implementation) | Developers + architects | After architecture is decided |

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRD Creation Workflow                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Initialize → Create 4 files with template                   │
│  2. Requirements → Gather to {scope}-prd-notes.md               │
│  2.5 Edge Cases → Scan codebase, infer patterns, ask smartly    │
│  3. Analysis → Research best practices, save to notes           │
│  4. Design → Propose architecture options (A/B/C), save to notes │
│  5. PRD → Write product requirements to {scope}-prd.md          │
│  6. Tech → Write technical design to {scope}-tech.md            │
│  7. Validate → Review with user, finalize                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                    ↓
           All thinking persisted to files
                    ↓
              No context switching
```

## Step 1: Initialize

Create the four files with templates:

### {scope}-prd-task-plan.md

```markdown
# PRD Task Plan: {Feature Name}

## Goal
Create a PRD and technical design for {feature description}.

## Owner
{User name/role}

## Phases
- [x] Phase 1: Initialize files ✓
- [ ] Phase 2: Gather requirements (CURRENT)
- [ ] Phase 3: Research & analysis
- [ ] Phase 4: Design solution
- [ ] Phase 5: Write PRD
- [ ] Phase 6: Write technical design
- [ ] Phase 7: Validate & finalize

## Status
**Currently in Phase 2** - Gathering requirements from user

## Progress Log
- {timestamp} - Phase 1 complete: Files initialized
```

### {scope}-prd-notes.md

```markdown
# PRD Notes: {Feature Name}

## Raw Requirements
(Add user requirements as they emerge)

## Constraints
(Add technical, business, time constraints)

## Inferred Patterns (from codebase)

| Edge Case | Source | Pattern Applied |
|-----------|--------|-----------------|
| (Filled after Step 2.5 codebase scan) | | |

## Edge Cases

### Auto-handled (following codebase patterns)
- (Filled after Step 2.5 analysis)

### Confirmed by User
- (Filled after user confirms edge case decisions)

### Open Questions
- (Track questions to ask user)

## Research Findings
(Add research on best practices, similar solutions)

## Architecture Options

- Option A: {Description}
  - Pros: {Advantages}
  - Cons: {Disadvantages}

- Option B: {Description}
  - Pros: {Advantages}
  - Cons: {Disadvantages}

- Option C: {Description}
  - Pros: {Advantages}
  - Cons: {Disadvantages}

**Selected**: Option {X}
```

### {scope}-prd.md

```markdown
# PRD: {Feature Name}

> Status: DRAFT
> Last updated: {timestamp}

## Table of Contents
- [Problem Statement](#problem-statement)
- [Goals and Non-Goals](#goals-and-non-goals)
- [Success Criteria](#success-criteria)
- [Scope](#scope)
- [Requirements](#requirements)
- [User Flows](#user-flows)
- [Implementation Plan](#implementation-plan)

---

## Problem Statement
_To be filled after requirements gathering_

## Goals and Non-Goals
### Goals
- {Specific achievable outcomes}

### Non-Goals
- {Explicit exclusions}

## Success Criteria
_To be filled with measurable criteria_

## Scope
### In Scope
- {Specific items included}

### Out of Scope
- {Specific items excluded}

... (rest of PRD sections)
```

### {scope}-tech.md

```markdown
# Technical Design: {Feature Name}

> Status: DRAFT
> Last updated: {timestamp}

## Overview
{High-level technical approach}

## Key Components
{List major components and their responsibilities}

## API Design
{API signatures, request/response formats}

## Data Flow
{How data flows through the system}

## Implementation Details
{Specific implementation notes}

## Migration Plan
{If applicable, how to migrate from existing system}
```

## Step 2: Gather Requirements

Ask clarifying questions and save responses to `{scope}-prd-notes.md`:

### Core Questions to Ask

1. **Problem**: What problem are we solving?
2. **Users**: Who will use this?
3. **Success**: How do we know it's successful?
4. **Constraints**: Any technical/time/budget constraints?

Save each answer to `{scope}-prd-notes.md` under appropriate section.

**Always update `{scope}-prd-task-plan.md` after gathering info:**
```markdown
- [x] Phase 2: Gather requirements ✓
- [ ] Phase 2.5: Edge case analysis (CURRENT)
- [ ] Phase 3: Research & analysis
```

## Step 2.5: Context-Aware Edge Case Analysis

Before asking users about edge cases, **scan the codebase first** to infer existing patterns. This reduces redundant questions and ensures consistency with the project.

> **Detailed reference**: See `references/edge-case-analysis.md` for full scanning commands and output formats.

### Quick Process

1. **Scan codebase** for existing patterns (delete strategy, error handling, empty states, pagination)
2. **Identify requirement type** (CRUD, State Workflow, Async, Data Display, Form, File)
3. **Generate smart assumptions** - patterns found in code don't need user confirmation
4. **Ask only when needed** - no precedent, multiple patterns, or business decision required

### When to Ask Users

| Condition | Action |
|-----------|--------|
| Pattern exists in codebase | Auto-apply, no question needed |
| No precedent found | Ask user with options |
| Multiple conflicting patterns | Ask user to choose |
| Business rule required | Ask user |

### Output to Notes File

Update `{scope}-prd-notes.md` with:

```markdown
## Inferred Patterns (from codebase)
| Edge Case | Source | Pattern Applied |
|-----------|--------|-----------------|
| Delete | `src/models/User.ts:45` | Soft delete |

## Edge Cases
### Auto-handled (following codebase patterns)
- Empty list → Use existing EmptyState component

### Confirmed by User
- Concurrent edit: Last write wins (confirmed {date})
```

**Update task plan:**
```markdown
- [x] Phase 2.5: Edge case analysis ✓
- [ ] Phase 3: Research & analysis (CURRENT)
```

## Step 3: Research & Analysis

Research best practices and save to `{scope}-prd-notes.md`:

```bash
# Search for similar implementations
grep -r "keyword" packages/ --include="*.ts"

# Search web for best practices
web search "best practices for {feature}"
```

Save findings to `{scope}-prd-notes.md` → Research Findings section.

## Step 4: Design Solution

Propose architecture with trade-offs, save to `{scope}-prd-notes.md`:

```markdown
## Architecture Options

- Option A: {Description}
  - Pros: {Advantages}
  - Cons: {Disadvantages}

- Option B: {Description}
  - Pros: {Advantages}
  - Cons: {Disadvantages}

- Option C: {Description}
  - Pros: {Advantages}
  - Cons: {Disadvantages}

**Selected**: Option {X} - because {reason}
```

## Step 5: Write PRD

Read `{scope}-prd-notes.md` and synthesize into polished PRD:

```markdown
1. Read {scope}-prd-notes.md to understand:
   - Requirements gathered
   - Research findings
   - Architecture decision (which option was selected)

2. Write {scope}-prd.md with:
   - Clear problem statement
   - Goals and Non-Goals (explicit exclusions)
   - Measurable success criteria (specific numbers/timings)
   - Scope (In Scope / Out of Scope)
   - Functional requirements
   - Non-functional requirements
   - User flows
   - Implementation plan (high level)

3. Reference tech doc: "See {scope}-tech.md for technical design"
```

## Step 6: Write Technical Design

```markdown
1. Read {scope}-prd-notes.md for selected architecture option

2. Write {scope}-tech.md with:
   - Overview (technical approach summary)
   - Key Components (what pieces, responsibilities)
   - API Design (signatures, contracts)
   - Data Flow (how data moves through system)
   - Implementation Details (specific notes)
   - Migration Plan (if applicable)
```

## Step 7: Validate & Finalize

Review with user:
1. Present PRD summary
2. Ask for feedback
3. Incorporate changes
4. Mark Phase 7 complete

## Important Rules

| Rule | Bad | Good |
|------|-----|------|
| Use Files | Keep in memory | Save to {scope}-prd-notes.md |
| Update Plan | Move on without update | Update task-plan.md with checkbox |
| Read Before Decide | Decide from memory | Read notes first |
| Separate Docs | Mix PRD + Tech | PRD for "what", Tech for "how" |
| Include Options | Jump to solution | Document 2-3 options with pros/cons |

## Phase Transitions

Update `{scope}-prd-task-plan.md` after each phase with checkbox ✓ and timestamp.

## Completing a PRD

Mark all phases complete, set status to "✅ COMPLETE", log final deliverables.

## File Cleanup (Optional)

After PRD is complete:
- Keep `{scope}-prd-notes.md` for reference (shows decision process)
- Archive `{scope}-prd-task-plan.md` or delete
- Final outputs are `{scope}-prd.md` and `{scope}-tech.md`

## Quick Start Template

```markdown
# PRD Task Plan: {Feature}

## Goal
Create PRD and technical design for {description}

## Phases
- [ ] Initialize 4 files
- [ ] Gather requirements
- [ ] Research & analysis
- [ ] Design solution (A/B/C options)
- [ ] Write PRD
- [ ] Write technical design
- [ ] Validate & finalize

## Status
Phase 1: Initializing files
```

## Why This Works

| Problem | Solution |
|---------|----------|
| Context switching | All thinking in files, read anytime |
| Lost requirements | Saved to {scope}-prd-notes.md immediately |
| Inconsistent PRDs | Same process, same structure |
| "Left brain vs right brain" | One coherent workflow |
| Re-explaining context | Files contain full context |
| Mixed concerns | PRD (product) separate from Tech (implementation) |
| Hidden decisions | Architecture options A/B/C documented |

## References

- [planning-with-files](../planning-with-files/) - File-based planning methodology
- [architecting-solutions](../architecting-solutions/) - PRD creation best practices
- Edge case scanning: `references/edge-case-analysis.md`

---

## Auto-Trigger (Automation)

When this skill completes, automatically trigger:
1. **self-improving-agent** (background) - Extract patterns
2. **session-logger** (auto) - Save session context
