---
name: orchardcore-custom-indexing-azureai
description: Skill for creating Orchard Core custom indexing pipelines for arbitrary data using Azure AI Search, based on CrestApps AI Memory and OrchardCore.Indexing patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Custom Indexing for Azure AI Search - Prompt Templates

## Create a custom Azure AI Search index for arbitrary data

You are an Orchard Core expert. Generate code and configuration for indexing arbitrary records into Azure AI Search using Orchard Core index profiles, document handlers, and provider-specific mappings.

### When to use this skill

Use this skill when Orchard content-item indexing is not enough and you need an index for custom records such as:

- generated AI artifacts
- domain records stored in a custom catalog
- user-scoped memory or preference records
- imported external business data
- custom vector-search sources

## Architecture to follow

Use the CrestApps AI Memory modules as the reference architecture:

- `CrestApps.OrchardCore.AI.Memory` contains the shared record/indexing logic and the master index setting.
- `CrestApps.OrchardCore.AI.Memory.AzureAI` registers the Azure AI Search indexing source plus provider-specific handlers.
- `CrestApps.OrchardCore.AI.Memory.Elasticsearch` proves the same neutral-document approach can target another provider with different mappings.

### Master index pattern

For arbitrary data, create a single logical index profile type for that record family and let the tenant choose the active master index profile by name.

Then:

1. persist the source record in your own store
2. build a neutral index document model from it
3. use `IDocumentIndexHandler` to map that neutral document into Azure AI Search fields
4. write through the keyed `IDocumentIndexManager`
5. trigger add/update/delete from the record lifecycle, not a single UI path

## Key Orchard Core pieces

- `IIndexProfileStore`
- `IndexProfileHandlerBase`
- `IDocumentIndexHandler`
- keyed `IDocumentIndexManager`
- `services.AddAzureAISearchIndexingSource(type, options => ...)`

## Recommended implementation steps

### 1. Define the custom index profile type

```csharp
public static class CustomerInsightsConstants
{
    public const string IndexingTaskType = "CustomerInsights";
}
```

### 2. Add profile metadata for provider-independent indexing configuration

```csharp
public sealed class CustomerInsightIndexProfileMetadata
{
    public string EmbeddingProviderName { get; set; }
    public string EmbeddingConnectionName { get; set; }
    public string EmbeddingDeploymentName { get; set; }
}
```

This mirrors `AIMemoryIndexProfileMetadata`, which stores embedding provider, connection, and deployment details so the indexing service can generate vectors.

### 3. Register the Azure AI Search source

```csharp
using OrchardCore.Indexing;
using OrchardCore.Indexing.Core;
using OrchardCore.Search.AzureAI;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddIndexProfileHandler<CustomerInsightAzureAISearchIndexProfileHandler>();
        services.AddScoped<IDocumentIndexHandler, CustomerInsightAzureAISearchDocumentIndexHandler>();

        services.AddAzureAISearchIndexingSource(CustomerInsightsConstants.IndexingTaskType, options =>
        {
            options.DisplayName = S["Customer insights (Azure AI Search)"];
            options.Description = S["Create an Azure AI Search index for custom customer insight records."];
        });
    }
}
```

### 4. Configure Azure AI Search mappings in an index-profile handler

