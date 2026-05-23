---
name: pm-organization-task-selection
description: Priority algorithm for selecting next PRD task based on category, dependencies, and risk
category: organization
---

# Task Selection Skill

> "Fail fast on risky work – tackle hard problems before easy wins."

## Parallel Task Opportunity Check (MANDATORY FIRST STEP)

**⚠️ CRITICAL: BEFORE selecting any single task, ALWAYS check if parallel assignment is possible.**

When both Developer AND Tech Artist are idle, the PM MUST check for parallel work opportunities. This happens BEFORE the standard single-task selection flow.

### Check Steps

```javascript
// 1. Read both PRD files for complete picture
const prd = readJson('prd.json');
const backlog = readJson(prd.backlogFile || 'prd_backlog.json');
const allItems = [...prd.items, ...backlog.backlogItems];

// 2. Check if BOTH agents are idle
const developerIdle =
  prd.agents.developer?.status === 'idle' || prd.agents.developer?.status === 'awaiting_pm';
const techartistIdle =
  prd.agents.techartist?.status === 'idle' || prd.agents.techartist?.status === 'awaiting_pm';

// 3. If both idle, find tasks for each agent
if (developerIdle && techartistIdle) {
  // Find Developer task (architectural, functional, integration categories)
  const devCategories = ['architectural', 'functional', 'integration'];
  const devTasks = allItems
    .filter(
      (item) =>
        !item.passes &&
        item.status === 'pending' &&
        devCategories.includes(item.category) &&
        item.dependencies.every((depId) => allItems.find((i) => i.id === depId)?.passes === true)
    )
    .sort(priorityComparator);

  // Find Tech Artist task (visual, shader, polish categories)
  const artistCategories = ['visual', 'shader', 'polish'];
  const artistTasks = allItems
    .filter(
      (item) =>
        !item.passes &&
        item.status === 'pending' &&
        artistCategories.includes(item.category) &&
        item.dependencies.every((depId) => allItems.find((i) => i.id === depId)?.passes === true)
    )
    .sort(priorityComparator);

  // 4. Check if we have non-conflicting tasks
  if (devTasks.length > 0 && artistTasks.length > 0) {
    const devTask = devTasks[0];
    const artistTask = artistTasks[0];

    // Check for file path conflicts
    if (!areTasksConflicting(devTask, artistTask)) {
      // ⭐ PARALLEL ASSIGNMENT PATH ⭐
      // Assign BOTH tasks in parallel using 5-step atomic process for each
      assignTask(devTask, 'developer');
      assignTask(artistTask, 'techartist');
      return 'parallel_assigned'; // Exit after parallel assignment
    }
  }
}

// 5. Fall through to single-task selection if no parallel opportunity
```

### Conflict Detection Function

```javascript
function areTasksConflicting(task1, task2) {
  // Direct file overlap check
  const paths1 = task1.files || [];
  const paths2 = task2.files || [];

  // Check if any file paths overlap
  for (const p1 of paths1) {
    for (const p2 of paths2) {
      // Extract directory paths
      const dir1 = p1.substring(0, p1.lastIndexOf('/'));
      const dir2 = p2.substring(0, p2.lastIndexOf('/'));
      if (dir1 === dir2) return true; // Same directory = conflict
    }
  }

  // Check shared dependencies
  const deps1 = new Set(task1.dependencies || []);
  const deps2 = new Set(task2.dependencies || []);
  for (const dep of deps1) {
    if (deps2.has(dep)) return true; // Shared dependency = conflict
  }

  return false; // No conflicts
}
```

### When to Use This Skill

Use when:

- Assigning a new task from the PRD
- `prd.json.session.currentTask` is null or task status is "passed"
- After retrospective completes

**⚠️ FIRST check for parallel assignment, then proceed to single-task selection if parallel is not possible.**

## Quick Start

```javascript
// 1. Read both PRD files
const prd = readJson('prd.json');
const backlog = readJson('prd.backlogFile' || 'prd_backlog.json');

// 2. Combine items from both files
const allItems = [...prd.items, ...backlog.backlogItems];

// 3. Filter incomplete items
const incomplete = allItems.filter((item) => !item.passes);

// 4. Filter unblocked items (dependencies met)
const unblocked = incomplete.filter((item) =>
  item.dependencies.every((depId) => allItems.find((i) => i.id === depId)?.passes === true)
);

// 5. Sort by priority and select first
const next = unblocked.sort(priorityComparator)[0];
```

