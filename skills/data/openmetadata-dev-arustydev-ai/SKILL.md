---
name: openmetadata-dev
description: Use OpenMetadata SDK and APIs to build integrations, connectors, and automations. Use when querying metadata, creating custom properties, building ingestion pipelines, automating governance workflows, or integrating OpenMetadata with other systems.
---

# OpenMetadata Development

Guide for using OpenMetadata Python/Java SDKs and REST APIs to build integrations, connectors, and automations.

## When to Use This Skill

- Querying and updating metadata via SDK/API
- Building custom ingestion connectors
- Creating and managing custom properties
- Automating governance workflows
- Integrating OpenMetadata with external systems
- Managing lineage programmatically

## This Skill Does NOT Cover

- Implementing new language SDKs (see `openmetadata-sdk-dev`)
- Administering OpenMetadata (bots, users, security) (see `openmetadata-ops`)
- Deploying or operating OpenMetadata infrastructure

---

## SDK Setup

### Python SDK Installation

```bash
pip install openmetadata-ingestion
```

### Initialize Client

```python
from metadata.ingestion.ometa.ometa_api import OpenMetadata
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    OpenMetadataConnection,
    AuthProvider,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)

# Configure connection
server_config = OpenMetadataConnection(
    hostPort="http://localhost:8585/api",
    authProvider=AuthProvider.openmetadata,
    securityConfig=OpenMetadataJWTClientConfig(
        jwtToken="<your-jwt-token>",
    ),
)

# Create client
metadata = OpenMetadata(server_config)

# Verify connection
assert metadata.health_check()
```

### Java SDK Setup

```xml
<dependency>
    <groupId>org.open-metadata</groupId>
    <artifactId>openmetadata-java-client</artifactId>
    <version>1.3.0</version>
</dependency>
```

```java
OpenMetadataConnection server = new OpenMetadataConnection();
server.setHostPort("http://localhost:8585/api");
server.setAuthProvider(AuthProvider.OPENMETADATA);
server.setSecurityConfig(new OpenMetadataJWTClientConfig().withJwtToken("<token>"));

OpenMetadata client = new OpenMetadata(server);
```

---

## Querying Metadata

### Get Entity by Name

```python
from metadata.generated.schema.entity.data.table import Table

# Get table by fully qualified name
table = metadata.get_by_name(
    entity=Table,
    fqn="prod.sales.public.orders",
    fields=["columns", "owner", "tags"],  # Optional: include related data
)

if table:
    print(f"Table: {table.name}")
    print(f"Columns: {[col.name for col in table.columns]}")
    print(f"Owner: {table.owner.name if table.owner else 'None'}")
```

### Get Entity by ID

```python
from uuid import UUID

table = metadata.get_by_id(
    entity=Table,
    entity_id=UUID("12345678-1234-1234-1234-123456789abc"),
    fields=["columns"],
)
```

### List Entities with Pagination

```python
from metadata.generated.schema.entity.data.table import Table

# List tables with pagination
tables = metadata.list_entities(
    entity=Table,
    limit=100,
    fields=["owner", "database"],
)

for table in tables.entities:
    print(f"{table.fullyQualifiedName}")

# Get next page
if tables.paging.after:
    next_page = metadata.list_entities(
        entity=Table,
        limit=100,
        after=tables.paging.after,
    )
```

### Search Entities

```python
# Search using Elasticsearch query
results = metadata.es_search_from_fqn(
    entity_type=Table,
    fqn_search_string="*orders*",
    size=50,
)

for hit in results:
    print(hit["_source"]["fullyQualifiedName"])
```

---

## Creating and Updating Entities

### Create Table

```python
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.generated.schema.entity.data.table import Column, DataType

create_request = CreateTableRequest(
    name="new_orders",
    databaseSchema="prod.sales.public",
    columns=[
        Column(name="id", dataType=DataType.BIGINT),
        Column(name="customer_id", dataType=DataType.BIGINT),
        Column(name="total", dataType=DataType.DECIMAL),
        Column(name="created_at", dataType=DataType.TIMESTAMP),
    ],
    description="Order transactions",
)

table = metadata.create_or_update(create_request)
print(f"Created table: {table.fullyQualifiedName}")
```

### Update Entity Description

```python
from metadata.generated.schema.type.tagLabel import TagLabel

# Update table description
metadata.patch_description(
    entity=Table,
    source=table,
    description="Updated description for orders table",
)
```

### Add Tags to Entity

