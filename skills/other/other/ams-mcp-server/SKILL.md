---
name: ams-mcp-server
description: Operate and troubleshoot the AMS unified MCP server for roadmap learning, GSD project orchestration, task management, ACL, autonomous workflows, memory/RAG, and cryptographic audit verification. Use when user asks to run AMS tools, work with E:/AMS projects, bootstrap roadmap-to-project flows, verify orchestration dependencies, or diagnose MCP runtime issues.
---

# AMS MCP Server Skill

> Version: `3.3.0`
> Status: `Active`
> Updated: `2026-02-16`
> Module: `unified-mcp-root`

Use this skill to execute AMS flows safely and in the correct order.

## Hard Dependency Chains

Apply these chains strictly. Do not skip prerequisites.

1. System bootstrap chain
   - `unified_init` -> `unified_vitals` -> domain tools

2. Roadmap to project chain
   - `roadmap_export_to_gsd` -> `unified_set_project` -> `watcher_start`

3. Audit proof chain
   - `context_create` or `context_ensure` -> `audit_session_start` -> work tools -> `audit_verify_chain` -> `merkle_finalize` -> `merkle_root`

4. Workflow execution chain
   - `workflow_run` dry run first for new sequences
   - If failure policy is configured: retry/backoff/rollback must be honored

5. Restoration chain
   - `unified_backup` before risky operations
   - Then `unified_import` or `unified_restore`
   - Then `unified_vitals` and `audit_verify_chain` for post-check

## Startup Checklist

Run this at the beginning of each operational session.

1. `unified_init`
2. `unified_vitals`
3. `unified_help` (refresh available tools and conventions)
4. If project scoped work is expected, set project context:
   - `unified_set_project` or pass canonical `project_id`

## Intent to Tool Mapping

Use this mapping to pick tools quickly.

- Explore learning paths:
  - `roadmap_list`, `roadmap_get`, `roadmap_nodes`, `roadmap_node_get`

- Validate and repair roadmap content:
  - `roadmap_validate`, `roadmap_validate_all`, `roadmap_repair`, `roadmap_repair_all`

- Create project from roadmap:
  - `roadmap_export_to_gsd`
  - then `unified_set_project`
  - then `watcher_start` (optional)

- Manage tasks:
  - `task_create`, `task_create_batch`, `task_list`, `task_update`, `task_delete`
  - `task_eisenhower`, `task_next_actions`, `task_report`
  - `task_deps`, `task_link_roadmap`, `task_sync_to_gsd`

- Analyze content:
  - `analysis_search`, `analysis_similar`, `analysis_recommend`, `analysis_keywords`, `analysis_compare`
  - RAG: `analysis_rag_index`, `analysis_rag_search`, `analysis_rag_stats`

- Manage memory and retention:
  - `memory_pack`, `memory_get`, `memory_map`, `memory_verify`, `memory_bundle`, `memory_stats`
  - `memory_retention`, `memory_gc`, `rag_retention`, `rag_gc`

- Run autonomous pipeline:
  - `ams_autonomous_run`, `ams_autonomous_apply_changes`, `ams_session_list`, `ams_session_resume`, `ams_session_rollback`

- Operate orchestration and architecture controls:
  - `unified_orchestration`, `workflow_run`, `parallel_execute`
  - `unified_architecture`, `unified_metrics`, `unified_stats`

- Access control:
  - `acl_add_member`, `acl_remove_member`, `acl_list_members`, `acl_set_owner`

- Notifications and git operations:
  - `notify`, `git_checkpoint`, `git_auto_commit`

## Safety Rules

1. Always run `unified_vitals` before and after changes.
2. Always establish project context before project-scoped tools.
3. Never call `watcher_start` for a project that was not exported/initialized.
4. Use dry-run style operations first where available (`repair_all`, `gc`, import/export flows).
5. For autonomous apply mode, ensure environment policy allows it.
6. For audit-grade sessions, finalize Merkle proof before closing delivery.
7. If runtime state and tracked files diverge, stop and verify with `unified_metrics` and `unified_help`.

## Common Failure Patterns

- "Project not found"
  - Cause: missing export/init or wrong project context
  - Fix: run `roadmap_export_to_gsd`, then `unified_set_project`, then retry

- "Roadmap not found"
  - Cause: invalid roadmap id
  - Fix: run `roadmap_list` and use exact id

- "MCP connection/runtime issue"
  - Cause: config mismatch, missing node path, server boot failure
  - Fix: verify client MCP config and run `unified_vitals`

- "Chain verification failed"
  - Cause: broken session/action context linkage
  - Fix: inspect with `audit_get_actions`, re-check `context_*`, then `audit_verify_chain`

## Skill Execution Policy

When this skill is triggered:

1. Prefer deterministic tool sequences over ad-hoc calls.
2. Explain prerequisite insertion explicitly when user skips a required step.
3. Keep orchestration transparent: show what was auto-resolved and why.
4. Report concrete outputs: ids, counts, statuses, and next required step.
5. If a tool set changed, trust runtime discovery via `unified_help` over static counts.

## Reference Loading

Load references only when needed:

1. Read `references/workflow.md` for end-to-end scenario flow details.
2. Read `references/tools.md` when the user asks for tool-specific argument examples.
3. Read `references/errors.md` for troubleshooting paths and recovery commands.

If references conflict with runtime behavior, runtime behavior is the source of truth.
