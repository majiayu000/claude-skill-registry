---
name: orchardcore-admin
description: Guidance for working with the Orchard Core admin panel, including admin controllers, menu registration, dashboard widgets, admin theme customization, settings pages, and admin-specific shapes and zones.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Admin Panel

The Orchard Core admin panel is the back-office interface used for content management, site configuration, and administrative tasks. It is rendered using the **TheAdmin** theme, which provides a dedicated layout, navigation structure, and styling separate from the front-end site.

## TheAdmin Theme

TheAdmin is the built-in administration theme that ships with Orchard Core. It defines the admin layout, sidebar navigation, header bar, and all administrative UI chrome. The theme is automatically activated for any request routed through the admin pipeline.

Key characteristics:

- Provides the `Layout` shape with admin-specific zones such as `Navigation`, `Content`, `Header`, `Footer`, `Messages`, and `DetailAdmin`.
- Uses Bootstrap-based styling with Orchard Core admin CSS.
- Supports customization through shape overrides, zone manipulation, and theme inheritance.

## Admin Controllers

To create a controller that renders inside the admin panel, apply the `[Admin]` attribute to the controller class or individual action methods. This attribute routes the action through the admin theme and enforces authentication.

```csharp
using Microsoft.AspNetCore.Mvc;
using OrchardCore.Admin;
using OrchardCore.DisplayManagement.Notify;

[Admin("MyModule/Settings/{action}", "MyModule.Settings")]
public sealed class SettingsController : Controller
{
    private readonly INotifier _notifier;

    public SettingsController(INotifier notifier)
    {
        _notifier = notifier;
    }

    public IActionResult Index()
    {
        return View();
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Update()
    {
        await _notifier.SuccessAsync(new LocalizedHtmlString("Settings updated."));
        return RedirectToAction(nameof(Index));
    }
}
```

The `[Admin]` attribute accepts two optional parameters:

1. **Route template** — defines the admin URL pattern for the controller (e.g., `"MyModule/Settings/{action}"`).
2. **Route name** — assigns a named route for URL generation (e.g., `"MyModule.Settings"`).

When applied at the class level, all actions in the controller are treated as admin actions. You can also apply it to individual actions if only some methods should be admin-scoped.

### Admin Route URL Generation

Use the named route to generate admin URLs:

```csharp
var url = Url.RouteUrl("MyModule.Settings", new { action = "Index" });
```

## Admin Menu Registration

Admin menu items are registered by implementing the `INavigationProvider` interface. Each provider contributes entries to the admin sidebar navigation.

```csharp
using Microsoft.Extensions.Localization;
using OrchardCore.Navigation;

public sealed class AdminMenu : INavigationProvider
{
    private readonly IStringLocalizer S;

    public AdminMenu(IStringLocalizer<AdminMenu> localizer)
    {
        S = localizer;
    }

    public ValueTask BuildNavigationAsync(string name, NavigationBuilder builder)
    {
        if (!NavigationHelper.IsAdminMenu(name))
        {
            return ValueTask.CompletedTask;
        }

        builder
            .Add(S["Content Management"], content => content
                .AddClass("content-management")
                .Id("contentmanagement")
                .Add(S["Taxonomies"], S["Taxonomies"].PrefixPosition(), taxonomies => taxonomies
                    .Permission(Permissions.ManageTaxonomies)
                    .Action("Index", "Admin", new { area = "MyModule" })
                    .LocalNav()
                )
            );

        return ValueTask.CompletedTask;
    }
}
```

Register the provider in `Startup.cs`:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddNavigationProvider<AdminMenu>();
    }
}
```

### Menu Grouping and Ordering

Menu items are organized hierarchically using nested `Add` calls. Use the `Position` method to control item order within a group. Position values are strings that support numeric sorting (e.g., `"1"`, `"2.5"`, `"10"`).

The Orchard Core admin sidebar uses these top-level groups:

| Group | Purpose |
|-------|---------|
| `Content Management` | Content items, taxonomies, media |
| `Settings` | Site settings and configuration pages |
| `Tools` | Non-settings admin utilities (cache, import/export) |
| `Access Control` | Users, Roles, and permissions |

```csharp
builder
    .Add(S["Settings"], settings => settings
        .Add(S["Email"], email => email
            .Action("Index", "Admin", new { area = "OrchardCore.Email" })
            .Permission(Permissions.ManageEmailSettings)
            .LocalNav()
        )
        .Add(S["Search"], search => search
            .Action("Index", "Admin", new { area = "OrchardCore.Search" })
            .Permission(Permissions.ManageSearchSettings)
            .LocalNav()
        )
    );
