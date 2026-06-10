---
name: cli-doctoring-workflow
description: |-
  Use when designing or auditing CLI doctor commands, health checks, repair hints, and diagnostic UX.
  Triggers:
practices:
- pragmatic-programmer
- docs-as-code
- operational-diagnostics
hexagonal_role: supporting
consumes:
- cli-source
- command-help
- error-reports
- installation-docs
- support-history
produces:
- doctor-command-design
- diagnostic-audit
- repair-hint-plan
- health-check-contract
context_rel: []
skill_api_version: 1
user-invocable: false
context:
  window: inherit
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: topic
metadata:
  tier: judgment
  stability: stable
  dependencies: []
output_contract: "A doctor command design or audit that defines checks, failure classification, safe repair hints, output format, verification strategy, and user-centered diagnostic behavior."
---

# CLI Doctoring Workflow - diagnostics that move users forward

Use this skill when designing or reviewing a CLI `doctor`, `diagnose`,
`preflight`, or health-check command. The command should explain what it checked,
what failed, how confident it is, what the user can do next, and what evidence is
safe to share in a support request.

The goal is not to prove every part of a system. The goal is to catch common
environment and configuration failures early, give precise repair hints, and
avoid sending users into vague troubleshooting loops.

## Core Standard

A doctor command earns its place when it is:

- **Actionable:** every failure names the broken condition and the next useful
  step.
- **Bounded:** each check says what it can and cannot prove.
- **Safe:** diagnostics avoid secrets, destructive writes, and surprise network
  calls unless explicitly requested.
- **Fast by default:** the normal path should finish quickly; expensive checks
  require a flag.
- **Scriptable:** machines get stable exit codes and structured output.
- **Readable:** humans get concise status, grouped causes, and repair hints.

## When To Use This Skill

Use it for:

- Designing a new `doctor` or `diagnose` command.
- Auditing existing CLI health-check output.
- Adding preflight checks before install, login, sync, deploy, test, or run
  workflows.
- Turning recurring support issues into checks and repair hints.
- Reviewing whether diagnostics leak sensitive data or produce noisy advice.

Do not use it to hide real errors behind generic help text. If a primary command
can report a precise error directly, fix that command first and let doctor cover
cross-cutting environment checks.

## Inputs To Gather

Read enough of the project to identify real failure modes:

- CLI command tree, help text, and exit-code conventions.
- Install, login, config, update, and first-run paths.
- Runtime dependencies such as binaries, services, credentials, sockets,
  config files, ports, certificates, databases, and background daemons.
- Existing error messages, support tickets, issue reports, logs, and docs.
- CI, packaging, and release scripts that define supported environments.

Separate observed failures from guesses. A guessed check can be useful, but label
it as a proposed check until a real failure mode justifies it.

## Design Procedure

1. **Name the workflow being protected.** State the user task that doctor helps:
   install, authenticate, sync, deploy, serve, connect to a device, or repair a
   workspace.
2. **Map the failure chain.** List prerequisites in the order the user encounters
   them: binary present, version compatible, config readable, credentials valid,
   service reachable, permissions sufficient, data shape accepted.
3. **Choose checks with clear evidence.** Each check needs a probe, a pass
   condition, a failure condition, and a reason the check matters.
4. **Classify failures.** Use categories such as missing dependency,
   incompatible version, unavailable service, invalid credentials, corrupt
   config, permission denied, stale cache, unsupported platform, or unknown.
5. **Write repair hints.** Prefer exact commands or file paths. If a repair is
   risky, explain the risk and require user confirmation outside doctor.
6. **Define output modes.** Human output should be compact and grouped.
   Structured output should be stable JSON for automation and support bundles.
7. **Set exit semantics.** A clean bill exits 0. User-fixable failures exit a
   nonzero code distinct from internal doctor errors when the CLI already has an
   exit-code convention.
8. **Verify with fixtures.** Test passing, failing, partial, slow, offline, and
   redacted-output cases. Include at least one regression check from a real bug
   or support issue when available.

## Check Contract

Define each health check with this shape:

| Field | Purpose |
| --- | --- |
| `id` | Stable machine name, such as `config.readable` or `auth.token.valid`. |
| `scope` | Local, workspace, account, network, service, device, or update. |
| `probe` | What the command does to collect evidence. |
| `pass` | Exact condition that counts as healthy. |
| `fail` | Exact condition that counts as unhealthy. |
| `severity` | `error`, `warning`, or `info`; avoid more levels unless the CLI already uses them. |
| `confidence` | High when evidence proves the cause; lower when it is a symptom. |
| `repair` | User action, command, or documentation link that addresses the likely cause. |
| `redaction` | Data that must be hidden in human, JSON, logs, and support output. |
| `timeout` | Maximum wait time and fallback behavior for slow probes. |

