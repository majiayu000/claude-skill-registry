---
name: starwards-workflow
description: Master index for Starwards development workflow - shows when to use each skill, workflow diagram, and how skills integrate together
version: 2025-11-05
author: Claude (based on Starwards project analysis)
related_skills:
  - using-superpowers
  - starwards-tdd
  - starwards-debugging
  - starwards-ci-debugging
  - starwards-verification
  - starwards-monorepo
  - starwards-colyseus
  - writing-plans
  - executing-plans
---

# Starwards Development Workflow

## Overview

This is the **master index** for all Starwards Claude skills. Use this to understand the complete development workflow and when to activate each skill.

## Skill Map

```
┌─────────────────────────────────────────────────────────────────┐
│                     STARWARDS WORKFLOW                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│  NEW TASK    │
└──────┬───────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. PLANNING PHASE                                               │
│                                                                 │
│ ┌─────────────────┐        ┌──────────────────┐              │
│ │ writing-plans   │───────▶│ executing-plans  │              │
│ │ (if complex)    │        │ (batch execution)│              │
│ └─────────────────┘        └──────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. DEVELOPMENT PHASE (Red-Green-Refactor)                       │
│                                                                 │
│ ┌──────────────────────────────────────────────┐              │
│ │ starwards-tdd                                │              │
│ │ • Write failing test (RED)                   │              │
│ │ • Verify it fails correctly                  │              │
│ │ • Minimal implementation (GREEN)             │              │
│ │ • Verify it passes                           │              │
│ │ • Refactor & repeat                          │              │
│ └──────────────────────────────────────────────┘              │
│         │                                                       │
│         │ (if test fails unexpectedly)                         │
│         ▼                                                       │
│ ┌──────────────────────────────────────────────┐              │
│ │ starwards-debugging                          │              │
│ │ Phase 1: Root cause investigation            │              │
│ │ Phase 2: Pattern analysis                    │              │
│ │ Phase 3: Hypothesis testing                  │              │
│ │ Phase 4: Implementation                      │              │
│ └──────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. VERIFICATION PHASE                                           │
│                                                                 │
│ ┌──────────────────────────────────────────────┐              │
│ │ starwards-verification                       │              │
│ │ • npm run test:types (TypeScript)            │              │
│ │ • npm run test:format (ESLint/Prettier)      │              │
│ │ • npm run build (all modules)                │              │
│ │ • npm test (unit/integration)                │              │
│ │ • npm run test:e2e (Playwright)              │              │
│ └──────────────────────────────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. COMPLETION PHASE                                             │
│                                                                 │
│ • Git commit with descriptive message                          │
│ • Push to feature branch                                       │
│ • Create PR (if ready)                                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ SUPPORTING SKILLS (use as needed throughout)                    │
│                                                                 │
│ ┌──────────────────┐  ┌─────────────────┐  ┌────────────────┐│
│ │starwards-monorepo│  │starwards-colyseus│  │using-superpowers│
│ │Build order       │  │@gameField        │  │Skill discovery │ │
│ │3-terminal setup  │  │State sync        │  │Mandatory use   │ │
│ │Module deps       │  │JSON Pointer      │  │Announcements   │ │
│ └──────────────────┘  └─────────────────┘  └────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## Skills Quick Reference

| Skill | When to Use | Key Activities |
|-------|-------------|----------------|
| **using-superpowers** | Start of ANY conversation | Check for relevant skills, announce usage |
| **writing-plans** | Complex multi-step feature | Create detailed implementation roadmap |
| **executing-plans** | Following a plan | Batch execution with checkpoints |
| **starwards-tdd** | Implementing ANY feature/fix | Write test first, RED-GREEN-REFACTOR |
| **starwards-debugging** | Encountering bugs/failures | 4-phase systematic root cause analysis |
| **starwards-ci-debugging** | GitHub Actions CI failures | Install gh CLI, download logs, analyze errors |
| **starwards-verification** | Before claiming "done" | Run full test suite, verify evidence |
| **starwards-monorepo** | Build issues, workspace setup | Understand module dependencies, build order |
| **starwards-colyseus** | State sync issues, multiplayer | @gameField patterns, room architecture |

## Common Workflows

### Workflow 1: New Ship System

```
1. using-superpowers → Announce using starwards-tdd
2. starwards-monorepo → Ensure core watch mode running (Terminal 1)
3. starwards-tdd:
   a. Write unit test (modules/core/test/shield.spec.ts) → RED
   b. Implement system (modules/core/src/ship/shield.ts) → GREEN
   c. Add to ShipState with @gameField
   d. Write integration test with ShipTestHarness → RED
   e. Create manager, add to update loop → GREEN
4. starwards-colyseus → Verify @gameField decorator order
5. starwards-verification → Run npm test, npm run build
6. Commit: "feat: add shield system with recharge mechanics"
```

### Workflow 2: UI Widget

```
1. using-superpowers → Announce using starwards-tdd
2. starwards-monorepo → Ensure all 3 terminals running
3. starwards-tdd:
   a. Write E2E test (modules/e2e/test/shield-widget.spec.ts) → RED
   b. Create widget (modules/browser/src/widgets/shield.ts) → GREEN
   c. Register in Dashboard
   d. Test with data-id selector
