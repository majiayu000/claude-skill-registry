---
name: status
description: Display current FIRE project status and validate integrity of intents, work items, and runs.
version: 2.0.0
---

<objective>
Display current FIRE project status and validate integrity across state.yaml and file system.
Detect inconsistencies and offer interactive resolution.
</objective>

<triggers>
  - User runs `/specsmd-fire status`
  - User asks "what's the status?"
  - User asks to "check" or "validate" the project state
</triggers>

<degrees_of_freedom>
  **LOW** — Report facts accurately. Never auto-fix without user confirmation.
</degrees_of_freedom>

<llm critical="true">
  <mandate>NEVER auto-fix inconsistencies — ALWAYS ask user first</mandate>
  <mandate>ALWAYS scan file system — state.yaml may be incomplete</mandate>
  <mandate>Report ALL findings before offering fixes</mandate>
  <mandate>state.yaml is source of truth for status — frontmatter may be stale</mandate>
</llm>

<flow>
  <step n="1" title="Read State">
    <action>Read .specs-fire/state.yaml</action>
    <check if="state.yaml not found">
      <output>No FIRE project found. Run `/specsmd-fire` to initialize.</output>
      <exit/>
    </check>
  </step>

  <step n="2" title="Display Status">
    <output>
      # FIRE Status

      **Project**: {project.name}
      **Workspace**: {workspace.type} / {workspace.structure}
      **Autonomy**: {workspace.autonomy_bias}
      **Version**: {project.fire_version}

      ## Intents

      {for each intent}
      ### {intent.title} [{intent.status}]

      | Work Item | Status | Complexity | Mode |
      |-----------|--------|------------|------|
      {for each work_item}
      | {title} | {status} | {complexity} | {mode} |
      {/for}

      {/for}

      ## Active Runs

      {if runs.active is array and has items}
      {for each active_run in runs.active}
      - **Run**: {active_run.id} | **Scope**: {active_run.scope}
      - **Current Item**: {active_run.current_item}
      - **Started**: {active_run.started}
      {/for}
      {else if active_run exists (legacy singular)}
      - **Run**: {active_run.id}
      - **Work Item**: {active_run.work_item}
      - **Started**: {active_run.started}
      {else}
      No active run.
      {/if}

      ## Quick Stats

      - Intents: {total_intents} ({completed_intents} completed)
      - Work Items: {total_work_items} ({completed_work_items} completed)
      - Runs: {total_runs} completed
    </output>
  </step>

  <!-- ═══════════════════════════════════════════════════════════════════════════ -->
  <!-- INTEGRITY VALIDATION (NEW)                                                   -->
  <!-- ═══════════════════════════════════════════════════════════════════════════ -->

  <step n="3" title="Scan File System">
    <critical>
      File system may have artifacts not tracked in state.yaml.
      state.yaml may reference artifacts that no longer exist on disk.
    </critical>

    <substep n="3a" title="Scan Intents">
      <action>Glob: .specs-fire/intents/*/brief.md</action>
      <action>Extract intent IDs from directory names</action>
      <action>Store as: intents_on_disk[]</action>
    </substep>

    <substep n="3b" title="Scan Work Items">
      <action>Glob: .specs-fire/intents/*/work-items/*.md</action>
      <action>Exclude design docs (*-design.md)</action>
      <action>Extract work item IDs and parent intents</action>
      <action>Store as: work_items_on_disk[]</action>
    </substep>

    <substep n="3c" title="Scan Runs">
      <action>Glob: .specs-fire/runs/run-*/run.md</action>
      <action>Extract run IDs from directory names</action>
      <action>For each run, check which artifacts exist:</action>
      <substep>plan.md, test-report.md, review-report.md, walkthrough.md</substep>
      <action>Store as: runs_on_disk[] with artifact_flags</action>
    </substep>
  </step>

  <step n="4" title="Compare File System vs State">
    <substep n="4a" title="Find Orphaned Artifacts (on disk but not in state)">
      <action>Compare intents_on_disk with state.intents</action>
      <action>Compare work_items_on_disk with state work_items</action>
      <action>Compare runs_on_disk with state.runs.completed + state.runs.active</action>

      <check if="intent on disk but not in state">
        <add_issue type="orphaned_intent" severity="warning">
          Intent '{id}' exists on disk but not tracked in state.yaml
        </add_issue>
      </check>

      <check if="work item on disk but not in state">
        <add_issue type="orphaned_work_item" severity="warning">
          Work item '{id}' exists on disk but not tracked in state.yaml
        </add_issue>
      </check>

      <check if="run folder on disk but not in state">
        <add_issue type="orphaned_run" severity="warning">
          Run '{id}' exists on disk but not tracked in state.yaml
        </add_issue>
      </check>
    </substep>

    <substep n="4b" title="Find Missing Files (in state but not on disk)">
      <check if="intent in state but no brief.md on disk">
        <add_issue type="missing_intent_file" severity="error">
          Intent '{id}' tracked but brief.md not found on disk
        </add_issue>
      </check>

      <check if="work item in state but no .md file on disk">
        <add_issue type="missing_work_item_file" severity="error">
          Work item '{id}' tracked but file not found on disk
        </add_issue>
      </check>

      <check if="completed run in state but no folder on disk">
        <add_issue type="missing_run_folder" severity="error">
          Run '{id}' marked complete but folder not found on disk
        </add_issue>
      </check>
    </substep>
  </step>

  <step n="5" title="Validate Status Cascade">
    <critical>
      Status must cascade correctly:
      - Run completes work item → work item should be "completed"
      - All work items completed → intent should be "completed"
      - Any work item in_progress → intent should be "in_progress"
    </critical>

    <substep n="5a" title="Work Item Status Check">
      <action>For each work item in state:</action>

      <check if="work item in runs.completed but status != completed">
        <add_issue type="status_mismatch" severity="error">
          Work item '{id}' was completed in run '{run_id}' but status is '{current_status}'
          Expected: completed
        </add_issue>
      </check>

      <check if="work item in runs.active as current_item but status != in_progress">
        <add_issue type="status_mismatch" severity="warning">
          Work item '{id}' is currently executing in run '{run_id}' but status is '{current_status}'
          Expected: in_progress
        </add_issue>
      </check>

      <check if="work item status is completed but not found in any completed run">
        <add_issue type="status_unverifiable" severity="warning" needs_code_check="true">
          Work item '{id}' marked as completed but no completed run found
          May have been done outside FIRE or run data is missing
        </add_issue>
      </check>
    </substep>

    <substep n="5b" title="Intent Status Check">
      <action>For each intent in state:</action>

      <derive_expected_status>
        IF any work_item.status == "in_progress":
          expected = "in_progress"
        ELSE IF all work_items.status == "completed":
          expected = "completed"
        ELSE IF all work_items.status == "pending":
          expected = "pending"
        ELSE: # mixed pending/completed
          expected = "in_progress"
      </derive_expected_status>

      <check if="intent.status != expected_status">
        <add_issue type="intent_status_mismatch" severity="error">
          Intent '{title}' has status '{current}' but should be '{expected}'
          Based on work item statuses: {breakdown}
        </add_issue>
      </check>
    </substep>
  </step>

  <step n="6" title="Validate Run Artifact Completeness">
    <substep n="6a" title="Check Completed Runs">
      <action>For each run in runs.completed (or runs_on_disk marked complete):</action>

      <required_artifacts>
        - run.md (mandatory)
        - plan.md (mandatory for all modes)
        - test-report.md (mandatory after tests)
        - walkthrough.md (mandatory after completion)
      </required_artifacts>

      <optional_artifacts>
        - review-report.md (created by code-review skill)
      </optional_artifacts>

      <check if="completed run missing required artifact">
        <add_issue type="incomplete_run_artifacts" severity="warning">
          Run '{id}' is marked complete but missing: {missing_artifacts}
        </add_issue>
      </check>
    </substep>

    <substep n="6b" title="Check Active Runs">
      <action>For each run in runs.active:</action>

      <check if="active run folder does not exist">
        <add_issue type="active_run_missing" severity="error">
          Active run '{id}' has no folder on disk
          Run may have been deleted or never initialized properly
        </add_issue>
      </check>

      <check if="active run has no run.md">
        <add_issue type="active_run_corrupted" severity="error">
          Active run '{id}' folder exists but run.md is missing
          Run initialization may have failed
        </add_issue>
      </check>
    </substep>
  </step>

  <step n="7" title="Detect Stale Runs">
    <action>For each run in runs.active[]:</action>
    <action>Calculate age: now - run.started</action>

    <check if="active run started more than 24 hours ago">
      <add_issue type="stale_run" severity="info" needs_user_decision="true">
        Active run '{id}' was started {age} ago
        Current item: {current_item}
        Artifacts present: {artifact_list}
        May be abandoned or work was done outside FIRE
      </add_issue>
    </check>

    <check if="active run has plan.md but no test-report.md and age > 1 hour">
      <add_issue type="interrupted_run" severity="warning" needs_user_decision="true">
        Run '{id}' appears interrupted mid-execution
        Has: plan.md
        Missing: test-report.md, walkthrough.md
        Execution may have been stopped before completion
      </add_issue>
    </check>
  </step>

  <step n="8" title="Check Frontmatter Sync">
    <note>state.yaml is source of truth. Frontmatter may drift.</note>

    <action>For each work item with status in state.yaml:</action>
    <action>Read work item file, parse frontmatter</action>

    <check if="frontmatter.status != state.yaml.status">
      <add_issue type="frontmatter_drift" severity="info">
        Work item '{id}' frontmatter says '{frontmatter_status}' but state.yaml says '{state_status}'
        state.yaml is authoritative
      </add_issue>
    </check>
  </step>

  <step n="9" title="Report Findings">
    <check if="no issues found">
      <output>
        ## ✅ Integrity Check Passed

        All artifacts are consistent:
        - {intent_count} intents tracked and verified
        - {work_item_count} work items with correct status
        - {run_count} runs with complete artifacts
        - No orphaned or missing files detected
      </output>
      <exit/>
    </check>

    <check if="issues found">
      <output>
        ## ⚠️ Integrity Issues Detected

        Found {issue_count} issue(s) requiring attention:

        | # | Type | Location | Issue | Suggested Fix |
        |---|------|----------|-------|---------------|
        {for each issue, numbered}
        | {n} | {severity_icon} | {location} | {description} | {fix_suggestion} |
        {/for}

        **Severity**: 🔴 Error | 🟡 Warning | 🔵 Info

        ---

        ### Actions

        **[1] fix-all** — Apply all recommended fixes automatically
        **[2] review** — Go through each issue one by one
        **[3] skip** — Continue without fixing
        {if any issue has needs_code_check}
        **[4] check-code** — Verify by inspecting the codebase
        {/if}

        Choose an action [1/2/3{if check-code available}/4{/if}]:
      </output>
    </check>
  </step>

  <step n="10" title="Process User Choice">
    <check if="response == 1 (fix-all)">
      <goto step="11"/>
    </check>

    <check if="response == 2 (review)">
      <goto step="12"/>
    </check>

    <check if="response == 3 (skip)">
      <output>Skipping integrity fixes. Issues may cause unexpected behavior.</output>
      <exit/>
    </check>

    <check if="response == 4 (check-code)">
      <goto step="13"/>
    </check>
  </step>

  <step n="11" title="Apply All Fixes">
    <action>For each issue with a fix:</action>

    <fix_actions>
      <fix for="orphaned_intent">
        Read brief.md frontmatter, add intent to state.yaml with status: pending
      </fix>

      <fix for="orphaned_work_item">
        Read work item frontmatter, add to parent intent in state.yaml
      </fix>

      <fix for="orphaned_run">
        Parse run.md, determine if complete or incomplete
        If complete: add to runs.completed
        If incomplete: offer to add to runs.active or delete
      </fix>

      <fix for="missing_intent_file">
        Remove intent from state.yaml (data loss warning)
        Or: Create placeholder brief.md from state data
      </fix>

      <fix for="status_mismatch">
        Update state.yaml status to expected value
      </fix>

      <fix for="intent_status_mismatch">
        Update intent status in state.yaml
      </fix>

      <fix for="frontmatter_drift">
        Update work item frontmatter to match state.yaml
      </fix>

      <fix for="incomplete_run_artifacts">
        Mark run as incomplete in state, or generate missing artifacts
      </fix>

      <fix for="stale_run">
        User must decide: resume, abandon, or check code
      </fix>
    </fix_actions>

    <output>
      ## Fixes Applied

      {for each fix applied}
      ✓ {description}
      {/for}

      {if any fixes skipped}
      ⏭️ Skipped (requires user decision):
      {for each skipped}
      - {description}
      {/for}
      {/if}
    </output>

    <goto step="14"/>
  </step>

  <step n="12" title="Interactive Review">
    <action>For each issue:</action>

    <output>
      ## Issue {n} of {total}

      **Type**: {type}
      **Severity**: {severity}
      **Location**: {location}

      ### Details
      {full_description}

      ### Suggested Fix
      {fix_suggestion}

      ---

      **[y]** Apply fix
      **[n]** Skip this issue
      **[c]** Check codebase for this item
      **[q]** Quit review (remaining issues skipped)

      Choice [y/n/c/q]:
    </output>

    <check if="response == y">
      <action>Apply fix for this issue</action>
      <output>✓ Fixed: {description}</output>
    </check>

    <check if="response == c">
      <action>Invoke code check for this specific item</action>
      <goto_substep>code-check for {item}</goto_substep>
    </check>

    <check if="response == q">
      <output>Review ended. {remaining} issues skipped.</output>
      <goto step="14"/>
    </check>

    <action>Continue to next issue</action>
  </step>

  <step n="13" title="Code Verification">
    <critical>
      This is a BEST EFFORT verification. AI will look for evidence
      but may not catch everything. User should confirm findings.
    </critical>

    <ask>
      I'll check the codebase for evidence that work items were completed.
      This involves reading work item acceptance criteria and looking for
      matching implementations.

      Which items should I check?

      {for each item with needs_code_check}
      **[{n}]** {work_item_title}
      {/for}
      **[a]** All items
      **[b]** Back to actions

      Choice:
    </ask>

    <substep n="13a" title="Verify Single Work Item">
      <action>Read work item file: .specs-fire/intents/{intent}/work-items/{id}.md</action>
      <action>Extract acceptance criteria</action>
      <action>Extract expected files/endpoints/components mentioned</action>

      <verification_checks>
        <check title="File Existence">
          Look for files mentioned in the work item description
          Example: "Create src/auth/login.ts" → check if file exists
        </check>

        <check title="Test Existence">
          Look for test files for the component
          Pattern: {filename}.test.ts, {filename}.spec.ts, __tests__/{filename}.ts
        </check>

        <check title="Implementation Markers">
          If file exists, do a quick scan for expected functions/classes
          Example: Work item mentions "login endpoint" → look for login handler
        </check>
      </verification_checks>

      <output>
        ## Code Verification: {work_item_title}

        ### Expected (from acceptance criteria)
        {list acceptance criteria}

        ### Found in Codebase
        {for each check}
        {check_result_icon} {check_description}
        {/for}

        ### Assessment
        {if all checks pass}
        ✅ **Likely Complete** — Implementation evidence found
        Recommend: Mark as completed in state.yaml
        {else if some checks pass}
        🟡 **Partially Complete** — Some evidence found
        Missing: {missing_items}
        Recommend: Review manually or continue implementation
        {else}
        ❌ **Not Found** — No implementation evidence
        Recommend: Keep as pending, implementation needed
        {/if}

        ---

        Apply this assessment? [y/n]:
      </output>

      <check if="response == y">
        <action>Update state.yaml based on assessment</action>
      </check>
    </substep>
  </step>

  <step n="14" title="Log Maintenance">
    <check if="any fixes were applied">
      <action>Append to .specs-fire/maintenance-log.md (create if needed):</action>

      <log_entry>
        ## {ISO-8601-timestamp} - Integrity Check

        **Triggered by**: status skill validation

        | Issue | Fix Applied | Details |
        |-------|-------------|---------|
        {for each fix}
        | {type} | {fix_description} | {location} |
        {/for}

        ---
      </log_entry>

      <output>
        Changes logged to: .specs-fire/maintenance-log.md
      </output>
    </check>
  </step>

  <step n="15" title="Final Summary">
    <output>
      ## Status Check Complete

      {if fixes applied}
      **Fixes Applied**: {fix_count}
      **Issues Remaining**: {remaining_count}
      {/if}

      {if all clean}
      ✅ Project state is consistent and ready for work.
      {else}
      ⚠️ Some issues remain unresolved. Run `/specsmd-fire status` again to review.
      {/if}

      ---

      **Next**: {suggest next action based on current state}
    </output>
  </step>
