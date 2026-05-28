---
name: orchardcore-content-queries
description: Skill for querying content items in Orchard Core using YesSql. Covers ContentItemIndex queries, custom index creation, ISession usage, IContentManager queries, and query optimization patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Content Queries - Prompt Templates

## Query Content Items

You are an Orchard Core expert. Generate code for querying content items using YesSql indexes and IContentManager.

### Guidelines

- Orchard Core uses YesSql as its document database abstraction over SQL.
- `ISession` is the primary interface for querying YesSql indexes.
- `ContentItemIndex` is the built-in index for all content items.
- Custom indexes can be created for frequently queried fields.
- `IContentManager` provides higher-level content operations (Get, New, Create, Publish).
- Always use `async/await` patterns for database queries.
- Use `.With<IndexType>()` to join against specific indexes.
- Always seal classes.

### Querying with ContentItemIndex

```csharp
using OrchardCore.ContentManagement;
using OrchardCore.ContentManagement.Records;
using YesSql;

public sealed class ContentQueryService
{
    private readonly ISession _session;

    public ContentQueryService(ISession session)
    {
        _session = session;
    }

    // Query by content type
    public async Task<IEnumerable<ContentItem>> GetByTypeAsync(string contentType)
    {
        return await _session
            .Query<ContentItem, ContentItemIndex>(x => x.ContentType == contentType && x.Published)
            .ListAsync();
    }

    // Query by content type with paging
    public async Task<IEnumerable<ContentItem>> GetPagedAsync(string contentType, int page, int pageSize)
    {
        return await _session
            .Query<ContentItem, ContentItemIndex>(x => x.ContentType == contentType && x.Published)
            .OrderByDescending(x => x.CreatedUtc)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ListAsync();
    }

    // Query by display text
    public async Task<ContentItem> GetByDisplayTextAsync(string displayText)
    {
        return await _session
            .Query<ContentItem, ContentItemIndex>(x => x.DisplayText == displayText && x.Published)
            .FirstOrDefaultAsync();
    }

    // Count content items
    public async Task<int> CountByTypeAsync(string contentType)
    {
        return await _session
            .Query<ContentItem, ContentItemIndex>(x => x.ContentType == contentType && x.Published)
            .CountAsync();
    }

    // Query latest versions (including drafts)
    public async Task<IEnumerable<ContentItem>> GetLatestAsync(string contentType)
    {
        return await _session
            .Query<ContentItem, ContentItemIndex>(x => x.ContentType == contentType && x.Latest)
            .ListAsync();
    }
}
```

### ContentItemIndex Fields Reference

The built-in `ContentItemIndex` has these fields:

- `ContentItemId` — Unique content item identifier.
- `ContentItemVersionId` — Version-specific identifier.
- `ContentType` — The content type name.
- `DisplayText` — The display text (usually from TitlePart).
- `Published` — Whether this version is the published one.
- `Latest` — Whether this version is the latest one.
- `CreatedUtc` — When the content item was created.
- `ModifiedUtc` — When the content item was last modified.
- `PublishedUtc` — When the content item was published.
- `Owner` — The owner user ID.
- `Author` — The author user name.

### Creating a Custom YesSql Index

```csharp
using OrchardCore.ContentManagement;
using YesSql.Indexes;

public sealed class {{PartName}}Index : MapIndex
{
    public string ContentItemId { get; set; }
    public string {{PropertyName}} { get; set; }
    public bool Published { get; set; }
}

public sealed class {{PartName}}IndexProvider : IndexProvider<ContentItem>
{
    public override void Describe(DescribeContext<ContentItem> context)
    {
        context.For<{{PartName}}Index>()
            .When(contentItem => contentItem.Has<{{PartName}}>())
            .Map(contentItem =>
            {
                var part = contentItem.As<{{PartName}}>();
                return new {{PartName}}Index
                {
                    ContentItemId = contentItem.ContentItemId,
                    {{PropertyName}} = part.{{PropertyName}},
                    Published = contentItem.Published
                };
            });
    }
}
```

### Registering Custom Index and Migration

```csharp
using OrchardCore.Data.Migration;
using YesSql.Sql;

public sealed class Migrations : DataMigration
{
    public async Task<int> CreateAsync()
    {
        await SchemaBuilder.CreateMapIndexTableAsync<{{PartName}}Index>(table => table
            .Column<string>(nameof({{PartName}}Index.ContentItemId), col => col.WithLength(26))
            .Column<string>(nameof({{PartName}}Index.{{PropertyName}}), col => col.WithLength(256))
            .Column<bool>(nameof({{PartName}}Index.Published))
        );

        await SchemaBuilder.AlterIndexTableAsync<{{PartName}}Index>(table => table
            .CreateIndex("IDX_{{PartName}}Index_{{PropertyName}}",
                nameof({{PartName}}Index.{{PropertyName}}),
                nameof({{PartName}}Index.Published))
        );

        return 1;
    }
}
```

### Registering Index Provider in Startup

```csharp
using OrchardCore.Data.Migration;
using YesSql.Indexes;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddIndexProvider<{{PartName}}IndexProvider>();
        services.AddScoped<IDataMigration, Migrations>();
    }
}
```

### Querying with Custom Index

```csharp
public sealed class {{PartName}}QueryService
{
    private readonly ISession _session;

    public {{PartName}}QueryService(ISession session)
    {
        _session = session;
    }

    public async Task<IEnumerable<ContentItem>> GetByPropertyAsync(string value)
    {
        return await _session
            .Query<ContentItem, {{PartName}}Index>(x => x.{{PropertyName}} == value && x.Published)
            .ListAsync();
    }
}
```

### Using IContentManager

```csharp
using OrchardCore.ContentManagement;

public sealed class ContentService
{
    private readonly IContentManager _contentManager;

    public ContentService(IContentManager contentManager)
    {
        _contentManager = contentManager;
    }

    // Get by ID
    public async Task<ContentItem> GetByIdAsync(string contentItemId)
    {
        return await _contentManager.GetAsync(contentItemId);
    }

    // Get specific version
    public async Task<ContentItem> GetVersionAsync(string contentItemId, string versionId)
    {
        return await _contentManager.GetVersionAsync(versionId);
    }

    // Create new content item
    public async Task<ContentItem> CreateAsync(string contentType)
    {
        var contentItem = await _contentManager.NewAsync(contentType);
        await _contentManager.CreateAsync(contentItem, VersionOptions.Draft);
        return contentItem;
    }

    // Publish a content item
    public async Task PublishAsync(ContentItem contentItem)
    {
        await _contentManager.PublishAsync(contentItem);
    }

    // Update content item
    public async Task UpdateAsync(ContentItem contentItem)
    {
        await _contentManager.UpdateAsync(contentItem);
    }

    // Remove content item
    public async Task RemoveAsync(ContentItem contentItem)
    {
        await _contentManager.RemoveAsync(contentItem);
    }
}
```

### Querying with SQL Directly (Advanced)

For complex queries that can't be expressed with YesSql indexes:

```csharp
using YesSql;

public sealed class AdvancedQueryService
{
    private readonly ISession _session;

    public AdvancedQueryService(ISession session)
    {
        _session = session;
    }

    public async Task<IEnumerable<ContentItem>> QueryWithSqlAsync()
    {
        return await _session
            .Query<ContentItem, ContentItemIndex>()
            .Where(x => x.Published && x.ContentType == "Article")
            .OrderByDescending(x => x.PublishedUtc)
            .Take(10)
            .ListAsync();
    }
}
```
