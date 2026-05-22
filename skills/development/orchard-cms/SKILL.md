---
name: orchard-cms
description: |
  USE FOR: Building modular content-managed web applications with Orchard Core. Use when you need a multi-tenant CMS with content types, custom modules, workflows, themes, and a decoupled or headless content API on ASP.NET Core.
  DO NOT USE FOR: Static sites without dynamic content management (use a static site generator), single-page applications that consume third-party headless CMS APIs (use Contentful or Strapi clients), or applications that do not need content authoring workflows (use ASP.NET Core directly).
license: MIT
metadata:
  displayName: Orchard CMS
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Orchard Core Documentation"
    url: "https://docs.orchardcore.net/"
  - title: "Orchard Core GitHub Repository"
    url: "https://github.com/OrchardCMS/OrchardCore"
  - title: "OrchardCore.Application.Cms.Targets NuGet Package"
    url: "https://www.nuget.org/packages/OrchardCore.Application.Cms.Targets"
---

# Orchard CMS

## Overview

Orchard Core is an open-source, modular, multi-tenant content management system and application framework built on ASP.NET Core. It uses a content type system where content is composed from reusable parts (TitlePart, MarkdownBodyPart, AutoroutePart) and fields (TextField, NumericField, MediaField). Orchard Core supports themes for presentation, workflows for automation, GraphQL and REST APIs for headless scenarios, localization, and media management. The module system allows extending Orchard with custom features that participate in dependency injection, migrations, and the request pipeline. Orchard Core runs on .NET 8+ and uses YesSql (a document-based abstraction over relational databases) for storage.

## Application Setup

Configure an Orchard Core CMS application with essential services.

```csharp
using OrchardCore.Logging;

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseNLogHost();

builder.Services
    .AddOrchardCms()
    .AddSetupFeatures("OrchardCore.AutoSetup");

var app = builder.Build();

app.UseStaticFiles();
app.UseOrchardCore();

app.Run();
```

## Content Type Migrations

Define content types and content parts using data migrations.

```csharp
using OrchardCore.ContentManagement.Metadata;
using OrchardCore.ContentManagement.Metadata.Settings;
using OrchardCore.Data.Migration;
using OrchardCore.Recipes.Services;

namespace MyModule;

public class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        await _contentDefinitionManager.AlterTypeDefinitionAsync("BlogPost", type => type
            .Creatable()
            .Listable()
            .Draftable()
            .Versionable()
            .WithPart("TitlePart", part => part.WithPosition("0"))
            .WithPart("AutoroutePart", part => part
                .WithPosition("1")
                .WithSettings(new AutoroutePartSettings
                {
                    Pattern = "{{ ContentItem | display_text | slugify }}",
                    AllowCustomPath = true
                }))
            .WithPart("MarkdownBodyPart", part => part.WithPosition("2"))
            .WithPart("PublishLaterPart", part => part.WithPosition("3"))
            .WithPart("BlogPost", part => part.WithPosition("4")));

        await _contentDefinitionManager.AlterPartDefinitionAsync("BlogPost", part => part
            .WithField("Category", field => field
                .OfType("TaxonomyField")
                .WithDisplayName("Category"))
            .WithField("FeaturedImage", field => field
                .OfType("MediaField")
                .WithDisplayName("Featured Image")
                .WithSettings(new MediaFieldSettings { Multiple = false })));

        return 1;
    }

    public async Task<int> UpdateFrom1Async()
    {
        await _contentDefinitionManager.AlterPartDefinitionAsync("BlogPost", part => part
            .WithField("Tags", field => field
                .OfType("TextField")
                .WithDisplayName("Tags")
                .WithEditor("Tag")));

        return 2;
    }
}
```

## Custom Module with Service and Controller

Create a module with dependency injection, a custom service, and a controller.

```csharp
using Microsoft.Extensions.DependencyInjection;
using OrchardCore.Modules;

namespace MyModule;

public class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IEventService, EventService>();
    }
}

// Services/IEventService.cs
public interface IEventService
{
    Task<IEnumerable<ContentItem>> GetUpcomingEventsAsync(int count);
    Task<ContentItem?> GetEventBySlugAsync(string slug);
}

// Services/EventService.cs
using OrchardCore.ContentManagement;
using YesSql;

public class EventService : IEventService
{
    private readonly ISession _session;
    private readonly IContentManager _contentManager;

    public EventService(ISession session, IContentManager contentManager)
    {
        _session = session;
        _contentManager = contentManager;
    }

    public async Task<IEnumerable<ContentItem>> GetUpcomingEventsAsync(int count)
    {
        return await _session.Query<ContentItem, ContentItemIndex>(x =>
                x.ContentType == "Event" &&
                x.Published &&
                x.Latest)
            .OrderBy(x => x.CreatedUtc)
            .Take(count)
            .ListAsync();
    }

    public async Task<ContentItem?> GetEventBySlugAsync(string slug)
    {
        var contentItem = await _session
            .Query<ContentItem, AutoroutePartIndex>(x => x.Path == slug)
            .FirstOrDefaultAsync();

        return contentItem;
    }
}
```

## Custom Content Part with Handler

Define a content part with a handler that executes logic on content lifecycle events.

