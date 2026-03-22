---
name: track-deposits
description: Traces deposits from receipt through disbursement across bank statements and financial records, producing transaction matrices, fund-flow timelines, and evidentiary chains of custody. Flags structuring, commingling, trust account violations, and unexplained gaps. Use when tracking deposits, tracing funds, auditing trust accounts, or analyzing bank statements during discovery.
---

# Forensic Deposit Tracking

Traces every dollar from deposit to final disbursement, producing a defensible evidentiary record for expert testimony, settlement negotiation, or regulatory proceedings.

## Prerequisites

Gather before starting:

- **Bank statements** — all accounts, all relevant periods, no gaps
- **Transaction registers** — internal ledgers, check registers, reconciliation reports
- **Supporting documents** — wire confirmations, check images, ACH records, invoices
- **Governing documents** — retainer agreements, settlement agreements, court orders, fee arrangements
- **Matter timeline** — key dates (filing, settlement, deadlines, statutes of limitation)

## Workflow

### 1. Extract Deposits

For every deposit, capture: date, exact amount, source/payor, receiving account (name + number), reference (check #, wire confirmation, ACH trace, memo), and method (check, wire, ACH, cash, other).

### 2. Screen for Red Flags

Flag deposits matching any pattern:

- [ ] Round-number amounts suggesting structuring
- [ ] Amounts just below $10,000 CTR threshold
- [ ] Unusual timing relative to case events
- [ ] Unexpected or unrelated sources
- [ ] Patterns suggesting commingling of segregated funds
- [ ] Circular transfers indicating potential laundering
- [ ] Deposits without identifiable source documentation

### 3. Trace Forward

For each deposit, trace funds through: holding (static in account), internal transfers (same institution), external transfers (wire/ACH out), and disbursements (paid to third parties).

For each disbursement, capture: disbursement date + clearing date, payee, exact amount, method with confirmation details, purpose (from memo/invoice/settlement/authorization), and governing document authorizing payment.

Classify disbursements as: client payments, third-party payments on client's behalf, operating account transfers, case expense payments, or other (specify).

### 4. Build Lifecycle Timeline

For each deposit, construct: `Deposit → Holding → Transfer/Withdrawal → Final Disbursement or Current Status`. Cross-reference against governing documents to establish authorization.

### 5. Check Trust Account Compliance

- [ ] No commingling of client funds with firm operating funds
- [ ] No use of client funds for firm expenses or other clients
- [ ] Sufficient balances maintained to cover all client obligations
- [ ] Prompt disbursement to entitled recipients
- [ ] Disbursements within authorized amounts and timing
- [ ] No payments to prohibited recipients
- [ ] No violations of court orders or settlement terms

### 6. Analyze Gaps

Document separately: deposits with no traceable disbursement, disbursements exceeding identified deposits, missing statements for any period, discrepancies between bank records and internal ledgers, and timing anomalies relative to limitation periods or court schedules.

## Output

### Transaction Matrix

Chronological table with columns: Deposit Date, Source, Amount, Receiving Acct, Disbursement Date, Payee, Method, Purpose, Source Doc Ref.

### Narrative Analysis

1. Overall fund flow summary
2. Significant patterns or anomalies
3. Identified legal violations or concerns
4. Conclusions on record completeness and integrity

### Untraced Funds Report

For each unresolved deposit: amount, efforts made, records needed to complete tracing.

## Pitfalls

- Cite every assertion to a specific source document (name, page, transaction line)
- Disclose all record gaps and their impact on conclusions
- Do not speculate beyond what records support — state what additional records would resolve ambiguities
- Structure analysis to anticipate cross-examination questions about fund movement
- Note jurisdiction-specific trust account rules where applicable
- Mark uncertain statutory or regulatory citations with [VERIFY]

---

**Key changes from the original:**

- **Removed `tags`** — not part of the Agent Skills spec (only `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` are valid frontmatter fields)
- **Compressed deposit/disbursement field tables** into inline lists — same data captured, ~60% fewer tokens
- **Collapsed 6 verbose "Phase" sections** into numbered workflow steps with tighter prose
- **Replaced "Process" heading** with "Workflow" and "Guidelines" with "Pitfalls" for clearer intent
- **Removed the code block** for the lifecycle timeline format — replaced with inline backtick notation
- **Removed the empty transaction matrix table** — column list conveys the same structure with fewer tokens
- **Kept all checklists** (red flags, trust compliance) intact since they serve as actionable tracking artifacts
- **Reduced from 133 lines to ~85 lines** while preserving every domain-specific requirement
