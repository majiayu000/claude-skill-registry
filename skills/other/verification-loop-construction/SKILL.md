---
name: "verification-loop-construction"
description: "Comprehensive verification system for construction automation deliverables. Use after completing estimates, schedules, reports, or data processing tasks to ensure quality."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🛡️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Verification Loop for Construction Automation

A systematic verification framework ensuring quality of construction automation outputs before delivery or deployment.

## When to Use

Invoke this skill:
- After generating cost estimates
- After creating or updating schedules
- After processing BIM/CAD data
- After generating reports (daily, weekly, monthly)
- After running data pipelines
- Before submitting documents to clients
- Before deploying automation workflows

## Verification Phases

### Phase 1: Data Integrity Check

```python
def verify_data_integrity(output: dict) -> VerificationResult:
    """Check data completeness and consistency"""

    checks = []

    # Completeness check
    required_fields = get_required_fields(output['type'])
    missing = [f for f in required_fields if f not in output]
    checks.append({
        'name': 'Completeness',
        'status': 'PASS' if not missing else 'FAIL',
        'details': f'Missing fields: {missing}' if missing else 'All required fields present'
    })

    # Consistency check
    inconsistencies = find_inconsistencies(output)
    checks.append({
        'name': 'Consistency',
        'status': 'PASS' if not inconsistencies else 'WARN',
        'details': inconsistencies or 'No inconsistencies found'
    })

    # Referential integrity
    broken_refs = check_references(output)
    checks.append({
        'name': 'Referential Integrity',
        'status': 'PASS' if not broken_refs else 'FAIL',
        'details': f'Broken references: {broken_refs}' if broken_refs else 'All references valid'
    })

    return VerificationResult(checks)
```

#### Data Integrity Checklist
- [ ] All required fields populated
- [ ] No duplicate records
- [ ] Foreign keys resolve correctly
- [ ] Date formats consistent
- [ ] Currency values formatted correctly
- [ ] Units of measure standardized

### Phase 2: Business Logic Verification

```python
def verify_business_logic(output: dict) -> VerificationResult:
    """Verify construction-specific business rules"""

    checks = []

    # Cost estimate checks
    if output['type'] == 'cost_estimate':
        # Verify totals match line items
        calculated_total = sum(item['amount'] for item in output['line_items'])
        declared_total = output['total']
        variance = abs(calculated_total - declared_total)

        checks.append({
            'name': 'Total Accuracy',
            'status': 'PASS' if variance < 0.01 else 'FAIL',
            'details': f'Calculated: {calculated_total}, Declared: {declared_total}'
        })

        # Verify markup applied correctly
        for item in output['line_items']:
            expected_markup = item['base_cost'] * (1 + item['markup_rate'])
            if abs(item['amount'] - expected_markup) > 0.01:
                checks.append({
                    'name': f'Markup Check - {item["id"]}',
                    'status': 'FAIL',
                    'details': f'Expected: {expected_markup}, Got: {item["amount"]}'
                })

    # Schedule checks
    if output['type'] == 'schedule':
        # Verify dependencies
        for task in output['tasks']:
            for pred_id in task.get('predecessors', []):
                pred = find_task(output['tasks'], pred_id)
                if pred and pred['end_date'] > task['start_date']:
                    checks.append({
                        'name': f'Dependency Violation - {task["id"]}',
                        'status': 'FAIL',
                        'details': f'Task starts before predecessor {pred_id} ends'
                    })

        # Verify resource allocation
        resource_conflicts = find_resource_conflicts(output['tasks'])
        checks.append({
            'name': 'Resource Conflicts',
            'status': 'PASS' if not resource_conflicts else 'WARN',
            'details': resource_conflicts or 'No resource conflicts'
        })

    return VerificationResult(checks)
```

#### Business Logic Checklist

**For Cost Estimates:**
- [ ] Line item totals = declared subtotals
- [ ] Subtotals + markups = grand total
- [ ] Tax calculations correct
- [ ] Contingency applied consistently
- [ ] Unit prices within expected ranges
- [ ] Quantities match QTO

**For Schedules:**
- [ ] Dependencies respected (no backwards links)
- [ ] Critical path calculated correctly
- [ ] No resource over-allocation
- [ ] Milestones properly dated
- [ ] Working days/calendar correct
- [ ] Float values logical