</flow>

<!-- ═══════════════════════════════════════════════════════════════════════════ -->
<!-- ISSUE TYPE REFERENCE                                                         -->
<!-- ═══════════════════════════════════════════════════════════════════════════ -->

<issue_types>

| Type | Severity | Auto-fixable | Description |
|------|----------|--------------|-------------|
| orphaned_intent | warning | yes | Intent on disk but not in state.yaml |
| orphaned_work_item | warning | yes | Work item on disk but not in state.yaml |
| orphaned_run | warning | partial | Run folder on disk but not tracked |
| missing_intent_file | error | partial | Intent in state but file missing |
| missing_work_item_file | error | partial | Work item in state but file missing |
| missing_run_folder | error | no | Completed run in state but folder missing |
| status_mismatch | error | yes | Work item status doesn't match run history |
| status_unverifiable | warning | no | Status can't be verified from run data |
| intent_status_mismatch | error | yes | Intent status inconsistent with work items |
| incomplete_run_artifacts | warning | partial | Run missing required artifacts |
| active_run_missing | error | no | Active run folder doesn't exist |
| active_run_corrupted | error | no | Active run folder missing run.md |
| stale_run | info | no | Active run is old, may be abandoned |
| interrupted_run | warning | no | Run appears stopped mid-execution |
| frontmatter_drift | info | yes | Frontmatter status differs from state |

