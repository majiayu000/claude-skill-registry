---
name: gsd-guide
description: GSD tutorial, command reference, and workflow explainer. Explains what a GSD workflow command does before you run it. Activates when user is new to GSD, asks about commands, wants to understand workflows, or mentions preview.
format: 2025-10-02
version: 1.0.0
status: ACTIVE
updated: 2026-04-15
triggers:
  - "user is new to GSD, asks about commands, wants to understand workflows, or mentions preview"
---

# GSD Guide — Quick Reference + Workflow Explainer

Combines the GSD tutorial/command reference (formerly `gsd-onboard`) with the per-command workflow explainer (formerly `gsd-explain`). Section 1 is the compact reference; Section 2 is the detailed "what will this do before I run it" explainer.

---

## Section 1 — Quick Reference

**GSD** = question → research → plan → execute → verify.

### Files

```
.planning/
├── PROJECT.md       # Vision, decisions
├── REQUIREMENTS.md  # REQ-IDs
├── ROADMAP.md       # Phases
├── STATE.md         # Current position
├── config.json      # Settings
├── phases/NN-name/  # Plans + summaries
└── milestones/      # Archives
```

### Commands

| Command | Purpose |
|---------|---------|
| /gsd:new-project | Init project |
| /gsd:new-milestone | New version |
| /gsd:progress | State + next action |
| /gsd:discuss-phase N | Gather context |
| /gsd:plan-phase N | Create plans |
| /gsd:execute-phase N | Build plans |
| /gsd:quick | Small tasks |
| /gsd:verify-work N | Test deliverables |
| /gsd:audit-milestone | Completion check |
| /gsd:complete-milestone | Archive |
| /gsd:debug | Debug with state |
| /gsd:pause-work | Checkpoint |
| /gsd:resume-work | Restore |

### Workflow

```
plan-phase N → /clear → execute-phase N → verify-work N
```

### Concepts

- **Atomic commits:** One per plan, surgical rollback
- **Fresh context:** `/clear` + STATE.md
- **Wave execution:** Parallel independent plans
- **Modes:** yolo (auto) or interactive

---

## Section 2 — Detailed Explanations

Helps users understand what a GSD command will do before they run it, reducing hesitation and preventing incorrect usage.

### When to Use

Activate when the user:

- Asks "what does /gsd:plan-phase do?"
- Wants to preview changes before running a command
- Is learning GSD and needs explanations
- Mentions wanting to understand a workflow

### What This Skill Does

1. **Reads the workflow file** from `/home/foxy/.claude/get-shit-done/workflows/`
2. **Parses the workflow structure** (trigger, purpose, process steps)
3. **Explains in plain language** what will happen
4. **Shows file previews** (what files will be created/modified)
5. **Estimates resources** (time, context usage, user prompts)

### Explanation Template

When explaining a GSD workflow, use this structure:

```markdown
## /gsd:command-name - [Purpose]

**What it does:**
[2-3 sentence overview]

**Process:**
1. [First step - what happens]
2. [Second step - what happens]
3. [Third step - what happens]

**Files created/modified:**
- `.planning/path/to/file.md` - [purpose]
- `.planning/other/file.json` - [purpose]

**Agents spawned:**
- `agent-name` (model) - [what it does]

**User interaction:**
- [Number] prompts expected
- [Type of input needed]

**Estimated:**
- Time: [duration estimate]
- Context: [percentage of window]

**After completion:**
- [What state the project will be in]
- [Next recommended command]
```

### Key Workflows to Explain

#### Initialization Workflows

**`/gsd:new-project`**

- Spawns 4 parallel researchers (stack, features, architecture, pitfalls)
- Creates PROJECT.md, REQUIREMENTS.md, ROADMAP.md
- Estimates: 15-30 minutes, high context usage
- User prompts: 10-15 questioning rounds

**`/gsd:new-milestone`**

- Updates PROJECT.md with new milestone context
- Creates new REQUIREMENTS.md for milestone scope
- Routes to roadmap creation
- Estimates: 5-10 minutes
- User prompts: 5-8 for requirements

#### Planning Workflows

**`/gsd:discuss-phase N`**

- Gathers user vision for phase before planning
- Creates `.planning/phases/NN-name/NN-CONTEXT.md`
- No agents spawned (direct conversation)
- Estimates: 3-5 minutes
- User prompts: 5-10 contextual questions

**`/gsd:plan-phase N`**

- Optionally spawns `gsd-phase-researcher` (if enabled)
- Spawns `gsd-planner` to create PLAN.md files
- Spawns `gsd-plan-checker` to verify plans
- Creates multiple plan files (`NN-01-PLAN.md`, `NN-02-PLAN.md`, …)
- Estimates: 3-8 minutes
- User prompts: 0-2 (only if plan checker finds issues)

**`/gsd:research-phase N`**

- Spawns `gsd-phase-researcher` standalone
- Creates `NN-RESEARCH.md` with findings
- WebSearch intensive
- Estimates: 5-10 minutes
- User prompts: 0

#### Execution Workflows

**`/gsd:execute-phase N`**

- Spawns `gsd-executor` agents (1 per wave)
- Executes all plans in phase with parallelization
- Creates `NN-NN-SUMMARY.md` for each plan
- Atomic commits per plan
- Estimates: Varies widely by plan complexity
- User prompts: 0 in YOLO mode, varies in interactive mode