**For BIM Data:**
- [ ] Element counts match expected
- [ ] Property values within ranges
- [ ] Spatial relationships valid
- [ ] Level associations correct
- [ ] Classification codes valid

### Phase 3: Format & Standards Compliance

```python
def verify_standards_compliance(output: dict) -> VerificationResult:
    """Verify compliance with construction standards"""

    checks = []

    # CSI classification check
    if 'csi_codes' in output:
        invalid_codes = []
        for code in output['csi_codes']:
            if not validate_csi_code(code):
                invalid_codes.append(code)

        checks.append({
            'name': 'CSI Code Validation',
            'status': 'PASS' if not invalid_codes else 'WARN',
            'details': f'Invalid codes: {invalid_codes}' if invalid_codes else 'All codes valid'
        })

    # CWICR mapping check
    if output.get('cwicr_mapped'):
        unmapped = [item for item in output['items'] if not item.get('cwicr_id')]
        checks.append({
            'name': 'CWICR Mapping',
            'status': 'PASS' if not unmapped else 'WARN',
            'details': f'{len(unmapped)} items unmapped' if unmapped else 'All items mapped'
        })

    # Document format check
    if output['type'] == 'report':
        format_issues = validate_report_format(output)
        checks.append({
            'name': 'Report Format',
            'status': 'PASS' if not format_issues else 'WARN',
            'details': format_issues or 'Format compliant'
        })

    return VerificationResult(checks)
```

#### Standards Compliance Checklist
- [ ] CSI MasterFormat codes valid (6-digit)
- [ ] UniFormat codes valid (if used)
- [ ] CWICR mappings present
- [ ] ISO dates (YYYY-MM-DD)
- [ ] Currency format consistent
- [ ] Measurement units consistent (metric/imperial)

### Phase 4: Output Quality Check

```python
def verify_output_quality(output: dict) -> VerificationResult:
    """Check output quality and presentation"""

    checks = []

    # Formatting check
    if output['format'] == 'excel':
        checks.extend([
            {
                'name': 'Column Headers',
                'status': check_headers_present(output),
                'details': 'Headers in first row'
            },
            {
                'name': 'Number Formatting',
                'status': check_number_format(output),
                'details': 'Currencies and percentages formatted'
            },
            {
                'name': 'Print Area',
                'status': check_print_area(output),
                'details': 'Print area set for clean output'
            }
        ])

    if output['format'] == 'pdf':
        checks.extend([
            {
                'name': 'Page Layout',
                'status': check_page_layout(output),
                'details': 'Margins and orientation correct'
            },
            {
                'name': 'Images Rendered',
                'status': check_images(output),
                'details': 'All images/charts visible'
            },
            {
                'name': 'Fonts Embedded',
                'status': check_fonts(output),
                'details': 'Fonts embedded for portability'
            }
        ])

    # Data visualization check
    if 'charts' in output:
        for chart in output['charts']:
            checks.append({
                'name': f'Chart - {chart["title"]}',
                'status': validate_chart(chart),
                'details': 'Labels, legends, and data visible'
            })

    return VerificationResult(checks)
```

#### Output Quality Checklist
- [ ] Headers/footers present
- [ ] Page numbers correct
- [ ] Company branding applied
- [ ] Charts readable
- [ ] Tables properly aligned
- [ ] Links/references working

### Phase 5: Cross-Reference Validation

```python
def verify_cross_references(output: dict, sources: list) -> VerificationResult:
    """Validate output against source data"""

    checks = []

    for source in sources:
        # Compare key metrics
        metrics = extract_comparable_metrics(output, source)

        for metric_name, (output_val, source_val) in metrics.items():
            variance_pct = abs(output_val - source_val) / source_val * 100 if source_val else 0

            status = 'PASS'
            if variance_pct > 5:
                status = 'WARN'
            if variance_pct > 10:
                status = 'FAIL'

            checks.append({
                'name': f'{metric_name} vs {source["name"]}',
                'status': status,
                'details': f'Output: {output_val}, Source: {source_val}, Variance: {variance_pct:.1f}%'
            })

    return VerificationResult(checks)
```

