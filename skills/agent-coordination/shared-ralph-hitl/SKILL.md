---
name: ralph-hitl
description: Single Ralph iteration with full visibility - learn before going AFK
category: orchestration
---

# Ralph HITL (Human-In-The-Loop) Mode

You are running a **single iteration** of Ralph with full visibility. This is for learning Ralph's behavior and refining your prompt before going AFK.

**Why HITL First?**

- Learn how Ralph operates before trusting it with autonomous mode
- Refine your prompt based on what you observe
- Build confidence in the system
- Catch issues early before they compound in AFK mode

**HITL vs AFK:**

- **HITL** (this mode): You watch, intervene when needed, learn the system
- **AFK** (autonomous): Set max iterations, walk away, review commits later

---

## Your Process

Work through **ONE task** from `prd.json`, showing me everything:

### Step 1: Review Progress & PRD (Show Me)

**First, read `progress.txt`** to understand what's already been done. This is how Ralph avoids expensive re-exploration.

Then:

- Read `prd.json`
- Tell me which task you selected and **WHY** (explain your priority reasoning)
- Show me the task's acceptance criteria
- Ask if I agree with the choice

**Priority Order:** architectural > integration > spike/unknown > functional > polish

- Explain why you chose this task over others
- Check dependencies are met

### Step 2: Explore (Show Me)

- Tell me which files you'll read
- Show me what patterns you're following from existing code
- Ask if I want you to consider anything else

### Step 3: Implement (Show Me)

- Make **small, focused changes** - one logical thing at a time
- Write the code with visibility
- Explain your decisions as you go
- Show me exactly what you're changing

### Step 4: Validate - ALL Feedback Loops (Show Me)

**Run ALL feedback loops before committing:**

- `npm run type-check` - Must pass with no errors
- `npm run lint` - Must pass with zero warnings
- `npm run test` - All tests must pass
- `npm run build` - Production build must succeed

**DO NOT commit if any fail.** Show me the errors and ask how to proceed.

### Step 5: Propose Commit (Wait for Approval)

- Show me the exact commit message
- Show me the files that changed (git diff)
- **WAIT for my approval before committing**

Commit format:

```
[ralph] feat-XXX: Brief description

- Change 1
- Change 2

PRD: feat-XXX | Iteration: N
```

### Step 6: Update State

- Update `prd.json` to mark `passes: true` for this task
- Append to `progress.txt` with:
  - Task completed and PRD item reference
  - Key decisions made and reasoning
  - Any blockers or notes for next iteration
- **STOP here** - do NOT continue to next task

---

## Important

- **Do NOT loop** - this is ONE iteration only for learning
- **Show everything** - I want to see your thought process
- **Wait for approval** - don't commit without my say-so
- **Answer questions** - explain why you're doing things
- **Quality over speed** - small steps compound into big progress

---

## What to Watch For

While observing Ralph, note:

- Does it pick the right task priority?
- Are the commits focused or too large?
- Do feedback loops catch issues?
- Is the code quality what you expect?

Use these observations to refine your prompt for AFK mode.

---

## Transitioning to AFK

Once you're comfortable with Ralph's behavior:

1. Refine your prompt based on HITL observations
2. Set a modest max iterations (10-20) for first AFK run
3. Review commits when you return
4. Iterate on your prompt

Begin by reading `progress.txt` (if it exists) and `prd.json`, then show me what tasks are available.
