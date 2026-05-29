---
name: run-status
description: Display current run status and progress. Shows work item, mode, duration, and files changed.
version: 1.0.0
---

<objective>
Display current run status and progress.
</objective>

<triggers>
  - User asks about run status
  - During long-running execution
</triggers>

<flow>
  <step n="1" title="Check Active Run">
    <action>Read state.yaml for runs.active[] array</action>
    <check if="no active run">
      <output>
        No active run. Last completed run: {last-run-id}
      </output>
      <stop/>
    </check>
  </step>

  <step n="2" title="Display Status">
    <output>
      ## Run Status: {run-id}

      **Work Item**: {title}
      **Intent**: {intent-title}
      **Mode**: {mode}
      **Started**: {started}
      **Duration**: {elapsed}

      ### Progress

      - [x] Initialize run
      - [x] Load context
      {checkpoint status}
      - [{status}] Execute implementation
      - [ ] Run tests
      - [ ] Generate walkthrough

      ### Files Changed So Far

      Created: {created-count}
      Modified: {modified-count}

      ### Recent Activity

      {last 5 actions}
    </output>
  </step>
</flow>

<example_output>

  ```
  ## Run Status: run-fabriqa-2026-003

  **Work Item**: Add session management
  **Intent**: User Authentication
  **Mode**: confirm
  **Started**: 2026-01-19T10:30:00Z
  **Duration**: 12 minutes

  ### Progress

  - [x] Initialize run
  - [x] Load context
  - [x] Plan approved (Checkpoint 1)
  - [~] Execute implementation
  - [ ] Run tests
  - [ ] Generate walkthrough

  ### Files Changed So Far

  Created: 2
  Modified: 1

  ### Recent Activity

  - Created src/auth/session.ts
  - Created src/auth/session.test.ts
  - Modified src/auth/index.ts
  ```

</example_output>

<success_criteria>
  <criterion>Current run status displayed</criterion>
  <criterion>Progress indicators accurate</criterion>
  <criterion>Files changed shown</criterion>
</success_criteria>
