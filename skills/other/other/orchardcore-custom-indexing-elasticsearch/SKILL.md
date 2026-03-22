---
name: orchardcore-custom-indexing-elasticsearch
description: Skill for creating Orchard Core custom indexing pipelines for arbitrary data using Elasticsearch, based on CrestApps AI Memory and OrchardCore.Indexing patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Custom Indexing for Elasticsearch - Prompt Templates

## Create a custom Elasticsearch index for arbitrary data

You are an Orchard Core expert. Generate code and configuration for indexing arbitrary records into Elasticsearch using Orchard Core index profiles, document handlers, and provider-specific mappings.

### When to use this skill

Use this skill when the data source is not standard Orchard content-item indexing. Good examples:

- user-scoped AI memory records
- CRM or ERP records stored in a custom catalog
- generated AI summaries
- external records synchronized into a tenant document store
- any custom record set that needs full-text search, filtering, or vector search

## Architecture to follow

Use the CrestApps AI Memory modules as the reference architecture:

- `CrestApps.OrchardCore.AI.Memory` defines the source record, master index settings, indexing service, and shared index-profile logic.
- `CrestApps.OrchardCore.AI.Memory.Elasticsearch` registers the Elasticsearch indexing source and provider-specific handlers.
- `CrestApps.OrchardCore.AI.Memory.AzureAI` uses the same shared record/indexing pattern but with Azure AI Search mappings.

### Master index pattern

For arbitrary data, create one logical master index profile type for that record family. Then:

1. Store the source records in your own catalog/store.
2. Configure a site setting that chooses the active index profile name.
3. Build a provider-neutral index document model from each source record.
4. Let provider-specific `IDocumentIndexHandler` implementations map that neutral document into Elasticsearch fields.
5. Trigger indexing from the data lifecycle, not from one individual controller, tool, or UI action.

## Key Orchard Core pieces

- `IIndexProfileStore` - loads index profiles
- `IndexProfileHandlerBase` - reacts when an index profile is created, updated, or synchronized
- `IDocumentIndexHandler` - maps a neutral record into `DocumentIndex`
- keyed `IDocumentIndexManager` - writes provider-specific documents
- `services.AddElasticsearchIndexingSource(type, options => ...)` - registers a new index source in the admin UI

## Recommended implementation steps

### 1. Define a source record and index type constant

```csharp
public static class CustomerInsightsConstants
{
    public const string IndexingTaskType = "CustomerInsights";
}

public sealed class CustomerInsightRecord : CatalogItem
{
    public string CustomerId { get; set; }
    public string Title { get; set; }
    public string Summary { get; set; }
    public string Content { get; set; }
    public DateTime UpdatedUtc { get; set; }
    public float[] Embedding { get; set; }
}
```

### 2. Add index-profile metadata when the index needs extra configuration

Use metadata for provider-independent settings such as embedding provider, connection, deployment, or other indexing options.

```csharp
public sealed class CustomerInsightIndexProfileMetadata
{
    public string EmbeddingProviderName { get; set; }
    public string EmbeddingConnectionName { get; set; }
    public string EmbeddingDeploymentName { get; set; }
}
```

### 3. Register the Elasticsearch index source

```csharp
using OrchardCore.Indexing;
using OrchardCore.Indexing.Core;
using OrchardCore.Search.Elasticsearch;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddIndexProfileHandler<CustomerInsightElasticsearchIndexProfileHandler>();
        services.AddScoped<IDocumentIndexHandler, CustomerInsightElasticsearchDocumentIndexHandler>();

        services.AddElasticsearchIndexingSource(CustomerInsightsConstants.IndexingTaskType, options =>
        {
            options.DisplayName = S["Customer insights (Elasticsearch)"];
            options.Description = S["Create an Elasticsearch index for custom customer insight records."];
        });
    }
}
```

### 4. Create a provider-specific index-profile handler

This is where Elasticsearch mappings are defined.

```csharp
using Elastic.Clients.Elasticsearch.Mapping;
using OrchardCore.Entities;
using OrchardCore.Indexing.Models;
using OrchardCore.Infrastructure.Entities;
using OrchardCore.Search.Elasticsearch;
using OrchardCore.Search.Elasticsearch.Core.Models;
using OrchardCore.Search.Elasticsearch.Models;

public sealed class CustomerInsightElasticsearchIndexProfileHandler : IndexProfileHandlerBase
{
    public override Task InitializingAsync(InitializingContext<IndexProfile> context)
        => SetMappingAsync(context.Model);

    public override Task CreatingAsync(CreatingContext<IndexProfile> context)
        => SetMappingAsync(context.Model);

    public override Task UpdatingAsync(UpdatingContext<IndexProfile> context)
        => SetMappingAsync(context.Model);

    private static Task SetMappingAsync(IndexProfile indexProfile)
    {
        if (!string.Equals(indexProfile.Type, CustomerInsightsConstants.IndexingTaskType, StringComparison.OrdinalIgnoreCase) ||
            !string.Equals(indexProfile.ProviderName, ElasticsearchConstants.ProviderName, StringComparison.OrdinalIgnoreCase))
        {
            return Task.CompletedTask;
        }

        var metadata = indexProfile.As<ElasticsearchIndexMetadata>();

        metadata.IndexMappings ??= new ElasticsearchIndexMap();
        metadata.IndexMappings.Mapping ??= new TypeMapping();
        metadata.IndexMappings.Mapping.Properties ??= [];

        metadata.IndexMappings.KeyFieldName = "RecordId";
        metadata.IndexMappings.Mapping.Properties["RecordId"] = new KeywordProperty();
        metadata.IndexMappings.Mapping.Properties["CustomerId"] = new KeywordProperty();
        metadata.IndexMappings.Mapping.Properties["Title"] = new TextProperty();
        metadata.IndexMappings.Mapping.Properties["Summary"] = new TextProperty();
        metadata.IndexMappings.Mapping.Properties["Content"] = new TextProperty();
        metadata.IndexMappings.Mapping.Properties["UpdatedUtc"] = new DateProperty();
        metadata.IndexMappings.Mapping.Properties["Embedding"] = new DenseVectorProperty
        {
            Dims = 1536,
            Index = true,
            Similarity = DenseVectorSimilarity.Cosine,
        };

        indexProfile.Put(metadata);

        var queryMetadata = indexProfile.As<ElasticsearchDefaultQueryMetadata>();
        queryMetadata.DefaultSearchFields = ["Title", "Summary", "Content"];
        indexProfile.Put(queryMetadata);

        return Task.CompletedTask;
    }
}
```