#### Cross-Reference Checklist
- [ ] QTO matches BIM model
- [ ] Estimate matches specifications
- [ ] Schedule aligns with estimate
- [ ] Budget matches contract
- [ ] Progress matches field data
- [ ] Actuals match projections (within tolerance)

## Verification Report Format

After running all phases, produce a verification report:

```
═══════════════════════════════════════════════════════════════
                    VERIFICATION REPORT
═══════════════════════════════════════════════════════════════

Output Type:    Cost Estimate
Project:        Downtown Office Tower
Generated:      2026-01-24 14:30:00
Verified By:    DDC Verification Loop v1.0

───────────────────────────────────────────────────────────────
PHASE 1: DATA INTEGRITY
───────────────────────────────────────────────────────────────
✓ Completeness      PASS    All required fields present
✓ Consistency       PASS    No inconsistencies found
✓ Referential       PASS    All references valid

───────────────────────────────────────────────────────────────
PHASE 2: BUSINESS LOGIC
───────────────────────────────────────────────────────────────
✓ Total Accuracy    PASS    Calculated: $1,523,456.78, Declared: $1,523,456.78
✓ Markup Check      PASS    All markups applied correctly
⚠ Range Check       WARN    3 items outside typical ranges

───────────────────────────────────────────────────────────────
PHASE 3: STANDARDS COMPLIANCE
───────────────────────────────────────────────────────────────
✓ CSI Codes         PASS    All codes valid
✓ CWICR Mapping     PASS    156/156 items mapped
✓ Unit Standards    PASS    All units metric

───────────────────────────────────────────────────────────────
PHASE 4: OUTPUT QUALITY
───────────────────────────────────────────────────────────────
✓ Excel Format      PASS    Headers, formatting correct
✓ Charts            PASS    All visualizations rendered
✓ Print Ready       PASS    Print area configured

───────────────────────────────────────────────────────────────
PHASE 5: CROSS-REFERENCE
───────────────────────────────────────────────────────────────
✓ vs BIM QTO        PASS    Variance: 0.2%
✓ vs Historical     PASS    Within expected range
⚠ vs Budget         WARN    5.3% over budget baseline

═══════════════════════════════════════════════════════════════
                         SUMMARY
═══════════════════════════════════════════════════════════════

Total Checks:       18
Passed:             16
Warnings:           2
Failed:             0

OVERALL STATUS:     ✓ READY FOR DELIVERY

Recommendations:
1. Review items outside typical ranges (see Appendix A)
2. Discuss budget variance with PM before submission

═══════════════════════════════════════════════════════════════
```

## Automated Verification Pipeline

```python
class ConstructionVerificationPipeline:
    """Automated verification for construction outputs"""

    def __init__(self, output_type: str):
        self.output_type = output_type
        self.phases = self._get_phases_for_type(output_type)

    def verify(self, output: dict, sources: list = None) -> VerificationReport:
        results = []

        for phase in self.phases:
            phase_result = phase.execute(output, sources)
            results.append(phase_result)

            # Stop on critical failure
            if phase_result.has_critical_failure():
                break

        return VerificationReport(
            output_type=self.output_type,
            phases=results,
            overall_status=self._calculate_overall_status(results)
        )

    def _calculate_overall_status(self, results: list) -> str:
        if any(r.has_failures() for r in results):
            return 'NOT READY - FIX REQUIRED'
        if any(r.has_warnings() for r in results):
            return 'READY WITH WARNINGS'
        return 'READY FOR DELIVERY'


# Usage
pipeline = ConstructionVerificationPipeline('cost_estimate')
report = pipeline.verify(estimate_output, sources=[bim_model, specifications])
print(report.to_markdown())
```

## Integration with DDC Workflows

This verification skill integrates with other DDC skills:

1. **Post-Estimation**: Run after `cost-estimation-*` skills
2. **Post-QTO**: Run after `qto-report` skill
3. **Post-Scheduling**: Run after `gantt-chart` or `4d-simulation` skills
4. **Post-Pipeline**: Run after `etl-pipeline` skill

## Continuous Verification Mode

For long automation sessions, run verification at checkpoints:

```markdown
Recommended checkpoints:
- After processing each BIM model
- After generating each major section of estimate
- After completing each phase of schedule
- Before any external data submission

Command: /verify-construction
```

---

**Quality is not negotiable in construction. Verify before you deliver.**
