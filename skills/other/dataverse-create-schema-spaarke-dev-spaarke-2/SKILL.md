# dataverse-create-schema

---
description: Create or update Dataverse schema components (entities, attributes, relationships, option sets) via Web API
tags: [dataverse, schema, entities, attributes, relationships, powershell]
techStack: [dataverse, power-platform, powershell, web-api]
appliesTo: ["create entity", "add column", "create table", "dataverse schema", "add field", "create relationship"]
alwaysApply: false
---

## Purpose

**Tier 1 Component Skill** - Creates or updates Dataverse schema components programmatically using the Dataverse Web API and PowerShell. This skill provides patterns for:

- Creating global option sets (choice columns)
- Creating new entities (tables)
- Adding attributes (columns) to entities
- Creating lookup relationships (1:N)
- Creating many-to-many relationships (N:N)
- Extending existing entities with new fields

**Why Web API Instead of PAC CLI?**
- PAC CLI (v1.46+) doesn't have direct `pac table create` or `pac column create` commands
- Web API provides full control over all metadata properties
- Idempotent scripts can safely re-run without errors
- Supports all attribute types and relationship configurations

---

## When to Use

- User says "create Dataverse entity", "add column to table", "create relationship"
- Task has tags: `dataverse`, `schema`, `entity`, `table`
- Need to create/modify Dataverse schema programmatically
- Deploying schema changes to multiple environments
- Schema definition exists in design docs or POML task files

---

## Prerequisites

### 1. Azure CLI Authentication

Required for obtaining Dataverse access tokens:

```powershell
# Login to Azure (if not already)
az login

# Verify account
az account show
```

### 2. PAC CLI Authentication (for verification)

```powershell
# Authenticate to target environment
pac auth create --environment https://spaarkedev1.crm.dynamics.com

# Verify connection
pac auth list
```

### 3. Target Environment URL

Standard environments:
| Environment | URL |
|-------------|-----|
| Dev | `https://spaarkedev1.crm.dynamics.com` |

---

## Core Patterns

### Authentication and Headers

```powershell
# Get OAuth token using Azure CLI
$Environment = "spaarkedev1.crm.dynamics.com"
$token = (az account get-access-token --resource "https://$Environment" --query accessToken -o tsv)

# Standard headers for Dataverse Web API
$headers = @{
    "Authorization" = "Bearer $token"
    "OData-MaxVersion" = "4.0"
    "OData-Version" = "4.0"
    "Content-Type" = "application/json"
    "Accept" = "application/json"
    "Prefer" = "return=representation"
}

$BaseUrl = "https://$Environment/api/data/v9.2"
```

### API Helper Function

```powershell
function Invoke-DataverseApi {
    param(
        [string]$Token,
        [string]$BaseUrl,
        [string]$Endpoint,
        [string]$Method = "GET",
        [object]$Body = $null
    )

    $uri = "$BaseUrl/$Endpoint"
    $headers = @{
        "Authorization" = "Bearer $Token"
        "OData-MaxVersion" = "4.0"
        "OData-Version" = "4.0"
        "Content-Type" = "application/json"
        "Accept" = "application/json"
    }

    $params = @{
        Uri = $uri
        Headers = $headers
        Method = $Method
    }

    if ($Body) {
        $params.Body = ($Body | ConvertTo-Json -Depth 20 -Compress)
    }

    return Invoke-RestMethod @params
}
```

### Label Helper

```powershell
function New-Label {
    param([string]$Text)
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.Label"
        "LocalizedLabels" = @(
            @{
                "@odata.type" = "Microsoft.Dynamics.CRM.LocalizedLabel"
                "Label" = $Text
                "LanguageCode" = 1033  # English
            }
        )
    }
}
```

---

## Attribute Type Definitions

### String Attribute

```powershell
function New-StringAttribute {
    param(
        [string]$SchemaName,
        [string]$DisplayName,
        [string]$Description,
        [int]$MaxLength = 200,
        [bool]$Required = $false
    )
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.StringAttributeMetadata"
        "SchemaName" = $SchemaName
        "RequiredLevel" = @{ "Value" = if ($Required) { "ApplicationRequired" } else { "None" } }
        "MaxLength" = $MaxLength
        "DisplayName" = New-Label -Text $DisplayName
        "Description" = New-Label -Text $Description
    }
}
```

### Memo (Multiline Text) Attribute

