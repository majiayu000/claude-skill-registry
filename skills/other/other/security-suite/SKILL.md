---
name: security-suite
description: 'Composable binary security suite for static analysis, dynamic tracing, contract capture, baseline drift, and policy gating. Triggers: "binary security", "reverse engineer binary", "black-box binary test", "behavioral trace", "baseline diff", "security suite".'
metadata:
  tier: execution
  dependencies: []
---

# Security Suite

> **Purpose:** Provide composable, repeatable security/internal-testing primitives for authorized binaries.

This skill separates concerns into primitives so security workflows stay testable and reusable.

## Guardrails

- Use only on binaries you own or are explicitly authorized to assess.
- Do not use this workflow to bypass legal restrictions or extract third-party proprietary content without authorization.
- Prefer behavioral assurance and policy gating over ad-hoc one-off reverse-engineering.

## Primitive Model

1. `collect-static` — file metadata, runtime heuristics, linked libraries, embedded archive signatures.
2. `collect-dynamic` — sandboxed execution trace (processes, file changes, network endpoints).
3. `collect-contract` — machine-readable behavior contract from help-surface probing.
4. `compare-baseline` — current vs baseline contract drift (added/removed commands, runtime change).
5. `enforce-policy` — allowlist/denylist gates and severity-based verdict.
6. `run` — thin orchestrator that composes primitives and writes suite summary.

## Quick Start

Single run (default dynamic command is `--help`):

```bash
python3 skills/security-suite/scripts/security_suite.py run \
  --binary "$(command -v ao)" \
  --out-dir .tmp/security-suite/ao-current
```

Baseline regression gate:

```bash
python3 skills/security-suite/scripts/security_suite.py run \
  --binary "$(command -v ao)" \
  --out-dir .tmp/security-suite/ao-current \
  --baseline-dir .tmp/security-suite/ao-baseline \
  --fail-on-removed
```

Policy gate:

```bash
python3 skills/security-suite/scripts/security_suite.py run \
  --binary "$(command -v ao)" \
  --out-dir .tmp/security-suite/ao-current \
  --policy-file skills/security-suite/references/policy-example.json \
  --fail-on-policy-fail
```

## Recommended Workflow

1. Capture baseline on known-good release.
2. Run suite on candidate binary in CI.
3. Compare against baseline and enforce policy.
4. Block promotion on failing verdict.

## Output Contract

All outputs are written under `--out-dir`:

- `static/static-analysis.json`
- `dynamic/dynamic-analysis.json`
- `contract/contract.json`
- `compare/baseline-diff.json` (when baseline supplied)
- `policy/policy-verdict.json` (when policy supplied)
- `suite-summary.json`

This output structure is intentionally machine-consumable for CI gates.

## Policy Model

Use `skills/security-suite/references/policy-example.json` as a starting point.

Supported checks:

- `required_top_level_commands`
- `deny_command_patterns`
- `max_created_files`
- `forbid_file_path_patterns`
- `allow_network_endpoint_patterns`
- `deny_network_endpoint_patterns`
- `block_if_removed_commands`
- `min_command_count`

## Technique Coverage

This suite is designed for broad binary classes, not just CLI metadata:

- static runtime/library fingerprinting
- sandboxed behavior observation
- command/contract capture
- drift classification
- policy enforcement and CI verdicting

It is intentionally modular so you can add deeper primitives later (syscall tracing, SBOM attestation verification, fuzz harnesses) without rewriting the workflow.

## Validation

Run:

```bash
bash skills/security-suite/scripts/validate.sh
```

Smoke test (recommended):

```bash
python3 skills/security-suite/scripts/security_suite.py run \
  --binary "$(command -v ao)" \
  --out-dir .tmp/security-suite-smoke \
  --policy-file skills/security-suite/references/policy-example.json
```

## Examples

### Scenario: Capture a Baseline and Gate a New Release

**User says:** `/security-suite run --binary $(command -v ao) --out-dir .tmp/security-suite/ao-v2.4`

**What happens:**
1. The suite runs static analysis (file metadata, linked libraries, embedded archive signatures), dynamic tracing (sandboxed `--help` execution observing processes, file changes, network endpoints), and contract capture against the `ao` binary.
2. It writes `static/static-analysis.json`, `dynamic/dynamic-analysis.json`, `contract/contract.json`, and `suite-summary.json` under the output directory.

**Result:** A complete baseline snapshot is captured for `ao` v2.4, ready to be used as `--baseline-dir` for future release comparisons.

### Scenario: CI Regression Gate With Baseline and Policy

**User says:** `/security-suite run --binary ./bin/ao-candidate --out-dir .tmp/ao-candidate --baseline-dir .tmp/security-suite/ao-v2.4 --policy-file skills/security-suite/references/policy-example.json --fail-on-removed --fail-on-policy-fail`

**What happens:**
1. The suite runs all three collection primitives on the candidate binary, then compares the resulting contract against the v2.4 baseline to produce `compare/baseline-diff.json` with any added, removed, or changed commands.
2. It evaluates the policy file checks (required commands, denied patterns, network allowlists, file limits) and writes `policy/policy-verdict.json` with a pass/fail verdict.

**Result:** The suite exits non-zero if any commands were removed or a policy check failed, blocking the candidate from promotion in the CI pipeline.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Suite exits non-zero with no clear finding | `--fail-on-removed` or `--fail-on-policy-fail` triggered on a legitimate change | Review `compare/baseline-diff.json` and `policy/policy-verdict.json` to identify the specific delta, then update the baseline or policy file accordingly. |
| `dynamic/dynamic-analysis.json` is empty or minimal | Binary requires arguments beyond `--help`, or sandbox blocked execution | Supply a custom dynamic command if supported, or verify the binary runs in the sandboxed environment (check permissions, missing shared libraries). |
| `contract/contract.json` shows zero commands | The binary does not expose a `--help` surface or uses a non-standard help flag | Verify the binary supports `--help`; for binaries with unusual help interfaces, run `collect-contract` separately with the correct invocation. |
| Policy verdict fails on `deny_command_patterns` | A new subcommand matches a deny regex in the policy file | Either rename the subcommand or update `deny_command_patterns` in your policy JSON to exclude the legitimate pattern. |
| `baseline-diff.json` not generated | `--baseline-dir` was not provided or points to a missing directory | Ensure the baseline directory exists and contains a valid `contract/contract.json` from a prior run. |
