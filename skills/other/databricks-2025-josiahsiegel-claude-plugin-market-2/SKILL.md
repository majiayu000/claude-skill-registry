---
name: databricks-2025
description: Databricks Job activity and 2025 Azure Data Factory connectors
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

# Azure Data Factory Databricks Integration 2025

## Databricks Job Activity (Recommended 2025)

**🚨 CRITICAL UPDATE (2025):** The Databricks Job activity is now the **ONLY recommended method** for orchestrating Databricks in ADF. Microsoft strongly recommends migrating from legacy Notebook, Python, and JAR activities.

### Why Databricks Job Activity?

**Old Pattern (Notebook Activity - ❌ LEGACY):**
```json
{
  "name": "RunNotebook",
  "type": "DatabricksNotebook",  // ❌ DEPRECATED - Migrate to DatabricksJob
  "linkedServiceName": { "referenceName": "DatabricksLinkedService" },
  "typeProperties": {
    "notebookPath": "/Users/user@example.com/MyNotebook",
    "baseParameters": { "param1": "value1" }
  }
}
```

**New Pattern (Databricks Job Activity - ✅ CURRENT 2025):**
```json
{
  "name": "RunDatabricksWorkflow",
  "type": "DatabricksJob",  // ✅ CORRECT activity type (NOT DatabricksSparkJob)
  "linkedServiceName": { "referenceName": "DatabricksLinkedService" },
  "typeProperties": {
    "jobId": "123456",  // Reference existing Databricks Workflow Job
    "jobParameters": {  // Pass parameters to the Job
      "param1": "value1",
      "runDate": "@pipeline().parameters.ProcessingDate"
    }
  },
  "policy": {
    "timeout": "0.12:00:00",
    "retry": 2,
    "retryIntervalInSeconds": 30
  }
}
```

### Benefits of Databricks Job Activity (2025)

1. **Serverless Execution by Default:**
   - ✅ No cluster specification needed in linked service
   - ✅ Automatically runs on Databricks serverless compute
   - ✅ Faster startup times and lower costs
   - ✅ Managed infrastructure by Databricks

2. **Advanced Workflow Features:**
   - ✅ **Run As** - Execute jobs as specific users/service principals
   - ✅ **Task Values** - Pass data between tasks within workflow
   - ✅ **Conditional Execution** - If/Else and For Each task types
   - ✅ **AI/BI Tasks** - Model serving endpoints, Power BI semantic models
   - ✅ **Repair Runs** - Rerun failed tasks without reprocessing successful ones
   - ✅ **Notifications/Alerts** - Built-in alerting on job failures
   - ✅ **Git Integration** - Version control for notebooks and code
   - ✅ **DABs Support** - Databricks Asset Bundles for deployment
   - ✅ **Built-in Lineage** - Data lineage tracking across tasks
   - ✅ **Queuing and Concurrent Runs** - Better resource management

3. **Centralized Job Management:**
   - Jobs defined once in Databricks workspace
   - Single source of truth for all environments
   - Versioning through Databricks (Git-backed)
   - Consistent across orchestration tools

4. **Better Orchestration:**
   - Complex task dependencies within Job
   - Multiple heterogeneous tasks (notebook, Python, SQL, Delta Live Tables)
   - Job-level monitoring and logging
   - Parameter passing between tasks

5. **Improved Reliability:**
   - Retry logic at Job and task level
   - Better error handling and recovery
   - Automatic cluster management

6. **Cost Optimization:**
   - Serverless compute (pay only for execution)
   - Job clusters (auto-terminating)
   - Optimized cluster sizing per task
   - Spot instance support

### Implementation

#### 1. Create Databricks Job

```python
# In Databricks workspace
# Create Job with tasks
{
  "name": "Data Processing Job",
  "tasks": [
    {
      "task_key": "ingest",
      "notebook_task": {
        "notebook_path": "/Notebooks/Ingest",
        "base_parameters": {}
      },
      "job_cluster_key": "small_cluster"
    },
    {
      "task_key": "transform",
      "depends_on": [{ "task_key": "ingest" }],
      "notebook_task": {
        "notebook_path": "/Notebooks/Transform"
      },
      "job_cluster_key": "medium_cluster"
    },
    {
      "task_key": "load",
      "depends_on": [{ "task_key": "transform" }],
      "notebook_task": {
        "notebook_path": "/Notebooks/Load"
      },
      "job_cluster_key": "small_cluster"
    }
  ],
  "job_clusters": [
    {
      "job_cluster_key": "small_cluster",
      "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "Standard_DS3_v2",
        "num_workers": 2
      }
    },
    {
      "job_cluster_key": "medium_cluster",
      "new_cluster": {
        "spark_version": "13.3.x-scala2.12",
        "node_type_id": "Standard_DS4_v2",
        "num_workers": 8
      }
    }
  ]
}

# Get Job ID after creation
```

