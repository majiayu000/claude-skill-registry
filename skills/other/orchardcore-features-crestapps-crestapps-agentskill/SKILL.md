---
name: orchardcore-features
description: Explains OrchardCore feature management including enabling and disabling features, programmatic control with IShellFeaturesManager, feature dependencies, conditional service registration, feature event handlers, recipe-based activation, and a catalog of commonly used features organized by category.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# OrchardCore Features

The **OrchardCore.Features** module provides the administrative interface and programmatic APIs for managing features within an Orchard Core application. Features are the fundamental units of functionality — each module exposes one or more features that can be independently enabled or disabled per tenant.

## Enabling the Features Module

The `OrchardCore.Features` feature is typically enabled by default in most Orchard Core setups. It powers the **Configuration → Features** page in the admin dashboard. If it is not enabled, add it through a recipe or enable it programmatically.

## Feature Management from the Admin Dashboard

Navigate to **Configuration → Features** in the admin panel to see a list of all available features. Each entry displays the feature name, description, category, and current state (enabled or disabled). Use the **Enable** or **Disable** buttons to toggle individual features. When enabling a feature that has dependencies, Orchard Core automatically resolves and enables the required dependencies first. Similarly, disabling a feature prompts a warning if other enabled features depend on it.

## Programmatic Feature Control with IShellFeaturesManager

Use `IShellFeaturesManager` to enable or disable features from code. This service is registered in the dependency injection container and provides methods for querying and modifying feature states.

### Querying Feature States

```csharp
public sealed class FeatureStatusChecker
{
    private readonly IShellFeaturesManager _shellFeaturesManager;

    public FeatureStatusChecker(IShellFeaturesManager shellFeaturesManager)
    {
        _shellFeaturesManager = shellFeaturesManager;
    }

    public async Task<bool> IsFeatureEnabledAsync(string featureId)
    {
        var enabledFeatures = await _shellFeaturesManager.GetEnabledFeaturesAsync();

        return enabledFeatures.Any(f => f.Id == featureId);
    }

    public async Task<IEnumerable<string>> GetDisabledFeatureIdsAsync()
    {
        var disabledFeatures = await _shellFeaturesManager.GetDisabledFeaturesAsync();

        return disabledFeatures.Select(f => f.Id);
    }
}
```

### Enabling and Disabling Features

```csharp
public sealed class FeatureToggleService
{
    private readonly IShellFeaturesManager _shellFeaturesManager;

    public FeatureToggleService(IShellFeaturesManager shellFeaturesManager)
    {
        _shellFeaturesManager = shellFeaturesManager;
    }

    public async Task EnableFeaturesAsync(IEnumerable<IFeatureInfo> features, bool force = false)
    {
        // The force parameter controls whether to bypass dependency validation.
        await _shellFeaturesManager.EnableFeaturesAsync(features, force);
    }

    public async Task DisableFeaturesAsync(IEnumerable<IFeatureInfo> features, bool force = false)
    {
        // The force parameter controls whether to disable even if dependents exist.
        await _shellFeaturesManager.DisableFeaturesAsync(features, force);
    }
}
```

### Retrieving Available Features

```csharp
public sealed class FeatureCatalogService
{
    private readonly IShellFeaturesManager _shellFeaturesManager;

    public FeatureCatalogService(IShellFeaturesManager shellFeaturesManager)
    {
        _shellFeaturesManager = shellFeaturesManager;
    }

    public async Task<IEnumerable<IFeatureInfo>> GetAvailableFeaturesAsync()
    {
        return await _shellFeaturesManager.GetAvailableFeaturesAsync();
    }
}
```

## Feature Dependencies and Dependency Resolution

Features can declare dependencies on other features in the module manifest (`Manifest.cs`). When a feature is enabled, Orchard Core walks the dependency graph and enables all required features in the correct order.

```csharp
[assembly: Feature(
    id: "MyModule.Reporting",
    name: "Reporting",
    description: "Provides reporting dashboards.",
    category: "Content",
    dependencies:
    [
        "OrchardCore.Contents",
        "OrchardCore.Queries"
    ]
)]
```

