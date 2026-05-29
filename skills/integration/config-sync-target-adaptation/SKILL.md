---
name: config-sync-target-adaptation
description: Coordinate target-specific adapters for Droid, Qwen, Codex, OpenCode, and Amp CLI environments.
allowed-tools:
  - Bash(commands/config-sync/adapters/*.sh *)
metadata:
  capability-level: 2
  layer: execution
  mode: target-adaptation
  style: tool-first
  tags:
    - toolchain
    - config-sync
    - adapters
  usage:
    - "Invoked from /config-sync/sync-cli when --target is set."
    - "Apply adapter logic for each target/component combination in the plan."
  validation:
    - "Driver uses sync-cli plan; adapters are not invoked ad-hoc."
    - "All target paths are resolved via get_target_config_dir/get_target_commands_dir/get_target_rules_dir in lib/common.sh, never by hard-coded home-relative paths."
    - "Each adapter enforces documented safety and permission constraints."
    - "Backups exist for all modified target configuration files."
---

## Purpose

Coordinate target-specific adapters so that config-sync applies correct rules, permissions, commands, settings, and memory updates for each CLI environment.

## IO Semantics

Input: Config-sync plan describing targets and components, adapter scripts under .claude/commands/config-sync/adapters, resolved target configuration and rules directories.  
Output: Adapter execution results and updated target configuration files per environment.  
Side Effects: Invokes adapter scripts that perform writes to target configuration directories; relies on existing backups created by higher-level workflow phases.

## Deterministic Steps

1. Adapter Selection
   - Read the config-sync plan to determine which targets and components require adapter execution.
   - Map each target to its corresponding adapter script.

2. Target Directory Resolution
   - Resolve configuration, rules, and commands directories using common helpers (get_target_config_dir, get_target_rules_dir, get_target_commands_dir).
   - Reject hard-coded home-relative paths in adapters.

3. Adapter Invocation
   - Execute adapter scripts for each target/component combination with required environment variables and paths.
   - Ensure adapters enforce documented safety and permission constraints.

4. Post-Execution Validation
   - Confirm that backups exist for all modified target configuration files.
   - Record adapter execution status into the plan or run metadata.