```powershell
function New-MemoAttribute {
    param(
        [string]$SchemaName,
        [string]$DisplayName,
        [string]$Description,
        [int]$MaxLength = 100000
    )
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.MemoAttributeMetadata"
        "SchemaName" = $SchemaName
        "RequiredLevel" = @{ "Value" = "None" }
        "MaxLength" = $MaxLength
        "DisplayName" = New-Label -Text $DisplayName
        "Description" = New-Label -Text $Description
    }
}
```

### Integer Attribute

```powershell
function New-IntegerAttribute {
    param(
        [string]$SchemaName,
        [string]$DisplayName,
        [string]$Description,
        [bool]$Required = $false,
        [int]$MinValue = -2147483648,
        [int]$MaxValue = 2147483647
    )
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.IntegerAttributeMetadata"
        "SchemaName" = $SchemaName
        "RequiredLevel" = @{ "Value" = if ($Required) { "ApplicationRequired" } else { "None" } }
        "DisplayName" = New-Label -Text $DisplayName
        "Description" = New-Label -Text $Description
        "MinValue" = $MinValue
        "MaxValue" = $MaxValue
    }
}
```

### Boolean Attribute

**Note**: Boolean attributes require an OptionSet definition with TrueOption/FalseOption.

```powershell
function New-BooleanAttribute {
    param(
        [string]$SchemaName,
        [string]$DisplayName,
        [string]$Description
    )
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.BooleanAttributeMetadata"
        "SchemaName" = $SchemaName
        "RequiredLevel" = @{ "Value" = "None" }
        "DisplayName" = New-Label -Text $DisplayName
        "Description" = New-Label -Text $Description
        "OptionSet" = @{
            "TrueOption" = @{
                "Value" = 1
                "Label" = New-Label -Text "Yes"
            }
            "FalseOption" = @{
                "Value" = 0
                "Label" = New-Label -Text "No"
            }
        }
    }
}
```

### Picklist (Choice) Attribute with Global Option Set

```powershell
function New-PicklistAttribute {
    param(
        [string]$SchemaName,
        [string]$DisplayName,
        [string]$Description,
        [string]$GlobalOptionSetName,
        [bool]$Required = $false
    )
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.PicklistAttributeMetadata"
        "SchemaName" = $SchemaName
        "RequiredLevel" = @{ "Value" = if ($Required) { "ApplicationRequired" } else { "None" } }
        "DisplayName" = New-Label -Text $DisplayName
        "Description" = New-Label -Text $Description
        "GlobalOptionSet@odata.bind" = "/GlobalOptionSetDefinitions(Name='$GlobalOptionSetName')"
    }
}
```

### DateTime Attribute

```powershell
function New-DateTimeAttribute {
    param(
        [string]$SchemaName,
        [string]$DisplayName,
        [string]$Description
    )
    return @{
        "@odata.type" = "Microsoft.Dynamics.CRM.DateTimeAttributeMetadata"
        "SchemaName" = $SchemaName
        "RequiredLevel" = @{ "Value" = "None" }
        "DisplayName" = New-Label -Text $DisplayName
        "Description" = New-Label -Text $Description
        "Format" = "DateAndTime"
        "DateTimeBehavior" = @{ "Value" = "UserLocal" }
    }
}
```

---

## Entity Operations

### Create New Entity

```powershell
function New-Entity {
    param(
        [string]$Token,
        [string]$BaseUrl,
        [string]$SchemaName,
        [string]$DisplayName,
        [string]$PluralName,
        [string]$Description,
        [bool]$IsAutoNumber = $false
    )

    $entityDef = @{
        "@odata.type" = "Microsoft.Dynamics.CRM.EntityMetadata"
        "SchemaName" = $SchemaName
        "DisplayName" = New-Label -Text $DisplayName
        "DisplayCollectionName" = New-Label -Text $PluralName
        "Description" = New-Label -Text $Description
        "OwnershipType" = "OrganizationOwned"
        "IsActivity" = $false
        "HasNotes" = $false
        "HasActivities" = $false
        "PrimaryNameAttribute" = "sprk_name"
        "Attributes" = @(
            @{
                "@odata.type" = "Microsoft.Dynamics.CRM.StringAttributeMetadata"
                "SchemaName" = "sprk_name"
                "RequiredLevel" = @{ "Value" = "ApplicationRequired" }
                "MaxLength" = 200
                "DisplayName" = New-Label -Text "Name"
                "Description" = New-Label -Text "Primary name field"
                "IsPrimaryName" = $true
                "AutoNumberFormat" = if ($IsAutoNumber) { "{SEQNUM:6}" } else { $null }
            }
        )
    }

    Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "EntityDefinitions" -Method "POST" -Body $entityDef
    Write-Host "  Created entity: $SchemaName" -ForegroundColor Green
}
```