</issue_types>

<!-- ═══════════════════════════════════════════════════════════════════════════ -->
<!-- EXAMPLE OUTPUT                                                               -->
<!-- ═══════════════════════════════════════════════════════════════════════════ -->

<example_output>

  ```
  # FIRE Status

  **Project**: my-saas-app
  **Workspace**: brownfield / monolith
  **Autonomy**: balanced
  **Version**: 0.1.8

  ## Intents

  ### User Authentication [in_progress]

  | Work Item | Status | Complexity | Mode |
  |-----------|--------|------------|------|
  | login-endpoint | completed | medium | confirm |
  | session-management | in_progress | medium | confirm |
  | password-reset | pending | high | validate |

  ## Active Runs

  - **Run**: run-fabriqa-2026-002 | **Scope**: single
  - **Current Item**: session-management
  - **Started**: 2026-01-19T10:30:00Z

  ## Quick Stats

  - Intents: 1 (0 completed)
  - Work Items: 3 (1 completed)
  - Runs: 1 completed

  ---

  ## ⚠️ Integrity Issues Detected

  Found 3 issue(s) requiring attention:

  | # | Type | Location | Issue | Suggested Fix |
  |---|------|----------|-------|---------------|
  | 1 | 🟡 | run-fabriqa-2026-002 | Run started 3 days ago, may be stale | Resume or abandon |
  | 2 | 🔵 | login-endpoint | Frontmatter says 'pending' but state says 'completed' | Sync frontmatter |
  | 3 | 🟡 | analytics-dashboard.md | Work item on disk but not tracked | Add to state.yaml |

  **Severity**: 🔴 Error | 🟡 Warning | 🔵 Info

  ---

  ### Actions

  **[1] fix-all** — Apply all recommended fixes automatically
  **[2] review** — Go through each issue one by one
  **[3] skip** — Continue without fixing
  **[4] check-code** — Verify by inspecting the codebase

  Choose an action [1/2/3/4]:
  ```

</example_output>

<success_criteria>
  <criterion>State file read successfully</criterion>
  <criterion>All intents and work items displayed</criterion>
  <criterion>Active run status shown</criterion>
  <criterion>Quick stats accurate</criterion>
  <criterion>File system scanned for all artifacts</criterion>
  <criterion>Orphaned artifacts detected (disk → state)</criterion>
  <criterion>Missing files detected (state → disk)</criterion>
  <criterion>Status cascade validated (work items → intents)</criterion>
  <criterion>Run artifact completeness checked</criterion>
  <criterion>Stale/interrupted runs detected</criterion>
  <criterion>Frontmatter sync checked</criterion>
  <criterion>Issues reported in clear table format</criterion>
  <criterion>User given choice: fix-all, review, skip, check-code</criterion>
  <criterion>Fixes logged to maintenance-log.md</criterion>
  <criterion>Code verification available for ambiguous cases</criterion>
</success_criteria>
