---
name: azure-cosmos-db
description: Build globally distributed applications with Azure Cosmos DB. Configure multi-region writes, consistency levels, partitioning, and change feed. Use for NoSQL databases, real-time analytics, and globally distributed data on Azure.
---

# Azure Cosmos DB

Expert guidance for globally distributed NoSQL database on Azure.

## Create Account

```bash
# Create Cosmos DB account
az cosmosdb create \
  --name mycosmosdb \
  --resource-group myResourceGroup \
  --default-consistency-level Session \
  --locations regionName=eastus failoverPriority=0 \
  --locations regionName=westus failoverPriority=1 \
  --enable-automatic-failover true

# Create database
az cosmosdb sql database create \
  --account-name mycosmosdb \
  --resource-group myResourceGroup \
  --name mydb

# Create container
az cosmosdb sql container create \
  --account-name mycosmosdb \
  --resource-group myResourceGroup \
  --database-name mydb \
  --name items \
  --partition-key-path "/partitionKey" \
  --throughput 400
```

## Python SDK

### Connection

```python
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

# Connection string
client = CosmosClient.from_connection_string(conn_str)

# Or with Managed Identity
credential = DefaultAzureCredential()
client = CosmosClient(url=endpoint, credential=credential)

# Get database and container
database = client.get_database_client("mydb")
container = database.get_container_client("items")
```

### CRUD Operations

```python
# Create item
item = {
    "id": "item-1",
    "partitionKey": "category-1",
    "name": "Product A",
    "price": 99.99,
    "tags": ["electronics", "sale"]
}
container.create_item(body=item)

# Read item
item = container.read_item(item="item-1", partition_key="category-1")

# Update item (replace)
item["price"] = 89.99
container.replace_item(item="item-1", body=item)

# Upsert item
container.upsert_item(body=item)

# Delete item
container.delete_item(item="item-1", partition_key="category-1")
```

### Queries

```python
# Simple query
query = "SELECT * FROM c WHERE c.price > 50"
items = list(container.query_items(
    query=query,
    enable_cross_partition_query=True
))

# Parameterized query
query = "SELECT * FROM c WHERE c.category = @category AND c.price < @maxPrice"
parameters = [
    {"name": "@category", "value": "electronics"},
    {"name": "@maxPrice", "value": 100}
]
items = list(container.query_items(
    query=query,
    parameters=parameters,
    enable_cross_partition_query=True
))

# Query with partition key (more efficient)
items = list(container.query_items(
    query="SELECT * FROM c WHERE c.price > 50",
    partition_key="category-1"
))

# Aggregate query
query = "SELECT VALUE COUNT(1) FROM c WHERE c.category = @category"
count = list(container.query_items(query=query, parameters=[{"name": "@category", "value": "electronics"}]))[0]
```

### Bulk Operations

```python
from azure.cosmos import exceptions

# Bulk create
items_to_create = [
    {"id": f"item-{i}", "partitionKey": "bulk", "value": i}
    for i in range(100)
]

for item in items_to_create:
    try:
        container.create_item(body=item)
    except exceptions.CosmosResourceExistsError:
        pass  # Item already exists
```

### Change Feed

```python
# Read change feed
change_feed = container.query_items_change_feed(
    is_start_from_beginning=True,
    partition_key="category-1"
)

for change in change_feed:
    print(f"Changed item: {change['id']}")

# Continue from continuation token
continuation_token = change_feed.continuation_token
change_feed = container.query_items_change_feed(
    continuation=continuation_token,
    partition_key="category-1"
)
```

## .NET SDK

```csharp
using Microsoft.Azure.Cosmos;

// Create client
CosmosClient client = new CosmosClient(connectionString);
Database database = await client.CreateDatabaseIfNotExistsAsync("mydb");
Container container = await database.CreateContainerIfNotExistsAsync(
    "items",
    "/partitionKey",
    throughput: 400
);

// Create item
var item = new { id = "item-1", partitionKey = "cat-1", name = "Product" };
await container.CreateItemAsync(item, new PartitionKey("cat-1"));

// Read item
var response = await container.ReadItemAsync<dynamic>(
    "item-1",
    new PartitionKey("cat-1")
);

// Query
var query = new QueryDefinition("SELECT * FROM c WHERE c.price > @price")
    .WithParameter("@price", 50);

using FeedIterator<dynamic> iterator = container.GetItemQueryIterator<dynamic>(query);
while (iterator.HasMoreResults)
{
    FeedResponse<dynamic> response = await iterator.ReadNextAsync();
    foreach (var item in response)
    {
        Console.WriteLine(item);
    }
}
```

## Consistency Levels

```bash
# Set default consistency
az cosmosdb update \
  --name mycosmosdb \
  --resource-group myResourceGroup \
  --default-consistency-level BoundedStaleness \
  --max-staleness-prefix 100000 \
  --max-interval 5
```

| Level | Description |
|-------|-------------|
| Strong | Linearizable reads, global order |
| Bounded Staleness | Reads lag by K versions or T time |
| Session | Read your own writes (default) |
| Consistent Prefix | Reads never see out-of-order writes |
| Eventual | No ordering guarantee |

## Indexing Policy

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
      "path": "/price/?",
      "indexes": [
        { "kind": "Range", "dataType": "Number" }
      ]
    }
  ],
  "excludedPaths": [
    { "path": "/description/*" },
    { "path": "/_etag/?" }
  ],
  "compositeIndexes": [
    [
      { "path": "/category", "order": "ascending" },
      { "path": "/price", "order": "descending" }
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

## Stored Procedures

```javascript
// Stored procedure
function bulkDelete(query) {
    var collection = getContext().getCollection();
    var response = getContext().getResponse();
    var deleted = 0;

    var accepted = collection.queryDocuments(
        collection.getSelfLink(),
        query,
        function(err, documents) {
            if (err) throw err;

            for (var i = 0; i < documents.length; i++) {
                var accepted = collection.deleteDocument(
                    documents[i]._self,
                    function(err) {
                        if (err) throw err;
                        deleted++;
                    }
                );
                if (!accepted) break;
            }

            response.setBody({ deleted: deleted });
        }
    );
}
```

## Bicep Deployment

```bicep
resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-04-15' = {
  name: accountName
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: true
      }
    ]
    databaseAccountOfferType: 'Standard'
    enableAutomaticFailover: true
    capabilities: [
      { name: 'EnableServerless' }
    ]
  }
}

resource database 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2023-04-15' = {
  parent: cosmosAccount
  name: databaseName
  properties: {
    resource: {
      id: databaseName
    }
  }
}

resource container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2023-04-15' = {
  parent: database
  name: containerName
  properties: {
    resource: {
      id: containerName
      partitionKey: {
        paths: ['/partitionKey']
        kind: 'Hash'
      }
      indexingPolicy: {
        indexingMode: 'consistent'
        includedPaths: [{ path: '/*' }]
        excludedPaths: [{ path: '/_etag/?' }]
      }
    }
  }
}
```

## Resources

- [Azure Cosmos DB Documentation](https://learn.microsoft.com/azure/cosmos-db/)
- [Cosmos DB Python SDK](https://learn.microsoft.com/azure/cosmos-db/nosql/sdk-python)
- [Best Practices](https://learn.microsoft.com/azure/cosmos-db/nosql/best-practice-dotnet)
