---
name: orchardcore-shapes
description: Skill for working with shapes in Orchard Core's display management system. Covers shape creation, shape templates (Liquid and Razor), shape alternates, shape wrappers, shape metadata, ad-hoc shapes, IShapeFactory usage, IShapeTableProvider, and rendering shapes in Liquid templates.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Shapes - Prompt Templates

## Working with Shapes

You are an Orchard Core expert. Generate shape templates, shape providers, and shape-related code for Orchard Core.

### Guidelines

- Shapes are the fundamental rendering unit in Orchard Core's display management.
- Every piece of visible output is rendered through a shape.
- Shapes have a type name (e.g., `Content`, `Widget`, `TextField`), metadata, and properties.
- Shape templates can be written in Liquid (`.liquid`) or Razor (`.cshtml`).
- Template file names map to shape types using conventions: `Content.liquid`, `Content__BlogPost.liquid`.
- Use double underscore (`__`) in file names to represent the dash (`-`) separator in alternates.
- `IShapeFactory` creates shapes dynamically from code.
- `IShapeTableProvider` customizes shape behavior (alternates, wrappers, bindings).
- `IDisplayManager<T>` orchestrates building and rendering shapes for content.
- Always seal classes.

## How Shapes Work

Shapes are dynamic objects that carry data and metadata for rendering. The rendering pipeline:

1. A **display driver** returns an `IDisplayResult` containing shape descriptors.
2. The **display manager** builds shapes from these descriptors using `IShapeFactory`.
3. **Placement** rules determine where shapes appear (zone and position).
4. The **shape table** resolves which template to use, applying alternates and wrappers.
5. The **template engine** (Liquid or Razor) renders the shape using the resolved template.

### Shape Metadata

Every shape has a `Metadata` property with:

- `Type` — The shape type name (e.g., `Content`, `Widget`).
- `DisplayType` — The display context (e.g., `Detail`, `Summary`).
- `Alternates` — List of alternate shape names to try (most specific first).
- `Wrappers` — List of wrapper shape names to wrap the shape output.
- `Name` — Optional name for referencing the shape.
- `Position` — The position within a zone.
- `Tab` — The editor tab group.
- `PlacementSource` — Where the placement rule came from.

## Creating Shape Templates

### Liquid Shape Template (Views/Content.liquid)

```liquid
<article>
    <header>
        {{ Model.Header | shape_render }}
    </header>

    {{ Model.Content | shape_render }}

    <footer>
        {{ Model.Footer | shape_render }}
    </footer>
</article>
```

### Razor Shape Template (Views/Content.cshtml)

```cshtml
<article>
    <header>
        @await DisplayAsync(Model.Header)
    </header>

    @await DisplayAsync(Model.Content)

    <footer>
        @await DisplayAsync(Model.Footer)
    </footer>
</article>
```

## Shape Alternates

Shape alternates allow more specific templates to override generic ones. Alternates are tried in order from most specific to least specific.

### Alternate Naming Conventions

For a `Content` shape displaying a `BlogPost` content type in `Summary` display type:

| Alternate | File Name (Liquid) | File Name (Razor) |
|---|---|---|
| `Content__BlogPost__Summary` | `Content__BlogPost__Summary.liquid` | `Content-BlogPost.Summary.cshtml` |
| `Content__BlogPost` | `Content__BlogPost.liquid` | `Content-BlogPost.cshtml` |
| `Content__Summary` | `Content__Summary.liquid` | `Content.Summary.cshtml` |
| `Content` (base) | `Content.liquid` | `Content.cshtml` |

### Liquid Template File Naming

In Liquid template file names:
- Use double underscore (`__`) to separate shape type segments.
- Example: `Content__BlogPost.liquid` for the `Content-BlogPost` alternate.
- Example: `Content__BlogPost__Summary.liquid` for `Content-BlogPost-Summary` alternate.
- Example: `Widget__ContainerWidget.liquid` for `Widget-ContainerWidget` alternate.

### Razor Template File Naming

In Razor template file names:
- Use a dot (`.`) to separate display type.
- Use a dash (`-`) to separate content type.
- Example: `Content-BlogPost.cshtml` for content type alternate.
- Example: `Content-BlogPost.Summary.cshtml` for content type + display type alternate.
- Example: `Content.Summary.cshtml` for display type alternate.

## Rendering Shapes in Liquid Templates

### Basic Shape Rendering

```liquid
<!-- Render a shape by name -->
{% shape "ShapeName" %}

<!-- Render a shape with properties -->
{% shape "ShapeName", prop1: "value1", prop2: "value2" %}

<!-- Render a zone (which is a shape containing other shapes) -->
{% zone "Content" %}
{% zone "Header" %}
{% zone "Footer" %}

<!-- Render a shape object using shape_render filter -->
{{ Model.Content | shape_render }}
{{ Model.Header | shape_render }}
```

