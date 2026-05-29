---
name: run-execute
description: Execute work items based on their assigned mode (autopilot, confirm, validate). Supports single-item and multi-item (batch/wide) runs.
version: 1.0.0
---

<objective>
Execute work items based on their assigned mode (autopilot, confirm, validate).
Supports both single-item and multi-item (batch/wide) runs.
</objective>

<progress_display>
  Show current position in workflow:

  ```text
  ### Run Progress
  - [ ] Run initialized (init-run.cjs)
  - [ ] Context loaded
  - [ ] Plan generated  ← {current_step}
  - [ ] Implementation
  - [ ] Tests passing
  - [ ] Code review
  - [ ] Run completed (complete-run.cjs)
  - [ ] Walkthrough generated
  ```

  Update markers as you progress: [x] = done, ← current = active step
</progress_display>

<prerequisites>
  Before executing scripts, ensure required dependencies are installed:

  <step n="1" title="Check yaml Package">
    <action>Run: npm list yaml --depth=0 2>/dev/null || echo "NOT_FOUND"</action>
    <check if="output contains NOT_FOUND">
      <output>Installing required dependency: yaml</output>
      <action>Run: npm install yaml</action>
    </check>
  </step>

  | Package | Purpose | Install Command |
  |---------|---------|-----------------|
  | `yaml` | Parse/stringify state.yaml | `npm install yaml` |

</prerequisites>

<triggers>
  - Pending work item ready for execution
  - Resumed from interrupted run
  - Batch of work items passed from run-plan
</triggers>

<resume_detection critical="true">
  Before starting execution, check if resuming an interrupted run:

  <step n="0" title="Check for Active Run">
    <action>Check state.yaml for runs.active[] array</action>

    <check if="runs.active is empty">
      <goto step="1">No active run, start fresh</goto>
    </check>

    <check if="runs.active has entries">
      <action>Load active run from state.yaml runs.active[0]</action>
      <action>Read scope (single/batch/wide) and work_items array</action>

      <substep n="0a" title="Enumerate Work Item Status">
        <action>For EACH work item in runs.active[0].work_items, classify by status:</action>
        <action>Build status summary from state.yaml (NOT from artifact files):</action>
        <format>
          [DONE] {item-id} — completed
          [WORKING] {item-id} (phase: {current_phase}) — in_progress
          [PENDING] {item-id} — pending
        </format>
        <action>Count: completed={X}, in_progress={Y}, pending={Z}</action>
      </substep>

      <substep n="0b" title="Determine Resume Point for Current Item">
        <action>Get current_item from state.yaml</action>
        <action>Read current_phase from the current item's entry in work_items</action>

        <determine_resume_point>
          Use current_phase from state.yaml to determine resume point:

          | current_phase | Resume At |
          |---------------|-----------|
          | plan (or unset) | Step 3 (Generate Plan) |
          | execute | Step 5 (Implementation) |
          | test | Step 6 (Run Tests) |
          | review | Step 6b (Code Review) |
        </determine_resume_point>
      </substep>

      <llm critical="true">
        <mandate>NEVER call --complete-item for items with status "completed" — they are already done</mandate>
        <mandate>NEVER re-execute steps (plan, implement, test) for completed items</mandate>
        <mandate>ONLY work on the current_item identified in state.yaml</mandate>
        <mandate>Use current_phase from state.yaml — do NOT infer phase from artifact file existence</mandate>
      </llm>

      <output>
        Resuming run {run-id} ({scope}) for work item {current_item}.
        Mode: {mode}
        Phase: {current_phase}
        Status: {completed_count} done, {in_progress_count} working, {pending_count} pending
        Resuming at: Step {step_number}
      </output>
    </check>
  </step>
</resume_detection>

<degrees_of_freedom>
  Varies by mode:

- **Autopilot**: LOW — Execute standard patterns decisively
- **Confirm**: MEDIUM — Present plan, adjust based on feedback
- **Validate**: LOW — Follow approved design precisely
</degrees_of_freedom>

