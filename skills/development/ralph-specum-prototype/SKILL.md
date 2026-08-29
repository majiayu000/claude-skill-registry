---
name: ralph-specum-prototype
description: This skill should be used only when the user explicitly invokes `$ralph-specum-prototype`, or explicitly asks Ralph Specum in Codex to run, resume, quick-run, or cancel an optional prototype.
metadata:
  surface: helper
  action: prototype
---

# Ralph Specum Prototype

Coordinate one optional prototype overlay. Delegate source work to a child agent and keep the main Ralph phase unchanged until the recorded handoff.

## Load the contract

Derive `RALPH_CODEX_PLUGIN_ROOT` from this loaded skill: take the directory containing `SKILL.md`, then its parent `skills` directory, then the next parent. Never derive the plugin root from the project working directory.

Read `../../references/prototype-coordinator.md` from this skill directory completely before any prototype mutation. Treat it as the source of truth for direct, suggested, resume, quick, cancel, isolation, review, publication, and handoff behavior.

## Route the request

1. Resolve an explicit path, exact spec name, or `.current-spec` with `"$RALPH_CODEX_PLUGIN_ROOT/scripts/resolve_spec_paths.py"`. Use only the returned `basePath`, `specRoot`, settings, and warnings.
2. Parse one mode: direct by default, suggested with a return phase, resume by ID, quick, or cancel by ID.
3. Reconcile candidate and final records before reserving, resuming, reviewing, or publishing.
4. Use only these mechanics:
   - `"$RALPH_CODEX_PLUGIN_ROOT/scripts/locked_state.py"` for `activePrototypes` and every state mutation
   - `"$RALPH_CODEX_PLUGIN_ROOT/scripts/prototype_records.py"` for exact candidate bytes, review receipts, immutable publication, reconciliation, and downstream selection
   - `"$RALPH_CODEX_PLUGIN_ROOT/scripts/prototype_harness.py"` for deterministic control outcomes and retry metadata
5. Spawn internal builders with child-agent tools. Store only the returned `agentId`; wait with `wait_agent` and stop with `interrupt_agent`. Never use `create_thread` or a `threadId` for an internal builder.
6. Keep normal capture, dirty-path transfer, verdict, handoff, deletion, and remote actions under explicit user control. Let quick mode own its bounded choices and continue to design after every terminal outcome.

## Completion gate

Finish only after the coordinator contract verifies the immutable final bytes, removes the active entry through the locked helper, applies stale and handoff gates, and reports the local source disposition. Keep every remote pointer pending until the user authorizes that exact remote write.
