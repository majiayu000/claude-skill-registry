---
name: microsoft-fabric
description: Expert guidance for Microsoft Fabric development using the Fabric MCP Server. Access Fabric public APIs, OpenAPI specs, item schemas, best practices, and OneLake file management. Use when working with Fabric workloads, Lakehouses, pipelines, semantic models, notebooks, or building Fabric integrations.
---

# Microsoft Fabric Development Expert

Expert guidance for Microsoft Fabric using the Fabric MCP Server. Access comprehensive API specifications, item definitions, best practices, and OneLake management capabilities - all running locally without connecting to live environments.

## Core Capabilities

1. **API Discovery** - Enumerate and access Fabric workload APIs
2. **Schema Access** - Get JSON schemas for item definitions
3. **Best Practices** - Access guidance and examples
4. **OneLake Management** - File and item operations
5. **Local-First** - All tools run locally for reference and development

## Quick Reference - MCP Tools

### API Access Tools

| Tool | Purpose |
|------|---------|
| `publicapis_list` | List all Fabric workload types |
| `publicapis_get` | Get OpenAPI spec for workload |
| `publicapis_platform_get` | Get platform API specs |
| `publicapis_bestpractices_get` | Get best practices documentation |
| `publicapis_bestpractices_examples_get` | Get API request/response examples |
| `publicapis_bestpractices_itemdefinition_get` | Get item schema definitions |

### OneLake Tools

| Tool | Purpose |
|------|---------|
| `onelake download file` | Download files from OneLake |
| `onelake upload file` | Upload files to OneLake |
| `onelake file list` | List files in OneLake |
| `onelake file delete` | Delete files from OneLake |
| `onelake directory create` | Create directories |
| `onelake directory delete` | Delete directories |
| `onelake item list` | List workspace items |
| `onelake item list-data` | List items via DFS endpoint |
| `onelake item create` | Create new Fabric items |

---

## Instructions

### API Discovery Tools

#### publicapis_list

List all Microsoft Fabric workload types that have public API specifications.

**Purpose:** Discover available Fabric workloads and their API coverage.

**When to use:**
- Starting Fabric development
- Exploring available workloads
- Finding workload-specific APIs

**Parameters:** None

**Returns:** List of all Fabric workload types with public APIs.

**Workload Types Include:**
- Lakehouses
- Data Pipelines
- Semantic Models (Power BI)
- Notebooks
- Spark Job Definitions
- Warehouses
- KQL Databases
- Eventhouse
- Real-Time Intelligence
- ML Models
- ML Experiments
- And more...

**Example Usage:**
```
Use publicapis_list to see all available workloads
```

---

#### publicapis_get

Retrieve complete OpenAPI/Swagger specification for a specific workload.

**Purpose:** Get full API documentation including endpoints, parameters, schemas, and examples.

**When to use:**
- Implementing workload-specific operations
- Understanding API structure
- Finding available endpoints

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workload | string | Yes | Workload type name |

**Returns:** Complete OpenAPI specification in JSON format.

**Workload Examples:**
- `DataPipeline`
- `Lakehouse`
- `SemanticModel`
- `Notebook`
- `SparkJobDefinition`
- `Warehouse`
- `KQLDatabase`

**Example Usage:**
```
Get API spec for Data Pipelines:
  workload: "DataPipeline"

Get API spec for Lakehouses:
  workload: "Lakehouse"
```

---

#### publicapis_platform_get

Access OpenAPI specifications for Microsoft Fabric platform-level APIs.

**Purpose:** Get platform APIs that work across all workloads (workspaces, items, permissions, etc.).

**When to use:**
- Managing workspaces
- Handling permissions
- Working with cross-workload operations
- Implementing generic Fabric operations

**Parameters:** None

**Returns:** Platform-level OpenAPI specification.

**Platform APIs Include:**
- Workspace management
- Item management (generic)
- Permission management
- Capacity operations
- Deployment pipelines
- Git integration

**Example Usage:**
```
Use publicapis_platform_get to access platform APIs
```