#### 2. Create ADF Pipeline with Databricks Job Activity (2025)

```json
{
  "name": "PL_Databricks_Serverless_Workflow",
  "properties": {
    "activities": [
      {
        "name": "ExecuteDatabricksWorkflow",
        "type": "DatabricksJob",  // ✅ Correct activity type
        "dependsOn": [],
        "policy": {
          "timeout": "0.12:00:00",
          "retry": 2,
          "retryIntervalInSeconds": 30
        },
        "typeProperties": {
          "jobId": "123456",  // Databricks Job ID from workspace
          "jobParameters": {  // ⚠️ Use jobParameters (not parameters)
            "input_path": "/mnt/data/input",
            "output_path": "/mnt/data/output",
            "run_date": "@pipeline().parameters.runDate",
            "environment": "@pipeline().parameters.environment"
          }
        },
        "linkedServiceName": {
          "referenceName": "DatabricksLinkedService_Serverless",
          "type": "LinkedServiceReference"
        }
      },
      {
        "name": "LogJobExecution",
        "type": "WebActivity",
        "dependsOn": [
          {
            "activity": "ExecuteDatabricksWorkflow",
            "dependencyConditions": ["Succeeded"]
          }
        ],
        "typeProperties": {
          "url": "@pipeline().parameters.LoggingEndpoint",
          "method": "POST",
          "body": {
            "jobId": "123456",
            "runId": "@activity('ExecuteDatabricksWorkflow').output.runId",
            "status": "Succeeded",
            "duration": "@activity('ExecuteDatabricksWorkflow').output.executionDuration"
          }
        }
      }
    ],
    "parameters": {
      "runDate": {
        "type": "string",
        "defaultValue": "@utcnow()"
      },
      "environment": {
        "type": "string",
        "defaultValue": "production"
      },
      "LoggingEndpoint": {
        "type": "string"
      }
    }
  }
}
```

#### 3. Configure Linked Service (2025 - Serverless)

**✅ RECOMMENDED: Serverless Linked Service (No Cluster Configuration)**
```json
{
  "name": "DatabricksLinkedService_Serverless",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "AzureDatabricks",
    "typeProperties": {
      "domain": "https://adb-123456789.azuredatabricks.net",
      "authentication": "MSI"  // ✅ Managed Identity (recommended 2025)
      // ⚠️ NO existingClusterId or newClusterNodeType needed for serverless!
      // The Databricks Job activity automatically uses serverless compute
    }
  }
}
```

**Alternative: Access Token Authentication**
```json
{
  "name": "DatabricksLinkedService_Token",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "AzureDatabricks",
    "typeProperties": {
      "domain": "https://adb-123456789.azuredatabricks.net",
      "accessToken": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "AzureKeyVault",
          "type": "LinkedServiceReference"
        },
        "secretName": "databricks-access-token"
      }
    }
  }
}
```

**🚨 CRITICAL: For Databricks Job activity, DO NOT specify cluster properties in the linked service. The job configuration in Databricks workspace controls compute resources.**

## 🆕 2025 New Connectors and Enhancements

### ServiceNow V2 Connector (RECOMMENDED - V1 End of Support)

**🚨 CRITICAL: ServiceNow V1 connector is at End of Support stage. Migrate to V2 immediately!**

**Key Features of V2:**
- ✅ **Native Query Builder** - Aligns with ServiceNow's condition builder experience
- ✅ **Enhanced Performance** - Optimized data extraction
- ✅ **Better Error Handling** - Improved diagnostics and retry logic
- ✅ **OData Support** - Modern API integration patterns

**Copy Activity Example:**
```json
{
  "name": "CopyFromServiceNowV2",
  "type": "Copy",
  "inputs": [
    {
      "referenceName": "ServiceNowV2Source",
      "type": "DatasetReference"
    }
  ],
  "outputs": [
    {
      "referenceName": "AzureSqlSink",
      "type": "DatasetReference"
    }
  ],
  "typeProperties": {
    "source": {
      "type": "ServiceNowV2Source",
      "query": "sysparm_query=active=true^priority=1^sys_created_on>=javascript:gs.dateGenerate('2025-01-01')",
      "httpRequestTimeout": "00:01:40"  // 100 seconds
    },
    "sink": {
      "type": "AzureSqlSink",
      "writeBehavior": "upsert",
      "upsertSettings": {
        "useTempDB": true,
        "keys": ["sys_id"]
      }
    },
    "enableStaging": true,
    "stagingSettings": {
      "linkedServiceName": {
        "referenceName": "AzureBlobStorage",
        "type": "LinkedServiceReference"
      }
    }
  }
}
```

