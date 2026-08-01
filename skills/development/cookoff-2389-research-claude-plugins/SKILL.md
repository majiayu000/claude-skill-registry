---
name: cookoff
description: 'MANDATORY implementation wrapper. ALWAYS invoke when moving from design→code.
  Present 3 options: (1) Cookoff - 2-5 parallel agents compete, each creates own plan,
  pick best, (2) Single subagent, (3) L'
---

---
name: cookoff
description: MANDATORY implementation wrapper. ALWAYS invoke when moving from design→code. Present 3 options: (1) Cookoff - 2-5 parallel agents compete, each creates own plan, pick best, (2) Single subagent, (3) Local. Triggers: "let's build", "implement", "looks good", user picks implementation option, ANY signal to start coding after design. This skill MUST run before writing-plans/executing-plans at design boundaries. For exploring DIFFERENT designs, use omakase-off.
---

# Cookoff

Same design, multiple cooks compete. Each implementation team creates their own plan from the shared design, then implements it. Natural variation emerges from independent planning decisions.

**Part of Test Kitchen Development:**
- `omakase-off` - Chef's choice exploration (different approaches/designs)
- `cookoff` - Same design, multiple cooks compete (each creates own plan + implements)

**Key insight:** Don't share a pre-made implementation plan. Each agent generates their own plan from the design doc, ensuring genuine variation.

## Directory Structure

```
docs/plans/<feature>/
  design.md                    # Input: from brainstorming
  cookoff/
    impl-1/
      plan.md                  # Agent 1's implementation plan
    impl-2/
      plan.md                  # Agent 2's implementation plan
    impl-3/
      plan.md                  # Agent 3's implementation plan
    result.md                  # Cookoff results and winner
```

## Skill Dependencies

| Reference | Primary (if installed) | Fallback |
|-----------|------------------------|----------|
| `writing-plans` | `superpowers:writing-plans` | Each agent writes their own implementation plan |
| `executing-plans` | `superpowers:executing-plans` | Execute plan tasks sequentially with verification |
| `parallel-agents` | `superpowers:dispatching-parallel-agents` | Dispatch multiple Task tools in single message |
| `git-worktrees` | `superpowers:using-git-worktrees` | `git worktree add .worktrees/<name> -b <branch>` |
| `tdd` | `superpowers:test-driven-development` | RED-GREEN-REFACTOR cycle |
| `verification` | `superpowers:verification-before-completion` | Run command, read output, THEN claim status |
| `fresh-eyes` | `fresh-eyes-review:skills` (2389) | 2-5 min review for security, logic, edge cases |
| `code-review` | `superpowers:requesting-code-review` | Dispatch code-reviewer subagent |
| `scenario-testing` | `scenario-testing:skills` (2389) | `.scratch/` E2E scripts, real dependencies |
| `finish-branch` | `superpowers:finishing-a-development-branch` | Verify tests, present options, cleanup |

## When to Use

Trigger when user wants to implement a design:
- "Execute this plan" / "Implement the plan" / "Let's build this"
- After brainstorming completes and design doc exists
- Can also invoke explicitly: "cookoff this"

**Important:** Cookoff works from a **design doc**, not a detailed implementation plan. Each agent creates their own implementation plan.

## Detecting the Design-to-Implementation Transition

**Cookoff triggers at a SITUATION, not a specific skill's output.**

**The situation:** Design is complete, implementation is about to start.

**Signals that design phase just completed:**
- Design doc was written/committed
- User approved a design ("looks good", "yes", "let's do it")
- Discussion shifted from "what to build" to "how to build it"
- Any skill/flow is about to start implementation

**When you detect this transition, ALWAYS offer cookoff:**

```
Before we start implementation, how would you like to proceed?

1. Cookoff (recommended) - N parallel agents, each creates own plan, pick best
   → Complexity: [assess from design]
   → Best for: medium-high complexity features
2. Single implementation - One agent/session implements
3. Direct coding - Start coding without detailed plan
```

**This applies regardless of:**
- Which brainstorming skill was used (superpowers, other, or none)
- Whether a formal design doc exists (could be informal agreement)
- What implementation options another skill might present

**The key insight:** We're not injecting into another skill's menu. We're recognizing a SITUATION (design→implementation) and ensuring cookoff is offered at that moment.

## Phase 1: Implementation Options

**Present choices when user wants to implement:**

```
How would you like to implement this design?

1. Single subagent - One agent plans and implements
2. Cookoff - N parallel agents, each creates own plan, pick best
   → Complexity: [assess from design]
   → Recommendation: N implementations
3. Local - Plan and implement here in this session

Which approach?
```

