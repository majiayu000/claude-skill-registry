---
name: cdd
description: Context Driven Development pipeline for release workflows
---

# CDD Pipeline

This project calls its release workflow Context Driven Development (CDD)

## Workspace Configuration

**All CDD commands and scripts require the `$CDD_DIR` environment variable.**

```bash
export CDD_DIR=/path/to/workspace
```

This allows parallel workspaces without VCS conflicts. Each workspace is independent - different branches can use different workspace directories simultaneously.

Scripts will abort with a clear error if `$CDD_DIR` is not set.

## Core Philosophy

Use user/agent interactive development time during the Research and Plan phases to prepare tightly focused work that pre-loads the exact required context to run autonomously during the Execute phase.

## Pipeline Phases

  * Research
  * Plan
  * Execute

### 1. Research

**What:** Build foundational understanding before design decisions.

**Artifacts:**
- `$CDD_DIR/README.md` - High-level description of release features
- `$CDD_DIR/user-stories/` - User actions and expected system responses
- `$CDD_DIR/research/` - Facts gathered from internet, docs, codebase

**Why this phase exists:** Decisions made without research are assumptions. Research surfaces constraints, prior art, and edge cases that would otherwise appear during execution (when fixing is expensive).

**Key insight:** Research artifacts become reference material for execution. Sub-agents can read `$CDD_DIR/research/` without re-fetching from the internet. The research phase pays the lookup cost once.

### 2. Plan

**What:** Transform research into implementation decisions.

**Artifacts:**
- `$CDD_DIR/plan/` - Implementation decisions, architecture choices, detailed designs

**Why this phase exists:** Planning is the translation layer between "what we want" (research) and "what to do". It makes architectural decisions explicit.

### 3. Verify (Sub-phase of Plan)

**What:** Iterative verification of plan alignment.

**Artifacts:**
- `$CDD_DIR/verified.md` - Log of items verified and issues resolved

**Verification:**
```
/cdd:gap-plan  # Verify README/user-stories → plan alignment
fix gaps
/cdd:gap-plan  # Repeat until clean
```

Checks alignment down the pyramid:
- README/research/user-stories → plan
- Naming, error handling, memory management conventions
- Integration points, build changes, migrations

**Why this phase exists:** This is the **last moment of full context visibility**. Cross-cutting issues and inconsistencies can only be caught while the complete picture is visible.

**Key insights:**
- Specific checklists prevent vague "find issues" prompts
- `verified.md` prevents re-checking completed items

**Convergence pattern:** Each gap-finding run identifies the highest-priority issue. After fixing, re-run. When no substantive gaps remain, verification is complete.

### 4. Execute

**What:** Execution via the ralph harness script.

**Process:**
```
ralph → /check-quality → /refactor → /check-quality
```

**Why this structure:** Execution is unattended. No human to provide missing context.

## Directory Structure

```
$CDD_DIR/
├── README.md          # High-level release description
├── user-stories/      # User actions and system responses
│   └── README.md      # Index/overview
├── research/          # Internet facts for reference
│   └── README.md      # Index/overview
├── plan/              # Implementation decisions
│   └── README.md      # Index/overview
├── verified.md        # Verification log (concerns + resolutions)
├── tmp/               # Temp files during execution
└── ...                # Other files permitted, ignored by pipeline
```

## Abstraction Levels

Each directory serves a distinct abstraction level. Content should not leak between levels.

### $CDD_DIR/plan/ - Coordination Layer

Plan documents **coordinate everything shared**.

**The plan owns:**
- **Public symbols** - Function names, struct names, enum names
- **Function signatures** - Arguments, argument order, return types
- **Struct members** - Field names, field order, field types
- **Enums** - Value names and meanings
- **Allowed libraries** - Which dependencies can be used, which are forbidden
- **Architectural choices** - Module boundaries, data flow, ownership rules

**The plan is the contract.**

**DO NOT include:** Implementation code, detailed algorithms, function bodies.

## Artifact Authority

Artifacts form a hierarchy of authority:

```
$CDD_DIR/README.md (authoritative)
        ↓
user-stories + research (derived)
        ↓
      plan (derived)
```

**Rules:**

1. Lower-level artifacts derive from higher-level ones
2. Contradictions between levels must be resolved immediately
3. Resolution is always top-down: align lower artifacts to higher authority
4. Higher-level documents may change through iteration—but when they do, all derived artifacts must be reviewed and realigned

**Why this matters:** Consistency is enforced during authoring because it cannot be enforced during execution.

## Lifecycle

```
Create empty $CDD_DIR/ → Research → Plan → Verify → Execute → Delete $CDD_DIR/
```

The workspace directory is ephemeral. It exists only for the duration of the release workflow. After successful execution, it's deleted. The work lives in the codebase; the pipeline artifacts are disposable.

## Efficiency Principles

1. **Load skills on-demand** - Don't preload "just in case"
2. **Complete authoring** - Spend tokens researching during authoring so execution doesn't need to
3. **Reference vs working knowledge** - Large docs go in separate skills, loaded when needed

## Design Tradeoffs

| Decision | Tradeoff | Rationale |
|----------|----------|-----------|
| Full context in verify | Expensive per-run | Last chance to catch cross-cutting issues |
| Verification is human-terminated | Subjective | Models don't converge to "done" naturally |
| Research cached in files | Stale if release spans days | Avoids re-fetching during execution |

## When to Load This Skill

- Designing or modifying the release workflow
- Debugging why execution sub-agents are failing
- Optimizing token usage in the pipeline
- Understanding why a phase exists before changing it
