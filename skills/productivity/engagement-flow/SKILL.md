---
name: engagement-flow
description: Use when starting, planning, or running a multi-phase pentest or red-team engagement — to sequence the Cyber Kill Chain phases with quality gates instead of jumping straight to exploitation
---

# Engagement Flow

## Overview

A pentest/red-team engagement is a **phased pipeline with gates**, not a pile of techniques run
ad hoc. This skill sequences the 9-phase Lockheed Martin Cyber Kill Chain and routes each phase to
its commands, domain skills, and discipline checks. It is the offensive analog of
brainstorming → writing-plans → executing-plans: scope the work, plan it, then execute phase by phase.

Don't jump to exploitation. Earlier phases earn the access that later phases need, and each gate
keeps quality high before you advance.

## The pipeline

```dot
digraph killchain {
    rankdir=LR;
    scope -> recon -> weaponize -> deliver -> exploit -> install -> c2 -> actions -> report;
    scope [label="0 SCOPE"]; recon [label="1 RECON"]; weaponize [label="2 WEAPONIZE"];
    deliver [label="3 DELIVER"]; exploit [label="4 EXPLOIT"]; install [label="5 INSTALL"];
    c2 [label="6 C2"]; actions [label="7 ACTIONS"]; report [label="8 REPORT"];
}
```

Each transition requires a **gate** (`/engage.gate`): required artifacts present, findings carry
CWE+CVSS+ATT&CK+evidence, and the automated checks pass. Gate FAIL → fix the gap before advancing.

## How to run it

1. Pick the workflow preset for the engagement type (web-app, network, red-team, cloud, mobile,
   ad-domain, bug-bounty) and drive phases with the `/engage.*` commands.
2. **Phase 0 (scope):** emit `.engage/scope/scope.json`. **REQUIRED:** scope-discipline.
3. **Phases 1-7:** before any target interaction → scope-discipline; before any outward action →
   opsec-discipline; invoke the matching domain skill for the technique.
4. **Recall prior intel:** at recon/weaponize, `/engage.memory recall` to start from what worked.
5. **Findings:** **REQUIRED:** finding-discipline — nothing is `[CONFIRMED]` without proof.
6. **Phase 8 (report):** record confirmed findings to engagement-memory; generate the report.
7. **Optional autopilot:** `engine/engine.py` runs the phases under a budget/loop/trace with `--resume`
   (`/engage.pickup`); offensive actions stay operator-gated.

## Red Flags — STOP, back up a phase

- "Let me just start exploiting" (no scope.json / no recon → back to phase 0/1)
- "Skip the gate, I'll document later" (gates exist so the report is complete and findings are real)
- "Recon is done, I didn't check prior intel" (run `/engage.memory recall`)

## Quick reference

| Phase | Command | Discipline / tooling |
|-------|---------|----------------------|
| Scope | `/engage.scope` | scope-discipline → `scope.json` |
| Recon | `/engage.recon` | scope-discipline; `/engage.memory recall` |
| Exploit | `/engage.exploit` | opsec-discipline; finding-discipline |
| Actions | `/engage.actions` | action_guard gate; opsec-discipline |
| Report | `/engage.report` | finding-discipline; record to memory |
| Gate / resume | `/engage.gate`, `/engage.pickup` | automated checks; engine trace |
