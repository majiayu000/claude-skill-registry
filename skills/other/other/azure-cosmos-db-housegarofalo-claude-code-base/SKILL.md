---
name: azure-cosmos-db
description: Build globally distributed applications with Azure Cosmos DB. Configure multi-region writes, consistency levels, partitioning, and change feed. Use for NoSQL databases, real-time analytics, and globally distributed data on Azure.
---

# Azure Cosmos DB

Expert guidance for globally distributed NoSQL database on Azure.

## Triggers

Use this skill when:
- Creating and configuring Azure Cosmos DB accounts
- Working with Python or .NET SDK for Cosmos DB
- Designing partition keys and data models
- Configuring consistency levels
- Setting up indexing policies
- Writing stored procedures and triggers
- Deploying with Bicep/ARM templates
- Implementing change feed patterns
- Keywords: cosmos db, azure cosmosdb, nosql, partition key, consistency level, change feed, globally distributed, documentdb

### Create Cosmos DB Account

```bash
# Create Cosmos DB account
az cosmosdb create \
    --name mycosmosdb \
    --resource-group mygroup \
    --kind GlobalDocumentDB \
    --default-consistency-level Session \
    --locations regionName=eastus failoverPriority=0 isZoneRedundant=True \
    --locations regionName=westus failoverPriority=1 isZoneRedundant=False

# Create database
az cosmosdb sql database create \
    --account-name mycosmosdb \
    --resource-group mygroup \
    --name mydb

# Create container with partition key
az cosmosdb sql container create \
    --account-name mycosmosdb \
    --resource-group mygroup \
    --database-name mydb \
    --name users \
    --partition-key-path /userId \
    --throughput 400
```

### Python SDK Operations

```python
from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Initialize client
client = CosmosClient(
    url="https://mycosmosdb.documents.azure.com:443/",
    credential="your-key"
)

# Get database and container
database = client.get_database_client("mydb")
container = database.get_container_client("users")

# Create item
user = {
    "id": "user-123",
    "userId": "user-123",
    "name": "John Doe",
    "email": "john@example.com",
    "createdAt": datetime.utcnow().isoformat()
}

container.create_item(body=user)

# Read item
item = container.read_item(
    item="user-123",
    partition_key="user-123"
)

# Query items
query = "SELECT * FROM c WHERE c.email = @email"
parameters = [{"name": "@email", "value": "john@example.com"}]

items = list(container.query_items(
    query=query,
    parameters=parameters,
    enable_cross_partition_query=True
))

# Update item
user["name"] = "John Smith"
container.replace_item(item="user-123", body=user)

# Delete item
container.delete_item(item="user-123", partition_key="user-123")
```

### TypeScript SDK Operations

```typescript
import { CosmosClient, Container } from "@azure/cosmos";

const client = new CosmosClient({
  endpoint: "https://mycosmosdb.documents.azure.com:443/",
  key: "your-key"
});

const database = client.database("mydb");
const container = database.container("users");

// Create item
const user = {
  id: "user-123",
  userId: "user-123",
  name: "John Doe",
  email: "john@example.com"
};

const { resource: createdItem } = await container.items.create(user);

// Read item
const { resource: item } = await container.item("user-123", "user-123").read();

// Query items
const { resources: items } = await container.items
  .query({
    query: "SELECT * FROM c WHERE c.email = @email",
    parameters: [{ name: "@email", value: "john@example.com" }]
  })
  .fetchAll();

// Update item
user.name = "John Smith";
await container.item("user-123", "user-123").replace(user);

// Delete item
await container.item("user-123", "user-123").delete();
```

### Partition Key Design

```python
# Single field partition key
container = database.create_container(
    id="orders",
    partition_key=PartitionKey(path="/customerId")
)

# Hierarchical partition key (preview)
container = database.create_container(
    id="events",
    partition_key=PartitionKey(path=["/tenantId", "/year", "/month"])
)

# Good partition key examples:
# - /userId for user data
# - /tenantId for multi-tenant apps
# - /categoryId for product catalog
# - /deviceId for IoT data
```

### Consistency Levels