**Linked Service (OAuth2 - Recommended):**
```json
{
  "name": "ServiceNowV2LinkedService",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "ServiceNowV2",
    "typeProperties": {
      "endpoint": "https://dev12345.service-now.com",
      "authenticationType": "OAuth2",
      "clientId": "your-oauth-client-id",
      "clientSecret": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "AzureKeyVault",
          "type": "LinkedServiceReference"
        },
        "secretName": "servicenow-client-secret"
      },
      "username": "service-account@company.com",
      "password": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "AzureKeyVault",
          "type": "LinkedServiceReference"
        },
        "secretName": "servicenow-password"
      },
      "grantType": "password"
    }
  }
}
```

**Linked Service (Basic Authentication - Legacy):**
```json
{
  "name": "ServiceNowV2LinkedService_Basic",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "ServiceNowV2",
    "typeProperties": {
      "endpoint": "https://dev12345.service-now.com",
      "authenticationType": "Basic",
      "username": "admin",
      "password": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "AzureKeyVault",
          "type": "LinkedServiceReference"
        },
        "secretName": "servicenow-password"
      }
    }
  }
}
```

**Migration from V1 to V2:**
1. Update linked service type from `ServiceNow` to `ServiceNowV2`
2. Update source type from `ServiceNowSource` to `ServiceNowV2Source`
3. Test queries in ServiceNow UI's condition builder first
4. Adjust timeout settings if needed (V2 may have different performance)

### Enhanced PostgreSQL Connector

Improved performance and features:

```json
{
  "name": "PostgreSQLLinkedService",
  "type": "PostgreSql",
  "typeProperties": {
    "connectionString": "host=myserver.postgres.database.azure.com;port=5432;database=mydb;uid=myuser",
    "password": {
      "type": "AzureKeyVaultSecret",
      "store": { "referenceName": "KeyVault" },
      "secretName": "postgres-password"
    },
    // 2025 enhancement
    "enableSsl": true,
    "sslMode": "Require"
  }
}
```

### Microsoft Fabric Warehouse Connector (NEW 2025)

**🆕 Native support for Microsoft Fabric Warehouse (Q3 2024+)**

**Supported Activities:**
- ✅ Copy Activity (source and sink)
- ✅ Lookup Activity
- ✅ Get Metadata Activity
- ✅ Script Activity
- ✅ Stored Procedure Activity

**Linked Service Configuration:**
```json
{
  "name": "FabricWarehouseLinkedService",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "Warehouse",  // ✅ NEW dedicated Fabric Warehouse type
    "typeProperties": {
      "endpoint": "myworkspace.datawarehouse.fabric.microsoft.com",
      "warehouse": "MyWarehouse",
      "authenticationType": "ServicePrincipal",  // Recommended
      "servicePrincipalId": "<app-registration-id>",
      "servicePrincipalKey": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "AzureKeyVault",
          "type": "LinkedServiceReference"
        },
        "secretName": "fabric-warehouse-sp-key"
      },
      "tenant": "<tenant-id>"
    }
  }
}
```

**Alternative: Managed Identity Authentication (Preferred)**
```json
{
  "name": "FabricWarehouseLinkedService_ManagedIdentity",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "Warehouse",
    "typeProperties": {
      "endpoint": "myworkspace.datawarehouse.fabric.microsoft.com",
      "warehouse": "MyWarehouse",
      "authenticationType": "SystemAssignedManagedIdentity"
    }
  }
}
```

**Copy Activity Example:**
```json
{
  "name": "CopyToFabricWarehouse",
  "type": "Copy",
  "inputs": [
    {
      "referenceName": "AzureSqlSource",
      "type": "DatasetReference"
    }
  ],
  "outputs": [
    {
      "referenceName": "FabricWarehouseSink",
      "type": "DatasetReference"
    }
  ],
  "typeProperties": {
    "source": {
      "type": "AzureSqlSource"
    },
    "sink": {
      "type": "WarehouseSink",
      "writeBehavior": "insert",  // or "upsert"
      "writeBatchSize": 10000,
      "tableOption": "autoCreate"  // Auto-create table if not exists
    },
    "enableStaging": true,  // Recommended for large data
    "stagingSettings": {
      "linkedServiceName": {
        "referenceName": "AzureBlobStorage",
        "type": "LinkedServiceReference"
      },
      "path": "staging/fabric-warehouse"
    },
    "translator": {
      "type": "TabularTranslator",
      "mappings": [
        {
          "source": { "name": "CustomerID" },
          "sink": { "name": "customer_id" }
        }
      ]
    }
  }
}
```