## PRD Backlog Architecture

**Since v3.1.0**, tasks are split between two files:

| File               | Contains           | Size      |
| ------------------ | ------------------ | --------- |
| `prd.json`         | Top 5 active queue | ~5 tasks  |
| `prd_backlog.json` | Remaining backlog  | ~70 tasks |

**Only PM and Game Designer need full backlog access.** Workers only read their assigned task.

### Reading Tasks from Both Files

When selecting tasks, PM must:

1. Read `prd.json` for active queue
2. Read `prd.backlogFile` (defaults to `prd_backlog.json`)
3. Combine arrays: `allItems = [...prd.items, ...backlog.backlogItems]`
4. Apply filtering/sorting on combined array
5. If selected task is in backlog, move it to `prd.json.items`

### Automatic Backlog Refill

After a task completes (status → "completed") and is removed from active queue:

```javascript
// Check if refill needed
if (prd.items.length < 5) {
  // Read backlog
  const backlog = readJson(prd.backlogFile);

  // Find highest-priority UNBLOCKED task from backlog
  const allTasks = [...prd.items, ...backlog.backlogItems];
  const candidates = backlog.backlogItems.filter((item) => {
    if (item.passes) return false;
    // Check dependencies (need to check across both files)
    const depsMet = item.dependencies.every(
      (depId) => allTasks.find((t) => t.id === depId)?.passes === true
    );
    return depsMet;
  });

  // Sort by priority tier, then by priority value
  const tierOrder = {
    TIER_0_BLOCKER: 1,
    TIER_1_FOUNDATION: 2,
    TIER_2_ECONOMY: 3,
    TIER_3_SUPPORT: 4,
  };
  candidates.sort((a, b) => {
    const tierDiff = (tierOrder[a.tier] || 99) - (tierOrder[b.tier] || 99);
    if (tierDiff !== 0) return tierDiff;
    return (
      (a.priority === 'critical' ? 1 : a.priority === 'high' ? 2 : 3) -
      (b.priority === 'critical' ? 1 : b.priority === 'high' ? 2 : 3)
    );
  });

  // Move highest priority to prd.json
  if (candidates.length > 0) {
    const toMove = candidates[0];
    // Remove from backlog
    backlog.backlogItems = backlog.backlogItems.filter((i) => i.id !== toMove.id);
    // Add to prd.json
    prd.items.push(toMove);
    // Update stats
    prd.session.stats.backlogSize = backlog.backlogItems.length;
    prd.session.stats.activeQueueSize = prd.items.length;
    // Write both files
    writeJson('prd_backlog.json', backlog);
    writeJson('prd.json', prd);
  }
}
```

## Decision Framework

| Category            | Priority    | When to Use                           |
| ------------------- | ----------- | ------------------------------------- |
| `architectural`     | 1 (Highest) | Affects entire codebase structure     |
| `integration`       | 2           | Reveals incompatibilities early       |
| `spike` / `unknown` | 3           | Exploratory work, reduces uncertainty |
| `functional`        | 4           | Standard feature implementation       |
| `polish`            | 5 (Lowest)  | UI, optimization, documentation       |

## Progressive Guide

### Level 1: Basic Selection

Select first incomplete, unblocked task (reads from both files):

```javascript
// Read both files
const prd = readJson('prd.json');
const backlog = readJson(prd.backlogFile || 'prd_backlog.json');
const allItems = [...prd.items, ...backlog.backlogItems];

const next = allItems.find(
  (item) => !item.passes && item.dependencies.every((d) => allItems.find((i) => i.id === d)?.passes)
);
```

### Level 2: Priority-Weighted Selection

Apply category priority ordering (reads from both files):

```javascript
// Read both files
const prd = readJson('prd.json');
const backlog = readJson(prd.backlogFile || 'prd_backlog.json');
const allItems = [...prd.items, ...backlog.backlogItems];

const priorityOrder = {
  architectural: 1,
  integration: 2,
  unknown: 3,
  spike: 3,
  functional: 4,
  polish: 5,
};

const priorityValue = { high: 1, medium: 2, low: 3 };

const incomplete = allItems.filter((item) => !item.passes);
const unblocked = incomplete.filter((item) =>
  item.dependencies.every((d) => allItems.find((i) => i.id === d)?.passes)
);

unblocked.sort((a, b) => {
  const catDiff = priorityOrder[a.category] - priorityOrder[b.category];
  if (catDiff !== 0) return catDiff;
  return priorityValue[a.priority] - priorityValue[b.priority];
});
```

