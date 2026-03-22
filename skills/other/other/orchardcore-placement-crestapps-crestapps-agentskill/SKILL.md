---
name: orchardcore-placement
description: Skill for configuring Orchard Core placement, including placement.json, tabs, cards, columns, alternates, wrappers, dynamic placement providers, and fluent location syntax in display drivers.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.1"
---

# Orchard Core Placement - Prompt Templates

## Configure Orchard Core placement

You are an Orchard Core expert. Generate correct placement for shapes, editor shapes, tabs, cards, columns, and fluent display-driver locations.

### Guidelines

- `placement.json` is the standard way to place shapes in modules and themes.
- Display drivers can also place editor/display shapes with `.Location("...")` or the fluent `PlacementLocationBuilder`.
- Placement can target a zone only, or a zone plus editor groupings such as tabs, cards, and columns.
- For Orchard Core editors that use tabs/cards/columns, the view must render Orchard's grouped output, typically with `@await DisplayAsync(Model.Content)`.
- Use tabs, cards, and columns only when Orchard Core is responsible for rendering the grouped editor UI.
- Keep tab, card, and column names in title case for consistency with Orchard editor grouping conventions.
- Use `-` to hide a shape.
- Use `alternates` to swap templates and `wrappers` to wrap a shape in additional markup.
- Use a custom `IShapePlacementProvider` only when placement must be computed dynamically.
- Always seal classes.

## Placement string format

The placement format supports these segments:

```text
Zone:position#TabName;tabPosition%CardName;cardPosition|ColumnName;columnPosition
```

Every segment after `Zone:position` is optional.

### Segment meanings

- `Zone` - target zone such as `Content`, `Header`, `Meta`, `Actions`, or `Parts`
- `:position` - position within the zone or within the current grouping
- `#TabName;tabPosition` - editor tab name and the tab's ordering position
- `%CardName;cardPosition` - editor card name and the card's ordering position
- `|ColumnName;columnPosition` - editor column name and the column's ordering position

### Important ordering rules

- The separators must appear in this order when combined: `#`, then `%`, then `|`.
- Use `;` before the group position for tabs, cards, and columns.
- Do not use `:` after a tab, card, or column name. `#General:1` creates the literal tab name `General:1`, which is wrong.

### Valid examples

| Placement | Meaning |
| --- | --- |
| `Content:5` | Place the shape in the `Content` zone at position 5 |
| `Content:1#General;1` | Place in the `General` tab |
| `Content:4%Interaction;1` | Place in the `Interaction` card inside `Content` |
| `Content:4#Capabilities;8%Tools;3` | Place in the `Capabilities` tab, then the `Tools` card |
| `Content:4#Capabilities;8%Tools;3|Right;6` | Place in the `Right` column inside the `Tools` card inside the `Capabilities` tab |

## placement.json examples

### Basic placement

```json
{
  "TextField_Edit": [
    {
      "place": "Content:2"
    }
  ],
  "MyPart_Edit": [
    {
      "place": "Content:5"
    }
  ]
}
```

### Cards inside the content editor

```json
{
  "AIProfileGeneralFields_Edit": [
    {
      "place": "Content:1%General;1"
    }
  ],
  "AIProfileDeployment_Edit": [
    {
      "place": "Content:2%Deployments;1"
    }
  ],
  "AIProfileInteractionFields_Edit": [
    {
      "place": "Content:3%Interactions;2"
    }
  ]
}
```

### Tabs and cards together

```json
{
  "MyTools_Edit": [
    {
      "place": "Content:7#Capabilities;8%Tools;3"
    }
  ],
  "MyAgents_Edit": [
    {
      "place": "Content:5#Capabilities;8%Agents;2"
    }
  ]
}
```

### Cards and columns together

```json
{
  "LeftPanel_Edit": [
    {
      "place": "Content:1%Layout;1|Left;1"
    }
  ],
  "RightPanel_Edit": [
    {
      "place": "Content:1%Layout;1|Right;2"
    }
  ]
}
```

### Content type and display type filters

```json
{
  "MyPart": [
    {
      "contentType": ["BlogPost"],
      "displayType": "Detail",
      "place": "Content:5"
    },
    {
      "contentType": ["Article"],
      "displayType": "Summary",
      "place": "Meta:2"
    }
  ]
}
```

### Differentiator, alternates, wrappers, and hide

```json
{
  "TextField": [
    {
      "differentiator": "BlogPost-Subtitle",
      "place": "Content:2"
    }
  ],
  "MyShape": [
    {
      "alternates": ["MyShape__BlogPost"],
      "wrappers": ["MyShape_Wrapper"],
      "place": "Content:5"
    }
  ],
  "SecretShape": [
    {
      "place": "-"
    }
  ]
}
```

## Display driver placement

You can use either the string form or the fluent builder form.

### String form

```csharp
return Initialize<MyViewModel>("MyShape_Edit", model =>
{
    model.Value = value;
})
.Location("Content:4%Interaction;1");
```

### Fluent card placement

```csharp
return Initialize<MyViewModel>("MyShape_Edit", model =>
{
    model.Value = value;
})
.Location(c => c.Zone("Content", "4").Card("Interaction", "1"));
```

### Fluent tab, card, and column placement

```csharp
return Initialize<MyViewModel>("MyShape_Edit", model =>
{
    model.Value = value;
})
.Location(c => c
    .Zone("Content", "4")
    .Tab("Capabilities", "8")
    .Card("Tools", "3")
    .Column("Right", "2"));
```

### Fluent layout zone placement

```csharp
return Initialize<MyViewModel>("MyShape", model =>
{
    model.Value = value;
})
.Location(c => c.Zone("Content", "5").AsLayoutZone());
```

Use `.AsLayoutZone()` when the placement should be treated as a layout zone rather than an editor grouping.

## Custom placement provider

Use an `IShapePlacementProvider` when placement depends on runtime conditions.

```csharp
using OrchardCore.DisplayManagement.Descriptors.ShapePlacementStrategy;

public sealed class MyPlacementProvider : IShapePlacementProvider
{
    public Task<IPlacementInfoResolver> BuildPlacementInfoResolverAsync(IBuildShapeContext context)
    {
        return Task.FromResult<IPlacementInfoResolver>(new Resolver());
    }

    private sealed class Resolver : IPlacementInfoResolver
    {
        public PlacementInfo ResolvePlacement(ShapePlacementContext placementContext)
        {
            if (placementContext.ShapeType == "MyShape")
            {
                return new PlacementInfo
                {
                    Location = "Content:5#General;1%Details;1",
                };
            }

            return null;
        }
    }
}
```

### Registering the provider

```csharp
using OrchardCore.DisplayManagement.Descriptors.ShapePlacementStrategy;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IShapePlacementProvider, MyPlacementProvider>();
    }
}
```

## Orchard Core editor grouping guidance

- Use tabs when you need top-level editor sections.
- Use cards when you need visually grouped fields inside a zone or tab.
- Use columns when a card needs multi-column layout.
- When placing display-driver editor shapes into cards, prefer keeping everything inside the `Content` zone unless Orchard specifically expects another zone.
- In CrestApps-style editors, a card-only placement such as `Content:4%Interaction;1` is valid and preferred over inventing custom zones like `Interaction:10`.

## Common zones

- `Content`
- `Content:before`
- `Content:after`
- `Header`
- `Navigation`
- `Sidebar`
- `Meta`
- `Tags`
- `Actions`
- `Footer`