```

> **Important**: Orchard Core no longer uses the `"Configuration"` or `"Security"` top-level menu groups. Use `"Settings"` for settings pages, `"Tools"` for non-settings utilities, and `"Access Control"` for user/role management.

### Permission-Based Menu Visibility

Use the `Permission` method to restrict menu item visibility. Items are automatically hidden from users who lack the specified permission. You can chain multiple `Permission` calls if any one of several permissions should grant visibility.

```csharp
builder
    .Add(S["Access Control"], accessControl => accessControl
        .Add(S["Users"], users => users
            .Permission(Permissions.ManageUsers)
            .Action("Index", "Admin", new { area = "OrchardCore.Users" })
            .LocalNav()
        )
        .Add(S["Roles"], roles => roles
            .Permission(Permissions.ManageRoles)
            .Action("Index", "Admin", new { area = "OrchardCore.Roles" })
            .LocalNav()
        )
    );
```

## Admin Views and Layouts

Admin views are standard Razor views placed in the `Views` folder of your module. When rendered through an admin controller, they automatically use the admin layout provided by TheAdmin theme.

To create an admin view at `Views/Settings/Index.cshtml`:

```html
<zone Name="Title">
    <h1>@T["My Module Settings"]</h1>
</zone>

<form asp-action="Update" method="post">
    <div class="mb-3">
        <label asp-for="DisplayName" class="form-label">@T["Display Name"]</label>
        <input asp-for="DisplayName" class="form-control" />
    </div>

    <div class="mb-3">
        <button type="submit" class="btn btn-primary">@T["Save"]</button>
    </div>
</form>
```

### Admin Zones

The admin layout defines several zones for placing content:

| Zone | Purpose |
|------|---------|
| `Title` | Page title displayed at the top of the content area |
| `Content` | Main body content |
| `Navigation` | Sidebar navigation menu |
| `Header` | Top bar area (user menu, site name) |
| `Messages` | Notification and alert messages |
| `DetailAdmin` | Secondary detail panel |
| `Footer` | Bottom area of the admin layout |
| `HeadMeta` | Additional `<meta>` tags in `<head>` |

Use the `<zone>` tag helper to inject content into these zones from any admin view:

```html
<zone Name="Messages">
    <div class="alert alert-info">@T["Remember to publish your changes."]</div>
</zone>
```

## Dashboard Widgets

Dashboard widgets appear on the admin dashboard landing page. To create a dashboard widget, implement a shape and register it with the dashboard zone.

### Creating a Dashboard Widget Shape

First, define a display driver for the widget:

```csharp
using OrchardCore.DisplayManagement.Handlers;
using OrchardCore.DisplayManagement.Views;
using OrchardCore.Admin;

public sealed class RecentActivityWidgetDisplayDriver : DisplayDriver<DashboardCard>
{
    public override IDisplayResult Display(DashboardCard model, BuildDisplayContext context)
    {
        return View("RecentActivityWidget", model)
            .Location("DetailAdmin", "Content:5");
    }
}
```

Register the driver in `Startup.cs`:

```csharp
services.AddDisplayDriver<DashboardCard, RecentActivityWidgetDisplayDriver>();
```

### Dashboard Widget View

Create `Views/RecentActivityWidget.cshtml`:

```html
<div class="card mb-3">
    <div class="card-header">
        <h5 class="card-title mb-0">@T["Recent Activity"]</h5>
    </div>
    <div class="card-body">
        <ul class="list-unstyled mb-0">
            <li>@T["3 content items published today"]</li>
            <li>@T["12 new users this week"]</li>
        </ul>
    </div>
</div>
```

## Admin Theme Customization and Branding

You can customize the admin theme by creating a theme that inherits from TheAdmin, overriding specific shapes, or injecting custom resources.

### Overriding the Admin Branding

Create a shape override for the admin header branding by defining a `Header.cshtml` shape in your module or custom admin theme:

```html
<header class="ta-navbar">
    <div class="d-flex align-items-center">
        <a class="ta-navbar-brand" href="~/admin">
            <img src="~/MyTheme/images/custom-logo.svg" alt="@T["Site Administration"]" height="32" />
        </a>
    </div>
</header>
```

### Injecting Custom Admin Styles

Use a resource manifest to add custom CSS to the admin panel:

```csharp
using OrchardCore.ResourceManagement;

public sealed class ResourceManifest : IResourceManifestProvider
{
    public void BuildManifests(IResourceManifestBuilder builder)
    {
        var manifest = builder.Add();

        manifest
            .DefineStyle("MyModule.AdminStyles")
            .SetUrl("~/MyModule/css/admin-custom.min.css", "~/MyModule/css/admin-custom.css");
    }
}
```

Then register a resource filter to include the styles on admin pages:

```csharp
using OrchardCore.ResourceManagement;

[RequireFeatures("OrchardCore.Admin")]
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddResourceConfiguration<AdminResourceFilter>();
    }
}