```python
from metadata.generated.schema.type.tagLabel import (
    TagLabel,
    TagSource,
    LabelType,
    State,
)

tag = TagLabel(
    tagFQN="PII.Sensitive",
    source=TagSource.Classification,
    labelType=LabelType.Manual,
    state=State.Confirmed,
)

metadata.patch_tag(
    entity=Table,
    source=table,
    tag_label=tag,
)
```

### Set Owner

```python
from metadata.generated.schema.type.entityReference import EntityReference

# Get user reference
user = metadata.get_by_name(entity=User, fqn="john.doe")

# Set owner
metadata.patch_owner(
    entity=Table,
    source=table,
    owner=EntityReference(id=user.id, type="user"),
)
```

---

## Custom Properties

### Create Custom Property Type

```python
from metadata.generated.schema.api.data.createCustomProperty import (
    CreateCustomPropertyRequest,
)
from metadata.generated.schema.type.customProperty import PropertyType

# Create custom property on Table entity
metadata.create_or_update_custom_property(
    ometa_custom_property=CreateCustomPropertyRequest(
        name="costCenter",
        description="Cost center for billing",
        propertyType=PropertyType(
            id=metadata.get_property_type("string").id,
            type="type",
        ),
    ),
    entity_type=Table,
)
```

### Set Custom Property Value

```python
# Set custom property value using extension
table = metadata.get_by_name(entity=Table, fqn="prod.sales.orders")

# Patch extension with custom property
metadata.patch(
    entity=Table,
    source=table,
    destination=table.copy(
        update={"extension": {"costCenter": "SALES-001"}}
    ),
)
```

### Read Custom Property Value

```python
table = metadata.get_by_name(entity=Table, fqn="prod.sales.orders")

if table.extension:
    cost_center = table.extension.get("costCenter")
    print(f"Cost Center: {cost_center}")
```

### Supported Property Types

| Type | Description | Example Value |
|------|-------------|---------------|
| `string` | Text value | `"SALES-001"` |
| `integer` | Whole number | `42` |
| `number` | Decimal number | `3.14` |
| `markdown` | Rich text | `"# Header\nContent"` |
| `enum` | Predefined values | `"option1"` |
| `date` | Date only | `"2024-01-15"` |
| `dateTime` | Date and time | `"2024-01-15T10:30:00Z"` |
| `time` | Time only | `"10:30:00"` |
| `duration` | Time duration | `"PT1H30M"` |
| `entityReference` | Link to entity | `{"id": "uuid", "type": "user"}` |
| `entityReferenceList` | Multiple links | `[{"id": "uuid", "type": "user"}]` |

---

## Lineage Management

### Add Lineage Edge

```python
from metadata.generated.schema.api.lineage.addLineage import AddLineage
from metadata.generated.schema.type.entityLineage import EntitiesEdge

# Get source and target tables
source = metadata.get_by_name(entity=Table, fqn="raw.events")
target = metadata.get_by_name(entity=Table, fqn="analytics.user_events")

# Add lineage
metadata.add_lineage(
    AddLineage(
        edge=EntitiesEdge(
            fromEntity=EntityReference(id=source.id, type="table"),
            toEntity=EntityReference(id=target.id, type="table"),
        ),
    )
)
```

### Add Column-Level Lineage

```python
from metadata.generated.schema.type.entityLineage import ColumnLineage

metadata.add_lineage(
    AddLineage(
        edge=EntitiesEdge(
            fromEntity=EntityReference(id=source.id, type="table"),
            toEntity=EntityReference(id=target.id, type="table"),
            lineageDetails=LineageDetails(
                columnsLineage=[
                    ColumnLineage(
                        fromColumns=["raw.events.user_id"],
                        toColumn="analytics.user_events.user_id",
                    ),
                    ColumnLineage(
                        fromColumns=["raw.events.event_type"],
                        toColumn="analytics.user_events.event_type",
                    ),
                ],
            ),
        ),
    )
)
```

### Query Lineage

```python
lineage = metadata.get_lineage_by_name(
    entity=Table,
    fqn="analytics.user_events",
    up_depth=3,    # Upstream hops
    down_depth=3,  # Downstream hops
)

print("Upstream tables:")
for node in lineage.upstreamEdges:
    print(f"  - {node.fromEntity.name}")

print("Downstream tables:")
for node in lineage.downstreamEdges:
    print(f"  - {node.toEntity.name}")
```

---

## Building Custom Connectors

