---
name: execution-phase
description: TDD-paired Gantt-style execution with compact waves. Each story gets tester agent (writes tests) BEFORE implementation agent (passes tests). Waves execute continuously with /compact between each wave. Respects dependencies, spawns up to 10 concurrent agents. Use when orchestrating parallel implementation workflows with test-first discipline.
---

# Execution Phase - TDD-Paired Domain Worker Orchestration

> **ROOT AGENT ONLY** - Called by commands only, never by subagents.

**Purpose:** Execute implementation tasks via TDD-paired domain worker agents
**Trigger:** After design-phase completes
**Input:** Execution plan with task dependencies, wave batching
**Output:** Collection of all worker outputs with test coverage

---

## Core Principle

**The orchestrator spawns agents and tracks progress. All implementation happens inside spawned agents.**

The execution phase orchestrates parallel work through agent spawning and state management. The orchestrator ALWAYS spawns domain workers (tester and coder agents) to perform implementation. The orchestrator NEVER writes implementation code directly—it coordinates, tracks progress, and manages state across waves.

---

## Workflow Steps

### Wave-Based Execution with TDD Pairing

1. **Load execution plan** from design-phase (tasks + dependencies + story files, grouped into waves)

2. **For each wave:**

   a. **Update workflow state:** Use `/skill state-management` to track wave progress

   ```javascript
   updateWorkflowState(projectFolder, {
     currentWave: waveNumber,
     status: "executing",
     stories: {
       ...state.stories,
       inProgress: waveStoryIds,
     },
   });
   ```

   b. **Persist progress:** Update all story files with current state (AC checkboxes, completion notes)

   c. **Compact context:** Run `/compact` to free context before spawning new agents

   d. **Spawn paired agents (sequential per story, parallel across stories):**
   - For each story in wave:
     1. **Tester phase:** Spawn tester agent (unit-test, integration-test, or e2e-test)
        - Read story file → extract acceptance criteria
        - Write test file (mock passing & failing cases)
        - Update story file: Status → 🧪 Testing
        - Update story file: Assignee → {tester-agent}
     2. **Implementation phase:** Spawn implementation agent (coder, backend-dev, react-component, etc.)
        - Read story file (includes test file path)
        - Implement features to pass tests
        - Update story file: Status → 🔄 Implementing
        - Update story file: Assignee → {implementation-agent}

   e. **Run pairs sequentially:** Tester → Implementation (one story pair at a time within max 10 concurrent limit)

   f. **Wait for ALL stories in wave to complete** before advancing to next wave

3. **On task completion (tester or implementation):**
   - Update story file: Status → ✅ Complete
   - Update story file: Completion section with files modified
   - Update story file: Verified → yes (if validation passes)
   - **Update workflow state:** Mark story complete

   ```javascript
   const state = readWorkflowState(projectFolder);
   markStoryComplete(state, storyId);
   writeWorkflowState(projectFolder, state);
   ```

   - Record result, add to completed set

4. **Production verification check:**
   - Confirm tests still pass (run test file)
   - Confirm AC checkboxes checked in story file
   - Mark story ready for validation phase

5. **On task failure:** Log error, update story status to ❌ Failed, continue (validation phase handles retries)

6. **Wave completion:**
   - **Continue to next wave:** Waves execute continuously (no HITL stop between waves)

7. **Return:** All results with status, files modified, errors, test coverage, story completion tracking

---

## State Tracking

Use `/skill state-management` for all workflow state operations. State tracking occurs at four key checkpoints:

### 1. Wave Start

At the start of each wave, update workflow-state.json with current wave and in-progress stories:

```javascript
updateWorkflowState(projectFolder, {
  currentWave: waveNumber,
  status: "executing",
  stories: {
    ...state.stories,
    inProgress: waveStoryIds, // e.g., ["msm-feat-003", "msm-feat-004", "msm-feat-005"]
  },
});
```

### 2. Story Completion

After each story completes (both tester and implementation phases):

```javascript
const state = readWorkflowState(projectFolder);
markStoryComplete(state, storyId); // Moves from inProgress to completed
updateEpicProgress(state, storyId); // ALWAYS update parent epic counter
writeWorkflowState(projectFolder, state);
```

### 3. Workflow Complete

After final wave and validation phase:

```javascript
updateWorkflowState(projectFolder, {
  status: "complete",
  lastUpdate: new Date().toISOString(),
});
```

**State persistence rationale:**

- Enables workflow resumption after interruption
- Provides audit trail of execution progress
- Tracks epic completion percentage for PM dashboards

---

## Interruption Handling

Save state early and often for reliable workflow resumption:

1. **Before spawning agent:** Update workflow-state.json with story in `inProgress`
2. **After story completes:** Update workflow-state.json with story in `completed` and epic counter incremented
3. **On any error:** Update workflow-state.json with `status: "error"` and error details

This ensures workflows can resume correctly after user interruption or context clear.

---

## Execution Logic

```
waves = [[Story prj-epc-001], [Story prj-epc-002, prj-epc-003]]
completed = new Set()

for each wave in waves:
  // Update workflow state - wave start
  updateWorkflowState(projectFolder, {
    currentWave: waveNumber,
    status: "executing",
    stories: { ...state.stories, inProgress: waveStoryIds }
  })

  updateStoryFiles(wave, current state)
  runCompact()  // Free context

  for each story in wave:
    tester_promise = spawnAgent(tester, story)
    await tester_promise

    impl_promise = spawnAgent(implementation, story)
    await impl_promise

    runProductionCheck(story)

    // Update workflow state - story completion
    state = readWorkflowState(projectFolder)
    markStoryComplete(state, story.id)
    writeWorkflowState(projectFolder, state)

  // All stories in wave complete before next wave
  completed += wave

// Workflow complete
updateWorkflowState(projectFolder, { status: "complete" })

return allResults
```

