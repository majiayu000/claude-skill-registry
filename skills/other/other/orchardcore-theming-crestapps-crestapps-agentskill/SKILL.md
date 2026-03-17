---
name: orchardcore-theming
description: Skill for creating and customizing Orchard Core themes. Covers theme scaffolding, Liquid and Razor templates, zones, shape templates, shape alternates, placement rules, asset management, resource manifests, and theme settings.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "2.0"
---

# Orchard Core Theming

Use this skill for Orchard Core theming tasks including theme creation, shape overrides, template discovery, content rendering, placement rules, and asset management.

## How to Use

- **Task match**: Scan the Tasks list below. If the request matches, go directly to the referenced files.
- **Exploration**: Use the section cues to pick a reference, then choose the relevant detail.
- Determine Razor vs Liquid early. Check the active theme for `.cshtml` (Razor) or `.liquid` files. If unclear, default to Liquid and confirm with the user.
- Open only the necessary reference files; prefer examples and ready-to-copy patterns.

## Evidence Rules

- Prefer repo evidence over assumptions: check the active theme, base theme, `placement.json`, and existing templates.
- Confirm unknown part/field properties in `ContentDefinition.json` or the database.
- Ask for missing identifiers (content type, part name, field name, display type) instead of inventing them.
- Do not invent recipe steps or feature IDs; consult the recipes skill for valid steps.

## Guidelines

- Theme names should be PascalCase and may be prefixed with the organization name (e.g., `CrestApps.MyTheme`).
- Themes must have a `Manifest.cs` declaring the theme and its base theme (if any).
- Prefer shapes over MVC partials for UI composition.
- `Views/Layout.cshtml` is treated as the site layout automatically; do not set `Layout = null` inside it.
- Override base theme views in the child theme rather than editing the base theme.
- Use `{% render_section "SectionName" %}` in Liquid layouts to render named sections.
- Asset pipelines can be managed through `wwwroot/` and resource manifests.
- The `TheAdmin` theme is used for the admin panel and can be extended.

## Reference Cues

Use these cues to decide which reference file to open:

- Use `references/theming-examples.md` for end-to-end theme creation examples (manifests, layouts, shape overrides).
- Use `references/shape-alternates.md` to find shape names, alternates, and naming rules for template overrides.
- Use `references/placement-rules.md` for `placement.json` patterns, filters, differentiators, and editor grouping.
- Use `references/shape-workflow.md` for a step-by-step checklist to build or override a shape safely.
- Use `references/assets-resources.md` for resource manifests, requiring scripts/styles, and built-in Orchard Core resources.

## Tasks

- Create a new theme from scratch.
- Override a content item shape template.
- Find shape alternates and placement rules.
- Add or override placement rules in `placement.json`.
- Add scripts/styles and include them in the layout.
- Create or customize the admin theme.
- Render BagPart/FlowPart/ListPart items in templates.
- Update a shape after adding fields.
- Work on theme structure or layout.
- Determine template language (Razor vs Liquid).

## Create a Theme

### Manifest Pattern

```csharp
using OrchardCore.DisplayManagement.Manifest;

[assembly: Theme(
    Name = "{{ThemeName}}",
    Author = "{{Author}}",
    Website = "{{Website}}",
    Version = "1.0.0",
    Description = "{{Description}}",
    BaseTheme = "{{BaseTheme}}"
)]
```

### Project File Pattern

```xml
<Project Sdk="Microsoft.NET.Sdk.Razor">

  <PropertyGroup>
    <TargetFramework>net10.0</TargetFramework>
    <AddRazorSupportForMvc>true</AddRazorSupportForMvc>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="OrchardCore.DisplayManagement" Version="2.*" />
    <PackageReference Include="OrchardCore.Theme.Targets" Version="2.*" />
  </ItemGroup>

</Project>
```

### Theme Folder Structure

