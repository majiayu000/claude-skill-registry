---
name: config-sync-cli-workflow
description: Orchestrate multi-target CLI configuration synchronization using config-sync phase runners and planners.
allowed-tools:
  - Bash(commands/config-sync/sync-cli.sh *)
  - Bash(commands/config-sync/lib/phases/*.sh *)
  - Bash(commands/config-sync/lib/planners/*.sh *)
metadata:
  capability-level: 2
  layer: execution
  mode: stateful-orchestration
  style: tool-first
  tags:
    - toolchain
    - workflow
    - config-sync
  usage:
    - "/config-sync/sync-cli --action=* across CLI targets."
    - "Replay existing sync plan files for CLI synchronization."
  validation:
    - "Normalize parameters against .claude/commands/config-sync/settings.json."
    - "Precede all write phases with backup and permission checks."
    - "Enforce phase order and behavior defined in sync-cli.md."
---

## Purpose

Drive the multi-target config-sync CLI workflow using the defined phase pipeline with consistent backup and audit behavior.

## IO Semantics

Input: CLI arguments, settings.json parameters, existing plan files, target tool configuration directories.  
Output: Execution plans, phase execution metadata, run logs, and backup records.  
Side Effects: Writes plan files, creates backups under backup directories, updates target configuration files when write phases execute.

## Deterministic Steps

1. Parameter Normalization
   - Read CLI arguments and merge with settings.json.
   - Resolve target list and component selection.

2. Plan Creation or Loading
   - Create a new plan describing collect, analyze, plan, prepare, adapt, execute, verify, cleanup, report phases; or load an existing plan file.

3. Phase Execution
   - Run collect and analyze to discover current configuration state.
   - Run plan and prepare to build and validate the execution plan, including backup locations.
   - Run adapt and execute to apply changes for selected targets and components.
   - Run verify, cleanup, and report to validate results, manage temporary artifacts, and emit summaries.

4. Result Persistence
   - Persist plan updates, run metadata, and logs into backup directories.
