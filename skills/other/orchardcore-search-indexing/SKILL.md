---
name: orchardcore-search-indexing
description: Skill for configuring search and indexing in Orchard Core. Covers Lucene indexing, Elasticsearch integration, search settings, index definitions, and search queries.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Search & Indexing - Prompt Templates

## Configure Search and Indexing

You are an Orchard Core expert. Generate search and indexing configurations for Orchard Core.

### Guidelines

- Orchard Core supports Lucene and Elasticsearch as search providers.
- Enable `OrchardCore.Search.Lucene` or `OrchardCore.Search.Elasticsearch` as needed.
- Lucene indexes are stored on the local file system.
- Elasticsearch requires an external Elasticsearch cluster.
- Create indexes that specify which content types and fields to index.
- Use queries to search indexed content programmatically or via Liquid.
- Content indexing is triggered automatically when content is published or updated.
- Rebuild indexes after changing index definitions.

### Enabling Search Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Search",
        "OrchardCore.Search.Lucene",
        "OrchardCore.Indexing"
      ],
      "disable": []
    }
  ]
}
```

### Lucene Index Configuration via Recipe

```json
{
  "steps": [
    {
      "name": "lucene-index",
      "Indices": [
        {
          "Search": {
            "AnalyzerName": "standardanalyzer",
            "IndexLatest": false,
            "IndexedContentTypes": [
              "Article",
              "BlogPost"
            ],
            "Culture": "",
            "StoreSourceData": false
          }
        }
      ]
    }
  ]
}
```

### Elasticsearch Configuration

Configure in `appsettings.json`:

```json
{
  "OrchardCore": {
    "OrchardCore_Elasticsearch": {
      "Url": "https://localhost:9200",
      "Ports": [9200],
      "ConnectionType": "SingleNodeConnectionPool"
    }
  }
}
```

### Elasticsearch Index via Recipe

```json
{
  "steps": [
    {
      "name": "elasticsearch-index",
      "Indices": [
        {
          "Search": {
            "AnalyzerName": "standard",
            "IndexLatest": false,
            "IndexedContentTypes": [
              "Article",
              "BlogPost"
            ],
            "Culture": "",
            "StoreSourceData": false
          }
        }
      ]
    }
  ]
}
```

### Lucene Queries via Recipe

```json
{
  "steps": [
    {
      "name": "Queries",
      "Queries": [
        {
          "Source": "Lucene",
          "Name": "RecentBlogPosts",
          "Index": "Search",
          "Template": "{\"query\":{\"bool\":{\"filter\":[{\"term\":{\"Content.ContentItem.ContentType\":\"BlogPost\"}}]}},\"sort\":{\"Content.ContentItem.CreatedUtc\":{\"order\":\"desc\"}},\"size\":10}",
          "ReturnContentItems": true,
          "Schema": "[]"
        }
      ]
    }
  ]
}
```

### Using Search in Liquid

```liquid
{% assign results = Queries.RecentBlogPosts | query %}
{% for item in results %}
    <article>
        <h2>{{ item.DisplayText }}</h2>
        <p>{{ item.Content.BlogPost.Subtitle.Text }}</p>
    </article>
{% endfor %}
```

### Programmatic Search Queries

```csharp
using OrchardCore.Search.Lucene;

public sealed class SearchService
{
    private readonly LuceneQueryService _queryService;
    private readonly LuceneIndexManager _indexManager;

    public SearchService(
        LuceneQueryService queryService,
        LuceneIndexManager indexManager)
    {
        _queryService = queryService;
        _indexManager = indexManager;
    }

    public async Task<IEnumerable<string>> SearchAsync(string query)
    {
        var results = await _queryService.SearchAsync(
            new LuceneQueryContext
            {
                IndexName = "Search",
                DefaultSearchFields = new[] { "Content.ContentItem.FullText" }
            },
            query);

        return results.TopDocs.ScoreDocs
            .Select(hit => hit.Doc.ToString());
    }
}
```

### Custom Content Part Indexing

```csharp
using OrchardCore.Indexing;

public sealed class MyPartIndexHandler : ContentPartIndexHandler<MyPart>
{
    public override Task BuildIndexAsync(
        MyPart part,
        BuildPartIndexContext context)
    {
        var options = DocumentIndexOptions.Store;

        context.DocumentIndex.Set(
            $"{nameof(MyPart)}.{nameof(MyPart.MyField)}",
            part.MyField,
            options);

        return Task.CompletedTask;
    }
}
```

### Registering Index Handler

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IContentPartIndexHandler, MyPartIndexHandler>();
    }
}
```

### Search Settings via Recipe

```json
{
  "steps": [
    {
      "name": "Settings",
      "SearchSettings": {
        "ProviderName": "Lucene",
        "Placeholder": "Search...",
        "PageSize": 10
      }
    }
  ]
}
```
