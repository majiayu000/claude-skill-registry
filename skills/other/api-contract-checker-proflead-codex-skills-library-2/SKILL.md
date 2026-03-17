---
name: api-contract-checker
description: Validate API changes against an expected contract. Use when a mid-level developer needs to detect breaking changes.
---

# API Contract Checker

## Purpose
Validate API changes against an expected contract.

## Inputs to request
- Old and new API specs or examples.
- Versioning policy and client expectations.
- Known consumers and usage patterns.

## Workflow
1. Compare endpoints, request/response fields, and status codes.
2. Identify breaking changes and backward-compatible adjustments.
3. Suggest versioning or migration notes.

## Output
- Breaking change report with mitigation steps.

## Quality bar
- Flag any removal or behavior change clearly.
- Recommend safe rollouts for clients.
