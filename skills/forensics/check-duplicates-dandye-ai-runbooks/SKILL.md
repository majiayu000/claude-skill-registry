---
name: check-duplicates
description: "Check for duplicate or similar cases. Use before deep analysis to avoid investigating the same incident twice. Takes a CASE_ID and returns list of similar cases."
required_roles:
  soar: roles/chronicle.editor
personas: [tier1-analyst, tier2-analyst, tier3-analyst]
---

# Check Duplicates Skill

Identify potentially duplicate or similar existing cases before starting deep analysis.

## Inputs

- `CASE_ID` - The ID of the current case to check
- `ALERT_GROUP_IDENTIFIERS` - Alert group identifiers for the case
- *(Optional)* `DAYS_BACK` - How many days to search back (default: 7)
- *(Optional)* `INCLUDE_OPEN` - Include open cases (default: true)
- *(Optional)* `INCLUDE_CLOSED` - Include closed cases (default: false)

## Workflow

### Step 1: Execute Similarity Check

```
secops-soar.siemplify_get_similar_cases(
    case_id=CASE_ID,
    alert_group_identifiers=ALERT_GROUP_IDENTIFIERS,
    days_back=DAYS_BACK,
    include_open_cases=INCLUDE_OPEN,
    include_closed_cases=INCLUDE_CLOSED
)
```

### Step 2: Process Results

Extract the list of similar case IDs from the response.

## Outputs

| Output | Description |
|--------|-------------|
| `SIMILAR_CASE_IDS` | List of case IDs identified as potentially similar/duplicate |
| `SIMILARITY_CHECK_STATUS` | Success/failure status of the check |

## Usage Pattern

```
1. Check duplicates BEFORE enrichment
2. If duplicates found:
   - Review similar case(s)
   - If confirmed duplicate: close as duplicate
   - If related but distinct: note correlation, continue
3. If no duplicates: proceed with analysis
```

## When Duplicates Are Found

If `SIMILAR_CASE_IDS` is not empty:

1. Document: "Closing as duplicate of [Similar Case ID]"
2. Close with:
   - Reason: `NOT_MALICIOUS`
   - Root cause: `Similar case is already under investigation`