<llm critical="true">
  <mandate>USE SCRIPTS — NEVER bypass init-run.cjs or complete-run.cjs</mandate>
  <mandate>ALWAYS CREATE plan.md — Create plan BEFORE implementation starts (ALL modes)</mandate>
  <mandate>ALWAYS CREATE test-report.md — Create test report AFTER tests complete</mandate>
  <mandate>ALWAYS RUN code-review — Invoke code-review skill after tests pass</mandate>
  <mandate>TRACK ALL FILE OPERATIONS — Every create, modify MUST be recorded</mandate>
  <mandate>NEVER skip tests — Tests are mandatory, not optional</mandate>
  <mandate>FOLLOW BROWNFIELD RULES — Read before write, match existing patterns</mandate>
</llm>

<artifact_timing critical="true">
  Artifacts MUST be created at these points:

  | Artifact | When Created | Created By |
  |----------|--------------|------------|
  | run.md | Start of run | init-run.cjs script |
  | plan.md | BEFORE implementation (Step 4) | Agent using template |
  | test-report.md | AFTER tests pass (Step 6) | Agent using template |
  | review-report.md | AFTER test report (Step 6b) | code-review skill |
  | walkthrough.md | After run completes (Step 8) | walkthrough-generate skill |

  For batch runs: Append each work item's section to plan.md and test-report.md.
</artifact_timing>