**Routing:**
- Option 1: Single agent uses writing-plans then executing-plans, cookoff exits
- Option 2: Continue to Phase 2
- Option 3: User implements manually, cookoff exits

## Phase 2: Complexity Assessment

**Read design doc and assess:**
- Feature scope (components, integrations, data models)
- Risk areas (auth, payments, migrations, concurrency)
- Estimated implementation size

**Map to implementation count:**

| Complexity | Scope | Risk signals | Implementations |
|------------|-------|--------------| --------------- |
| Low | Small feature | None | 2 |
| Medium | Medium feature | Some | 3 |
| High | Large feature | Several | 4 |
| Very high | Major system | Critical areas | 5 |

**Setup directories:**
```bash
mkdir -p docs/plans/<feature>/cookoff/impl-{1,2,3}
```

**Announce:**
```
Complexity assessment: medium feature, touches auth
Spawning 3 parallel implementations
Each will create their own implementation plan from the design.
```

## Phase 3: Parallel Execution

**Setup worktrees:**
```
.worktrees/cookoff-impl-1/
.worktrees/cookoff-impl-2/
.worktrees/cookoff-impl-3/

Branches:
<feature>/cookoff/impl-1
<feature>/cookoff/impl-2
<feature>/cookoff/impl-3
```

**CRITICAL: Dispatch ALL agents in a SINGLE message**

Use `parallel-agents` pattern. Send ONE message with multiple Task tool calls:

```
<single message>
  Task(impl-1, run_in_background: true)
  Task(impl-2, run_in_background: true)
  Task(impl-3, run_in_background: true)
</single message>
```

Do NOT send separate messages for each agent.

**Subagent prompt (each gets same instructions with their impl number):**

```
You are implementation team N of M in a cookoff competition.
Other teams are implementing the same design in parallel.
Each team creates their own implementation plan - your approach may differ from others.

**Your working directory:** /path/to/.worktrees/cookoff-impl-N
**Design doc:** docs/plans/<feature>/design.md
**Your plan location:** docs/plans/<feature>/cookoff/impl-N/plan.md

**Your workflow:**
1. Read the design doc thoroughly
2. Use writing-plans skill to create YOUR implementation plan
   - Save to: docs/plans/<feature>/cookoff/impl-N/plan.md
   - Make your own architectural decisions
   - Don't try to guess what other teams will do
3. Use executing-plans skill to implement your plan
4. Follow TDD for each task
5. Use verification before claiming done

**Report when done:**
- Plan created: yes/no
- All tasks completed: yes/no
- Test results (npm test output)
- Files changed count
- Any issues encountered

Your goal: best possible implementation. Good luck!
```

**Monitor progress:**
```
Cookoff status (design: auth-system):
- impl-1: planning... → implementing 5/8 tasks
- impl-2: planning... → implementing 3/8 tasks
- impl-3: planning... → implementing 6/8 tasks
```

## Phase 4: Judging

**Step 1: Gate check**
- All tests pass
- Design adherence - implemented what the design specified

**Step 2: Check for identical implementations**

Before fresh-eyes, diff the implementations:
```bash
diff -r .worktrees/cookoff-impl-1/src .worktrees/cookoff-impl-2/src
```

If implementations are >95% identical, note this - the planning step didn't create enough variation. Still proceed but flag in results.

**Step 3: Fresh-eyes on survivors**
```
Starting fresh-eyes review of impl-1 (N files)...
Checking: security, logic errors, edge cases
Fresh-eyes complete: 1 minor issue
```

**Step 4: Compare survivors**

| Input | Source | Weight |
|-------|--------|--------|
| Fresh-eyes findings | Step 3 | High - quality signal |
| Code complexity | Lines, dependencies | Medium - simpler is better |
| Test coverage | Test count, coverage % | Medium - confidence signal |
| Plan quality | Clarity, task breakdown | Medium - shows thinking |
| Speed | Who finished first | Low - tiebreaker |

**Present comparison:**
```
All 3 implementations passed tests. Fresh-eyes results:

| Impl | Tests | Fresh-Eyes | Lines | Plan approach |
|------|-------|------------|-------|---------------|
| impl-1 | 24/24 | 1 minor | 680 | Component-first |
| impl-2 | 22/22 | 0 issues | 720 | Data-layer-first |
| impl-3 | 26/26 | 2 minor | 590 | TDD-strict |

Recommendation: impl-2 (clean fresh-eyes, solid architecture)

Pick winner: [1] [2] [3] or [show diffs]
```

## Phase 5: Completion

**Verification on winner:**
```
Running final verification on winner (impl-2):
- npm test: 22/22 passing ✓
- npm run build: exit 0 ✓
- Design adherence: all requirements met ✓

Verification complete. Winner confirmed.
```