```csharp
using OrchardCore.ContentManagement;

namespace MyModule.Models;

public class EventPart : ContentPart
{
    public DateTime EventDate { get; set; }
    public string Location { get; set; } = string.Empty;
    public int MaxAttendees { get; set; }
    public int CurrentAttendees { get; set; }
}

// Handlers/EventPartHandler.cs
using OrchardCore.ContentManagement.Handlers;
using Microsoft.Extensions.Logging;

namespace MyModule.Handlers;

public class EventPartHandler : ContentPartHandler<EventPart>
{
    private readonly ILogger<EventPartHandler> _logger;

    public EventPartHandler(ILogger<EventPartHandler> logger)
    {
        _logger = logger;
    }

    public override Task PublishedAsync(PublishContentContext context, EventPart part)
    {
        if (part.EventDate < DateTime.UtcNow)
        {
            _logger.LogWarning(
                "Event '{Title}' published with a past date: {Date}",
                context.ContentItem.DisplayText,
                part.EventDate);
        }

        return Task.CompletedTask;
    }

    public override Task ValidatingAsync(ValidateContentContext context, EventPart part)
    {
        if (part.MaxAttendees <= 0)
        {
            context.Fail(
                new ValidationError("MaxAttendees must be greater than zero."),
                nameof(EventPart),
                nameof(EventPart.MaxAttendees));
        }

        return Task.CompletedTask;
    }
}
```

## Headless API with Decoupled Content

Expose content via REST endpoints for headless CMS scenarios.

```csharp
using Microsoft.AspNetCore.Mvc;
using OrchardCore.ContentManagement;

namespace MyModule.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ArticlesController : ControllerBase
{
    private readonly IContentManager _contentManager;
    private readonly ISession _session;

    public ArticlesController(
        IContentManager contentManager,
        ISession session)
    {
        _contentManager = contentManager;
        _session = session;
    }

    [HttpGet]
    public async Task<IActionResult> GetArticles(int page = 1, int pageSize = 10)
    {
        var query = _session.Query<ContentItem, ContentItemIndex>(x =>
            x.ContentType == "Article" && x.Published && x.Latest);

        var total = await query.CountAsync();
        var items = await query
            .OrderByDescending(x => x.CreatedUtc)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ListAsync();

        var articles = items.Select(item => new
        {
            item.ContentItemId,
            item.DisplayText,
            item.CreatedUtc,
            Body = item.As<MarkdownBodyPart>()?.Markdown,
            Slug = item.As<AutoroutePart>()?.Path
        });

        return Ok(new { total, page, pageSize, data = articles });
    }

    [HttpGet("{contentItemId}")]
    public async Task<IActionResult> GetArticle(string contentItemId)
    {
        var item = await _contentManager.GetAsync(contentItemId, VersionOptions.Published);
        if (item is null) return NotFound();

        return Ok(new
        {
            item.ContentItemId,
            item.DisplayText,
            item.CreatedUtc,
            Body = item.As<MarkdownBodyPart>()?.Markdown,
            Slug = item.As<AutoroutePart>()?.Path
        });
    }
}
```

## Orchard Core vs Other CMS Platforms

| Feature | Orchard Core | Umbraco | Piranha CMS | WordPress (.NET ports) |
|---|---|---|---|---|
| Framework | ASP.NET Core | ASP.NET Core | ASP.NET Core | PHP (or .NET ports) |
| Multi-tenancy | Built-in | Not built-in | Not built-in | Multisite plugin |
| Content model | Parts + Fields | Document types | Content types | Post types |
| Storage | YesSql (doc-over-SQL) | Entity Framework | Entity Framework | MySQL |
| Module system | Full DI modules | Packages | Not modular | Plugins |
| Headless API | GraphQL + REST | Content Delivery API | REST API | REST API |
| Workflows | Built-in | Forms only | Not built-in | Plugin-based |
| Themes | Liquid + Razor | Razor | Razor | PHP templates |

## Best Practices

1. **Define content types through code migrations (`DataMigration`) rather than through the admin UI** so that content type definitions are version-controlled, reproducible across environments, and deployable through CI/CD pipelines without manual admin steps.

2. **Compose content types from small, reusable content parts** (`TitlePart`, `AutoroutePart`, `MarkdownBodyPart`, custom parts) rather than creating monolithic content types with many fields directly on the type, enabling part reuse across multiple content types and keeping each part's handler focused.

3. **Use `ContentPartHandler<T>` for lifecycle hooks** (Published, Created, Validated) rather than subscribing to generic content events, because typed handlers receive the strongly-typed part and only execute for content items that contain that part, reducing unnecessary processing.

4. **Use `ISession` (YesSql) queries with typed indexes for read operations** and `IContentManager` for create/update/publish operations, because `IContentManager` triggers content handlers and workflows while `ISession` provides efficient read-only querying with index support.

5. **Create custom indexes by implementing `MapIndex<T>` for frequently queried fields** (event dates, product SKUs, author names) rather than deserializing full content items and filtering in memory, because YesSql indexes are stored in relational tables with proper SQL indexes for fast lookups.

6. **Use the Liquid template engine for themes and display templates** instead of Razor where possible, because Liquid templates can be edited by content authors through the admin UI without recompilation, and they sandbox template execution to prevent arbitrary code execution.

7. **Implement recipes (JSON setup recipes) for seeding initial content and configuration** (content types, roles, settings) so that new tenants or fresh installations start with the correct content structure, menu items, and permissions without manual admin configuration.

8. **Use `IContentManager.GetAsync(id, VersionOptions.Published)` for public-facing queries** and `VersionOptions.DraftRequired` for editing workflows, ensuring that published content is served to end users while editors work on draft versions that do not affect the live site until published.

9. **Register custom modules with `Startup : StartupBase` and declare module dependencies in the module manifest** (`Module.cs` or `Manifest.cs`) so that Orchard Core resolves module initialization order correctly and enables/disables features with their dependencies.

10. **Enable the GraphQL module for headless frontends** and define custom GraphQL query types by implementing `ISchemaBuilder` to expose custom content part fields, rather than building custom REST controllers for every content type, because the GraphQL module auto-generates queries for all registered content types with filtering and pagination.