### Add Attribute to Existing Entity

```powershell
function Add-EntityAttribute {
    param(
        [string]$Token,
        [string]$BaseUrl,
        [string]$EntityLogicalName,
        [hashtable]$AttributeDef
    )

    $endpoint = "EntityDefinitions(LogicalName='$EntityLogicalName')/Attributes"
    Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint $endpoint -Method "POST" -Body $AttributeDef
    Write-Host "    Created: $($AttributeDef.SchemaName)" -ForegroundColor Green
}
```

### Check If Entity/Attribute Exists

```powershell
function Test-EntityExists {
    param([string]$Token, [string]$BaseUrl, [string]$LogicalName)
    try {
        Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "EntityDefinitions(LogicalName='$LogicalName')" -Method "GET" | Out-Null
        return $true
    } catch { return $false }
}

function Test-AttributeExists {
    param([string]$Token, [string]$BaseUrl, [string]$EntityLogicalName, [string]$AttributeLogicalName)
    try {
        Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "EntityDefinitions(LogicalName='$EntityLogicalName')/Attributes(LogicalName='$AttributeLogicalName')" -Method "GET" | Out-Null
        return $true
    } catch { return $false }
}
```

---

## Relationship Operations

### Create Lookup (1:N) Relationship

**CRITICAL**: Lookup attributes CANNOT be created directly via AttributeMetadata. You MUST create them via RelationshipDefinitions.

```powershell
function New-OneToManyRelationship {
    param(
        [string]$Token,
        [string]$BaseUrl,
        [string]$ReferencedEntity,      # Parent entity (1 side)
        [string]$ReferencingEntity,     # Child entity (N side)
        [string]$LookupSchemaName,      # e.g., "sprk_parentid"
        [string]$LookupDisplayName,
        [string]$LookupDescription,
        [bool]$Required = $false,
        [string]$DeleteBehavior = "RemoveLink"  # RemoveLink, Restrict, Cascade
    )

    $relationshipSchemaName = "sprk_$($ReferencedEntity)_$($ReferencingEntity)_$($LookupSchemaName -replace 'sprk_', '')"

    $relationshipDef = @{
        "@odata.type" = "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata"
        "SchemaName" = $relationshipSchemaName
        "ReferencedEntity" = $ReferencedEntity
        "ReferencingEntity" = $ReferencingEntity
        "CascadeConfiguration" = @{
            "Assign" = "NoCascade"
            "Delete" = $DeleteBehavior
            "Merge" = "NoCascade"
            "Reparent" = "NoCascade"
            "Share" = "NoCascade"
            "Unshare" = "NoCascade"
        }
        "Lookup" = @{
            "SchemaName" = $LookupSchemaName
            "DisplayName" = New-Label -Text $LookupDisplayName
            "Description" = New-Label -Text $LookupDescription
            "RequiredLevel" = @{ "Value" = if ($Required) { "ApplicationRequired" } else { "None" } }
        }
    }

    Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "RelationshipDefinitions" -Method "POST" -Body $relationshipDef
    Write-Host "    Created lookup: $LookupSchemaName" -ForegroundColor Green
}
```

### Delete Behavior Options

| Behavior | Description |
|----------|-------------|
| `Cascade` | Delete child records when parent is deleted |
| `Restrict` | Prevent parent deletion if children exist |
| `RemoveLink` | Clear the lookup value on children (default) |

### Create Many-to-Many (N:N) Relationship

```powershell
function New-ManyToManyRelationship {
    param(
        [string]$Token,
        [string]$BaseUrl,
        [string]$Entity1LogicalName,
        [string]$Entity2LogicalName,
        [string]$RelationshipSchemaName  # e.g., "sprk_entity1_entity2"
    )

    $relationshipDef = @{
        "@odata.type" = "Microsoft.Dynamics.CRM.ManyToManyRelationshipMetadata"
        "SchemaName" = $RelationshipSchemaName
        "Entity1LogicalName" = $Entity1LogicalName
        "Entity2LogicalName" = $Entity2LogicalName
        "Entity1AssociatedMenuConfiguration" = @{
            "Behavior" = "UseCollectionName"
            "Group" = "Details"
            "Order" = 10000
        }
        "Entity2AssociatedMenuConfiguration" = @{
            "Behavior" = "UseCollectionName"
            "Group" = "Details"
            "Order" = 10000
        }
        "IntersectEntityName" = $RelationshipSchemaName
    }

    Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "RelationshipDefinitions" -Method "POST" -Body $relationshipDef
    Write-Host "  Created N:N: $RelationshipSchemaName" -ForegroundColor Green
}
```

