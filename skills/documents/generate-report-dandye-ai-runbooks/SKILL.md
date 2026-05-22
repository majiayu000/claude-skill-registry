---
name: generate-report
description: "Save investigation findings to a markdown report file. Use after completing triage, enrichment, or investigation to create a permanent record. Generates timestamped files in ./reports/ directory."
personas: [all]
---

# Generate Report Skill

Save generated report content to a markdown file with standardized naming convention.

## Inputs

- `REPORT_CONTENT` - The full markdown content of the report
- `REPORT_TYPE` - Short identifier for the report type:
  - `alert_triage` - Alert triage reports
  - `ioc_enrichment` - IOC enrichment reports
  - `case_investigation` - Case investigation reports
  - `hunt_summary` - Threat hunt reports
  - `incident_report` - Incident response reports
- `REPORT_NAME_SUFFIX` - Descriptive suffix (e.g., case ID, IOC value, hunt name)
- *(Optional)* `TARGET_DIRECTORY` - Directory to save in (default: `./reports/`)

## Workflow

### Step 1: Construct Filename

Generate standardized filename:
```
{TARGET_DIRECTORY}/{REPORT_TYPE}_{REPORT_NAME_SUFFIX}_{YYYYMMDD_HHMM}.md
```

Examples:
- `./reports/alert_triage_case_1234_20250115_1430.md`
- `./reports/ioc_enrichment_198.51.100.10_20250115_0900.md`
- `./reports/hunt_summary_APT29_20250115_1200.md`

### Step 2: Write File

Use the Write tool to save `REPORT_CONTENT` to the constructed path.

## Outputs

| Output | Description |
|--------|-------------|
| `REPORT_FILE_PATH` | Full path to the saved report file |
| `WRITE_STATUS` | Success/failure status of the write operation |

## Report Template Structure

```markdown
# [Report Type]: [Subject]

**Generated:** [timestamp]
**Runbook:** [runbook name that generated this]
**Case/Alert ID:** [if applicable]

## Summary
[Brief overview of findings]

## Details
[Detailed findings, enrichment data, etc.]

## Assessment
[Risk assessment, classification]

## Recommendations
[Next steps, actions to take]

## Appendix
[Raw data, tool outputs, diagrams]
```

## Naming Convention

| Report Type | Suffix Example | Full Example |
|-------------|----------------|--------------|
| alert_triage | case_1234 | `alert_triage_case_1234_20250115_1430.md` |
| ioc_enrichment | evil.com | `ioc_enrichment_evil.com_20250115_0900.md` |
| hunt_summary | APT29 | `hunt_summary_APT29_20250115_1200.md` |
