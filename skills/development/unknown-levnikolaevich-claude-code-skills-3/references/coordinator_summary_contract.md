<!-- SOURCE-OF-TRUTH: shared/references/coordinator_summary_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Coordinator Summary Contract

Runtime summary envelope for cross-skill routing. Domain fields live in the active family runtime or summary contract.

## Hard Rules

- Write summaries only under the active run output directory or the explicit caller-provided summary path.
- Never write outside `.hex-skills/runtime-artifacts/runs/{run_id}/` unless the active skill contract names another path.
- Resolve the target path before writing and reject absolute or traversal paths from user input.
- Include this envelope; add only active-family fields.

## Shared Envelope

Required fields:

```json
{
  "schema_version": "1.0",
  "run_id": "string",
  "skill": "string",
  "status": "completed|partial|failed|skipped",
  "summary_type": "string",
  "artifacts": [],
  "findings": [],
  "next_actions": []
}
```

Load only the active family contract for specialized fields.
