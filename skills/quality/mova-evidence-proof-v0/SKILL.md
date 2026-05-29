---
name: mova-evidence-proof-v0
description: Use for deterministic changes, evidence-first delivery, or assembling proof kits with clear safety justification.
allowed-tools: Bash, Read, Grep, Glob
---

## Determinism rules
- Business results belong in result payloads; run-specific data goes to env/meta and artifacts.
- Do not fabricate outputs; rerun commands if needed.

## Negative suite
- Required for risky paths: unauthorized, deny, bad signature, oversize, and validation errors.
- Add minimal, explicit cases and surface them in evidence.

## Evidence-first standard
- Prefer artifacts and reports over narrative claims.
- Always link to evidence paths in `artifacts/**`.

## Evidence sources
- Artifacts paths, `gw_request_id`, and episode ids/refs.
- History lookup must use `mova_search_episodes_v0` (read-only).
