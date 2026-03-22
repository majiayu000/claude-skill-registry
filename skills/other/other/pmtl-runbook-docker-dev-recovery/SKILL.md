---
name: pmtl-runbook-docker-dev-recovery
description: PMTL_VN Docker recovery runbook. Use when Docker Desktop, compose-backed dev services, or local infrastructure stop booting correctly and the agent needs the documented recovery path instead of trial-and-error.
---

# PMTL Runbook Docker Dev Recovery

## Purpose

Provide the canonical PMTL dev-lane recovery path when Docker Desktop, compose-backed services, or local infrastructure stop booting correctly.

## Use When

- Docker Desktop is down, stuck, or cannot serve Compose commands.
- `infra/docker/compose.dev.yml` services fail to boot in local dev.
- The task is incident recovery for local/dev infra, not feature implementation.

## Required Inputs

- current failure symptom such as Docker unavailable, compose failure, or service unhealthy
- whether this is local/dev only or mixed with app/runtime failure
- any diagnostics already collected

## Expected Output

- A recovered Docker dev environment or a cleanly documented blocked state with diagnostics.
- No random edits to compose files or repo config before the documented recovery path is exhausted.

## Read First

- `infra/scripts/docker-recover.ps1`
- `docs/troubleshooting.md`
- `docs/runbooks.md`

## Execution Approach

1. Confirm Docker Desktop service availability.
2. Run the recovery script before touching compose files.
3. Re-check compose service health after the engine is ready.
4. Only then restart the PMTL dev stack.

## Command

```powershell
powershell -ExecutionPolicy Bypass -File infra/scripts/docker-recover.ps1
```

If Docker still does not come back, collect diagnostics instead of guessing.

## Verification

- Confirm `docker info` succeeds before retrying stack commands.
- Confirm `docker compose ... ps` shows the expected core services as running or healthy.
- Confirm the PMTL dev stack can boot again via the normal repo entrypoint, not just that Docker Desktop reopened.
- If recovery fails, stop and capture diagnostics rather than mutating compose or env files blindly.

## Quality Criteria

- Recovery follows the documented path instead of trial-and-error edits.
- The result is observable: Docker reachable, compose services responsive, PMTL stack restartable.
- Incident notes distinguish `Docker engine failure`, `compose wiring failure`, and `app boot failure`.

## Edge Cases

- Windows host restarts can leave Docker Desktop open but engine-unready.
- Compose may be healthy while one PMTL service still fails for app-specific reasons; at that point switch from Docker recovery to the relevant app/runtime lane.
- Do not treat production Docker guidance as interchangeable with this local/dev recovery skill.

## References

- `infra/scripts/docker-recover.ps1`
- `docs/troubleshooting.md`
- `docs/runbooks.md`
- `AGENTS.md`

## Pair with

- `pmtl-production-baseline` when the incident crosses from Docker into app runtime policy.
- `pmtl-automation-smoke-suite` after recovery when a smoke command is the fastest confidence check.
