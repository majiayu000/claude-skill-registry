---
name: fabric-onelake-2025
description: Microsoft Fabric Lakehouse, OneLake, and Fabric Warehouse connectors for Azure Data Factory (2025)
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

# Microsoft Fabric Integration with Azure Data Factory (2025)

## Overview

Microsoft Fabric represents a unified SaaS analytics platform that combines Power BI, Azure Synapse Analytics, and Azure Data Factory capabilities. Azure Data Factory now provides native connectors for Fabric Lakehouse and Fabric Warehouse, enabling seamless data movement between ADF and Fabric workspaces.

## Microsoft Fabric Lakehouse Connector

The Fabric Lakehouse connector enables both read and write operations to Microsoft Fabric Lakehouse for tables and files.

### Supported Activities
- ✅ Copy Activity (source and sink)
- ✅ Lookup Activity
- ✅ Get Metadata Activity
- ✅ Delete Activity

### Linked Service Configuration

**Using Service Principal Authentication (Recommended):**
```json
{
  "name": "FabricLakehouseLinkedService",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "Lakehouse",
    "typeProperties": {
      "workspaceId": "12345678-1234-1234-1234-123456789abc",
      "artifactId": "87654321-4321-4321-4321-cba987654321",
      "servicePrincipalId": "<app-registration-client-id>",
      "servicePrincipalKey": {
        "type": "AzureKeyVaultSecret",
        "store": {
          "referenceName": "AzureKeyVault",
          "type": "LinkedServiceReference"
        },
        "secretName": "fabric-service-principal-key"
      },
      "tenant": "<tenant-id>"
    }
  }
}
```

**Using Managed Identity Authentication (Preferred 2025):**
```json
{
  "name": "FabricLakehouseLinkedService_ManagedIdentity",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "Lakehouse",
    "typeProperties": {
      "workspaceId": "12345678-1234-1234-1234-123456789abc",
      "artifactId": "87654321-4321-4321-4321-cba987654321"
      // Managed identity used automatically - no credentials needed!
    }
  }
}
```

**Finding Workspace and Artifact IDs:**
1. Navigate to Fabric workspace in browser
2. Copy workspace ID from URL: `https://app.powerbi.com/groups/<workspaceId>/...`
3. Open Lakehouse settings to find artifact ID
4. Or use Fabric REST API to enumerate workspace items

### Dataset Configuration

**For Lakehouse Files:**
```json
{
  "name": "FabricLakehouseFiles",
  "properties": {
    "type": "LakehouseTable",
    "linkedServiceName": {
      "referenceName": "FabricLakehouseLinkedService",
      "type": "LinkedServiceReference"
    },
    "typeProperties": {
      "table": "Files/raw/sales/2025"
    }
  }
}
```

**For Lakehouse Tables:**
```json
{
  "name": "FabricLakehouseTables",
  "properties": {
    "type": "LakehouseTable",
    "linkedServiceName": {
      "referenceName": "FabricLakehouseLinkedService",
      "type": "LinkedServiceReference"
    },
    "typeProperties": {
      "table": "SalesData"  // Table name in Lakehouse
    }
  }
}
```

### Copy Activity Examples

**Copy from Azure SQL to Fabric Lakehouse:**
```json
{
  "name": "CopyToFabricLakehouse",
  "type": "Copy",
  "inputs": [
    {
      "referenceName": "AzureSqlSource",
      "type": "DatasetReference"
    }
  ],
  "outputs": [
    {
      "referenceName": "FabricLakehouseTables",
      "type": "DatasetReference",
      "parameters": {
        "tableName": "DimCustomer"
      }
    }
  ],
  "typeProperties": {
    "source": {
      "type": "AzureSqlSource",
      "sqlReaderQuery": "SELECT * FROM dbo.Customers WHERE ModifiedDate > '@{pipeline().parameters.LastRunTime}'"
    },
    "sink": {
      "type": "LakehouseTableSink",
      "tableActionOption": "append"  // or "overwrite"
    },
    "enableStaging": false,
    "translator": {
      "type": "TabularTranslator",
      "mappings": [
        {
          "source": { "name": "CustomerID" },
          "sink": { "name": "customer_id", "type": "Int32" }
        },
        {
          "source": { "name": "CustomerName" },
          "sink": { "name": "customer_name", "type": "String" }
        }
      ]
    }
  }
}
```

