---
name: invoice
description: "Maintain an append-only project INVOICES.csv ledger from explicit billing facts and recorded lifecycle evidence; never infer charges or payment from activity or time logs."
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# /as:invoice

Before acting, read the [host contract](../../docs/host-harness-contract.md), this component's [declaration](host-contract.json) (`skill:invoice`), and applicable [workspace semantics](../../docs/workspace-model.md). Load only the required modes from the [shared catalog](../../corpus/host-contracts.json).

<!-- architecture-studio:harness-compatibility -->
Use the [host adapter](../../docs/host-adapters.md) and [native context procedure](../project/references/context-resolution.md). The harness performs the semantic operations below using its available native tools; ordinary task-specific code is allowed. No Arch Studio runtime, installer, bridge, supplied script or source checkout is required. Direct skill invocation is valid. Existing exact authorization persists; ask only for material missing facts or unavailable access.

Own INVOICES.csv; invoice documents are registered through receive with kind `invoice`. No agreement is required: amounts and currency may come from confirmed terms in PROJECT.md's Agreement section or explicit user input. Never infer billability, payment, hours or completion from task/time/activity signals.

## Before changing records

Before persistent changes, follow the [native mutation sequence](../../docs/workspace-model.md#native-mutation-sequence): **Inspect → Prepare → Verify preparation → Apply → Verify result → Complete**. Inspect pending work first. Finish and verify preparation before the first canonical write: separately reread every saved original and prepared file, check its complete actual bytes, establish durable saving, and inspect actual permissions, ownership and ACLs. Merely writing recovery files does not finish verification. Apply only that verified set. Mark complete only after fresh readback validates the entire affected result and its relationships. Read-only requests and inline drafts need no publication sequence.

Ledger append/lifecycle changes affect the complete INVOICES.csv only; guard any cited invoice document or Agreement evidence without editing it. Invoice-document creation/registration is a separate authorized document-plus-DOCUMENTS.csv operation. A next-ID preview is read-only and does not reserve identity.

Use `invoice.status` to list preserved rows and separate totals by currency. `invoice.allocate` reports the next permanent I-number without reserving it; append allocates against the actual current register. `invoice.init` reports the fresh setup register without replacing it.

For `invoice.append`, preview invoice number, billing period, currency, base, expenses, total, explicit sent/paid dates/status, correction target and optional registered invoice document ID. Decimal arithmetic must reconcile base + expenses = total. Preserve malformed registers; do not guess missing amounts or silently reuse an invoice number. Corrections append distinct rows referencing the original; do not erase its history or silently net correction totals.

`invoice.set-lifecycle` records sent/paid/void date evidence without deleting a row. Actual sending or bank reconciliation requires its own available capability and authorization. A lifecycle update never manufactures payment. Re-read the row and report its ID, facts and any unmet external action.

## Native execution and completion

Follow the exact [INVOICES semantics](../../docs/workspace-model.md#native-invoice-operations) for
whole-register validation, decimal values, permanent IDs, number uniqueness, correction references,
registered documents, lifecycle history and retry identity. These are native semantic operations,
not a script interface. `invoice.init`, `invoice.allocate` and `invoice.status` are read-only;
init never creates or replaces a missing register. A displayed next ID is not reserved.

Confirm missing commercial facts before append; preserve existing authorization for exact rows.
Use decimal arithmetic for all checks and totals, without binary floating-point rounding. Status
totals include all nonvoid rows per currency; they are not a calculation of outstanding balance.
Corrections retain their own signed, explicit amounts and distinct invoice number; no netting or
payment inference is authorized by the presence of an earlier row.

Before any append or lifecycle change, bind exact intent and actual current register; reconcile
concurrent changes or refuse before publication. Use the verified single-register preparation
from the mutation sequence. After interruption, inspect actual old/new state and history before
retry; do not duplicate an invoice or lifecycle event.

Re-read the canonical destination and report register path, invoice ID/number, exact amounts and
currency, explicit status/dates, appended event count and any unmet external action. Recording
sent or paid evidence does not send a message, invoice the customer or perform bank reconciliation.
