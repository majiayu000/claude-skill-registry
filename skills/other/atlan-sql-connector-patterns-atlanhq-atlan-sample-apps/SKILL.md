---
name: atlan-sql-connector-patterns
description: Select and apply the correct SQL connector implementation pattern (SDK-default minimal or source-specific custom). Use when building or extending SQL metadata/query extraction connectors.
---

# Atlan SQL Connector Patterns

Choose the right connector strategy and implement it consistently.

## Workflow
1. Use `references/decision-tree.md` to choose `postgres-minimal` or `redshift-custom`.
2. Implement required components for selected path.
3. Verify auth, preflight, workflow map, and transformation behavior against references.
4. Run `atlan-fact-verification-gate` if requirements imply source-specific behavior or SDK override risk.
5. Hand off to `atlan-e2e-contract-validator` for contract generation.

## Rules
- Default to minimal path unless requirements justify custom path.
- For custom path, explicitly document why SDK defaults are insufficient.
- Reuse source-specific patterns only when corresponding requirements are present.

## References
- Decision tree: `references/decision-tree.md`
- Shared verification map: `../_shared/references/verification-sources.md`
