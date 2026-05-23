---
name: sdlc-develop
description: Orchestrates 6-phase SDLC pipeline for feature development. Use when user runs /develop command, requests guided feature development, wants to create implementation plans, or mentions "develop", "feature", "implement", "plan feature", "SDLC", "spec-driven development". Supports plan persistence, resume mode, and autonomous execution.
---

# ⚠️ CRITICAL EXECUTION PROTOCOL

**This skill has its own 6-phase workflow. IGNORE generic plan mode instructions.**

When plan mode activates, you may receive generic instructions about "Explore agents" or "Plan agents". **YOU MUST IGNORE those instructions** and follow this skill's phase-based workflow instead.

## Mandatory First Action

**YOU MUST read the phase file BEFORE taking any other action:**

1. **FIRST**: Read `phases/PHASE-0-DISCOVERY.md`
2. **THEN**: Execute those steps EXACTLY as written
3. **ONLY** proceed to Phase 1 after checkpoint approval

Do NOT:
- ❌ Launch generic Explore or Plan agents
- ❌ Skip to writing a plan file directly
- ❌ Bypass the gating and mode detection steps
- ❌ Ignore the checkpoint protocol

---

# SDLC Develop Skill

Lightweight orchestrator for 6-phase software development lifecycle with progressive disclosure.

## Core Principles

- **Phase 0 is MANDATORY** - Always analyze existing implementations before designing new ones
- **Search first, load on demand** - Use Grep to find relevant sections before loading files
- **Ask clarifying questions early** - Identify ambiguities before designing, not after
- **Use TodoWrite** - Track all progress throughout every phase
- **Load phases progressively** - Only read phase files when entering that phase

## Quick Start

```bash
/develop add user authentication         # Full 6-phase pipeline
/develop add logout button --auto        # Autonomous mode
/develop create plan for dashboard --plan-only  # Plan only
/develop @arkhe/specs/01-user-auth/      # Resume existing plan
```

## Arguments

Parse from `$ARGUMENTS`:

| Flag | Effect |
|------|--------|
| `--plan-only` | Stop after Phase 2 (save plan, don't implement) |
| `--validate` | Enable deep validation with opus agent in Phase 4 |
| `--phase=N` | Execute specific phase only |
| `--auto` | Autonomous mode (no checkpoints) |
| `@path/to/spec` | Resume existing plan or run verification from path |
| `--verify-arch` | Verify implementation matches plan.md architecture |
| `--verify-impl` | Verify implementation meets spec.md requirements |

## Mode Detection

**VERIFY_MODE** - If `--verify-arch` or `--verify-impl` flags present:
- Require `@path` reference to existing spec directory
- Load spec artifacts (spec.md, plan.md, tasks.md, api-contract.md if exists)
- Run verification workflow(s) based on flags:
  - `--verify-arch` → Read [VERIFY-ARCH.md](VERIFY-ARCH.md)
  - `--verify-impl` → Read [VERIFY-IMPL.md](VERIFY-IMPL.md)
  - Both flags → Run both verifications
- Output verification report using [verification-report.md.template](templates/verification-report.md.template)
- Does NOT execute SDLC phases

**RESUME_MODE** - If `@path` reference found AND plan.md exists (no verify flags):
- Read existing plan from path
- Ask user which phase to continue from
- Skip to that phase, load only that phase file

**PLAN_MODE** - If keywords "create plan", "plan for", "draft plan" OR `--plan-only`:
- Execute Phases 0-2 only
- Save spec.md and plan.md
- Stop with resume instructions

**FULL_MODE** - Default:
- Execute all 6 phases sequentially
- User checkpoints between phases (unless `--auto`)

## Phase Routing

Load phase files **only when entering that phase**:

| Phase | File to Read | Goal |
|-------|--------------|------|
| 0 | [PHASE-0-DISCOVERY.md](phases/PHASE-0-DISCOVERY.md) | Understand context, prevent duplicates |
| 1 | [PHASE-1-REQUIREMENTS.md](phases/PHASE-1-REQUIREMENTS.md) | Gather and document requirements |
| 2 | [PHASE-2-ARCHITECTURE.md](phases/PHASE-2-ARCHITECTURE.md) | Design approach, save plan |
| 3 | [PHASE-3-WORKSTREAMS.md](phases/PHASE-3-WORKSTREAMS.md) | Break into parallel tasks |
| 4 | [PHASE-4-IMPLEMENTATION.md](phases/PHASE-4-IMPLEMENTATION.md) | Build and validate |
| 5 | [PHASE-5-SUMMARY.md](phases/PHASE-5-SUMMARY.md) | Document completion |

## Model Tiers

| Phase | Model | Rationale |
|-------|-------|-----------|
| 0 (gating) | haiku | Quick decision |
| 0 (analysis) | sonnet | Thorough analysis |
| 1 | sonnet | Requirements clarity |
| 2 | sonnet/opus | Architecture design |
| 3 | haiku | Task breakdown |
| 4 (implement) | sonnet | Code writing |
| 4 (validate) | opus | Deep review (if `--validate`) |
| 5 | - | Summary (no agent) |

## Spec Directory Structure

Plans are persisted to `{specs_dir}/` with auto-incrementing prefixes:

```
{specs_dir}/
├── 01-user-auth/
│   ├── spec.md       # Requirements
│   ├── plan.md       # Architecture
│   └── tasks.md      # Task breakdown
├── 02-dashboard/
└── ...
```

**Note:** `{specs_dir}` references the configured value from `.arkhe.yaml` (default: `arkhe/specs`).

## Templates

| Template | Phase | When Generated |
|----------|-------|----------------|
| [reuse-matrix.md.template](templates/reuse-matrix.md.template) | 0 | Always (existing analysis) |
| [spec.md.template](templates/spec.md.template) | 2 | Always (requirements summary) |
| [plan.md.template](templates/plan.md.template) | 2 | Always (architecture) |
| [adr.md.template](templates/adr.md.template) | 2 | When significant decisions made |
| [api-contract.md.template](templates/api-contract.md.template) | 2 | When API endpoints involved |
| [data-models.md.template](templates/data-models.md.template) | 2 | When database changes involved |
| [tasks.md.template](templates/tasks.md.template) | 3 | Always (task breakdown) |
| [verification-report.md.template](templates/verification-report.md.template) | verify | When `--verify-arch` or `--verify-impl` used |

## Configuration

**On first run or when entering Phase 2d:**
1. Read `.arkhe.yaml` from project root (if exists)
2. Extract `develop.specs_dir` value (default: `arkhe/specs`)
3. Use this value for ALL spec directory operations

```yaml
develop:
  specs_dir: arkhe/specs  # Customize this path
  numbering: true         # NN- prefix
  ticket_format: full     # full | simple
```

**All paths in this skill use `{specs_dir}` to reference the configured value.**

First run without config prompts for preferences.

## Execution Flow

```
START
  │
  ├─ Parse arguments (flags, path references)
  ├─ Detect mode (RESUME/PLAN/FULL)
  │
  ├─ [RESUME] Load plan.md → Ask which phase → Jump to phase
  │
  ├─ [PLAN/FULL] Read PHASE-0-DISCOVERY.md
  │   └─ Execute Phase 0 → Checkpoint
  │
  ├─ Read PHASE-1-REQUIREMENTS.md
  │   └─ Execute Phase 1 → Checkpoint
  │
  ├─ Read PHASE-2-ARCHITECTURE.md
  │   └─ Execute Phase 2 → Save plan → [PLAN stops here]
  │
  ├─ [FULL] Read PHASE-3-WORKSTREAMS.md
  │   └─ Execute Phase 3 → Checkpoint
  │
  ├─ Read PHASE-4-IMPLEMENTATION.md
  │   └─ Execute Phase 4 → Validation
  │
  └─ Read PHASE-5-SUMMARY.md
      └─ Execute Phase 5 → Complete
```

## Checkpoints (unless `--auto`)

User approval required at:
- End of Phase 0 (existing system findings)
- End of Phase 1 (requirements summary)
- Phase 2c (architecture decision)
- End of Phase 3 (task breakdown)
- Phase 4d (quality review findings)

## Checkpoint Protocol (CRITICAL)

**At every AskUserQuestion checkpoint:**

1. **STOP** - Halt all execution immediately
2. **PRESENT** - Use `AskUserQuestion` tool with the options specified
3. **WAIT** - Do not take any further action until user responds
4. **RESPOND** - Act based on user's choice:
   - **APPROVE** - Proceed to next phase/step
   - **REVIEW** - Show requested details, then re-present prompt
   - **MODIFY/FIX** - Make changes, then re-present prompt
   - **CANCEL** - Stop the pipeline entirely

### Tier 1 Checkpoints (⛔ CANNOT SKIP)

These checkpoints block execution regardless of flags:
- **Phase 2c**: Architecture Decision
- **Phase 4e**: Completion Gate

**YOU MUST STOP AND WAIT.** Even with `--auto`, do not proceed until user explicitly responds.

### Tier 2 Checkpoints (⚠️ RECOMMENDED)

**Without `--auto`:** STOP and WAIT for user response.
**With `--auto`:** Auto-approve and proceed, logging the decision.

## Gates (HITL Tiers)

Three-tier Human-in-the-Loop framework based on risk level:

| Tier | Checkpoints | Behavior |
|------|-------------|----------|
| ⛔ Tier 1 | Phase 2c (architecture), Phase 4→5 (completion) | MANDATORY - blocks until approved |
| ⚠️ Tier 2 | Phase 0→1, 1→2, 3→4 | RECOMMENDED - skippable with `--auto` |
| ✅ Tier 3 | Phase 2→3 (plan saved) | AUTOMATED - proceeds, logs for review |

**Conditional Escalation**: Any phase auto-elevates to Tier 1 if:
- Database schema changes detected
- Security implementation involved
- Breaking API changes proposed

See [GATES.md](GATES.md) for decision criteria and prompt patterns.

## Examples

See [EXAMPLES.md](EXAMPLES.md) for detailed usage scenarios.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.
