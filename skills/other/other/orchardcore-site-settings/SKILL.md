---
name: orchardcore-site-settings
description: Skill for accessing and extending Orchard Core site-level configuration. Covers ISiteService, custom settings sections with the CustomSettings stereotype, SiteSettingsDisplayDriver pattern, admin navigation registration, and recipe-based configuration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Site Settings - Prompt Templates

## Access and Extend Site Settings

You are an Orchard Core expert. Generate code and configuration for working with site-level settings, creating custom settings sections, and rendering them in the admin dashboard.

### Guidelines

- Use `ISiteService` to read and write site-level configuration at runtime.
- `ISite` is the read-only representation of the site document; obtain it via `ISiteService.GetSiteSettingsAsync()`.
- Built-in site properties include `SiteName`, `BaseUrl`, `TimeZoneId`, `Culture`, `PageSize`, and `UseCdn`.
- Custom settings sections are content types with the `CustomSettings` stereotype.
- Each custom settings section is stored as a named JSON property inside the site document.
- Use `ISite.As<TSettings>()` to read a custom settings section and `ISite.Properties[typeName]` for raw access.
- Render custom settings in admin using `DisplayDriver<ISite>` (not `ContentPartDisplayDriver`).
- Register an `INavigationProvider` to add settings entries to the admin navigation menu.
- Define a dedicated permission to control who can manage each settings section.
- All C# classes must use the `sealed` modifier.
- All recipe JSON must be wrapped in the root `{ "steps": [...] }` format.

### Core Services

| Service | Purpose |
|---------|---------|
| `ISiteService` | Read and write the site settings document. Returns `ISite`. |
| `ISite` | Read-only site settings object. Use `.As<T>()` to access custom sections. |
| `IContentDefinitionManager` | Define custom settings content types with the `CustomSettings` stereotype. |
| `DisplayDriver<ISite>` | Base class for rendering site settings sections in admin. |
| `INavigationProvider` | Register admin menu entries for settings pages. |

### Built-In Site Properties

| Property | Type | Description |
|----------|------|-------------|
| `SiteName` | `string` | Display name of the site. |
| `BaseUrl` | `string` | Root URL used for absolute link generation. |
| `TimeZoneId` | `string` | IANA time zone identifier (e.g., `America/New_York`). |
| `Culture` | `string` | Default culture code (e.g., `en-US`). |
| `PageSize` | `int` | Default number of items per page in lists. |
| `UseCdn` | `bool` | Whether to serve static resources from a CDN. |

### Reading Site Settings

```csharp
public sealed class MyService
{
    private readonly ISiteService _siteService;

    public MyService(ISiteService siteService)
    {
        _siteService = siteService;
    }

    public async Task<string> GetSiteNameAsync()
    {
        var site = await _siteService.GetSiteSettingsAsync();

        return site.SiteName;
    }
}
```

### Updating Site Settings

```csharp
public sealed class MyService
{
    private readonly ISiteService _siteService;

    public MyService(ISiteService siteService)
    {
        _siteService = siteService;
    }

    public async Task UpdateBaseUrlAsync(string newBaseUrl)
    {
        var site = await _siteService.LoadSiteSettingsAsync();
        site.BaseUrl = newBaseUrl;
        await _siteService.UpdateSiteSettingsAsync(site);
    }
}
```

Use `LoadSiteSettingsAsync()` when you intend to modify the site document. Use `GetSiteSettingsAsync()` for read-only access; it returns a cached instance.

### Creating a Custom Settings Section

#### Step 1: Define a Content Part for the Settings

```csharp
public sealed class {{SettingsPartName}} : ContentPart
{
    public string {{PropertyName}} { get; set; }

    public bool {{BoolPropertyName}} { get; set; }
}
```

#### Step 2: Register the Content Type with the CustomSettings Stereotype

```csharp
public sealed class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        await _contentDefinitionManager.AlterTypeDefinitionAsync("{{SettingsTypeName}}", type => type
            .DisplayedAs("{{Settings Display Name}}")
            .Stereotype("CustomSettings")
            .WithPart("{{SettingsPartName}}", part => part
                .WithPosition("0")
            )
        );

        return 1;
    }
}
```

