---
name: orchardcore-seo
description: Skill for configuring SEO in Orchard Core. Covers SeoMetaPart for meta tags and social sharing, sitemap generation and indexing, canonical URLs, robots.txt, structured data with JSON-LD, and SEO-friendly URL patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core SEO - Prompt Templates

## Configure SEO Features

You are an Orchard Core expert. Generate code and configuration for SEO optimization in Orchard Core.

### Guidelines

- The `OrchardCore.Seo` module provides `SeoMetaPart` for managing meta tags, Open Graph, and Twitter Card metadata per content item.
- The `OrchardCore.Sitemaps` module handles XML sitemap generation, sitemap indexes, and custom sitemap sources.
- Attach `SeoMetaPart` to any routable content type that needs meta tag control.
- Use `AutoroutePart` alongside `SeoMetaPart` for SEO-friendly URL patterns.
- Configure canonical URLs to prevent duplicate content penalties.
- Use recipe steps to provision sitemaps, sitemap indexes, and SEO settings across environments.
- Always seal classes.

### Enabling SEO and Sitemap Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Seo",
        "OrchardCore.Sitemaps",
        "OrchardCore.Autoroute"
      ],
      "disable": []
    }
  ]
}
```

## SeoMetaPart Configuration

### Attaching SeoMetaPart to a Content Type via Migration

```csharp
using OrchardCore.ContentManagement.Metadata;
using OrchardCore.ContentManagement.Metadata.Settings;
using OrchardCore.Data.Migration;
using OrchardCore.Seo.Models;