**Copy Parquet Files to Fabric Lakehouse:**
```json
{
  "name": "CopyParquetToLakehouse",
  "type": "Copy",
  "inputs": [
    {
      "referenceName": "AzureBlobParquetFiles",
      "type": "DatasetReference"
    }
  ],
  "outputs": [
    {
      "referenceName": "FabricLakehouseFiles",
      "type": "DatasetReference"
    }
  ],
  "typeProperties": {
    "source": {
      "type": "ParquetSource",
      "storeSettings": {
        "type": "AzureBlobStorageReadSettings",
        "recursive": true,
        "wildcardFolderPath": "raw/sales/2025",
        "wildcardFileName": "*.parquet"
      }
    },
    "sink": {
      "type": "LakehouseFileSink",
      "storeSettings": {
        "type": "LakehouseWriteSettings",
        "copyBehavior": "PreserveHierarchy"
      }
    }
  }
}
```

### Lookup Activity Example

```json
{
  "name": "LookupFabricLakehouseTable",
  "type": "Lookup",
  "typeProperties": {
    "source": {
      "type": "LakehouseTableSource",
      "query": "SELECT MAX(LastUpdated) as MaxDate FROM SalesData"
    },
    "dataset": {
      "referenceName": "FabricLakehouseTables",
      "type": "DatasetReference"
    }
  }
}
```

## Microsoft Fabric Warehouse Connector

The Fabric Warehouse connector provides T-SQL based data warehousing capabilities within the Fabric ecosystem.

### Supported Activities
- ✅ Copy Activity (source and sink)
- ✅ Lookup Activity
- ✅ Get Metadata Activity
- ✅ Script Activity
- ✅ Stored Procedure Activity

### Linked Service Configuration