**TDD Pairing Model:**

- Tester writes tests from AC (mocks passing & failing scenarios)
- Implementation agent reads test file + story AC
- Implementation runs tests until all pass
- Production check: tests still pass + AC checkboxes marked

---

## Agent Spawning

**Agent Announcement (ALWAYS do this before spawning):**

Before spawning any agent, announce the selection:
"Spawning {agent-type} agent ({agent-name}) for {story-id}"

Example: "Spawning tester agent (core-claude-plugin:generic:tester) for msm-auth-001"

**Tester spawn template:**

```
CONSTITUTION: 1) Change only what must change 2) Fix root cause 3) Read first 4) Verify before done 5) Do exactly what asked

ROLE: Tester Agent (TDD Pairing)
TASK: Write comprehensive tests for story acceptance criteria

STORY: Read {storyFilePath}
  - Extract acceptance criteria
  - Write test file with passing & failing scenarios
  - Update story: Status → 🧪 Testing

FILES: Write tests to {testFilePath}
VERIFY: Tests compile and run (no passing yet - implementation comes next)
```

**Implementation spawn template:**

```
CONSTITUTION: 1) Change only what must change 2) Fix root cause 3) Read first 4) Verify before done 5) Do exactly what asked

ROLE: Implementation Agent (TDD Pairing)
TASK: Implement features to pass all tests

STORY: Read {storyFilePath}
TESTS: Run {testFilePath} - ALL must pass
  - Implement code to satisfy acceptance criteria
  - Update story: Status → 🔄 Implementing
  - Verify all tests pass before submitting

FILES: Report files modified for PM tracking
UPDATE: Story status → ✅ Complete (tests passing)
```

**Key Changes:**

- Tester writes tests from AC (before implementation exists)
- Implementation reads both story AC AND test file
- Tests act as contract between tester and implementation
- Story file persists progress between agent spawns

---

## Domain Agent Categories

| Phase  | Category | Agents                                         |
| ------ | -------- | ---------------------------------------------- |
| Tester | Testing  | unit-test, integration-test, e2e-test          |
| Impl   | Backend  | backend-dev, data-service, integration-service |
| Impl   | Frontend | react-component, shadcn                        |
| Impl   | Database | prisma-database                                |
| Impl   | Config   | 26+ config agents (for /audit)                 |

**Tester selection:** Choose by test scope (unit → integration → e2e)

---

## Constraints

| Constraint     | Value | Rationale                   |
| -------------- | ----- | --------------------------- |
| Max concurrent | 10    | Prevent resource exhaustion |

---

## Output Format

```json
{
  "totalWaves": 2,
  "totalStories": 5,
  "storiesCompleted": ["msm-auth-001", "msm-auth-002", "msm-auth-003"],
  "storiesFailed": ["msm-auth-004"],
  "storiesRemaining": ["msm-auth-005"],
  "results": [
    {
      "storyId": "msm-auth-001",
      "wave": 1,
      "testerAgent": "unit-test",
      "testFile": "src/__tests__/auth.test.ts",
      "testsPassed": true,
      "implAgent": "backend-dev",
      "implStatus": "success",
      "filesModified": ["src/auth.ts", "src/__tests__/auth.test.ts"],
      "acChecklistComplete": true,
      "verifiedProduction": true
    }
  ],
  "totalTestsCovered": 45,
  "totalTestsPassed": 45
}
```

---

## Success Criteria

- ALWAYS spawn tester and coder agents for each story (orchestrator only directs work)
- ALWAYS track all implementation code written by spawned agents (tester writes tests, coder writes features)
- ALWAYS persist story state (status, assignments, completion notes) between agent spawns
- ALWAYS run production verification (tests pass, AC checkboxes marked) before marking story complete
- All implementation code written by spawned agents (tester and coder agents)
- Orchestrator only spawns, waits, tracks, and updates state
- No implementation code added by the orchestrator itself

---

## Integration

**Called by:** /audit, /build, /ms (complexity ≥15)
**Calls:** Domain agents, vibe_learn MCP (errors)
**Next phase:** validation-phase

---

## Example

```
/build JWT authentication API

Wave 1: msm-auth-001 (Schema + AuthService)
  1. updateStoryFiles(msm-auth-001)
  2. runCompact()
  3. T-001 (unit-test): Write auth.test.ts (mocks User model + AuthService)
  4. I-001 (backend-dev): Implement User model + AuthService (pass T-001)
  5. productionCheck: tests still pass, AC marked

Wave 2: msm-auth-002 (TokenService) | msm-auth-003 (API integration)
  1. updateStoryFiles(msm-auth-002, msm-auth-003)
  2. runCompact()
  3a. T-002 (unit-test): Write token.test.ts (parallel)
  3b. T-003 (integration-test): Write api.test.ts (parallel)
  4a. I-002 (backend-dev): Implement TokenService (pass T-002) (parallel)
  4b. I-003 (coder): Implement API routes (pass T-003) (parallel)
  5. productionCheck: all tests pass, AC marked

PM Gantt Format:
  Wave 1: [T-001]→[I-001] (sequential pair)
  Wave 2: [T-002]→[I-002] | [T-003]→[I-003] (parallel pairs)

Output: 3 stories completed, 45 tests passed, 12 files modified
```
