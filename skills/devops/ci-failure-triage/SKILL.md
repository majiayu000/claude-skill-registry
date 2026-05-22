---
name: ci-failure-triage
description: Diagnose CI failures and stabilize pipelines. Use when a mid-level developer needs to resolve flaky or failing builds.
---

# CI Failure Triage

## Purpose
Diagnose CI failures and stabilize pipelines.

## Inputs to request
- CI logs and failing jobs.
- Recent merges and environment changes.
- Flake frequency and patterns.

## Workflow
1. Classify failures by stage and error type.
2. Check for environment changes and test flakiness.
3. Propose fixes and temporary mitigations.

## Output
- Triage summary with root cause candidates.

## Quality bar
- Separate flake from deterministic failure.
- Prefer fixes that reduce future noise.