**Using Service Principal:**
```json
{
  "name": "FabricWarehouseLinkedService",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "Warehouse",
    "typeProperties": {
      "endpoint": "myworkspace.datawarehouse.fabric.microsoft.com",
      "warehouse": "MyWarehouse",
      "authenticationType": "ServicePrincipal",
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

**Using System-Assigned Managed Identity (Recommended):**
```json
{
  "name": "FabricWarehouseLinkedService_SystemMI",
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

**Using User-Assigned Managed Identity:**
```json
{
  "name": "FabricWarehouseLinkedService_UserMI",
  "type": "Microsoft.DataFactory/factories/linkedservices",
  "properties": {
    "type": "Warehouse",
    "typeProperties": {
      "endpoint": "myworkspace.datawarehouse.fabric.microsoft.com",
      "warehouse": "MyWarehouse",
      "authenticationType": "UserAssignedManagedIdentity",
      "credential": {
        "referenceName": "UserAssignedManagedIdentityCredential",
        "type": "CredentialReference"
      }
    }
  }
}
```

### Copy Activity to Fabric Warehouse

**Bulk Insert Pattern:**
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
      "type": "AzureSqlSource",
      "sqlReaderQuery": "SELECT * FROM dbo.FactSales WHERE OrderDate >= '@{pipeline().parameters.StartDate}'"
    },
    "sink": {
      "type": "WarehouseSink",
      "preCopyScript": "TRUNCATE TABLE staging.FactSales",
      "writeBehavior": "insert",
      "writeBatchSize": 10000,
      "tableOption": "autoCreate",  // Auto-create table if doesn't exist
      "disableMetricsCollection": false
    },
    "enableStaging": true,
    "stagingSettings": {
      "linkedServiceName": {
        "referenceName": "AzureBlobStorage",
        "type": "LinkedServiceReference"
      },
      "path": "staging/fabric-warehouse",
      "enableCompression": true
    },
    "parallelCopies": 4,
    "dataIntegrationUnits": 8
  }
}
```

**Upsert Pattern:**
```json
{
  "sink": {
    "type": "WarehouseSink",
    "writeBehavior": "upsert",
    "upsertSettings": {
      "useTempDB": true,
      "keys": ["customer_id"],
      "interimSchemaName": "staging"
    },
    "writeBatchSize": 10000
  }
}
```

### Stored Procedure Activity

```json
{
  "name": "ExecuteFabricWarehouseStoredProcedure",
  "type": "SqlServerStoredProcedure",
  "linkedServiceName": {
    "referenceName": "FabricWarehouseLinkedService",
    "type": "LinkedServiceReference"
  },
  "typeProperties": {
    "storedProcedureName": "dbo.usp_ProcessSalesData",
    "storedProcedureParameters": {
      "StartDate": {
        "value": "@pipeline().parameters.StartDate",
        "type": "DateTime"
      },
      "EndDate": {
        "value": "@pipeline().parameters.EndDate",
        "type": "DateTime"
      }
    }
  }
}
```

### Script Activity

```json
{
  "name": "ExecuteFabricWarehouseScript",
  "type": "Script",
  "linkedServiceName": {
    "referenceName": "FabricWarehouseLinkedService",
    "type": "LinkedServiceReference"
  },
  "typeProperties": {
    "scripts": [
      {
        "type": "Query",
        "text": "DELETE FROM staging.FactSales WHERE LoadDate < DATEADD(day, -30, GETDATE())"
      },
      {
        "type": "Query",
        "text": "UPDATE dbo.FactSales SET ProcessedFlag = 1 WHERE OrderDate = '@{pipeline().parameters.ProcessDate}'"
      }
    ],
    "scriptBlockExecutionTimeout": "02:00:00"
  }
}
```

## OneLake Integration Patterns

### Pattern 1: Azure Data Lake Gen2 to OneLake via Shortcuts

**Concept:** Use OneLake shortcuts instead of copying data

OneLake shortcuts allow you to reference data in Azure Data Lake Gen2 without physically copying it:

1. In Fabric Lakehouse, create shortcut to ADLS Gen2 container
2. Data appears in OneLake immediately (zero-copy)
3. Use ADF to orchestrate transformations on shortcut data
4. Write results back to OneLake

**Benefits:**
- Zero data duplication
- Real-time data access
- Reduced storage costs
- Single source of truth

**ADF Pipeline Pattern:**
```json
{
  "name": "PL_Process_Shortcut_Data",
  "activities": [
    {
      "name": "TransformShortcutData",
      "type": "ExecuteDataFlow",
      "typeProperties": {
        "dataFlow": {
          "referenceName": "DF_Transform",
          "type": "DataFlowReference"
        },
        "compute": {
          "coreCount": 8,
          "computeType": "General"
        }
      }
    },
    {
      "name": "WriteToCuratedZone",
      "type": "Copy",
      "typeProperties": {
        "source": {
          "type": "ParquetSource"
        },
        "sink": {
          "type": "LakehouseTableSink",
          "tableActionOption": "overwrite"
        }
      }
    }
  ]
}
```

### Pattern 2: Incremental Load to Fabric Lakehouse

```json
{
  "name": "PL_Incremental_Load_To_Fabric",
  "activities": [
    {
      "name": "GetLastWatermark",
      "type": "Lookup",
      "typeProperties": {
        "source": {
          "type": "LakehouseTableSource",
          "query": "SELECT MAX(LoadTimestamp) as LastLoad FROM ControlTable"
        }
      }
    },
    {
      "name": "CopyIncrementalData",
      "type": "Copy",
      "dependsOn": [
        {
          "activity": "GetLastWatermark",
          "dependencyConditions": ["Succeeded"]
        }
      ],
      "typeProperties": {
        "source": {
          "type": "AzureSqlSource",
          "sqlReaderQuery": "SELECT * FROM dbo.Orders WHERE ModifiedDate > '@{activity('GetLastWatermark').output.firstRow.LastLoad}'"
        },
        "sink": {
          "type": "LakehouseTableSink",
          "tableActionOption": "append"
        }
      }
    },
    {
      "name": "UpdateWatermark",
      "type": "Script",
      "dependsOn": [
        {
          "activity": "CopyIncrementalData",
          "dependencyConditions": ["Succeeded"]
        }
      ],
      "linkedServiceName": {
        "referenceName": "FabricLakehouseLinkedService",
        "type": "LinkedServiceReference"
      },
      "typeProperties": {
        "scripts": [
          {
            "type": "Query",
            "text": "INSERT INTO ControlTable VALUES ('@{utcnow()}')"
          }
        ]
      }
    }
  ]
}
```

### Pattern 3: Cross-Platform Pipeline with Invoke Pipeline

**NEW 2025: Invoke Pipeline Activity for Cross-Platform Calls**

```json
{
  "name": "PL_ADF_Orchestrates_Fabric_Pipeline",
  "activities": [
    {
      "name": "PrepareDataInADF",
      "type": "Copy",
      "typeProperties": {
        "source": {
          "type": "AzureSqlSource"
        },
        "sink": {
          "type": "LakehouseTableSink"
        }
      }
    },
    {
      "name": "InvokeFabricPipeline",
      "type": "InvokePipeline",
      "dependsOn": [
        {
          "activity": "PrepareDataInADF",
          "dependencyConditions": ["Succeeded"]
        }
      ],
      "typeProperties": {
        "workspaceId": "12345678-1234-1234-1234-123456789abc",
        "pipelineId": "87654321-4321-4321-4321-cba987654321",
        "waitOnCompletion": true,
        "parameters": {
          "processDate": "@pipeline().parameters.RunDate",
          "environment": "production"
        }
      }
    }
  ]
}
```

## Permission Configuration

### Azure Data Factory Managed Identity Permissions in Fabric

**For Fabric Lakehouse:**
1. Open Fabric workspace
2. Go to Workspace settings → Manage access
3. Add ADF managed identity with **Contributor** role
4. Or assign **Workspace Admin** for full access

**For Fabric Warehouse:**
1. Navigate to Warehouse SQL endpoint
2. Execute SQL to create user:
```sql
CREATE USER [your-adf-name] FROM EXTERNAL PROVIDER;
ALTER ROLE db_datareader ADD MEMBER [your-adf-name];
ALTER ROLE db_datawriter ADD MEMBER [your-adf-name];
```

### Service Principal Permissions

**App Registration Setup:**
1. Register app in Microsoft Entra ID
2. Create client secret (store in Key Vault)
3. Add app to Fabric workspace with Contributor role
4. For Warehouse, create SQL user as shown above

## Best Practices (2025)

### 1. Use Managed Identity
- ✅ System-assigned for single ADF
- ✅ User-assigned for multiple ADFs
- ❌ Avoid service principal keys when possible
- ✅ Store any secrets in Key Vault

### 2. Enable Staging for Large Loads
```json
{
  "enableStaging": true,
  "stagingSettings": {
    "linkedServiceName": {
      "referenceName": "AzureBlobStorage",
      "type": "LinkedServiceReference"
    },
    "path": "staging/fabric-loads",
    "enableCompression": true
  }
}
```

**When to Stage:**
- Data volume > 1 GB
- Complex transformations
- Loading to Fabric Warehouse
- Need better performance

### 3. Leverage OneLake Shortcuts

**Instead of:**
```
ADLS Gen2 → [Copy Activity] → Fabric Lakehouse
```

**Use:**
```
ADLS Gen2 → [OneLake Shortcut] → Direct Access in Fabric
```

**Benefits:**
- No data movement
- Instant availability
- Reduced ADF costs
- Lower storage costs

### 4. Monitor Fabric Capacity Units (CU)

Fabric uses capacity-based pricing. Monitor:
- CU consumption per pipeline run
- Peak usage times
- Throttling events
- Optimize by:
  - Using incremental loads
  - Scheduling during off-peak
  - Right-sizing copy parallelism

### 5. Use Table Option AutoCreate

```json
{
  "sink": {
    "type": "WarehouseSink",
    "tableOption": "autoCreate"  // Creates table if missing
  }
}
```

**Benefits:**
- No manual schema management
- Automatic type mapping
- Faster development
- Works for dynamic schemas

### 6. Implement Error Handling

```json
{
  "activities": [
    {
      "name": "CopyToFabric",
      "type": "Copy",
      "policy": {
        "retry": 2,
        "retryIntervalInSeconds": 30,
        "timeout": "0.12:00:00"
      }
    },
    {
      "name": "LogFailure",
      "type": "WebActivity",
      "dependsOn": [
        {
          "activity": "CopyToFabric",
          "dependencyConditions": ["Failed"]
        }
      ],
      "typeProperties": {
        "url": "@pipeline().parameters.LoggingEndpoint",
        "method": "POST",
        "body": {
          "error": "@activity('CopyToFabric').error.message",
          "pipeline": "@pipeline().Pipeline"
        }
      }
    }
  ]
}
```

## Common Issues and Solutions

### Issue 1: Permission Denied

**Error:** "User does not have permission to access Fabric workspace"

**Solution:**
1. Verify ADF managed identity added to Fabric workspace
2. Check role is **Contributor** or higher
3. For Warehouse, verify SQL user created
4. Allow up to 5 minutes for permission propagation

### Issue 2: Endpoint Not Found

**Error:** "Unable to connect to endpoint"

**Solution:**
1. Verify `workspaceId` and `artifactId` are correct
2. Check Fabric workspace URL in browser
3. Ensure Lakehouse/Warehouse is not paused
4. Verify firewall rules allow ADF IP ranges

### Issue 3: Schema Mismatch

**Error:** "Column types do not match"

**Solution:**
1. Use `tableOption: "autoCreate"` for initial load
2. Explicitly define column mappings in translator
3. Enable staging for complex transformations
4. Use Data Flow for schema evolution

### Issue 4: Performance Degradation

**Symptoms:** Slow copy performance to Fabric

**Solutions:**
1. Enable staging for large datasets
2. Increase `parallelCopies` (try 4-8)
3. Use appropriate `dataIntegrationUnits` (8-32)
4. Check Fabric capacity unit throttling
5. Schedule during off-peak hours

## Resources

- [Fabric Lakehouse Connector](https://learn.microsoft.com/azure/data-factory/connector-microsoft-fabric-lakehouse)
- [Fabric Warehouse Connector](https://learn.microsoft.com/azure/data-factory/connector-microsoft-fabric-warehouse)
- [OneLake Documentation](https://learn.microsoft.com/fabric/onelake/)
- [Fabric Capacity Management](https://learn.microsoft.com/fabric/enterprise/licenses)
- [ADF to Fabric Integration Guide](https://learn.microsoft.com/fabric/data-factory/how-to-ingest-data-into-fabric-from-azure-data-factory)

This comprehensive guide enables seamless integration between Azure Data Factory and Microsoft Fabric's modern data platform capabilities.