### Connector Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Workflow                                │
├─────────────────────────────────────────────────────────────┤
│  Source → Processor → Processor → Sink                      │
│    ↓          ↓           ↓         ↓                        │
│  Extract   Transform   Enrich    Load to                     │
│  Records    Data       Data      OpenMetadata                │
└─────────────────────────────────────────────────────────────┘
```

### Source Implementation

```python
from abc import ABC, abstractmethod
from typing import Iterable, Optional
from metadata.ingestion.api.models import Either
from metadata.ingestion.api.steps import Source
from metadata.ingestion.ometa.ometa_api import OpenMetadata

class MyCustomSource(Source):
    """Custom source for extracting metadata."""

    def __init__(self):
        super().__init__()
        self.config = None
        self.metadata = None

    @classmethod
    def create(
        cls,
        config_dict: dict,
        metadata: OpenMetadata,
    ) -> "MyCustomSource":
        instance = cls()
        instance.config = MySourceConfig.parse_obj(config_dict)
        instance.metadata = metadata
        return instance

    def prepare(self):
        """Initialize connections before extraction."""
        self.client = MyApiClient(self.config.api_url)

    def _iter(self) -> Iterable[Either]:
        """Yield records to downstream steps."""
        for item in self.client.list_items():
            yield Either(right=self._convert_to_entity(item))

    def _convert_to_entity(self, item) -> CreateTableRequest:
        """Convert API response to OpenMetadata entity."""
        return CreateTableRequest(
            name=item["name"],
            databaseSchema=self.config.database_schema,
            columns=[
                Column(name=col["name"], dataType=self._map_type(col["type"]))
                for col in item["columns"]
            ],
        )

    def close(self):
        """Cleanup resources."""
        if self.client:
            self.client.close()

    def test_connection(self) -> None:
        """Verify connectivity to source system."""
        self.client.health_check()
```

### Processor Implementation

```python
from metadata.ingestion.api.steps import Processor

class EnrichmentProcessor(Processor):
    """Add additional metadata to records."""

    @classmethod
    def create(cls, config_dict: dict, metadata: OpenMetadata):
        instance = cls()
        instance.config = EnrichmentConfig.parse_obj(config_dict)
        instance.metadata = metadata
        return instance

    def _run(self, record: CreateTableRequest) -> Either:
        """Process each record."""
        # Add custom enrichment
        record.description = self._generate_description(record)
        record.tags = self._auto_classify(record)
        return Either(right=record)

    def close(self):
        pass
```

### Sink Implementation

```python
from metadata.ingestion.api.steps import Sink

class OpenMetadataSink(Sink):
    """Write records to OpenMetadata."""

    @classmethod
    def create(cls, config_dict: dict, metadata: OpenMetadata):
        instance = cls()
        instance.metadata = metadata
        return instance

    def _run(self, record: CreateTableRequest) -> Either:
        """Write record to OpenMetadata."""
        try:
            entity = self.metadata.create_or_update(record)
            return Either(right=entity)
        except Exception as e:
            return Either(left=StackTraceError(str(e)))

    def close(self):
        pass
```

### Workflow Configuration

```yaml
# connector.yaml
source:
  type: MyCustomSource
  serviceName: my-source
  serviceConnection:
    config:
      api_url: https://api.example.com
      database_schema: prod.my_db.public

processor:
  type: EnrichmentProcessor
  config:
    auto_classify: true

sink:
  type: metadata-rest
  config: {}

workflowConfig:
  openMetadataServerConfig:
    hostPort: http://localhost:8585/api
    authProvider: openmetadata
    securityConfig:
      jwtToken: ${OM_JWT_TOKEN}
```

### Run Workflow

```python
from metadata.workflow.metadata import MetadataWorkflow

config = yaml.safe_load(open("connector.yaml"))
workflow = MetadataWorkflow.create(config)

workflow.execute()
workflow.print_status()
workflow.stop()
```

---

## Automation Patterns

### Bulk Tagging

```python
def bulk_tag_tables(metadata: OpenMetadata, pattern: str, tag_fqn: str):
    """Apply tag to all tables matching pattern."""
    tables = metadata.es_search_from_fqn(
        entity_type=Table,
        fqn_search_string=pattern,
    )

    tag = TagLabel(
        tagFQN=tag_fqn,
        source=TagSource.Classification,
        labelType=LabelType.Automated,
        state=State.Confirmed,
    )

    for hit in tables:
        table = metadata.get_by_id(
            entity=Table,
            entity_id=UUID(hit["_source"]["id"]),
        )
        metadata.patch_tag(entity=Table, source=table, tag_label=tag)
        print(f"Tagged: {table.fullyQualifiedName}")

