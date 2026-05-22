---
name: orchardcore-content-items
description: Skill for working with Orchard Core content items. Covers the content item lifecycle, IContentManager API, content item JSON structure, querying with YesSql, content handlers, recipe import/export, and accessing parts and fields programmatically.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Content Items - Prompt Templates

## Working with Content Items

You are an Orchard Core expert. Generate code and configuration for managing content items in Orchard Core.

### Guidelines

- Content items are the fundamental data units in Orchard Core, composed of parts and fields.
- Every content item has a `ContentItemId` (stable across versions) and a `ContentItemVersionId` (unique per version).
- Use `IContentManager` for all content item CRUD operations; do not manipulate the database directly.
- Content items support draft and published states when the content type is configured as `Draftable`.
- Content items support versioning when the content type is configured as `Versionable`.
- Always call `await ISession.SaveChangesAsync()` or let the request pipeline flush changes when modifying content outside of `IContentManager`.
- Use `IContentHandler` to hook into lifecycle events such as creating, publishing, and removing content.
- Enable `OrchardCore.ContentManagement` feature to access content management APIs.

### Content Item Lifecycle

A content item progresses through the following states:

1. **New** - Created in memory with `NewAsync`, not yet persisted.
2. **Draft** - Saved but not published. Only visible to editors.
3. **Published** - Live and visible to all users. Sets `Published = true` and `Latest = true`.
4. **Unpublished** - Previously published, now reverted to draft state.
5. **Removed** - Soft-deleted from the system.

When a published content item is edited, a new draft version is created while the published version remains live. Publishing the draft replaces the previous published version.

### Content Item JSON Structure

```json
{
  "ContentItemId": "{{unique-content-item-id}}",
  "ContentItemVersionId": "{{unique-version-id}}",
  "ContentType": "{{ContentTypeName}}",
  "DisplayText": "{{Display Title}}",
  "Latest": true,
  "Published": true,
  "CreatedUtc": "2025-01-01T00:00:00Z",
  "ModifiedUtc": "2025-01-01T00:00:00Z",
  "PublishedUtc": "2025-01-01T00:00:00Z",
  "Owner": "{{userId}}",
  "Author": "{{userName}}",
  "TitlePart": {
    "Title": "{{Display Title}}"
  },
  "AutoroutePart": {
    "Path": "{{url-slug}}",
    "SetHomepage": false
  },
  "{{ContentTypeName}}": {
    "{{FieldName}}": {
      "Text": "{{field value}}"
    }
  }
}
```

### IContentManager API

Use `IContentManager` to perform all content item operations:

```csharp
public sealed class {{ServiceName}}
{
    private readonly IContentManager _contentManager;

    public {{ServiceName}}(IContentManager contentManager)
    {
        _contentManager = contentManager;
    }

    public async Task ManageContentAsync()
    {
        // Create a new content item in memory (not yet saved).
        var contentItem = await _contentManager.NewAsync("{{ContentTypeName}}");

        // Persist the content item as a draft.
        await _contentManager.CreateAsync(contentItem, VersionOptions.Draft);

        // Retrieve a content item by its ID (latest version).
        var latest = await _contentManager.GetAsync(
            contentItem.ContentItemId, VersionOptions.Latest);

        // Retrieve the published version of a content item.
        var published = await _contentManager.GetAsync(
            contentItem.ContentItemId, VersionOptions.Published);

        // Update an existing content item.
        await _contentManager.UpdateAsync(contentItem);

        // Publish a draft content item.
        await _contentManager.PublishAsync(contentItem);

        // Unpublish a published content item (revert to draft).
        await _contentManager.UnpublishAsync(contentItem);

        // Remove (soft-delete) a content item.
        await _contentManager.RemoveAsync(contentItem);
    }
}
```

### Accessing Parts and Fields

Content items store data in parts and fields. Use the `As<T>()` and `Get<T>()` extension methods to access them:

```csharp
public sealed class {{ServiceName}}
{
    private readonly IContentManager _contentManager;

    public {{ServiceName}}(IContentManager contentManager)
    {
        _contentManager = contentManager;
    }

    public async Task ReadPartAndFieldValuesAsync(string contentItemId)
    {
        var contentItem = await _contentManager.GetAsync(
            contentItemId, VersionOptions.Published);

        // Access a well-known part using the strongly-typed helper.
        var titlePart = contentItem.As<TitlePart>();
        var title = titlePart?.Title;

        // Access a named part as a content element.
        var customPart = contentItem.Get<ContentPart>("{{ContentTypeName}}");

        // Access a field within the named part.
        var textField = customPart?.Get<TextField>("{{FieldName}}");
        var fieldValue = textField?.Text;
    }

    public async Task SetPartAndFieldValuesAsync()
    {
        var contentItem = await _contentManager.NewAsync("{{ContentTypeName}}");

        // Set a well-known part value.
        contentItem.Alter<TitlePart>(part =>
        {
            part.Title = "{{Title}}";
        });

        // Set a field value on a named part.
        contentItem.Alter<ContentPart>("{{ContentTypeName}}", part =>
        {
            part.Alter<TextField>("{{FieldName}}", field =>
            {
                field.Text = "{{value}}";
            });
        });

        await _contentManager.CreateAsync(contentItem, VersionOptions.Published);
    }
}
```

