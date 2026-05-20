---
name: atlan-sdk-objectstore-io-defaults
description: Enforce object store and IO defaults from the Atlan SDK for output paths, prefixes, and file writes. Use when implementing or reviewing raw/transformed output handling.
---

# Atlan SDK Objectstore IO Defaults

Apply SDK-native defaults for all output read/write logic.

## Workflow
1. Apply defaults from `references/defaults.md`.
2. Use SDK path-building conventions instead of hardcoded prefixes.
3. Route writes through SDK IO abstractions where possible.
4. If local SDK checkout is unavailable, verify behavior from installed package source or remote SDK source/docs.
5. Run `atlan-fact-verification-gate` when output behavior changed or conflicts with existing tests.
6. Validate expected output sections in `e2e_case_contract.yaml`.

## Non-Negotiable Rules
- Do not hardcode bucket prefixes when SDK-derived paths exist.
- Keep raw and transformed outputs under workflow-specific output path.
- Align output naming with e2e assertions.

## References
- Defaults and anti-patterns: `references/defaults.md`
- Shared templates: `../_shared/references/artifact-templates.md`
