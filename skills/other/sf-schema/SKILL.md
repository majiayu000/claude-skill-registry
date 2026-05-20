---
name: sf-schema
description: |
  Scaffold custom objects, fields, validation rules, permission sets, and other
  schema metadata as SFDX source XML. Use when asked to create objects, custom
  fields, permission sets, validation rules, or generate metadata XML. Activate
  on mentions of "custom object", "custom field", "permission set", "validation
  rule", "picklist", "lookup field", or "object-meta.xml".
license: Apache-2.0
compatibility: Requires Salesforce CLI (sf) v2+. Authenticated org needed for deployment.
metadata:
  author: clientell
  version: "1.0.0"
  tags: salesforce, schema, metadata, permissions, custom-objects
# Claude Code specific
allowed-tools: Read,Write,Edit,Bash(sf *),Glob,Grep
context: fork
---

# Schema Design & Permission Management

You are a Salesforce schema and metadata specialist. Generate valid SFDX source format metadata.

## Custom Object
```xml
<!-- force-app/main/default/objects/Invoice__c/Invoice__c.object-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Invoice</label>
    <pluralLabel>Invoices</pluralLabel>
    <nameField>
        <label>Invoice Number</label>
        <type>AutoNumber</type>
        <displayFormat>INV-{000000}</displayFormat>
    </nameField>
    <deploymentStatus>Deployed</deploymentStatus>
    <sharingModel>Private</sharingModel>
    <enableActivities>true</enableActivities>
    <enableHistory>true</enableHistory>
    <enableReports>true</enableReports>
</CustomObject>
```

## Custom Fields
```xml
<!-- force-app/main/default/objects/Invoice__c/fields/Amount__c.field-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Amount__c</fullName>
    <label>Amount</label>
    <type>Currency</type>
    <precision>18</precision>
    <scale>2</scale>
    <required>true</required>
</CustomField>
```

### Common Field Types
```xml
<!-- Text -->
<type>Text</type>
<length>255</length>

<!-- Long Text Area -->
<type>LongTextArea</type>
<length>32768</length>
<visibleLines>5</visibleLines>

<!-- Picklist -->
<type>Picklist</type>
<valueSet>
    <restricted>true</restricted>
    <valueSetDefinition>
        <sorted>false</sorted>
        <value><fullName>Active</fullName><default>true</default><label>Active</label></value>
        <value><fullName>Inactive</fullName><default>false</default><label>Inactive</label></value>
    </valueSetDefinition>
</valueSet>

<!-- Lookup -->
<type>Lookup</type>
<referenceTo>Account</referenceTo>
<relationshipLabel>Invoices</relationshipLabel>
<relationshipName>Invoices</relationshipName>

<!-- Master-Detail -->
<type>MasterDetail</type>
<referenceTo>Account</referenceTo>
<relationshipLabel>Invoices</relationshipLabel>
<relationshipName>Invoices</relationshipName>
<reparentableMasterDetail>false</reparentableMasterDetail>
<writeRequiresMasterRead>false</writeRequiresMasterRead>

<!-- Checkbox -->
<type>Checkbox</type>
<defaultValue>false</defaultValue>

<!-- Date -->
<type>Date</type>

<!-- DateTime -->
<type>DateTime</type>

<!-- Number -->
<type>Number</type>
<precision>18</precision>
<scale>0</scale>

<!-- Formula -->
<type>Text</type>
<formula>Account__r.Name &amp; ' - ' &amp; TEXT(Amount__c)</formula>
```

## Validation Rules
```xml
<!-- force-app/main/default/objects/Invoice__c/validationRules/Amount_Required.validationRule-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<ValidationRule xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Amount_Must_Be_Positive</fullName>
    <active>true</active>
    <errorConditionFormula>Amount__c &lt;= 0</errorConditionFormula>
    <errorDisplayField>Amount__c</errorDisplayField>
    <errorMessage>Amount must be greater than zero.</errorMessage>
</ValidationRule>
```

## Permission Sets
```xml
<!-- force-app/main/default/permissionsets/Invoice_Manager.permissionset-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Invoice Manager</label>
    <hasActivationRequired>false</hasActivationRequired>
    <objectPermissions>
        <object>Invoice__c</object>
        <allowCreate>true</allowCreate>
        <allowDelete>false</allowDelete>
        <allowEdit>true</allowEdit>
        <allowRead>true</allowRead>
        <modifyAllRecords>false</modifyAllRecords>
        <viewAllRecords>true</viewAllRecords>
    </objectPermissions>
    <fieldPermissions>
        <field>Invoice__c.Amount__c</field>
        <editable>true</editable>
        <readable>true</readable>
    </fieldPermissions>
    <fieldPermissions>
        <field>Invoice__c.Status__c</field>
        <editable>true</editable>
        <readable>true</readable>
    </fieldPermissions>
</PermissionSet>
```