---

## Global Option Set Operations

### Create Global Option Set

```powershell
function New-GlobalOptionSet {
    param(
        [string]$Token,
        [string]$BaseUrl,
        [string]$Name,
        [string]$DisplayName,
        [string]$Description,
        [hashtable[]]$Options  # @{ Value = 0; Label = "Option1" }, ...
    )

    $optionSetDef = @{
        "@odata.type" = "Microsoft.Dynamics.CRM.OptionSetMetadata"
        "Name" = $Name
        "DisplayName" = New-Label -Text $DisplayName
        "Description" = New-Label -Text $Description
        "IsGlobal" = $true
        "OptionSetType" = "Picklist"
        "Options" = @(
            $Options | ForEach-Object {
                @{
                    "Value" = $_.Value
                    "Label" = New-Label -Text $_.Label
                }
            }
        )
    }

    Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "GlobalOptionSetDefinitions" -Method "POST" -Body $optionSetDef
    Write-Host "  Created option set: $Name" -ForegroundColor Green
}

# Example usage:
$statusOptions = @(
    @{ Value = 0; Label = "Pending" },
    @{ Value = 1; Label = "Running" },
    @{ Value = 2; Label = "Completed" },
    @{ Value = 3; Label = "Failed" }
)
New-GlobalOptionSet -Token $token -BaseUrl $baseUrl -Name "sprk_status" -DisplayName "Status" -Description "Execution status" -Options $statusOptions
```

### Get Global Option Set (for referencing in picklist attributes)

```powershell
function Get-GlobalOptionSet {
    param([string]$Token, [string]$BaseUrl, [string]$Name)
    return Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "GlobalOptionSetDefinitions(Name='$Name')" -Method "GET"
}
```

---

## Publishing Customizations

After creating schema components, publish to make them available:

```powershell
function Publish-Customizations {
    param(
        [string]$Token,
        [string]$BaseUrl,
        [string[]]$EntityLogicalNames  # Optional - specific entities only
    )

    if ($EntityLogicalNames -and $EntityLogicalNames.Count -gt 0) {
        $entityXml = ($EntityLogicalNames | ForEach-Object { "<entity>$_</entity>" }) -join ""
        $publishXml = @{
            "ParameterXml" = "<importexportxml><entities>$entityXml</entities></importexportxml>"
        }
    } else {
        $publishXml = @{
            "ParameterXml" = "<importexportxml><entities/></importexportxml>"
        }
    }

    Invoke-DataverseApi -Token $Token -BaseUrl $BaseUrl -Endpoint "PublishXml" -Method "POST" -Body $publishXml
    Write-Host "Customizations published" -ForegroundColor Green
}
```

---

## Script Execution Order

When creating schema, follow this order to avoid dependency issues:

```
Phase 1: Global Option Sets
    ↓ (Option sets must exist before picklist attributes)
Phase 2: Lookup Reference Entities (small lookup tables)
    ↓ (Reference entities must exist before lookups to them)
Phase 3: Extend Existing Entities (add fields to existing tables)
    ↓ (Existing entities get new fields)
Phase 4: Create New Entities with Attributes and Relationships
    ↓ (New entities created with all components)
Phase 5: Create N:N Relationships
    ↓ (Both entities must exist first)
Phase 6: Publish Customizations
```

---

## Reference Scripts

The following scripts in the repository demonstrate these patterns:

### Main Schema Deployment

**`projects/ai-node-playbook-builder/scripts/Deploy-PlaybookNodeSchema.ps1`**
- Complete 5-phase deployment script
- Creates option sets, entities, attributes, lookups
- Idempotent (checks for existing items before creating)

### Add Missing Attributes

**`projects/ai-node-playbook-builder/scripts/Fix-PlaybookNodeAttributes.ps1`**
- Pattern for adding attributes to existing entities
- Focused on a single entity or set of entities
- Useful for incremental schema updates

### Create N:N Relationships

**`projects/ai-node-playbook-builder/scripts/Create-NNRelationships.ps1`**
- Pattern for many-to-many relationships
- Includes boolean attribute creation with OptionSet

### Existing Script Pattern Reference

**`scripts/Deploy-ChartDefinitionEntity.ps1`**
- Original pattern script
- Shows entity creation with custom fields