---

#### publicapis_bestpractices_get

Get embedded best practice documentation for Fabric development.

**Purpose:** Access guidance on pagination, error handling, authentication, and recommended patterns.

**When to use:**
- Implementing reliable API calls
- Handling errors and retries
- Understanding rate limits
- Following Microsoft recommendations

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| topic | string | Yes | Best practice topic |

**Topics Include:**
- Pagination patterns
- Error handling
- Retry/backoff strategies
- Authentication
- Rate limiting
- API versioning
- Request/response patterns

**Example Usage:**
```
Get pagination best practices:
  topic: "pagination"

Get error handling guidance:
  topic: "error_handling"

Get retry strategies:
  topic: "retry_backoff"
```

---

#### publicapis_bestpractices_examples_get

Retrieve example API request/response files for workloads.

**Purpose:** Get concrete examples of API calls and their responses.

**When to use:**
- Learning API request format
- Understanding response structure
- Implementing specific operations
- Debugging API calls

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workload | string | Yes | Workload type |
| example_type | string | No | Type of example |

**Example Types:**
- `create` - Creation requests
- `update` - Update operations
- `get` - Retrieval operations
- `list` - Listing operations
- `delete` - Deletion operations

**Example Usage:**
```
Get Lakehouse creation example:
  workload: "Lakehouse"
  example_type: "create"

Get Data Pipeline examples:
  workload: "DataPipeline"
```

---

#### publicapis_bestpractices_itemdefinition_get

Access JSON schema definitions for items within workload APIs.

**Purpose:** Get the complete schema for specific Fabric item types including required properties, data types, and constraints.

**When to use:**
- Creating new items
- Validating item definitions
- Understanding item structure
- Implementing item configuration

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workload | string | Yes | Workload type |
| item_type | string | Yes | Specific item type |

**Common Item Types:**
- Lakehouse: `lakehouse`
- Pipeline: `datapipeline`, `activity`
- Semantic Model: `semanticmodel`, `dataset`
- Notebook: `notebook`
- Warehouse: `warehouse`
- KQL Database: `kqldatabase`

**Returns:** JSON schema with properties, required fields, types, and constraints.

**Example Usage:**
```
Get Lakehouse schema:
  workload: "Lakehouse"
  item_type: "lakehouse"

Get Pipeline activity schema:
  workload: "DataPipeline"
  item_type: "activity"
```

---

### OneLake Management Tools

#### onelake download file

Download files from OneLake to local disk.

**Purpose:** Retrieve data files from OneLake storage.

**When to use:**
- Accessing data for local processing
- Backing up files
- Downloading analysis results
- Retrieving artifacts

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |
| item | string | Yes | Item ID or name.type format |
| path | string | Yes | File path in OneLake |
| local_path | string | Yes | Local destination path |

**Item Format:** Can be:
- GUID: `550e8400-e29b-41d4-a716-446655440000`
- Name.Type: `MyLakehouse.Lakehouse`

**Example Usage:**
```
Download file from Lakehouse:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  path: "/Files/data.csv"
  local_path: "./downloaded_data.csv"
```

---

#### onelake upload file

Upload local files to OneLake storage.

**Purpose:** Transfer files from local disk to OneLake.

**When to use:**
- Uploading source data
- Deploying artifacts
- Saving processing results
- Backing up to cloud

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |
| item | string | Yes | Item ID or name.type format |
| local_path | string | Yes | Local file path |
| onelake_path | string | Yes | Destination path in OneLake |

**Example Usage:**
```
Upload data file:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  local_path: "./source_data.csv"
  onelake_path: "/Files/uploaded_data.csv"
```

---

#### onelake file list

List files in OneLake via hierarchical endpoint.

**Purpose:** Browse file structure in OneLake items.

**When to use:**
- Exploring data structure
- Finding files
- Verifying uploads
- Building file lists

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |
| item | string | Yes | Item ID or name.type format |
| path | string | No | Path to list (default: root) |

