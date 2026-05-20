---
name: orchardcore-content-parts
description: Skill for adding and configuring built-in content parts in Orchard Core. Covers every built-in content part with all available settings, migration code patterns, and recipe configuration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Content Parts - Prompt Templates

## Add and Configure Content Parts

You are an Orchard Core expert. Generate migration code and recipes for attaching and configuring built-in content parts.

### Guidelines

- Parts are attached to content types using `AlterTypeDefinitionAsync` in a migration.
- Each part has specific settings that control its behavior.
- Part settings are applied via `.WithSettings(new XxxPartSettings { ... })`.
- Use `.WithPosition("N")` to control the order of parts in the editor.
- Third-party modules providing parts (CrestApps, Lombiq, etc.) must be installed as NuGet packages in the web project (the startup project of the solution), not just in the module project.
- Always seal classes.

### General Pattern for Attaching a Part

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("{{PartName}}", part => part
        .WithPosition("{{Position}}")
        .WithSettings(new {{PartName}}Settings
        {
            // Part-specific settings
        })
    )
);
```

---

## TitlePart

Provides a title/display text for a content item. Feature: `OrchardCore.Title`.

### TitlePart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Options` | TitlePartOptions | `Editable` | Title behavior: `Editable`, `GeneratedDisabled`, `GeneratedHidden`, `EditableRequired`. |
| `Pattern` | string | `""` | Liquid pattern to generate the title (used with `GeneratedDisabled` or `GeneratedHidden`). |
| `RenderTitle` | bool | `true` | Whether to render the title in the content shape. |

### TitlePart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("TitlePart", part => part
        .WithPosition("0")
        .WithSettings(new TitlePartSettings
        {
            Options = TitlePartOptions.EditableRequired,
            RenderTitle = true
        })
    )
);
```

### TitlePart with Generated Title

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("TitlePart", part => part
        .WithPosition("0")
        .WithSettings(new TitlePartSettings
        {
            Options = TitlePartOptions.GeneratedDisabled,
            Pattern = "{{ ContentItem.Content.{{ContentType}}.Name.Text }} - {{ ContentItem.Content.{{ContentType}}.Date.Value | date: '%Y-%m-%d' }}"
        })
    )
);
```

---

## AutoroutePart

Generates a URL (slug) for a content item. Feature: `OrchardCore.Autoroute`.

### AutoroutePart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `AllowCustomPath` | bool | `false` | Whether users can define a custom path. |
| `Pattern` | string | `"{{ ContentItem.DisplayText \| slugify }}"` | Liquid pattern to generate the slug. |
| `ShowHomepageOption` | bool | `false` | Whether to show the "Set as homepage" option. |
| `AllowUpdatePath` | bool | `false` | Whether to allow re-generating the path on data change. |
| `AllowDisabled` | bool | `false` | Whether to allow disabling autoroute on individual items. |
| `AllowRouteContainedItems` | bool | `false` | Whether to route contained items. |
| `ManageContainedItemRoutes` | bool | `false` | Whether this part manages contained item routes. |
| `AllowAbsolutePath` | bool | `false` | Whether to allow absolute paths for contained items. |

### AutoroutePart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("AutoroutePart", part => part
        .WithPosition("1")
        .WithSettings(new AutoroutePartSettings
        {
            AllowCustomPath = true,
            ShowHomepageOption = false,
            Pattern = "{{ ContentItem.DisplayText | slugify }}",
            AllowUpdatePath = true
        })
    )
);
```

---

## HtmlBodyPart

Provides a rich HTML body editor. Feature: `OrchardCore.Html`.

### HtmlBodyPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `SanitizeHtml` | bool | `true` | Whether to sanitize HTML content. |

### HtmlBodyPart Editors

| Editor | Description |
|---|---|
| *(default)* | Standard rich text editor. |
| `Wysiwyg` | WYSIWYG HTML editor. |
| `Trumbowyg` | Trumbowyg WYSIWYG editor. |
| `Monaco` | Monaco code editor. |

### HtmlBodyPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("HtmlBodyPart", part => part
        .WithPosition("2")
        .WithEditor("Wysiwyg")
        .WithSettings(new HtmlBodyPartSettings
        {
            SanitizeHtml = true
        })
    )
);
```

---

## MarkdownBodyPart

Provides a Markdown body editor. Feature: `OrchardCore.Markdown`.

### MarkdownBodyPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `SanitizeHtml` | bool | `true` | Whether to sanitize HTML output. |

### MarkdownBodyPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("MarkdownBodyPart", part => part
        .WithPosition("2")
        .WithSettings(new MarkdownBodyPartSettings
        {
            SanitizeHtml = true
        })
    )
);
```

---

## ListPart

Makes a content type a container for other content items. Feature: `OrchardCore.Lists`.

### ListPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `PageSize` | int | `10` | Number of items to display per page. |
| `EnableOrdering` | bool | `false` | Whether to allow manual ordering. |
| `ContainedContentTypes` | string[] | `[]` | Content types that can be contained. |
| `ShowHeader` | bool | `true` | Whether to show the list header. |

### ListPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("Blog", type => type
    .WithPart("ListPart", part => part
        .WithPosition("3")
        .WithSettings(new ListPartSettings
        {
            PageSize = 10,
            EnableOrdering = false,
            ContainedContentTypes = new[] { "BlogPost" },
            ShowHeader = true
        })
    )
);
```

---

## FlowPart

Enables a content type to contain a flow of widget content items. Feature: `OrchardCore.Flows`.

### FlowPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `ContainedContentTypes` | string[] | `[]` | Content types that can be added to the flow. |

### FlowPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("FlowPart", part => part
        .WithPosition("3")
        .WithSettings(new FlowPartSettings
        {
            ContainedContentTypes = new[] { "HtmlWidget", "ImageWidget", "BlockQuote" }
        })
    )
);
```

---

## BagPart

A container part allowing nested content items within a content item. Feature: `OrchardCore.Flows`.

### BagPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `ContainedContentTypes` | string[] | `[]` | Content types that can be added to the bag. |
| `DisplayType` | string | `"Detail"` | Display type for rendering bag items. |

### BagPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("BagPart", "{{BagPartName}}", part => part
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("4")
        .WithSettings(new BagPartSettings
        {
            ContainedContentTypes = new[] { "Slide", "Testimonial" }
        })
    )
);
```

---

## AliasPart

Provides an alias identifier for a content item. Feature: `OrchardCore.Alias`.

### AliasPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Pattern` | string | `""` | Liquid pattern to generate the alias. |

### AliasPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("AliasPart", part => part
        .WithPosition("1")
        .WithSettings(new AliasPartSettings
        {
            Pattern = "{{ ContentItem.DisplayText | slugify }}"
        })
    )
);
```

---

## PublishLaterPart

Allows scheduling future publish dates. Feature: `OrchardCore.PublishLater`.

### PublishLaterPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("PublishLaterPart", part => part
        .WithPosition("5")
    )
);
```

---

## LocalizationPart

Enables content localization (translation). Feature: `OrchardCore.ContentLocalization`.

### LocalizationPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("LocalizationPart", part => part
        .WithPosition("6")
    )
);
```

---

## TaxonomyPart

Makes a content type act as a taxonomy container. Feature: `OrchardCore.Taxonomies`.

### TaxonomyPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `TermContentType` | string | `""` | The content type to use for terms. |

### TaxonomyPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{TaxonomyType}}", type => type
    .WithPart("TitlePart", part => part.WithPosition("0"))
    .WithPart("TaxonomyPart", part => part
        .WithPosition("1")
        .WithSettings(new TaxonomyPartSettings
        {
            TermContentType = "{{TermContentType}}"
        })
    )
);
```

---

## SeoMetaPart

Provides SEO metadata (meta title, description, etc.). Feature: `OrchardCore.Seo`.

### SeoMetaPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("SeoMetaPart", part => part
        .WithPosition("10")
    )
);
```

---

## PreviewPart

Enables content preview. Feature: `OrchardCore.ContentPreview`.

### PreviewPart Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Pattern` | string | `""` | Liquid pattern for the preview URL. |

### PreviewPart Migration

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .WithPart("PreviewPart", part => part
        .WithPosition("11")
        .WithSettings(new PreviewPartSettings
        {
            Pattern = "{{ ContentItem | display_url }}"
        })
    )
);
```

---

## Content Type Options

When defining a content type, these options control the content type behavior:

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("{{ContentType}}", type => type
    .DisplayedAs("{{DisplayName}}")
    .Creatable()        // Can be created from the admin
    .Listable()         // Appears in content listings
    .Draftable()        // Supports draft versions
    .Versionable()      // Supports versioning
    .Securable()        // Supports per-content permissions
    .Stereotype("{{Stereotype}}") // Set a stereotype (e.g., "Widget", "MenuItem")
);
```

---

## Installing Third-Party Part Modules

Modules that provide custom parts from external sources (CrestApps, Lombiq, or community modules) must be installed as NuGet packages in the **web project** (the startup project of the solution):

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">
  <ItemGroup>
    <!-- Orchard Core base -->
    <PackageReference Include="OrchardCore.Application.Cms.Targets" Version="2.*" />

    <!-- Third-party modules must be added to the web project -->
    <PackageReference Include="CrestApps.OrchardCore.AI" Version="1.*" />
    <PackageReference Include="Lombiq.HelpfulExtensions.OrchardCore" Version="1.*" />
  </ItemGroup>
</Project>
```

For local project references to third-party modules:

```xml
<ItemGroup>
  <!-- Local third-party module project reference in the web project -->
  <ProjectReference Include="../ThirdParty.Module/ThirdParty.Module.csproj" />
</ItemGroup>
```
