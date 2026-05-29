---
name: progress
description: Real-time progress display during command execution with stage and task status indicators.
---

# Progress Skill

Real-time progress display during command execution with stage and task status indicators.

## When Used

| Command      | Progress Displays                                   |
| ------------ | --------------------------------------------------- |
| `/plan`      | Research → Write → Validate phases with sub-agents  |
| `/implement` | Per-stage progress with TDD phases and verification |
| `/ship`      | Commit → PR → CI → CodeRabbit stages                |

**NOT used by:** `/start` (quick operation), `/guide` (informational), `/mode` (immediate)

## Events

| Event                    | Display Update                    |
| ------------------------ | --------------------------------- |
| Command starts           | Show initial progress frame       |
| Stage starts             | Update stage status to RUNNING    |
| Sub-agent starts         | Show sub-agent with spinner       |
| Sub-agent completes      | Show checkmark and timing         |
| Sub-agent outputs result | Show summary below sub-agent      |
| Stage completes          | Update stage status, move to next |
| Command completes        | Show final summary                |
| Error occurs             | Show error inline, update status  |

## Progress Data Structure

```typescript
interface ExecutionProgress {
  // Command context
  command: string;
  startTime: Date;

  // Current state
  currentStage: number;
  totalStages: number;

  // Stages
  stages: StageProgress[];

  // Overall progress
  percentComplete: number;
  status: "running" | "completed" | "failed";
}

interface StageProgress {
  number: number;
  name: string;
  status: "pending" | "running" | "completed" | "failed";
  agent?: string;
  subAgents: SubAgentProgress[];
  startTime?: Date;
  endTime?: Date;
}

interface SubAgentProgress {
  name: string;
  model: "Opus" | "Sonnet" | "Haiku";
  status: "pending" | "running" | "completed" | "failed";
  output?: string; // Brief summary of result
  duration?: number; // Seconds
  parallel?: boolean; // True if runs in parallel
}
```

---

## Display Format

### /plan Progress

```text
┌─────────────────────────────────────────────────────────────────┐
│  /plan user-authentication                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  PHASE 1: RESEARCH                                  [COMPLETE]  │
│  ├─ ✓ domain-researcher (Opus)                      [3.2s]      │
│  │   Found: session.ts, email.ts - no conflicts                 │
│                                                                 │
│  PHASE 2: WRITE                                     [RUNNING]   │
│  ├─ ● domain-writer (Sonnet)                        [RUNNING]   │
│  │   Writing: specs/user-authentication/design.md               │
│                                                                 │
│  PHASE 3: VALIDATE                                  [PENDING]   │
│  └─ ○ quality-validator (Haiku)                                 │
│                                                                 │
│  Progress: ██████████░░░░░░░░░░ 50%                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### /implement Progress (Multi-Stage)

```text
┌─────────────────────────────────────────────────────────────────┐
│  /implement user-authentication                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STAGE 1: DATABASE SCHEMA                           [COMPLETE]  │
│  Agent: code-agent                                              │
│  ├─ ✓ code-researcher (Opus)                        [2.1s]      │
│  │   Found: Prisma schema at prisma/schema.prisma               │
│  ├─ ✓ code-writer [TDD-RED] (Sonnet)                [4.5s]      │
│  │   Wrote: 3 failing tests                                     │
│  ├─ ✓ code-writer [TDD-GREEN] (Sonnet)              [8.2s]      │
│  │   Implemented: User model + migration                        │
│  └─ ✓ code-validator (Haiku)                        [2.1s]      │
│      Tests: PASS (3/3)                                          │
│                                                                 │
│  STAGE 2: AUTH API                                  [RUNNING]   │
│  Agent: code-agent                                              │
│  ├─ ✓ code-researcher (Opus)                        [1.8s]      │
│  │   Context: Using JWT pattern from session.ts                 │
│  ├─ ● code-writer [TDD-RED] (Sonnet)                [RUNNING]   │
│  │   Writing: tests for login/register mutations                │
│  └─ ○ code-writer [TDD-GREEN] (Sonnet)              [PENDING]   │
│  └─ ○ code-validator (Haiku)                        [PENDING]   │
│                                                                 │
│  STAGE 3: UI COMPONENTS                             [PENDING]   │
│  Agent: ui-agent                                                │
│  └─ [3 sub-agents pending]                                      │
│                                                                 │
│  STAGE 4: FINAL VERIFICATION                        [PENDING]   │
│  Agent: check-agent (parallel)                                  │
│  └─ [5 checkers pending]                                        │
│                                                                 │
│  Progress: ████████░░░░░░░░░░░░ 40%                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### /ship Progress