4. starwards-verification → Run npm run test:e2e
5. Commit: "feat: add shield status widget to engineering screen"
```

### Workflow 3: Bug Fix

```
1. starwards-debugging:
   Phase 1: Investigate (read error, reproduce, check changes)
   Phase 2: Pattern analysis (find working examples, compare)
   Phase 3: Hypothesis (form single hypothesis, test minimally)
   Phase 4: Implementation (see step 2 below)
2. starwards-tdd:
   a. Write failing test reproducing bug → RED
   b. Implement fix → GREEN
3. starwards-verification → Full test suite
4. Commit: "fix: shield strength not syncing to clients"
```

### Workflow 4: Multiplayer Feature

```
1. starwards-colyseus → Review state sync patterns
2. starwards-tdd:
   a. Write MultiClientDriver test → RED
   b. Add @gameField to state
   c. Implement command handler
   d. Test with 2+ clients → GREEN
3. starwards-verification → npm test, npm run test:e2e
4. Commit: "feat: multi-crew shield power distribution"
```

### Workflow 5: Monorepo Build Issues

```
1. starwards-debugging → Phase 1: Check which module failing
2. starwards-monorepo:
   - Verify build order (core → others)
   - Check if core watch mode running
   - Try fresh build: npm run clean && npm run build
3. If still broken → starwards-debugging Phase 2-4
4. starwards-verification → Verify clean build
```

## Integration Matrix

| From Skill | To Skill | When |
|------------|----------|------|
| using-superpowers | ANY | Start of conversation |
| writing-plans | executing-plans | Plan complete, ready to implement |
| executing-plans | starwards-tdd | Implementing each task in plan |
| starwards-tdd | starwards-debugging | Test fails unexpectedly |
| starwards-debugging | starwards-tdd | Found root cause, write test for fix |
| starwards-tdd | starwards-verification | Implementation complete |
| starwards-verification | (commit) | All checks pass |
| starwards-monorepo | starwards-tdd | Setting up dev environment |
| starwards-colyseus | starwards-tdd | Implementing state sync feature |
| starwards-colyseus | starwards-debugging | State sync not working |

## Skill Dependencies

```
using-superpowers (master skill)
  ├─→ ALL other skills

starwards-tdd
  ├─→ starwards-monorepo (understand build workflow)
  ├─→ starwards-colyseus (when testing state sync)
  └─→ starwards-debugging (when tests fail)

starwards-debugging
  ├─→ starwards-tdd (write test for fix)
  ├─→ starwards-monorepo (debug build issues)
  └─→ starwards-colyseus (debug state sync)

starwards-verification
  ├─→ starwards-monorepo (understand test commands)
  └─→ starwards-tdd (verification patterns)
```

## MANDATORY First Response Protocol

**Before responding to ANY user message:**

1. ☐ Check: Does this match any skill?
2. ☐ Read: Use Skill tool to load relevant skill
3. ☐ Announce: "I'm using [Skill Name] to [task]"
4. ☐ Follow: Execute skill instructions exactly

**Example:**

```
User: "Add a new cloaking device system to ships"

Claude:
1. Checks skills → starwards-tdd matches (implementing new feature)
2. Reads starwards-tdd skill
3. Announces: "I'm using starwards-tdd to implement the cloaking device"
4. Follows TDD cycle: write test → verify RED → implement → verify GREEN
```

## Skill Activation Triggers

| User Says | Activate Skill |
|-----------|----------------|
| "Add X", "Implement Y", "Create Z" | starwards-tdd |
| "Fix bug", "X is broken", "Not working" | starwards-debugging |
| "Is it done?", "Does it work?", "Can I commit?" | starwards-verification |
| "Build fails", "Can't find module", "Import error" | starwards-monorepo |
| "State not syncing", "@gameField issue" | starwards-colyseus |
| "Plan out X", "How should I implement Y?" | writing-plans |
| "Follow this plan..." | executing-plans |

## Version History

- **2025-11-04**: Initial workflow master index created

## Related Documentation

- [CLAUDE.md](../../CLAUDE.md) - Quick reference for AI assistants
- [docs/DEVELOPMENT.md](../../docs/DEVELOPMENT.md) - Development setup
- [docs/testing/README.md](../../docs/testing/README.md) - Testing guide
- [docs/PATTERNS.md](../../docs/PATTERNS.md) - Code patterns

## Quick Links

**Skills:**
- [using-superpowers.md](./using-superpowers.md) - Master skill activation
- [starwards-tdd.md](./starwards-tdd.md) - Test-driven development
- [starwards-debugging.md](./starwards-debugging.md) - Systematic debugging
- [starwards-verification.md](./starwards-verification.md) - Verification commands
- [starwards-monorepo.md](./starwards-monorepo.md) - Monorepo workflow
- [starwards-colyseus.md](./starwards-colyseus.md) - Multiplayer patterns
- [writing-plans.md](./writing-plans.md) - Planning complex features
- [executing-plans.md](./executing-plans.md) - Plan execution

## The Bottom Line

**Development workflow in 4 steps:**

1. **Plan** (if complex) → writing-plans
2. **Develop** (always) → starwards-tdd (RED-GREEN-REFACTOR)
3. **Verify** (always) → starwards-verification (full test suite)
4. **Commit** → git commit & push

**When stuck:**
- Bug/failure → starwards-debugging (4 phases)
- Build issue → starwards-monorepo (check dependencies)
- State sync → starwards-colyseus (check @gameField)

**Remember:** using-superpowers is MANDATORY at start of every conversation.
