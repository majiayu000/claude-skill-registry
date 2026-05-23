---
name: commerce-quality
description: Manage quality inspections, non-conformance reports, and quality holds. Use when inspecting received goods, production output, or customer returns for defects.
---

# Commerce Quality

Run quality inspections, track non-conformances, and place quality holds on inventory.

## How It Works

1. Create an inspection for incoming goods, production output, or returns.
2. Inspect items and record pass/fail results with defect codes.
3. Create non-conformance reports (NCRs) for failures.
4. Place quality holds to prevent movement of suspect inventory.
5. Resolve NCRs with root cause analysis and corrective actions.
6. Release holds when items pass re-inspection.

## Usage

- MCP tools: `create_inspection`, `list_inspections`, `record_inspection_result`, `create_ncr`, `update_ncr`, `create_quality_hold`, `release_quality_hold`.
- Writes require `--apply`.

## Inspection Types

- Incoming, Receiving, InProcess, Final, Random, Return

## Inspection Results

- Pending, Pass, Fail, ConditionalPass

## NCR Statuses

- Open -> UnderReview -> PendingDisposition -> CorrectiveAction -> PreventiveAction -> Verification -> Closed (or Cancelled)

## Severity Levels

- Critical, Major, Minor, Observation

## Disposition Options

- UseAsIs, Rework, Repair, Scrap, ReturnToVendor, Downgrade, SortAndScreen

## Hold Types

- QualityInspection, CustomerReturn, Recall, Damaged, Expired, Quarantine, RegulatoryHold, InvestigationHold

## Output

```json
{"status":"inspection_completed","inspection_id":"INS-001","result":"conditional_pass","pass_rate":0.96,"ncr_created":"NCR-2025-0012"}
```

## Present Results to User

- Inspection result and pass rate.
- Defect codes and quantities affected.
- NCR number and required disposition.
- Active quality holds and affected SKUs.

## Troubleshooting

- Cannot complete inspection: ensure all items have been inspected.
- Hold blocking shipment: release the hold or re-route to quarantine location.
- NCR stuck open: check that corrective action and verification steps are completed.

## References
- references/quality-inspections.md
- /home/dom/stateset-icommerce/crates/stateset-core/src/models/quality.rs
- /home/dom/stateset-icommerce/crates/stateset-embedded/src/quality.rs
