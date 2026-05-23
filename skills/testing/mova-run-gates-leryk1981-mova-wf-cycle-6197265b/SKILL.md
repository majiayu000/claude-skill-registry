---
name: "MOVA: run gates (wrapper)"
description: "Runs npm validate/test/smoke gates and emits a JSON gate report with log paths."
when_to_use:
  - "Need fresh validation/test/smoke evidence before merging or handing off to Ops"
inputs:
  - kind: none
    schema: "n/a (drives repo npm scripts directly)"
outputs:
  - kind: json
    schema: "artifacts/run_gates/<timestamp>/run_gates_report.json"
deterministic: true
---

## Command
`node .codex/skills/mova_run_gates/scripts/run.mjs`

## Notes
- Wrapper runs `npm run validate`, `npm test`, and `npm run smoke:wf_cycle`, storing logs under `artifacts/run_gates/<timestamp>/`.
- The JSON report contains status/duration/log path per gate and is also saved next to the logs for evidence uploads.
- If a step fails the remaining gates are marked `skipped`; fix the failure before relaunching for a clean PASS sweep.