### Level 3: Risk-Adjusted Selection

Consider retry count and complexity (reads from both files):

```javascript
// Read both files
const prd = readJson('prd.json');
const backlog = readJson(prd.backlogFile || 'prd_backlog.json');
const allItems = [...prd.items, ...backlog.backlogItems];

// Deprioritize repeatedly failing tasks
if (task.retryCount >= 3) {
  // Consider skipping or escalating
  logWarning(`Task ${task.id} failed ${task.retryCount} times`);
}

// Boost tasks that unblock many others (check across both files)
const unblockScore = allItems.filter((i) => i.dependencies.includes(task.id)).length;
```

## Anti-Patterns

❌ **DON'T:**

- Select tasks with unmet dependencies
- Assign new task while `prd.json.session.currentTask` is not null
- Skip retrospective to assign faster
- Assign multiple tasks to the SAME agent simultaneously
- Assign parallel tasks that modify the same files/directories
- **Skip backlog refill** when `prd.json.items.length < 5`
- **Only read prd.json** without checking prd_backlog.json
- **Leave completed tasks** in prd.json instead of moving to completed file

✅ **DO:**

- Verify all dependencies have `passes: true` (check across both files)
- Wait for QA validation before assigning next
- Complete retrospective before clearing `prd.json.session.currentTask`
- Log selection rationale in progress file
- **Assign parallel tasks to Developer AND Tech Artist when safe** (see Parallel Assignment below)
- **Read both prd.json and prd_backlog.json** when selecting tasks
- **Automatically refill** when active queue drops below 5 tasks
- **Move completed tasks** to prd_completed.json and refill queue

## Parallel Task Assignment (Git Worktree Support)

**With git worktrees, Developer and Tech Artist can work simultaneously on non-conflicting tasks.**

### When to Assign Parallel Tasks

Check these conditions before assigning parallel tasks:

1. **Both agents are idle:**
   - `prd.json.agents.developer.status === "idle"` (or "awaiting_pm")
   - `prd.json.agents.techartist.status === "idle"` (or "awaiting_pm")

2. **Tasks are non-conflicting:**
   - Different file paths (e.g., `src/hooks/` vs `src/assets/`)
   - No shared dependencies
   - Can be tested independently

3. **Each agent has their own worktree:**
   - Developer works in `../developer-worktree` on `developer-worktree` branch
   - Tech Artist works in `../techartist-worktree` on `techartist-worktree` branch

### Conflict Detection Matrix

| Developer Category                                  | Tech Artist Category      | File Path Overlap? | Safe for Parallel?      |
| --------------------------------------------------- | ------------------------- | ------------------ | ----------------------- |
| `architectural` (src/hooks, src/stores, src/server) | `visual` (src/assets)     | ❌ No              | ✅ Yes                  |
| `functional` (src/components/\* logic)              | `shader` (src/vfx)        | ❌ No              | ✅ Yes                  |
| `integration` (src/utils)                           | `polish` (src/styles)     | ❌ No              | ✅ Yes                  |
| `architectural` (src/components)                    | `visual` (src/components) | ⚠️ Yes             | ❌ No - sequential only |
| `functional` (public/)                              | `visual` (public/)        | ⚠️ Yes             | ❌ No - sequential only |

### Parallel Assignment Algorithm

```javascript
// Check if parallel assignment is possible
const developerIdle = prd.agents.developer?.status === 'idle';
const techartistIdle = prd.agents.techartist?.status === 'idle';

if (developerIdle && techartistIdle) {
  // Find highest priority Developer task
  const devTask = findNextTaskForAgent('developer', allItems);

  // Find highest priority Tech Artist task
  const artistTask = findNextTaskForAgent('techartist', allItems);

  // Check if tasks are non-conflicting
  if (areTasksNonConflicting(devTask, artistTask)) {
    // Assign to both agents in parallel
    assignTask(devTask, 'developer');
    assignTask(artistTask, 'techartist');
    return; // Exit after parallel assignment
  }
}

// Otherwise, assign single task to available agent
```

