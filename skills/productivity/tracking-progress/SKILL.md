---
name: tracking-progress
description: Use this skill when check project progress, show context, and route to next action (execute or plan). Triggers include "progress".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
---

<user_command>/kata:check-progress</user_command>


<objective>
Check project progress, summarize recent work and what's ahead, then intelligently route to the next action - either executing an existing plan or creating the next one.

Provides situational awareness before continuing work.
</objective>


<process>

<step name="verify">
**Verify planning structure exists:**

Use Bash (not Glob) to check—Glob respects .gitignore but .planning/ is often gitignored:

```bash
test -d .planning && echo "exists" || echo "missing"
```

If no `.planning/` directory:

```
No planning structure found.

Run /kata:new-project to start a new project.
```

Exit.

If missing STATE.md: suggest `/kata:new-project`.

**If ROADMAP.md missing but PROJECT.md exists:**

This means a milestone was completed and archived. Go to **Route F** (between milestones).

If missing both ROADMAP.md and PROJECT.md: suggest `/kata:new-project`.
</step>

<step name="load">
**Load full project context:**

- Read `.planning/STATE.md` for living memory (position, decisions, issues)
- Read `.planning/ROADMAP.md` for phase structure and objectives
- Read `.planning/PROJECT.md` for current state (What This Is, Core Value, Requirements)
- Read `.planning/config.json` for settings (model_profile, workflow toggles)

**Load PR workflow config:**

```bash
PR_WORKFLOW=$(cat .planning/config.json 2>/dev/null | grep -o '"pr_workflow"[[:space:]]*:[[:space:]]*[^,}]*' | grep -o 'true\|false' || echo "false")
```
  </step>

<step name="recent">
**Gather recent work context:**

- Find the 2-3 most recent SUMMARY.md files
- Extract from each: what was accomplished, key decisions, any issues logged
- This shows "what we've been working on"
  </step>

<step name="position">
**Parse current position:**

- From STATE.md: current phase, plan number, status
- Calculate: total plans, completed plans, remaining plans
- Note any blockers or concerns
- Check for CONTEXT.md: For phases without PLAN.md files, check if `{phase}-CONTEXT.md` exists in phase directory
- Count pending todos: `ls .planning/todos/pending/*.md 2>/dev/null | wc -l`
- Check for active debug sessions: `ls .planning/debug/*.md 2>/dev/null | grep -v resolved | wc -l`
  </step>

<step name="report">
**Present rich status report:**

```
# [Project Name]

**Progress:** [████████░░] 8/10 plans complete
**Profile:** [quality/balanced/budget]

## Recent Work
- [Phase X, Plan Y]: [what was accomplished - 1 line]
- [Phase X, Plan Z]: [what was accomplished - 1 line]

## Current Position
Phase [N] of [total]: [phase-name]
Plan [M] of [phase-total]: [status]
CONTEXT: [✓ if CONTEXT.md exists | - if not]

## Key Decisions Made
- [decision 1 from STATE.md]
- [decision 2]

## Blockers/Concerns
- [any blockers or concerns from STATE.md]

## Pending Todos
- [count] pending — /kata:check-todoss to review

## Active Debug Sessions
- [count] active — /kata:debug-issue to continue
(Only show this section if count > 0)

## PR Status
(Only show this section if PR_WORKFLOW is true)

Check for PR on current branch:

```bash
if [ "$PR_WORKFLOW" = "true" ]; then
  CURRENT_BRANCH=$(git branch --show-current)
  PR_INFO=$(gh pr list --head "$CURRENT_BRANCH" --json number,state,title,url --jq '.[0]' 2>/dev/null)

  if [ -n "$PR_INFO" ] && [ "$PR_INFO" != "null" ]; then
    PR_NUMBER=$(echo "$PR_INFO" | jq -r '.number')
    PR_STATE=$(echo "$PR_INFO" | jq -r '.state')
    PR_TITLE=$(echo "$PR_INFO" | jq -r '.title')
    PR_URL=$(echo "$PR_INFO" | jq -r '.url')

    # Check if draft
    if [ "$PR_STATE" = "OPEN" ]; then
      IS_DRAFT=$(gh pr view "$PR_NUMBER" --json isDraft --jq '.isDraft' 2>/dev/null)
      if [ "$IS_DRAFT" = "true" ]; then
        STATE_DISPLAY="Draft"
      else
        STATE_DISPLAY="Ready for review"
      fi
    elif [ "$PR_STATE" = "MERGED" ]; then
      STATE_DISPLAY="Merged"
    elif [ "$PR_STATE" = "CLOSED" ]; then
      STATE_DISPLAY="Closed"
    else
      STATE_DISPLAY="$PR_STATE"
    fi
  fi
fi
```

**If PR exists:**
```
## PR Status

PR #[number]: [title]
Status: [Draft | Ready for review | Merged]
URL: [url]
```

**If no PR exists:**
```
## PR Status

No open PR for current branch.
Branch: [current_branch]
```

## What's Next
[Next phase/plan objective from ROADMAP]
```

</step>

<step name="route">
**Determine next action based on verified counts.**

**Step 1: Count plans, summaries, and issues in current phase**

List files in the current phase directory:

```bash
ls -1 .planning/phases/[current-phase-dir]/*-PLAN.md 2>/dev/null | wc -l
ls -1 .planning/phases/[current-phase-dir]/*-SUMMARY.md 2>/dev/null | wc -l
ls -1 .planning/phases/[current-phase-dir]/*-UAT.md 2>/dev/null | wc -l
```

