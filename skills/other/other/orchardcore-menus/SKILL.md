---
name: orchardcore-menus
description: Skill for creating and managing menus in Orchard Core. Covers menu content types, menu item types, menu widgets, navigation rendering, pager shapes, breadcrumbs, and menu customization via shapes and alternates.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Menus - Prompt Templates

## Create and Manage Navigation Menus

You are an Orchard Core expert. Generate menu definitions, navigation structures, menu widgets, and pager configurations for Orchard Core.

### Guidelines

- Enable `OrchardCore.Menu` to manage menus. Menus are content items with the `Menu` content type.
- A menu consists of a `MenuItemsListPart` that holds an ordered tree of menu items.
- Built-in menu item types include `LinkMenuItem`, `ContentMenuItem`, and `UrlMenuItem`.
- `LinkMenuItem` renders a static link with a display text and URL.
- `ContentMenuItem` links to a published content item and derives its text and URL from the item.
- `UrlMenuItem` renders a link whose URL is evaluated as a Liquid expression at runtime.
- Display menus on the front end by placing a `MenuWidget` in a theme zone via a layer.
- Pager shapes (`Pager`, `PagerSlim`, `Pager_Links`) provide pagination for content lists.
- All recipe JSON blocks must be wrapped in the root recipe format `{ "steps": [...] }`.
- All C# classes in code samples must use the `sealed` modifier.