### File Path-Based Conflict Detection

```javascript
function areTasksNonConflicting(task1, task2) {
  // Define file path patterns for each agent
  const devPaths = [
    'src/hooks/',
    'src/stores/',
    'src/server/',
    'src/utils/',
    'src/types/',
    'test/',
  ];

  const artistPaths = [
    'src/assets/',
    'src/vfx/',
    'src/styles/',
    'public/textures/',
    'public/models/',
  ];

  // Check for overlap (simplified - in production, parse task descriptions)
  const task1Path = guessFilePathFromTask(task1);
  const task2Path = guessFilePathFromTask(task2);

  // Tasks in different directories = non-conflicting
  const task1InDev = devPaths.some((p) => task1Path?.startsWith(p));
  const task2InArtist = artistPaths.some((p) => task2Path?.startsWith(p));

  return task1InDev && task2InArtist;
}
```

### Parallel Assignment Steps

1. Check both Developer and Tech Artist are idle
2. Find highest-priority incomplete task for each agent
3. Verify tasks are non-conflicting (different file paths, no shared deps)
4. Assign to Developer (5-step atomic process)
5. Assign to Tech Artist (5-step atomic process)
6. Exit - both agents work in parallel in their worktrees

## Checklist

Before assigning a task:

- [ ] **Current task is `null`** (MUST be null, not "passed")
  - Check: `prd.json.session.currentTask === null`
- [ ] **NOT in any retrospective or playtest phase** (forbidden to assign during these phases)
  - Check: `prd.json.session.status !== "in_retrospective"`
  - Check: `prd.json.session.status !== "retrospective_synthesized"`
  - Check: `prd.json.session.status !== "playtest_phase"`
  - Check: `prd.json.session.status !== "playtest_complete"`
  - Check: `prd.json.session.status !== "prd_refinement"`
  - Check: `prd.json.session.status !== "skill_research"`
- [ ] **Previous task is "completed" status** (all phases complete)
  - Check: `prd.json.items[{previousTaskId}].status === "completed"`
- [ ] **Acceptance criteria received from Game Designer** (MANDATORY before assignment)
  - Check: `prd.json.items[{taskId}].acceptanceCriteria` exists
  - Check: `prd.json.items[{taskId}].testPlan` exists (provided by Game Designer)
  - If not exist: Send `acceptance_criteria_request` to Game Designer FIRST
- [ ] Task has all required fields (id, title, description, acceptanceCriteria, testPlan)
- [ ] All dependencies have `passes: true`
- [ ] Worker heartbeats are fresh (< 60 seconds)
  - Check: `prd.json.agents.{agent}.lastHeartbeat` within last 60s
- [ ] Selection rationale logged to progress.txt

**⚠️ CRITICAL: New Phased Workflow Must Complete Before Assignment**

When a task status is `"passed"`, the following phases MUST complete in order:

1. **Retrospective** (worker contributions only) → `retrospective_synthesized`
2. **Playtest Session** (Game Designer validates) → `playtest_complete`
3. **PRD Refinement** (optional, if needed) → `prd_refinement` or skip
4. **Acceptance Criteria** (MANDATORY - Game Designer provides) → `task_ready`
5. **Skill Research** (PM improves ALL skills) → `completed`

ONLY when status is `"completed"` may you set `prd.json.session.currentTask = null` and select the next task.

**⚠️ NEVER assign a task without acceptance criteria from Game Designer.**

---

## After Selecting a Task

**Once a task is selected, you MUST update it in the PRD before assigning:**

1. Read `prd.json`
2. Find the selected task by ID
3. Update the task with:
   ```json
   {
     "status": "assigned",
     "assignedAt": "{{ISO_TIMESTAMP}}"
   }
   ```
4. Write back to `prd.json`
5. Then update session state in `prd.json.session`:
   ```json
   {
     "session": {
       "currentTask": "{{taskId}}",
       "currentTaskStatus": "assigned",
       "lastAssignmentTime": "{{ISO_TIMESTAMP}}"
     }
   }
   ```

**⚠️ This is Step 1 of the 5-step atomic assignment process. See PM AGENT.md for complete flow.**

---

## Completed Task Cleanup (MANDATORY After Retrospective)