```csharp
using OrchardCore.Entities;
using OrchardCore.Indexing.Models;
using OrchardCore.Infrastructure.Entities;
using OrchardCore.Search.AzureAI;
using OrchardCore.Search.AzureAI.Core;
using OrchardCore.Search.AzureAI.Models;

public sealed class CustomerInsightAzureAISearchIndexProfileHandler : IndexProfileHandlerBase
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
            !string.Equals(indexProfile.ProviderName, AzureAISearchConstants.ProviderName, StringComparison.OrdinalIgnoreCase))
        {
            return Task.CompletedTask;
        }

        var metadata = indexProfile.As<AzureAISearchIndexMetadata>();

        metadata.IndexMappings.Add(new AzureAISearchIndexMap
        {
            AzureFieldKey = "RecordId",
            Type = DocumentIndex.Types.Text,
            IsKey = true,
            IsFilterable = true,
        });
        metadata.IndexMappings.Add(new AzureAISearchIndexMap
        {
            AzureFieldKey = "CustomerId",
            Type = DocumentIndex.Types.Text,
            IsFilterable = true,
        });
        metadata.IndexMappings.Add(new AzureAISearchIndexMap
        {
            AzureFieldKey = "Title",
            Type = DocumentIndex.Types.Text,
            IsSearchable = true,
            IsFilterable = true,
        });
        metadata.IndexMappings.Add(new AzureAISearchIndexMap
        {
            AzureFieldKey = "Summary",
            Type = DocumentIndex.Types.Text,
            IsSearchable = true,
        });
        metadata.IndexMappings.Add(new AzureAISearchIndexMap
        {
            AzureFieldKey = "Content",
            Type = DocumentIndex.Types.Text,
            IsSearchable = true,
        });
        metadata.IndexMappings.Add(new AzureAISearchIndexMap
        {
            AzureFieldKey = "UpdatedUtc",
            Type = DocumentIndex.Types.DateTime,
            IsFilterable = true,
            IsSortable = true,
        });
        metadata.IndexMappings.Add(new AzureAISearchIndexMap
        {
            AzureFieldKey = "Embedding",
            Type = DocumentIndex.Types.Number,
            VectorInfo = new AzureAISearchIndexMapVectorInfo
            {
                Dimensions = 1536,
            },
        });

        indexProfile.Put(metadata);
        return Task.CompletedTask;
    }
}
```

### 5. Map neutral records into Azure AI Search documents

```csharp
using OrchardCore.Indexing;
using OrchardCore.Indexing.Models;
using OrchardCore.Search.AzureAI;

public sealed class CustomerInsightAzureAISearchDocumentIndexHandler : IDocumentIndexHandler
{
    public Task BuildIndexAsync(BuildDocumentIndexContext context)
    {
        if (context.Record is not CustomerInsightIndexDocument record)
        {
            return Task.CompletedTask;
        }

        if (!context.AdditionalProperties.TryGetValue(nameof(IndexProfile), out var profile) ||
            profile is not IndexProfile indexProfile ||
            !string.Equals(indexProfile.ProviderName, AzureAISearchConstants.ProviderName, StringComparison.OrdinalIgnoreCase))
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

### 6. Implement a custom indexing service

For arbitrary data, a dedicated indexing service like `AIMemoryIndexingService` is the recommended approach.

That service should:

- read the configured master index profile from site settings
- resolve the profile from `IIndexProfileStore`
- create a neutral index document model
- resolve the keyed `IDocumentIndexManager`
- add/update documents
- delete documents by stable record ID
- support full sync for selected profile IDs

If embeddings are needed, resolve `IEmbeddingGenerator<string, Embedding<float>>` from `IAIClientFactory` and generate vectors during document build.

### 7. Trigger indexing from the store lifecycle

Do not wire Azure AI Search updates only into a tool, controller, or admin button.

Preferred pattern:

- queue upserts and deletes in a scoped handler
- flush them after the underlying catalog/store successfully saves changes

This is the same improvement used in CrestApps AI Memory so every create, update, and delete path stays synchronized automatically.

### 8. Support re-sync when the profile changes

Use `IndexProfileHandlerBase.SynchronizedAsync(...)` to rebuild all documents for the affected profile IDs.

That is especially important when:

- field mappings change
- embedding configuration changes
- the Azure AI Search profile is re-created or renamed

## Azure AI Search specifics

- use `AzureAISearchIndexMetadata`
- create one `AzureAISearchIndexMap` per field
- set `IsKey = true` for the stable document ID field
- use `VectorInfo.Dimensions` for embedding fields
- mark searchable text fields with `IsSearchable = true`
- mark sortable/filterable fields explicitly

## Choosing between Orchard indexing service styles

### Use `NamedIndexingService` when

- the module already fits Orchard's named indexing-task abstraction
- you are coordinating a named provider pipeline with minimal custom orchestration

### Use a custom indexing service when

- the source is arbitrary data
- the module owns the records and the document-building logic
- site settings choose the active master index
- provider-specific handlers shape the final `DocumentIndex`
- indexing must happen from a shared store lifecycle

## CrestApps reference points

- `CrestApps.OrchardCore.AI.Memory`
- `CrestApps.OrchardCore.AI.Memory.AzureAI`
- `CrestApps.OrchardCore.AI.Memory.Elasticsearch`

Follow that separation when generating code:

1. shared module for source records and indexing orchestration
2. provider module for Azure AI Search registration and mappings
