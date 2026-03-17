---
name: orchardcore-localization
description: Skill for configuring localization and multi-language support in Orchard Core. Covers culture settings, content localization, PO file translations, and localization configuration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Localization - Prompt Templates

## Configure Localization and Multi-Language Support

You are an Orchard Core expert. Generate localization configuration for multi-language Orchard Core sites.

### Guidelines

- Enable `OrchardCore.Localization` for basic localization support.
- Enable `OrchardCore.ContentLocalization` for content item translation.
- PO files (`.po`) are used for string translations.
- Place PO files in the module's `Localization/` folder.
- Use `IStringLocalizer<T>` in C# code for localizable strings.
- Use `{% t %}` tag in Liquid templates for translations.
- Content localization links translated content items together.
- Culture picker allows users to switch between languages.

### Enabling Localization Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Localization",
        "OrchardCore.ContentLocalization",
        "OrchardCore.ContentLocalization.ContentCulturePicker"
      ],
      "disable": []
    }
  ]
}
```

### Localization Settings via Recipe

```json
{
  "steps": [
    {
      "name": "Settings",
      "LocalizationSettings": {
        "DefaultCulture": "{{DefaultCulture}}",
        "SupportedCultures": [
          "{{Culture1}}",
          "{{Culture2}}",
          "{{Culture3}}"
        ]
      }
    }
  ]
}
```

### PO File Format

Place PO files in `Localization/{culture}.po` (e.g., `Localization/fr.po`):

```po
# French translations
msgid "Hello"
msgstr "Bonjour"

msgid "Welcome to {0}"
msgstr "Bienvenue à {0}"

msgid "Blog Post"
msgstr "Article de blog"

# Context-specific translation
msgctxt "MyModule"
msgid "Title"
msgstr "Titre"
```

### PO File Location Convention

```
MyModule/
├── Localization/
│   ├── fr.po
│   ├── es.po
│   ├── de.po
│   └── ja.po
```

### Using Localization in C# Code

```csharp
using Microsoft.Extensions.Localization;

public sealed class MyController : Controller
{
    private readonly IStringLocalizer S;

    public MyController(IStringLocalizer<MyController> localizer)
    {
        S = localizer;
    }

    public IActionResult Index()
    {
        ViewData["Title"] = S["Welcome to my site"];
        ViewData["Message"] = S["Hello, {0}!", User.Identity.Name];
        return View();
    }
}
```

### Using Localization in Views (Razor)

```cshtml
@inject IViewLocalizer Localizer

<h1>@Localizer["Welcome"]</h1>
<p>@Localizer["This site has {0} articles.", articleCount]</p>
```

### Using Localization in Liquid

```liquid
{% t "Welcome to our site" %}
{% t "Hello, {0}!" User.Identity.Name %}
```

### Content Localization

Content localization connects translated versions of the same content item:

```csharp
// Add LocalizationPart to a content type
_contentDefinitionManager.AlterTypeDefinition("Article", type => type
    .WithPart("LocalizationPart")
);
```

### Culture Picker Widget

Add the culture picker to your layout:

```liquid
{% shape "ContentCulturePicker" %}
```

### Configuring Request Culture Providers

```json
{
  "OrchardCore": {
    "OrchardCore_Localization_CultureProvider": {
      "CookieName": ".AspNetCore.Culture",
      "UseUserOverrideCulture": true
    }
  }
}
```

### Date and Number Formatting

Localized date formatting in Liquid:

```liquid
{{ Model.ContentItem.PublishedUtc | local | date: "%x" }}
{{ Model.ContentItem.PublishedUtc | local | date: "%B %d, %Y" }}
```

### Plural Forms in PO Files

```po
msgid "One item"
msgid_plural "{0} items"
msgstr[0] "Un élément"
msgstr[1] "{0} éléments"
```