public sealed class SeoMigrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public SeoMigrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentTypeName}}", type => type
            .WithPart("TitlePart", part => part
                .WithPosition("0")
            )
            .WithPart("AutoroutePart", part => part
                .WithPosition("1")
                .WithSettings(new AutoroutePartSettings
                {
                    AllowCustomPath = true,
                    Pattern = "{{ Model.ContentItem | display_text | slugify }}"
                })
            )
            .WithPart("SeoMetaPart", part => part
                .WithPosition("5")
            )
        );

        return 1;
    }
}
```

### Attaching SeoMetaPart via Recipe

```json
{
  "steps": [
    {
      "name": "ContentDefinition",
      "ContentTypes": [
        {
          "Name": "{{ContentTypeName}}",
          "DisplayName": "{{DisplayName}}",
          "Settings": {
            "ContentTypeSettings": {
              "Creatable": true,
              "Listable": true,
              "Draftable": true
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
                  "Pattern": "{{ Model.ContentItem | display_text | slugify }}"
                }
              }
            },
            {
              "PartName": "SeoMetaPart",
              "Name": "SeoMetaPart",
              "Settings": {
                "ContentTypePartSettings": {
                  "Position": "5"
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

### SeoMetaPart Fields

| Field | Description |
|-------|-------------|
| `PageTitle` | Overrides the default `<title>` tag for the page. |
| `MetaDescription` | Sets the `<meta name="description">` tag content. |
| `MetaKeywords` | Sets the `<meta name="keywords">` tag content. |
| `Canonical` | Sets a custom canonical URL (`<link rel="canonical">`). |
| `MetaRobots` | Controls indexing directives (e.g., `noindex`, `nofollow`). |
| `CustomMetaTags` | Allows adding arbitrary custom `<meta>` tags. |
| `OpenGraphType` | Sets the `og:type` value (e.g., `website`, `article`). |
| `OpenGraphTitle` | Sets the `og:title` value. |
| `OpenGraphDescription` | Sets the `og:description` value. |
| `OpenGraphImage` | Sets the `og:image` media path. |
| `TwitterCard` | Sets `twitter:card` type (`summary`, `summary_large_image`). |
| `TwitterTitle` | Sets the `twitter:title` value. |
| `TwitterDescription` | Sets the `twitter:description` value. |
| `TwitterImage` | Sets the `twitter:image` media path. |
| `TwitterCreator` | Sets the `twitter:creator` handle (e.g., `@username`). |
| `TwitterSite` | Sets the `twitter:site` handle. |
| `GoogleSchema` | Stores JSON-LD structured data for the page. |

## Canonical URLs

- When `SeoMetaPart.Canonical` is left empty, Orchard Core automatically uses the URL generated by `AutoroutePart`.
- Set a custom canonical URL only when multiple URLs resolve to the same content (e.g., query string variations, pagination).
- Canonical URLs must be absolute (include scheme and host).

## Social Media Meta Tags

### Open Graph Configuration

Open Graph tags control how content appears when shared on Facebook, LinkedIn, and other platforms. The `SeoMetaPart` editor exposes fields for `og:type`, `og:title`, `og:description`, and `og:image`. If Open Graph fields are left empty, the part falls back to the page title and meta description.

### Twitter Card Configuration

Twitter Card tags define how content appears in Twitter/X post previews. Set the `TwitterCard` field to either `summary` (small thumbnail) or `summary_large_image` (large banner). If Twitter-specific fields are left empty, they fall back to Open Graph values.

## Structured Data with JSON-LD

The `GoogleSchema` field on `SeoMetaPart` accepts raw JSON-LD. This structured data is rendered in a `<script type="application/ld+json">` block in the page head.

### Common Structured Data Pattern

Use the `GoogleSchema` field on a content item to provide structured data:

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{ArticleTitle}}",
  "description": "{{ArticleDescription}}",
  "author": {
    "@type": "Person",
    "name": "{{AuthorName}}"
  },
  "datePublished": "{{PublishedDate}}",
  "dateModified": "{{ModifiedDate}}",
  "image": "{{ImageUrl}}"
}
```

## Robots.txt

Orchard Core does not provide a built-in robots.txt editor. Serve a `robots.txt` file using one of these approaches:

### Static File Approach

Place a `robots.txt` file in the `wwwroot` folder of the web project:

```
User-agent: *
Allow: /
Sitemap: https://{{YourDomain}}/sitemap.xml
```

### Middleware Approach

```csharp
public sealed class RobotsTxtMiddleware
{
    private readonly RequestDelegate _next;

    public RobotsTxtMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        if (context.Request.Path.StartsWithSegments("/robots.txt"))
        {
            context.Response.ContentType = "text/plain";
            var siteUrl = $"{context.Request.Scheme}://{context.Request.Host}";
            await context.Response.WriteAsync(
                $"""
                User-agent: *
                Allow: /
                Sitemap: {siteUrl}/sitemap.xml
                """);
            return;
        }

        await _next(context);
    }
}
```

Register the middleware in `Startup`:

```csharp
public sealed class Startup : StartupBase
{
    public override void Configure(IApplicationBuilder app, IEndpointRouteBuilder routes, IServiceProvider serviceProvider)
    {
        app.UseMiddleware<RobotsTxtMiddleware>();
    }
}
```

## Sitemap Configuration

### Creating a Sitemap via Recipe

```json
{
  "steps": [
    {
      "name": "Sitemaps",
      "Sitemaps": [
        {
          "SitemapId": "{{UniqueSitemapId}}",
          "Name": "{{SitemapName}}",
          "Path": "sitemap.xml",
          "Enabled": true,
          "SitemapSources": [
            {
              "Type": "SitemapSource",
              "ContentTypes": [
                {
                  "ContentTypeName": "{{ContentTypeName}}",
                  "ChangeFrequency": "daily",
                  "Priority": 5
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Sitemap Change Frequency Values

| Value | Description |
|-------|-------------|
| `always` | Content changes on every access. |
| `hourly` | Updated every hour. |
| `daily` | Updated once a day. |
| `weekly` | Updated once a week. |
| `monthly` | Updated once a month. |
| `yearly` | Updated once a year. |
| `never` | Archived content that will not change. |

### Creating a Sitemap Index

A sitemap index aggregates multiple sitemaps into a single entry point:

```json
{
  "steps": [
    {
      "name": "SitemapIndexes",
      "SitemapIndexes": [
        {
          "SitemapIndexId": "{{UniqueIndexId}}",
          "Name": "Sitemap Index",
          "Path": "sitemap.xml",
          "Enabled": true,
          "ContainedSitemapIds": [
            "{{SitemapId1}}",
            "{{SitemapId2}}"
          ]
        }
      ]
    }
  ]
}
```

## SEO-Friendly URL Patterns with AutoroutePart

### Common URL Pattern Templates

| Pattern | Example Output |
|---------|---------------|
| `{{ Model.ContentItem \| display_text \| slugify }}` | `my-blog-post` |
| `blog/{{ Model.ContentItem \| display_text \| slugify }}` | `blog/my-blog-post` |
| `{{ Model.ContentItem.CreatedUtc \| date: '%Y/%m' }}/{{ Model.ContentItem \| display_text \| slugify }}` | `2025/01/my-blog-post` |
| `products/{{ Model.ContentItem.Content.ProductPart.Category.Text \| slugify }}/{{ Model.ContentItem \| display_text \| slugify }}` | `products/electronics/wireless-headphones` |

### Configuring AutoroutePart Settings in Migration

```csharp
using OrchardCore.Autoroute.Models;
using OrchardCore.ContentManagement.Metadata;
using OrchardCore.Data.Migration;

public sealed class AutorouteMigrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public AutorouteMigrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        await _contentDefinitionManager.AlterTypeDefinitionAsync("BlogPost", type => type
            .WithPart("AutoroutePart", part => part
                .WithSettings(new AutoroutePartSettings
                {
                    AllowCustomPath = true,
                    AllowUpdatePath = true,
                    Pattern = "blog/{{ Model.ContentItem | display_text | slugify }}",
                    ShowHomepageOption = true
                })
            )
        );

        return 1;
    }
}
```

## Page Title Customization

The `PageTitle` field in `SeoMetaPart` overrides the browser tab title. When left empty, Orchard Core uses the `TitlePart` display text combined with the site name. The title is rendered using the page title tag helper.

### Overriding Title Format in a Theme

Use the `<page-title>` tag helper in the layout to control the title format:

```html
<page-title separator=" | " site-name="true" position="AfterTitle" />
```

| Attribute | Description |
|-----------|-------------|
| `separator` | Character(s) between page title and site name. |
| `site-name` | Whether to include the site name. |
| `position` | `AfterTitle` appends site name; `BeforeTitle` prepends it. |

## Custom Meta Tags via SeoMetaPart

`SeoMetaPart` supports adding arbitrary meta tags through the `CustomMetaTags` collection. Each entry specifies a `Name`, `Content`, `HttpEquiv`, and `Charset` value.

### Adding Custom Meta Tags in a Content Item Recipe

```json
{
  "steps": [
    {
      "name": "Content",
      "data": [
        {
          "ContentType": "{{ContentTypeName}}",
          "ContentItemId": "{{ContentItemId}}",
          "DisplayText": "{{PageTitle}}",
          "TitlePart": {
            "Title": "{{PageTitle}}"
          },
          "SeoMetaPart": {
            "PageTitle": "{{CustomBrowserTitle}}",
            "MetaDescription": "{{Description}}",
            "MetaKeywords": "{{Keywords}}",
            "Canonical": "https://{{YourDomain}}/{{CanonicalPath}}",
            "MetaRobots": "index, follow",
            "OpenGraphType": "article",
            "OpenGraphTitle": "{{OgTitle}}",
            "OpenGraphDescription": "{{OgDescription}}",
            "OpenGraphImage": {
              "Paths": ["{{OgImagePath}}"]
            },
            "TwitterCard": "summary_large_image",
            "TwitterTitle": "{{TwitterTitle}}",
            "TwitterDescription": "{{TwitterDescription}}",
            "TwitterImage": {
              "Paths": ["{{TwitterImagePath}}"]
            },
            "TwitterCreator": "@{{TwitterHandle}}",
            "TwitterSite": "@{{SiteTwitterHandle}}",
            "GoogleSchema": "{\"@context\":\"https://schema.org\",\"@type\":\"WebPage\",\"name\":\"{{PageTitle}}\"}",
            "CustomMetaTags": [
              {
                "Name": "author",
                "Content": "{{AuthorName}}"
              },
              {
                "Name": "theme-color",
                "Content": "#{{HexColor}}"
              }
            ]
          }
        }
      ]
    }
  ]
}
```
