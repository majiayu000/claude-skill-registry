---
name: orchardcore-razor
description: Skill for building Razor views in Orchard Core themes and modules. Covers tag helpers, shape rendering, resource management, IOrchardHelper extensions, layout patterns, and _ViewImports.cshtml setup.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Razor Views - Prompt Templates

## _ViewImports.cshtml Setup

Every Orchard Core theme or module should include a `_ViewImports.cshtml` file at the root of its `Views` folder.

### Minimum Required Directives

```cshtml
@inherits OrchardCore.DisplayManagement.Razor.RazorPage<TModel>
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
@addTagHelper *, OrchardCore.DisplayManagement
@addTagHelper *, OrchardCore.ResourceManagement
@addTagHelper *, OrchardCore.Menu
@addTagHelper *, OrchardCore.Contents
@addTagHelper *, OrchardCore.Media
@using OrchardCore.DisplayManagement
@using OrchardCore.DisplayManagement.Shapes
@using OrchardCore.ContentManagement
@using Microsoft.AspNetCore.Html
```

### Guidelines

- `@inherits OrchardCore.DisplayManagement.Razor.RazorPage<TModel>` gives access to `IOrchardHelper` via `Orchard` and shape display helpers.
- Add only the `@addTagHelper` lines for assemblies your theme or module actually uses.
- `@using OrchardCore.DisplayManagement.Razor` is not needed when `@inherits` already references that namespace.
- For themes, add `@using OrchardCore` to access general extension methods.

## _ViewStart.cshtml Conventions

```cshtml
@{
    Layout = "Layout";
}
```

- Place `_ViewStart.cshtml` in the `Views` folder to set the default layout.
- `"Layout"` references the shape named `Layout` which resolves to `Layout.cshtml`.
- Modules typically do not set a layout in `_ViewStart.cshtml` because their views render inside the theme's layout automatically.
- Override per-view by setting `Layout = null;` for partial or layoutless pages.

## Layout Rendering Patterns

A theme's `Layout.cshtml` renders zones that contain shapes placed by modules and the admin UI.

### Minimal Layout Template

```cshtml
@{
    var body = await RenderBodyAsync();
}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@RenderTitleSegments(Site.SiteName)</title>
    <resources type="Meta" />
    <style asp-name="{{ThemeStyleName}}"></style>
    <resources type="HeadLink" />
    <resources type="HeadScript" />
    <resources type="StyleSheet" />
</head>
<body>
    <zone name="Header" />

    <zone name="Content">
        @body
    </zone>

    <zone name="Footer" />

    <resources type="FooterScript" />
</body>
</html>
```

### Guidelines

- Always call `await RenderBodyAsync()` **before** rendering any zone that wraps it, so the body content registers its resources first.
- Use `@RenderTitleSegments(Site.SiteName)` to render page title segments separated by the site name.
- Render resource tags in the correct location: `Meta`, `HeadLink`, `HeadScript`, `StyleSheet` in `<head>`, and `FooterScript` before `</body>`.

## Shape Tag Helpers

Shapes are the fundamental rendering unit in Orchard Core. Use tag helpers to display and compose shapes.

### Display a Shape

```cshtml
<shape type="{{ShapeType}}" />
```

### Display a Shape with Properties

```cshtml
<shape type="{{ShapeType}}" prop-title="@item.Title" prop-content="@item.Content" />
```

- Prefix shape properties with `prop-` to pass data into the shape template.

### Display a Dynamic Shape Object

When you have a shape object (e.g., from a zone or shape table), render it with `display`:

```cshtml
@await DisplayAsync(Model)
@await DisplayAsync(Model.Content)
```

### Named Shapes with Cache

```cshtml
<shape type="{{ShapeType}}" cache-id="{{unique-id}}" cache-expires-after="@TimeSpan.FromMinutes(5)" />
```

## Zone Tag Helper

Zones are named buckets in the layout that collect shapes for rendering.

### Render a Zone

```cshtml
<zone name="{{ZoneName}}" />
```