**`/gsd:quick`**

- Lightweight execution without full planning
- Single `gsd-executor` agent
- Creates STATE.md entry
- Atomic commit
- Estimates: 2-5 minutes
- User prompts: 0

#### Validation Workflows

**`/gsd:verify-work N`**

- Spawns `gsd-verifier` agent
- UAT-style testing of phase deliverables
- Creates VERIFICATION.md report
- Estimates: 3-7 minutes
- User prompts: Multiple (testing scenarios)

**`/gsd:audit-milestone`**

- Spawns `gsd-verifier` and `gsd-integration-checker`
- Comprehensive completion check
- Creates MILESTONE-AUDIT.md
- Estimates: 5-10 minutes
- User prompts: 0

### File Structure Reference

Help users visualize what files GSD creates:

```
.planning/
├── PROJECT.md           # Vision, requirements, decisions
├── REQUIREMENTS.md      # What we're building (REQ-IDs)
├── ROADMAP.md           # Phase structure and status
├── STATE.md             # Session memory, current position
├── config.json          # Workflow preferences
│
├── phases/
│   ├── 01-foundation/
│   │   ├── 01-CONTEXT.md      # User vision for phase
│   │   ├── 01-RESEARCH.md     # Optional research findings
│   │   ├── 01-01-PLAN.md      # Executable plan
│   │   └── 01-01-SUMMARY.md   # What was built
│   │
│   └── 02-features/
│       └── [same structure]
│
└── milestones/
    └── v1.0-ROADMAP.md        # Archived completed milestones
```

### Agent Type Reference

| Agent Type | Purpose | Spawned By |
|------------|---------|------------|
| `gsd-project-researcher` | Research domain before roadmap | /gsd:new-project |
| `gsd-research-synthesizer` | Synthesize parallel research | /gsd:new-project |
| `gsd-roadmapper` | Create project roadmap | /gsd:new-project |
| `gsd-phase-researcher` | Research implementation approach | /gsd:plan-phase, /gsd:research-phase |
| `gsd-planner` | Create executable plans | /gsd:plan-phase |
| `gsd-plan-checker` | Verify plans match goals | /gsd:plan-phase |
| `gsd-executor` | Execute plans with atomic commits | /gsd:execute-phase, /gsd:quick |
| `gsd-verifier` | Test phase deliverables | /gsd:verify-work |
| `gsd-debugger` | Systematic debugging | /gsd:debug |
| `gsd-integration-checker` | Cross-phase integration tests | /gsd:audit-milestone |

### Common User Questions

**"How long will this take?"** — Initialization: 15-30 minutes. Planning a phase: 3-8 minutes. Executing a phase: 5-40 minutes depending on complexity. Verification: 3-7 minutes.

**"Will this modify my code?"** — Planning workflows only create `.planning/` files. Execution workflows modify code with atomic commits. Verification workflows are read-only.

**"Can I undo this?"** — All GSD commits are atomic (one per plan). Use `git revert <commit>` to undo specific plans. STATE.md tracks what was done.

**"What happens if I /clear mid-workflow?"** — GSD writes `.continue-here.md` files at checkpoints. `/gsd:resume-work` or `/gsd:progress` restores context. STATE.md maintains session continuity.

### Example Explanation

**User asks: "What does /gsd:plan-phase 3 do?"**

```
## /gsd:plan-phase 3 - Create Executable Plans for Phase 3

**What it does:**
Reads Phase 3 from your ROADMAP.md and creates detailed, executable
PLAN.md files that break the phase goal into atomic tasks with
verification criteria.

**Process:**
1. Reads Phase 3 details from .planning/ROADMAP.md
2. Checks for .planning/phases/03-name/03-CONTEXT.md (optional)
3. Spawns gsd-phase-researcher if research enabled in config
4. Spawns gsd-planner to create PLAN.md files
5. Spawns gsd-plan-checker to verify plans achieve phase goal
6. Commits plans to git

**Files created:**
- `.planning/phases/03-name/03-RESEARCH.md` (if research enabled)
- `.planning/phases/03-name/03-01-PLAN.md` (first plan)
- `.planning/phases/03-name/03-02-PLAN.md` (additional plans)

**Agents spawned:**
- gsd-phase-researcher (Opus) - Optional, researches implementation
- gsd-planner (Opus/Sonnet) - Creates executable plans
- gsd-plan-checker (Opus) - Verifies plans match phase goals

**User interaction:**
- 0-2 prompts (only if plan checker finds issues)

**Estimated:**
- Time: 3-8 minutes (longer if research enabled)
- Context: ~30-40% of window

**After completion:**
- Phase 3 plans ready in .planning/phases/03-name/
- Ready to run /gsd:execute-phase 3
```

### Tips for Better Explanations

1. **Use plain language** — avoid jargon, explain technical terms.
2. **Show file paths** — help users visualize what's created.
3. **Estimate honestly** — base estimates on actual workflow complexity.
4. **Mention alternatives** — if there's another way, mention it.
5. **Link to next steps** — what command typically follows?

### Integration with GSD

This skill **complements** GSD by reducing onboarding friction, providing "what if" previews before running commands, explaining GSD's internal agent orchestration, and helping users choose the right workflow. It **does not replace** GSD — users still run the actual commands, no workflow logic is duplicated, and this is purely educational.
