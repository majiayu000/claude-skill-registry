---
name: document-in-case
description: "Add a comment to a case to document findings, actions, or recommendations. Use to maintain audit trail during investigations. Requires CASE_ID and comment text."
required_roles:
  soar: roles/chronicle.editor
personas: [tier1-analyst, tier2-analyst, tier3-analyst, threat-hunter, incident-responder]
---

# Document in Case Skill

Add a standardized comment to a case to document findings, actions taken, or recommendations.

## Inputs

- `CASE_ID` - The SOAR case ID to add the comment to
- `COMMENT_TEXT` - The full text of the comment to be added
- *(Optional)* `ALERT_GROUP_IDENTIFIERS` - Alert group identifiers if required

## Workflow

### Step 1: Post Comment

```
secops-soar.post_case_comment(
    case_id=CASE_ID,
    comment=COMMENT_TEXT,
    alert_group_identifiers=ALERT_GROUP_IDENTIFIERS  // if provided
)
```

### Step 2: Verify Status

Check the API response to confirm the comment was posted successfully.

## Outputs

| Output | Description |
|--------|-------------|
| `COMMENT_POST_STATUS` | Success/failure status of the comment posting |

## Comment Templates

**Enrichment Summary:**
```
IOC Enrichment for [IOC_VALUE] ([IOC_TYPE]):
- GTI Reputation: [score/classification]
- SIEM Activity: [first/last seen, alert count]
- IOC Match: [Yes/No]
- Assessment: [Low/Medium/High risk]
- Recommendation: [next steps]
```

**Triage Decision:**
```
Alert Triage Complete:
- Classification: [FP/BTP/TP/Suspicious]
- Key Findings: [summary]
- Rationale: [why this classification]
- Action Taken: [closed/escalated]
```

**Investigation Update:**
```
Investigation Update [timestamp]:
- Actions Completed: [list]
- Findings: [summary]
- Next Steps: [planned actions]
```