### Rendering Content Part Shapes in Liquid

```liquid
<!-- Render all shapes in the Content zone -->
{{ Model.Content | shape_render }}

<!-- Render a specific part's shape -->
{{ Model.Content.TitlePart | shape_render }}
{{ Model.Content.HtmlBodyPart | shape_render }}

<!-- Render with a specific display type -->
{% shape "Content", Model: Model.ContentItem, DisplayType: "Summary" %}
```

### Iterating Over Shapes in a Zone

```liquid
{% for item in Model.Content %}
    {{ item | shape_render }}
{% endfor %}
```

### Conditional Shape Rendering in Liquid

```liquid
{% if Model.Content.TitlePart %}
    <h1>{{ Model.Content.TitlePart | shape_render }}</h1>
{% endif %}

{% if Model.Footer %}
    <footer>{{ Model.Footer | shape_render }}</footer>
{% endif %}
```

## Rendering Shapes in Razor Templates

```cshtml
@* Render a zone *@
@await DisplayAsync(Model.Content)
@await DisplayAsync(Model.Header)
@await DisplayAsync(Model.Footer)

@* Render a specific part shape *@
@await DisplayAsync(Model.Content.TitlePart)
@await DisplayAsync(Model.Content.HtmlBodyPart)

@* Create and render an ad-hoc shape *@
@{
    var shape = await New.MyCustomShape(Property1: "value1");
}
@await DisplayAsync(shape)
```

## Creating Shapes from Code

### Using IShapeFactory

```csharp
using OrchardCore.DisplayManagement;

public sealed class MyService
{
    private readonly IShapeFactory _shapeFactory;

    public MyService(IShapeFactory shapeFactory)
    {
        _shapeFactory = shapeFactory;
    }

    public async Task<IShape> CreateCustomShapeAsync()
    {
        // Create a shape that maps to a "MyCustomShape" template
        var shape = await _shapeFactory.CreateAsync("MyCustomShape", Arguments.From(new
        {
            Title = "Hello",
            Description = "World"
        }));

        return shape;
    }
}
```

### Using Initialize in Display Drivers

Display drivers create shapes using `Initialize<TModel>`:

```csharp
public sealed class MyPartDisplayDriver : ContentPartDisplayDriver<MyPart>
{
    public override IDisplayResult Display(MyPart part, BuildPartDisplayContext context)
    {
        return Initialize<MyPartViewModel>("MyPart", model =>
        {
            model.Text = part.Text;
            model.ContentItem = part.ContentItem;
        })
        .Location("Detail", "Content:5")
        .Location("Summary", "Content:5");
    }
}
```

### Combining Multiple Shapes

```csharp
public override IDisplayResult Display(MyPart part, BuildPartDisplayContext context)
{
    return Combine(
        Initialize<MyPartViewModel>("MyPart", model =>
        {
            model.Text = part.Text;
        }).Location("Detail", "Content:5"),

        Initialize<MyPartSummaryViewModel>("MyPart_Summary", model =>
        {
            model.Summary = part.Summary;
        }).Location("Summary", "Content:5"),

        Dynamic("MyPart_Actions")
            .Location("SummaryAdmin", "Actions:5")
    );
}
```

### Ad-Hoc (Dynamic) Shapes

Create shapes without a specific view model:

```csharp
public override IDisplayResult Display(MyPart part, BuildPartDisplayContext context)
{
    return Dynamic("MyPart_Badge", shape =>
    {
        shape.Text = part.BadgeText;
        shape.CssClass = part.IsActive ? "active" : "inactive";
    })
    .Location("Detail", "Meta:5");
}
```

## Shape Table Providers

`IShapeTableProvider` lets you customize shape behavior globally.

### Adding Alternates

```csharp
using OrchardCore.DisplayManagement.Descriptors;

public sealed class ContentShapeTableProvider : IShapeTableProvider
{
    public ValueTask DiscoverAsync(ShapeTableBuilder builder)
    {
        builder.Describe("Content")
            .OnDisplaying(context =>
            {
                var contentType = context.Shape.GetProperty<string>("ContentType");
                var displayType = context.Shape.Metadata.DisplayType;

                if (!string.IsNullOrEmpty(contentType))
                {
                    // Add content-type-specific alternate
                    context.Shape.Metadata.Alternates.Add($"Content__{contentType}");

                    // Add content-type + display-type alternate
                    if (!string.IsNullOrEmpty(displayType))
                    {
                        context.Shape.Metadata.Alternates.Add($"Content__{contentType}__{displayType}");
                    }
                }
            });

        return ValueTask.CompletedTask;
    }
}
```

