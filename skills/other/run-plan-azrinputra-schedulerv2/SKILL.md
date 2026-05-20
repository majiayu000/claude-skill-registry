---
name: run-plan
description: Plan the scope of a run by discovering available work items and suggesting groupings. Invoked before run-execute.
version: 1.0.0
---

<objective>
Plan the scope of a run by discovering available work items and suggesting groupings.
</objective>

<triggers>
  - After work-item decomposition completes
  - User wants to start execution
  - Pending work items exist
</triggers>

<degrees_of_freedom>
  **MEDIUM** — Present smart grouping suggestions but let user choose scope.
</degrees_of_freedom>

<llm critical="true">
  <mandate>DISCOVER all available work — both in state.yaml AND file system</mandate>
  <mandate>FILE SYSTEM IS SOURCE OF TRUTH — state.yaml may be incomplete</mandate>
  <mandate>ALWAYS SCAN FILE SYSTEM — even if state.yaml shows all completed</mandate>
  <mandate>SUGGEST smart groupings based on mode, dependencies, and user history</mandate>
  <mandate>LEARN from user choices to improve future recommendations</mandate>
  <mandate>NEVER force a scope — always let user choose</mandate>
  <mandate>DEPENDENCIES = SEQUENTIAL EXECUTION, NOT SEPARATE RUNS</mandate>
</llm>

<critical_clarifications>
  <clarification title="Dependencies Mean Sequential Execution, NOT Separate Runs">
    When work items have dependencies:
    - They execute **sequentially within the SAME run**
    - They do **NOT** require separate runs
    - The dependent item waits for its dependency to complete before starting

    **Example**: If item 05 depends on item 04:
    - **CORRECT**: ONE run with both items, 04 executes first, then 05
    - **WRONG**: TWO separate runs
  </clarification>

  <clarification title="All Options Can Include Multiple Items Per Run">
    | Option | Items Per Run | Execution |
    |--------|---------------|-----------|
    | Single | 1 item | One at a time, separate runs |
    | Batch | Multiple items (same mode) | Sequential within run |
    | Wide | All compatible items | Sequential within run |
  </clarification>
</critical_clarifications>

