---
name: adf-validation-rules
description: Comprehensive Azure Data Factory validation rules, activity nesting limitations, linked service requirements, and edge-case handling guidance
---

## 🚨 CRITICAL GUIDELINES

### Windows File Path Requirements

**MANDATORY: Always Use Backslashes on Windows for File Paths**

When using Edit or Write tools on Windows, you MUST use backslashes (`\`) in file paths, NOT forward slashes (`/`).

**Examples:**
- ❌ WRONG: `D:/repos/project/file.tsx`
- ✅ CORRECT: `D:\repos\project\file.tsx`

This applies to:
- Edit tool file_path parameter
- Write tool file_path parameter
- All file operations on Windows systems


### Documentation Guidelines

**NEVER create new documentation files unless explicitly requested by the user.**

- **Priority**: Update existing README.md files rather than creating new documentation
- **Repository cleanliness**: Keep repository root clean - only README.md unless user requests otherwise
- **Style**: Documentation should be concise, direct, and professional - avoid AI-generated tone
- **User preference**: Only create additional .md files when user specifically asks for documentation


---

# Azure Data Factory Validation Rules and Limitations

## 🚨 CRITICAL: Activity Nesting Limitations

Azure Data Factory has **STRICT** nesting rules for control flow activities. Violating these rules will cause pipeline failures or prevent pipeline creation.

### Supported Control Flow Activities for Nesting

Four control flow activities support nested activities:
- **ForEach**: Iterates over collections and executes activities in a loop
- **If Condition**: Branches based on true/false evaluation
- **Until**: Implements do-until loops with timeout options
- **Switch**: Evaluates activities matching case conditions

### ✅ PERMITTED Nesting Combinations

| Parent Activity | Can Contain | Notes |
|----------------|-------------|-------|
| **ForEach** | If Condition | ✅ Allowed |
| **ForEach** | Switch | ✅ Allowed |
| **Until** | If Condition | ✅ Allowed |
| **Until** | Switch | ✅ Allowed |

### ❌ PROHIBITED Nesting Combinations

| Parent Activity | CANNOT Contain | Reason |
|----------------|----------------|---------|
| **If Condition** | ForEach | ❌ Not supported - use Execute Pipeline workaround |
| **If Condition** | Switch | ❌ Not supported - use Execute Pipeline workaround |
| **If Condition** | Until | ❌ Not supported - use Execute Pipeline workaround |
| **If Condition** | Another If | ❌ Cannot nest If within If |
| **Switch** | ForEach | ❌ Not supported - use Execute Pipeline workaround |
| **Switch** | If Condition | ❌ Not supported - use Execute Pipeline workaround |
| **Switch** | Until | ❌ Not supported - use Execute Pipeline workaround |
| **Switch** | Another Switch | ❌ Cannot nest Switch within Switch |
| **ForEach** | Another ForEach | ❌ Single level only - use Execute Pipeline workaround |
| **Until** | Another Until | ❌ Single level only - use Execute Pipeline workaround |
| **ForEach** | Until | ❌ Single level only - use Execute Pipeline workaround |
| **Until** | ForEach | ❌ Single level only - use Execute Pipeline workaround |

### 🚫 Special Activity Restrictions

**Validation Activity**:
- ❌ **CANNOT** be placed inside ANY nested activity
- ❌ **CANNOT** be used within ForEach, If, Switch, or Until activities
- ✅ Must be at pipeline root level only

### 🔧 Workaround: Execute Pipeline Pattern

**The ONLY supported workaround for prohibited nesting combinations:**

Instead of direct nesting, use the **Execute Pipeline Activity** to call a child pipeline:

```json
{
  "name": "ParentPipeline_WithIfCondition",
  "activities": [
    {
      "name": "IfCondition_Parent",
      "type": "IfCondition",
      "typeProperties": {
        "expression": "@equals(pipeline().parameters.ProcessData, 'true')",
        "ifTrueActivities": [
          {
            "name": "ExecuteChildPipeline_WithForEach",
            "type": "ExecutePipeline",
            "typeProperties": {
              "pipeline": {
                "referenceName": "ChildPipeline_ForEachLoop",
                "type": "PipelineReference"
              },
              "parameters": {
                "ItemList": "@pipeline().parameters.Items"
              }
            }
          }
        ]
      }
    }
  ]
}
```

**Child Pipeline Structure:**
```json
{
  "name": "ChildPipeline_ForEachLoop",
  "parameters": {
    "ItemList": {"type": "array"}
  },
  "activities": [
    {
      "name": "ForEach_InChildPipeline",
      "type": "ForEach",
      "typeProperties": {
        "items": "@pipeline().parameters.ItemList",
        "activities": [
          // Your ForEach logic here
        ]
      }
    }
  ]
}
```

**Why This Works:**
- Each pipeline can have ONE level of nesting
- Execute Pipeline creates a new pipeline context
- Child pipeline gets its own nesting level allowance
- Enables unlimited depth through pipeline chaining

## 🔢 Activity and Resource Limits

### Pipeline Limits
| Resource | Limit | Notes |
|----------|-------|-------|
| **Activities per pipeline** | 80 | Includes inner activities for containers |
| **Parameters per pipeline** | 50 | - |
| **ForEach concurrent iterations** | 50 (maximum) | Set via `batchCount` property |
| **ForEach items** | 100,000 | - |
| **Lookup activity rows** | 5,000 | Maximum rows returned |
| **Lookup activity size** | 4 MB | Maximum size of returned data |
| **Web activity timeout** | 1 hour | Default timeout for Web activities |
| **Copy activity timeout** | 7 days | Maximum execution time |

### ForEach Activity Configuration
```json
{
  "name": "ForEachActivity",
  "type": "ForEach",
  "typeProperties": {
    "items": "@pipeline().parameters.ItemList",
    "isSequential": false,  // false = parallel execution
    "batchCount": 50,       // Max 50 concurrent iterations
    "activities": [
      // Nested activities
    ]
  }
}
```

**Critical Considerations:**
- `isSequential: true` → Executes one item at a time (slow but predictable)
- `isSequential: false` → Executes up to `batchCount` items in parallel
- Maximum `batchCount` is **50** regardless of setting
- **Cannot use Set Variable activity** inside parallel ForEach (variable scope is pipeline-level)

### Set Variable Activity Limitations
❌ **CANNOT** use `Set Variable` inside ForEach with `isSequential: false`
- Reason: Variables are pipeline-scoped, not ForEach-scoped
- Multiple parallel iterations would cause race conditions
- ✅ **Alternative**: Use `Append Variable` with array type, or use sequential execution

## 📊 Linked Services: Azure Blob Storage

### Authentication Methods

#### 1. Account Key (Basic)
```json
{
  "type": "AzureBlobStorage",
  "typeProperties": {
    "connectionString": {
      "type": "SecureString",
      "value": "DefaultEndpointsProtocol=https;AccountName=<account>;AccountKey=<key>"
    }
  }
}
```
**⚠️ Limitations:**
- Secondary Blob service endpoints are **NOT supported**
- **Security Risk**: Account keys should be stored in Azure Key Vault

#### 2. Shared Access Signature (SAS)
```json
{
  "type": "AzureBlobStorage",
  "typeProperties": {
    "sasUri": {
      "type": "SecureString",
      "value": "https://<account>.blob.core.windows.net/<container>?<SAS-token>"
    }
  }
}
```
**Critical Requirements:**
- Dataset `folderPath` must be **absolute path from container level**
- SAS token expiry **must extend beyond pipeline execution**
- SAS URI path must align with dataset configuration

#### 3. Service Principal
```json
{
  "type": "AzureBlobStorage",
  "typeProperties": {
    "serviceEndpoint": "https://<account>.blob.core.windows.net",
    "accountKind": "StorageV2",  // REQUIRED for service principal
    "servicePrincipalId": "<client-id>",
    "servicePrincipalCredential": {
      "type": "SecureString",
      "value": "<client-secret>"
    },
    "tenant": "<tenant-id>"
  }
}
```
**Critical Requirements:**
- `accountKind` **MUST** be set (StorageV2, BlobStorage, or BlockBlobStorage)
- Service Principal requires **Storage Blob Data Reader** (source) or **Storage Blob Data Contributor** (sink) role
- ❌ **NOT compatible** with soft-deleted blob accounts in Data Flow

#### 4. Managed Identity (Recommended)
```json
{
  "type": "AzureBlobStorage",
  "typeProperties": {
    "serviceEndpoint": "https://<account>.blob.core.windows.net",
    "accountKind": "StorageV2"  // REQUIRED for managed identity
  },
  "connectVia": {
    "referenceName": "AutoResolveIntegrationRuntime",
    "type": "IntegrationRuntimeReference"
  }
}
```
**Critical Requirements:**
- `accountKind` **MUST** be specified (cannot be empty or "Storage")
- ❌ Empty or "Storage" account kind will cause Data Flow failures
- Managed identity must have **Storage Blob Data Reader/Contributor** role assigned
- For Storage firewall: **Must enable "Allow trusted Microsoft services"**

### Common Blob Storage Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Data Flow fails with managed identity | `accountKind` empty or "Storage" | Set `accountKind` to StorageV2 |
| Secondary endpoint doesn't work | Using account key auth | Not supported - use different auth method |
| SAS token expired during run | Token expiry too short | Extend SAS token validity period |
| Cannot access $logs container | System container not visible in UI | Use direct path reference |
| Soft-deleted blobs inaccessible | Service principal/managed identity | Use account key or SAS instead |
| Private endpoint connection fails | Wrong endpoint for Data Flow | Ensure ADLS Gen2 private endpoint exists |

## 📊 Linked Services: Azure SQL Database

### Authentication Methods

#### 1. SQL Authentication
```json
{
  "type": "AzureSqlDatabase",
  "typeProperties": {
    "server": "<server-name>.database.windows.net",
    "database": "<database-name>",
    "authenticationType": "SQL",
    "userName": "<username>",
    "password": {
      "type": "SecureString",
      "value": "<password>"
    }
  }
}
```
**Best Practice:**
- Store password in Azure Key Vault
- Use connection string with Key Vault reference

#### 2. Service Principal
```json
{
  "type": "AzureSqlDatabase",
  "typeProperties": {
    "server": "<server-name>.database.windows.net",
    "database": "<database-name>",
    "authenticationType": "ServicePrincipal",
    "servicePrincipalId": "<client-id>",
    "servicePrincipalCredential": {
      "type": "SecureString",
      "value": "<client-secret>"
    },
    "tenant": "<tenant-id>"
  }
}
```
**Requirements:**
- Microsoft Entra admin must be configured on SQL server
- Service principal must have contained database user created
- Grant appropriate role: `db_datareader`, `db_datawriter`, etc.

#### 3. Managed Identity
```json
{
  "type": "AzureSqlDatabase",
  "typeProperties": {
    "server": "<server-name>.database.windows.net",
    "database": "<database-name>",
    "authenticationType": "SystemAssignedManagedIdentity"
  }
}
```
**Requirements:**
- Create contained database user for managed identity
- Grant appropriate database roles
- Configure firewall to allow Azure services (or specific IP ranges)

### SQL Database Configuration Best Practices

#### Connection String Parameters
```
Server=tcp:<server>.database.windows.net,1433;
Database=<database>;
Encrypt=mandatory;          // Options: mandatory, optional, strict
TrustServerCertificate=false;
ConnectTimeout=30;
CommandTimeout=120;
Pooling=true;
ConnectRetryCount=3;
ConnectRetryInterval=10;
```

**Critical Parameters:**
- `Encrypt`: Default is `mandatory` (recommended)
- `Pooling`: Set to `false` if experiencing idle connection issues
- `ConnectRetryCount`: Recommended for transient fault handling
- `ConnectRetryInterval`: Seconds between retries

### Common SQL Database Pitfalls

| Issue | Cause | Solution |
|-------|-------|----------|
| Serverless tier auto-paused | Pipeline doesn't wait for resume | Implement retry logic or keep-alive |
| Connection pool timeout | Idle connections closed | Add `Pooling=false` or configure retry |
| Firewall blocks connection | IP not whitelisted | Add Azure IR IPs or enable Azure services |
| Always Encrypted fails in Data Flow | Not supported for sink | Use service principal/managed identity in copy activity |
| Decimal precision loss | Copy supports up to 28 precision | Use string type for higher precision |
| Parallel copy not working | No partition configuration | Enable physical or dynamic range partitioning |

### Performance Optimization

#### Parallel Copy Configuration
```json
{
  "source": {
    "type": "AzureSqlSource",
    "partitionOption": "PhysicalPartitionsOfTable"  // or "DynamicRange"
  },
  "parallelCopies": 8,  // Recommended: (DIU or IR nodes) × (2 to 4)
  "enableStaging": true,
  "stagingSettings": {
    "linkedServiceName": {
      "referenceName": "AzureBlobStorage",
      "type": "LinkedServiceReference"
    }
  }
}
```

**Partition Options:**
- `PhysicalPartitionsOfTable`: Uses SQL Server physical partitions
- `DynamicRange`: Creates logical partitions based on column values
- `None`: No partitioning (default)

**Staging Best Practices:**
- Always use staging for large data movements (> 1GB)
- Use PolyBase or COPY statement for best performance
- Parquet format recommended for staging files

## 🔍 Data Flow Limitations

### General Limits
- **Column name length**: 128 characters maximum
- **Row size**: 1 MB maximum (some sinks like SQL have lower limits)
- **String column size**: Varies by sink (SQL: 8000 for varchar, 4000 for nvarchar)

### Transformation-Specific Limits
| Transformation | Limitation |
|----------------|------------|
| **Lookup** | Cache size limited by cluster memory |
| **Join** | Large joins may cause memory errors |
| **Pivot** | Maximum 10,000 unique values |
| **Window** | Requires partitioning for large datasets |

### Performance Considerations
- **Partitioning**: Always partition large datasets before transformations
- **Broadcast**: Use broadcast hint for small dimension tables
- **Sink optimization**: Enable table option "Recreate" instead of "Truncate" for better performance

## 🛡️ Validation Checklist for Pipeline Creation

### Before Creating Pipeline
- [ ] Verify activity nesting follows permitted combinations
- [ ] Check ForEach activities don't contain other ForEach/Until
- [ ] Verify If/Switch activities don't contain ForEach/Until/If/Switch
- [ ] Ensure Validation activities are at pipeline root level only
- [ ] Confirm total activities < 80 per pipeline
- [ ] Verify no Set Variable activities in parallel ForEach

### Linked Service Validation
- [ ] **Blob Storage**: If using managed identity/service principal, `accountKind` is set
- [ ] **SQL Database**: Authentication method matches security requirements
- [ ] **All services**: Secrets stored in Key Vault, not hardcoded
- [ ] **All services**: Firewall rules configured for integration runtime IPs
- [ ] **Network**: Private endpoints configured if using VNet integration

### Activity Configuration Validation
- [ ] **ForEach**: `batchCount` ≤ 50 if parallel execution
- [ ] **Lookup**: Query returns < 5000 rows and < 4 MB data
- [ ] **Copy**: DIU configured appropriately (2-256 for Azure IR)
- [ ] **Copy**: Staging enabled for large data movements
- [ ] **All activities**: Timeout values appropriate for expected execution time
- [ ] **All activities**: Retry logic configured for transient failures

### Data Flow Validation
- [ ] Column names ≤ 128 characters
- [ ] Source query doesn't return > 1 MB per row
- [ ] Partitioning configured for large datasets
- [ ] Sink has appropriate schema and data type mappings
- [ ] Staging linked service configured for optimal performance

## 🔍 Automated Validation Script

**CRITICAL: Always run automated validation before committing or deploying ADF pipelines!**

The adf-master plugin includes a comprehensive PowerShell validation script that checks for ALL the rules and limitations documented above.

### Using the Validation Script

**Location:** `${CLAUDE_PLUGIN_ROOT}/scripts/validate-adf-pipelines.ps1`

**Basic usage:**
```powershell
# From the root of your ADF repository
pwsh -File validate-adf-pipelines.ps1
```

**With custom paths:**
```powershell
pwsh -File validate-adf-pipelines.ps1 `
    -PipelinePath "path/to/pipeline" `
    -DatasetPath "path/to/dataset"
```

**With strict mode (additional warnings):**
```powershell
pwsh -File validate-adf-pipelines.ps1 -Strict
```

### What the Script Validates

The automated validation script checks for issues that Microsoft's official `@microsoft/azure-data-factory-utilities` package does **NOT** validate:

1. **Activity Nesting Violations:**
   - ForEach → ForEach, Until, Validation
   - Until → Until, ForEach, Validation
   - IfCondition → ForEach, If, IfCondition, Switch, Until, Validation
   - Switch → ForEach, If, IfCondition, Switch, Until, Validation

2. **Resource Limits:**
   - Pipeline activity count (max 120, warn at 100)
   - Pipeline parameter count (max 50)
   - Pipeline variable count (max 50)
   - ForEach batchCount limit (max 50, warn at 30 in strict mode)

3. **Variable Scope Violations:**
   - SetVariable in parallel ForEach (causes race conditions)
   - Proper AppendVariable vs SetVariable usage

4. **Dataset Configuration Issues:**
   - Missing fileName or wildcardFileName for file-based datasets
   - AzureBlobFSLocation missing required fileSystem property
   - Missing required properties for DelimitedText, Json, Parquet types

5. **Copy Activity Validations:**
   - Source/sink type compatibility with dataset types
   - Lookup activity firstRowOnly=false warnings (5000 row/4MB limits)
   - Blob file dependencies (additionalColumns logging pattern)

### Integration with CI/CD

**GitHub Actions example:**
```yaml
- name: Validate ADF Pipelines
  run: |
    pwsh -File validate-adf-pipelines.ps1 -PipelinePath pipeline -DatasetPath dataset
  shell: pwsh
```

**Azure DevOps example:**
```yaml
- task: PowerShell@2
  displayName: 'Validate ADF Pipelines'
  inputs:
    filePath: 'validate-adf-pipelines.ps1'
    arguments: '-PipelinePath pipeline -DatasetPath dataset'
    pwsh: true
```

### Command Reference

Use the `/adf-validate` command to run the validation script with proper guidance:

```bash
/adf-validate
```

This command will:
1. Detect your ADF repository structure
2. Run the validation script with appropriate paths
3. Parse and explain any errors or warnings found
4. Provide specific solutions for each violation
5. Recommend next actions based on results
6. Suggest CI/CD integration patterns

### Exit Codes

- **0**: Validation passed (no errors)
- **1**: Validation failed (errors found - DO NOT DEPLOY)

### Best Practices

1. **Run validation before every commit** to catch issues early
2. **Add validation to CI/CD pipeline** to prevent invalid deployments
3. **Use strict mode during development** for additional warnings
4. **Re-validate after bulk changes** or generated pipelines
5. **Document validation exceptions** if you must bypass a warning
6. **Share validation results with team** to prevent repeated mistakes

## 🚨 CRITICAL: Enforcement Protocol

**When creating or modifying ADF pipelines:**

1. **ALWAYS validate activity nesting** against the permitted/prohibited table
2. **REJECT** any attempt to create prohibited nesting combinations
3. **SUGGEST** Execute Pipeline workaround for complex nesting needs
4. **VALIDATE** linked service authentication matches the connector type
5. **CHECK** all limits (activities, parameters, ForEach iterations, etc.)
6. **VERIFY** required properties are set (e.g., `accountKind` for managed identity)
7. **WARN** about common pitfalls specific to the connector being used

**Example Validation Response:**
```
❌ INVALID PIPELINE STRUCTURE DETECTED:

Issue: ForEach activity contains another ForEach activity
Location: Pipeline "PL_DataProcessing" → ForEach "OuterLoop" → ForEach "InnerLoop"

This violates Azure Data Factory nesting rules:
- ForEach activities support only a SINGLE level of nesting
- You CANNOT nest ForEach within ForEach

✅ RECOMMENDED SOLUTION:
Use the Execute Pipeline pattern:
1. Create a child pipeline with the inner ForEach logic
2. Replace the inner ForEach with an Execute Pipeline activity
3. Pass required parameters to the child pipeline

Would you like me to generate the refactored pipeline structure?
```

## 📚 Reference Documentation

**Official Microsoft Learn Resources:**
- Activity nesting: https://learn.microsoft.com/en-us/azure/data-factory/concepts-nested-activities
- Blob Storage connector: https://learn.microsoft.com/en-us/azure/data-factory/connector-azure-blob-storage
- SQL Database connector: https://learn.microsoft.com/en-us/azure/data-factory/connector-azure-sql-database
- Pipeline limits: https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#data-factory-limits

**Last Updated:** 2025-01-24 (Based on official Microsoft documentation)

This validation rules skill MUST be consulted before creating or modifying ANY Azure Data Factory pipeline to ensure compliance with platform limitations and best practices.

## Progressive Disclosure References

For detailed validation matrices and resource limits, see:

- **Nesting Rules**: `references/nesting-rules.md` - Complete matrix of permitted and prohibited activity nesting combinations with workaround patterns
- **Resource Limits**: `references/resource-limits.md` - Complete reference for all ADF limits (pipeline, activity, trigger, data flow, integration runtime, expression, API)