The `CustomSettings` stereotype tells Orchard Core this content type represents a site settings section rather than a regular content item.

#### Step 3: Create the Display Driver

The display driver inherits from `DisplayDriver<ISite>`, not from `ContentPartDisplayDriver<T>`.

```csharp
public sealed class {{SettingsPartName}}DisplayDriver : DisplayDriver<ISite>
{
    private readonly IHttpContextAccessor _httpContextAccessor;
    private readonly IAuthorizationService _authorizationService;

    public {{SettingsPartName}}DisplayDriver(
        IHttpContextAccessor httpContextAccessor,
        IAuthorizationService authorizationService)
    {
        _httpContextAccessor = httpContextAccessor;
        _authorizationService = authorizationService;
    }

    public override IDisplayResult Edit(ISite model, BuildEditorContext context)
    {
        var user = _httpContextAccessor.HttpContext?.User;

        if (!await _authorizationService.AuthorizeAsync(user, Permissions.Manage{{SettingsPartName}}))
        {
            return null;
        }

        return Initialize<{{SettingsPartName}}ViewModel>("{{SettingsPartName}}_Edit", viewModel =>
        {
            var settings = model.As<{{SettingsPartName}}>();

            viewModel.{{PropertyName}} = settings.{{PropertyName}};
            viewModel.{{BoolPropertyName}} = settings.{{BoolPropertyName}};
        }).Location("Content:5")
        .OnGroup("{{settingsGroupId}}");
    }

    public override async Task<IDisplayResult> UpdateAsync(ISite model, UpdateEditorContext context)
    {
        var user = _httpContextAccessor.HttpContext?.User;

        if (!await _authorizationService.AuthorizeAsync(user, Permissions.Manage{{SettingsPartName}}))
        {
            return null;
        }

        if (context.GroupId == "{{settingsGroupId}}")
        {
            var viewModel = new {{SettingsPartName}}ViewModel();

            await context.Updater.TryUpdateModelAsync(viewModel, Prefix);

            model.Put(new {{SettingsPartName}}
            {
                {{PropertyName}} = viewModel.{{PropertyName}},
                {{BoolPropertyName}} = viewModel.{{BoolPropertyName}},
            });
        }

        return await EditAsync(model, context);
    }
}
```

Important: The `OnGroup()` call ties the editor shape to a specific group identifier. This must match the group used in the admin controller and navigation entry.

#### Step 4: Create the View Model

```csharp
public class {{SettingsPartName}}ViewModel
{
    public string {{PropertyName}} { get; set; }

    public bool {{BoolPropertyName}} { get; set; }
}
```

#### Step 5: Create the Razor View

Create a view at `Views/{{SettingsPartName}}_Edit.cshtml`:

```html
@model {{SettingsPartName}}ViewModel

<div class="mb-3">
    <label asp-for="{{PropertyName}}" class="form-label">{{Property Display Name}}</label>
    <input asp-for="{{PropertyName}}" class="form-control" />
    <span asp-validation-for="{{PropertyName}}"></span>
</div>

<div class="mb-3">
    <div class="form-check">
        <input asp-for="{{BoolPropertyName}}" class="form-check-input" />
        <label asp-for="{{BoolPropertyName}}" class="form-check-label">{{Bool Display Name}}</label>
    </div>
</div>
```

#### Step 6: Register Admin Navigation

```csharp
public sealed class AdminMenu : INavigationProvider
{
    internal readonly IStringLocalizer S;

    public AdminMenu(IStringLocalizer<AdminMenu> localizer)
    {
        S = localizer;
    }

    public Task BuildNavigationAsync(string name, NavigationBuilder builder)
    {
        if (!NavigationHelper.IsAdminMenu(name))
        {
            return Task.CompletedTask;
        }

        builder
            .Add(S["Settings"], settings => settings
                .Add(S["{{Settings Display Name}}"], S["{{Settings Display Name}}"].PrefixPosition(), entry => entry
                    .AddClass("{{iconCssClass}}")
                    .Id("{{settingsMenuId}}")
                    .Permission(Permissions.Manage{{SettingsPartName}})
                    .Action("Index", "Admin", new { area = "OrchardCore.Settings", groupId = "{{settingsGroupId}}" })
                    .LocalNav()
                )
            );

        return Task.CompletedTask;
    }
}
```