### Adding Wrappers

```csharp
public sealed class WidgetShapeTableProvider : IShapeTableProvider
{
    public ValueTask DiscoverAsync(ShapeTableBuilder builder)
    {
        builder.Describe("Widget")
            .OnDisplaying(context =>
            {
                // Wrap all widgets with a wrapper template
                context.Shape.Metadata.Wrappers.Add("Widget_Wrapper");
            });

        return ValueTask.CompletedTask;
    }
}
```

### Registering a Shape Table Provider

```csharp
public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IShapeTableProvider, ContentShapeTableProvider>();
    }
}
```

## Shape Wrapper Templates

Wrappers surround a shape's output with additional markup.

### Liquid Wrapper (Views/Widget_Wrapper.liquid)

```liquid
<div class="widget widget-{{ Model.Metadata.Type | downcase }}">
    {{ Model | shape_render }}
</div>
```

### Razor Wrapper (Views/Widget_Wrapper.cshtml)

```cshtml
<div class="widget widget-@Model.Metadata.Type.ToLowerInvariant()">
    @await DisplayAsync(Model)
</div>
```

## Common Shape Types Reference

| Shape Type | Description | Template |
|---|---|---|
| `Content` | Main content item display | `Content.liquid` |
| `Content_Edit` | Content item editor | `Content_Edit.liquid` |
| `Widget` | Widget display wrapper | `Widget.liquid` |
| `Zone` | Layout zone container | `Zone.liquid` |
| `MenuItem` | Menu item rendering | `MenuItem.liquid` |
| `MenuItemLink` | Menu item with link | `MenuItemLink.liquid` |
| `NavigationItem` | Navigation item | `NavigationItem.liquid` |
| `List` | List part container | `List.liquid` |
| `PagerSlim` | Pagination controls | `PagerSlim.liquid` |
| `Pager` | Full pagination | `Pager.liquid` |
| `TextField` | Text field display | `TextField.liquid` |
| `HtmlField` | HTML field display | `HtmlField.liquid` |
| `BooleanField` | Boolean field display | `BooleanField.liquid` |
| `DateTimeField` | DateTime field display | `DateTimeField.liquid` |
| `NumericField` | Numeric field display | `NumericField.liquid` |
| `MediaField` | Media field display | `MediaField.liquid` |
| `ContentPickerField` | Content picker display | `ContentPickerField.liquid` |
| `TaxonomyField` | Taxonomy field display | `TaxonomyField.liquid` |
| `LinkField` | Link field display | `LinkField.liquid` |

## Overriding Built-In Shape Templates

### Override Content Display (Views/Content.liquid)

```liquid
<article class="content-item content-item-{{ Model.ContentItem.ContentType | downcase }}">
    {% if Model.Header %}
        <header>{{ Model.Header | shape_render }}</header>
    {% endif %}

    {% if Model.Meta %}
        <div class="meta">{{ Model.Meta | shape_render }}</div>
    {% endif %}

    {{ Model.Content | shape_render }}

    {% if Model.Footer %}
        <footer>{{ Model.Footer | shape_render }}</footer>
    {% endif %}
</article>
```

### Override Content for Specific Type (Views/Content__BlogPost.liquid)

```liquid
<article class="blog-post">
    <header>
        <h1>{{ Model.ContentItem.DisplayText }}</h1>
        <time datetime="{{ Model.ContentItem.PublishedUtc | date: '%Y-%m-%d' }}">
            {{ Model.ContentItem.PublishedUtc | date: "%B %d, %Y" }}
        </time>
    </header>

    {{ Model.Content | shape_render }}

    {% if Model.Footer %}
        <footer class="post-footer">
            {{ Model.Footer | shape_render }}
        </footer>
    {% endif %}
</article>
```

### Override Widget Wrapper (Views/Widget.liquid)

```liquid
<div class="widget widget-{{ Model.ContentItem.ContentType | downcase }}">
    <div class="widget-body">
        {{ Model.Content | shape_render }}
    </div>
</div>
```

### Override Summary Display (Views/Content__Summary.liquid)

```liquid
<article class="content-summary">
    <h3>
        <a href="{{ Model.ContentItem | display_url }}">
            {{ Model.ContentItem.DisplayText }}
        </a>
    </h3>
    {% if Model.Meta %}
        <div class="meta">{{ Model.Meta | shape_render }}</div>
    {% endif %}
    {{ Model.Content | shape_render }}
</article>
```
