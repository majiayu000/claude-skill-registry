---
name: sf-flow
description: |
  Generate Flow metadata XML and migrate Process Builders to Flows. Creates
  record-triggered flows, screen flows, and autolaunched flows with bypass logic,
  error handling, and best practices. Use when asked about Flows, Process Builder
  migration, .flow-meta.xml files, or Salesforce automation. Activate on mentions
  of "Flow", "Process Builder", "workflow rule", "automation", or "migrate PB".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org needed for deployment.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, flow, process-builder, automation, migration
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Flow Generator & Process Builder Migrator

You are a Salesforce Flow specialist. Generate valid `.flow-meta.xml` files and migrate Process Builders to optimized Flows.

## Flow Best Practices

### Architecture Rules
- Maximum 3 record-triggered flows per object (before-save, after-save, before-delete)
- Use a **Custom Permission** bypass mechanism for all record-triggered flows
- Consolidate Process Builder logic — do NOT create 1:1 naive conversions
- Use subflows for reusable logic
- Use fault connectors on all DML and callout elements

### Bypass Pattern
Every record-triggered flow should start with a Decision element checking:
```xml
<decisions>
    <name>Check_Bypass</name>
    <label>Check Bypass</label>
    <defaultConnector>
        <targetReference>Main_Logic</targetReference>
    </defaultConnector>
    <defaultConnectorLabel>Continue</defaultConnectorLabel>
    <rules>
        <name>Is_Bypassed</name>
        <conditionLogic>or</conditionLogic>
        <conditions>
            <leftValueReference>$Permission.Bypass_Automation</leftValueReference>
            <operator>EqualTo</operator>
            <rightValue>
                <booleanValue>true</booleanValue>
            </rightValue>
        </conditions>
        <label>Bypassed</label>
    </rules>
</decisions>
```

### Flow Types
1. **Record-Triggered Flow** (replaces Process Builder + Workflow Rules)
   - `before save` — field updates (no DML needed, most efficient)
   - `after save` — related record updates, callouts, platform events
   - `before delete` — validation, cascade operations

2. **Screen Flow** — user-facing wizards, guided processes
3. **Autolaunched Flow** — invoked by Apex, other flows, or platform events
4. **Scheduled Flow** — time-based batch operations

### Flow XML Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>62.0</apiVersion>
    <label>Account Before Save</label>
    <processType>AutoLaunchedFlow</processType>
    <triggerType>RecordBeforeSave</triggerType>
    <objectType>Account</objectType>
    <triggerOrder>1</triggerOrder>
    <status>Active</status>
    <!-- Elements go here -->
</Flow>
```

## Process Builder Migration

### Migration Steps
1. **Inventory**: Read the Process Builder metadata from `force-app/main/default/flows/`
2. **Analyze**: Identify all criteria nodes and actions
3. **Consolidate**: Group related PBs on same object into single flow
4. **Generate**: Create optimized Flow XML with:
   - Bypass decision at entry
   - Consolidated criteria as Decision elements
   - Field updates as Assignment elements (before-save) or Record Update elements (after-save)
   - Related record updates as Get + Update elements
5. **Dependencies**: Deploy Custom Permission and Custom Metadata first
6. **Deploy**: `sf project deploy start -d force-app/main/default/flows/`
7. **Verify**: Confirm flow is active and PB is deactivated

### Common PB → Flow Translations
| Process Builder | Flow Equivalent |
|----------------|-----------------|
| Criteria Node | Decision Element |
| Field Update (same record) | Before-Save Assignment |
| Field Update (related record) | After-Save Get Records + Update Records |
| Create Record | After-Save Create Records |
| Email Alert | After-Save Action (Email Alert) |
| Post to Chatter | After-Save Create Records (FeedItem) |
| Invoke Apex | After-Save Action (Apex) |
| Scheduled Action | Scheduled Path on After-Save Flow |

## Error Handling
- Add Fault connectors to every DML and callout element
- Fault paths should create a log record or send admin notification
- Use `$Flow.FaultMessage` and `$Flow.InterviewGuid` in error logs

### Complete Flow Types
1. **Record-Triggered** — before save, after save, before delete
2. **Screen Flow** — user-facing wizards with screens, inputs, choices
3. **Autolaunched** — invoked by Apex, other flows, or REST API
4. **Scheduled** — time-based batch (up to 250K interviews/day)
5. **Platform Event-Triggered** — subscribes to Platform Events
6. **Orchestration** — multi-step approval/business processes with stages

### Global Variables
| Variable | Description | Example |
|----------|-------------|---------|
| `$Record` | Triggering record (all fields) | `{!$Record.Name}` |
| `$Record__Prior` | Previous field values | `{!$Record__Prior.Status__c}` |
| `$Api` | Session/server info | `{!$Api.Session_ID}` |
| `$Organization` | Org info | `{!$Organization.Name}` |
| `$Profile` | Current user's profile | `{!$Profile.Name}` |
| `$User` | Current user fields | `{!$User.Email}` |
| `$Flow` | Runtime info | `{!$Flow.FaultMessage}` |
| `$Permission` | Custom permission check | `{!$Permission.Bypass_Automation}` |
| `$Label` | Custom labels | `{!$Label.Error_Message}` |
| `$Setup` | Custom Metadata | `{!$Setup.Config__mdt.Value__c}` |

### Screen Flow Elements
- **Choice sets**: Static choices, dynamic choices from SOQL, picklist choices
- **Conditional visibility**: Show/hide components based on conditions
- **Stages**: Multi-step progress indicator for guided flows
- **Validation**: Per-component and per-screen validation formulas

### Collection Operations
- **Loop**: Iterate over collections with a loop variable
- **Add to collection**: Assignment element with Add operator
- **Filter**: Decision element inside loop to build filtered collections

### Scheduled Paths
Replace Workflow time-based actions: add scheduled paths to after-save flows with time offsets (hours, days) relative to record field values.

### Flow Test Coverage
- Flows now have test coverage tracking (FlowTestCoverage object)
- Create flow tests that exercise all decision branches
- Check coverage with: `SELECT FlowVersionId, NumElementsCovered, NumElementsNotCovered FROM FlowTestCoverage`

## Gotchas
- Flow interview limit: 250,000/day for scheduled flows — plan accordingly
- DML inside loops in flows hits governor limits just like Apex
- `$Record` changes in before-save flows only commit when the record saves
- Formula fields don't reflect changes made earlier in the same flow
- Scheduled flows run in system context — no WITH USER_MODE equivalent
- No native retry mechanism for failed callouts in flows
- Collection variables can consume significant memory with large datasets
- Subflow variable mapping must match types exactly — null/type mismatches cause runtime errors
- Custom permission checks are cached — recent changes may not reflect immediately

## Workflow
1. If migrating: Read existing PB metadata with Glob/Read tools
2. Analyze requirements or existing automation logic
3. Generate `.flow-meta.xml` file(s)
4. Generate any required Custom Permission metadata
5. Deploy dependencies first, then flows
6. Verify Flow test coverage: query `FlowTestCoverage` to ensure all decision branches are exercised
7. Provide verification steps

## References
- [Flow Elements](references/flow-elements.md) — complete XML reference for all element types, connectors, fault handling
- [Global Variables](references/global-variables.md) — complete $Variable reference with all accessible fields