```text
┌─────────────────────────────────────────────────────────────────┐
│  /ship                                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  STAGE 1: COMMIT                                    [COMPLETE]  │
│  ├─ ✓ change-analyzer (Sonnet)                      [2.3s]      │
│  │   Message: "feat: add user authentication"                   │
│  └─ ✓ git-executor (Haiku)                          [0.5s]      │
│      Commit: abc1234                                            │
│                                                                 │
│  STAGE 2: CREATE PR                                 [COMPLETE]  │
│  ├─ ✓ pr-analyzer (Sonnet)                          [3.1s]      │
│  │   Title: "feat: add user authentication"                     │
│  └─ ✓ git-executor (Haiku)                          [1.2s]      │
│      PR: #42 created                                            │
│                                                                 │
│  STAGE 3: WAIT FOR CI                               [RUNNING]   │
│  ├─ ● Polling GitHub Actions...                     [45s]       │
│  │   Status: Tests running (3/5 jobs complete)                  │
│                                                                 │
│  STAGE 4: WAIT FOR CODERABBIT                       [PENDING]   │
│  └─ ○ Waiting for CI to complete first...                       │
│                                                                 │
│  Progress: ██████████████░░░░░░ 70%                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Final Verification Progress (Parallel)

```text
┌─────────────────────────────────────────────────────────────────┐
│  STAGE 4: FINAL VERIFICATION                        [RUNNING]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Agent: check-agent (parallel)                                  │
│  ├─ ✓ build-checker (Haiku)                         [8.2s]      │
│  │   Build: SUCCESS (no errors)                                 │
│  ├─ ✓ type-checker (Haiku)                          [3.1s]      │
│  │   Types: PASS (0 errors)                                     │
│  ├─ ● lint-checker (Haiku)                          [RUNNING]   │
│  │   Checking: 47 files...                                      │
│  ├─ ● test-runner (Haiku)                           [RUNNING]   │
│  │   Running: 23/47 tests...                                    │
│  └─ ○ security-scanner (Haiku)                      [PENDING]   │
│                                                                 │
│  ⊕ = runs in parallel                                           │
│                                                                 │
│  Progress: ████████████░░░░░░░░ 60%                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Status Indicators

### Visual Symbols

| Symbol | Meaning   | Description                     |
| ------ | --------- | ------------------------------- |
| `○`    | Pending   | Not yet started                 |
| `●`    | Running   | Currently executing             |
| `✓`    | Completed | Finished successfully           |
| `✗`    | Failed    | Finished with error             |
| `⊕`    | Parallel  | Running in parallel with others |

### Status Colors (Terminal)

| Status    | Color  | ANSI Code  |
| --------- | ------ | ---------- |
| Pending   | Gray   | `\x1b[90m` |
| Running   | Yellow | `\x1b[33m` |
| Completed | Green  | `\x1b[32m` |
| Failed    | Red    | `\x1b[31m` |

### Stage Status Tags

| Tag           | Meaning                     |
| ------------- | --------------------------- |
| `[PENDING]`   | Stage not started           |
| `[RUNNING]`   | Stage currently executing   |
| `[COMPLETED]` | Stage finished successfully |
| `[FAILED]`    | Stage finished with error   |

---

## Progress Bar

### Calculation

```typescript
function calculateProgress(stages: StageProgress[]): number {
  // Bounds check: ensure stages array is non-empty
  if (!stages || stages.length === 0) {
    return 0;
  }

  const weights = stages.map((stage) => {
    // Weight by sub-agent count
    return stage.subAgents.length;
  });

  const totalWeight = weights.reduce((a, b) => a + b, 0);

  // Division by zero guard: if no sub-agents across all stages
  if (totalWeight === 0) {
    return 0;
  }

  let completedWeight = 0;
  stages.forEach((stage, i) => {
    const stageWeight = weights[i];
    const completedSubAgents = stage.subAgents.filter(
      (sa) => sa.status === "completed"
    ).length;
    const runningSubAgents = stage.subAgents.filter(
      (sa) => sa.status === "running"
    ).length;

    // Division by zero guard: only calculate if stage has sub-agents
    if (stage.subAgents.length > 0) {
      // Completed sub-agents count fully
      completedWeight +=
        (completedSubAgents / stage.subAgents.length) * stageWeight;
      // Running sub-agents count as 50%
      completedWeight +=
        (runningSubAgents / stage.subAgents.length) * stageWeight * 0.5;
    }
  });

  return Math.round((completedWeight / totalWeight) * 100);
}
```

### Visual Representation

```text
Progress: ████████████░░░░░░░░ 60%
          │          │        │
          └─ Filled  │        └─ Percentage
                     └─ Empty
```

Width: 20 characters for bar + 5 for percentage

---

## Real-Time Updates

### Update Mechanism