**Example Usage:**
```
List all files in Lakehouse:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"

List specific directory:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  path: "/Files/data"
```

---

#### onelake file delete

Delete individual files from OneLake storage.

**Purpose:** Remove files from OneLake.

**When to use:**
- Cleaning up temporary files
- Removing old data
- Managing storage space
- Implementing data retention

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |
| item | string | Yes | Item ID or name.type format |
| path | string | Yes | File path to delete |

**Example Usage:**
```
Delete specific file:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  path: "/Files/temp_data.csv"
```

---

#### onelake directory create

Create directories in OneLake via DFS endpoint.

**Purpose:** Provision directory structure in OneLake.

**When to use:**
- Organizing data storage
- Creating folder structures
- Preparing for uploads
- Setting up data layouts

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |
| item | string | Yes | Item ID or name.type format |
| path | string | Yes | Directory path to create |

**Example Usage:**
```
Create data directory:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  path: "/Files/raw_data"

Create nested directories:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  path: "/Files/processed/2024/01"
```

---

#### onelake directory delete

Remove directories from OneLake (with recursive option).

**Purpose:** Delete directory structures from OneLake.

**When to use:**
- Cleaning up directories
- Removing old data structures
- Resetting storage layout
- Managing workspace organization

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |
| item | string | Yes | Item ID or name.type format |
| path | string | Yes | Directory path to delete |
| recursive | boolean | No | Delete contents recursively |

**Example Usage:**
```
Delete empty directory:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  path: "/Files/temp"

Delete directory with contents:
  workspace: "MyWorkspace"
  item: "DataLakehouse.Lakehouse"
  path: "/Files/old_data"
  recursive: true
```

---

#### onelake item list

List workspace items with metadata.

**Purpose:** Display all Fabric items in a workspace.

**When to use:**
- Discovering workspace contents
- Finding item GUIDs
- Checking item types
- Auditing workspace resources

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |

**Returns:** List of items with:
- Item ID (GUID)
- Display name
- Item type
- Description
- Created/modified dates

**Example Usage:**
```
List all workspace items:
  workspace: "MyWorkspace"

List items by GUID:
  workspace: "550e8400-e29b-41d4-a716-446655440000"
```

---

#### onelake item list-data

List Fabric items via DFS endpoint.

**Purpose:** Enumerate items using OneLake DFS API.

**When to use:**
- Accessing items via DFS protocol
- Integrating with DFS-based tools
- Alternative item listing method
- Low-level OneLake access

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |

**Example Usage:**
```
List items via DFS:
  workspace: "MyWorkspace"
```

---

#### onelake item create

Create new Fabric items (Lakehouses, notebooks, pipelines, etc.).

**Purpose:** Provision new items in Fabric workspaces.

**When to use:**
- Creating Lakehouses
- Provisioning notebooks
- Setting up pipelines
- Deploying warehouses
- Initializing any Fabric item type

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| workspace | string | Yes | Workspace ID or name |
| item_type | string | Yes | Type of item to create |
| display_name | string | Yes | Item display name |
| description | string | No | Item description |
| definition | object | No | Item-specific configuration |

**Item Types:**
- `Lakehouse`
- `DataPipeline`
- `Notebook`
- `Warehouse`
- `KQLDatabase`
- `SemanticModel`
- `SparkJobDefinition`
- And more...

**Example Usage:**
```
Create Lakehouse:
  workspace: "MyWorkspace"
  item_type: "Lakehouse"
  display_name: "AnalyticsLakehouse"
  description: "Lakehouse for analytics data"

Create Notebook:
  workspace: "MyWorkspace"
  item_type: "Notebook"
  display_name: "DataProcessing"
  definition: { "language": "python" }
```

---

## Development Workflows

### Workflow 1: Discover and Use Fabric APIs

```
1. publicapis_list
   - See all available workloads

2. publicapis_get
   workload: "DataPipeline"
   - Get complete API specification

3. publicapis_bestpractices_itemdefinition_get
   workload: "DataPipeline"
   item_type: "datapipeline"
   - Get schema for pipeline definition

4. publicapis_bestpractices_examples_get
   workload: "DataPipeline"
   example_type: "create"
   - See example API calls

5. Implement based on specs and examples
```

