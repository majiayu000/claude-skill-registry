---
name: orchardcore-placement
description: Skill for configuring shape placement in Orchard Core. Covers placement.json files, IShapePlacementProvider, shape alternates, wrappers, and zone/position configuration.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Placement - Prompt Templates

## Configure Shape Placement

You are an Orchard Core expert. Generate placement configuration for Orchard Core shapes.

### Guidelines

- Placement controls where and how shapes are rendered in the layout.
- `placement.json` is the standard way to configure placement in a module or theme.
- Each entry maps a shape type to a zone and position.
- Placement can be scoped by content type, display type, and differentiator.
- The `place` property sets the zone and position (e.g., `"Content:5"`).
- `alternates` adds alternative templates for a shape.
- `wrappers` wraps a shape with additional markup.
- Custom `IShapePlacementProvider` can provide dynamic placement.
- Always seal classes.

### Basic placement.json

```json
{
  "TextField_Edit": [
    {
      "place": "Content:2"
    }
  ],
  "{{PartName}}": [
    {
      "place": "Content:5",
      "alternates": ["{{PartName}}_Summary__{{ContentType}}"]
    }
  ],
  "{{PartName}}_Edit": [
    {
      "place": "Content:5"
    }
  ]
}
```

### Placement Scoped by Content Type

```json
{
  "{{PartName}}": [
    {
      "contentType": ["BlogPost"],
      "place": "Content:after"
    },
    {
      "contentType": ["Article"],
      "place": "Sidebar:5"
    }
  ]
}
```

### Placement Scoped by Display Type

```json
{
  "{{PartName}}": [
    {
      "displayType": "Detail",
      "place": "Content:5"
    },
    {
      "displayType": "Summary",
      "place": "Meta:5"
    },
    {
      "displayType": "SummaryAdmin",
      "place": "Actions:5"
    }
  ]
}
```

### Hiding a Shape

```json
{
  "{{PartName}}": [
    {
      "place": "-"
    }
  ]
}
```

### Using Alternates

```json
{
  "{{PartName}}": [
    {
      "contentType": ["BlogPost"],
      "displayType": "Detail",
      "alternates": ["{{PartName}}__BlogPost"]
    }
  ]
}
```

### Using Wrappers

```json
{
  "{{PartName}}": [
    {
      "place": "Content:5",
      "wrappers": ["{{PartName}}_Wrapper"]
    }
  ]
}
```

### Placement with Differentiator

```json
{
  "TextField": [
    {
      "differentiator": "BlogPost-Subtitle",
      "place": "Content:2"
    },
    {
      "differentiator": "BlogPost-Author",
      "place": "Meta:1"
    }
  ]
}
```

### Custom Shape Placement Provider

```csharp
using OrchardCore.DisplayManagement.Descriptors.ShapePlacementStrategy;

public sealed class {{ProviderName}}PlacementProvider : IShapePlacementProvider
{
    public Task<IPlacementInfoResolver> BuildPlacementInfoResolverAsync(IBuildShapeContext context)
    {
        return Task.FromResult<IPlacementInfoResolver>(new PlacementInfoResolver(context));
    }

    private sealed class PlacementInfoResolver : IPlacementInfoResolver
    {
        private readonly IBuildShapeContext _context;

        public PlacementInfoResolver(IBuildShapeContext context)
        {
            _context = context;
        }

        public PlacementInfo ResolvePlacement(ShapePlacementContext placementContext)
        {
            if (placementContext.ShapeType == "{{ShapeType}}")
            {
                return new PlacementInfo
                {
                    Location = "Content:5",
                };
            }

            return null;
        }
    }
}
```

### Registering Custom Placement Provider

```csharp
using OrchardCore.DisplayManagement.Descriptors.ShapePlacementStrategy;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddScoped<IShapePlacementProvider, {{ProviderName}}PlacementProvider>();
    }
}
```

### Placement Zones Reference

Common zones in Orchard Core themes:

- `Header` — Top of the page.
- `Navigation` — Main navigation area.
- `Content` — Primary content area.
- `Content:before` — Before the content.
- `Content:after` — After the content.
- `Sidebar` — Sidebar area.
- `Footer` — Bottom of the page.
- `Meta` — Metadata area (dates, author, etc.).
- `Tags` — Tags area.
- `Actions` — Action buttons (edit, delete, etc.).
