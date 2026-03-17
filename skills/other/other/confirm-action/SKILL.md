---
name: confirm-action
description: "Ask the user to confirm before taking a significant action. Use before containment, remediation, or other impactful operations to ensure analyst approval. Presents options and waits for response."
personas: [all]
---

# Confirm Action Skill

Ask the user a confirmation question before proceeding with a significant action.

## Inputs

- `QUESTION_TEXT` - The specific question to ask (e.g., "Isolate endpoint WORKSTATION-01?", "Proceed with account disable for jsmith?")
- *(Optional)* `RESPONSE_OPTIONS` - Predefined options for the user:
  - Default: `["Yes", "No"]`
  - Custom examples: `["Disable Account", "Reset Password", "Monitor Only"]`

## Workflow

### Step 1: Present Question

Display the question to the user with available options.

### Step 2: Wait for Response

Collect the user's selection or custom input.

### Step 3: Return Response

Provide the response back to the calling workflow for decision branching.

## Outputs

| Output | Description |
|--------|-------------|
| `USER_RESPONSE` | The user's answer to the confirmation question |

## When to Use

**Always confirm before:**
- Isolating/quarantining endpoints
- Disabling user accounts
- Blocking IPs/domains at firewall
- Terminating processes
- Deleting files
- Escalating to incident response
- Closing cases as false positive (for high-severity alerts)

**May skip confirmation for:**
- Adding comments to cases
- Running enrichment queries
- Generating reports
- Read-only operations

## Example Confirmations

**Containment:**
```
Question: "Isolate endpoint WORKSTATION-01 from the network?"
Options: ["Yes - Isolate", "No - Continue Monitoring", "Escalate First"]
```

**Account Action:**
```
Question: "User jsmith shows signs of compromise. What action?"
Options: ["Disable Account", "Force Password Reset", "Monitor Only", "Escalate to IR"]
```

**Case Closure:**
```
Question: "Close case 1234 as False Positive?"
Options: ["Yes - Close FP", "No - Keep Open", "Escalate to Tier 2"]
```
