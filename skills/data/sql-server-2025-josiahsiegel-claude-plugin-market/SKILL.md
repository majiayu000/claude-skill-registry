---
name: sql-server-2025
description: SQL Server 2025 and SqlPackage 170.2.70 (October 2025) - Vector databases, AI integration, and latest features
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

# SQL Server 2025 & SqlPackage 170.2.70 Support

## Overview

**SQL Server 2025** is the enterprise AI-ready database with native vector database capabilities, built-in AI model integration, and semantic search from ground to cloud.

**SqlPackage 170.2.70** (October 14, 2025) - Latest production release with full SQL Server 2025 support, data virtualization, and parquet file enhancements.

## SqlPackage 170.x Series (2025 Releases)

### Latest Version: 170.2.70 (October 14, 2025)

Three major 2025 releases:
- **170.2.70** - October 14, 2025 (Current)
- **170.1.61** - July 30, 2025 (Data virtualization)
- **170.0.94** - April 15, 2025 (SQL Server 2025 initial support)

### Key 2025 Features

**Data Virtualization (170.1.61+)**:
- Support for Azure SQL Database data virtualization objects
- Import/export/extract/publish operations for external data sources
- Parquet file support for Azure SQL Database with Azure Blob Storage
- Automatic fallback to BCP for CLR types and LOBs > 1MB

**New Data Types**:
- **VECTOR** - Up to 3,996 dimensions with half-precision (2-byte) floating-point
- **JSON** - Native JSON data type for Azure SQL Database

**New Permissions (170.0+)**:
- `ALTER ANY INFORMATION PROTECTION` - SQL Server 2025 & Azure SQL
- `ALTER ANY EXTERNAL MIRROR` - Azure SQL & SQL database in Fabric
- `CREATE/ALTER ANY EXTERNAL MODEL` - AI/ML model management

**Deployment Options**:
- `/p:IgnorePreDeployScript=True/False` - Skip pre-deployment scripts
- `/p:IgnorePostDeployScript=True/False` - Skip post-deployment scripts

### SqlPackage Commands

```bash
# Publish to SQL Server 2025
sqlpackage /Action:Publish \
  /SourceFile:Database.dacpac \
  /TargetServerName:server2025.database.windows.net \
  /TargetDatabaseName:MyDatabase \
  /TargetDatabaseEdition:Premium \
  /p:TargetPlatform=SqlServer2025  # New target platform

# Extract from SQL Server 2025
sqlpackage /Action:Extract \
  /SourceServerName:server2025.database.windows.net \
  /SourceDatabaseName:MyDatabase \
  /TargetFile:Database.dacpac \
  /p:ExtractAllTableData=False \
  /p:VerifyExtraction=True

# Export with SQL Server 2025 features
sqlpackage /Action:Export \
  /SourceServerName:server2025.database.windows.net \
  /SourceDatabaseName:MyDatabase \
  /TargetFile:Database.bacpac
```

## ScriptDom Version 170.0.64

New ScriptDom version for SQL Server 2025 syntax parsing:

```csharp
// Package: Microsoft.SqlServer.TransactSql.ScriptDom 170.0.64

using Microsoft.SqlServer.TransactSql.ScriptDom;

// Parse SQL Server 2025 syntax
var parser = new TSql170Parser(true);
IList<ParseError> errors;
var fragment = parser.Parse(new StringReader(sql), out errors);

// Supports SQL Server 2025 new T-SQL features
```

## Microsoft.Build.Sql 2.0.0 GA (2025)

**MAJOR MILESTONE:** Microsoft.Build.Sql SDK entered General Availability in 2025!

### Latest Version: 2.0.0 (Production Ready)

**Breaking Change from Preview:**
- SDK is now production-ready and recommended for all new database projects
- No longer in preview status
- Full cross-platform support (Windows/Linux/macOS)
- Requires .NET 8+ (was .NET 6+ in preview)

### SQL Server 2025 Support

**Current Status:** SQL Server 2025 target platform support coming in future Microsoft.Build.Sql release (post-2.0.0).

