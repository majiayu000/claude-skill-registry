---
name: which-skill-to-use
description: Decision tree for choosing the right skill/command for the current situation
---

# Which Skill Should I Use?

Quick decision guide for choosing the right tool.

## Quick Decision Tree

```
START: What do you need to do?
  │
  ├─► Debug/test failure?
  │   └─► Use: systematic-debugging
  │       └─► 3+ failed attempts?
  │           └─► Add: troubleshoot-and-continue
  │
  ├─► Complete work session?
  │   └─► Check time gate: finish-work
  │       └─► Time remaining?
  │           ├─► YES: Keep working
  │           └─► NO: verification-before-completion
  │               └─► /finish (handoff docs)
  │                   └─► finishing-a-development-branch (git)
  │
  ├─► Execute implementation plan?
  │   ├─► Have plan already?
  │   │   ├─► Stay in this session?
  │   │   │   ├─► YES: subagent-driven-development
  │   │   │   └─► NO: executing-plans
  │   │   └─► Need fresh subagent per task + 2 reviewers?
  │   │       └─► Use: subagent-driven-development
  │   └─► Need to create plan first?
  │       └─► Use: writing-plans
  │
  ├─► Complex multi-step work (30+ min)?
  │   ├─► Batch asset generation (10+ sprites/tiles)?
  │   │   └─► Use: /ralph
  │   └─► Feature implementation?
  │       └─► Use: /longplan
  │
  ├─► Parallel investigation?
  │   ├─► Multiple independent problems?
  │   │   └─► Use: dispatching-parallel-agents
  │   └─► Research/analysis tasks?
  │       └─► Use: longplan (5-10+ parallel subagents)
  │
  ├─► Stuck/blocked?
  │   └─► Use: troubleshoot-and-continue
  │       └─► Exhausted all resources?
  │           └─► Consider asking user (last resort)
  │
  └─► Review code?
      ├─► Request review of your work?
      │   └─► Use: requesting-code-review
      └─► Review someone else's PR?
          └─► Use: receiving-code-review
```

## Detailed Selection Guide

### Execution Skills (Getting Work Done)

| Situation | Primary Skill | Why |
|-----------|---------------|-----|
| Have plan, stay in session, fresh subagent per task | `subagent-driven-development` | 2-stage review per task |
| Have plan, new session | `executing-plans` | Parallel session execution |
| Complex feature, multi-step, 30+ min | `/longplan` | 1A2A workflow, autonomous mode |
| Batch assets (10+ tiles/sprites) | `/ralph` | Automatic MiniMax orchestration |
| Quick task, no plan needed | Just do it | No skill overhead |

### Debugging Skills (Fixing Problems)

| Situation | Primary Skill | Addition |
|-----------|---------------|----------|
| Any bug/test failure | `systematic-debugging` | Scientific 4-phase method |
| 3+ failed attempts | Add `troubleshoot-and-continue` | Resource exhaustion protocol |
| Multiple independent failures | `dispatching-parallel-agents` | One agent per problem |

### Completion Skills (Finishing Work)

| Step | Skill/Command | Purpose |
|------|---------------|---------|
| 1 | `finish-work` | Time gate enforcement |
| 2 | `verification-before-completion` | Quality verification |
| 3 | `/finish` | Handoff documentation |
| 4 | `finishing-a-development-branch` | Git workflow (merge/PR) |

### Planning Skills (Before Execution)

| Situation | Skill | Output |
|-----------|-------|--------|
| Need implementation plan | `writing-plans` | Detailed plan file |
| Explore options first | `brainstorming` | Decision on approach |
| Complex task, need worktree | `using-git-worktrees` | Isolated workspace |

## Common Confusions Clarified

### `/longplan` vs `/ralph`
- **`/longplan`**: Complex features, dialogue writing, multi-file changes
- **`/ralph`**: Batch asset generation (sprites, tiles, images)
- **Overlap**: Both use parallel subagents, but `/ralph` is optimized for asset generation

### `subagent-driven-development` vs `executing-plans`
- **`subagent-driven-development`**: Same session, fresh subagent per task + 2 reviewers
- **`executing-plans`**: New parallel session (separate window)
- **Key difference**: Session context (same vs parallel)

### `systematic-debugging` vs `troubleshoot-and-continue`
- **`systematic-debugging`**: Scientific debugging methodology (4 phases)
- **`troubleshoot-and-continue`**: Resource exhaustion for autonomous work
- **Use together**: After 3 failed attempts in systematic debugging, activate troubleshoot-and-continue

### `finish-work` vs `/finish`
- **`finish-work`**: Time gate (session-level)
- **`/finish`**: Handoff docs (after work complete)
- **Use in sequence**: finish-work FIRST, then /finish

## Autonomous Work Recommendations

**For long autonomous blocks (2+ hours):**

1. **Start with**: `/longplan` (creates structured plan)
2. **Debugging**: `systematic-debugging` + `troubleshoot-and-continue`
3. **Self-checkpoint**: Every 30 min or 5 file operations
4. **Quality gates**: verification-before-completion
5. **End with**: finish-work → /finish

**For batch tasks (10+ similar items):**

1. **Use**: `/ralph` (optimized for batch work)
2. **Self-checkpoint**: Progress file auto-updates
3. **End with**: finish-work → /finish

**For stuck tasks:**

1. **First**: Try 2-3 alternatives yourself
2. **Then**: `troubleshoot-and-continue` protocol
3. **Spawn**: MiniMax subagents for help
4. **Last resort**: Document and skip to next task

## When Skills Combine

**Example: Complex feature with debugging**
```
1. /longplan (create plan)
2. During 2A: systematic-debugging (if bugs found)
3. If stuck: troubleshoot-and-continue
4. End: finish-work → /finish
5. If branch: finishing-a-development-branch
```

**Example: Batch asset generation with issues**
```
1. /ralph (generate assets)
2. If failures: dispatching-parallel-agents (parallel debugging)
3. End: finish-work → /finish
```

## Quick Reference Card

| I need to... | Use |
|--------------|-----|
| Check if I can stop yet | finish-work |
| Debug a failure | systematic-debugging |
| Get unstuck | troubleshoot-and-continue |
| Execute a plan in this session | subagent-driven-development |
| Execute a plan in new session | executing-plans |
| Do complex multi-step work | /longplan |
| Generate batch assets | /ralph |
| Request code review | requesting-code-review |
| Review a PR | receiving-code-review |
| Create implementation plan | writing-plans |
| Finish and document | /finish |
| Merge/PR a branch | finishing-a-development-branch |

---

**Remember:** When in doubt, start with the most specific skill for your task. Skills can be combined sequentially.