```
MyTheme/
├── Manifest.cs
├── MyTheme.csproj
├── Views/
│   ├── Layout.liquid (or Layout.cshtml)
│   ├── _ViewImports.cshtml
│   └── Items/
│       └── Content-BlogPost.liquid
├── wwwroot/
│   ├── css/
│   │   └── site.css
│   └── js/
│       └── site.js
├── placement.json (optional)
└── ResourceManifest.cs (optional)
```

### _ViewImports for Razor Themes

If a theme uses Razor, `_ViewImports.cshtml` should exist with at least:

```cshtml
@inherits OrchardCore.DisplayManagement.Razor.RazorPage<TModel>
```

If it's missing, it can cause build errors.

### Liquid Layout Template

```liquid
<!DOCTYPE html>
<html lang="{{ Culture.Name }}">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ Model.Title }} - {{ Site.SiteName }}</title>
    {% resources type: "HeadMeta" %}
    {% resources type: "HeadLink" %}
    {% style src: "~/{{ThemeName}}/css/site.css" %}
    {% resources type: "Stylesheet" %}
</head>
<body>
    {% zone "Header" %}

    <main role="main" class="container">
        {% zone "BeforeContent" %}
        {% zone "Content" %}
        {% zone "AfterContent" %}
    </main>

    {% zone "Footer" %}

    {% resources type: "FooterScript" %}
    {% script src: "~/{{ThemeName}}/js/site.js" at: "Foot" %}
</body>
</html>
```

### Razor Layout Template

```cshtml
@inject OrchardCore.IOrchardHelper Orchard

<!DOCTYPE html>
<html lang="@Orchard.CultureName()">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>@RenderTitleSegments(Site.SiteName)</title>
    @await RenderSectionAsync("HeadMeta", required: false)
    <link rel="stylesheet" href="~/{{ThemeName}}/css/site.css" />
    @RenderSection("Styles", required: false)
</head>
<body>
    @await DisplayAsync(ThemeLayout.Header)

    <main role="main" class="container">
        @await DisplayAsync(ThemeLayout.Content)
    </main>

    @await DisplayAsync(ThemeLayout.Footer)

    <script src="~/{{ThemeName}}/js/site.js"></script>
    @RenderSection("Scripts", required: false)
</body>
</html>
```

### Shape Templates

Override shape rendering by creating templates in the `Views/` folder:

- `Content.liquid` — Default content item display.
- `Content-BlogPost.liquid` — Content display for BlogPost type.
- `Content-BlogPost.Summary.liquid` — Summary display mode for BlogPost type.
- `Widget.liquid` — Default widget wrapper.
- `MenuItem.liquid` — Menu item rendering.

File naming convention: `__` in shape type maps to `-` in file names; `_DisplayType` maps to `.DisplayType` suffix.

### Resource Manifest

```csharp
using OrchardCore.ResourceManagement;

public sealed class ResourceManifest : IResourceManifestProvider
{
    public void BuildManifests(IResourceManifestBuilder builder)
    {
        var manifest = builder.Add();

        manifest
            .DefineStyle("{{ThemeName}}")
            .SetUrl("~/{{ThemeName}}/css/site.min.css", "~/{{ThemeName}}/css/site.css");

        manifest
            .DefineScript("{{ThemeName}}")
            .SetUrl("~/{{ThemeName}}/js/site.min.js", "~/{{ThemeName}}/js/site.js")
            .SetPosition(ResourcePosition.Foot);
    }
}
```

### Zones

Common zones used in Orchard Core themes:

| Zone | Purpose |
|------|---------|
| `Header` | Top of the page, navigation bar area |
| `Content` | Main content area |
| `Footer` | Bottom of the page |
| `BeforeContent` | Before the main content |
| `AfterContent` | After the main content |
| `Navigation` | Primary navigation area |
| `Sidebar` | Sidebar content area |
| `AsideFirst` / `AsideSecond` | Multi-column sidebars |

### Zone Alternates

Zone shapes support alternates for per-zone template overrides:

- `Zone__ZoneName` → file `Zone-Footer.cshtml` (or `.liquid`)