State: "This phase has {X} plans, {Y} summaries."

**Step 1.5: Check for unaddressed UAT gaps**

Check for UAT.md files with status "diagnosed" (has gaps needing fixes).

```bash
# Check for diagnosed UAT with gaps
grep -l "status: diagnosed" .planning/phases/[current-phase-dir]/*-UAT.md 2>/dev/null
```

Track:
- `uat_with_gaps`: UAT.md files with status "diagnosed" (gaps need fixing)

**Step 2: Route based on counts**

| Condition                       | Meaning                 | Action            |
| ------------------------------- | ----------------------- | ----------------- |
| uat_with_gaps > 0               | UAT gaps need fix plans | Go to **Route E** |
| summaries < plans               | Unexecuted plans exist  | Go to **Route A** |
| summaries = plans AND plans > 0 | Phase complete          | Go to Step 3      |
| plans = 0                       | Phase not yet planned   | Go to **Route B** |

---

**Route A: Unexecuted plan exists**

Find the first PLAN.md without matching SUMMARY.md.
Read its `<objective>` section.

```
---

## ▶ Next Up

**{phase}-{plan}: [Plan Name]** — [objective summary from PLAN.md]
{If PR_WORKFLOW is true AND PR exists: PR #[number] ([state]) — [url]}

`/kata:execute-phase {phase}`

<sub>`/clear` first → fresh context window</sub>

---
```

---

**Route B: Phase needs planning**

Check if `{phase}-CONTEXT.md` exists in phase directory.

**If CONTEXT.md exists:**

```
---

## ▶ Next Up

**Phase {N}: {Name}** — {Goal from ROADMAP.md}
<sub>✓ Context gathered, ready to plan</sub>

`/kata:plan-phase {phase-number}`

<sub>`/clear` first → fresh context window</sub>

---
```

**If CONTEXT.md does NOT exist:**

```
---

## ▶ Next Up

**Phase {N}: {Name}** — {Goal from ROADMAP.md}

`/kata:discuss-phase {phase}` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/kata:plan-phase {phase}` — skip discussion, plan directly
- `/kata:list-assumptions {phase}` — see Claude's assumptions

---
```

---

**Route E: UAT gaps need fix plans**

UAT.md exists with gaps (diagnosed issues). User needs to plan fixes.

```
---

## ⚠ UAT Gaps Found

**{phase}-UAT.md** has {N} gaps requiring fixes.

`/kata:plan-phase {phase} --gaps`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/kata:execute-phase {phase}` — execute phase plans
- `/kata:verify-work {phase}` — run more UAT testing

---
```

---

**Step 3: Check milestone status (only when phase complete)**

Read ROADMAP.md and identify:
1. Current phase number
2. All phase numbers in the current milestone section

Count total phases and identify the highest phase number.

State: "Current phase is {X}. Milestone has {N} phases (highest: {Y})."

**Route based on milestone status:**

| Condition                     | Meaning            | Action            |
| ----------------------------- | ------------------ | ----------------- |
| current phase < highest phase | More phases remain | Go to **Route C** |
| current phase = highest phase | Milestone complete | Go to **Route D** |

---

**Route C: Phase complete, more phases remain**

Read ROADMAP.md to get the next phase's name and goal.

```
---

## ✓ Phase {Z} Complete

## ▶ Next Up

{If PR_WORKFLOW is true AND PR exists:
**⚠️ Merge PR #[number] first** — [url]
Then continue with:
}
**Phase {Z+1}: {Name}** — {Goal from ROADMAP.md}

`/kata:discuss-phase {Z+1}` — gather context and clarify approach

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/kata:plan-phase {Z+1}` — skip discussion, plan directly
- `/kata:verify-work {Z}` — user acceptance test before continuing

---
```

---

**Route D: Milestone complete**

```
---

## 🎉 Milestone Complete

All {N} phases finished!

## ▶ Next Up

{If PR_WORKFLOW is true: **⚠️ Merge all phase PRs first** before completing milestone
Then continue with:
}
**Complete Milestone** — archive and prepare for next

`/kata:complete-milestone`

<sub>`/clear` first → fresh context window</sub>

---

**Also available:**
- `/kata:verify-work` — user acceptance test before completing milestone

---
```

---

**Route F: Between milestones (ROADMAP.md missing, PROJECT.md exists)**

A milestone was completed and archived. Ready to start the next milestone cycle.

Read MILESTONES.md to find the last completed milestone version.

```
---

## ✓ Milestone v{X.Y} Complete

Ready to plan the next milestone.

## ▶ Next Up

**Start Next Milestone** — questioning → research → requirements → roadmap

`/kata:new-milestone`

<sub>`/clear` first → fresh context window</sub>

---
```

</step>

<step name="edge_cases">
**Handle edge cases:**

- Phase complete but next phase not planned → offer `/kata:plan-phase [next]`
- All work complete → offer milestone completion
- Blockers present → highlight before offering to continue
- Handoff file exists → mention it, offer `/kata:resume-work`
  </step>

</process>

<success_criteria>

- [ ] Rich context provided (recent work, decisions, issues)
- [ ] Current position clear with visual progress
- [ ] What's next clearly explained
- [ ] Smart routing: /kata:execute-phase if plans exist, /kata:plan-phase if not
- [ ] User confirms before any action
- [ ] Seamless handoff to appropriate kata command
      </success_criteria>
