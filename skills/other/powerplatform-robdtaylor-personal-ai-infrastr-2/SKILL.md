---
name: PowerPlatform
description: Generate Power Automate flows from natural language. Reads connector schemas from work repo, outputs deployable solution files. USE WHEN user says 'create flow', 'power automate', 'automate workflow', or describes a business process to automate.
---

# PowerPlatform - Flow Generation Skill

Generate Power Automate flows from natural language descriptions using connector schemas exported from your work environment.

## Examples

**Example: Simple notification flow**
```
User: "Create a flow that sends me a Teams message when I get an email with 'urgent' in the subject"
-> Reads Office365/Teams connector schemas
-> Generates flow JSON with email trigger + Teams action
-> Outputs solution ZIP to work repo
```

**Example: Approval workflow**
```
User: "Make a flow for document approval - when a file is added to SharePoint, start an approval, then move to approved/rejected folder"
-> Uses SharePoint trigger + Approvals + SharePoint actions
-> Includes conditional branching
-> Outputs deployable solution
```

---

## Architecture

```
Work Repo (schemas)                    PAI (this skill)
~/Projects/work/scripts/               ~/.claude/skills/PowerPlatform/
power-platform/
├── connectors/          ──reads──>    ├── SKILL.md
│   ├── shared_teams.json              ├── templates/
│   ├── shared_outlook.json            ├── reference/
│   └── ...                            └── examples/
├── manifest.json
└── generated/           <──writes──   [Solution ZIPs]
```

---

## Workflow

### 1. Check Available Connectors

Before generating, read the manifest to see what connectors are available:

```bash
cat ~/Projects/work/scripts/power-platform/manifest.json
```

If `manifest.json` doesn't exist or is stale, inform user to run the export script at work.

### 2. Parse User Request

Extract from natural language:
- **Trigger**: What starts the flow (email arrives, file created, scheduled, manual)
- **Actions**: What the flow does (send message, create item, update record)
- **Conditions**: Any branching logic (if/then, switch)
- **Data flow**: What data passes between steps

### 3. Generate Flow Definition

Create the flow JSON following Power Automate schema. Key structure:

```json
{
  "properties": {
    "definition": {
      "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
      "triggers": { ... },
      "actions": { ... }
    },
    "connectionReferences": { ... }
  }
}
```

### 4. Package as Solution

Wrap in solution structure for import:
```
solution/
├── [Content_Types].xml
├── customizations.xml
├── solution.xml
└── Workflows/
    └── {flow-guid}-{flow-name}.json
```

### 5. Output

Save to: `~/Projects/work/scripts/power-platform/generated/`

---

## Connection References

Flows use **connection references** that map to actual connections in the target environment. Use placeholder IDs that will be resolved on import:

```json
"connectionReferences": {
  "shared_teams": {
    "connectionName": "shared_teams",
    "source": "Embedded",
    "id": "/providers/Microsoft.PowerApps/apis/shared_teams",
    "tier": "NotSpecified"
  }
}
```

On import, Power Platform prompts user to map these to their actual connections.

---

## Expression Syntax

Power Automate uses a specific expression language. Common patterns:

### Dynamic Content References
```
@{triggerOutputs()?['body/subject']}           # Email subject from trigger
@{body('Get_item')?['Title']}                  # Field from previous action
@{items('Apply_to_each')?['name']}             # Current item in loop
```

### Functions
```
@{utcNow()}                                    # Current timestamp
@{concat('Hello ', triggerBody()?['name'])}   # String concatenation
@{if(equals(1,1),'yes','no')}                 # Conditional
@{length(body('Get_items')?['value'])}        # Array length
@{formatDateTime(utcNow(),'yyyy-MM-dd')}      # Date formatting
```

### Conditions
```json
"expression": {
  "and": [
    { "contains": ["@triggerOutputs()?['body/subject']", "urgent"] },
    { "equals": ["@triggerOutputs()?['body/importance']", "high"] }
  ]
}
```

See `reference/expressions.md` for full syntax guide.

---

## Common Triggers

| Trigger | Connector | Use Case |
|---------|-----------|----------|
| `When_a_new_email_arrives` | Office365 | Email automation |
| `When_a_file_is_created` | SharePoint | Document workflows |
| `When_an_item_is_created` | SharePoint | List automation |
| `When_a_row_is_added` | Dataverse | Database triggers |
| `Recurrence` | Schedule | Scheduled jobs |
| `manual` | Manual | Button-triggered |
| `When_a_HTTP_request_is_received` | HTTP | Webhook/API trigger |

---

## Common Actions

| Action | Connector | Use Case |
|--------|-----------|----------|
| `Send_an_email` | Office365 | Email notifications |
| `Post_message_in_a_chat_or_channel` | Teams | Team notifications |
| `Create_item` | SharePoint | Add list items |
| `Update_item` | SharePoint | Modify list items |
| `Start_and_wait_for_an_approval` | Approvals | Approval workflows |
| `Create_a_row` | Dataverse | Database writes |
| `HTTP` | HTTP | External API calls |

---

## Templates

Pre-built patterns in `templates/`:

- `approval-flow.json` - Standard approval workflow
- `notification-flow.json` - Event-triggered notifications
- `scheduled-report.json` - Scheduled data collection
- `form-processing.json` - Forms response handling
- `file-sync.json` - Cross-system file operations

---

## Generation Process

When asked to create a flow:

1. **Read available schemas**:
   ```bash
   ls ~/Projects/work/scripts/power-platform/connectors/
   cat ~/Projects/work/scripts/power-platform/manifest.json
   ```

2. **Load relevant connector schemas** for the requested functionality

3. **Select appropriate template** or build from scratch

4. **Generate flow JSON** with:
   - Unique GUID for flow
   - Proper trigger configuration
   - Action sequence with correct operation IDs
   - Connection references for all connectors used
   - Expression syntax for dynamic content

5. **Create solution package** using `tools/package-solution.sh`

6. **Save to generated folder** and inform user

---

## Limitations

- **Cannot deploy directly** - User must import at work
- **Connection mapping required** - User maps connections on import
- **Premium connectors** - Some require premium licenses
- **Custom connectors** - Not supported without schema export
- **Schema freshness** - Depends on export frequency at work

---

## Files Reference

| File | Purpose |
|------|---------|
| `templates/*.json` | Pre-built flow patterns |
| `reference/expressions.md` | Expression syntax guide |
| `reference/triggers.md` | Trigger configurations |
| `reference/actions.md` | Action configurations |
| `examples/*.json` | Working example flows |
| `tools/package-solution.sh` | Solution packager script |
