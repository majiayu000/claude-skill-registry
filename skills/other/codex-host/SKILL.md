---
name: codex-host
description: Run the great_cto controlled Codex lifecycle with controller-owned writes, verifier evidence, human gates and optional artifact release.
when_to_use: Use when the user asks Codex to run or inspect a full great_cto pipeline rather than only use an individual skill.
effort: high
allowed-tools: Read, Bash
---

# Controlled Codex host

Use the supported CLI entrypoint. Do not imitate Claude Code hooks or manually
chain roles: the controller reads `shared/pipeline.toml`, persists the cursor and
owns every write and gate transition.

## Preflight

```sh
great-cto codex-host doctor
great-cto codex-host list --dir /absolute/project
```

`doctor.state=blocked` means do not start. Docker may be unavailable when no
checks/release policy is requested; GitHub CLI may be unavailable when the local
adapter is used. The run store must not be group/world accessible.

## Start

Policies must be operator-owned absolute files outside the worker project.
Allowed paths are explicit controller write boundaries.

```sh
great-cto codex-host start \
  --dir /absolute/project \
  --prompt "the requested outcome" \
  --allow src,tests,docs \
  --checks-policy /absolute/operator/checks.json \
  --release-policy /absolute/operator/release.json
```

Read the returned `status`, `pending` and `release` object. Never treat exit 2 as
success: it means a gate, manual action or blocked evidence requires attention.

## Gates and recovery

Show the operator the exact gate/release summary and wait for explicit approval.
Then pass back the controller-issued token; never synthesize or persist one in a
project file.

```sh
great-cto codex-host approve RUN_UUID --token GATE_TOKEN
great-cto codex-host approve-release RUN_UUID --token RELEASE_TOKEN
great-cto codex-host resume RUN_UUID
```

Use `recover` only after inspecting the recorded reason. Recovery reuses the
same candidate and refuses unknown partial writes. `cancel` revokes unexecuted
approval but does not delete external audit evidence.

## Release boundary

The local and GitHub Release adapters publish immutable artifacts and declare
`activation: none`. They do not deploy traffic. Local rollback means selecting
a previous directory; GitHub rollback is a newly gated superseding release.
Production activation needs a separate adapter and approval contract.

Detailed policy schemas and limitations are in `docs/HOST-CODEX.md`.