### Render a Zone with Wrapper Content

```cshtml
<zone name="{{ZoneName}}">
    <div class="container">
        @RenderBody()
    </div>
</zone>
```

### Conditional Zone Rendering

Check if a zone has content before rendering its wrapper:

```cshtml
@if (Model.{{ZoneName}} != null)
{
    <aside>
        <zone name="{{ZoneName}}" />
    </aside>
}
```

Common zone names: `Header`, `Navigation`, `Content`, `Sidebar`, `Footer`, `AfterContent`, `BeforeContent`.

## Resource Tag Helpers

### Register a Stylesheet

```cshtml
<style asp-name="{{ResourceName}}"></style>
```

### Register a Stylesheet with a CDN Fallback

```cshtml
<style asp-name="{{ResourceName}}" version="{{Version}}" cdn-url="{{CdnUrl}}"></style>
```

### Register a Script at the Foot of the Page

```cshtml
<script asp-name="{{ResourceName}}" at="Foot"></script>
```

### Register a Script at the Head

```cshtml
<script asp-name="{{ResourceName}}" at="Head"></script>
```

### Register an Inline Script

```cshtml
<script at="Foot">
    document.addEventListener('DOMContentLoaded', function () {
        console.log('Page loaded');
    });
</script>
```

### Script Dependencies

```cshtml
<script asp-name="{{ResourceName}}" depends-on="jQuery" at="Foot"></script>
```

### Render All Registered Resources

Place these in the layout to output all resources registered by shapes and modules:

```cshtml
<resources type="Meta" />
<resources type="HeadLink" />
<resources type="HeadScript" />
<resources type="StyleSheet" />
<resources type="FooterScript" />
```

### Resource Positions

| Position | Description |
|----------|-------------|
| `Head` | Rendered in `<head>` via `<resources type="HeadScript" />` |
| `Foot` | Rendered before `</body>` via `<resources type="FooterScript" />` |

## Media Tag Helper

### Render an Image from the Media Library

```cshtml
<img asp-src="@Model.ContentItem.Content.{{PartName}}.{{FieldName}}.Paths[0]" />
```

### Resize an Image

```cshtml
<img asp-src="@imagePath" asp-resize-width="300" />
```

### Resize with Width and Height

```cshtml
<img asp-src="@imagePath" asp-resize-width="800" asp-resize-height="600" />
```

### Resize Modes

```cshtml
<img asp-src="@imagePath" asp-resize-width="400" asp-resize-height="400" asp-resize-mode="Crop" />
```

| Mode | Description |
|------|-------------|
| `Pad` | Resize and pad to fit the target dimensions |
| `BoxPad` | Pad the image to fit within the bounding box |
| `Crop` | Resize and crop to fill the target dimensions |
| `Min` | Resize to the minimum of the target dimensions |
| `Max` | Resize to the maximum of the target dimensions |
| `Stretch` | Stretch the image to fill the target dimensions |

## Content Tag Helpers

### Render a Content Item

```cshtml
<contentitem alias="alias:{{alias}}" display-type="Summary" />
```

### Render a Content Item by Content Item ID

```cshtml
<contentitem content-item-id="@Model.ContentItem.ContentItemId" display-type="Detail" />
```

### Common Display Types

| Display Type | Description |
|--------------|-------------|
| `Detail` | Full detail view |
| `Summary` | Abbreviated summary view |
| `SummaryAdmin` | Admin-specific summary |

## Menu Tag Helper

### Render a Named Menu

```cshtml
<menu alias="alias:main-menu" />
```

- The `alias` attribute specifies the alias of the menu content item.
- The menu renders using the menu shape templates, which can be overridden in your theme.

## Caching Tag Helper

### Cache a Section of Markup

```cshtml
<cache expires-after="@TimeSpan.FromMinutes(10)">
    <p>This content is cached for 10 minutes.</p>
</cache>
```

### Cache with a Vary-By Key