### Querying Content Items with YesSql

Use `ISession` to query content items through YesSql indexes:

```csharp
public sealed class {{ServiceName}}
{
    private readonly ISession _session;

    public {{ServiceName}}(ISession session)
    {
        _session = session;
    }

    public async Task<IEnumerable<ContentItem>> QueryContentItemsAsync()
    {
        // Query published content items of a specific type.
        var items = await _session
            .Query<ContentItem, ContentItemIndex>(index =>
                index.ContentType == "{{ContentTypeName}}"
                && index.Published)
            .ListAsync();

        return items;
    }

    public async Task<ContentItem?> FindByDisplayTextAsync(string displayText)
    {
        // Query by display text.
        var item = await _session
            .Query<ContentItem, ContentItemIndex>(index =>
                index.DisplayText == displayText
                && index.Published)
            .FirstOrDefaultAsync();

        return item;
    }
}
```

### Content Handlers

Implement `IContentHandler` to respond to content lifecycle events. Handlers are invoked by `IContentManager` during create, update, publish, unpublish, and remove operations:

```csharp
public sealed class {{HandlerName}} : ContentHandlerBase
{
    private readonly ILogger<{{HandlerName}}> _logger;

    public {{HandlerName}}(ILogger<{{HandlerName}}> logger)
    {
        _logger = logger;
    }

    public override Task PublishedAsync(PublishContentContext context)
    {
        if (context.ContentItem.ContentType == "{{ContentTypeName}}")
        {
            _logger.LogInformation(
                "Content item '{DisplayText}' was published.",
                context.ContentItem.DisplayText);
        }

        return Task.CompletedTask;
    }

    public override Task RemovedAsync(RemoveContentContext context)
    {
        if (context.ContentItem.ContentType == "{{ContentTypeName}}")
        {
            _logger.LogInformation(
                "Content item '{DisplayText}' was removed.",
                context.ContentItem.DisplayText);
        }

        return Task.CompletedTask;
    }
}
```

Register the handler in a `Startup` class:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddContentHandler<{{HandlerName}}>();
    }
}
```

Common handler methods include:
- `CreatingAsync` / `CreatedAsync` - Before and after a content item is persisted.
- `UpdatingAsync` / `UpdatedAsync` - Before and after a content item is updated.
- `PublishingAsync` / `PublishedAsync` - Before and after a content item is published.
- `UnpublishingAsync` / `UnpublishedAsync` - Before and after a content item is unpublished.
- `RemovingAsync` / `RemovedAsync` - Before and after a content item is removed.
- `LoadingAsync` / `LoadedAsync` - When a content item is loaded from the store.

### Content Item Import/Export via Recipes

Use the `content` recipe step to import or export content items:

```json
{
  "steps": [
    {
      "name": "Content",
      "data": [
        {
          "ContentItemId": "{{unique-id-1}}",
          "ContentType": "{{ContentTypeName}}",
          "DisplayText": "{{Title}}",
          "Latest": true,
          "Published": true,
          "TitlePart": {
            "Title": "{{Title}}"
          },
          "{{ContentTypeName}}": {
            "{{FieldName}}": {
              "Text": "{{value}}"
            }
          }
        }
      ]
    }
  ]
}
```

- Each object in the `data` array represents a content item to import.
- Set `ContentItemId` to a stable unique value to allow re-importing without duplicates.
- Set `Published` to `true` to publish the item immediately upon import.
- Part and field data are stored as nested objects matching their technical names.

### ContentElement, ContentPart, and ContentField

- `ContentElement` is the base class for all content components. It exposes the parent `ContentItem` reference and JSON data access.
- `ContentPart` extends `ContentElement` and represents a composable unit attached to a content type (e.g., `TitlePart`, `AutoroutePart`).
- `ContentField` extends `ContentElement` and represents a data field within a part (e.g., `TextField`, `HtmlField`, `NumericField`).
- Custom parts and fields can be created by inheriting from `ContentPart` or `ContentField` respectively.

```csharp
public sealed class {{PartName}} : ContentPart
{
    public string? Subtitle { get; set; }
    public bool IsFeatured { get; set; }
}
```