<flow>
  <step n="1" title="Discover Available Work" critical="true">
    <critical>
      MUST scan file system BEFORE deciding if work exists.
      state.yaml may be missing intents or work items that exist on disk.
      DO NOT skip this step even if state.yaml shows all items completed.
    </critical>

    <substep n="1a" title="List All Intent Directories">
      <action>Use Glob to list: .specs-fire/intents/*/brief.md</action>
      <action>Extract intent IDs from directory names</action>
      <output>Found intent directories: {list}</output>
    </substep>

    <substep n="1b" title="List All Work Item Files">
      <action>Use Glob to list: .specs-fire/intents/*/work-items/*.md</action>
      <action>Extract work item IDs and their parent intents</action>
      <output>Found work item files: {list}</output>
    </substep>

    <substep n="1c" title="Compare with state.yaml">
      <action>Read state.yaml for known intents and work items</action>
      <action>Compare file system list against state.yaml entries</action>
    </substep>

    <substep n="1d" title="Reconcile Differences">
      <check if="intent directory exists but not in state.yaml">
        <output>
          **Discovered new intent**: {intent-id}
          (exists in file system but not in state.yaml)
        </output>
        <action>Parse brief.md frontmatter for intent metadata</action>
        <action>Add intent to state.yaml with status: active</action>
        <action>Scan its work-items/ folder</action>
      </check>

      <check if="work item file exists but not in state.yaml">
        <output>
          **Discovered new work item**: {work-item-id} in {intent-id}
          (exists in file system but not in state.yaml)
        </output>
        <action>Parse work item frontmatter for metadata</action>
        <action>Add work item to state.yaml with status: pending</action>
      </check>

      <check if="work item exists in both but status mismatch">
        <note>
          state.yaml is authoritative for status (tracks run history).
          Frontmatter status may be stale from initial creation.
        </note>
        <output>
          **Status mismatch**: {work-item-id}
          - state.yaml: {state_status}
          - frontmatter: {frontmatter_status}
          (Using state.yaml as authoritative)
        </output>
        <action if="frontmatter says pending but state says completed">
          Update work item frontmatter to match state.yaml
        </action>
        <action if="state says pending but frontmatter says completed">
          Flag for review - work may have been done outside FIRE
        </action>
      </check>

      <check if="state says completed but item is in runs.active[].work_items with current_phase != review">
        <output>
          **Suspect completion**: {work-item-id}
          - state.yaml status: completed
          - But current_phase: {current_phase} (not "review")
          - Item is still in active run {run-id}
          Resetting to in_progress — item was likely marked complete prematurely.
        </output>
        <action>Reset work item status to in_progress in state.yaml</action>
        <action>Update frontmatter to match</action>
      </check>

      <check if="in state.yaml but file missing">
        <output>Warning: {item} in state but file not found on disk</output>
      </check>
    </substep>

    <output>
      ## File System Scan Complete

      Intents on disk: {count}
      Intents in state.yaml: {count}
      Work items on disk: {count}
      Work items in state.yaml: {count}

      {if new items discovered}
      **Newly discovered (added to state.yaml)**:
      {list new items}
      {/if}
    </output>
  </step>

  <step n="2" title="Collect Pending Work Items">
    <action>Filter work items with status == pending</action>
    <action>Group by intent</action>
    <action>Note mode (after autonomy_bias applied) for each</action>
    <action>Identify dependencies within and across intents</action>

    <check if="no pending work items">
      <output>
        No pending work items found.

        Create a new intent? [Y/n]
      </output>
      <check if="response == y">
        <route_to>planner-agent (intent-capture)</route_to>
      </check>
      <stop/>
    </check>
  </step>

  <step n="3" title="Analyze Groupings">
    <action>Read workspace.autonomy_bias from state.yaml</action>
    <action>Read workspace.run_scope_preference from state.yaml (if exists)</action>

    <grouping_rules>
      <rule>Dependencies = SEQUENTIAL execution in SAME run (NOT separate runs)</rule>
      <rule>batch mode: Group items BY mode type (autopilot together, confirm together, etc.)</rule>
      <rule>wide mode: ALL items in ONE run regardless of mode (executed sequentially)</rule>
      <rule>Cross-intent items allowed in same run if compatible</rule>
      <rule>Validate mode items may benefit from batch (separate run with focused checkpoints)</rule>
    </grouping_rules>

    <generate_options>
      <option name="single">
        Each work item in its own run
        Total runs: {count of pending items}
        Maximum control, review after each item
      </option>

      <option name="batch">
        Group items BY MODE into separate runs
        Total runs: 1 per mode type present (e.g., autopilot run, confirm run, validate run)
        Less context switching within each run
        Example: 3 autopilot + 2 confirm + 1 validate = 3 runs
      </option>

      <option name="wide">
        ALL items in ONE run regardless of mode
        Total runs: 1
        Execute sequentially, pause at confirm/validate checkpoints
        Maximum throughput, minimum interruption between runs
      </option>
    </generate_options>
  </step>

  <step n="4" title="Present Options">
    <action>Determine recommended option based on:</action>
    <substep>autonomy_bias (autonomous→batch, controlled→single)</substep>
    <substep>run_scope_preference (user's historical choice)</substep>
    <substep>Number of pending items (few items→single is fine)</substep>

    <template_output section="options">
      ## Run Planning

      **Found**: {count} pending work items across {intent_count} intent(s)

      {for each intent with pending items}
      **{intent.title}**:
      {for each pending item}
      - {item.title} ({item.mode})
      {/for}
      {/for}

      {if dependencies exist}
      **Dependencies** (determines execution order):
      - {dependent_item} depends on {dependency_item}
      {/if}

      ---

      **How would you like to execute?**

      **[1] One at a time** — {single_count} separate runs
          Most controlled, review after each run

      **[2] Group by mode** — {batch_run_count} run(s)
          {autopilot_count} autopilot items → Run A (no pauses)
          {confirm_count} confirm items → Run B (1 checkpoint each)
          {validate_count} validate items → Run C (2 checkpoints each)
          Less context switching per run

      **[3] All in one** — 1 run with all {count} items (Recommended)
          Execute sequentially: {item1} → {item2} → ...
          Pause at confirm/validate checkpoints
          Maximum throughput

      Choose [1/2/3]:
    </template_output>
  </step>

  <step n="5" title="Process Choice">
    <check if="response == 1">
      <set>run_scope = single</set>
      <set>work_items_for_run = [first_pending_item]</set>
      <note>User will re-invoke run-plan after each run completes</note>
    </check>

    <check if="response == 2">
      <set>run_scope = batch</set>
      <action>Group pending items by mode:</action>
      <substep>autopilot_items = items where mode == autopilot</substep>
      <substep>confirm_items = items where mode == confirm</substep>
      <substep>validate_items = items where mode == validate</substep>
      <action>Start with first non-empty group (autopilot preferred)</action>
      <set>work_items_for_run = first_mode_group_in_dependency_order</set>
      <note>After this run, user re-invokes for next mode group</note>
    </check>

    <check if="response == 3">
      <set>run_scope = wide</set>
      <set>work_items_for_run = all_pending_items_in_dependency_order</set>
      <note>All items in one run, sequential execution</note>
    </check>
  </step>

  <step n="6" title="Learn Preference">
    <action>Update workspace.run_scope_preference in state.yaml</action>
    <action>Add to workspace.run_scope_history (keep last 10)</action>

    <history_entry>
      choice: {run_scope}
      items_count: {count}
      timestamp: {now}
    </history_entry>

    <note>
      After 3+ consistent choices, start pre-selecting that option
      and ask "Proceed with {preference}? [Y/n/change]" instead
    </note>
  </step>

  <step n="7" title="Confirm Run">
    <output>
      Starting run with {count} work item(s):

      {for each item in work_items_for_run}
      {index}. {item.title} ({item.mode})
      {/for}

      Items will execute sequentially within this run.
      {if any item is confirm or validate}
      Checkpoints will pause for approval at confirm/validate items.
      {/if}

      ---

      Begin execution? [Y/n]
    </output>
    <check if="response == y">
      <invoke_skill args="work_items_for_run, run_scope">run-execute</invoke_skill>
    </check>
  </step>
</flow>


<file_discovery_logic>

  ```
  .specs-fire/
  ├── intents/
  │   ├── user-auth/
  │   │   ├── brief.md           ← Parse frontmatter for intent metadata
  │   │   └── work-items/
  │   │       ├── login-endpoint.md   ← Parse for work item metadata
  │   │       └── session-mgmt.md
  │   └── analytics/
  │       ├── brief.md
  │       └── work-items/
  │           └── dashboard.md
  ```

  **Frontmatter parsing**:

- Extract `id`, `title`, `status` from YAML frontmatter
- If status missing, default to `pending`
- If in file but not state.yaml, add to state
</file_discovery_logic>

<grouping_algorithm>

  ```
  1. Collect all pending items with their modes
  2. Build dependency graph
  3. Sort items in dependency order (dependencies first)
  4. For "single" option:
     - Each item is its own run
  5. For "batch" or "wide" option:
     - ALL items in ONE run
     - Execution order follows dependency graph
     - Checkpoints pause at confirm/validate items
  ```

</grouping_algorithm>

<recommendation_logic>

  ```
  IF run_scope_history has 3+ same choices:
    pre_selected = most_common_choice

  ELSE IF autonomy_bias == autonomous:
    recommended = batch (all in one run)

  ELSE IF autonomy_bias == controlled:
    recommended = single

  ELSE: # balanced
    IF pending_count <= 2:
      recommended = single
    ELSE:
      recommended = batch
  ```

</recommendation_logic>

<success_criteria>
  <criterion>File system scanned for all intents and work items</criterion>
  <criterion>state.yaml reconciled with file system</criterion>
  <criterion>Run scope options presented to user</criterion>
  <criterion>User choice recorded for future recommendations</criterion>
  <criterion>run-execute invoked with selected work items</criterion>
</success_criteria>