---

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `LookupAttributeMetadata cannot be created through the SDK` | Tried to create lookup via Attributes endpoint | Use RelationshipDefinitions endpoint with OneToManyRelationshipMetadata |
| `DefaultValue property does not exist` | DefaultValue not valid for some attribute types | Remove DefaultValue from IntegerAttributeMetadata |
| `An unexpected error occurred` | Transient API error or malformed request | Re-run script (idempotent design), check JSON structure |
| `Entity with name X already exists` | Entity already created | Add existence check before creation |
| `GlobalOptionSet not found` | Option set referenced before creation | Create global option sets in Phase 1 |

---

## Verification

After deployment, verify schema:

```powershell
# Verify entity exists
$entity = Invoke-DataverseApi -Token $token -BaseUrl $baseUrl `
    -Endpoint "EntityDefinitions(LogicalName='sprk_myentity')?`$select=LogicalName"

# Verify attributes
$attrs = Invoke-DataverseApi -Token $token -BaseUrl $baseUrl `
    -Endpoint "EntityDefinitions(LogicalName='sprk_myentity')?`$expand=Attributes(`$select=LogicalName,AttributeType)"

$attrs.Attributes | Where-Object { $_.LogicalName -like "sprk_*" } |
    ForEach-Object { "$($_.LogicalName) ($($_.AttributeType))" }

# Verify relationships
$rels = Invoke-DataverseApi -Token $token -BaseUrl $baseUrl `
    -Endpoint "EntityDefinitions(LogicalName='sprk_myentity')/ManyToOneRelationships?`$select=SchemaName,ReferencedEntity"

# Verify N:N relationships
$nn = Invoke-DataverseApi -Token $token -BaseUrl $baseUrl `
    -Endpoint "EntityDefinitions(LogicalName='sprk_myentity')/ManyToManyRelationships?`$select=SchemaName"
```

---

## Integration with Other Skills

| Skill | Relationship |
|-------|--------------|
| `dataverse-deploy` | Deploy solutions after schema creation |
| `task-execute` | May invoke this skill for tasks with `dataverse`, `schema` tags |
| `adr-aware` | ADR-022 requires unmanaged solutions |

---

## ADR Compliance

- **ADR-022**: All schema changes must use **unmanaged solutions** only
- Schema created via Web API is automatically unmanaged
- Never deploy managed solutions to dev environments

---

## Example: Complete Entity Creation

```powershell
# Create entity with all attribute types
$token = (az account get-access-token --resource "https://spaarkedev1.crm.dynamics.com" --query accessToken -o tsv)
$baseUrl = "https://spaarkedev1.crm.dynamics.com/api/data/v9.2"

# 1. Create option set
New-GlobalOptionSet -Token $token -BaseUrl $baseUrl -Name "sprk_mystatus" -DisplayName "My Status" -Description "Status options" -Options @(
    @{ Value = 0; Label = "Draft" },
    @{ Value = 1; Label = "Active" },
    @{ Value = 2; Label = "Archived" }
)

# 2. Create entity
New-Entity -Token $token -BaseUrl $baseUrl -SchemaName "sprk_myentity" -DisplayName "My Entity" -PluralName "My Entities" -Description "Sample entity"

# 3. Add attributes
Add-EntityAttribute -Token $token -BaseUrl $baseUrl -EntityLogicalName "sprk_myentity" -AttributeDef `
    (New-StringAttribute -SchemaName "sprk_code" -DisplayName "Code" -Description "Unique code" -MaxLength 50 -Required $true)

Add-EntityAttribute -Token $token -BaseUrl $baseUrl -EntityLogicalName "sprk_myentity" -AttributeDef `
    (New-MemoAttribute -SchemaName "sprk_notes" -DisplayName "Notes" -Description "Additional notes" -MaxLength 100000)

Add-EntityAttribute -Token $token -BaseUrl $baseUrl -EntityLogicalName "sprk_myentity" -AttributeDef `
    (New-PicklistAttribute -SchemaName "sprk_status" -DisplayName "Status" -Description "Record status" -GlobalOptionSetName "sprk_mystatus")

# 4. Create lookup (if parent entity exists)
New-OneToManyRelationship -Token $token -BaseUrl $baseUrl -ReferencedEntity "sprk_parententity" -ReferencingEntity "sprk_myentity" `
    -LookupSchemaName "sprk_parentid" -LookupDisplayName "Parent" -LookupDescription "Parent record" -Required $true -DeleteBehavior "Cascade"

# 5. Publish
Publish-Customizations -Token $token -BaseUrl $baseUrl -EntityLogicalNames @("sprk_myentity")
```

---

*Skill created from Task 009 implementation patterns. For questions, see the reference scripts in `projects/ai-node-playbook-builder/scripts/`.*
