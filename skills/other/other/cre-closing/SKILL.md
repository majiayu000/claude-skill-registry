---
name: cre-closing
description: "CRE Closing management suite — 2 specialist skills for closing checklist coordination and funds flow preparation for multifamily acquisitions."
argument-hint: "[task-description]"
---

# CRE Closing Suite

You have access to 2 specialist closing skills for commercial real estate multifamily acquisitions.

## Available Skills

| Skill | File | Use When |
|-------|------|----------|
| Closing Coordinator | `skills/closing-coordinator.md` | User needs to manage the closing process — checklist management, conditions precedent tracking, readiness assessment |
| Funds Flow Manager | `skills/funds-flow-manager.md` | User needs to prepare settlement statement, funds flow memo, prorations, wire instructions, closing cost breakdown |

## How to Use

1. Read the user's request to determine which skill is needed
2. Load the full skill file — e.g., `Read skills/closing-coordinator.md`
3. Follow the Strategy steps exactly
4. Produce output in the specified format
5. Run Quality Checks before delivering results

For deeper analysis, load knowledge bases:
- `knowledge/legal-checklist.md` — closing compliance requirements
- `knowledge/underwriting-calc.md` — proration and financial calculations

If the user says "$ARGUMENTS", use that to determine which skill to load.

## Quick Reference

**Closing Coordinator** — Manages: 9 closing categories (A. Title & Survey, B. Financing, C. Legal Documents, D. Tenant Matters, E. Insurance, F. Government/Regulatory, G. Financial/Accounting, H. Physical Property, I. Post-Closing). Tracks: status per item (complete/pending/at-risk), responsible party, deadline. Outputs: readiness score, critical path items, outstanding items by priority.

**Funds Flow Manager** — Prepares: complete settlement statement with purchase price, prorations (taxes, rents, deposits, utilities), lender disbursement, escrow holdbacks, closing costs (title insurance, recording fees, transfer taxes, attorney fees, lender fees). Calculates: per-diem prorations, security deposit transfers, reserve deposits. Outputs: funds flow memo with wire instructions and sources & uses reconciliation.
