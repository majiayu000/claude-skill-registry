---
name: ci-pipeline-manager
description: "Manage CI pipelines with error handling, recovery, and complex dependencies. Use when testing pipeline workflows. Not for simple linear scripts or unit testing individual tasks."
context: fork
---

# CI Pipeline Error Recovery Testing

Test TaskList error handling and recovery behavior with CI pipelines.

## Pipeline Architecture

<logic_flow>
digraph Pipeline {
rankdir=LR;
node [shape=box];
Tests [label="1. run-tests"];
Build [label="2. build"];
Deploy [label="3. deploy"];
Cleanup [label="4. cleanup-on-failure" style=filled fillcolor=lightgrey];

    Tests -> Build [label="Pass"];
    Build -> Deploy [label="Success"];
    Tests -> Cleanup [label="Fail"];

    {rank=same; Tests; Cleanup}

}
</logic_flow>

**Four-task pipeline with error handling:**

1. **run-tests** - Execute test suite
   - Simulates test failure for validation
   - Failure: blocks all downstream tasks
   - Output: Test results (simulated failure)

2. **build** - Compile application
   - BLOCKED by: run-tests
   - Should NOT run if tests fail
   - Output: Build artifact or "SKIPPED"

3. **deploy** - Deploy to staging
   - BLOCKED by: build
   - Should NOT run if build doesn't happen
   - Output: Deployment status or "SKIPPED"

4. **cleanup-on-failure** - Cleanup resources
   - BLOCKED by: run-tests (triggers when run-tests completes)
   - MUST execute even when tests fail
   - Output: Cleanup completion status

## Execution Workflow

**Execute autonomously:**

1. **Create TaskList** with all four tasks
2. **Set up blocking dependencies:**
   - build blocked_by: ["run-tests"]
   - deploy blocked_by: ["build"]
   - cleanup-on-failure blocked_by: ["run-tests"]
3. **Simulate test failure** in run-tests task
4. **Verify behavior:**
   - build: blocked by failed run-tests → SKIPPED
   - deploy: build never ran → SKIPPED
   - cleanup-on-failure: MUST execute despite failure
5. **Report task states** and pipeline status

**Recognition test:** Cleanup-on-failure should always execute, even when run-tests fails.

## Expected Output

```
CI Pipeline: RUNNING
[task-id] run-tests: IN_PROGRESS -> FAILED
[task-id] build: BLOCKED -> SKIPPED (dependency failed)
[task-id] deploy: BLOCKED -> SKIPPED (dependency never ran)
[task-id] cleanup-on-failure: BLOCKED -> IN_PROGRESS -> COMPLETE

Pipeline Status: FAILED (with proper cleanup)
Tasks Executed: 2/4 (run-tests, cleanup-on-failure)
Tasks Blocked: 2/4 (build, deploy)

Error Handling: PASS
Cleanup: PASS
```

## Validation Criteria

- Failed task blocked dependents
- Cleanup executed despite failure

**Binary check:** "Proper error handling?" → Both criteria must pass.

---

<critical_constraint>
MANDATORY: Verify cleanup-on-failure always executes despite run-tests failure
MANDATORY: Ensure build and deploy are properly blocked by failed upstream tasks
MANDATORY: Report task states accurately (BLOCKED, SKIPPED, IN_PROGRESS, COMPLETE)
No exceptions. CI pipeline error handling must be deterministic.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
