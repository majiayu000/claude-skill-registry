<!-- SOURCE-OF-TRUTH: shared/references/environment_state_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Environment State Contract

Project-scoped runtime contract for `.hex-skills/environment_state.json`. Load only when reading or writing agent availability, provider routing, research fallback, setup health, hook mode, or Codex skill-root health.

## Location

```text
{project_root}/.hex-skills/environment_state.json
```

Rules:
- Never read or write environment state outside the current target project root.
- Missing file means default-enabled environment with `task_management.provider = "file"`.
- Malformed JSON is a deterministic contract error.
- Schema details are writer/runtime-validator assets owned by environment setup skills; routine readers use only this contract.

## Reader Fields

Routine readers need only:

```json
{
  "agents": {
    "claude": { "available": true, "disabled": false },
    "codex": { "available": true, "disabled": false }
  },
  "task_management": {
    "provider": "file",
    "status": "active",
    "fallback": "file",
    "linear": {},
    "github": {},
    "fallback_metadata": {}
  },
  "research": {
    "provider": "web_search",
    "fallback_chain": []
  }
}
```

## Hard Rules

- `agents.{name}.disabled=true` means the agent must not be probed or launched.
- `task_management.provider` selects provider operations; use `references/storage_mode_detection.md` after reading it.
- On provider auth/rate-limit/transport/tool failure, set `provider="file"`, keep `status="active"`, and record `fallback_metadata`.
- Tool failures must not become domain findings unless there is independent domain evidence.
- Codex skill-root health follows `references/agent_skill_roots_contract.md` only when the skill audits or repairs Codex discovery.

## Writer Fields

Writers may populate only relevant sections: `agents`, `task_management`, `research`, `claude_md`, `assessment`, `hooks`, `ide_extension`.

## Reader Pattern

1. Read `.hex-skills/environment_state.json`.
2. If missing, default to `task_provider="file"` and all agents enabled.
3. If malformed, fail with a contract error.
4. Extract `task_provider = task_management.provider || "file"`.
5. Use `storage_mode_detection.md` for provider operations.

**Version:** 3.1.0
**Last Updated:** 2026-04-07
