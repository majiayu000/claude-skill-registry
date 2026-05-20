---
name: orchardcore-display-management
description: Skill for using Orchard Core's display management system. Covers display drivers, display managers, shapes, display types, shape table providers, placement, and editor/display mode patterns.
license: Apache-2.0
metadata:
  author: CrestApps Team
  version: "1.0"
---

# Orchard Core Display Management - Prompt Templates

## Create Display Drivers and Shapes

You are an Orchard Core expert. Generate display drivers, shapes, and display management code for Orchard Core.

### Guidelines

- Every content part that needs custom rendering requires a `DisplayDriver`.
- Display drivers inherit from `ContentPartDisplayDriver<TPart>`.
- Drivers handle three operations: `Display`, `Edit`, and `Update`.
- Each operation returns `IDisplayResult` (shapes to render).
- View models are used to pass data between drivers and views.
- Shape names follow the convention `{PartName}` for display and `{PartName}_Edit` for editor.
- Use `Initialize<TModel>` to create shapes with a view model.
- Register drivers in `Startup.cs` using `services.AddContentPart<TPart>().UseDisplayDriver<TDriver>()`.
- Always seal classes.

### Content Part Display Driver Pattern

```csharp
using OrchardCore.ContentManagement.Display.ContentDisplay;
using OrchardCore.ContentManagement.Display.Models;
using OrchardCore.DisplayManagement.ModelBinding;
using OrchardCore.DisplayManagement.Views;

public sealed class {{PartName}}DisplayDriver : ContentPartDisplayDriver<{{PartName}}>
{
    public override IDisplayResult Display({{PartName}} part, BuildPartDisplayContext context)
    {
        return Initialize<{{PartName}}ViewModel>("{{PartName}}", model =>
        {
            model.{{PropertyName}} = part.{{PropertyName}};
            model.ContentItem = part.ContentItem;
        })
        .Location("Detail", "Content:5")
        .Location("Summary", "Content:5");
    }

    public override IDisplayResult Edit({{PartName}} part, BuildPartEditorContext context)
    {
        return Initialize<{{PartName}}ViewModel>("{{PartName}}_Edit", model =>
        {
            model.{{PropertyName}} = part.{{PropertyName}};
            model.ContentItem = part.ContentItem;
        });
    }

    public override async Task<IDisplayResult> UpdateAsync({{PartName}} part, UpdatePartEditorContext context)
    {
        var model = new {{PartName}}ViewModel();

        await context.Updater.TryUpdateModelAsync(model, Prefix);

        part.{{PropertyName}} = model.{{PropertyName}};

        return Edit(part, context);
    }
}
```

### View Model Pattern

```csharp
using OrchardCore.ContentManagement;

public class {{PartName}}ViewModel
{
    public string {{PropertyName}} { get; set; }
    public ContentItem ContentItem { get; set; }
}
```

### Display Shape View (Views/{{PartName}}.cshtml)

```cshtml
@model {{Namespace}}.ViewModels.{{PartName}}ViewModel

<p>@Model.{{PropertyName}}</p>
```

### Editor Shape View (Views/{{PartName}}_Edit.cshtml)

```cshtml
@model {{Namespace}}.ViewModels.{{PartName}}ViewModel

<div class="mb-3">
    <label asp-for="{{PropertyName}}" class="form-label">{{DisplayLabel}}</label>
    <input asp-for="{{PropertyName}}" class="form-control" />
    <span asp-validation-for="{{PropertyName}}" class="text-danger"></span>
</div>
```

### Registering a Display Driver

```csharp
using OrchardCore.ContentManagement;
using OrchardCore.ContentManagement.Display.ContentDisplay;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        services.AddContentPart<{{PartName}}>()
            .UseDisplayDriver<{{PartName}}DisplayDriver>();
    }
}
```

### Content Part with Handler Pattern

```csharp
using OrchardCore.ContentManagement;
using OrchardCore.ContentManagement.Handlers;

public sealed class {{PartName}}Handler : ContentPartHandler<{{PartName}}>
{
    public override Task InitializingAsync(InitializingContentContext context, {{PartName}} part)
    {
        part.{{PropertyName}} = "default value";
        return Task.CompletedTask;
    }
}
```

### Display Types

Orchard Core uses display types to differentiate how content is rendered:

- `Detail` — Full content display (e.g., a blog post page).
- `Summary` — Abbreviated display (e.g., in a list).
- `SummaryAdmin` — Admin-specific summary view.
- `Edit` — Editor form for the content part.

### Placing Shapes in Zones

Use `.Location()` to place shapes in zones with positions:

```csharp
return Initialize<MyViewModel>("MyShape", model => { ... })
    .Location("Detail", "Content:5")      // Detail view, Content zone, position 5
    .Location("Summary", "Meta:5")        // Summary view, Meta zone, position 5
    .Location("SummaryAdmin", "Actions:5"); // Admin summary, Actions zone, position 5
```

### Content Field Display Driver

```csharp
using OrchardCore.ContentManagement.Display.ContentDisplay;
using OrchardCore.ContentManagement.Display.Models;

public sealed class {{FieldName}}FieldDisplayDriver : ContentFieldDisplayDriver<{{FieldName}}Field>
{
    public override IDisplayResult Display({{FieldName}}Field field, BuildFieldDisplayContext context)
    {
        return Initialize<{{FieldName}}FieldViewModel>(
            GetDisplayShapeType(context),
            model =>
            {
                model.Field = field;
                model.Part = context.ContentPart;
                model.PartFieldDefinition = context.PartFieldDefinition;
            })
            .Location("Detail", "Content")
            .Location("Summary", "Content");
    }
}
```

### Shape Table Provider

Override shape rendering behavior:

```csharp
using OrchardCore.DisplayManagement.Descriptors;

public sealed class MyShapeTableProvider : IShapeTableProvider
{
    public ValueTask DiscoverAsync(ShapeTableBuilder builder)
    {
        builder.Describe("Content")
            .OnDisplaying(context =>
            {
                // Add alternates, wrappers, etc.
                context.Shape.Metadata.Alternates.Add("Content__{{ContentType}}");
            });

        return ValueTask.CompletedTask;
    }
}
```