### Enabling Menu Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Menu",
        "OrchardCore.Widgets",
        "OrchardCore.Layers"
      ],
      "disable": []
    }
  ]
}
```

### Menu Item Types

| Type | Purpose | URL Source |
|---|---|---|
| `LinkMenuItem` | Static navigation link | Hardcoded URL in `LinkMenuItemPart.Url` |
| `ContentMenuItem` | Link derived from a content item | Resolved from the referenced content item's route |
| `UrlMenuItem` | Dynamic link with Liquid URL | Liquid expression evaluated at render time |

### Creating a Menu via Recipe

```json
{
  "steps": [
    {
      "name": "Content",
      "data": [
        {
          "ContentItemId": "main-navigation",
          "ContentType": "Menu",
          "DisplayText": "Main Navigation",
          "Latest": true,
          "Published": true,
          "MenuPart": {},
          "TitlePart": {
            "Title": "Main Navigation"
          },
          "MenuItemsListPart": {
            "MenuItems": [
              {
                "ContentItemId": "menu-item-home",
                "ContentType": "LinkMenuItem",
                "DisplayText": "Home",
                "LinkMenuItemPart": {
                  "Name": "Home",
                  "Url": "~/"
                }
              },
              {
                "ContentItemId": "menu-item-about",
                "ContentType": "LinkMenuItem",
                "DisplayText": "About",
                "LinkMenuItemPart": {
                  "Name": "About",
                  "Url": "~/about"
                }
              },
              {
                "ContentItemId": "menu-item-blog",
                "ContentType": "LinkMenuItem",
                "DisplayText": "Blog",
                "LinkMenuItemPart": {
                  "Name": "Blog",
                  "Url": "~/blog"
                }
              },
              {
                "ContentItemId": "menu-item-contact",
                "ContentType": "LinkMenuItem",
                "DisplayText": "Contact",
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

### Multi-Level Navigation Menu

Nest menu items inside a parent item's `MenuItemsListPart` to create dropdown or flyout submenus:

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
          "TitlePart": {
            "Title": "Main Menu"
          },
          "MenuItemsListPart": {
            "MenuItems": [
              {
                "ContentItemId": "menu-products",
                "ContentType": "LinkMenuItem",
                "DisplayText": "Products",
                "LinkMenuItemPart": {
                  "Name": "Products",
                  "Url": "~/products"
                },
                "MenuItemsListPart": {
                  "MenuItems": [
                    {
                      "ContentItemId": "menu-products-software",
                      "ContentType": "LinkMenuItem",
                      "DisplayText": "Software",
                      "LinkMenuItemPart": {
                        "Name": "Software",
                        "Url": "~/products/software"
                      }
                    },
                    {
                      "ContentItemId": "menu-products-hardware",
                      "ContentType": "LinkMenuItem",
                      "DisplayText": "Hardware",
                      "LinkMenuItemPart": {
                        "Name": "Hardware",
                        "Url": "~/products/hardware"
                      }
                    }
                  ]
                }
              },
              {
                "ContentItemId": "menu-services",
                "ContentType": "LinkMenuItem",
                "DisplayText": "Services",
                "LinkMenuItemPart": {
                  "Name": "Services",
                  "Url": "~/services"
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

### Placing a Menu Widget in a Zone

Use a `MenuWidget` assigned to a layer and zone to render a menu on the front end:

```json
{
  "steps": [
    {
      "name": "Content",
      "data": [
        {
          "ContentItemId": "widget-main-menu",
          "ContentType": "MenuWidget",
          "DisplayText": "Main Menu Widget",
          "Latest": true,
          "Published": true,
          "LayerMetadata": {
            "Layer": "Always",
            "Zone": "Navigation",
            "Position": 0
          },
          "MenuWidget": {
            "MenuContentItemId": "main-navigation"
          }
        }
      ]
    }
  ]
}
```

### UrlMenuItem with Liquid Expression

`UrlMenuItem` accepts a Liquid template in its `Url` field. The expression is evaluated at render time, allowing dynamic URLs based on request context:

```json
{
  "ContentItemId": "menu-item-profile",
  "ContentType": "UrlMenuItem",
  "DisplayText": "My Profile",
  "UrlMenuItemPart": {
    "Name": "My Profile",
    "Url": "{{ '~/profile/' | append: User.Identity.Name }}"
  }
}
```

### ContentMenuItem Linking to a Content Item

`ContentMenuItem` generates its URL and display text from a referenced content item:

```json
{
  "ContentItemId": "menu-item-featured",
  "ContentType": "ContentMenuItem",
  "DisplayText": "Featured Article",
  "ContentMenuItemPart": {
    "ContentItem": {
      "ContentItemId": "article-featured-2025"
    }
  }
}
```

### Menu Shapes and Alternates

Orchard Core renders menus through a shape hierarchy. Override these shapes to customize rendering:

| Shape | Purpose |
|---|---|
| `Menu` | The root shape wrapping the entire menu as a `<nav>` element. |
| `MenuItem` | Each individual menu entry, rendered as an `<li>` element. |
| `MenuItemLink` | The anchor tag `<a>` inside a `MenuItem`. |

Available shape alternates for targeted overrides:

- `Menu-{MenuName}` — Targets a specific menu by its alias (e.g., `Menu-MainNavigation`).
- `MenuItem-{MenuName}` — Targets items within a specific menu.
- `MenuItemLink-{MenuName}` — Targets links within a specific menu.
- `MenuItem-{MenuItemType}` — Targets a specific menu item type (e.g., `MenuItem-LinkMenuItem`).
- `MenuItemLink-{MenuItemType}` — Targets links for a specific item type.

### Customizing Menu Rendering in Razor

Override the `MenuItem` shape with an alternate. Create `Views/MenuItem-MainNavigation.cshtml`:

```cshtml
@using OrchardCore.ContentManagement
@{
    var items = (IEnumerable<dynamic>)Model.Items;
    var menuItem = (ContentItem)Model.ContentItem;
    var hasChildren = items != null && items.Any();
}

<li class="nav-item @(hasChildren ? "dropdown" : "")">
    <a class="nav-link @(hasChildren ? "dropdown-toggle" : "")"
       href="@Model.Href"
       @if (hasChildren)
       {
           <text>data-bs-toggle="dropdown" aria-expanded="false"</text>
       }>
        @Model.Text
    </a>
    @if (hasChildren)
    {
        <ul class="dropdown-menu">
            @foreach (var child in items)
            {
                @await DisplayAsync(child)
            }
        </ul>
    }
</li>
```

### Customizing Menu Rendering in Liquid

Create a Liquid alternate at `Views/Menu-MainNavigation.liquid`:

```liquid
<nav class="navbar navbar-expand-lg" aria-label="{{ Model.Menu.DisplayText }}">
    <ul class="navbar-nav">
        {% for item in Model.Items %}
            {% shape_clear_alternates item %}
            {% shape_add_alternates item "MenuItem_NavBar" %}
            {{ item | shape_render }}
        {% endfor %}
    </ul>
</nav>
```

### Styling Menus with CSS Classes

Assign CSS classes to menu items by adding `HtmlMenuItemPart` settings. Common patterns:

- Add `active` class to the currently selected menu item using theme or JavaScript logic.
- Use Bootstrap navigation classes: `navbar`, `nav`, `nav-item`, `nav-link`, `dropdown`, `dropdown-menu`.
- Apply icon classes via the `IconClass` property on menu items.

### Menu Item Icons and Attributes

Menu items support icons and HTML attributes:

```json
{
  "ContentItemId": "menu-item-dashboard",
  "ContentType": "LinkMenuItem",
  "DisplayText": "Dashboard",
  "LinkMenuItemPart": {
    "Name": "Dashboard",
    "Url": "~/dashboard"
  },
  "HtmlMenuItemPart": {
    "IconClass": "fa fa-tachometer-alt",
    "SelectedCssClass": "active"
  }
}
```

In templates, access icon and attribute values:

```liquid
<li class="nav-item {{ Model.SelectedCssClass }}">
    {% if Model.IconClass %}
        <i class="{{ Model.IconClass }}"></i>
    {% endif %}
    <a class="nav-link" href="{{ Model.Href }}">{{ Model.Text }}</a>
</li>
```

### Breadcrumb Navigation

Build breadcrumb navigation from the current content item's position in a menu tree. Use `INavigationManager` to resolve the trail:

```csharp
using Microsoft.AspNetCore.Mvc;
using OrchardCore.Navigation;

public sealed class BreadcrumbViewComponent : ViewComponent
{
    private readonly INavigationManager _navigationManager;

    public BreadcrumbViewComponent(INavigationManager navigationManager)
    {
        _navigationManager = navigationManager;
    }

    public async Task<IViewComponentResult> InvokeAsync()
    {
        var menuItems = await _navigationManager.BuildMenuAsync("main", ActionContext);
        var breadcrumbs = new List<MenuItem>();
        FindBreadcrumbTrail(menuItems, HttpContext.Request.Path, breadcrumbs);
        return View(breadcrumbs);
    }

    private static bool FindBreadcrumbTrail(
        IEnumerable<MenuItem> items,
        string currentPath,
        List<MenuItem> trail)
    {
        foreach (var item in items)
        {
            trail.Add(item);

            if (item.Href != null && currentPath.StartsWith(item.Href, StringComparison.OrdinalIgnoreCase))
            {
                return true;
            }

            if (item.Items.Count > 0 && FindBreadcrumbTrail(item.Items, currentPath, trail))
            {
                return true;
            }

            trail.RemoveAt(trail.Count - 1);
        }

        return false;
    }
}
```

Render the breadcrumb in a Razor view `Views/Shared/Components/Breadcrumb/Default.cshtml`:

```cshtml
@model List<OrchardCore.Navigation.MenuItem>

<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        @for (var i = 0; i < Model.Count; i++)
        {
            var item = Model[i];
            var isLast = i == Model.Count - 1;
            <li class="breadcrumb-item @(isLast ? "active" : "")"
                @(isLast ? "aria-current=\"page\"" : "")>
                @if (!isLast)
                {
                    <a href="@item.Href">@item.Text</a>
                }
                else
                {
                    @item.Text
                }
            </li>
        }
    </ol>
</nav>
```

### Pager Shapes

Orchard Core includes pager shapes for paginating content lists. These shapes are used by list content types and custom queries.

| Shape | Purpose |
|---|---|
| `Pager` | Full pagination control with page numbers, next, and previous links. |
| `PagerSlim` | Lightweight pager with only previous and next links. |
| `Pager_Links` | Renders the page number links within a `Pager`. |
| `Pager_First` | Link to the first page. |
| `Pager_Previous` | Link to the previous page. |
| `Pager_Next` | Link to the next page. |
| `Pager_Last` | Link to the last page. |
| `Pager_Gap` | Ellipsis indicator between non-contiguous page numbers. |

Override pager shapes to match your theme. Create `Views/Pager.cshtml`:

```cshtml
@{
    var pager = Model;
}

<nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
        @if (Model.PreviousPage != null)
        {
            <li class="page-item">
                <a class="page-link" href="@Model.PreviousPage">Previous</a>
            </li>
        }

        @await DisplayAsync(Model.Pager_Links)

        @if (Model.NextPage != null)
        {
            <li class="page-item">
                <a class="page-link" href="@Model.NextPage">Next</a>
            </li>
        }
    </ul>
</nav>
```

### PagerSlim for Blog or Feed Lists

`PagerSlim` is useful for scenarios where the total count is unknown:

```liquid
{% assign pagerSlim = Model.Pager %}
<nav aria-label="Pagination">
    <ul class="pagination">
        {% if pagerSlim.PreviousPage %}
            <li class="page-item">
                <a class="page-link" href="{{ pagerSlim.PreviousPage }}">Newer Posts</a>
            </li>
        {% endif %}
        {% if pagerSlim.NextPage %}
            <li class="page-item">
                <a class="page-link" href="{{ pagerSlim.NextPage }}">Older Posts</a>
            </li>
        {% endif %}
    </ul>
</nav>
```

### Registering a Custom Navigation Provider

Provide menu items programmatically by implementing `INavigationProvider`:

```csharp
using Microsoft.Extensions.Localization;
using OrchardCore.Navigation;

public sealed class MainMenuNavigationProvider : INavigationProvider
{
    private readonly IStringLocalizer _localizer;

    public MainMenuNavigationProvider(IStringLocalizer<MainMenuNavigationProvider> localizer)
    {
        _localizer = localizer;
    }

    public ValueTask BuildNavigationAsync(string name, NavigationBuilder builder)
    {
        if (!string.Equals(name, "main", StringComparison.OrdinalIgnoreCase))
        {
            return ValueTask.CompletedTask;
        }

        builder
            .Add(_localizer["Home"], "0", item => item
                .Url("~/")
                .AddClass("nav-home"))
            .Add(_localizer["Products"], "1", item => item
                .Url("~/products")
                .AddClass("nav-products")
                .Add(_localizer["Software"], "0", sub => sub
                    .Url("~/products/software"))
                .Add(_localizer["Hardware"], "1", sub => sub
                    .Url("~/products/hardware")));

        return ValueTask.CompletedTask;
    }
}
```

Register in `Startup.cs`:

```csharp
using Microsoft.Extensions.DependencyInjection;
using OrchardCore.Modules;
using OrchardCore.Navigation;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<INavigationProvider, MainMenuNavigationProvider>();
    }
}
```