```cshtml
<cache expires-after="@TimeSpan.FromMinutes(5)" vary-by="@Context.Request.Path">
    @await DisplayAsync(Model.Content)
</cache>
```

### Cache Attributes

| Attribute | Description |
|-----------|-------------|
| `expires-after` | `TimeSpan` after which the cache entry expires |
| `expires-on` | Absolute `DateTimeOffset` for expiration |
| `expires-sliding` | Sliding `TimeSpan` expiration window |
| `vary-by` | Key to vary the cached output (e.g., per path or query) |
| `vary-by-user` | When `true`, caches separately per authenticated user |

## Date-Time and Time-Zone Tag Helpers

### Render a UTC Date in the Site's Time Zone

```cshtml
<date-time utc="@Model.ContentItem.CreatedUtc" />
```

### Render a Date with a Custom Format

```cshtml
<date-time utc="@Model.ContentItem.PublishedUtc" format="MMMM dd, yyyy" />
```

### Render the Current Time Zone Name

```cshtml
<time-zone />
```

## IOrchardHelper Extensions

Access `IOrchardHelper` via the `Orchard` property in Razor views that inherit from `OrchardCore.DisplayManagement.Razor.RazorPage<TModel>`.

### Get a Content Item by ID

```cshtml
@{
    var item = await Orchard.GetContentItemByIdAsync("{{contentItemId}}");
}
```

### Get a Content Item by Version ID

```cshtml
@{
    var item = await Orchard.GetContentItemByVersionIdAsync("{{contentItemVersionId}}");
}
```

### Query Content Items

```cshtml
@{
    var items = await Orchard.QueryContentItemsAsync(query =>
        query.Where(index => index.ContentType == "BlogPost" && index.Published));
}
```

### Get Content Items by Content Type

```cshtml
@{
    var items = await Orchard.GetRecentContentItemsByContentTypeAsync("BlogPost", 10);
}
```

### Get a Content Item by Alias

```cshtml
@{
    var item = await Orchard.GetContentItemByHandleAsync("alias:{{alias}}");
}
```

### Get Site Settings Value

```cshtml
@{
    var siteName = Orchard.ConsoleLog(Site.SiteName);
}
```

Access global site settings via `Site`:

```cshtml
<p>@Site.SiteName</p>
<p>@Site.BaseUrl</p>
```

### Liquid-to-HTML Rendering

```cshtml
@{
    var html = await Orchard.LiquidToHtmlAsync("{{ 'now' | date: '%B %d, %Y' }}");
}
```

### Content Item Display

```cshtml
@{
    var shape = await Orchard.DisplayContentItemAsync(contentItem, "Summary");
}
@await DisplayAsync(shape)
```

## Defining a Resource Manifest

Register stylesheets and scripts so they can be referenced by name in Razor views.

### Resource Manifest Class

```csharp
public sealed class ResourceManifest : IResourceManifestProvider
{
    public void BuildManifests(IResourceManifestBuilder builder)
    {
        var manifest = builder.Add();

        manifest.DefineStyle("{{ThemeStyleName}}")
            .SetUrl("~/{{ModuleOrThemeId}}/css/site.min.css", "~/{{ModuleOrThemeId}}/css/site.css");

        manifest.DefineScript("{{ThemeScriptName}}")
            .SetUrl("~/{{ModuleOrThemeId}}/js/site.min.js", "~/{{ModuleOrThemeId}}/js/site.js")
            .SetPosition("Foot");
    }
}
```

### Guidelines

- The first `SetUrl` parameter is the minified version; the second is the debug version.
- Use `SetPosition("Foot")` for scripts that should render before `</body>`.
- Use `SetDependencies("jQuery")` to declare script dependencies.
- Register the manifest class in `Startup.cs`:

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddResourceManifest<ResourceManifest>();
    }
}
```

## Recipe Step for Themes

### Set the Active Theme via Recipe

```json
{
    "steps": [
        {
            "name": "Themes",
            "Site": "{{ThemeId}}",
            "Admin": "TheAdmin"
        }
    ]
}
```
