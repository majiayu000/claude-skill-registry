---
name: orchardcore-autoroute
description: Skill for configuring AutoroutePart in Orchard Core. Covers URL pattern syntax using Liquid expressions, AutoroutePartSettings, SEO-friendly slugs, hierarchical container routing, home page routing, route conflict resolution, and programmatic route management.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core AutoroutePart - Prompt Templates

## Configure AutoroutePart

You are an Orchard Core expert. Generate code and configuration for AutoroutePart URL routing.

### Guidelines

- AutoroutePart generates SEO-friendly URLs (permalinks) for content items based on Liquid patterns.
- The default URL pattern is `{{ ContentItem | display_text | slugify }}`, which derives the slug from the content item's display text.
- AutoroutePart requires `TitlePart` (or another display text source) to be attached to the content type for `display_text` to resolve.
- Enable the `OrchardCore.Autoroute` feature before using AutoroutePart.
- Set `AllowCustomPath = true` to let editors override the generated URL with a custom path.
- Set `ShowHomepageOption = true` to allow editors to designate a content item as the site home page.
- Set `AllowRouteContainedItems = true` on container types (those with `ListPart` or `BagPart`) to generate routes for child items using hierarchical URL patterns.
- Orchard Core automatically appends a numeric suffix (e.g., `-1`, `-2`) when a generated slug conflicts with an existing route.
- Liquid patterns have access to `ContentItem` properties including `ContentType`, `DisplayText`, `CreatedUtc`, and all attached part data.

### AutoroutePartSettings Properties

| Property | Type | Description |
|---|---|---|
| `Pattern` | `string` | Liquid template that generates the URL path. |
| `AllowCustomPath` | `bool` | When `true`, editors can manually enter a custom URL. |
| `ShowHomepageOption` | `bool` | When `true`, a checkbox appears to set the item as the site home page. |
| `AllowRouteContainedItems` | `bool` | When `true`, contained items in `ListPart` or `BagPart` receive their own routes derived from the container path. |
| `AllowDisabled` | `bool` | When `true`, editors can disable autoroute generation for individual content items. |
| `AllowAbsolutePath` | `bool` | When `true`, allows paths that start with `/` to be treated as absolute. |

### Migration Pattern

```csharp
public sealed class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public int Create()
    {
        _contentDefinitionManager.AlterTypeDefinition("{{ContentTypeName}}", type => type
            .DisplayedAs("{{DisplayName}}")
            .Creatable()
            .Listable()
            .Draftable()
            .Versionable()
            .WithPart("TitlePart", part => part
                .WithPosition("0")
            )
            .WithPart("AutoroutePart", part => part
                .WithPosition("1")
                .WithSettings(new AutoroutePartSettings
                {
                    AllowCustomPath = true,
                    ShowHomepageOption = true,
                    Pattern = "{{ ContentItem | display_text | slugify }}"
                })
            )
        );

        return 1;
    }
}
```

### Enabling AutoroutePart via Recipe

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Autoroute",
        "OrchardCore.Contents"
      ],
      "disable": []
    }
  ]
}
```

### Content Type Definition with AutoroutePart via Recipe

```json
{
  "steps": [
    {
      "name": "ContentDefinition",
      "ContentTypes": [
        {
          "Name": "Article",
          "DisplayName": "Article",
          "Settings": {
            "ContentTypeSettings": {
              "Creatable": true,
              "Listable": true,
              "Draftable": true,
              "Versionable": true
            }
          },
          "ContentTypePartDefinitionRecords": [
            {
              "PartName": "TitlePart",
              "Name": "TitlePart",
              "Settings": {
                "ContentTypePartSettings": {
                  "Position": "0"
                }
              }
            },
            {
              "PartName": "AutoroutePart",
              "Name": "AutoroutePart",
              "Settings": {
                "ContentTypePartSettings": {
                  "Position": "1"
                },
                "AutoroutePartSettings": {
                  "AllowCustomPath": true,
                  "ShowHomepageOption": true,
                  "Pattern": "{{ ContentItem | display_text | slugify }}"
                }
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### Common Liquid URL Patterns

```text
# Simple slug from display text
{{ ContentItem | display_text | slugify }}

# Prefixed with content type
{{ ContentItem.ContentType | downcase }}/{{ ContentItem | display_text | slugify }}

# Date-based blog pattern
{{ ContentItem.CreatedUtc | date: '%Y' }}/{{ ContentItem.CreatedUtc | date: '%m' }}/{{ ContentItem | display_text | slugify }}

# Category prefix from a taxonomy field
{% assign terms = ContentItem.Content.Article.Category.TermContentItemIds | terms %}
{% for term in terms %}{{ term | display_text | slugify }}/{% endfor %}{{ ContentItem | display_text | slugify }}
```

### Container Routing with ListPart

When `AllowRouteContainedItems` is enabled on a container, child items inherit the container's URL as a prefix. For example, a Blog container at `/blog` with a BlogPost child titled "My First Post" generates the URL `/blog/my-first-post`.

```csharp
public sealed class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public int Create()
    {
        _contentDefinitionManager.AlterTypeDefinition("Blog", type => type
            .DisplayedAs("Blog")
            .Creatable()
            .Listable()
            .Draftable()
            .WithPart("TitlePart", part => part
                .WithPosition("0")
            )
            .WithPart("AutoroutePart", part => part
                .WithPosition("1")
                .WithSettings(new AutoroutePartSettings
                {
                    AllowCustomPath = true,
                    Pattern = "{{ ContentItem | display_text | slugify }}",
                    AllowRouteContainedItems = true
                })
            )
            .WithPart("ListPart", part => part
                .WithPosition("2")
                .WithSettings(new ListPartSettings
                {
                    ContainedContentTypes = new[] { "BlogPost" }
                })
            )
        );

        _contentDefinitionManager.AlterTypeDefinition("BlogPost", type => type
            .DisplayedAs("Blog Post")
            .Draftable()
            .Versionable()
            .WithPart("TitlePart", part => part
                .WithPosition("0")
            )
            .WithPart("AutoroutePart", part => part
                .WithPosition("1")
                .WithSettings(new AutoroutePartSettings
                {
                    AllowCustomPath = true,
                    Pattern = "{{ ContentItem | display_text | slugify }}"
                })
            )
            .WithPart("HtmlBodyPart", part => part
                .WithPosition("2")
                .WithEditor("Wysiwyg")
            )
        );

        return 1;
    }
}
```

### Programmatic Route Management

Use `IAutorouteEntries` to look up and manage route entries programmatically:

```csharp
using OrchardCore.Autoroute.Services;

public sealed class RouteService
{
    private readonly IAutorouteEntries _autorouteEntries;

    public RouteService(IAutorouteEntries autorouteEntries)
    {
        _autorouteEntries = autorouteEntries;
    }

    public async Task<string> GetContentItemIdByPathAsync(string path)
    {
        (var found, var entry) = await _autorouteEntries.TryGetEntryByPathAsync(path);

        if (found)
        {
            return entry.ContentItemId;
        }

        return null;
    }
}
```

### Home Page Routing

When `ShowHomepageOption` is enabled and an editor marks a content item as the home page, Orchard Core routes the site root URL (`/`) to that content item. Only one content item can be the home page at a time; setting a new home page automatically unsets the previous one.
