---
name: route
description: Analyze project state and route user to the appropriate agent based on current context.
version: 1.0.0
---

<objective>
Analyze project state and route user to the appropriate agent.
</objective>

<triggers>
  - User runs `/specsmd-fire` on initialized project
  - After any agent completes its task
</triggers>

<llm critical="true">
  <mandate>ALWAYS scan file system for intents/work-items not in state.yaml</mandate>
  <mandate>FILE SYSTEM is source of truth — state.yaml may be incomplete</mandate>
  <mandate>Route based on VERIFIED state, not assumptions</mandate>
</llm>

<flow>
  <step n="1" title="Discover and Read State">
    <action>Read .specs-fire/state.yaml</action>

    <file_system_scan critical="true">
      Use these EXACT glob patterns:

      <pattern purpose="Find intent briefs">
        .specs-fire/intents/*/brief.md
      </pattern>

      <pattern purpose="Find work items">
        .specs-fire/intents/*/work-items/*.md
      </pattern>

      Work items are {work-item-id}.md files directly in work-items/ folder.
    </file_system_scan>

    <action>Reconcile: add discovered items to state as pending</action>
    <action>Parse current project state</action>
  </step>

  <step n="2" title="Check Active Run">
    <check if="runs.active is not empty">
      <output>
        Resuming active run: {runs.active[0].id}
        Scope: {runs.active[0].scope}
        Current item: {runs.active[0].current_item}
        Progress: {completed_count}/{total_count} items
      </output>
      <route_to>builder-agent (run-execute)</route_to>
      <stop/>
    </check>
  </step>

  <step n="3" title="Check Pending Work Items">
    <action>Find work items with status == pending across all intents</action>
    <check if="pending work items exist">
      <output>
        **{pending_count} pending work items** found across {intent_count} intent(s).

        Plan run scope and start execution? [Y/n]
      </output>
      <check if="response == y">
        <route_to>builder-agent (run-plan)</route_to>
      </check>
      <stop/>
    </check>
  </step>

  <step n="4" title="Check Active Intent">
    <action>Find intents with status == in_progress</action>
    <check if="active intent has no work items">
      <output>
        Intent "{intent.title}" needs decomposition.
        Routing to Planner to create work items.
      </output>
      <route_to>planner-agent (work-item-decompose)</route_to>
      <stop/>
    </check>
    <check if="all work items completed">
      <action>Mark intent as completed</action>
      <output>
        Intent "{intent.title}" completed!

        Work items delivered:
        {list completed work items}

        Ready for next intent? [Y/n]
      </output>
    </check>
  </step>

  <step n="5" title="No Active Work">
    <output>
      No active work. Ready for a new intent.

      What do you want to build?
    </output>
    <route_to>planner-agent (intent-capture)</route_to>
  </step>
</flow>

<routing_decision_tree>

  ```
  state.yaml + file system scan
      │
      ├── runs.active? ─────────────> Builder (run-execute, resume)
      │
      ├── pending work items? ──────> Builder (run-plan, then execute)
      │
      ├── intent without work items? > Planner (work-item-decompose)
      │
      └── no active intents ────────> Planner (intent-capture)
  ```

</routing_decision_tree>

<context_passed_to_agents>
  **To Planner:**

  ```yaml
  context:
    action: intent-capture | work-item-decompose
    intent_id: {if decomposing}
  ```

  **To Builder:**

  ```yaml
  context:
    action: run-plan | run-execute | resume
    pending_items: [{list of pending work items}]  # for run-plan
    run_id: {if resuming}
  ```

</context_passed_to_agents>

<success_criteria>
  <criterion>File system scanned for untracked intents/work-items</criterion>
  <criterion>State reconciled with file system</criterion>
  <criterion>Correct agent selected based on state</criterion>
  <criterion>Context passed to target agent</criterion>
</success_criteria>
