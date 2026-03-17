---
name: atlan-workflow-args-secrets-state
description: Implement workflow argument retrieval, credential_guid usage, and state store updates using Atlan SDK patterns. Use when workflows or activities handle credentials, runtime args, or persisted workflow state.
---

# Atlan Workflow Args Secrets State

Keep workflow and activity data flow aligned with SDK patterns.

## Workflow
1. Read `references/state-flow.md`.
2. Ensure workflow args are loaded through SDK-supported state path.
3. Replace direct credential payload handling with `credential_guid` + secret retrieval.
4. Keep `get_workflow_args` focused on args retrieval/normalization.
5. Keep business transformation and artifact writes in dedicated activity methods orchestrated by workflow.
6. Persist workflow state through SDK-compatible state store APIs.
7. Run `atlan-fact-verification-gate` for any workflow lifecycle change that can affect runtime behavior.
8. Reflect this behavior in e2e contracts and loop reports.

## Rules
- Never persist raw secrets in workflow args snapshots.
- Never bypass state store for cross-activity workflow state.
- Keep retries/timeouts aligned with workflow conventions.
- Do not collapse the full business pipeline into `get_workflow_args` side effects.

## References
- State flow map: `references/state-flow.md`
- Shared artifacts: `../_shared/references/artifact-templates.md`
