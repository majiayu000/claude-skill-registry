---
name: close-case-artifact
description: "Close a case or alert with proper reason and documentation. Use when triage determines an alert is FP/BTP or investigation is complete. Requires artifact ID, type, closure reason, and root cause."
required_roles:
  soar: roles/chronicle.editor
personas: [tier1-analyst, tier2-analyst, tier3-analyst, incident-responder]
---

# Close Case Artifact Skill

Close a case or alert with the required reason, root cause, and justification comment.

## Inputs

- `ARTIFACT_ID` - The ID of the case or alert to close
- `ARTIFACT_TYPE` - Either "Case" or "Alert"
- `CLOSURE_REASON` - Must be one of:
  - `MALICIOUS` - Confirmed threat
  - `NOT_MALICIOUS` - False positive or benign
  - `MAINTENANCE` - System/maintenance activity
  - `INCONCLUSIVE` - Unable to determine
  - `UNKNOWN` - Unknown/other
- `ROOT_CAUSE` - Must match a predefined root cause (use `get_case_settings_root_causes` to list options)
- `CLOSURE_COMMENT` - Detailed justification for closure
- *(Optional)* `ALERT_GROUP_IDENTIFIERS` - Alert group identifiers
- *(Optional, for alerts)* `ASSIGN_TO_USER` - User to assign closed alert to
- *(Optional, for alerts)* `TAGS` - Comma-separated tags

## Workflow

### Step 1: Execute Closure

**For Cases:**
```
secops-soar.siemplify_close_case(
    case_id=ARTIFACT_ID,
    reason=CLOSURE_REASON,
    root_cause=ROOT_CAUSE,
    comment=CLOSURE_COMMENT,
    alert_group_identifiers=ALERT_GROUP_IDENTIFIERS
)
```

**For Alerts:**
```
secops-soar.siemplify_close_alert(
    alert_id=ARTIFACT_ID,
    reason=CLOSURE_REASON,
    root_cause=ROOT_CAUSE,
    comment=CLOSURE_COMMENT,
    assign_to_user=ASSIGN_TO_USER,
    tags=TAGS
)
```

## Outputs

| Output | Description |
|--------|-------------|
| `CLOSURE_STATUS` | Success/failure status of the closure |

## Common Closure Patterns

| Scenario | Reason | Typical Root Cause |
|----------|--------|-------------------|
| False Positive | `NOT_MALICIOUS` | "Legit action", "Normal behavior" |
| Duplicate | `NOT_MALICIOUS` | "Similar case is already under investigation" |
| Benign True Positive | `NOT_MALICIOUS` | "Legit action" |
| Confirmed Threat (remediated) | `MALICIOUS` | Varies by threat type |
| Unable to determine | `INCONCLUSIVE` | "Insufficient data" |

## Get Valid Root Causes

If unsure of valid root cause values:
```
secops-soar.get_case_settings_root_causes()
```
