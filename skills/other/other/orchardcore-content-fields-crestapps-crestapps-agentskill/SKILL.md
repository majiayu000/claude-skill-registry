---
name: orchardcore-content-fields
description: Skill for adding and configuring content fields in Orchard Core. Covers every built-in field type with all available settings, editor options, display modes, and migration code patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Content Fields - Prompt Templates

## Add and Configure Content Fields

You are an Orchard Core expert. Generate migration code and recipes for adding content fields with all available settings.

### Guidelines

- Fields are added to content parts using `AlterPartDefinitionAsync` in a migration.
- Each field has a `FieldSettings` base with `Hint` (string) and `Required` (bool).
- Each field type has its own specific settings class (e.g., `TextFieldSettings`, `NumericFieldSettings`).
- Fields also have `ContentPartFieldSettings` controlling `DisplayName`, `Description`, `Editor`, `DisplayMode`, and `Position`.
- Use `.WithEditor("EditorName")` to select an editor variant.
- Use `.WithDisplayMode("DisplayModeName")` to select a display variant.
- Third-party modules providing fields (CrestApps, Lombiq, etc.) must be installed as NuGet packages in the web project (the startup project of the solution), not just in the module project.
- Always seal classes.

### General Pattern for Adding a Field

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("{{FieldType}}")
        .WithDisplayName("{{DisplayName}}")
        .WithDescription("{{Description}}")
        .WithPosition("{{Position}}")
        .WithSettings(new {{FieldType}}Settings
        {
            // Field-specific settings
        })
    )
);
```

---

## TextField

Stores a single text value. Supports multiple editor modes.

### TextField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `DefaultValue` | string | `null` | Default value for new content items. |
| `Type` | FieldBehaviorType | `Unset` | Field behavior type. |
| `Pattern` | string | `null` | The pattern used to build the value. |
| `Placeholder` | string | `""` | Placeholder text. |

### TextField Editors

| Editor | Description |
|---|---|
| *(default)* | Standard single-line text input. |
| `TextArea` | Multi-line text area. |
| `CodeMirror` | Code editor with syntax highlighting. |
| `PredefinedList` | Dropdown or radio buttons from a predefined list. |
| `Monaco` | Monaco code editor. |

### TextField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("TextField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new TextFieldSettings
        {
            Required = true,
            Hint = "{{Hint}}",
            DefaultValue = "{{DefaultValue}}",
            Placeholder = "{{Placeholder}}"
        })
    )
);
```

### TextField with TextArea Editor

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("TextField")
        .WithDisplayName("{{DisplayName}}")
        .WithEditor("TextArea")
        .WithPosition("{{Position}}")
        .WithSettings(new TextFieldSettings
        {
            Hint = "Enter a detailed description"
        })
    )
);
```

### TextField with PredefinedList Editor

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("TextField")
        .WithDisplayName("{{DisplayName}}")
        .WithEditor("PredefinedList")
        .WithPosition("{{Position}}")
        .WithSettings(new TextFieldPredefinedListEditorSettings
        {
            Editor = EditorOption.Dropdown,
            DefaultValue = "option1",
            Options = new[]
            {
                new ListValueOption("Option 1", "option1"),
                new ListValueOption("Option 2", "option2"),
                new ListValueOption("Option 3", "option3")
            }
        })
    )
);
```

---

## HtmlField

Stores HTML content with optional sanitization.

### HtmlField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `SanitizeHtml` | bool | `true` | Whether to sanitize HTML content. |

### HtmlField Editors

| Editor | Description |
|---|---|
| *(default)* | Rich text editor (WYSIWYG). |
| `Wysiwyg` | WYSIWYG HTML editor. |
| `Trumbowyg` | Trumbowyg WYSIWYG editor. |
| `Monaco` | Monaco code editor for raw HTML. |

