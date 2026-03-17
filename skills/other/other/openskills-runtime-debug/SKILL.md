---
name: openskills-runtime-debug
description: Diagnose openskills-runtime execution failures in sandboxed paths (Landlock, seatbelt, native script execution, wasm execution) and produce root-cause-first findings with minimal-risk remediation steps.
---

# OpenSkills Runtime Debug

Use this skill when debugging runtime failures in `runtime/` and execution paths used by `run_skill_target`, native scripts, or sandbox enforcement.

## Primary Targets

- `runtime/src/executor.rs`
- `runtime/src/native_runner.rs`
- `runtime/src/wasm_runner.rs`
- `runtime/src/permissions.rs`
- `runtime/tests/*sandbox*`
- `runtime/tests/seatbelt_tests.rs`

## Workflow

1. Reproduce with the smallest command that fails.
2. Classify failure bucket:
   - sandbox policy issue
   - feature/config mismatch
   - script/tool resolution issue
   - wasm runtime issue
3. Confirm behavior against tests and existing fallback logic.
4. Propose the smallest safe fix that preserves security boundaries.
5. Re-run focused tests, then broader runtime tests.

## Recommended Commands

```bash
cargo check -p openskills-runtime
cargo test -p openskills-runtime
cargo test -p openskills-runtime seatbelt_tests -- --nocapture
```

## Debug Heuristics

- Treat silent degradation in sandbox setup as high risk.
- Prefer explicit error propagation over ignored `Result`.
- If fallback behavior is intentional, confirm it is visible in logs and tests.
- Keep macOS and Linux behavior differences explicit in findings.

## Output Format

Return:

1. Root cause
2. Impact surface
3. Fix proposal
4. Verification evidence
5. Residual risks
