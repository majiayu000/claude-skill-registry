---
name: "node-zombie-guardian"
description: "Use when diagnosing stale or orphaned Node.js processes launched by VCO, auditing ownership/liveness, or safely simulating cleanup without touching external Node workloads."
---

# Node Zombie Guardian

This skill is for managed-process hygiene inside the VCO ecosystem.

It exists to answer one question safely: which Node processes belong to VCO, which of them are stale, and which of those are eligible for cleanup without risking live external workloads.

## Safety Boundary

- Only processes with `ownership = vco-managed` can ever become cleanup candidates.
- `external` and `unknown` processes remain audit-only.
- Cleanup is report-first by default.
- Fixture `-Apply` mode remains simulation-only and must never terminate real processes.

## When To Use

- Node processes accumulate after long VCO runs and you need an ownership-aware audit.
- You want to register or observe VCO-launched Node processes through the wrapper.
- You need a Markdown or JSON report of managed vs external Node processes.
- You want to simulate cleanup of stale VCO-managed Node processes without touching real workloads.

## Operator Surfaces

This skill is a focused wrapper around the operator scripts that live in the bundled `vibe` skill:

- `../vibe/scripts/common/NodeLaunchWrapper.ps1`
- `../vibe/scripts/governance/Invoke-NodeProcessAudit.ps1`
- `../vibe/scripts/governance/Invoke-NodeZombieCleanup.ps1`
- `../vibe/scripts/verify/vibe-node-zombie-gate.ps1`

## Quick Start

### 1. Launch a managed Node process through the wrapper

Use the wrapper when VCO starts a Node workload that should be tracked in the ledger.

```powershell
& "..\vibe\scripts\common\NodeLaunchWrapper.ps1" `
  -RepoRoot "C:\path\to\repo" `
  -Command "node" `
  -ArgumentList @("scripts\worker.js")
```

### 2. Audit live Node ownership and liveness

Default mode is read-only and emits a report.

```powershell
& "..\vibe\scripts\governance\Invoke-NodeProcessAudit.ps1" `
  -RepoRoot "C:\path\to\repo" `
  -WriteArtifacts
```

Expected outcomes:

- classify processes such as `managed_live`, `managed_stale`, `external_audit_only`
- emit JSON and Markdown artifacts for review
- keep non-managed processes out of the cleanup candidate set

### 3. Simulate cleanup

Cleanup remains report-only unless explicitly switched, and the safety filters still apply.

```powershell
& "..\vibe\scripts\governance\Invoke-NodeZombieCleanup.ps1" `
  -RepoRoot "C:\path\to\repo" `
  -WriteArtifacts
```

Use this to confirm which managed stale processes would be targeted before any real cleanup path is considered.

## Verification

Run the dedicated gate before trusting changes in this area:

```powershell
& "..\vibe\scripts\verify\vibe-node-zombie-gate.ps1" -WriteArtifacts
```

The gate proves:

- classification is deterministic on fixtures
- only managed rows become cleanup candidates
- external rows never become cleanup candidates
- report-only mode never terminates processes
- fixture `-Apply` mode stays simulated