## Custom Permissions (for Flow Bypass)
```xml
<!-- force-app/main/default/customPermissions/Bypass_Automation.customPermission-meta.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<CustomPermission xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Bypass Automation</label>
    <isLicensed>false</isLicensed>
</CustomPermission>
```

### Additional Field Types

**Formula Field:**
```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>FullName__c</fullName>
    <label>Full Name</label>
    <type>Text</type>
    <formula>FirstName__c &amp; ' ' &amp; LastName__c</formula>
    <formulaTreatBlanksAs>BlankAsZero</formulaTreatBlanksAs>
</CustomField>
```

**Rollup Summary Field** (master-detail only):
```xml
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Total_Amount__c</fullName>
    <label>Total Amount</label>
    <type>Summary</type>
    <summarizedField>LineItem__c.Amount__c</summarizedField>
    <summaryOperation>sum</summaryOperation>
    <summaryForeignKey>LineItem__c.Order__c</summaryForeignKey>
</CustomField>
```

**Geolocation Field:**
```xml
<type>Location</type>
<displayLocationInDecimal>true</displayLocationInDecimal>
<scale>6</scale>
```

**Global Value Set (Reusable Picklist):**
```xml
<GlobalValueSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <masterLabel>Industries</masterLabel>
    <sorted>false</sorted>
    <customValue><fullName>Technology</fullName><default>false</default><label>Technology</label></customValue>
    <customValue><fullName>Healthcare</fullName><default>false</default><label>Healthcare</label></customValue>
</GlobalValueSet>
```

### Relationship Types
| Type | Delete Behavior | Rollup Summary | Reparenting | Max per Object |
|------|----------------|----------------|-------------|----------------|
| Master-Detail | Cascade delete | Yes | Configurable | 2 |
| Lookup | Block/Clear/Restrict | No | N/A | 40 (25 std) |
| External Lookup | N/A | No | N/A | - |
| Hierarchical | N/A | No | N/A | 1 (User only) |
| Junction (M2M) | Two master-details | On both parents | - | - |

### Record Types
```xml
<RecordType xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>Enterprise</fullName>
    <label>Enterprise</label>
    <active>true</active>
    <businessProcess>Enterprise Sales Process</businessProcess>
    <description>For enterprise accounts</description>
</RecordType>
```

### Custom Metadata Types vs Custom Settings
| Feature | Custom Metadata Types | Custom Settings (Hierarchy) |
|---------|----------------------|---------------------------|
| Deployable | Yes (metadata) | No (data) |
| SOQL required | Yes (or getInstance) | No (getOrgDefaults) |
| User/Profile override | No | Yes |
| Counts against SOQL limit | Yes | No |
| Use for | Org config, mappings | User preferences |

### Permission Set Groups
```xml
<PermissionSetGroup xmlns="http://soap.sforce.com/2006/04/metadata">
    <label>Sales Team</label>
    <permissionSets>
        <permissionSet>Account_Manager</permissionSet>
        <permissionSet>Opportunity_Editor</permissionSet>
        <permissionSet>Report_Viewer</permissionSet>
    </permissionSets>
</PermissionSetGroup>
```

## SFDX Source Directory Structure
```
force-app/main/default/
├── objects/
│   └── Invoice__c/
│       ├── Invoice__c.object-meta.xml
│       ├── fields/
│       │   ├── Amount__c.field-meta.xml
│       │   └── Status__c.field-meta.xml
│       ├── validationRules/
│       │   └── Amount_Must_Be_Positive.validationRule-meta.xml
│       └── listViews/
│           └── All.listView-meta.xml
├── permissionsets/
│   └── Invoice_Manager.permissionset-meta.xml
├── customPermissions/
│   └── Bypass_Automation.customPermission-meta.xml
└── layouts/
    └── Invoice__c-Invoice Layout.layout-meta.xml
```

## Gotchas
- Max **40 custom relationships** per object (25 for standard objects)
- Formula fields **cannot reference** LongTextArea, RichTextArea, MultiSelectPicklist, or Encrypted fields
- Rollup Summary fields work **only on Master-Detail** relationships — not Lookups
- Global Value Sets **cannot be converted back** to local picklists once shared
- Encrypted Text fields are **not searchable or sortable**
- Record type-dependent picklists require **explicit value mapping** per record type
- Permission Set Groups **recalculate asynchronously** — changes may take minutes to apply
- Custom Metadata Type records **cannot be created/updated via DML in production** — deploy only
- Profiles are **notoriously merge-conflict-prone** — prefer Permission Sets for everything

## References
- [Schema Reference](references/schema-reference.md) — formula fields, rollup summaries, geolocation, Global Value Sets, record types, page layouts, FlexiPages, custom metadata, platform events, Big Objects, quick actions, custom labels

## Workflow
1. Understand object/field requirements
2. Generate SFDX source format XML files
3. Generate permission set for new objects/fields
4. Deploy schema first, then code that references it
5. Verify with: `sf org list metadata -m CustomObject --target-org myOrg`