### 5. Create a provider-specific document index handler

Follow the AI Memory pattern: check the record type, read the `IndexProfile` from `AdditionalProperties`, verify the provider name, then map the fields.

```csharp
using OrchardCore.Indexing;
using OrchardCore.Indexing.Models;
using OrchardCore.Search.Elasticsearch;

public sealed class CustomerInsightElasticsearchDocumentIndexHandler : IDocumentIndexHandler
{
    public Task BuildIndexAsync(BuildDocumentIndexContext context)
    {
        if (context.Record is not CustomerInsightIndexDocument record)
        {
            return Task.CompletedTask;
        }

        if (!context.AdditionalProperties.TryGetValue(nameof(IndexProfile), out var profile) ||
            profile is not IndexProfile indexProfile ||
            !string.Equals(indexProfile.ProviderName, ElasticsearchConstants.ProviderName, StringComparison.OrdinalIgnoreCase))
        {
            return Task.CompletedTask;
        }

        context.DocumentIndex.Set("RecordId", record.RecordId, DocumentIndexOptions.Store);
        context.DocumentIndex.Set("CustomerId", record.CustomerId, DocumentIndexOptions.Store);
        context.DocumentIndex.Set("Title", record.Title, DocumentIndexOptions.Store);
        context.DocumentIndex.Set("Summary", record.Summary, DocumentIndexOptions.Store);
        context.DocumentIndex.Set("Content", record.Content, DocumentIndexOptions.Store);
        context.DocumentIndex.Set("UpdatedUtc", record.UpdatedUtc, DocumentIndexOptions.Store);
        context.DocumentIndex.Set("Embedding", record.Embedding, DocumentIndexOptions.Store);

        return Task.CompletedTask;
    }
}
```

### 6. Implement the indexing service

Use a custom indexing service when you are indexing arbitrary records. This is the correct choice when the source is not Orchard content items.

Follow the AI Memory pattern:

- load the active site setting that points to the master index profile
- resolve the profile from `IIndexProfileStore`
- build one neutral index document per record
- get the keyed `IDocumentIndexManager` for the current provider
- call `AddOrUpdateDocumentsAsync()` or `DeleteDocumentsAsync()`

Use `NamedIndexingService` only when the problem already fits Orchard's named indexing-task abstraction. If your module owns a custom store and custom document-building process, a dedicated service like `AIMemoryIndexingService` is usually clearer.

### 7. Trigger indexing from the data lifecycle

Do not call Elasticsearch indexing directly from just one controller or tool.

Preferred pattern:

- track created, updated, and deleted records in a scoped handler
- flush those indexing operations after the store successfully saves changes

That keeps every write path synchronized, including admin pages, tools, background jobs, and future integrations.

### 8. Support full re-sync when an index profile changes

Use `IndexProfileHandlerBase.SynchronizedAsync(...)` to rebuild the external index for the affected profile IDs.

This is how CrestApps AI Memory handles changes to index-profile metadata or mapping configuration.

## Building vector search indexes

If the index uses embeddings:

- store embedding configuration in index-profile metadata
- resolve the embedding generator from `IAIClientFactory`
- generate embeddings during document build
- map vectors with `DenseVectorProperty`
- set `Similarity = DenseVectorSimilarity.Cosine` unless another metric is required

## Choosing between Orchard indexing service styles

### Use `NamedIndexingService` when

- you already fit Orchard's indexing-task model
- the main job is coordinating a known named index task
- the data source already follows Orchard indexing conventions

### Use a custom service like `AIMemoryIndexingService` when

- the source is arbitrary data
- you need site settings to select the active master profile
- you must build a custom neutral document model
- you need provider-specific handlers to shape the final document
- indexing must be triggered from a catalog/store lifecycle

## CrestApps reference points

- `CrestApps.OrchardCore.AI.Memory` - source records, settings, and indexing service
- `CrestApps.OrchardCore.AI.Memory.Elasticsearch` - Elasticsearch source registration and mappings
- `CrestApps.OrchardCore.AI.Memory.AzureAI` - Azure AI Search variant of the same pattern

When generating new code, follow that same separation:

1. shared core module for source records and indexing orchestration
2. provider module for Elasticsearch-specific mapping and provider registration