The `groupId` route value must match the group used in the display driver's `OnGroup()` call. The `OrchardCore.Settings` area provides the built-in admin controller that handles rendering settings groups.

> **Note**: Settings pages are registered directly under the `"Settings"` top-level menu group. The `"Configuration"` menu group is no longer used in Orchard Core.

#### Step 7: Register Services in Startup

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddContentPart<{{SettingsPartName}}>();
        services.AddScoped<IDisplayDriver<ISite>, {{SettingsPartName}}DisplayDriver>();
        services.AddScoped<INavigationProvider, AdminMenu>();
        services.AddScoped<IPermissionProvider, Permissions>();
    }
}
```

### Reading Custom Settings in Views

Use the `ISite` object available through `ISiteService` or the `Orchard` helper in Liquid templates:

```html
@inject ISiteService SiteService

@{
    var site = await SiteService.GetSiteSettingsAsync();
    var settings = site.As<{{SettingsPartName}}>();
}

<p>@settings.{{PropertyName}}</p>
```

### Reading Custom Settings in Services

```csharp
public sealed class MyService
{
    private readonly ISiteService _siteService;

    public MyService(ISiteService siteService)
    {
        _siteService = siteService;
    }

    public async Task<{{SettingsPartName}}> GetSettingsAsync()
    {
        var site = await _siteService.GetSiteSettingsAsync();

        return site.As<{{SettingsPartName}}>();
    }
}
```

### Configuring Site Settings via Recipes

Use the `Settings` recipe step to configure built-in site properties:

```json
{
    "steps": [
        {
            "name": "Settings",
            "SiteName": "My Orchard Core Site",
            "BaseUrl": "https://www.example.com",
            "TimeZoneId": "America/New_York",
            "Culture": "en-US",
            "PageSize": 10,
            "UseCdn": true
        }
    ]
}
```

### Configuring Custom Settings via Recipes

Use the `custom-settings` recipe step to set values for a custom settings section:

```json
{
    "steps": [
        {
            "name": "custom-settings",
            "{{SettingsTypeName}}": {
                "ContentItemId": "[js:uuid()]",
                "ContentType": "{{SettingsTypeName}}",
                "{{SettingsPartName}}": {
                    "{{PropertyName}}": "{{value}}",
                    "{{BoolPropertyName}}": true
                }
            }
        }
    ]
}
```

### Adding Content Fields to Custom Settings

Custom settings parts can include content fields for richer configuration:

```csharp
public sealed class Migrations : DataMigration
{
    private readonly IContentDefinitionManager _contentDefinitionManager;

    public Migrations(IContentDefinitionManager contentDefinitionManager)
    {
        _contentDefinitionManager = contentDefinitionManager;
    }

    public async Task<int> CreateAsync()
    {
        await _contentDefinitionManager.AlterTypeDefinitionAsync("{{SettingsTypeName}}", type => type
            .DisplayedAs("{{Settings Display Name}}")
            .Stereotype("CustomSettings")
            .WithPart("{{SettingsPartName}}", part => part
                .WithPosition("0")
            )
        );

        await _contentDefinitionManager.AlterPartDefinitionAsync("{{SettingsPartName}}", part => part
            .WithField("Logo", field => field
                .OfType("MediaField")
                .WithDisplayName("Site Logo")
                .WithPosition("0")
            )
            .WithField("FooterText", field => field
                .OfType("HtmlField")
                .WithDisplayName("Footer Text")
                .WithPosition("1")
                .WithEditor("Wysiwyg")
            )
            .WithField("SocialLink", field => field
                .OfType("LinkField")
                .WithDisplayName("Social Media Link")
                .WithPosition("2")
            )
        );

        return 1;
    }
}
```

When using content fields in custom settings, the fields are rendered automatically by the content field display drivers. You do not need to handle them manually in the site settings display driver.