# Tag all PII tables
bulk_tag_tables(metadata, "*customer*", "PII.Sensitive")
```

### Auto-Assign Owners

```python
def auto_assign_owners(metadata: OpenMetadata, rules: dict):
    """Assign owners based on schema/database patterns."""
    for pattern, owner_fqn in rules.items():
        owner = metadata.get_by_name(entity=User, fqn=owner_fqn)
        owner_ref = EntityReference(id=owner.id, type="user")

        tables = metadata.es_search_from_fqn(
            entity_type=Table,
            fqn_search_string=pattern,
        )

        for hit in tables:
            table = metadata.get_by_id(
                entity=Table,
                entity_id=UUID(hit["_source"]["id"]),
            )
            if table.owner is None:
                metadata.patch_owner(entity=Table, source=table, owner=owner_ref)
                print(f"Assigned {owner_fqn} to {table.fullyQualifiedName}")

# Define ownership rules
rules = {
    "*.sales.*": "sales-team-lead",
    "*.analytics.*": "analytics-team-lead",
    "*.finance.*": "finance-team-lead",
}
auto_assign_owners(metadata, rules)
```

### Data Quality Automation

```python
from metadata.generated.schema.tests.testCase import TestCase
from metadata.generated.schema.tests.testDefinition import TestDefinition

def add_null_check_tests(metadata: OpenMetadata, table_fqn: str):
    """Add null check tests to all required columns."""
    table = metadata.get_by_name(
        entity=Table,
        fqn=table_fqn,
        fields=["columns"],
    )

    null_test = metadata.get_by_name(
        entity=TestDefinition,
        fqn="columnValuesToBeNotNull",
    )

    for column in table.columns:
        if column.constraint == "NOT NULL":
            test_case = TestCase(
                name=f"{column.name}_not_null",
                testDefinition=EntityReference(id=null_test.id, type="testDefinition"),
                entityLink=f"<#E::table::{table_fqn}::columns::{column.name}>",
                parameterValues=[],
            )
            metadata.create_or_update(test_case)
            print(f"Added null check for {column.name}")
```

### Lineage Propagation

```python
def propagate_tags_downstream(
    metadata: OpenMetadata,
    source_fqn: str,
    tag_fqn: str,
    max_depth: int = 3,
):
    """Propagate tags through lineage."""
    source = metadata.get_by_name(entity=Table, fqn=source_fqn)

    lineage = metadata.get_lineage_by_name(
        entity=Table,
        fqn=source_fqn,
        down_depth=max_depth,
    )

    tag = TagLabel(
        tagFQN=tag_fqn,
        source=TagSource.Classification,
        labelType=LabelType.Propagated,
        state=State.Confirmed,
    )

    for edge in lineage.downstreamEdges:
        downstream = metadata.get_by_id(
            entity=Table,
            entity_id=edge.toEntity.id,
        )
        metadata.patch_tag(entity=Table, source=downstream, tag_label=tag)
        print(f"Propagated {tag_fqn} to {downstream.fullyQualifiedName}")

# Propagate PII tag through lineage
propagate_tags_downstream(metadata, "raw.customers", "PII.Sensitive")
```

---

## REST API Direct Usage

### Authentication

```bash
# Get JWT token
curl -X POST "http://localhost:8585/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@openmetadata.org", "password": "admin"}'
```

### Common Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List tables | GET | `/api/v1/tables` |
| Get table | GET | `/api/v1/tables/{id}` |
| Get by name | GET | `/api/v1/tables/name/{fqn}` |
| Create/Update | PUT | `/api/v1/tables` |
| Patch | PATCH | `/api/v1/tables/{id}` |
| Delete | DELETE | `/api/v1/tables/{id}` |
| Search | GET | `/api/v1/search/query?q={query}` |
| Lineage | GET | `/api/v1/lineage/{type}/{fqn}` |

### Example: Create Table via REST

```bash
curl -X PUT "http://localhost:8585/api/v1/tables" \
  -H "Authorization: Bearer ${JWT_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "new_table",
    "databaseSchema": "prod.db.schema",
    "columns": [
      {"name": "id", "dataType": "BIGINT"},
      {"name": "name", "dataType": "VARCHAR"}
    ]
  }'
```

---

## Error Handling

### Common Exceptions

```python
from metadata.ingestion.ometa.client import APIError

try:
    table = metadata.get_by_name(entity=Table, fqn="nonexistent.table")
except APIError as e:
    if e.status_code == 404:
        print("Table not found")
    elif e.status_code == 403:
        print("Permission denied")
    else:
        raise
```

### Retry Pattern

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
)
def resilient_create(metadata: OpenMetadata, entity):
    return metadata.create_or_update(entity)
```