### HtmlField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("HtmlField")
        .WithDisplayName("{{DisplayName}}")
        .WithEditor("Wysiwyg")
        .WithPosition("{{Position}}")
        .WithSettings(new HtmlFieldSettings
        {
            Required = true,
            SanitizeHtml = true,
            Hint = "Enter HTML content"
        })
    )
);
```

---

## NumericField

Stores a numeric (decimal) value.

### NumericField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Scale` | int | `0` | Number of decimal places. |
| `Minimum` | decimal? | `null` | Minimum allowed value. |
| `Maximum` | decimal? | `null` | Maximum allowed value. |
| `Placeholder` | string | `null` | Placeholder text. |
| `DefaultValue` | string | `null` | Default value. |

### NumericField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("NumericField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new NumericFieldSettings
        {
            Required = true,
            Minimum = 0,
            Maximum = 999999,
            Scale = 2,
            Placeholder = "0.00",
            Hint = "Enter the price"
        })
    )
);
```

---

## BooleanField

Stores a true/false value.

### BooleanField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Label` | string | `null` | Label text for the checkbox. |
| `DefaultValue` | bool | `false` | Default checked state. |

### BooleanField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("BooleanField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new BooleanFieldSettings
        {
            Label = "Is Featured",
            DefaultValue = false,
            Hint = "Check to mark as featured"
        })
    )
);
```

---

## DateField

Stores a date value (no time component).

### DateField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |

### DateField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("DateField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new DateFieldSettings
        {
            Required = true,
            Hint = "Select a date"
        })
    )
);
```

---

## DateTimeField

Stores a date and time value.

### DateTimeField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |

### DateTimeField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("DateTimeField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new DateTimeFieldSettings
        {
            Required = true,
            Hint = "Select date and time"
        })
    )
);
```

---

## TimeField

Stores a time value.

### TimeField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Step` | string | `null` | Step interval for the time picker (e.g., `"00:15:00"` for 15-minute steps). |

### TimeField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("TimeField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new TimeFieldSettings
        {
            Required = true,
            Step = "00:15:00",
            Hint = "Select a time"
        })
    )
);
```

---

## ContentPickerField

References other content items.

### ContentPickerField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Multiple` | bool | `false` | Whether to allow selecting multiple content items. |
| `DisplayAllContentTypes` | bool | `false` | Whether to show all content types in the picker. |
| `DisplayedContentTypes` | string[] | `[]` | Content types to display in the picker. |
| `DisplayedStereotypes` | string[] | `[]` | Stereotypes to filter displayed content types. |
| `Placeholder` | string | `""` | Placeholder text. |
| `TitlePattern` | string | `"{{ Model.ContentItem \| display_text }}"` | Liquid pattern for the displayed title. |

### ContentPickerField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("ContentPickerField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new ContentPickerFieldSettings
        {
            Required = true,
            Multiple = false,
            DisplayedContentTypes = new[] { "BlogPost", "Article" },
            Hint = "Select a related article"
        })
    )
);
```

---

## MediaField

Attaches media files from the media library.

### MediaField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Multiple` | bool | `true` | Whether to allow multiple files. |
| `AllowMediaText` | bool | `true` | Whether to allow alt text for media. |
| `AllowAnchors` | bool | `false` | Whether to allow anchor points on images. |
| `AllowedExtensions` | string[] | `[]` | Allowed file extensions (empty = all allowed). |

### MediaField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("MediaField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new MediaFieldSettings
        {
            Required = true,
            Multiple = false,
            AllowMediaText = true,
            AllowedExtensions = new[] { ".jpg", ".jpeg", ".png", ".gif", ".webp" },
            Hint = "Upload an image"
        })
    )
);
```

---

## LinkField

Stores a URL with optional link text and target.

### LinkField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `HintLinkText` | string | `null` | Hint text for the link text input. |
| `LinkTextMode` | LinkTextMode | `Optional` | Link text mode (`Optional`, `Required`, `Static`, `Url`). |
| `UrlPlaceholder` | string | `null` | Placeholder for the URL input. |
| `TextPlaceholder` | string | `null` | Placeholder for the text input. |
| `DefaultUrl` | string | `null` | Default URL value. |
| `DefaultText` | string | `null` | Default link text. |
| `DefaultTarget` | string | `null` | Default target (e.g., `_blank`). |

### LinkField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("LinkField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new LinkFieldSettings
        {
            Required = true,
            LinkTextMode = LinkTextMode.Required,
            UrlPlaceholder = "https://example.com",
            TextPlaceholder = "Click here",
            Hint = "Enter an external link"
        })
    )
);
```

