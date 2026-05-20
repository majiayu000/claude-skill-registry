---
name: orchardcore-navigation
description: Skill for creating and managing navigation menus in Orchard Core. Covers menu creation, navigation providers, admin menus, breadcrumbs, and menu content types.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Navigation - Prompt Templates

## Create Navigation and Menus

You are an Orchard Core expert. Generate navigation menus, admin menus, and menu items for Orchard Core.

### Guidelines

- Enable `OrchardCore.Menu` and `OrchardCore.Navigation` for menu support.
- Menus in Orchard Core are content items of type `Menu`.
- Menu items are nested content items within a menu (e.g., `LinkMenuItem`, `ContentMenuItem`).
- Admin menus are defined through `INavigationProvider` implementations.
- Use the `Position` property to control menu item ordering (lower numbers appear first).
- Admin menu positions follow the pattern: `"1"`, `"1.1"`, `"1.2"` for nested items.
- Navigation providers must be registered as scoped services.

### Enabling Navigation Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Menu",
        "OrchardCore.Navigation",
        "OrchardCore.AdminMenu"
      ],
      "disable": []
    }
  ]
}
```

### Custom Admin Navigation Provider

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
        if (!string.Equals(name, "admin", StringComparison.OrdinalIgnoreCase))
        {
            return ValueTask.CompletedTask;
        }

        builder
            .Add(S["{{MenuGroupName}}"], NavigationConstants.AdminMenuSettingsPosition, settings => settings
                .AddClass("{{icon-class}}")
                .Id("{{menuId}}")
                .Add(S["{{SubMenuName}}"], S["{{SubMenuName}}"].PrefixPosition(), item => item
                    .Action("Index", "Admin", new { area = "{{ModuleName}}" })
                    .Permission(Permissions.{{PermissionName}})
                    .LocalNav()
                )
            );

        return ValueTask.CompletedTask;
    }
}
```

### Registering Navigation Provider

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<INavigationProvider, AdminMenu>();
    }
}
```

### Menu Recipe (Creating a Menu via Recipe)

```json
{
  "steps": [
    {
      "name": "Content",
      "data": [
        {
          "ContentItemId": "main-menu",
          "ContentType": "Menu",
          "DisplayText": "Main Menu",
          "Latest": true,
          "Published": true,
          "MenuPart": {},
          "MenuItemsListPart": {
            "MenuItems": [
              {
                "ContentType": "LinkMenuItem",
                "ContentItemId": "menu-home",
                "LinkMenuItemPart": {
                  "Name": "Home",
                  "Url": "~/"
                }
              },
              {
                "ContentType": "LinkMenuItem",
                "ContentItemId": "menu-about",
                "LinkMenuItemPart": {
                  "Name": "About",
                  "Url": "~/about"
                }
              },
              {
                "ContentType": "LinkMenuItem",
                "ContentItemId": "menu-contact",
                "LinkMenuItemPart": {
                  "Name": "Contact",
                  "Url": "~/contact"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### Rendering Menu in Liquid Template

```liquid
{% shape "Menu", alias: "main-menu" %}
```

### Rendering Breadcrumbs

Enable `OrchardCore.Menu` for breadcrumb support:

```liquid
{% zone "Breadcrumbs" %}
```

### Content Menu Item

To add a content item as a menu item:

```json
{
  "ContentType": "ContentMenuItem",
  "ContentItemId": "menu-blog",
  "ContentMenuItemPart": {
    "ContentItem": {
      "ContentItemId": "{{BlogContentItemId}}"
    }
  }
}
```