---

## Best Practices

### Connection Management

```python
# Use context manager pattern
class OpenMetadataSession:
    def __init__(self, config: OpenMetadataConnection):
        self.config = config
        self.client = None

    def __enter__(self) -> OpenMetadata:
        self.client = OpenMetadata(self.config)
        self.client.health_check()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Client cleanup if needed
        pass

# Usage
with OpenMetadataSession(config) as metadata:
    table = metadata.get_by_name(entity=Table, fqn="prod.sales.orders")
```

### Batch Operations

```python
def batch_update(metadata: OpenMetadata, entities: list, batch_size: int = 50):
    """Update entities in batches to avoid rate limits."""
    for i in range(0, len(entities), batch_size):
        batch = entities[i:i + batch_size]
        for entity in batch:
            metadata.create_or_update(entity)
        time.sleep(0.5)  # Rate limit protection
```

### Idempotent Operations

```python
def ensure_table_exists(metadata: OpenMetadata, create_request: CreateTableRequest):
    """Create table if not exists, otherwise return existing."""
    existing = metadata.get_by_name(
        entity=Table,
        fqn=f"{create_request.databaseSchema}.{create_request.name}",
    )
    if existing:
        return existing
    return metadata.create_or_update(create_request)
```

---

## MCP Server Integration

OpenMetadata provides a Model Context Protocol (MCP) server that enables AI assistants (like Claude and ChatGPT) to interact with your metadata catalog using natural language.

### What is MCP?

MCP (Model Context Protocol) is an open standard that allows AI systems to interact with external tools and data sources in a uniform, secure way. OpenMetadata's MCP server exposes its metadata knowledge graph to AI tools.

### Use Cases

- Natural language queries about data assets
- "What tables contain customer data?"
- "Who owns the orders table?"
- "Show me the lineage for the sales dashboard"
- AI-powered data discovery
- Conversational data governance

### Setting Up MCP

#### 1. Install MCP Application

1. Navigate to **Settings → Applications → Marketplace**
2. Find the **MCP** application
3. Click **Install**
4. Configure the application settings

#### 2. Generate Personal Access Token

1. Go to **Profile → Access Token**
2. Click **Generate New Token**
3. Set appropriate expiration
4. Copy token (shown only once)

#### 3. Configure MCP Client

**For Claude Desktop:**

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "openmetadata": {
      "url": "http://localhost:8585/api/v1/mcp",
      "headers": {
        "Authorization": "Bearer <your-token>"
      }
    }
  }
}
```

**For API Integration:**

```python
import requests

MCP_ENDPOINT = "http://localhost:8585/api/v1/mcp"
TOKEN = "<your-token>"

def query_mcp(prompt: str) -> dict:
    """Send natural language query to OpenMetadata MCP."""
    response = requests.post(
        f"{MCP_ENDPOINT}/query",
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
        json={"prompt": prompt},
    )
    return response.json()

# Example queries
result = query_mcp("What tables are in the sales database?")
result = query_mcp("Show me the owner of the customers table")
result = query_mcp("What is the lineage for the revenue dashboard?")
```

### Available MCP Tools

The MCP server exposes tools for:

| Tool | Description |
|------|-------------|
| **search_assets** | Search for data assets by keyword |
| **get_asset_details** | Get detailed metadata for an asset |
| **get_lineage** | Retrieve lineage for an entity |
| **get_owner** | Find asset ownership |
| **list_tables** | List tables in a database |
| **get_schema** | Get table schema details |

### Security Considerations

1. **Use dedicated tokens** - Don't share personal tokens
2. **Set appropriate permissions** - MCP uses token's permissions
3. **Rotate tokens regularly** - Follow security policies
4. **Audit usage** - Monitor MCP queries in logs

---

## References

- [OpenMetadata Python SDK](https://docs.open-metadata.org/latest/sdk/python)
- [OpenMetadata Java SDK](https://docs.open-metadata.org/latest/sdk/java)
- [OpenMetadata API Reference](https://docs.open-metadata.org/swagger.html)
- [Building Connectors](https://docs.open-metadata.org/latest/sdk/python/build-connector)
- [Data Governance Automation](https://docs.open-metadata.org/latest/how-to-guides/data-governance)
- [MCP Server Guide](https://docs.open-metadata.org/latest/how-to-guides/mcp)
- `openmetadata-sdk-dev` - Implementing SDKs for new languages
- `openmetadata-ops` - Administering OpenMetadata
- `openmetadata-user` - UI navigation and discovery
- `openmetadata-dq` - Data quality and observability