In this example, enabling `MyModule.Reporting` automatically enables `OrchardCore.Contents` and `OrchardCore.Queries` if they are not already enabled. Circular dependencies are not permitted and result in a startup error.

## Conditional Service Registration with RequireFeatures

The `[RequireFeatures]` attribute restricts a `Startup` class so that its services are only registered when the specified features are enabled. This is useful for optional integrations between modules.

```csharp
[RequireFeatures("OrchardCore.Search.Lucene")]
public sealed class LuceneIntegrationStartup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        // These services are only registered when OrchardCore.Search.Lucene is enabled.
        services.AddScoped<ILuceneQueryProvider, CustomLuceneQueryProvider>();
    }
}
```

You can specify multiple features. All listed features must be enabled for the `Startup` class to activate:

```csharp
[RequireFeatures("OrchardCore.Contents", "OrchardCore.Workflows")]
public sealed class ContentWorkflowStartup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IWorkflowTask, PublishContentTask>();
    }
}
```

## Feature Event Handlers

Implement `IFeatureEventHandler` to execute custom logic when features are enabled or disabled. This is useful for running data migrations, seeding initial data, or performing cleanup.

```csharp
public sealed class SampleFeatureEventHandler : IFeatureEventHandler
{
    private readonly ILogger<SampleFeatureEventHandler> _logger;

    public SampleFeatureEventHandler(ILogger<SampleFeatureEventHandler> logger)
    {
        _logger = logger;
    }

    public Task EnablingAsync(IFeatureInfo feature)
    {
        // Runs before the feature is enabled.
        return Task.CompletedTask;
    }

    public Task EnabledAsync(IFeatureInfo feature)
    {
        _logger.LogInformation("Feature '{FeatureId}' has been enabled.", feature.Id);

        return Task.CompletedTask;
    }

    public Task DisablingAsync(IFeatureInfo feature)
    {
        // Runs before the feature is disabled.
        return Task.CompletedTask;
    }

    public Task DisabledAsync(IFeatureInfo feature)
    {
        _logger.LogInformation("Feature '{FeatureId}' has been disabled.", feature.Id);

        return Task.CompletedTask;
    }

    public Task InstallingAsync(IFeatureInfo feature)
    {
        // Runs before a feature is installed for the first time.
        return Task.CompletedTask;
    }

    public Task InstalledAsync(IFeatureInfo feature)
    {
        _logger.LogInformation("Feature '{FeatureId}' has been installed.", feature.Id);

        return Task.CompletedTask;
    }

    public Task UninstallingAsync(IFeatureInfo feature)
    {
        return Task.CompletedTask;
    }

    public Task UninstalledAsync(IFeatureInfo feature)
    {
        return Task.CompletedTask;
    }
}
```

Register the event handler in your module's `Startup` class:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IFeatureEventHandler, SampleFeatureEventHandler>();
    }
}
```

## Enabling Features via Recipes

Use the `feature` recipe step to enable or disable features as part of a site setup recipe or a standalone recipe.

### Enabling Features

```json
{
  "steps": [
    {
      "name": "feature",
      "enable": [
        "OrchardCore.Contents",
        "OrchardCore.ContentTypes",
        "OrchardCore.Title",
        "OrchardCore.Media",
        "OrchardCore.Users",
        "OrchardCore.Roles"
      ]
    }
  ]
}
```

### Disabling Features

```json
{
  "steps": [
    {
      "name": "feature",
      "disable": [
        "OrchardCore.Search.Lucene"
      ]
    }
  ]
}
```

### Enabling and Disabling in a Single Step

```json
{
  "steps": [
    {
      "name": "feature",
      "enable": [
        "OrchardCore.Search.Elasticsearch"
      ],
      "disable": [
        "OrchardCore.Search.Lucene"
      ]
    }
  ]
}
```

## Feature Guards and Always-On Features

Some features are marked as **always enabled** and cannot be disabled. These are foundational features that the system depends on (e.g., `OrchardCore.Settings`). This is declared in the manifest:

```csharp
[assembly: Feature(
    id: "OrchardCore.Settings",
    name: "Settings",
    description: "Provides site-level settings.",
    isAlwaysEnabled: true
)]
```

Custom modules can also declare features as always-on if they provide critical infrastructure that should never be turned off.

A **feature guard** is a pattern where you check at runtime whether a feature is enabled before executing logic:

```csharp
public sealed class ConditionalContentHandler : ContentHandlerBase
{
    private readonly IShellFeaturesManager _shellFeaturesManager;

