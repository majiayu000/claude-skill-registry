---
name: exploration-plan
description: "Structure work into plans and Beads. Three modes: plan from brainstorm, plan from scratch, or create Beads from existing plan."
---

# /exploration-plan - Planning & Beads Creation

Turn ideas into executable plans, and plans into Beads. This skill handles the full journey from exploration to tracked work items.

## The Process

1. **Ask which mode** - Use AskUserQuestion with the three options
2. **Execute the selected mode**
3. **After creating plan.md** - Always offer to create Beads

## Mode Selection

```
Which planning mode?
  • Plan from brainstorm  → reads ideas/<topic>/spec.md
  • Plan from scratch     → start with just an idea
  • Create Beads from plan → reads planned/<topic>/plan.md
```

---

## Mode 1: Plan from Brainstorm

**Input:** `exploration/ideas/YYYY-MM-DD-<topic>/spec.md`
**Output:** `plan.md` in same folder, then move to `planned/`

### Steps

1. **List available explorations** in `exploration/ideas/`
2. **Confirm selection** with user
3. **Read spec.md** - Form your own view first
   - *Fallback:* If `spec.md` not found, check for legacy `exploration.md`
4. **Ask to convene council** - "Ready to send planning agents?"
5. **Spawn council** - 3 agents analyze in parallel (see Council section)
6. **Synthesize** - Combine your analysis + council input
7. **Present for approval** - Feature structure, sequence, implementation approach
8. **Write plan.md** - In the same folder
9. **Move folder** - `ideas/<topic>/` → `planned/<topic>/`
10. **Offer Beads** - "Create these as Beads now?"

If user says yes to Beads, execute Mode 3.

---

## Mode 2: Plan from Scratch

**Input:** User describes idea
**Output:** `planned/YYYY-MM-DD-<topic>/plan.md`

### Steps

1. **Discuss the idea** - Ask clarifying questions (use AskUserQuestion)
2. **Ask to convene council** - Same as Mode 1
3. **Spawn council** - 3 agents analyze in parallel
4. **Synthesize** - Combine your analysis + council input
5. **Present for approval** - Feature structure, sequence, implementation approach
6. **Create folder** - `exploration/planned/YYYY-MM-DD-<topic>/`
7. **Write plan.md** - No exploration.md (that's fine)
8. **Offer Beads** - "Create these as Beads now?"

If user says yes to Beads, execute Mode 3.

---

## Mode 3: Create Beads from Plan

**Input:** `exploration/planned/YYYY-MM-DD-<topic>/plan.md`
**Output:** Beads (feature + tasks), move folder to `mission/staged/`

### Steps

1. **List available plans** in `exploration/planned/`
2. **Confirm selection** with user
3. **Read plan.md** - Parse the feature and tasks
4. **Show what will be created** - List feature name + task names
5. **Create Beads:**
   ```bash
   # Get active epic
   EPIC_ID=$(bd list -t epic --status open --json | jq -r '.[0].id')

   # Create feature under epic
   bd create "Feature title" -t feature --parent "$EPIC_ID" -p 2

   # Get the feature ID just created
   FEATURE_ID=$(bd list -t feature --status open --json | jq -r '.[-1].id')

   # Create tasks under feature with descriptions from plan.md
   bd create "Task 1" -t task --parent "$FEATURE_ID" -p 1 -d "$(cat <<'EOF'
   **Goal:** [One sentence goal from plan]

   **Files:**
   - [file list from plan]

   **Steps:**
   1. [steps from plan]
   EOF
   )"

   bd create "Task 2" -t task --parent "$FEATURE_ID" -p 2 -d "$(cat <<'EOF'
   **Goal:** [One sentence goal from plan]

   **Files:**
   - [file list from plan]

   **Steps:**
   1. [steps from plan]
   EOF
   )"

   # Set up dependencies if specified in plan
   bd dep add <task-id> <depends-on-id>

   bd sync
   ```

   **Description format:** Extract from each `### Task:` section in plan.md:
   - `**Goal:**` from task's Goal line
   - `**Files:**` from task's Files line
   - `**Steps:**` from task's Steps list
6. **Rename and move folder** - Use the feature number (e.g., `1.5` from `space-agents-1.5`) instead of the date: `planned/YYYY-MM-DD-<topic>/` → `mission/staged/<feature-num>-<topic>/`
7. **Confirm** - "Feature ready. Run `/mission` to begin execution."

---

## The Council

Advisors, not decision makers. HOUSTON synthesizes and can override.

- `space-agents:plan-task-planner` - Breaks feature into tasks
- `space-agents:plan-sequencer` - Analyzes dependencies, execution order
- `space-agents:plan-implementer` - Creates TDD task breakdown per task

Spawn all 3 in parallel with `run_in_background: true`. Continue conversation while they work.

---

## plan.md Structure

Use explicit hierarchy that maps to Beads:

```markdown
# Feature: [Feature Name]

**Goal:** [One sentence description]

## Overview

[Context, motivation, what this achieves]

## Tasks

### Task: [Task 1 Name]

**Goal:** [One sentence]
**Files:** [Create/Modify/Test]
**Depends on:** [None or other task names]

**Steps:**
1. [Step description]
2. [Step description]

### Task: [Task 2 Name]

**Goal:** [One sentence]
**Files:** [Create/Modify/Test]
**Depends on:** Task 1 Name

**Steps:**
1. [Step description]
2. [Step description]

## Sequence

1. Task 1 (no dependencies)
2. Task 2 (depends on Task 1)
3. Task 3 (can run parallel with Task 2)

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

**Parsing rules:**
- `# Feature:` → Creates Beads feature
- `### Task:` → Creates Beads task
- `**Depends on:**` → Sets up `bd dep add`

---

## Folder Lifecycle

```
exploration/
  ideas/       ← /brainstorm creates spec.md here
  planned/     ← /plan creates plan.md, moves from ideas/

mission/
  staged/      ← /plan creates Beads, moves from exploration/planned/
  complete/    ← /land moves here when feature closes
```

---

## Remember

- Always use AskUserQuestion for mode selection and approvals
- Council are advisors - synthesize their input, don't just accept it
- After writing plan.md, always offer to create Beads
- Move folders at each transition
- Beads auto-generates IDs