If a check cannot produce a useful repair hint, reconsider whether it belongs in
the default doctor run.

## Output Shape

Human output should answer four questions:

1. What was checked?
2. What failed?
3. What should I do next?
4. What can I share safely if I need help?

Recommended human shape:

```text
Checking workspace
  OK   config.readable        Loaded ./tool.yaml
  FAIL auth.token.valid       Token expired 2026-06-01
       Fix: run `tool login` and retry `tool doctor`

Summary: 1 failure, 0 warnings, 3 passed
Next: fix the failed check above, then run `tool doctor` again
```

Recommended JSON shape:

```json
{
  "status": "fail",
  "summary": {"passed": 3, "warnings": 0, "failed": 1},
  "checks": [
    {
      "id": "auth.token.valid",
      "status": "fail",
      "severity": "error",
      "confidence": "high",
      "message": "Token is expired.",
      "repair": {"command": "tool login"},
      "redacted": true
    }
  ]
}
```

Keep JSON stable. Add fields; do not rename existing fields casually once users
or support tooling depend on them.

## Repair Hint Rules

- Give the shortest safe action that fixes the likely cause.
- Prefer commands the CLI owns over shell fragments that vary by platform.
- Include file paths only when they are relevant and safe to reveal.
- Do not print secrets, tokens, private URLs, full environment dumps, or raw
  headers.
- Mark destructive repairs as manual instructions unless the command has an
  explicit `--fix` mode with confirmation and dry-run behavior.
- When multiple causes are possible, say what evidence would distinguish them.

Avoid vague hints such as "check your configuration" unless followed by a
specific file, key, command, or expected value.

## Flags And Modes

Consider these modes when they fit the CLI:

- `--json` for stable machine-readable output.
- `--verbose` for extra evidence and timing.
- `--offline` to skip network checks without failing the whole run.
- `--network` or `--deep` for slower probes that are not safe as defaults.
- `--fix` only for reversible, well-scoped repairs.
- `--support-bundle` for redacted diagnostic evidence that users can attach to
  a ticket.

Default mode should be safe, quiet, and fast. Expensive or privacy-sensitive
checks must be opt-in.

## Audit Checklist

Use this checklist when reviewing an existing doctor command:

- The command starts with the workflow it is checking, not a wall of logs.
- Every failure has a stable check id, severity, cause, and repair hint.
- The output distinguishes warnings from failures.
- Checks are ordered in dependency order so early root causes do not cascade into
  confusing secondary failures.
- Network probes have timeouts and offline behavior.
- Secret redaction is tested, including structured output and support bundles.
- Exit codes match the CLI's documented convention.
- The default run is fast enough for users to try repeatedly.
- JSON output is deterministic enough for tests and automation.
- Documentation shows when to run doctor and what a healthy result looks like.

## Implementation Notes

- Build checks as small units with explicit inputs and outputs. This makes them
  testable and lets the CLI reuse them for preflight warnings.
- Prefer dependency injection for filesystem, environment, clock, network, and
  command execution probes.
- Treat probe failure as data. A probe that cannot run should produce a clear
  doctor result, not crash the whole command unless doctor itself is broken.
- Capture durations for slow checks, but keep timing out of golden output unless
  tests normalize it.
- Keep platform differences visible in the check contract instead of scattering
  platform branches through presentation code.

## Testing Strategy

Test at three levels:

- **Unit tests:** each check handles pass, fail, timeout, permission denied, and
  redaction cases.
- **Command tests:** human and JSON output stay stable for representative
  healthy and unhealthy fixtures.
- **Workflow tests:** at least one common support scenario ends with the repair
  hint that would have helped the user.

Golden output is useful for doctor commands, but normalize timestamps, user
paths, home directories, hostnames, ports, and durations before comparing.

## Output Specification

Return one of these artifacts:

- A doctor command design with check contracts, output modes, exit semantics,
  repair hints, and tests.
- A diagnostic audit with concrete findings, severity, affected checks, and
  suggested changes.
- A repair-hint plan that maps recurring symptoms to probes and safe next
  actions.

Include the assumptions you could not verify from the codebase or support
evidence.

## Quality Rubric

A CLI doctoring workflow passes when:

- A user can tell what failed and what to try next without reading source code.
- A maintainer can add or modify checks without rewriting presentation logic.
- Support can request structured output without receiving secrets.
- Automation can rely on stable JSON and meaningful exit codes.
- The command does not mask primary command errors that should be fixed at their
  source.