    public ConditionalContentHandler(IShellFeaturesManager shellFeaturesManager)
    {
        _shellFeaturesManager = shellFeaturesManager;
    }

    public override async Task PublishedAsync(PublishContentContext context)
    {
        var enabledFeatures = await _shellFeaturesManager.GetEnabledFeaturesAsync();

        if (!enabledFeatures.Any(f => f.Id == "OrchardCore.Notifications"))
        {
            return;
        }

        // Perform notification logic only when OrchardCore.Notifications is enabled.
    }
}
```

However, the preferred approach is to use `[RequireFeatures]` on a `Startup` class rather than runtime guards, as it avoids unnecessary service resolution.

## Listing Available Features per Tenant

Each tenant in a multi-tenant Orchard Core application has its own set of enabled features. Use the admin dashboard or `IShellFeaturesManager` to inspect the feature state for the current tenant.

```csharp
public sealed class TenantFeatureReporter
{
    private readonly IShellFeaturesManager _shellFeaturesManager;
    private readonly ShellSettings _shellSettings;

    public TenantFeatureReporter(
        IShellFeaturesManager shellFeaturesManager,
        ShellSettings shellSettings)
    {
        _shellFeaturesManager = shellFeaturesManager;
        _shellSettings = shellSettings;
    }

    public async Task<TenantFeatureSummary> GetSummaryAsync()
    {
        var enabled = await _shellFeaturesManager.GetEnabledFeaturesAsync();
        var disabled = await _shellFeaturesManager.GetDisabledFeaturesAsync();

        return new TenantFeatureSummary
        {
            TenantName = _shellSettings.Name,
            EnabledCount = enabled.Count(),
            DisabledCount = disabled.Count(),
            EnabledFeatureIds = enabled.Select(f => f.Id).OrderBy(id => id),
            DisabledFeatureIds = disabled.Select(f => f.Id).OrderBy(id => id),
        };
    }
}