**Workaround for SDK-Style Projects:**
```xml
<!-- Database.sqlproj (SDK-style with SQL Server 2025 compatibility) -->
<Project Sdk="Microsoft.Build.Sql/2.0.0">
  <PropertyGroup>
    <Name>MyDatabase</Name>
    <!-- Use SQL Server 2022 (160) provider until 2025 provider available -->
    <DSP>Microsoft.Data.Tools.Schema.Sql.Sql160DatabaseSchemaProvider</DSP>
    <TargetFramework>net8.0</TargetFramework>
    <SqlServerVersion>Sql160</SqlServerVersion>

    <!-- SQL Server 2025 features will still work in runtime database -->
    <!-- Only build-time validation uses Sql160 provider -->
  </PropertyGroup>

  <ItemGroup>
    <Folder Include="Tables\" />
    <Folder Include="Views\" />
    <Folder Include="StoredProcedures\" />
  </ItemGroup>
</Project>
```

### Visual Studio 2022 Support

**Requirement:** Visual Studio 2022 version 17.12 or later for SDK-style SQL projects.

**Note:** Side-by-side installation with original SQL projects (legacy SSDT) is NOT supported.

## SQL Server 2025 Release Status

**Current Status**: SQL Server 2025 (17.x) is in **Release Candidate (RC1)** stage as of October 2025. Public preview began May 2025.

**Predicted GA Date**: November 12, 2025 (based on historical release patterns - SQL Server 2019: Nov 4, SQL Server 2022: Nov 16). Expected announcement at Microsoft Ignite conference (November 18-21, 2025).

**Not Yet Production**: SQL Server 2025 is not yet generally available. All features described are available in RC builds for testing purposes only.

## SQL Server 2025 New Features

### Vector Database for AI

**Native Enterprise Vector Store** with built-in security, compliance, and DiskANN indexing technology.

**Key Capabilities:**
- **Up to 3,996 dimensions** per vector (half-precision 2-byte floating-point)
- **DiskANN indexing** - Disk-based approximate nearest neighbor for efficient large-scale vector search
- **Hybrid AI vector search** - Combine vectors with SQL data for semantic + keyword search
- **Built-in security & compliance** - Enterprise-grade data protection

**Vector Embedding & Text Chunking:**
```sql
-- Create table with vector column
CREATE TABLE Documents (
    Id INT PRIMARY KEY IDENTITY,
    Title NVARCHAR(200),
    Content NVARCHAR(MAX),
    -- Half-precision vectors support up to 3,996 dimensions
    ContentVector VECTOR(1536)  -- OpenAI ada-002: 1,536 dims
    -- ContentVector VECTOR(3072)  -- OpenAI text-embedding-3-large: 3,072 dims
    -- ContentVector VECTOR(3996)  -- Maximum: 3,996 dims
);

-- Insert vectors (T-SQL built-in embedding generation)
INSERT INTO Documents (Title, Content, ContentVector)
VALUES (
    'AI Documentation',
    'Azure AI services...',
    CAST('[0.1, 0.2, 0.3, ...]' AS VECTOR(1536))
);

-- Semantic similarity search with DiskANN
DECLARE @QueryVector VECTOR(1536) = CAST('[0.15, 0.25, ...]' AS VECTOR(1536));

SELECT TOP 10
    Id,
    Title,
    Content,
    VECTOR_DISTANCE('cosine', ContentVector, @QueryVector) AS Similarity
FROM Documents
ORDER BY Similarity;

-- Create DiskANN vector index for performance
CREATE INDEX IX_Documents_Vector
ON Documents(ContentVector)
USING VECTOR_INDEX
WITH (
    DISTANCE_METRIC = 'cosine',  -- or 'euclidean', 'dot_product'
    VECTOR_SIZE = 1536
);

-- Hybrid search: Combine vector similarity with traditional filtering
SELECT TOP 10
    Id,
    Title,
    VECTOR_DISTANCE('cosine', ContentVector, @QueryVector) AS Similarity
FROM Documents
WHERE Title LIKE '%Azure%'  -- Traditional keyword filter
ORDER BY Similarity;
```

### AI Model Integration

**Built into T-SQL** - Seamlessly integrate AI services with model definitions directly in the database.

**Supported AI Services:**
- Azure AI Foundry
- Azure OpenAI Service
- OpenAI
- Ollama (local/self-hosted models)
- Custom REST APIs