**Best Practices for Fabric Warehouse:**
- ✅ Use managed identity for authentication (no secret rotation)
- ✅ Enable staging for large data loads (> 1GB)
- ✅ Use `tableOption: autoCreate` for dynamic schema creation
- ✅ Leverage Fabric's lakehouse integration for unified analytics
- ✅ Monitor Fabric capacity units (CU) consumption

### Enhanced Snowflake Connector

Improved performance:

```json
{
  "name": "SnowflakeLinkedService",
  "type": "Snowflake",
  "typeProperties": {
    "connectionString": "jdbc:snowflake://myaccount.snowflakecomputing.com",
    "database": "mydb",
    "warehouse": "mywarehouse",
    "authenticationType": "KeyPair",
    "username": "myuser",
    "privateKey": {
      "type": "AzureKeyVaultSecret",
      "store": { "referenceName": "KeyVault" },
      "secretName": "snowflake-private-key"
    },
    "privateKeyPassphrase": {
      "type": "AzureKeyVaultSecret",
      "store": { "referenceName": "KeyVault" },
      "secretName": "snowflake-passphrase"
    }
  }
}
```

## Managed Identity for Azure Storage (2025)

### Azure Table Storage

Now supports system-assigned and user-assigned managed identity:

```json
{
  "name": "AzureTableStorageLinkedService",
  "type": "AzureTableStorage",
  "typeProperties": {
    "serviceEndpoint": "https://mystorageaccount.table.core.windows.net",
    "authenticationType": "ManagedIdentity"  // New in 2025
    // Or user-assigned:
    // "credential": {
    //   "referenceName": "UserAssignedManagedIdentity"
    // }
  }
}
```

### Azure Files

Now supports managed identity authentication:

```json
{
  "name": "AzureFilesLinkedService",
  "type": "AzureFileStorage",
  "typeProperties": {
    "fileShare": "myshare",
    "accountName": "mystorageaccount",
    "authenticationType": "ManagedIdentity"  // New in 2025
  }
}
```

## Mapping Data Flows - Spark 3.3

Spark 3.3 now powers Mapping Data Flows:

**Performance Improvements:**
- 30% faster data processing
- Improved memory management
- Better partition handling
- Enhanced join performance

**New Features:**
- Adaptive Query Execution (AQE)
- Dynamic partition pruning
- Improved caching
- Better column statistics

```json
{
  "name": "DataFlow1",
  "type": "MappingDataFlow",
  "typeProperties": {
    "sources": [
      {
        "dataset": { "referenceName": "SourceDataset" }
      }
    ],
    "transformations": [
      {
        "name": "Transform1"
      }
    ],
    "sinks": [
      {
        "dataset": { "referenceName": "SinkDataset" }
      }
    ]
  }
}
```

## Azure DevOps Server 2022 Support

Git integration now supports on-premises Azure DevOps Server 2022:

```json
{
  "name": "DataFactory",
  "properties": {
    "repoConfiguration": {
      "type": "AzureDevOpsGit",
      "accountName": "on-prem-ado-server",
      "projectName": "MyProject",
      "repositoryName": "adf-repo",
      "collaborationBranch": "main",
      "rootFolder": "/",
      "hostName": "https://ado-server.company.com"  // On-premises server
    }
  }
}
```

## 🔐 Managed Identity 2025 Best Practices

### User-Assigned vs System-Assigned Managed Identity

**System-Assigned Managed Identity:**
```json
{
  "type": "AzureBlobStorage",
  "typeProperties": {
    "serviceEndpoint": "https://mystorageaccount.blob.core.windows.net",
    "accountKind": "StorageV2"
    // ✅ Uses Data Factory's system-assigned identity automatically
  }
}
```

**User-Assigned Managed Identity (NEW 2025):**
```json
{
  "type": "AzureBlobStorage",
  "typeProperties": {
    "serviceEndpoint": "https://mystorageaccount.blob.core.windows.net",
    "accountKind": "StorageV2",
    "credential": {
      "referenceName": "UserAssignedManagedIdentityCredential",
      "type": "CredentialReference"
    }
  }
}
```