<flow>
  <step n="1" title="Initialize Run">
    <hard_gate>
      ⛔ HARD GATE - SCRIPT EXECUTION REQUIRED
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      You MUST call init-run.cjs script.
      DO NOT use mkdir or create files directly.
      The script creates BOTH the folder AND run.md file.
      If you skip this, state.yaml will be inconsistent.
    </hard_gate>

    <action>Prepare work items JSON array:</action>
    <code>
      # For single item:
      node scripts/init-run.cjs {rootPath} {workItemId} {intentId} {mode}

      # For batch/wide (multiple items):
      node scripts/init-run.cjs {rootPath} --batch '[
        {"id": "item-1", "intent": "intent-1", "mode": "autopilot"},
        {"id": "item-2", "intent": "intent-1", "mode": "confirm"}
      ]' --scope=batch
    </code>

    <action>Parse script output for runId and runPath</action>
    <action>Verify run.md was created in .specs-fire/runs/{run-id}/</action>

    <check if="run.md not found">
      <error>init-run.cjs failed to create run.md. Check script output.</error>
    </check>
  </step>

  <step n="2" title="Load Work Item Context">
    <note>For batch runs, repeat steps 2-6b for each work item</note>

    <action>Get current_item from state.yaml runs.active[0]</action>
    <action>Load work item from .specs-fire/intents/{intent}/work-items/{id}.md</action>
    <action>Read intent brief for broader context</action>
    <action>Load project standards using hierarchical resolution:</action>

    <standards_resolution critical="true">
      <substep n="2a" title="Discover Standards Locations">
        <action>Scan repository for: **/.specs-fire/standards/</action>
        <action>Build list sorted by path depth (root = depth 0)</action>
        <example>
          depth 0: .specs-fire/standards/
          depth 2: packages/api/.specs-fire/standards/
          depth 2: apps/mobile/.specs-fire/standards/
        </example>
      </substep>

      <substep n="2b" title="Load Constitution (Root Only)">
        <action>Load .specs-fire/standards/constitution.md from ROOT</action>
        <critical>IGNORE any constitution.md in nested directories</critical>
        <critical>Constitution is ALWAYS inherited, NEVER overridden</critical>
        <note>If constitution.md doesn't exist, skip gracefully</note>
      </substep>

      <substep n="2c" title="Resolve Module Standards">
        <action>For each discovered standards location (excluding root):</action>

        <resolution_algorithm>
          FOR each standard_file IN [tech-stack.md, coding-standards.md,
                                      testing-standards.md, system-architecture.md]:

            IF {location}/standards/{standard_file} EXISTS:
              → USE this file for scope {location.parent_path}/**
            ELSE:
              → Walk UP to find nearest ancestor with this file
              → USE ancestor's file (ultimately root if none found)
        </resolution_algorithm>
      </substep>

      <substep n="2d" title="Present Standards with Scoping">
        <action>Present loaded standards with clear path-based scoping:</action>

        <output_format>
          ## Constitution (applies to ALL files)
          [content of root constitution.md]

          ## Standards for {module_path}/** files
          When editing files under {module_path}/, apply:
          - Tech Stack: [resolved tech-stack.md for this scope]
          - Coding Standards: [resolved coding-standards.md for this scope]
          - Testing Standards: [resolved testing-standards.md for this scope]

          ## Default Standards (paths without specific scope)
          For all other files, apply root standards.
        </output_format>
      </substep>
    </standards_resolution>

    <action>Determine execution mode from work item</action>
  </step>

  <step n="3a" title="Autopilot Mode" if="mode == autopilot">
    <output>
      Executing in Autopilot mode (0 checkpoints).
      Work item: {title}
    </output>
    <goto step="4"/>
  </step>

  <step n="3b" title="Confirm Mode" if="mode == confirm">
    <action>Generate implementation plan</action>
    <action>Save plan IMMEDIATELY using template: templates/plan.md.hbs</action>
    <action>Write to: .specs-fire/runs/{run-id}/plan.md</action>
    <output>Plan saved to: .specs-fire/runs/{run-id}/plan.md</output>
    <action>Mark checkpoint as waiting:</action>
    <code>node scripts/update-checkpoint.cjs {rootPath} {runId} awaiting_approval --checkpoint=plan</code>

    <checkpoint>
      <template_output section="plan">
        ## Implementation Plan for "{title}"

        ### Approach
        {describe approach}

        ### Files to Create
        {list files}

        ### Files to Modify
        {list files}

        ### Tests
        {list test files}

        ---
        Approve plan? [Y/n/edit]
      </template_output>
    </checkpoint>

    <check if="response == edit">
      <ask>What changes to the plan?</ask>
      <action>Adjust plan</action>
      <action>Update plan.md with changes</action>
      <goto step="3b"/>
    </check>
    <action>Mark checkpoint approved:</action>
    <code>node scripts/update-checkpoint.cjs {rootPath} {runId} approved --checkpoint=plan</code>
    <goto step="5"/>
  </step>

  <step n="3c" title="Validate Mode" if="mode == validate">
    <action>Load design doc from .specs-fire/intents/{intent}/work-items/{id}-design.md</action>
    <action>Generate implementation plan based on design</action>
    <action>Save plan IMMEDIATELY using template: templates/plan.md.hbs</action>
    <action>Write to: .specs-fire/runs/{run-id}/plan.md</action>
    <action>Include reference to design doc in plan</action>
    <output>Plan saved to: .specs-fire/runs/{run-id}/plan.md</output>
    <action>Mark checkpoint as waiting:</action>
    <code>node scripts/update-checkpoint.cjs {rootPath} {runId} awaiting_approval --checkpoint=plan</code>

    <checkpoint>
      <template_output section="plan">
        ## Implementation Plan for "{title}"

        Based on approved design document.

        ### Implementation Checklist
        {from design doc}

        ### Files to Create
        {list files}

        ### Files to Modify
        {list files}

        ---
        This is Checkpoint 2 of Validate mode.
        Approve implementation plan? [Y/n/edit]
      </template_output>
    </checkpoint>

    <check if="response == edit">
      <ask>What changes to the plan?</ask>
      <action>Adjust plan</action>
      <action>Update plan.md with changes</action>
      <goto step="3c"/>
    </check>
    <action>Mark checkpoint approved:</action>
    <code>node scripts/update-checkpoint.cjs {rootPath} {runId} approved --checkpoint=plan</code>
    <goto step="5"/>
  </step>

  <step n="4" title="Generate Plan (Autopilot Only)" if="mode == autopilot">
    <note>Confirm and Validate modes already saved plan in Step 3b/3c</note>

    <batch_handling critical="true">
      <check if="batch/wide run AND plan.md already exists">
        <action>Read existing plan.md content</action>
        <action>Append new section for current work item:</action>
        <format>
          ---

          ## Work Item: {work_item_id}

          ### Approach
          {describe approach for this specific work item}

          ### Files to Create
          {list files}

          ### Files to Modify
          {list files}

          ### Tests
          {list test files}
        </format>
        <action>Write updated plan.md (preserving previous sections)</action>
      </check>

      <check if="plan.md does not exist OR single run">
        <action>Generate implementation plan</action>
        <action>Save plan using template: templates/plan.md.hbs</action>
        <action>Write to: .specs-fire/runs/{run-id}/plan.md</action>
      </check>
    </batch_handling>

    <output>
      Plan saved to: .specs-fire/runs/{run-id}/plan.md
      (Autopilot mode - continuing without checkpoint)
    </output>
    <note>No checkpoint in autopilot - human can review plan.md while agent works</note>
  </step>

  <step n="5" title="Execute Implementation">
    <action>Update phase to 'execute':</action>
    <code>node scripts/update-phase.cjs {rootPath} {runId} execute</code>

    <action>For each planned change:</action>
    <substep n="5a">Implement the change</substep>
    <substep n="5b">Track file operation (create/modify)</substep>
    <substep n="5c">Record decisions made</substep>

    <standards_application critical="true">
      When editing a file at path X:
      1. Find the LONGEST matching standards scope (most specific)
      2. Apply those standards to the file
      3. If no specific scope matches, apply root standards

      <example>
        Editing packages/api/src/handler.go
        → Apply "Standards for packages/api/**"

        Editing scripts/deploy.sh
        → Apply "Default Standards" (root)
      </example>
    </standards_application>

    <brownfield_rules>
      <rule>READ existing code before modifying</rule>
      <rule>MATCH existing naming conventions</rule>
      <rule>FOLLOW existing patterns in the codebase</rule>
      <rule>PRESERVE existing tests</rule>
      <rule>USE module-specific standards when editing module files</rule>
    </brownfield_rules>
  </step>

  <step n="6" title="Run Tests">
    <action>Update phase to 'test':</action>
    <code>node scripts/update-phase.cjs {rootPath} {runId} test</code>

    <action>Load testing standards from .specs-fire/standards/testing-standards.md</action>
    <action>Write tests following testing standards:</action>
    <substep>Unit tests for new/modified functions</substep>
    <substep>Integration tests for API endpoints or workflows</substep>
    <substep>Follow test naming and structure conventions</substep>

    <action>Run test suite</action>
    <check if="tests fail">
      <output>Tests failed. Fixing issues...</output>
      <action>Fix failing tests</action>
      <action>Re-run tests</action>
    </check>

    <action>Validate acceptance criteria from work item</action>

    <critical>Create test report AFTER tests pass</critical>

    <batch_handling critical="true">
      <check if="batch/wide run AND test-report.md already exists">
        <action>Read existing test-report.md content</action>
        <action>Append new section for current work item:</action>
        <format>
          ---

          ## Work Item: {work_item_id}

          ### Test Results
          - Passed: {passed_count}
          - Failed: {failed_count}
          - Skipped: {skipped_count}

          ### Acceptance Criteria Validation
          {validation_results}
        </format>
        <action>Write updated test-report.md (preserving previous sections)</action>
      </check>

      <check if="test-report.md does not exist OR single run">
        <action>Generate test report using template: templates/test-report.md.hbs</action>
        <action>Write to: .specs-fire/runs/{run-id}/test-report.md</action>
      </check>
    </batch_handling>

    <action>Include in test report:</action>
    <substep>Test results summary (passed/failed/skipped)</substep>
    <substep>Code coverage percentage</substep>
    <substep>Acceptance criteria validation results</substep>
    <substep>Any test warnings or notes</substep>
    <output>Test report saved to: .specs-fire/runs/{run-id}/test-report.md</output>
  </step>

  <step n="6b" title="Code Review">
    <action>Update phase to 'review':</action>
    <code>node scripts/update-phase.cjs {rootPath} {runId} review</code>

    <critical>ALWAYS run code review after tests pass</critical>
    <output>Running code review...</output>

    <action>Invoke code-review skill with context:</action>
    <code>
      invoke-skill: code-review
      context:
        files_created: {files_created}
        files_modified: {files_modified}
        run_id: {run_id}
        intent_id: {intent_id}
    </code>

    <invoke_skill>code-review</invoke_skill>

    <note>
      Code review skill will:
      1. Review all files created/modified in this work item
      2. Auto-fix no-brainer issues (unused imports, console.log, etc.)
      3. Present suggestions requiring approval
      4. Create review-report.md artifact
    </note>

    <check if="code-review returns suggestions">
      <note>User interaction happens within code-review skill</note>
      <action>Wait for code-review skill to complete</action>
    </check>

    <check if="code-review applied fixes">
      <action>Re-run tests to verify fixes didn't break anything</action>
      <check if="tests fail">
        <output>Code review fixes caused test failure. Reverting...</output>
        <action>Revert code review changes</action>
        <action>Re-run tests to confirm passing</action>
      </check>
    </check>

    <output>
      Code review complete.
      Review report: .specs-fire/runs/{run-id}/review-report.md
    </output>
  </step>

  <step n="7" title="Complete Current Work Item">
    <hard_gate>
      ⛔ HARD GATE - SCRIPT EXECUTION REQUIRED
      ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
      You MUST call complete-run.cjs script.
      DO NOT manually update state.yaml or run.md.
      Use --complete-item for batch runs with remaining items.
      Use --complete-run only when ALL items are done.
      If you skip this, state becomes inconsistent.
    </hard_gate>

    <llm critical="true">
      <mandate>BATCH RUNS: You MUST loop until ALL items are done</mandate>
      <mandate>NEVER call --complete-run until ALL items have artifacts</mandate>
      <mandate>ALWAYS check pending count BEFORE deciding which flag to use</mandate>
    </llm>

    <substep n="7a" title="Check Batch Status">
      <action>Read state.yaml runs.active[{runId}]</action>
      <action>Get scope value: single, batch, or wide</action>
      <action>Count work_items where status == "pending"</action>
      <action>Store pending_count for decision</action>
    </substep>

    <substep n="7b" title="Route Based on Batch Status">
      <check if="scope in [batch, wide] AND pending_count > 0">
        <critical>DO NOT call --complete-run yet - more items remain!</critical>
        <action>Call complete-run.cjs with --complete-item flag:</action>
        <code>
          node scripts/complete-run.cjs {rootPath} {runId} --complete-item
        </code>
        <action>Parse output JSON for nextItem and remainingItems</action>
        <output>
          Completed: {current_item}
          Next item: {nextItem}
          Remaining: {remainingItems} items
        </output>
        <goto step="2">MUST continue with next work item - loop back NOW</goto>
      </check>

      <check if="scope == single OR pending_count == 0">
        <action>All items complete - finalize the run</action>
        <action>Call complete-run.cjs with --complete-run flag:</action>
        <code>
          node scripts/complete-run.cjs {rootPath} {runId} --complete-run \
            --files-created='[{"path":"...","purpose":"..."}]' \
            --files-modified='[{"path":"...","changes":"..."}]' \
            --tests=5 --coverage=85
        </code>
        <goto step="8"/>
      </check>
    </substep>
  </step>

  <step n="8" title="Generate Walkthrough">
    <invoke_skill>walkthrough-generate</invoke_skill>
  </step>

  <step n="9" title="Report Completion">
    <output>
      Run {run-id} completed.

      Work items completed: {count}
      Files created: {count}
      Files modified: {count}
      Tests added: {count}

      Artifacts:
      - Run Log: .specs-fire/runs/{run-id}/run.md
      - Plan: .specs-fire/runs/{run-id}/plan.md
      - Test Report: .specs-fire/runs/{run-id}/test-report.md
      - Code Review: .specs-fire/runs/{run-id}/review-report.md
      - Walkthrough: .specs-fire/runs/{run-id}/walkthrough.md
    </output>
  </step>
</flow>

<scripts>
  | Script | Purpose | Usage |
  |--------|---------|-------|
  | `scripts/init-run.cjs` | Initialize run record and folder | Creates run.md with all work items |
  | `scripts/update-checkpoint.cjs` | Mark approval gate state for active item | `awaiting_approval` / `approved` |
  | `scripts/update-phase.cjs` | Update current work item's phase | `node scripts/update-phase.cjs {rootPath} {runId} {phase}` |
  | `scripts/complete-run.cjs` | Finalize run and update state | `--complete-item` or `--complete-run` |

  <script name="init-run.cjs">
    ```bash
    # Single work item
    node scripts/init-run.cjs /project work-item-id intent-id autopilot

    # Batch/wide (multiple items)
    node scripts/init-run.cjs /project --batch '[
      {"id": "wi-1", "intent": "int-1", "mode": "autopilot"},
      {"id": "wi-2", "intent": "int-1", "mode": "confirm"}
    ]' --scope=batch
    ```

    <output_format>
      ```json
      {
        "success": true,
        "runId": "run-fabriqa-2026-001",
        "runPath": "/project/.specs-fire/runs/run-fabriqa-2026-001",
        "scope": "batch",
        "workItems": [...],
        "currentItem": "wi-1"
      }
      ```
    </output_format>
  </script>

  <script name="complete-run.cjs">
    ```bash
    # Complete current item (batch runs - moves to next item)
    node scripts/complete-run.cjs /project run-fabriqa-2026-001 --complete-item

    # Complete entire run (single runs or final item in batch)
    node scripts/complete-run.cjs /project run-fabriqa-2026-001 --complete-run \
      --files-created='[{"path":"src/new.ts","purpose":"New feature"}]' \
      --files-modified='[{"path":"src/old.ts","changes":"Added import"}]' \
      --tests=5 --coverage=85
    ```

    <complete_item_output>
      ```json
      {
        "success": true,
        "runId": "run-fabriqa-2026-001",
        "completedItem": "wi-1",
        "nextItem": "wi-2",
        "remainingItems": 1,
        "allItemsCompleted": false
      }
      ```
    </complete_item_output>

    <complete_run_output>
      ```json
      {
        "success": true,
        "runId": "run-fabriqa-2026-001",
        "scope": "batch",
        "workItemsCompleted": 2,
        "completedAt": "2026-01-20T..."
      }
      ```
    </complete_run_output>
  </script>
</scripts>

<file_tracking_format>

  ```yaml
  files_created:
    - path: src/auth/login.ts
      purpose: Login endpoint handler

  files_modified:
    - path: src/routes/index.ts
      changes: Added login route

  decisions:
    - decision: Use JWT for tokens
      rationale: Stateless, works with load balancer
  ```

</file_tracking_format>

<run_folder_structure>
  After init-run.cjs creates a run:

  ```
  .specs-fire/runs/run-fabriqa-2026-001/
  ├── run.md           # Created by init-run.cjs, updated by complete-run.cjs
  ├── plan.md          # Created BEFORE implementation (ALL modes - required)
  ├── test-report.md   # Created AFTER tests pass (required)
  ├── review-report.md # Created by code-review skill (Step 6b)
  └── walkthrough.md   # Created by walkthrough-generate skill
  ```

  <timeline>
    1. `run.md` — Created at run start by init-run.cjs
    2. `plan.md` — Created BEFORE implementation begins (Step 4)
    3. `test-report.md` — Created AFTER tests pass (Step 6)
    4. `review-report.md` — Created by code-review skill (Step 6b)
    5. `walkthrough.md` — Created after run completes (Step 8)
  </timeline>

  The run.md contains:

- All work items with their statuses
- Current item being executed
- Files created/modified (after completion)
- Decisions made (after completion)
- Summary (after completion)
</run_folder_structure>

<success_criteria>
  <criterion>Run initialized via init-run.cjs script</criterion>
  <criterion>Standards loaded with hierarchical resolution</criterion>
  <criterion>Constitution loaded from root (if exists)</criterion>
  <criterion>Module-specific standards applied to module files</criterion>
  <criterion>plan.md created BEFORE implementation</criterion>
  <criterion>All work items implemented</criterion>
  <criterion>All tests pass</criterion>
  <criterion>test-report.md created AFTER tests pass</criterion>
  <criterion>code-review skill invoked and completed</criterion>
  <criterion>review-report.md created</criterion>
  <criterion>Run completed via complete-run.cjs script</criterion>
  <criterion>walkthrough.md generated</criterion>
</success_criteria>
