---
name: agreement
description: "Maintain sourced agreement context and scope in PROJECT.md, cite registered contracts/proposals, and record amendments without imposing a commercial workflow."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:agreement

Before acting, read the [host contract](../../docs/host-harness-contract.md), this component's [declaration](host-contract.json) (`skill:agreement`), and applicable [workspace semantics](../../docs/workspace-model.md). Load only the required modes from the [shared catalog](../../corpus/host-contracts.json).

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md) and available native tools or ordinary task-specific code. Operation names identify the semantic work in the [workspace model](../../docs/workspace-model.md), not installed functions or a script API. Resolve canonical context before durable work. No Arch Studio runner, package installation or executable reconstruction is required. Existing exact authorization persists; ask only for material missing information or missing permission.

Own only the bounded Agreement section in PROJECT.md plus authored agreement/contract documents. Project owns other facts; studio owns registration/status. Register supplied signed agreements, SOWs and amendments through receive; never overwrite a prior agreement document.

## Before changing records

Before persistent changes, follow the [native mutation sequence](../../docs/workspace-model.md#native-mutation-sequence): **Inspect → Prepare → Verify preparation → Apply → Verify result → Complete**. Inspect pending work first. Finish and verify preparation before the first canonical write: separately reread every saved original and prepared file, check its complete actual bytes, establish durable saving, and inspect actual permissions, ownership and ACLs. Merely writing recovery files does not finish verification. Apply only that verified set. Mark complete only after fresh readback validates the entire affected result and its relationships. Read-only requests and inline drafts need no publication sequence.

Agreement context edits affect only the bounded PROJECT.md section; retain the complete original/prepared PROJECT.md and guard the cited registered document bytes, raw hash and applicable terms seal. Registering an authored agreement or amendment affects that document plus DOCUMENTS.csv before any optional, separately authorized context update. A cited source is not permission to edit it.

`agreement.init` creates the bounded context from a registered agreement/contract ID. `agreement.promote` is optional for an accepted sealed proposal and cites its ID, content hash and issued-terms hash without duplicating the proposal. Direct engagements do not require a proposal. Facts have field/value/source/date; preserve unknowns, and interpret clauses through the harness and applicable originals rather than deterministic scope classification.

The section contains parties/term/fees/caps and exactly the scope headings In scope, Not in scope and Requires SOW when supplied. `check` reads those source-linked bullets and presents advisory in-scope/needs-SOW/out-of-scope findings; the user decides. No status or automatic invoice gate is introduced.

`agreement.record-amendment` cites a registered agreement/contract ID, explicit date and summary. Preview any associated fact/scope changes separately when not already authorized; retain prior evidence. `agreement.verify` checks cited documents. A malformed section, missing document or checksum conflict blocks dependent mutation and remains preserved. Reopen PROJECT.md and cited originals after the action. Legal interpretation or execution status is not established by a successful registration.