**Winner:** Use `finish-branch`
- Options: merge locally, create PR, keep as-is, discard

**Losers:** Cleanup
```bash
git worktree remove .worktrees/cookoff-impl-1
git worktree remove .worktrees/cookoff-impl-3
git branch -D <feature>/cookoff/impl-1
git branch -D <feature>/cookoff/impl-3
# Keep winner's worktree until merged
```

**Write result.md:**
```markdown
# Cookoff Results: <feature>

## Design
docs/plans/<feature>/design.md

## Implementations
| Impl | Plan Approach | Tests | Fresh-Eyes | Lines | Result |
|------|---------------|-------|------------|-------|--------|
| impl-1 | Component-first | 24/24 | 1 minor | 680 | eliminated |
| impl-2 | Data-layer-first | 22/22 | 0 issues | 720 | WINNER |
| impl-3 | TDD-strict | 26/26 | 2 minor | 590 | eliminated |

## Plans Generated
- impl-1: docs/plans/<feature>/cookoff/impl-1/plan.md
- impl-2: docs/plans/<feature>/cookoff/impl-2/plan.md
- impl-3: docs/plans/<feature>/cookoff/impl-3/plan.md

## Winner Selection
Reason: Clean fresh-eyes review, solid data-layer-first architecture

## Cleanup
Worktrees removed: 2
Branches deleted: <feature>/cookoff/impl-1, <feature>/cookoff/impl-3
Winner branch: <feature>/cookoff/impl-2
```

Save to: `docs/plans/<feature>/cookoff/result.md`

## Skills Orchestrated

| Dependency | Phase | Usage |
|------------|-------|-------|
| `writing-plans` | 3 | Each subagent creates their own implementation plan |
| `executing-plans` | 3 | Each subagent implements their plan |
| `parallel-agents` | 3 | Dispatch ALL subagents in SINGLE message |
| `git-worktrees` | 3 | Create worktree per implementation |
| `tdd` | 3 | Subagents follow RED-GREEN-REFACTOR |
| `verification` | 3, 5 | Before claiming done; before declaring winner |
| `code-review` | 3 | Review each impl after completion |
| `fresh-eyes` | 4 | Quality review → judge input |
| `scenario-testing` | 4 | Validate if scenarios defined |
| `finish-branch` | 5 | Handle winner, cleanup losers |

## Common Mistakes

**Sharing a pre-made implementation plan**
- Problem: All teams copy same code, no variation
- Fix: Each team uses writing-plans to create THEIR OWN plan from design doc

**Dispatching agents in separate messages**
- Problem: Serial dispatch instead of parallel
- Fix: Send ALL Task tools in a SINGLE message

**Not using writing-plans + executing-plans**
- Problem: Subagent implements ad-hoc
- Fix: Each subagent MUST use writing-plans then executing-plans

**Skipping fresh-eyes**
- Problem: Judge has no quality signal, just test counts
- Fix: Fresh-eyes on ALL survivors before comparing

**Not checking for identical implementations**
- Problem: Wasted compute on duplicates
- Fix: Diff implementations before fresh-eyes, flag if >95% similar

**Forgetting cleanup**
- Problem: Orphaned worktrees and branches
- Fix: Always cleanup losers, write result.md

## Example Invocation

```
User: "Let's build this" (after brainstorming produced design.md)

Claude: I'm using cookoff.

How would you like to implement this design?

1. Single subagent - One agent plans and implements
2. Cookoff - 3 parallel agents, each creates own plan, pick best
   → Complexity: medium feature, touches auth
   → Recommendation: 3 implementations
3. Local - Plan and implement here

User: "2"

Claude: Spawning 3 parallel implementations...
Each will create their own implementation plan from the design.

[Phase 3: Create worktrees, dispatch ALL 3 agents in single message]
[Each agent: reads design → writes plan → implements]

Cookoff status:
- impl-1: planning → implementing 6/8 tasks
- impl-2: planning → implementing 4/7 tasks
- impl-3: planning → implementing 5/9 tasks

[All 3 complete]

[Phase 4: Diff check - implementations are different ✓]
[Fresh-eyes on all 3]

| Impl | Plan Approach | Tests | Fresh-Eyes |
|------|---------------|-------|------------|
| impl-1 | Component-first | 24/24 | 1 minor |
| impl-2 | Data-layer-first | 22/22 | 0 issues |
| impl-3 | TDD-strict | 26/26 | 2 minor |

Recommendation: impl-2 (cleanest)
User: "2"

[Phase 5: Verify winner, cleanup losers]

Winner: impl-2 ready to merge
Cleanup: 2 worktrees removed
Plans preserved: docs/plans/<feature>/cookoff/
```
