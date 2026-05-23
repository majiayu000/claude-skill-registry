---
name: today
description: Displays tasks and work for today with progress tracking and prioritization. Use when the user asks "what should I work on today", "show my tasks", or "/today". Pulls from the beads task system and provides a personalized, actionable digest.
---

# Today's Task Dashboard

Shows your prioritized work for today with context, dependencies, and progress tracking.

## When to Use

Activate when users:
- Ask "what should I work on today?"
- Request "show my tasks"
- Want to check their task list or project status
- Use the `/today` slash command
- Ask for a daily digest or summary

## What Gets Displayed

The skill gathers and displays:

1. **Today's Tasks** - All active tasks with status
2. **Blocked Tasks** - Tasks waiting on dependencies
3. **Progress Summary** - Completion percentage and momentum
4. **Priority Order** - Recommended work sequence
5. **Context Notes** - Task descriptions and acceptance criteria

## Display Format

### Task List Layout

```
═══════════════════════════════════════════════════════════════
  📋 TODAY'S DASHBOARD
  {date} • {task_count} tasks • {completed}/{total} complete
═══════════════════════════════════════════════════════════════

🎯 READY TO START ({ready_count})
───────────────────────────────────────────────────────────────
{task-1-priority} {task_1_title}
   {task_1_description}
   Status: {status} | Estimate: {estimate}

{task-2-priority} {task_2_title}
   {task_2_description}
   Status: {status} | Estimate: {estimate}


🔄 IN PROGRESS ({in_progress_count})
───────────────────────────────────────────────────────────────
{task-3-title}
   Progress: {progress_bar} {percent}%
   Current step: {current_step}


⏳ BLOCKED ({blocked_count})
───────────────────────────────────────────────────────────────
{task-4-title}
   Waiting on: {blocking_task}
   Status: {blocker_status}


✅ COMPLETED ({completed_count})
───────────────────────────────────────────────────────────────
{completed_tasks_summary}


📊 TODAY'S METRICS
───────────────────────────────────────────────────────────────
Completion Rate: {percent}%
Estimated Completion: {est_time}
Context Available: {context_used}% of limit
```

## Generation Process

### Step 1: Invoke Today Agent

Run the TypeScript agent to fetch and format task data:

```bash
bun run packages/agents/src/cli/agent-cli.ts today
```

The agent will:
1. Query the beads task system for all tasks
2. Filter tasks by status (pending, in_progress, completed, blocked)
3. Determine task priority based on:
   - Dependencies (blockedBy, blocks)
   - Priority field (if set)
   - Estimated complexity
4. Generate a markdown digest with prioritized recommendations
5. Output context metrics for awareness

**Example output:**
```
📋 TODAY'S DASHBOARD
2026-01-26 • 8 tasks • 3/8 complete (38%)

🎯 READY TO START (3)
───────────────────────────────────────
⭐ Fix authentication bug in login flow
   Critical vulnerability allowing bypass. Acceptance: no
   /auth endpoints allow unauthenticated POST
   Status: pending | Estimate: 1-2 hours

🎯 Update database schema migration
   Add support for new user preferences table
   Status: pending | Estimate: 30 min

🔄 IN PROGRESS (2)
───────────────────────────────────────
🏃 Implement new blog feature
   Progress: ████████░░ 80%
   Current: Writing tests

⏳ BLOCKED (1)
───────────────────────────────────────
⏸️ Deploy to production
   Waiting on: Fix authentication bug (pending)
```

### Step 2: Present the Digest

After agent output, present:

1. **Task digest** - Formatted list with priorities
2. **Quick actions** - Suggested next steps:
   ```bash
   Start work: bd update <task-id> --status=in_progress
   Mark done: bd update <task-id> --status=completed
   View details: bd show <task-id>
   Create task: bd create
   ```
3. **Context reminder** - Time-box estimate and context headroom

### Step 3: Interactive Suggestions

Offer next steps based on task state:

**If tasks are blocked:**
```
Some tasks are waiting on dependencies. Would you like to:
1. Focus on unblocked work first
2. Check blocker status
3. Escalate blockers to get them moving
```

**If many tasks completed:**
```
You've made great progress (70% complete)! Consider:
1. Taking a break
2. Reviewing completed work
3. Planning for tomorrow
```