```typescript
interface ProgressUpdate {
  type:
    | "stage_start"
    | "subagent_start"
    | "subagent_complete"
    | "subagent_output"
    | "stage_complete"
    | "error";
  stageIndex: number;
  subAgentIndex?: number;
  data: {
    output?: string;
    duration?: number;
    error?: string;
  };
}

function applyUpdate(
  progress: ExecutionProgress,
  update: ProgressUpdate
): ExecutionProgress {
  const newProgress = { ...progress };

  // Bounds check: validate stageIndex is within valid range
  if (update.stageIndex < 0 || update.stageIndex >= newProgress.stages.length) {
    // Invalid stage index, return progress unchanged
    return newProgress;
  }

  const stage = newProgress.stages[update.stageIndex];

  switch (update.type) {
    case "stage_start":
      stage.status = "running";
      stage.startTime = new Date();
      break;

    case "subagent_start":
      if (
        update.subAgentIndex !== undefined &&
        update.subAgentIndex >= 0 &&
        update.subAgentIndex < stage.subAgents.length
      ) {
        stage.subAgents[update.subAgentIndex].status = "running";
      }
      break;

    case "subagent_complete":
      if (
        update.subAgentIndex !== undefined &&
        update.subAgentIndex >= 0 &&
        update.subAgentIndex < stage.subAgents.length
      ) {
        const subAgent = stage.subAgents[update.subAgentIndex];
        subAgent.status = "completed";
        subAgent.duration = update.data.duration;
        subAgent.output = update.data.output;
      }
      break;

    case "stage_complete":
      stage.status = "completed";
      stage.endTime = new Date();
      // Bounds check: ensure currentStage doesn't exceed total stages
      if (newProgress.currentStage < newProgress.stages.length - 1) {
        newProgress.currentStage++;
      }
      break;

    case "error":
      if (
        update.subAgentIndex !== undefined &&
        update.subAgentIndex >= 0 &&
        update.subAgentIndex < stage.subAgents.length
      ) {
        stage.subAgents[update.subAgentIndex].status = "failed";
      }
      stage.status = "failed";
      break;
  }

  newProgress.percentComplete = calculateProgress(newProgress.stages);
  return newProgress;
}
```

### Refresh Rate

| Scenario           | Refresh Rate |
| ------------------ | ------------ |
| Sub-agent running  | 500ms        |
| Waiting for result | 1000ms       |
| Parallel execution | 250ms        |
| Error state        | Immediate    |

---

## Sub-Agent Output Display

### Output Formatting

Summarize sub-agent outputs to fit single line:

```typescript
function formatOutput(output: string, maxLength: number = 60): string {
  // Remove newlines
  const clean = output.replace(/\n/g, " ").trim();

  // Truncate if needed
  if (clean.length > maxLength) {
    return clean.substring(0, maxLength - 3) + "...";
  }

  return clean;
}
```

### Output Examples

| Sub-Agent    | Raw Output                               | Displayed                                 |
| ------------ | ---------------------------------------- | ----------------------------------------- |
| researcher   | `Found 3 related files...`               | `Found: 3 related files in src/lib/`      |
| writer       | `Created LoginForm.tsx...`               | `Writing: src/components/LoginForm.tsx`   |
| validator    | `Tests passed: 12/12, coverage: 82%`     | `Tests: PASS (12/12, 82% coverage)`       |
| investigator | `Root cause identified in middleware...` | `Root cause: Middleware session handling` |

---

## Completion Display

### Success

```text
┌─────────────────────────────────────────────────────────────────┐
│  /implement login form                                [COMPLETED]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✓ All stages completed successfully                            │
│                                                                 │
│  Summary:                                                       │
│  ├─ Files created: 3                                            │
│  │   • src/components/LoginForm.tsx                             │
│  │   • src/components/LoginForm.test.tsx                        │
│  │   • src/lib/validation.ts                                    │
│  ├─ Tests: 8 passing                                            │
│  ├─ Coverage: 85%                                               │
│  └─ Duration: 45.2s                                             │
│                                                                 │
│  Next: /ship                                           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Failure

```text
┌─────────────────────────────────────────────────────────────────┐
│  /implement login form                                   [FAILED]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ✗ Stage 2 (BUILD) failed                                       │
│                                                                 │
│  Error:                                                         │
│  ├─ Sub-agent: ui-validator                                     │
│  ├─ Reason: TypeScript error in LoginForm.tsx                   │
│  └─ Details:                                                    │
│      Type 'string' is not assignable to type 'number'           │
│      at line 42, column 15                                      │
│                                                                 │
│  Partial Progress:                                              │
│  ├─ ✓ ui-researcher completed                                   │
│  ├─ ✓ ui-builder completed                                      │
│  └─ ✗ ui-validator failed                                       │
│                                                                 │
│  Recovery: Fix type error and run /implement login form again       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Error Handling

| Scenario                | Display Behavior                   |
| ----------------------- | ---------------------------------- |
| Sub-agent timeout       | Show timeout error, mark as failed |
| Sub-agent crash         | Show error message, mark as failed |
| Network error           | Show retry message, attempt retry  |
| User interrupt (Ctrl+C) | Show interrupted message, clean up |
| Partial completion      | Show what completed, what remains  |

---

## Timing Display

### Format

| Duration     | Display   |
| ------------ | --------- |
| < 1 second   | `[0.Xs]`  |
| 1-59 seconds | `[Xs]`    |
| 1-59 minutes | `[Xm Ys]` |
| 1+ hours     | `[Xh Ym]` |

### Examples

```text
[0.3s]   # 300 milliseconds
[2.1s]   # 2.1 seconds
[45s]    # 45 seconds
[1m 23s] # 1 minute 23 seconds
[5m 0s]  # 5 minutes
```