public sealed class AdminResourceFilter : IResourceFilterProvider
{
    public void AddResourceFilter(ResourceFilterBuilder builder)
    {
        builder
            .WhenAdmin()
            .IncludeStyle("MyModule.AdminStyles");
    }
}
```

## Admin Settings Pages

Admin settings pages allow module authors to expose configurable options in the admin panel. The recommended pattern uses `ISiteService` to persist settings as part of the site configuration document.

### Defining a Settings Model

```csharp
public sealed class NotificationSettings
{
    public bool EnableEmailNotifications { get; set; }

    public string DefaultRecipient { get; set; }

    public int MaxRetryAttempts { get; set; } = 3;
}
```

### Creating a Settings Display Driver

```csharp
using OrchardCore.DisplayManagement.Handlers;
using OrchardCore.DisplayManagement.Views;
using OrchardCore.Settings;

public sealed class NotificationSettingsDisplayDriver : SiteDisplayDriver<NotificationSettings>
{
    public const string GroupId = "notifications";

    protected override string SettingsGroupId => GroupId;

    public override IDisplayResult Edit(ISite site, NotificationSettings settings, BuildEditorContext context)
    {
        return Initialize<NotificationSettingsViewModel>("NotificationSettings_Edit", model =>
        {
            model.EnableEmailNotifications = settings.EnableEmailNotifications;
            model.DefaultRecipient = settings.DefaultRecipient;
            model.MaxRetryAttempts = settings.MaxRetryAttempts;
        }).Location("Content:5#Notifications")
          .OnGroup(SettingsGroupId);
    }

    public override async Task<IDisplayResult> UpdateAsync(ISite site, NotificationSettings settings, UpdateEditorContext context)
    {
        var model = new NotificationSettingsViewModel();
        await context.Updater.TryUpdateModelAsync(model, Prefix);

        settings.EnableEmailNotifications = model.EnableEmailNotifications;
        settings.DefaultRecipient = model.DefaultRecipient;
        settings.MaxRetryAttempts = model.MaxRetryAttempts;

        return Edit(site, settings, context);
    }
}
```

### Settings View Model

```csharp
public class NotificationSettingsViewModel
{
    public bool EnableEmailNotifications { get; set; }

    public string DefaultRecipient { get; set; }

    public int MaxRetryAttempts { get; set; }
}
```

### Registering Settings Navigation

```csharp
public sealed class AdminMenu : INavigationProvider
{
    private readonly IStringLocalizer S;

    public AdminMenu(IStringLocalizer<AdminMenu> localizer)
    {
        S = localizer;
    }

    public ValueTask BuildNavigationAsync(string name, NavigationBuilder builder)
    {
        if (!NavigationHelper.IsAdminMenu(name))
        {
            return ValueTask.CompletedTask;
        }

        builder
            .Add(S["Settings"], settings => settings
                .Add(S["Notifications"], S["Notifications"].PrefixPosition(), notifications => notifications
                    .Permission(Permissions.ManageNotificationSettings)
                    .Action("Index", "Admin", new { area = "OrchardCore.Settings", groupId = NotificationSettingsDisplayDriver.GroupId })
                    .LocalNav()
                )
            );

        return ValueTask.CompletedTask;
    }
}
```

## Admin Filters and Middleware

Admin filters allow you to execute logic for every admin request, such as injecting data into the layout, enforcing policies, or modifying the response.

### Creating an Admin Result Filter

```csharp
using Microsoft.AspNetCore.Mvc.Filters;
using OrchardCore.Admin;
using OrchardCore.DisplayManagement;
using OrchardCore.DisplayManagement.Layout;

public sealed class AdminBannerFilter : IAsyncResultFilter
{
    private readonly ILayoutAccessor _layoutAccessor;
    private readonly IShapeFactory _shapeFactory;

    public AdminBannerFilter(
        ILayoutAccessor layoutAccessor,
        IShapeFactory shapeFactory)
    {
        _layoutAccessor = layoutAccessor;
        _shapeFactory = shapeFactory;
    }

    public async Task OnResultExecutionAsync(ResultExecutingContext context, ResultExecutionDelegate next)
    {
        if (!AdminAttribute.IsApplied(context.HttpContext))
        {
            await next();
            return;
        }

        var layout = await _layoutAccessor.GetLayoutAsync();
        var messagesZone = layout.Zones["Messages"];

        var bannerShape = await _shapeFactory.CreateAsync("AdminBanner");
        await messagesZone.AddAsync(bannerShape, "0");

        await next();
    }
}
```

Register the filter in `Startup.cs`:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddMvcFilter<AdminBannerFilter>();
    }
}
```

## Configuring Admin Options via Recipes

Use recipes to configure admin-related settings during site setup or tenant initialization:

```json
{
    "steps": [
        {
            "name": "settings",
            "AdminSettings": {
                "DisplayMenuFilter": true,
                "DisplayDarkMode": true,
                "DisplayThemeToggler": true
            }
        }
    ]
}
```

For additional practical examples covering admin controllers, menus, widgets, and settings, see the `references/admin-examples.md` file.