### Workflow 2: Create and Configure Lakehouse

```
1. onelake item create
   workspace: "MyWorkspace"
   item_type: "Lakehouse"
   display_name: "DataLakehouse"

2. onelake directory create
   item: "DataLakehouse.Lakehouse"
   path: "/Files/raw"

3. onelake directory create
   item: "DataLakehouse.Lakehouse"
   path: "/Files/processed"

4. onelake upload file
   item: "DataLakehouse.Lakehouse"
   local_path: "./data.csv"
   onelake_path: "/Files/raw/data.csv"

5. onelake file list
   item: "DataLakehouse.Lakehouse"
   - Verify upload
```

### Workflow 3: Build Data Pipeline

```
1. publicapis_get
   workload: "DataPipeline"

2. publicapis_bestpractices_itemdefinition_get
   workload: "DataPipeline"
   item_type: "activity"

3. onelake item create
   item_type: "DataPipeline"
   display_name: "ETL Pipeline"
   definition: { /* pipeline config */ }

4. publicapis_bestpractices_get
   topic: "error_handling"
```

---

## Best Practices

### API Usage
1. **Start with publicapis_list** - Discover available workloads
2. **Get full spec** - Use publicapis_get for complete API documentation
3. **Use schemas** - Validate against item definitions
4. **Follow examples** - Start from provided examples
5. **Handle errors** - Implement retry logic from best practices

### OneLake Management
1. **Use friendly names** - Prefer `name.type` format over GUIDs
2. **Check before operations** - List files/items first
3. **Organize structure** - Create logical directory hierarchies
4. **Cleanup regularly** - Delete unnecessary files
5. **Verify uploads** - List files after upload operations

### Item Creation
1. **Get schema first** - Use itemdefinition_get before creating
2. **Validate configuration** - Check required properties
3. **Start simple** - Begin with minimal configuration
4. **Test incrementally** - Create, verify, then enhance
5. **Use examples** - Adapt from examples_get results

---

## Fabric Workload Reference

### Lakehouse
- **Purpose:** Delta Lake storage with SQL analytics
- **Use publicapis_get:** `Lakehouse`
- **Item type:** `Lakehouse`
- **OneLake structure:** `/Files`, `/Tables`

### Data Pipeline
- **Purpose:** Data integration and ETL
- **Use publicapis_get:** `DataPipeline`
- **Item type:** `DataPipeline`
- **Components:** Activities, datasets, linked services

### Semantic Model
- **Purpose:** Power BI datasets
- **Use publicapis_get:** `SemanticModel`
- **Item type:** `SemanticModel`
- **Components:** Tables, measures, relationships

### Notebook
- **Purpose:** Interactive code notebooks
- **Use publicapis_get:** `Notebook`
- **Item type:** `Notebook`
- **Languages:** Python, Scala, R, SQL

### Warehouse
- **Purpose:** SQL data warehouse
- **Use publicapis_get:** `Warehouse`
- **Item type:** `Warehouse`
- **Features:** T-SQL, tables, views, procedures

### KQL Database
- **Purpose:** Real-time analytics with Kusto
- **Use publicapis_get:** `KQLDatabase`
- **Item type:** `KQLDatabase`
- **Query language:** KQL (Kusto Query Language)

---

## When to Use This Skill

- Developing Microsoft Fabric integrations
- Building Fabric REST API clients
- Creating Lakehouses and data pipelines
- Managing OneLake storage programmatically
- Understanding Fabric item schemas
- Implementing Fabric best practices
- Automating Fabric workspace operations
- Learning Fabric API capabilities

## Keywords

microsoft fabric, onelake, lakehouse, data pipeline, semantic model, notebook, warehouse, kql database, fabric api, openapi, rest api, item definition, schema, best practices, workspace management, file operations, fabric workload