**⚠️ CRITICAL: After a task completes retrospective (status: "completed"), you MUST:**

1. **Move completed task to `prd_completed.json`**
2. **Remove it from `prd.json.items` array**
3. **Refill from backlog if `prd.json.items.length < 5`**

### Step-by-Step Cleanup Procedure

```javascript
// 1. Identify completed tasks
const prd = readJson('prd.json');
const completedTasks = prd.items.filter(
  (item) => item.status === 'completed' && item.passes === true
);

// 2. For each completed task, append to prd_completed.json
for (const task of completedTasks) {
  const entry = {
    id: task.id,
    title: task.title,
    category: task.category,
    tier: task.tier,
    completedAt: task.completedAt || task.qaValidatedAt,
    notes: task.notes || '',
    validationSummary: task.validationResults || 'PASSED',
  };

  // Append to completed file
  appendFileSync('prd_completed.json', JSON.stringify(entry, null, 2) + '\n\n');
}

// 3. Remove completed tasks from prd.json
prd.items = prd.items.filter((item) => !(item.status === 'completed' && item.passes === true));

// 4. Update completedTasks count
prd.completedTasks =
  parseInt(readFileSync('prd_completed.json', 'utf8').match(/"id":/g)?.length || 0) +
  completedTasks.length;

// 5. Refill from backlog if needed
if (prd.items.length < 5) {
  const backlog = readJson(prd.backlogFile || 'prd_backlog.json');

  // Find highest-priority UNBLOCKED task from backlog
  const allTasks = [...prd.items, ...backlog.backlogItems];
  const candidates = backlog.backlogItems.filter((item) => {
    if (item.passes || item.status === 'deferred') return false;
    // Check dependencies (need to check across both files)
    const depsMet =
      item.dependencies?.every((depId) => allTasks.find((t) => t.id === depId)?.passes === true) ??
      true;
    return depsMet;
  });

  // Sort by priority tier, then by priority value
  const tierOrder = {
    TIER_0_BLOCKER: 1,
    TIER_1_FOUNDATION: 2,
    TIER_2_ECONOMY: 3,
    TIER_3_SUPPORT: 4,
  };
  candidates.sort((a, b) => {
    const tierDiff = (tierOrder[a.tier] || 99) - (tierOrder[b.tier] || 99);
    if (tierDiff !== 0) return tierDiff;
    return (
      (a.priority === 'critical' ? 1 : a.priority === 'high' ? 2 : 3) -
      (b.priority === 'critical' ? 1 : b.priority === 'high' ? 2 : 3)
    );
  });

  // Move highest priority to prd.json until we have 5 items
  while (prd.items.length < 5 && candidates.length > 0) {
    const toMove = candidates.shift();
    // Remove from backlog
    backlog.backlogItems = backlog.backlogItems.filter((i) => i.id !== toMove.id);
    // Add to prd.json
    prd.items.push(toMove);
  }

  // Update backlog
  writeJson(prd.backlogFile || 'prd_backlog.json', backlog);
}

// 6. Update stats
prd.session.stats.activeQueueSize = prd.items.length;
prd.session.stats.completed = prd.completedTasks;
prd.session.stats.backlogSize = backlog.backlogItems.length;

// 7. Write updated prd.json
writeJson('prd.json', prd);
```

### Cleanup Timing

**When to run cleanup:**

- ✅ **AFTER** retrospective completes (task status = "completed", passes = true)
- ✅ **BEFORE** selecting next task (keeps prd.json clean)
- ❌ **NOT** during task assignment (too many file operations)

### Cleanup Checklist

- [ ] Task has `status: "completed"` AND `passes: true`
- [ ] Retrospective completed (`retrospectiveCompletedAt` is set)
- [ ] Task appended to `prd_completed.json`
- [ ] Task removed from `prd.json.items`
- [ ] `prd.completedTasks` count updated
- [ ] If `prd.json.items.length < 5`, refilled from backlog
- [ ] `prd.session.stats` updated

## Reference

- [pm-organization-scale-adaptive](../pm-organization-scale-adaptive/SKILL.md) — Scale-adaptive planning
- [pm-organization-task-research](../pm-organization-task-research/SKILL.md) — Codebase research before assignment
- [shared-worktree](../shared-worktree/SKILL.md) — Git worktree coordination for parallel agents