```bash
# Set default consistency level
az cosmosdb update \
    --name mycosmosdb \
    --resource-group mygroup \
    --default-consistency-level BoundedStaleness \
    --max-interval 5 \
    --max-staleness-prefix 100

# Consistency levels (strongest to weakest):
# 1. Strong - Linearizable reads
# 2. Bounded Staleness - Reads lag by at most k versions or t time
# 3. Session - Monotonic reads/writes within session (default)
# 4. Consistent Prefix - Reads never see out-of-order writes
# 5. Eventual - No ordering guarantee
```

### Change Feed

```python
from azure.cosmos import ChangeFeedState

# Read change feed from beginning
change_feed = container.query_items_change_feed(
    start_time="Beginning"
)

for item in change_feed:
    print(f"Changed item: {item['id']}")

# Read change feed from specific time
change_feed = container.query_items_change_feed(
    start_time=datetime(2024, 1, 1)
)

# Continue from continuation token
change_feed = container.query_items_change_feed(
    continuation=previous_continuation_token
)
```

### Stored Procedures

```javascript
// Create stored procedure
function bulkDelete(query) {
    var collection = getContext().getCollection();
    var response = getContext().getResponse();
    var deleted = 0;

    collection.queryDocuments(
        collection.getSelfLink(),
        query,
        function(err, documents) {
            if (err) throw err;

            documents.forEach(function(doc) {
                collection.deleteDocument(doc._self, function(err) {
                    if (err) throw err;
                    deleted++;
                });
            });

            response.setBody({ deleted: deleted });
        }
    );
}
```

```python
# Register stored procedure
container.scripts.create_stored_procedure({
    "id": "bulkDelete",
    "body": stored_procedure_code
})

# Execute stored procedure
result = container.scripts.execute_stored_procedure(
    sproc="bulkDelete",
    params=["SELECT * FROM c WHERE c.expired = true"],
    partition_key="partition-value"
)
```

### Indexing Policy

```json
{
  "indexingMode": "consistent",
  "automatic": true,
  "includedPaths": [
    {
      "path": "/name/?",
      "indexes": [
        { "kind": "Range", "dataType": "String" }
      ]
    },
    {
      "path": "/age/?",
      "indexes": [
        { "kind": "Range", "dataType": "Number" }
      ]
    }
  ],
  "excludedPaths": [
    { "path": "/metadata/*" },
    { "path": "/_etag/?" }
  ],
  "compositeIndexes": [
    [
      { "path": "/name", "order": "ascending" },
      { "path": "/age", "order": "descending" }
    ]
  ],
  "spatialIndexes": [
    {
      "path": "/location/*",
      "types": ["Point", "Polygon"]
    }
  ]
}
```

### Multi-Region Configuration

```bash
# Add region
az cosmosdb update \
    --name mycosmosdb \
    --resource-group mygroup \
    --locations regionName=eastus failoverPriority=0 \
    --locations regionName=westus failoverPriority=1 \
    --locations regionName=northeurope failoverPriority=2

# Enable multi-region writes
az cosmosdb update \
    --name mycosmosdb \
    --resource-group mygroup \
    --enable-multiple-write-locations true

# Manual failover
az cosmosdb failover-priority-change \
    --name mycosmosdb \
    --resource-group mygroup \
    --failover-policies westus=0 eastus=1
```

## Best Practices

1. **Partition Key**: Choose high-cardinality fields that evenly distribute data
2. **Consistency**: Use Session consistency for most scenarios
3. **Indexing**: Exclude paths not used in queries
4. **RU Budget**: Monitor and optimize Request Unit consumption
5. **Multi-Region**: Enable for high availability and low latency

## Common Workflows

### Set Up Cosmos DB
1. Create Cosmos DB account with appropriate regions
2. Create database and containers with partition keys
3. Configure indexing policy for query patterns
4. Set up connection in application
5. Implement CRUD operations with SDK

### Optimize Performance
1. Review Query Metrics in Azure Portal
2. Analyze partition key distribution
3. Optimize indexing policy
4. Implement caching for hot data
5. Scale throughput based on usage patterns