**If high priority tasks pending:**
```
You have 2 critical tasks waiting. Recommended priority:
1. Fix authentication bug (1-2 hours) - unblocks deployment
2. Update schema (30 min) - prerequisite for feature
3. Implement feature (2-3 hours) - depends on above
```

## Optional Parameters

### Filter by Status

Show only specific task statuses:

```bash
bun run packages/agents/src/cli/agent-cli.ts today --status=in_progress
bun run packages/agents/src/cli/agent-cli.ts today --status=ready
```

### Filter by Priority

Show only high-priority tasks:

```bash
bun run packages/agents/src/cli/agent-cli.ts today --priority=critical,high
```

### Custom Date

Show tasks for a different date:

```bash
bun run packages/agents/src/cli/agent-cli.ts today --date=2026-01-27
```

## Task Workflow Integration

After showing today's digest, help with task management:

**Starting work:**
- User picks a task
- Run `bd update <task-id> --status=in_progress`
- Ask if they need task details or context

**Reporting progress:**
- Remind user can update status anytime: `bd update <id> --status=...`
- Offer to check for newly unblocked tasks
- Suggest taking a screenshot/snapshot of progress

**Completing work:**
- Prompt to mark complete: `bd update <task-id> --status=completed`
- Check if any previously blocked tasks are now ready
- Suggest creating a follow-up task if needed

## Voice and Tone

- **Energetic and encouraging** - Help user see momentum
- **Clear priorities** - Remove ambiguity about what matters today
- **Dependency-aware** - Highlight blockers and unblock paths
- **Progress-focused** - Celebrate completed work
- **Realistic estimates** - Under-promise, over-deliver

## File Locations

| Resource | Path |
|----------|------|
| Task system | `.beads/issues.jsonl` |
| Task schema | `.beads/schema.json` |
| Today Agent | `packages/agents/src/cli/agent-cli.ts` |
| Beads CLI | `gt` / `bd` commands |
| Config | `.beads/.local_version` |

## Example Interactions

**User:** What should I work on today?

**Assistant:** Let me pull up your task dashboard for today.

```bash
bun run packages/agents/src/cli/agent-cli.ts today
```

```
📋 TODAY'S DASHBOARD
2026-01-26 • 5 tasks • 2/5 complete (40%)

🎯 READY TO START (2)
───────────────────────────────────────
⭐ Review and merge PR #42
   Waiting for your review before merge. All checks pass.
   Status: pending | Estimate: 15 min

🎯 Fix typo in documentation
   Three instances in README and guides
   Status: pending | Estimate: 5 min

🔄 IN PROGRESS (1)
───────────────────────────────────────
🏃 Implement new API endpoint
   Progress: ██████░░░░ 60%
   Current: Writing unit tests

✅ COMPLETED (2)
───────────────────────────────────────
✓ Set up database fixtures
✓ Create test user seed data

📊 TODAY'S METRICS
───────────────────────────────────────
Completion Rate: 40%
Momentum: Good (2 completed this morning)
Context Available: 65% of limit
```

**Recommended priority:**
1. **Finish API endpoint** (in progress - 30 min remaining) - highest momentum
2. **Review PR #42** (15 min) - unblocks deployment
3. **Documentation typo** (5 min) - quick win

Would you like to continue with the API tests, or switch to reviewing the PR?

---

**User:** Show only my blocked tasks.

**Assistant:**
```bash
bun run packages/agents/src/cli/agent-cli.ts today --status=blocked
```

You don't have any blocked tasks right now! All your work is either ready to start or already in progress. That's great momentum.

Ready to jump into something? Your highest priority unstarted task is "Review PR #42" (15 min estimate).

---

**User:** I just finished the API endpoint. What's next?

**Assistant:** Excellent! Let me update your task status and show what's next.

```bash
bd update <task-id> --status=completed
bun run packages/agents/src/cli/agent-cli.ts today
```

Congratulations on finishing the API endpoint! You're now at 60% complete for today (3/5 tasks).

**Next recommended:** Review PR #42 (15 min)
This unblocks the deployment and is critical path. Then the quick documentation fix.

Want to start the PR review now?
