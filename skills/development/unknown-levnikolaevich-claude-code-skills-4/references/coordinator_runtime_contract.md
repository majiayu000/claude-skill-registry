<!-- SOURCE-OF-TRUTH: shared/references/coordinator_runtime_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Coordinator Runtime Contract

Deterministic runtime contract for stateful coordinators.

## Runtime State

Every coordinator runtime keeps project-scoped, run-scoped state:

| Artifact | Purpose |
|---|---|
| `manifest.json` | immutable run inputs |
| `state.json` | latest mutable snapshot |
| `checkpoints.json` | latest checkpoint per phase plus history |
| `history.jsonl` | append-only execution events |
| active pointer | current run indexed by `skill + identifier` |

Required vocabulary:
- `run_id`
- `skill`
- `identifier`
- `phase`
- `complete`
- `paused_reason`
- `pending_decision`
- `final_result`
- `resume_action`

## Status Rules

- `DONE` means orchestration completed correctly.
- `PAUSED` means deterministic intervention is required.
- Business failure may end in `DONE` if follow-up actions were checkpointed.
- Lifecycle status is not retry health; use `loop_health` only when deciding whether another attempt is useful.
- Transport, permission, auth, tool-missing, and rate-limit failures must not become domain verdicts without domain evidence.

## Pending Decision

Persist approvals and user choices as:

```json
{
  "kind": "preview_confirmation",
  "question": "Confirm preview?",
  "choices": ["confirm_preview", "cancel"],
  "default_choice": "confirm_preview",
  "context": {},
  "resume_to_phase": "PHASE_6_DELEGATE",
  "blocking": true
}
```

Resume must be derivable from runtime state, not chat memory.

## Runtime vs Public Outputs

- Runtime artifacts stay under `.hex-skills/runtime-artifacts/runs/{run_id}/...`.
- Public outputs are durable project artifacts such as docs, reports, or `.hex-skills/environment_state.json`.
- Do not merge runtime checkpoints into public output files.

## CLI Contract

Each runtime supports the deterministic lifecycle:

```bash
node <runtime>/cli.mjs start ...
node <runtime>/cli.mjs status ...
node <runtime>/cli.mjs checkpoint ...
node <runtime>/cli.mjs advance ...
node <runtime>/cli.mjs pause ...
node <runtime>/cli.mjs complete ...
```

Domain runtimes may add `record-*` commands, but worker outputs must be consumed through machine-readable summaries.

## Guards

- No phase transition without a checkpoint for the current phase.
- Malformed manifest, checkpoint payload, worker summary, or environment state fails validation before transition.
- `resume_action` must be derivable from state and checkpoints.
- Concurrent runs must not share active pointers or artifact directories.
- After `loop_health.should_pause=true`, pause with an actionable reason instead of retrying blindly.