public sealed class TenantFeatureSummary
{
    public string TenantName { get; set; }
    public int EnabledCount { get; set; }
    public int DisabledCount { get; set; }
    public IEnumerable<string> EnabledFeatureIds { get; set; }
    public IEnumerable<string> DisabledFeatureIds { get; set; }
}
```

## Feature Catalog

Below is a catalog of commonly used OrchardCore features organized by category. Enable these feature IDs via the admin dashboard, recipes, or `IShellFeaturesManager`.

### Content Management

| Feature ID | Description |
|---|---|
| `OrchardCore.Contents` | Core content management system for creating, editing, publishing, and versioning content items. |
| `OrchardCore.ContentTypes` | Admin UI for defining and editing content type definitions, parts, and fields. |
| `OrchardCore.Title` | Adds a title part to content items. |
| `OrchardCore.Alias` | Provides an alias part for assigning URL-friendly identifiers to content items. |
| `OrchardCore.Autoroute` | Automatically generates URL routes for content items based on configurable patterns. |
| `OrchardCore.Html` | Adds an HTML body part for rich-text content editing. |
| `OrchardCore.Markdown` | Adds a Markdown body part for Markdown-based content editing. |
| `OrchardCore.Lists` | Enables list functionality for organizing content items in ordered collections. |
| `OrchardCore.Taxonomies` | Provides taxonomy management for categorizing content with hierarchical terms. |
| `OrchardCore.Flows` | Allows building content layouts using a flow of widgets and content items. |
| `OrchardCore.ContentFields` | Adds a library of reusable fields (text, numeric, boolean, date, link, etc.) to content types. |
| `OrchardCore.ContentLocalization` | Enables localization of content items into multiple cultures. |
| `OrchardCore.Indexing` | Provides content indexing infrastructure used by search modules. |
| `OrchardCore.PublishLater` | Allows scheduling content items for future publication. |

### Media

| Feature ID | Description |
|---|---|
| `OrchardCore.Media` | Core media management for uploading, organizing, and serving media files. |
| `OrchardCore.MediaLibrary` | Provides a media library UI for browsing and selecting media assets. |
| `OrchardCore.Media.Indexing` | Enables indexing of media file metadata for search. |

### Navigation

| Feature ID | Description |
|---|---|
| `OrchardCore.Menu` | Provides menu content types and rendering for site navigation. |
| `OrchardCore.Navigation` | Core navigation infrastructure for building and managing navigation menus. |
| `OrchardCore.Sitemaps` | Generates XML sitemaps for search engine optimization. |

### Security and Users

| Feature ID | Description |
|---|---|
| `OrchardCore.Users` | User registration, authentication, and profile management. |
| `OrchardCore.Roles` | Role-based authorization and role management. |
| `OrchardCore.OpenId` | OpenID Connect server and client support for authentication. |
| `OrchardCore.Users.TwoFactorAuthentication` | Adds two-factor authentication support for user accounts. |

### Search

| Feature ID | Description |
|---|---|
| `OrchardCore.Search` | Core search infrastructure providing a unified search API. |
| `OrchardCore.Search.Lucene` | Full-text search powered by Lucene.NET. |
| `OrchardCore.Search.Elasticsearch` | Full-text search powered by Elasticsearch. |
| `OrchardCore.Queries` | Query engine for defining and executing named queries. |

### Workflows

| Feature ID | Description |
|---|---|
| `OrchardCore.Workflows` | Visual workflow engine for automating processes with activities and events. |
| `OrchardCore.Workflows.Http` | Adds HTTP request and response activities to workflows. |
| `OrchardCore.Workflows.Timers` | Adds timer-based triggers for scheduling workflow execution. |

### Email and Notifications

| Feature ID | Description |
|---|---|
| `OrchardCore.Email` | Core email sending infrastructure with SMTP support. |
| `OrchardCore.Notifications` | In-app notification system for delivering messages to users. |

### Theming and Display

| Feature ID | Description |
|---|---|
| `OrchardCore.Themes` | Theme management for selecting and configuring site themes. |
| `OrchardCore.Templates` | Liquid template overrides for customizing shape rendering. |
| `OrchardCore.Layers` | Conditional widget layer rules for displaying content in zones based on conditions. |
| `OrchardCore.Widgets` | Widget content types for placing content in layout zones. |

### Localization

| Feature ID | Description |
|---|---|
| `OrchardCore.Localization` | Provides localization infrastructure for translating the admin UI and front-end. |
| `OrchardCore.ContentLocalization` | Enables localization of content items into multiple cultures. |

### Infrastructure

| Feature ID | Description |
|---|---|
| `OrchardCore.Settings` | Site-level settings management (always enabled). |
| `OrchardCore.Recipes` | Recipe infrastructure for importing and exporting site configuration. |
| `OrchardCore.Tenants` | Multi-tenancy support for running isolated sites from a single application. |
| `OrchardCore.BackgroundTasks` | Background task scheduling and execution. |
| `OrchardCore.Scripting` | Scripting engine for executing dynamic expressions in recipes and workflows. |
| `OrchardCore.DynamicCache` | Shape-level output caching for improved rendering performance. |
| `OrchardCore.ResponseCompression` | Enables HTTP response compression (Gzip, Brotli). |
| `OrchardCore.HealthChecks` | ASP.NET Core health check endpoints for monitoring application status. |

### Data and Queries

| Feature ID | Description |
|---|---|
| `OrchardCore.Queries` | Query engine for defining reusable named queries. |
| `OrchardCore.Queries.Sql` | SQL-based query provider for running SQL queries against the database. |
| `OrchardCore.GraphQL` | GraphQL API endpoint for querying content and site data. |
| `OrchardCore.Apis.GraphQL` | Exposes a GraphQL API for content and resource queries. |

### SEO and Social

| Feature ID | Description |
|---|---|
| `OrchardCore.Seo` | SEO meta tags and canonical URL management. |
| `OrchardCore.Sitemaps` | XML sitemap generation for search engines. |
| `OrchardCore.ReCaptcha` | Google reCAPTCHA integration for form protection. |