**Developer Frameworks:**
- LangChain integration
- Semantic Kernel integration
- Entity Framework Core support
- **GraphQL via Data API Builder (DAB)** - Expose SQL Server data through GraphQL endpoints

**External Models (ONNX):**
```sql
-- Create external model from ONNX file
CREATE EXTERNAL MODEL AIModel
FROM 'https://storage.account.blob.core.windows.net/models/model.onnx'
WITH (
    TYPE = 'ONNX',
    INPUT_DATA_FORMAT = 'JSON',
    OUTPUT_DATA_FORMAT = 'JSON'
);

-- Use model for predictions
DECLARE @Input NVARCHAR(MAX) = '{"text": "Hello world"}';
SELECT PREDICT(MODEL = AIModel, DATA = @Input) AS Prediction;

-- Grant model permissions (new SQL Server 2025 permission)
GRANT CREATE ANY EXTERNAL MODEL TO [ModelAdmin];
GRANT ALTER ANY EXTERNAL MODEL TO [ModelAdmin];
GRANT EXECUTE ON EXTERNAL MODEL::AIModel TO [AppUser];
```

**AI Service Integration:**
```sql
-- Example: Azure OpenAI integration
-- Model definitions built directly into T-SQL
-- Access through REST APIs with built-in authentication
```

### Optimized Locking (Performance Enhancement)

**Key Innovation**: Dramatically reduces lock memory consumption and minimizes blocking for concurrent transactions.

**Two Primary Components**:

1. **Transaction ID (TID) Locking**:
   - Each row labeled with last TID (Transaction ID) that modified it
   - Single lock on TID instead of many row locks
   - Locks released as soon as row is updated
   - Only one TID lock held until transaction ends
   - **Example**: Updating 1,000 rows requires 1,000 X row locks, but each is released immediately, and only one TID lock is held until commit

2. **Lock After Qualification (LAQ)**:
   - Evaluates query predicates using latest committed version WITHOUT acquiring lock
   - Requires READ COMMITTED SNAPSHOT ISOLATION (RCSI)
   - Predicates checked optimistically on committed data
   - X row lock taken only if predicate satisfied
   - Lock released immediately after row update

**Benefits**:
- Reduced lock memory usage
- Increased concurrency and scale
- Minimized lock escalation
- Enhanced application uptime
- Better performance for high-concurrency workloads

**Enabling Optimized Locking**:
```sql
-- Enable RCSI (required for LAQ)
ALTER DATABASE MyDatabase
SET READ_COMMITTED_SNAPSHOT ON;

-- Optimized locking is automatically enabled at database level
-- No additional configuration needed for SQL Server 2025

-- Verify optimized locking status
SELECT name, is_read_committed_snapshot_on
FROM sys.databases
WHERE name = 'MyDatabase';

-- Monitor optimized locking performance
SELECT *
FROM sys.dm_tran_locks
WHERE request_session_id = @@SPID;
```

### Microsoft Fabric Mirroring (Zero-ETL Analytics)

**Integration**: Near real-time replication of SQL Server databases to Microsoft Fabric OneLake for analytics.

**Key Capabilities**:
- **Zero-ETL Experience**: No complex ETL pipelines required
- **SQL Server 2025-Specific**: Uses new change feed technology (vs CDC in SQL Server 2016-2022)
- **Azure Arc Required**: SQL Server 2025 requires Azure Arc-enabled server for Fabric communication
- **Real-Time Analytics**: Offload analytic workloads to Fabric without impacting production

**Supported Scenarios**:
- SQL Server 2025 on-premises (Windows)
- NOT supported: Azure VM or Linux instances (yet)

**How It Works**:
```sql
-- SQL Server 2025 uses change feed (automatic)
-- Azure Arc agent handles replication to Fabric OneLake

-- Traditional SQL Server 2016-2022 approach (CDC):
-- EXEC sys.sp_cdc_enable_db;
-- EXEC sys.sp_cdc_enable_table ...

-- SQL Server 2025: Change feed is built-in, no CDC setup needed
```

**Benefits**:
- Free Fabric compute for replication
- Free OneLake storage (based on capacity size)
- Near real-time data availability
- BI and analytics without production load
- Integration with Power BI, Synapse, Azure ML