---

## MultiTextField

Stores multiple text values from predefined options.

### MultiTextField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Options` | MultiTextFieldValueOption[] | `[]` | Available options with Name, Value, and Default. |

### MultiTextField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("MultiTextField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new MultiTextFieldSettings
        {
            Options = new[]
            {
                new MultiTextFieldValueOption { Name = "Red", Value = "red", Default = false },
                new MultiTextFieldValueOption { Name = "Green", Value = "green", Default = true },
                new MultiTextFieldValueOption { Name = "Blue", Value = "blue", Default = false }
            },
            Hint = "Select one or more colors"
        })
    )
);
```

---

## UserPickerField

References users.

### UserPickerField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Multiple` | bool | `false` | Whether to allow multiple users. |
| `DisplayAllUsers` | bool | `true` | Whether to display all users. |
| `DisplayedRoles` | string[] | `[]` | Roles to filter displayed users. |
| `Placeholder` | string | `""` | Placeholder text. |

### UserPickerField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("UserPickerField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new UserPickerFieldSettings
        {
            Required = true,
            Multiple = false,
            DisplayAllUsers = false,
            DisplayedRoles = new[] { "Author", "Editor" },
            Hint = "Select an author"
        })
    )
);
```

---

## YoutubeField

Stores a YouTube video URL and embeds the player.

### YoutubeField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `Label` | string | `null` | Label text. |
| `Width` | int | `0` | Embed player width (0 = default). |
| `Height` | int | `0` | Embed player height (0 = default). |
| `Placeholder` | string | `""` | Placeholder text. |

### YoutubeField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("YoutubeField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new YoutubeFieldSettings
        {
            Required = false,
            Width = 640,
            Height = 360,
            Placeholder = "https://www.youtube.com/watch?v=...",
            Hint = "Paste a YouTube video URL"
        })
    )
);
```

---

## TaxonomyField

References taxonomy terms. Provided by the `OrchardCore.Taxonomies` module.

### TaxonomyField Settings

| Setting | Type | Default | Description |
|---|---|---|---|
| `Hint` | string | `null` | Help text displayed below the field. |
| `Required` | bool | `false` | Whether the field is required. |
| `TaxonomyContentItemId` | string | `null` | The content item ID of the taxonomy. |
| `Unique` | bool | `false` | Whether to enforce unique selection. |
| `LeavesOnly` | bool | `false` | Whether to allow only leaf terms (no parents). |
| `Open` | bool | `false` | Whether the taxonomy tree is open by default. |

### TaxonomyField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("TaxonomyField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
        .WithSettings(new TaxonomyFieldSettings
        {
            Required = true,
            TaxonomyContentItemId = "{{TaxonomyContentItemId}}",
            LeavesOnly = true,
            Hint = "Select a category"
        })
    )
);
```

---

## LocalizationSetContentPickerField

References content items by localization set (for multi-lingual content). Provided by `OrchardCore.ContentLocalization`.

### LocalizationSetContentPickerField Migration

```csharp
await _contentDefinitionManager.AlterPartDefinitionAsync("{{PartName}}", part => part
    .WithField("{{FieldName}}", field => field
        .OfType("LocalizationSetContentPickerField")
        .WithDisplayName("{{DisplayName}}")
        .WithPosition("{{Position}}")
    )
);
```

---

## Installing Third-Party Field Modules

Modules that provide custom fields from external sources (CrestApps, Lombiq, or community modules) must be installed as NuGet packages in the **web project** (the startup project of the solution):

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
