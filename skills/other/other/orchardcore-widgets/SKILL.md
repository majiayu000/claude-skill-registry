---
name: orchardcore-widgets
description: Skill for creating and managing widgets in Orchard Core. Covers widget content types, zones, layers, layer rules, and widget placement configuration.
---

# Orchard Core Widgets - Prompt Templates

## Create and Manage Widgets

You are an Orchard Core expert. Generate widget definitions, layer configurations, and zone placement for Orchard Core.

### Guidelines

- Widgets are content types with the `Widget` stereotype.
- Widgets are placed in zones defined by the theme layout.
- Layers control when widgets are visible using rule expressions.
- Enable `OrchardCore.Widgets` and `OrchardCore.Layers` for widget support.
- Each widget is a content item that can be edited from the admin panel.
- Layer rules use JavaScript-like expressions to control visibility.
- Use `FlowPart` to allow widgets inside content items.

### Enabling Widget Features

```json
{
  "steps": [
    {
      "name": "Feature",
      "enable": [
        "OrchardCore.Widgets",
        "OrchardCore.Layers",
        "OrchardCore.Flows"
      ],
      "disable": []
    }
  ]
}
```

### Creating a Widget Content Type

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
        await _contentDefinitionManager.AlterTypeDefinitionAsync("{{WidgetName}}", type => type
            .DisplayedAs("{{WidgetDisplayName}}")
            .Stereotype("Widget")
            .WithPart("{{WidgetName}}", part => part
                .WithPosition("0")
            )
        );

        await _contentDefinitionManager.AlterPartDefinitionAsync("{{WidgetName}}", part => part
            .WithField("{{FieldName}}", field => field
                .OfType("{{FieldType}}")
                .WithDisplayName("{{FieldDisplayName}}")
                .WithPosition("0")
            )
        );

        return 1;
    }
}
```

### Layer Configuration via Recipe

```json
{
  "steps": [
    {
      "name": "Layers",
      "Layers": [
        {
          "Name": "Always",
          "LayerRule": {
            "Conditions": [
              {
                "Name": "BooleanCondition",
                "Value": true
              }
            ]
          },
          "Description": "Widgets on this layer are always displayed."
        },
        {
          "Name": "Homepage",
          "LayerRule": {
            "Conditions": [
              {
                "Name": "UrlCondition",
                "Value": "^/$"
              }
            ]
          },
          "Description": "Widgets on this layer are displayed on the homepage."
        },
        {
          "Name": "Authenticated",
          "LayerRule": {
            "Conditions": [
              {
                "Name": "IsAuthenticatedCondition",
                "Value": true
              }
            ]
          },
          "Description": "Widgets on this layer are displayed for authenticated users."
        }
      ]
    }
  ]
}
```

### Layer Rule Expressions

Common layer rule conditions:

- `UrlCondition` - Match by URL pattern (regex): `^/$` (homepage), `^/blog/.*` (blog section).
- `IsAuthenticatedCondition` - Visible for authenticated users.
- `IsAnonymousCondition` - Visible for anonymous users.
- `RoleCondition` - Visible for specific roles.
- `CultureCondition` - Visible for specific cultures.
- `BooleanCondition` - Always true/false.
- `JavascriptCondition` - Custom JavaScript expression.

### Placing Widgets in Zones

Widgets are assigned to zones and layers via the admin UI or recipes:

```json
{
  "steps": [
    {
      "name": "Content",
      "data": [
        {
          "ContentItemId": "widget-hero-banner",
          "ContentType": "HeroBanner",
          "DisplayText": "Welcome Banner",
          "Latest": true,
          "Published": true,
          "LayerMetadata": {
            "Layer": "Homepage",
            "Zone": "Header",
            "Position": 0
          },
          "HeroBanner": {
            "Heading": {
              "Text": "Welcome to Our Site"
            },
            "Description": {
              "Html": "<p>Your one-stop solution.</p>"
            }
          }
        }
      ]
    }
  ]
}
```

### Widget Template (Liquid)

Create a template at `Views/Widget-{{WidgetName}}.liquid`:

```liquid
<div class="widget widget-{{ Model.ContentItem.ContentType | downcase }}">
    <h3>{{ Model.ContentItem.Content.{{WidgetName}}.Heading.Text }}</h3>
    <div class="widget-body">
        {{ Model.ContentItem.Content.{{WidgetName}}.Body.Html }}
    </div>
</div>
```

### Widget Template (Razor)

Create a template at `Views/Widget-{{WidgetName}}.cshtml`:

```cshtml
@model OrchardCore.ContentManagement.ContentItem

<div class="widget">
    <h3>@Model.Content.{{WidgetName}}.Heading.Text</h3>
    <div class="widget-body">
        @Html.Raw(Model.Content.{{WidgetName}}.Body.Html)
    </div>
</div>
```

### FlowPart for Inline Widgets

Allow widgets inside content items using `FlowPart`:

```csharp
await _contentDefinitionManager.AlterTypeDefinitionAsync("Page", type => type
    .WithPart("FlowPart")
);
```

FlowPart allows editors to add widgets inline within content item editing.

### Common Built-in Widget Types

- `HtmlWidget` - Renders custom HTML content.
- `LiquidWidget` - Renders Liquid template content.
- `MenuWidget` - Renders a menu.
- `ContainerWidget` - Contains other widgets in a layout.

### Widget Best Practices

- Use the `Widget` stereotype for all widget content types.
- Keep widget templates small and focused.
- Use layer rules to control visibility instead of conditional logic in templates.
- Test widgets across different zones and screen sizes.
- Use `FlowPart` for content-embedded widgets.