**Configuration**:
1. Enable Azure Arc on SQL Server 2025 instance
2. Configure Fabric workspace and OneLake
3. Enable mirroring in Fabric portal
4. Select database and tables to mirror
5. Data automatically replicated with change feed

**Monitoring**:
```sql
-- Monitor replication lag
SELECT
    database_name,
    table_name,
    last_sync_time,
    rows_replicated,
    replication_lag_seconds
FROM sys.dm_fabric_replication_status;
```

### Native JSON Support Enhancements

**New JSON Data Type**: Native JSON data type for Azure SQL Database (coming to SQL Server 2025).

```sql
-- New JSON data type
CREATE TABLE Products (
    Id INT PRIMARY KEY,
    Name NVARCHAR(100),
    Metadata JSON  -- Native JSON type
);

-- JSON functions enhanced
INSERT INTO Products (Id, Name, Metadata)
VALUES (1, 'Laptop', JSON('{"brand": "Dell", "ram": 16, "ssd": 512}'));

-- Query JSON with improved performance
SELECT
    Id,
    Name,
    JSON_VALUE(Metadata, '$.brand') AS Brand,
    JSON_VALUE(Metadata, '$.ram') AS RAM
FROM Products;
```

### Regular Expression (RegEx) Support

**T-SQL RegEx Functions**: Validate, search, and manipulate strings with regular expressions.

```sql
-- RegEx matching
SELECT REGEXP_LIKE('test@example.com', '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$') AS IsValidEmail;

-- RegEx replace
SELECT REGEXP_REPLACE('Phone: 555-1234', '\d+', 'XXX') AS MaskedPhone;

-- RegEx extract
SELECT REGEXP_SUBSTR('Order #12345', '\d+') AS OrderNumber;
```

### REST API Integration

**Built-in REST Capabilities**: Call external REST APIs directly from T-SQL.

```sql
-- Call REST API from T-SQL
DECLARE @Response NVARCHAR(MAX);

EXEC sp_invoke_external_rest_endpoint
    @url = 'https://api.example.com/data',
    @method = 'GET',
    @headers = '{"Authorization": "Bearer token123"}',
    @response = @Response OUTPUT;

SELECT @Response AS APIResponse;

-- Enrich database data with external APIs
UPDATE Customers
SET EnrichedData = (
    SELECT JSON_VALUE(response, '$.data')
    FROM OPENROWSET(REST, 'https://api.example.com/customer/' + CustomerId)
)
WHERE CustomerId = 12345;
```

### Optional Parameter Plan Optimization (OPPO)

**Performance Enhancement**: SQL Server 2025 introduces OPPO to enable optimal execution plan selection based on customer-provided runtime parameter values.

**Key Benefits:**
- Solves parameter sniffing issues
- Optimizes plans for specific runtime parameters
- Improves query performance with parameter-sensitive workloads
- Reduces need for query hints or plan guides

**Enabling OPPO:**
```sql
-- Enable at database level
ALTER DATABASE MyDatabase
SET PARAMETER_SENSITIVE_PLAN_OPTIMIZATION = ON;

-- Check status
SELECT name, is_parameter_sensitive_plan_optimization_on
FROM sys.databases
WHERE name = 'MyDatabase';

-- Monitor OPPO usage
SELECT
    query_plan_hash,
    parameter_values,
    execution_count,
    avg_duration_ms
FROM sys.dm_exec_query_stats
WHERE is_parameter_sensitive = 1;
```

### Microsoft Entra Managed Identities

**Security Enhancement**: SQL Server 2025 adds support for Microsoft Entra managed identities for improved credential management.

**Key Benefits:**
- Eliminates hardcoded credentials
- Reduces security vulnerabilities
- Provides compliance and auditing capabilities
- Simplifies credential rotation

**Configuration:**
```sql
-- Create login with managed identity
CREATE LOGIN [managed-identity-name] FROM EXTERNAL PROVIDER;

-- Grant permissions
CREATE USER [managed-identity-name] FOR LOGIN [managed-identity-name];
GRANT CONTROL ON DATABASE::MyDatabase TO [managed-identity-name];

-- Use in connection strings
-- Connection string: Server=myserver;Database=mydb;Authentication=Active Directory Managed Identity;
```

### Enhanced Information Protection

Sensitivity classification and encryption:

```sql
-- Classify sensitive columns
ADD SENSITIVITY CLASSIFICATION TO
    Customers.Email,
    Customers.CreditCard
WITH (
    LABEL = 'Confidential',
    INFORMATION_TYPE = 'Financial'
);

-- Query classification
SELECT
    schema_name(o.schema_id) AS SchemaName,
    o.name AS TableName,
    c.name AS ColumnName,
    s.label AS SensitivityLabel,
    s.information_type AS InformationType
FROM sys.sensitivity_classifications s
INNER JOIN sys.objects o ON s.major_id = o.object_id
INNER JOIN sys.columns c ON s.major_id = c.object_id AND s.minor_id = c.column_id;
```

## Deployment to SQL Server 2025

### Using SqlPackage

```bash
# Publish with 2025 features
sqlpackage /Action:Publish \
  /SourceFile:Database.dacpac \
  /TargetConnectionString:"Server=tcp:server2025.database.windows.net;Database=MyDb;Authentication=ActiveDirectoryManagedIdentity;" \
  /p:BlockOnPossibleDataLoss=True \
  /p:IncludeCompositeObjects=True \
  /p:DropObjectsNotInSource=False \
  /p:DoNotDropObjectTypes=Users;RoleMembership \
  /p:GenerateSmartDefaults=True \
  /DiagnosticsFile:deploy.log
```

### Using MSBuild

```xml
<!-- Database.publish.xml -->
<Project>
  <PropertyGroup>
    <TargetConnectionString>Server=tcp:server2025.database.windows.net;Database=MyDb;Authentication=ActiveDirectoryManagedIdentity;</TargetConnectionString>
    <BlockOnPossibleDataLoss>True</BlockOnPossibleDataLoss>
    <TargetDatabaseName>MyDatabase</TargetDatabaseName>
    <ProfileVersionNumber>1</ProfileVersionNumber>
  </PropertyGroup>

  <ItemGroup>
    <SqlCmdVariable Include="Environment">
      <Value>Production</Value>
    </SqlCmdVariable>
  </ItemGroup>
</Project>
```

```bash
# Deploy using MSBuild
msbuild Database.sqlproj \
  /t:Publish \
  /p:PublishProfile=Database.publish.xml \
  /p:TargetPlatform=SqlServer2025
```

## CI/CD Best Practices 2025

### Key Principles

**State-Based Deployment (Recommended):**
- Source code represents current database state
- All objects (procedures, tables, triggers, views) in separate .sql files
- SqlPackage generates incremental scripts automatically
- Preferred over migration-based approaches

**Testing & Quality:**
- **tSQLt** - Unit testing for SQL Server stored procedures and functions
- Tests produce machine-readable results
- Abort pipeline on test failure with immediate notifications
- Never continue deployment if tests fail

**Security:**
- **Windows Authentication preferred** for CI/CD (avoid plain text passwords)
- Never commit credentials to source control
- Use Azure Key Vault or GitHub Secrets for connection strings

**Version Control:**
- All database objects in source control
- Test scripts versioned and executed in Build step
- Require comments on check-ins
- Configure custom check-in policies

### GitHub Actions (2025 Pattern)

```yaml
name: Deploy to SQL Server 2025

on:
  push:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - name: Setup .NET 8
      uses: actions/setup-dotnet@v4
      with:
        dotnet-version: '8.0.x'

    - name: Install SqlPackage 170.2.70
      run: dotnet tool install -g Microsoft.SqlPackage --version 170.2.70

    - name: Build DACPAC
      run: dotnet build Database.sqlproj -c Release

    - name: Run tSQLt Unit Tests
      run: |
        # Run unit tests and capture results
        # Abort if tests fail
        echo "Running tSQLt unit tests..."
        # Add your tSQLt test execution here

    - name: Generate Deployment Report
      run: |
        sqlpackage /Action:DeployReport \
          /SourceFile:bin/Release/Database.dacpac \
          /TargetConnectionString:"${{ secrets.SQL_CONNECTION_STRING }}" \
          /OutputPath:deploy-report.xml \
          /p:BlockOnPossibleDataLoss=True

    - name: Publish to SQL Server 2025
      run: |
        sqlpackage /Action:Publish \
          /SourceFile:bin/Release/Database.dacpac \
          /TargetConnectionString:"${{ secrets.SQL_CONNECTION_STRING }}" \
          /p:TargetPlatform=SqlServer2025 \
          /p:BlockOnPossibleDataLoss=True \
          /DiagnosticsFile:publish.log \
          /DiagnosticsLevel:Verbose

    - name: Upload Artifacts
      if: always()
      uses: actions/upload-artifact@v4
      with:
        name: deployment-logs
        path: |
          publish.log
          deploy-report.xml
```