**When to Use User-Assigned:**
- ✅ Sharing identity across multiple data factories
- ✅ Complex multi-environment setups
- ✅ Granular permission management
- ✅ Identity lifecycle independent of data factory

**Credential Consolidation (NEW 2025):**

ADF now supports a centralized **Credentials** feature:
```json
{
  "name": "ManagedIdentityCredential",
  "type": "Microsoft.DataFactory/factories/credentials",
  "properties": {
    "type": "ManagedIdentity",
    "typeProperties": {
      "resourceId": "/subscriptions/{sub}/resourceGroups/{rg}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{identity-name}"
    }
  }
}
```

**Benefits:**
- ✅ Consolidate all Microsoft Entra ID-based credentials in one place
- ✅ Reuse credentials across multiple linked services
- ✅ Centralized permission management
- ✅ Easier audit and compliance tracking

### MFA Enforcement Compatibility (October 2025)

**🚨 IMPORTANT: Azure requires MFA for all users by October 2025**

**Impact on ADF:**
- ✅ **Managed identities are UNAFFECTED** - No MFA required for service accounts
- ✅ Continue using system-assigned and user-assigned identities without changes
- ❌ **Interactive user logins affected** - Personal Azure AD accounts need MFA
- ✅ **Service principals with certificate auth** - Recommended alternative to secrets

**Best Practice:**
```json
{
  "type": "AzureSqlDatabase",
  "typeProperties": {
    "server": "myserver.database.windows.net",
    "database": "mydb",
    "authenticationType": "SystemAssignedManagedIdentity"
    // ✅ No MFA needed, no secret rotation, passwordless
  }
}
```

### Principle of Least Privilege (2025)

**Storage Blob Data Roles:**
- `Storage Blob Data Reader` - Read-only access (source)
- `Storage Blob Data Contributor` - Read/write access (sink)
- ❌ Avoid `Storage Blob Data Owner` unless needed

**SQL Database Roles:**
```sql
-- Create contained database user for managed identity
CREATE USER [datafactory-name] FROM EXTERNAL PROVIDER;

-- Grant minimal required permissions
ALTER ROLE db_datareader ADD MEMBER [datafactory-name];
ALTER ROLE db_datawriter ADD MEMBER [datafactory-name];

-- ❌ Avoid db_owner unless truly needed
```

**Key Vault Access Policies:**
```json
{
  "permissions": {
    "secrets": ["Get"]  // ✅ Only Get permission needed
    // ❌ Don't grant List, Set, Delete unless required
  }
}
```

## Best Practices (2025)

1. **Use Databricks Job Activity (MANDATORY):**
   - ❌ STOP using Notebook, Python, JAR activities
   - ✅ Migrate to DatabricksJob activity immediately
   - ✅ Define workflows in Databricks workspace
   - ✅ Leverage serverless compute (no cluster config needed)
   - ✅ Utilize advanced features (Run As, Task Values, If/Else, Repair Runs)

2. **Managed Identity Authentication (MANDATORY 2025):**
   - ✅ Use managed identities for ALL Azure resources
   - ✅ Prefer system-assigned for simple scenarios
   - ✅ Use user-assigned for shared identity needs
   - ✅ Leverage Credentials feature for consolidation
   - ✅ MFA-compliant for October 2025 enforcement
   - ❌ Avoid access keys and connection strings
   - ✅ Store any remaining secrets in Key Vault

3. **Monitor Job Execution:**
   - Track Databricks Job run IDs from ADF output
   - Log Job parameters for auditability
   - Set up alerts for job failures
   - Use Databricks job-level monitoring
   - Leverage built-in lineage tracking

4. **Optimize Spark 3.3 Usage (Data Flows):**
   - Enable Adaptive Query Execution (AQE)
   - Use appropriate partition counts (4-8 per core)
   - Monitor execution plans in Databricks
   - Use broadcast joins for small dimensions
   - Implement dynamic partition pruning

## Resources

- [Databricks Job Activity](https://learn.microsoft.com/azure/data-factory/transform-data-using-databricks-spark-job)
- [ADF Connectors](https://learn.microsoft.com/azure/data-factory/connector-overview)
- [Managed Identity Authentication](https://learn.microsoft.com/azure/data-factory/data-factory-service-identity)
- [Mapping Data Flows](https://learn.microsoft.com/azure/data-factory/concepts-data-flow-overview)
