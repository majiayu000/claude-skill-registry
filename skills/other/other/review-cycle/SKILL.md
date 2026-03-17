---
name: review-cycle
description: Unified multi-dimensional code review with automated fix orchestration. Routes to session-based (git changes), module-based (path patterns), or fix mode. Triggers on "workflow:review-cycle", "workflow:review-session-cycle", "workflow:review-module-cycle", "workflow:review-cycle-fix".
allowed-tools: Task, AskUserQuestion, TaskCreate, TaskUpdate, TaskList, Read, Write, Edit, Bash, Glob, Grep, Skill
---

# Review Cycle

Unified code review orchestrator with mode-based routing. Detects input type and dispatches to the appropriate execution phase.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────┐
│  Review Cycle Orchestrator (SKILL.md)                     │
│  → Parse input → Detect mode → Read phase doc → Execute   │
└───────────────────────────┬──────────────────────────────┘
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
   │   session    │  │   module    │  │    fix      │
   │  (git changes│  │(path pattern│  │(export file │
   │   review)    │  │   review)   │  │  auto-fix)  │
   └─────────────┘  └─────────────┘  └─────────────┘
   phases/           phases/           phases/
   review-session.md review-module.md  review-fix.md
```

## Auto Mode Detection

```javascript
// ★ 统一 auto mode 检测：-y/--yes 从 $ARGUMENTS 或 ccw 传播
const autoYes = /\b(-y|--yes)\b/.test($ARGUMENTS)
```

When `autoYes` is true, skip all interactive confirmations and use defaults throughout the review cycle phases.

## Mode Detection

```javascript
function detectMode(args) {
  if (args.includes('--fix')) return 'fix';
  if (args.match(/\*|\.ts|\.js|\.py|\.vue|\.jsx|\.tsx|src\/|lib\//)) return 'module';
  if (args.match(/^WFS-/) || args.trim() === '') return 'session';
  return 'session';  // default
}
```

| Input Pattern | Detected Mode | Phase Doc |
|---------------|---------------|-----------|
| `src/auth/**` | `module` | phases/review-module.md |
| `src/auth/**,src/payment/**` | `module` | phases/review-module.md |
| `WFS-payment-integration` | `session` | phases/review-session.md |
| _(empty)_ | `session` | phases/review-session.md |
| `--fix .review/` | `fix` | phases/review-fix.md |
| `--fix --resume` | `fix` | phases/review-fix.md |

## Usage

```
Skill(skill="review-cycle", args="src/auth/**")                                    # Module mode
Skill(skill="review-cycle", args="src/auth/** --dimensions=security,architecture") # Module + custom dims
Skill(skill="review-cycle", args="WFS-payment-integration")                        # Session mode
Skill(skill="review-cycle", args="")                                               # Session: auto-detect
Skill(skill="review-cycle", args="--fix .workflow/active/WFS-123/.review/")        # Fix mode
Skill(skill="review-cycle", args="--fix --resume")                                 # Fix: resume
Skill(skill="review-cycle", args="-y src/auth/**")                                 # Auto mode (skip confirmations)

# Common flags (all modes):
--dimensions=dim1,dim2,...    Custom dimensions (default: all 7)
--max-iterations=N           Max deep-dive iterations (default: 3)

# Fix-only flags:
--fix                        Enter fix pipeline
--resume                     Resume interrupted fix session
--batch-size=N               Findings per planning batch (default: 5)
--max-iterations=N           Max retry per finding (default: 3)
```

## Execution Flow

```
1. Parse $ARGUMENTS → extract mode + flags
2. Detect mode (session | module | fix)
3. Read corresponding phase doc:
   - session → Read phases/review-session.md → execute
   - module  → Read phases/review-module.md  → execute
   - fix     → Read phases/review-fix.md     → execute
4. Phase doc contains full execution detail (5 phases for review, 4+1 phases for fix)
```

**Phase Reference Documents** (read on-demand based on detected mode):

| Mode | Document | Source | Description |
|------|----------|--------|-------------|
| session | [phases/review-session.md](phases/review-session.md) | review-session-cycle.md | Session-based review: git changes → 7-dimension parallel analysis → aggregation → deep-dive → completion |
| module | [phases/review-module.md](phases/review-module.md) | review-module-cycle.md | Module-based review: path patterns → 7-dimension parallel analysis → aggregation → deep-dive → completion |
| fix | [phases/review-fix.md](phases/review-fix.md) | review-cycle-fix.md | Automated fix: export file → intelligent batching → parallel planning → execution → completion |

## Core Rules

1. **Mode Detection First**: Parse input to determine session/module/fix mode before anything else
2. **Progressive Loading**: Read ONLY the phase doc for the detected mode, not all three
3. **Full Delegation**: Once mode is detected, the phase doc owns the entire execution flow
4. **Auto-Continue**: Phase docs contain their own multi-phase execution (Phase 1-5 or Phase 1-4+5)
5. **DO NOT STOP**: Continuous execution until all internal phases within the phase doc complete

## Error Handling

| Error | Action |
|-------|--------|
| Cannot determine mode from input | AskUserQuestion to clarify intent |
| Phase doc not found | Error and exit with file path |
| Invalid flags for mode | Warn and continue with defaults |

## Related Commands

```bash
# View review/fix progress dashboard
ccw view

# Workflow pipeline
# Step 1: Review
Skill(skill="review-cycle", args="src/auth/**")
# Step 2: Fix (after review complete)
Skill(skill="review-cycle", args="--fix .workflow/active/WFS-{session-id}/.review/")
```