### Azure DevOps

```yaml
trigger:
- main

pool:
  vmImage: 'windows-2022'

steps:
- task: MSBuild@1
  displayName: 'Build Database Project'
  inputs:
    solution: 'Database.sqlproj'
    configuration: 'Release'

- task: SqlAzureDacpacDeployment@1
  displayName: 'Deploy to SQL Server 2025'
  inputs:
    azureSubscription: 'Azure Subscription'
    authenticationType: 'servicePrincipal'
    serverName: 'server2025.database.windows.net'
    databaseName: 'MyDatabase'
    deployType: 'DacpacTask'
    deploymentAction: 'Publish'
    dacpacFile: '$(Build.SourcesDirectory)/bin/Release/Database.dacpac'
    additionalArguments: '/p:TargetPlatform=SqlServer2025'
```

## New SqlPackage Diagnostic Features

```bash
# Enable detailed diagnostics
sqlpackage /Action:Publish \
  /SourceFile:Database.dacpac \
  /TargetServerName:server2025.database.windows.net \
  /TargetDatabaseName:MyDatabase \
  /DiagnosticsLevel:Verbose \
  /DiagnosticPackageFile:diagnostics.zip

# Creates diagnostics.zip containing:
# - Deployment logs
# - Performance metrics
# - Error details
# - Schema comparison results
```

## Microsoft Fabric Data Warehouse Support

**New in SqlPackage 162.5+:** Full support for SQL database in Microsoft Fabric.

**Fabric Deployment:**
```bash
# Deploy to Fabric Warehouse
sqlpackage /Action:Publish \
  /SourceFile:Warehouse.dacpac \
  /TargetConnectionString:"Server=tcp:myworkspace.datawarehouse.fabric.microsoft.com;Database=mywarehouse;Authentication=ActiveDirectoryInteractive;" \
  /p:DatabaseEdition=Fabric \
  /p:DatabaseServiceObjective=SqlDbFabricDatabaseSchemaProvider

# Extract from Fabric
sqlpackage /Action:Extract \
  /SourceConnectionString:"Server=tcp:myworkspace.datawarehouse.fabric.microsoft.com;Database=mywarehouse;Authentication=ActiveDirectoryInteractive;" \
  /TargetFile:Fabric.dacpac

# New permission: ALTER ANY EXTERNAL MIRROR (Fabric-specific)
GRANT ALTER ANY EXTERNAL MIRROR TO [FabricAdmin];
```

## Best Practices for SQL Server 2025

1. **Use Target Platform Specification:**
```xml
<PropertyGroup>
  <TargetPlatform>SqlServer2025</TargetPlatform>
</PropertyGroup>
```

2. **Test Vector Operations:**
```sql
-- Verify vector support
SELECT SERVERPROPERTY('IsVectorSupported') AS VectorSupport;
```

3. **Monitor AI Model Performance:**
```sql
-- Track model execution
SELECT
    model_name,
    AVG(execution_time_ms) AS AvgExecutionTime,
    COUNT(*) AS ExecutionCount
FROM sys.dm_exec_external_model_stats
GROUP BY model_name;
```

4. **Implement Sensitivity Classification:**
```sql
-- Classify all PII columns
ADD SENSITIVITY CLASSIFICATION TO dbo.Customers.Email
WITH (LABEL = 'Confidential - GDPR', INFORMATION_TYPE = 'Email');
```

## Resources

- [SQL Server 2025 Preview](https://aka.ms/sqlserver2025)
- [SqlPackage Documentation](https://learn.microsoft.com/sql/tools/sqlpackage/)
- [SDK-Style Projects](https://learn.microsoft.com/sql/tools/sql-database-projects/concepts/sdk-style-projects)
- [Vector Database](https://learn.microsoft.com/sql/relational-databases/vectors/)
